import pandas as pd
import json
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("data/processed/test.csv").dropna()

total = len(df)
fake_count = len(df[df["label"] == 0])
real_count = len(df[df["label"] == 1])
fake_pct = round(fake_count / total * 100, 2)
real_pct = round(real_count / total * 100, 2)

fairness = {
    "total_samples": total,
    "class_distribution": {
        "fake_news": {"count": fake_count, "percentage": fake_pct},
        "real_news": {"count": real_count, "percentage": real_pct}
    },
    "bias_assessment": {
        "class_imbalance_detected": abs(fake_pct - real_pct) > 20,
        "imbalance_ratio": round(max(fake_count, real_count) / min(fake_count, real_count), 2),
        "recommendation": "Classes are balanced. No resampling required." if abs(fake_pct - real_pct) < 20 else "Class imbalance detected. Consider resampling."
    },
    "known_biases": [
        "Dataset sourced primarily from US political news outlets",
        "May underperform on satire, opinion pieces, or non-English content",
        "Training data collected up to 2018 — recent news styles may differ"
    ],
    "mitigation_strategies": [
        "Regularly retrain with recent news data",
        "Monitor drift scores monthly using Evidently AI",
        "Expand dataset to include international news sources"
    ]
}

with open("reports/fairness_report.json", "w") as f:
    json.dump(fairness, f, indent=2)

print("Fairness report saved.")
print(f"Class balance — Fake: {fake_pct}%, Real: {real_pct}%")
print(f"Imbalance ratio: {fairness['bias_assessment']['imbalance_ratio']}")