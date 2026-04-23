const Sidebar = ({ activeSection, onSectionChange }) => {
  const sections = [
    { id: "analyze", label: "Analyze News", icon: "📝" },
    { id: "dashboard", label: "Dashboard", icon: "📊" },
    { id: "insights", label: "Model Insights", icon: "🧠" },
  ];

  return (
    <aside className="sidebar">
      <h1 className="brand">Fake News MLOps</h1>
      <p className="brand-subtitle">Analytical intelligence platform</p>
      <nav className="sidebar-nav">
        {sections.map((section) => (
          <button
            key={section.id}
            className={`nav-item ${activeSection === section.id ? "active" : ""}`}
            onClick={() => onSectionChange(section.id)}
          >
            <span>{section.icon}</span>
            {section.label}
          </button>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
