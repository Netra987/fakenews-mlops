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

  const analyzeNews = async () => {
    if (!text.trim()) return;
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/predict", { text });
      setResult(res.data);
      setHistory((prev) => [...prev, res.data]);
      setLastAnalyzedText(text);
      setActiveSection("dashboard");
    } catch (err) {
      console.log(err);
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
            {loading ? "Analyzing..." : "Run Prediction"}
          </button>
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
            <MetricsDashboard />
            <MonitoringPanel history={history} />
          </section>
        )}

        {activeSection === "insights" && (
          <section className="grid-stack">
            <MetricsDashboard />
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