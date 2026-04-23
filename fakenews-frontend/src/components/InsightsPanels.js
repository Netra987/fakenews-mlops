import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

export const DatasetInsights = () => {
  const distribution = [
    { label: "Fake", count: 5200 },
    { label: "Real", count: 4800 },
  ];

  const frequentWords = ["breaking", "official", "claim", "viral", "report", "source"];

  return (
    <section className="card">
      <h3>Dataset Insights</h3>
      <div className="two-col">
        <div>
          <p className="muted">Class distribution and article statistics</p>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={distribution}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="label" stroke="#cbd5e1" />
              <YAxis stroke="#cbd5e1" />
              <Tooltip />
              <Bar dataKey="count" fill="#06b6d4" />
            </BarChart>
          </ResponsiveContainer>
          <p className="muted">Average article length: 412 words</p>
        </div>
        <div>
          <p className="muted">Top frequent words</p>
          <div className="chip-row">
            {frequentWords.map((word) => (
              <span key={word} className="impact-chip">
                {word}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export const ABTestingPanel = ({ history }) => {
  const modelA = history.filter((item) => (item.model || item.model_used) === "A").length;
  const modelB = history.filter((item) => (item.model || item.model_used) === "B").length;
  const total = history.length || 1;
  const usageA = Math.round((modelA / total) * 100);
  const usageB = Math.round((modelB / total) * 100);
  const avgLatencyA =
    modelA === 0
      ? 0
      : Math.round(
          history
            .filter((item) => (item.model || item.model_used) === "A")
            .reduce((sum, item) => sum + (item.latency ?? item.latency_ms ?? 0), 0) / modelA
        );
  const avgLatencyB =
    modelB === 0
      ? 0
      : Math.round(
          history
            .filter((item) => (item.model || item.model_used) === "B")
            .reduce((sum, item) => sum + (item.latency ?? item.latency_ms ?? 0), 0) / modelB
        );

  return (
    <section className="card">
      <h3>A/B Testing Insights</h3>
      <div className="metrics-grid">
        <div className="metric-card">
          <p>Model A Usage</p>
          <strong>{usageA}%</strong>
        </div>
        <div className="metric-card">
          <p>Model B Usage</p>
          <strong>{usageB}%</strong>
        </div>
        <div className="metric-card">
          <p>Model A Latency</p>
          <strong>{avgLatencyA} ms</strong>
        </div>
        <div className="metric-card">
          <p>Model B Latency</p>
          <strong>{avgLatencyB} ms</strong>
        </div>
      </div>
    </section>
  );
};

export const MonitoringPanel = ({ history }) => {
  const total = history.length;
  const avgConfidence =
    total === 0 ? 0 : Math.round((history.reduce((sum, item) => sum + item.confidence, 0) / total) * 100);
  const fakePct =
    total === 0
      ? 0
      : Math.round((history.filter((item) => item.prediction === "FAKE").length / total) * 100);

  return (
    <section className="card">
      <h3>Monitoring</h3>
      <div className="metrics-grid">
        <div className="metric-card">
          <p>Total Predictions</p>
          <strong>{total}</strong>
        </div>
        <div className="metric-card">
          <p>Average Confidence</p>
          <strong>{avgConfidence}%</strong>
        </div>
        <div className="metric-card">
          <p>Fake Detected</p>
          <strong>{fakePct}%</strong>
        </div>
      </div>
      <div className="recent-history">
        <p className="muted">Last 5 predictions</p>
        {history.slice(-5).reverse().map((item, index) => (
          <div key={`${item.prediction}-${index}`} className="history-item">
            <span>{item.label || item.prediction}</span>
            <span>{Math.round(item.confidence * 100)}%</span>
            <span>Model {item.model || item.model_used}</span>
          </div>
        ))}
      </div>
    </section>
  );
};
