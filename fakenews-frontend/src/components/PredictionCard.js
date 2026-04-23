const PredictionCard = ({ result }) => {
  if (!result) {
    return (
      <section className="card prediction-card">
        <h3>Prediction</h3>
        <p className="empty-state">Submit an article to see prediction details.</p>
      </section>
    );
  }

  const isFake = result.prediction === "FAKE";
  const confidencePct = Math.round(result.confidence * 100);

  return (
    <section className={`card prediction-card ${isFake ? "fake" : "real"}`}>
      <h3>Prediction</h3>
      <p className="prediction-label">{isFake ? "FAKE ❌" : "REAL ✅"}</p>
      <p className="prediction-confidence">{confidencePct}% confidence</p>
      <div className="confidence-meter">
        <div className="confidence-fill" style={{ width: `${confidencePct}%` }} />
      </div>
      <div className="prediction-meta">
        <span>Model {result.model_used}</span>
        <span>{result.latency_ms} ms</span>
      </div>
    </section>
  );
};

export default PredictionCard;
