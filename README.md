# Fake News Detection — MLOps Pipeline

**[Live demo](https://fakenews-mlops.vercel.app)** · **[API docs](https://fakenews-mlops.onrender.com/docs)** · **[Model on HuggingFace](https://huggingface.co/netra05/fakenews-distilbert)**

> First prediction after inactivity may take 20–30 seconds — Render free tier sleeps when unused, and the HuggingFace inference model needs to warm up.

A DistilBERT-based fake news classifier with a full MLOps lifecycle — data versioning, CI/CD, live monitoring, drift detection, and governance reporting. Built to understand the gap between a model that works in a notebook and one you can trust in production.

---

## The interesting part: a model that was *too* accurate

The first version hit 99.9% accuracy almost immediately — which should make you suspicious, not happy. Digging into the data, I found that nearly all "real" news articles in the Kaggle dataset carried Reuters datelines (`WASHINGTON (Reuters) -`), while fake ones never did. The model wasn't learning to detect misinformation — it was learning to detect Reuters' writing format.

I stripped datelines during preprocessing and rebalanced classes 50/50. This is documented in `reports/fairness_report.json`. Training accuracy stayed at 99.9% after the fix — but as the external validation shows, that number alone still wasn't telling the whole story.

---

## Architecture

DATA LAYER TRAINING LAYER SERVING LAYER
────────────── ────────────── ─────────────
Kaggle Dataset → Google Colab → FastAPI on Render
DVC Versioning DistilBERT HF Inference API
MLflow Tracking /predict endpoint

CICD LAYER MONITORING LAYER GOVERNANCE LAYER
────────── ──────────────── ────────────────
GitHub Actions → Prometheus → Model Card
Real API Tests Evidently AI Fairness Report
17 tests passing Drift Score 0.83 GDPR Audit Trail


---

## Quick start (local)

```bash
git clone https://github.com/Netra987/fakenews-mlops.git
cd fakenews-mlops
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.app:app --port 8000

cd fakenews-frontend && npm install && npm start
```

---

## Results — the honest version

| Metric | Value |
|---|---|
| Training accuracy | 99.9% |
| External validation accuracy | 71% (5/7 manually verified) |
| Dataset drift score | 0.832 — retraining recommended |
| CI status | Passing — 17 real API tests |
| Live demo | https://fakenews-mlops.vercel.app |

The gap between 99.9% training and 71% external accuracy is the most important number in this table. The model still generalizes imperfectly beyond its training distribution — likely because all data is US political news from 2016–2018. I'm reporting this because hiding it wouldn't make the model better, just the README less honest.

---

## Known limitations

- Trained only on US political news (2016–2018) — performance on other domains, satire, or non-English content is unverified
- External validation (71%) is meaningfully lower than training accuracy (99.9%)
- HuggingFace free inference API returns 50% confidence on first call after inactivity (model cold start) — subsequent calls return real scores
- `request_history` is in-memory only — resets on server restart, not suitable for multi-replica deployments

## What I'd do next

- Move `request_history` to Redis for persistent metrics across restarts
- Retrain on recent news (2024–2026) to address the 0.832 drift score
- Add a second real model variant for genuine A/B testing
- Try a RAG-based fact-checking approach as comparison to pure classification

---

## MLOps coverage

| Topic | Implementation |
|---|---|
| Data Management | DVC versioning, preprocessing, class balance analysis |
| Training | DistilBERT fine-tuning, MLflow experiment tracking |
| Serving | FastAPI, Docker, Render deployment |
| Monitoring | Prometheus live metrics + Evidently AI drift detection |
| Governance | Model card, fairness report, GDPR audit trail |
| CI/CD | GitHub Actions — 17 real API tests with mocked model |
| Frontend | React 19 + Recharts, Vercel deployment |

## Tech stack

| Category | Tools |
|---|---|
| Model | DistilBERT (HuggingFace), hosted on HF Hub |
| API | FastAPI + Uvicorn, deployed on Render |
| Frontend | React 19 + Recharts, deployed on Vercel |
| Data versioning | DVC |
| Experiment tracking | MLflow |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus + Evidently AI |
| Containerization | Docker |