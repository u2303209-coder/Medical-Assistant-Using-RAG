import React, { useState } from "react";
import "./App.css";

function App() {

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {

    if (!question.trim()) return;

    const newMessages = [
      ...messages,
      { type: "user", text: question }
    ];

    setMessages(newMessages);
    setLoading(true);

    const response = await fetch("http://127.0.0.1:5000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ question })
    });

    const data = await response.json();

    setMessages([
  ...newMessages,
  {
    type: "assistant",
    text: data.answer,
    warning: data.warning,
    sources: data.sources
  }
]);

    setQuestion("");
    setLoading(false);
  };

  return (
    <div className="app">

      <h1>🩺 AskMed AI</h1>

      <div className="chat">

        {messages.map((msg, index) => (

          <div key={index} className={msg.type}>

            <div className="bubble">
  {msg.text}

  {msg.warning && (
    <div className="warning">
      {msg.warning}
    </div>
  )}
</div>

            {msg.sources && (
              <div className="sources">
                Sources: {msg.sources.join(", ")}
              </div>
            )}

          </div>

        ))}

        {loading && <div className="assistant">Thinking...</div>}

      </div>

      <div className="inputBox">

        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a medical question..."
        />

        <button onClick={askQuestion}>
          Ask
        </button>

      </div>

    </div>
  );
}

export default App;