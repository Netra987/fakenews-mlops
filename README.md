# Fake News Detection — MLOps Pipeline

A production-grade MLOps pipeline for detecting fake news using DistilBERT,
with full lifecycle management including data versioning, CI/CD,
drift monitoring, and governance.

## Accuracy: 99.9% | Drift Score: 0.832 | All 6 MLOps Units Covered

## Architecture
- **Model**: DistilBERT fine-tuned on 5,000 news articles
- **API**: FastAPI REST endpoint with Swagger UI
- **Versioning**: DVC for data, MLflow for experiments
- **CI/CD**: GitHub Actions — auto tests on every push
- **Monitoring**: Evidently AI drift detection dashboard
- **Governance**: Model card, fairness report, audit trail
- **Cloud**: AWS EC2 ap-south-1 (Mumbai) deployment ready

## Quick Start
```bash
# Clone and setup
git clone https://github.com/Netra987/fakenews-mlops.git
cd fakenews-mlops
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run API
uvicorn src.app:app --port 8000

# Generate drift report
python src\simulate_drift.py
python src\monitor.py

# Run governance
python src\fairness.py
python src\governance.py
```

## Syllabus Coverage
| Unit | Topic | Implementation |
|------|-------|----------------|
| I | MLOps Introduction | Pipeline architecture, responsible AI |
| II | Data Management | DVC versioning, preprocessing, class balance |
| III | Training & Deployment | DistilBERT, FastAPI, Docker, GitHub Actions |
| IV | Model Monitoring | Evidently AI drift detection (score: 0.832) |
| V | Governance & Compliance | Model card, fairness report, GDPR audit |
| VI | MLOps for AWS | EC2 deployment architecture, Mumbai region |

## Results
- Training accuracy: 99.9%
- Dataset drift detected on new news patterns
- CI pipeline: all tests passing
- API response time: ~3 seconds per prediction