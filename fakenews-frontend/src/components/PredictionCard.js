const PredictionCard = ({ result, onFeedback, feedbackGiven }) => {
  if (!result) {
    return (
      <section className="card prediction-card">
        <h3>Prediction</h3>
        <p className="empty-state">Submit an article to see prediction details.</p>
      </section>
    );
  }

  const isFake = result.prediction === "FAKE";
  const isUncertain = result.label === "UNCERTAIN" || result.label === "LOW CONFIDENCE";
  const confidencePct = Math.round(result.confidence * 100);
  const dominant = result.prob_fake > result.prob_real ? "fake" : "real";
  const confidenceClass = isUncertain ? "uncertain" : dominant;

  return (
    <section className={`card prediction-card ${isFake ? "fake" : "real"}`}>
      <h3>Prediction</h3>
      <p className="prediction-label">
        {result.label === "UNCERTAIN" && "UNCERTAIN"}
        {result.label === "LOW CONFIDENCE" && "LOW CONFIDENCE"}
        {result.label !== "UNCERTAIN" && result.label !== "LOW CONFIDENCE" && (isFake ? "FAKE" : "REAL")}
      </p>
      <p className="prediction-confidence">{confidencePct}% confidence</p>
      <div className="confidence-meter">
        <div className={`confidence-fill ${confidenceClass}`} style={{ width: `${confidencePct}%` }} />
      </div>
      <p className="probability-line">
        Fake: {Math.round(result.prob_fake * 100)}% | Real: {Math.round(result.prob_real * 100)}%
      </p>
      <div className="prediction-meta">
        <span>Model {result.model_used}</span>
        <span>{result.latency_ms} ms</span>
      </div>

      <div className="feedback-row">
        {feedbackGiven ? (
          <p className="muted">Thanks — feedback recorded for this prediction.</p>
        ) : (
          <>
            <p className="muted">Was this correct?</p>
            <button className="feedback-btn real" onClick={() => onFeedback("REAL")}>
              Actually Real
            </button>
            <button className="feedback-btn fake" onClick={() => onFeedback("FAKE")}>
              Actually Fake
            </button>
          </>
        )}
      </div>
    </section>
  );
};

export default PredictionCard;