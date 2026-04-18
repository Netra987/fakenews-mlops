architecture = """
╔══════════════════════════════════════════════════════════════╗
║           FAKE NEWS DETECTION — MLOPS ARCHITECTURE           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  DATA LAYER          TRAINING LAYER      SERVING LAYER       ║
║  ─────────────       ──────────────      ────────────        ║
║  Kaggle Dataset  →   Google Colab    →   FastAPI App         ║
║  DVC Versioning      DistilBERT          Docker Container    ║
║  data/raw/           MLflow Tracking     Port 8000           ║
║  data/processed/     99.9% Accuracy      /predict endpoint   ║
║                                                              ║
║  CICD LAYER          MONITORING LAYER    GOVERNANCE LAYER    ║
║  ──────────          ───────────────     ────────────────    ║
║  GitHub Actions  →   Evidently AI    →   Model Card         ║
║  Auto Tests          Drift Detection     Fairness Report     ║
║  On Every Push       Drift Score: 0.83   Audit Trail        ║
║                      Alerts Triggered    GDPR Compliant      ║
║                                                              ║
║  CLOUD LAYER                                                 ║
║  ───────────                                                 ║
║  AWS ap-south-1 (Mumbai)                                     ║
║  EC2 t2.micro — Free Tier                                    ║
║  CloudWatch Monitoring                                       ║
╚══════════════════════════════════════════════════════════════╝
"""

print(architecture)

with open("reports/architecture.txt", "w") as f:
    f.write(architecture)
print("Architecture saved to reports/architecture.txt")