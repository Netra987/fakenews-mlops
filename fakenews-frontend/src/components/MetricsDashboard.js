const MetricsDashboard = ({ history = [] }) => {
  const total = history.length;
  const correct = history.filter((item) => item.isCorrect).length;
  const accuracy = total === 0 ? 0 : correct / total;

  const tp = history.filter((item) => item.prediction === "REAL" && item.expectedLabel === "REAL").length;
  const tn = history.filter((item) => item.prediction === "FAKE" && item.expectedLabel === "FAKE").length;
  const fp = history.filter((item) => item.prediction === "REAL" && item.expectedLabel === "FAKE").length;
  const fn = history.filter((item) => item.prediction === "FAKE" && item.expectedLabel === "REAL").length;

  const precision = tp + fp === 0 ? 0 : tp / (tp + fp);
  const recall = tp + fn === 0 ? 0 : tp / (tp + fn);
  const f1 = precision + recall === 0 ? 0 : (2 * precision * recall) / (precision + recall);

  const rollingWindow = history.slice(-5);
  const rollingCorrect = rollingWindow.filter((item) => item.isCorrect).length;
  const rollingAccuracy = rollingWindow.length === 0 ? 0 : rollingCorrect / rollingWindow.length;

  const metrics = [
    { label: "Accuracy", value: `${Math.round(accuracy * 100)}%` },
    { label: "Precision", value: `${Math.round(precision * 100)}%` },
    { label: "Recall", value: `${Math.round(recall * 100)}%` },
    { label: "F1-score", value: `${Math.round(f1 * 100)}%` },
    { label: "Rolling Accuracy (last 5)", value: `${Math.round(rollingAccuracy * 100)}%` },
  ];

  return (
    <section className="card">
      <h3>Model Metrics</h3>
      <div className="metrics-grid">
        {metrics.map((metric) => (
          <div key={metric.label} className="metric-card">
            <p>{metric.label}</p>
            <strong>{metric.value}</strong>
          </div>
        ))}
      </div>
      <div className="confusion-matrix">
        <p className="muted">Confusion Matrix (simulated ground truth)</p>
        <div className="matrix-grid">
          <div className="matrix-cell">TP: {tp}</div>
          <div className="matrix-cell">FP: {fp}</div>
          <div className="matrix-cell">FN: {fn}</div>
          <div className="matrix-cell">TN: {tn}</div>
        </div>
      </div>
    </section>
  );
};

export default MetricsDashboard;
