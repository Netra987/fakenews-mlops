import pandas as pd
import os
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

reference = pd.read_csv("data/processed/test.csv").dropna()
current = pd.read_csv("data/processed/drifted.csv").dropna()

reference = reference[["text", "label"]]
current = current[["text", "label"]]

report = Report(metrics=[DataDriftPreset()])
report.run(reference_data=reference, current_data=current)

os.makedirs("reports", exist_ok=True)
report.save_html("reports/drift_report.html")
print("Drift report saved to reports/drift_report.html")