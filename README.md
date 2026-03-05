# 🩺 AskMed AI – Medical Knowledge Assistant (RAG)

AskMed AI is a medical question-answering system built using Retrieval-Augmented Generation (RAG).
It retrieves information from trusted medical documents and generates answers using an AI model.

⚠ This system is for educational purposes only and does not replace professional medical advice.


#  Project Description

This project demonstrates how AI can provide reliable medical information while following responsible AI practices.

Instead of generating answers directly from a language model, the system:

1. Retrieves relevant information from medical documents.
2. Uses an AI model to generate an answer based on that information.
3. Displays the source of the information.

Safety features such as emergency detection and medical disclaimers are included to reduce misuse.



 # Technologies 
 # Frontend

* React.js
* CSS

# Backend

* Python
* Flask
* Flask-CORS

# AI / RAG System

* LangChain
* ChromaDB (Vector Database)
* HuggingFace Embeddings
* Groq LLM

# Document Processing

* PDFPlumber
* Recursive Text Splitter



#  Features

Medical question-answering chatbot
Retrieval-Augmented Generation (RAG)
Answers generated from medical documents
Source documents displayed for transparency
Safety filter for medical prescriptions and diagnosis
Emergency detection system
Medical disclaimer included in responses
Interactive chat-style UI

---


#  Project Structure

```
Responsible_Medical_RAG_Project
│
├── backend
│   ├── app.py
│   ├── rag_pipeline.py
│   ├── requirements.txt
│   ├── documents/
│   └── chroma_db/
│
├── frontend
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   ├── public/
│   └── package.json
│
└── README.md
```

---



# Clone the Repository

```
git clone https://github.com/yourusername/AskMed-AI.git
cd AskMed-AI
```

---

# Run Backend

```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend runs on:

```
http://127.0.0.1:5000
```

---

#  Run Frontend

```
cd frontend
npm install
npm start
```

Frontend runs on:

```
http://localhost:3000
```

#  Responsible AI Notice

This system:

* Does not provide prescriptions
* Does not diagnose diseases
* Encourages consulting healthcare professionals

It is designed only to provide educational medical information.


#  Author

I built an  AI project which demonstrates Responsible Medical Knowledge Retrieval using RAG.
