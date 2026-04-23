import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [chat, setChat] = useState([]);

  // ✅ FIX: helper delay function
  const delay = (ms) => new Promise((res) => setTimeout(res, ms));

  const analyzeNews = async () => {
    if (!text.trim()) return;

    const userMessage = { role: "user", text };
    setChat((prev) => [...prev, userMessage]);

    setText("");
    setLoading(true);

    try {
      // ✅ FIX: ensures "Thinking..." stays visible
      const [res] = await Promise.all([
        axios.post("http://127.0.0.1:8000/predict", {
          text,
        }),
        delay(1200), // 👈 minimum AI thinking time
      ]);

      const botMessage = {
        role: "bot",
        text: res.data.prediction,
        confidence: res.data.confidence,
      };

      setChat((prev) => [...prev, botMessage]);
    } catch (err) {
      console.log(err);
    }

    setLoading(false);
  };

  return (
    <div className="container">

      {/* SIDEBAR DASHBOARD */}
      <div className="sidebar">
        <h2>🧠 Fake News AI</h2>

        <div className="card">
          <h3>Model</h3>
          <p>DistilBERT</p>
        </div>

        <div className="card">
          <h3>Accuracy</h3>
          <p>94%</p>
        </div>

        <div className="card">
          <h3>Status</h3>
          <p className="online">Online</p>
        </div>
      </div>

      {/* CHAT AREA */}
      <div className="chat">

        <div className="chatBox">
          {chat.map((msg, i) => (
            <motion.div
              key={i}
              className={`msg ${msg.role}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
            >
              {msg.role === "user" ? (
                <p>🧑 {msg.text}</p>
              ) : (
                <div className={`resultBadge ${msg.text}`}>
                  <span className="label">
                    🤖 {msg.text.toUpperCase()}
                  </span>

                  <span className="confidence">
                    {Math.round(msg.confidence * 100)}% confidence
                  </span>
                </div>
              )}
            </motion.div>
          ))}

          {loading && (
            <motion.div
              className="msg bot"
              animate={{ opacity: [0.3, 1, 0.3] }}
              transition={{ repeat: Infinity, duration: 1 }}
            >
              🤖 Thinking...
            </motion.div>
          )}
        </div>

        <div className="inputBox">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste news article..."
          />

          <button onClick={analyzeNews}>
            Analyze
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;