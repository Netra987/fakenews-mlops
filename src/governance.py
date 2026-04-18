import pandas as pd, json
from sklearn.metrics import classification_report

df = pd.read_csv("data/processed/test.csv").dropna()
report = classification_report(df["label"], df["label"], output_dict=True)

audit = {
    "model_version": "v1.0",
    "dataset_size": len(df),
    "class_balance": df["label"].value_counts().to_dict(),
    "training_data_source": "Kaggle - Fake and Real News Dataset",
    "known_limitations": "Trained on US political news only. May not generalize to other domains.",
    "gdpr_notes": "No personal data used. Dataset is public domain."
}

with open("reports/governance_audit.json", "w") as f:
    json.dump(audit, f, indent=2)
print("Governance audit saved.")