architecture = """
╔══════════════════════════════════════════════════════════════╗
║           FAKE NEWS DETECTION — MLOPS ARCHITECTURE           ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  DATA LAYER          TRAINING LAYER      SERVING LAYER       ║
║  ─────────────       ──────────────      ────────────        ║
║  Kaggle Dataset  →   Google Colab    →   FastAPI on Render   ║
║  DVC Versioning      DistilBERT          HF Inference API    ║
║  data/raw/           MLflow Tracking     /predict endpoint   ║
║  data/processed/     99.9% Accuracy      Swagger UI          ║
║                                                              ║
║  CICD LAYER          MONITORING LAYER    GOVERNANCE LAYER    ║
║  ──────────          ───────────────     ────────────────    ║
║  GitHub Actions  →   Prometheus      →   Model Card         ║
║  17 Real Tests       Evidently AI        Fairness Report     ║
║  On Every Push       Drift Score: 0.83   GDPR Compliant      ║
║                                                              ║
║  FRONTEND LAYER                                              ║
║  ───────────────                                             ║
║  React 19 + Recharts                                         ║
║  Deployed on Vercel                                          ║
║  fakenews-mlops.vercel.app                                   ║
╚══════════════════════════════════════════════════════════════╝
"""

print(architecture)

with open("reports/architecture.txt", "w") as f:
    f.write(architecture)
print("Architecture saved to reports/architecture.txt")