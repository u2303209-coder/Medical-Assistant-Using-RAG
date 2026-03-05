from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_pipeline import get_rag_response, emergency_detect

app = Flask(__name__)
CORS(app)

def safety_filter(question):
    risky_words = ["dosage", "prescribe", "treatment plan", "how much medicine", "diagnose me"]
    return any(word in question.lower() for word in risky_words)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data["question"]

    if emergency_detect(question):
        return jsonify({
            "answer": "🚨 This may indicate a medical emergency. Please seek immediate professional medical care."
        })

    if safety_filter(question):
        return jsonify({
            "answer": "⚠ I cannot provide prescriptions or medical treatment advice. Please consult a licensed healthcare professional."
        })

    answer, sources = get_rag_response(question)

    return jsonify({
    "answer": answer,
    "warning": "⚠ This system provides educational information only and is not a substitute for professional medical advice.",
    "sources": sources
})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
