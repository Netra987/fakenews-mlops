import { useState } from "react";
import axios from "axios";
import "./App.css";
import Sidebar from "./components/Sidebar";
import PredictionCard from "./components/PredictionCard";
import ChartsPanel from "./components/ChartsPanel";
import ExplanationPanel from "./components/ExplanationPanel";
import MetricsDashboard from "./components/MetricsDashboard";
import { DatasetInsights, ABTestingPanel, MonitoringPanel } from "./components/InsightsPanels";

function App() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [activeSection, setActiveSection] = useState("analyze");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);          // raw predictions, for A/B + monitoring
  const [feedbackHistory, setFeedbackHistory] = useState([]); // only user-labeled ones
  const [lastAnalyzedText, setLastAnalyzedText] = useState("");
  const [error, setError] = useState("");
  const [currentPredictionId, setCurrentPredictionId] = useState(null);

  const analyzeNews = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError("");

    try {
      const res = await axios.post(
        process.env.REACT_APP_API_URL || "http://127.0.0.1:8000/predict",
        { text }
      );
      const predictionId = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
      setResult({ ...res.data, predictionId });
      setCurrentPredictionId(predictionId);
      setHistory((prev) => [...prev, { ...res.data, predictionId }]);
      setLastAnalyzedText(text);
      setActiveSection("dashboard");
    } catch (err) {
      console.log(err);
      setError("Prediction failed. Please check that backend API is running.");
    } finally {
      setLoading(false);
    }
  };

  // Called when the user clicks 👍/👎 on a prediction.
  const submitFeedback = (userLabel) => {
    if (!result || !currentPredictionId) return;
    setFeedbackHistory((prev) => [
      ...prev,
      {
        predictionId: currentPredictionId,
        text: lastAnalyzedText.slice(0, 60),
        prediction: result.prediction,
        confidence: result.confidence,
        userLabel,
        isCorrect: result.prediction === userLabel,
        timestamp: Date.now(),
      },
    ]);
  };

  return (
    <div className="app-shell">
      <Sidebar activeSection={activeSection} onSectionChange={setActiveSection} />
      <main className="main-content">
        <header className="top-panel">
          <h2>Analyze News Article</h2>
          <p>Paste a news article below to inspect prediction, confidence, and model insights.</p>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste news article text here..."
          />
          <button onClick={analyzeNews} disabled={loading}>
            {loading ? (
              <span className="button-loading">
                <span className="spinner" />
                Analyzing...
              </span>
            ) : (
              "Run Prediction"
            )}
          </button>
          {error && <p className="error-text">{error}</p>}
        </header>

        {activeSection === "analyze" && (
          <section className="grid-stack">
            <PredictionCard
              result={result}
              onFeedback={submitFeedback}
              feedbackGiven={feedbackHistory.some((f) => f.predictionId === currentPredictionId)}
            />
            <ExplanationPanel result={result} inputText={lastAnalyzedText} />
          </section>
        )}

        {activeSection === "dashboard" && (
          <section className="grid-stack">
            <PredictionCard
              result={result}
              onFeedback={submitFeedback}
              feedbackGiven={feedbackHistory.some((f) => f.predictionId === currentPredictionId)}
            />
            <ChartsPanel result={result} />
            <MetricsDashboard feedbackHistory={feedbackHistory} />
            <MonitoringPanel history={history} />
          </section>
        )}

        {activeSection === "insights" && (
          <section className="grid-stack">
            <MetricsDashboard feedbackHistory={feedbackHistory} />
            <DatasetInsights />
            <ABTestingPanel history={history} />
            <MonitoringPanel history={history} />
          </section>
        )}
      </main>
    </div>
  );
}

export default App;