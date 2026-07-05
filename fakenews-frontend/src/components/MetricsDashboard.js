const MetricsDashboard = ({ feedbackHistory = [] }) => {
  const total = feedbackHistory.length;

  if (total === 0) {
    return (
      <section className="card">
        <h3>Model Metrics</h3>
        <p className="empty-state">
          No labeled feedback yet. Click "Actually Real" / "Actually Fake" on a
          prediction to start tracking real accuracy.
        </p>
      </section>
    );
  }

  const correct = feedbackHistory.filter((item) => item.isCorrect).length;
  const accuracy = correct / total;

  const tp = feedbackHistory.filter((i) => i.prediction === "REAL" && i.userLabel === "REAL").length;
  const tn = feedbackHistory.filter((i) => i.prediction === "FAKE" && i.userLabel === "FAKE").length;
  const fp = feedbackHistory.filter((i) => i.prediction === "REAL" && i.userLabel === "FAKE").length;
  const fn = feedbackHistory.filter((i) => i.prediction === "FAKE" && i.userLabel === "REAL").length;

  const precision = tp + fp === 0 ? 0 : tp / (tp + fp);
  const recall = tp + fn === 0 ? 0 : tp / (tp + fn);
  const f1 = precision + recall === 0 ? 0 : (2 * precision * recall) / (precision + recall);

  const rollingWindow = feedbackHistory.slice(-5);
  const rollingAccuracy =
    rollingWindow.filter((i) => i.isCorrect).length / rollingWindow.length;

  const metrics = [
    { label: "Accuracy", value: `${Math.round(accuracy * 100)}%` },
    { label: "Precision", value: `${Math.round(precision * 100)}%` },
    { label: "Recall", value: `${Math.round(recall * 100)}%` },
    { label: "F1-score", value: `${Math.round(f1 * 100)}%` },
    { label: "Rolling Accuracy (last 5)", value: `${Math.round(rollingAccuracy * 100)}%` },
    { label: "Labeled samples", value: total },
  ];

  return (
    <section className="card">
      <h3>Model Metrics</h3>
      <p className="muted" style={{ marginBottom: 12 }}>
        Computed from {total} user-confirmed prediction{total !== 1 ? "s" : ""} — not simulated.
      </p>
      <div className="metrics-grid">
        {metrics.map((metric) => (
          <div key={metric.label} className="metric-card">
            <p>{metric.label}</p>
            <strong>{metric.value}</strong>
          </div>
        ))}
      </div>
      <div className="confusion-matrix">
        <p className="muted">Confusion Matrix (user-confirmed labels)</p>
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