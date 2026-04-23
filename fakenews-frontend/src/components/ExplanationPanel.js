const ExplanationPanel = ({ result, inputText }) => {
  if (!result || !result.top_words?.length) {
    return (
      <section className="card">
        <h3>Why this prediction?</h3>
        <p className="empty-state">Influential words will be listed after prediction.</p>
      </section>
    );
  }

  const highlightedText = inputText.split(/\s+/).map((token, index) => {
    const cleanToken = token.toLowerCase().replace(/[^a-z]/g, "");
    const match = result.top_words.find((item) => item.word === cleanToken);
    return (
      <span key={`${token}-${index}`} className={match ? "highlighted-word" : ""}>
        {token}{" "}
      </span>
    );
  });

  return (
    <section className="card">
      <h3>Why this prediction?</h3>
      <div className="chip-row">
        {result.top_words.map((item) => (
          <div key={item.word} className="impact-chip">
            <span>{item.word}</span>
            <strong>{item.impact}</strong>
          </div>
        ))}
      </div>
      <p className="highlighted-text">{highlightedText}</p>
    </section>
  );
};

export default ExplanationPanel;
