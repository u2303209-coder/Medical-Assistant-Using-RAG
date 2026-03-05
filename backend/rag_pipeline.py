import os

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from langchain_groq import ChatGroq


# -------------------------
# CONFIG
# -------------------------

PERSIST_DIRECTORY = "chroma_db"
PDF_DIRECTORY = "documents"

# Add your Groq API Key here
os.environ["GROQ_API_KEY"] = "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"


# -------------------------
# Embedding Model
# -------------------------

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -------------------------
# Build Vector Store
# -------------------------

def build_vectorstore():

    all_documents = []

    for file in os.listdir(PDF_DIRECTORY):

        if file.endswith(".pdf"):

            pdf_path = os.path.join(PDF_DIRECTORY, file)

            loader = PDFPlumberLoader(pdf_path)

            documents = loader.load()

            all_documents.extend(documents)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=300
    )

    texts = text_splitter.split_documents(all_documents)

    vectorstore = Chroma.from_documents(
        texts,
        embedding_model,
        persist_directory=PERSIST_DIRECTORY
    )

    vectorstore.persist()

    return vectorstore


# -------------------------
# Load Existing DB
# -------------------------

if os.path.exists(PERSIST_DIRECTORY):

    vectorstore = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_model
    )

else:

    vectorstore = build_vectorstore()


# -------------------------
# GROQ LLM
# -------------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)


# -------------------------
# Emergency Detection
# -------------------------

def emergency_detect(question):

    emergency_keywords = [
        "can't breathe",
        "severe chest pain",
        "unconscious",
        "bleeding heavily",
        "heart attack",
        "stroke"
    ]

    return any(word in question.lower() for word in emergency_keywords)


# -------------------------
# Prompt Template
# -------------------------

prompt_template = """
You are a responsible medical knowledge assistant.

Use ONLY the provided context to answer the user's question.

Guidelines:

• If the question is about a disease:
Explain symptoms, diagnosis, treatment, and prevention.

• If the question is about first aid or emergency care:
Explain the immediate steps clearly and provide additional care advice.

• If the question is about health advice:
Provide clear and practical guidance.

Important rules:
- Do NOT invent information.
- If the answer is not in the context say:
"I do not have enough information in the medical knowledge base."
- Do NOT diagnose patients or prescribe medications.
- Encourage consulting a healthcare professional when needed.
- Avoid repeating sentences.

Context:
{context}

Question:
{question}

Write a detailed explanation (5-7 sentences).
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)


# -------------------------
# RAG Response
# -------------------------

def get_rag_response(question):

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k":8,
            "fetch_k":15
        }
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
        chain_type_kwargs={"prompt": PROMPT}
    )

    result = qa.invoke({"query": question})

    answer = result["result"]
    source_docs = result["source_documents"]

    sources = set()

    for doc in source_docs:

        source_path = doc.metadata.get("source", "")
        filename = os.path.basename(source_path)

        sources.add(filename)

    return answer.strip(), list(sources)