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
  const [history, setHistory] = useState([]);
  const [lastAnalyzedText, setLastAnalyzedText] = useState("");
  const [error, setError] = useState("");

  const getSimulatedTruth = (inputText) => {
    const hash = inputText
      .split("")
      .reduce((sum, char) => sum + char.charCodeAt(0), 0);
    return hash % 2 === 0 ? "REAL" : "FAKE";
  };

  const analyzeNews = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setError("");

    try {
      const res = await axios.post("http://127.0.0.1:8000/predict", { text });
      setResult(res.data);
      const truthLabel = getSimulatedTruth(text);
      setHistory((prev) => [
        ...prev,
        {
          ...res.data,
          expectedLabel: truthLabel,
          isCorrect: res.data.prediction === truthLabel,
        },
      ]);
      setLastAnalyzedText(text);
      setActiveSection("dashboard");
    } catch (err) {
      console.log(err);
      setError("Prediction failed. Please check that backend API is running on port 8000.");
    } finally {
      setLoading(false);
    }
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
            <PredictionCard result={result} />
            <ExplanationPanel result={result} inputText={lastAnalyzedText} />
          </section>
        )}

        {activeSection === "dashboard" && (
          <section className="grid-stack">
            <PredictionCard result={result} />
            <ChartsPanel result={result} />
            <MetricsDashboard history={history} />
            <MonitoringPanel history={history} />
          </section>
        )}

        {activeSection === "insights" && (
          <section className="grid-stack">
            <MetricsDashboard history={history} />
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