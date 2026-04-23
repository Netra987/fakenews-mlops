const MetricsDashboard = () => {
  const metrics = [
    { label: "Accuracy", value: "99.9%" },
    { label: "Precision", value: "99.4%" },
    { label: "Recall", value: "99.1%" },
    { label: "F1-score", value: "99.2%" },
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
    </section>
  );
};

export default MetricsDashboard;
