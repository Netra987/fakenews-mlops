# Fake News Detection — MLOps Pipeline

A production-grade MLOps pipeline for detecting fake news using DistilBERT,
with full lifecycle management including data versioning, CI/CD,
drift monitoring, and governance.

**Accuracy: 99.9% | Drift Score: 0.832 | All 6 MLOps Units Covered**

---

## What This Project Does

This system takes any news article as input and predicts whether it is **fake or real**
with a confidence score. Beyond prediction, it monitors itself over time — detecting
when incoming news patterns have drifted so far from training data that the model
needs retraining. This is the core problem MLOps solves.

---

## Project Structure
fakenews-mlops/
├── src/
│   ├── preprocess.py       # Cleans and splits raw CSV data
│   ├── train.py            # Fine-tunes DistilBERT (run on Google Colab)
│   ├── app.py              # FastAPI prediction endpoint
│   ├── simulate_drift.py   # Simulates drifted news data
│   ├── monitor.py          # Generates Evidently AI drift report
│   ├── fairness.py         # Class balance and bias analysis
│   ├── governance.py       # Creates audit trail JSON
│   └── architecture.py     # AWS deployment architecture
├── data/
│   ├── raw/                # Original Kaggle CSVs (DVC tracked)
│   └── processed/          # Cleaned train/test splits (DVC tracked)
├── models/
│   └── saved/              # Trained model files (download from Drive)
├── reports/
│   ├── model_card.md       # Responsible AI documentation
│   ├── fairness_report.json
│   ├── governance_audit.json
│   └── aws_deployment_plan.md
├── tests/
│   └── test_preprocess.py  # CI test suite
├── .github/workflows/
│   └── ci.yml              # GitHub Actions CI pipeline
└── Dockerfile              # Container configuration

---

## Running This Project

### Prerequisites
- Python 3.10
- Git

### Step 1 — Clone the repository
```bash
git clone https://github.com/Netra987/fakenews-mlops.git
cd fakenews-mlops
```

### Step 2 — Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3 — Download the trained model
The model file is 255MB and cannot be stored on GitHub.
It is tracked via DVC and hosted on Google Drive.

1. Download the model folder from: https://drive.google.com/drive/folders/1Gf4ZABfJPIYLUph9tt3cV5vsa3kdAfnl?usp=sharing
2. You will find these 4 files inside:
   - `config.json`
   - `model.safetensors`
   - `tokenizer_config.json`
   - `tokenizer.json`
3. Create this folder in your cloned project: `models/saved/`
4. Place all 4 files inside `models/saved/`

### Step 4 — Run the prediction API
```bash
uvicorn src.app:app --port 8000
```
Open **http://localhost:8000/docs** in your browser.

- Click `POST /predict`
- Click **Try it out**
- Replace the text with any news article
- Click **Execute**
- See the prediction and confidence score

Example input:
```json
{
  "text": "Scientists confirm the earth revolves around the sun according to NASA research."
}
```

Example output:
```json
{
  "prediction": "real",
  "confidence": 0.9991
}
```

### Step 5 — Generate drift monitoring report
```bash
python src\simulate_drift.py
python src\monitor.py
start reports\drift_report.html
```
Opens an interactive HTML dashboard showing data drift detection.
Current drift score: **0.832** — retraining recommended.

### Step 6 — Run governance audit
```bash
python src\fairness.py
python src\governance.py
```
Reports saved to the `reports/` folder.

---

## Architecture
DATA LAYER          TRAINING LAYER      SERVING LAYER
──────────────      ──────────────      ─────────────
Kaggle Dataset  →   Google Colab    →   FastAPI App
DVC Versioning      DistilBERT          Port 8000
MLflow Tracking     /predict endpoint
99.9% Accuracy      Swagger UI
CICD LAYER          MONITORING LAYER    GOVERNANCE LAYER
──────────          ────────────────    ────────────────
GitHub Actions  →   Evidently AI    →   Model Card
Auto Tests          Drift Score 0.832   Fairness Report
Every Push          Retraining Alert    GDPR Audit Trail
CLOUD LAYER
───────────
AWS EC2 t2.micro — ap-south-1 Mumbai
Free Tier — $0/month
CloudWatch Monitoring

---

## Topics Coverage

| Topic | Implementation |
|-------|----------------|
| MLOps Introduction | Full pipeline architecture, responsible AI documentation |
| Data Management | DVC versioning, preprocessing, class balance analysis |
| Training & Deployment | DistilBERT fine-tuning, FastAPI, Docker, GitHub Actions CI/CD |
| Model Monitoring | Evidently AI drift detection dashboard, drift score 0.832 |
| Governance & Compliance | Model card, fairness report, GDPR audit trail |
| MLOps for AWS | EC2 t2.micro architecture, Mumbai region, CloudWatch |

---

## Results

| Metric | Value |
|--------|-------|
| Training accuracy | 99.9% |
| Test accuracy | 99.9% |
| Dataset drift score | 0.832 (high — retraining needed) |
| CI pipeline status | Passing |
| API response time | ~3 seconds per prediction |
| Deployment cost | $0 (AWS free tier) |

---

## Tech Stack

| Category | Tools |
|----------|-------|
| Model | DistilBERT (HuggingFace Transformers) |
| API | FastAPI + Uvicorn |
| Data versioning | DVC |
| Experiment tracking | MLflow |
| CI/CD | GitHub Actions |
| Drift monitoring | Evidently AI |
| Containerization | Docker |
| Cloud | AWS EC2, S3, CloudWatch |
| Language | Python 3.10 |

---

## Key Insight

> Fake news language evolves constantly. A model trained on 2018 news articles
> will gradually fail on 2024 news — not because the code broke, but because
> the world changed. This project demonstrates how MLOps solves exactly this
> problem through continuous monitoring, drift detection, and governance.
