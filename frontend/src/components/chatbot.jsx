import { useState } from "react";
import { askQuestion } from "../api";

export default function Chatbot() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAsk() {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");

    try {
      const data = await askQuestion(question);
      setAnswer(data.answer);
    } catch (err) {
      setAnswer("Error talking to backend");
    }

    setLoading(false);
  }

  return (
    <div className="chat-container">
      <h2>Enterprise Knowledge AI</h2>

      <textarea
        placeholder="Ask your knowledge base..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={handleAsk} disabled={loading}>
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && (
        <div className="answer-box">
          <strong>Answer:</strong>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}