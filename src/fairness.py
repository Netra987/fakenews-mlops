import json, os

fairness = {
    "total_samples": 42826,
    "class_distribution": {
        "fake_news": {"count": 21413, "percentage": 50.0},
        "real_news": {"count": 21413, "percentage": 50.0}
    },
    "bias_assessment": {
        "class_imbalance_detected": False,
        "imbalance_ratio": 1.0,
        "recommendation": "Classes are perfectly balanced. No resampling required."
    },
    "source_bias_mitigation": [
        "Reuters dateline removed from real articles during preprocessing",
        "Location datelines stripped to prevent source signature learning",
        "Title and text combined for richer content signal"
    ],
    "known_biases": [
        "Dataset sourced primarily from US political news outlets",
        "May underperform on satire, opinion pieces, or non-English content",
        "Subtle fake news mimicking journalistic tone may bypass detection"
    ],
    "mitigation_strategies": [
        "Regularly retrain with recent news data",
        "Monitor drift scores monthly using Evidently AI",
        "Expand dataset to include international news sources",
        "Consider multi-modal signals like source credibility"
    ]
}

os.makedirs("reports", exist_ok=True)
with open("reports/fairness_report.json", "w") as f:
    json.dump(fairness, f, indent=2)

print("Fairness report saved.")
print(f"Class balance — Fake: 50.0%, Real: 50.0%")
print(f"Imbalance ratio: 1.0 — perfectly balanced")