import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

const COLORS = {
  fake: "#ef4444",
  real: "#22c55e",
};

const ChartsPanel = ({ result }) => {
  if (!result) {
    return (
      <section className="card">
        <h3>Probability Breakdown</h3>
        <p className="empty-state">Charts appear after your first prediction.</p>
      </section>
    );
  }

  const probabilityData = [
    { name: "Fake", value: result.probabilities.fake, color: COLORS.fake },
    { name: "Real", value: result.probabilities.real, color: COLORS.real },
  ];

  const importanceData = result.top_words.map((item) => ({
    word: item.word,
    impact: item.impact,
  }));

  return (
    <section className="charts-grid">
      <div className="card chart-card">
        <h3>Probability Distribution</h3>
        <ResponsiveContainer width="100%" height={240}>
          <PieChart>
            <Pie data={probabilityData} dataKey="value" outerRadius={85} label>
              {probabilityData.map((entry) => (
                <Cell key={entry.name} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip formatter={(value) => `${Math.round(value * 100)}%`} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      <div className="card chart-card">
        <h3>Top Word Impact</h3>
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={importanceData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
            <XAxis dataKey="word" stroke="#cbd5e1" />
            <YAxis stroke="#cbd5e1" />
            <Tooltip />
            <Bar dataKey="impact" fill="#8b5cf6" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
};

export default ChartsPanel;
