from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter
from dotenv import load_dotenv
import torch
import time
import time as time_module
import re
import math
import random
import logging
import os
import json as json_module

load_dotenv()

app = FastAPI(title="Fake News Detector")

# CORS — reads from .env locally, from Render env var in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Prometheus instrumentation -------------------------------------------
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

prediction_counter = Counter(
    "fakenews_predictions_total",
    "Total predictions made, labeled by predicted class",
    ["prediction"],
)
low_confidence_counter = Counter(
    "fakenews_low_confidence_total",
    "Total predictions where model was uncertain or low-confidence",
)
ab_model_counter = Counter(
    "fakenews_model_ab_total",
    "Total requests served by each A/B model variant",
    ["model"],
)
# --------------------------------------------------------------------------

SERVICE_START_TIME = time_module.time()
MODEL_VERSION = "v3.0"

# Load model
MODEL_ID = os.getenv("MODEL_ID", "netra05/fakenews-distilbert")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_ID)
model.eval()
device = torch.device("cpu")
model.to(device)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("fakenews-api")

request_history = []
document_frequency = {}
doc_count = 0


class Article(BaseModel):
    text: str


def _safe_label_from_confidence(base_label: str, confidence: float) -> str:
    if confidence > 0.85:
        return base_label
    if 0.6 <= confidence <= 0.85:
        return "UNCERTAIN"
    return "LOW CONFIDENCE"


def extract_top_words(text: str, fake_prob: float, real_prob: float):
    global doc_count

    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    if not words:
        return []

    stop_words = {
        "this", "that", "with", "from", "have", "were", "they", "their",
        "about", "there", "would", "could", "should", "after", "before",
        "because",
    }
    filtered = [word for word in words if word not in stop_words]
    if not filtered:
        filtered = words

    doc_count += 1
    unique_words = set(filtered)
    for token in unique_words:
        document_frequency[token] = document_frequency.get(token, 0) + 1

    frequency = {}
    for word in filtered:
        frequency[word] = frequency.get(word, 0) + 1

    total_terms = sum(frequency.values()) if frequency else 1
    prediction_weight = max(fake_prob, real_prob)
    scored_words = []
    for word, count in frequency.items():
        tf = count / total_terms
        df = document_frequency.get(word, 1)
        idf = math.log((doc_count + 1) / (df + 1)) + 1
        impact = tf * idf * prediction_weight * 10
        scored_words.append({"word": word, "impact": round(impact, 3)})

    scored_words.sort(key=lambda item: item["impact"], reverse=True)
    return scored_words[:5]

@app.get("/health")
def health():
    """
    Liveness check — answers instantly without running inference.
    Used by Render, load balancers, and monitoring tools.
    """
    return {
        "status": "ok",
        "model_version": MODEL_VERSION,
        "model_loaded": model is not None,
        "uptime_seconds": int(time_module.time() - SERVICE_START_TIME),
    }


@app.get("/metrics/summary")
def metrics_summary():
    """
    Aggregates request_history server-side as JSON for the React
    frontend dashboard. Plain JSON — not Prometheus format.
    Survives page refresh since data lives on the server.
    """
    total = len(request_history)
    if total == 0:
        return {
            "total_predictions": 0,
            "avg_confidence": 0.0,
            "fake_pct": 0.0,
            "real_pct": 0.0,
            "avg_latency_ms": 0,
            "model_a_count": 0,
            "model_b_count": 0,
        }
    avg_confidence = sum(item["confidence"] for item in request_history) / total
    fake_count = sum(1 for item in request_history if item["prediction"] == "FAKE")
    avg_latency = sum(item["latency_ms"] for item in request_history) / total
    model_a_count = sum(1 for item in request_history if item["model"] == "A")
    model_b_count = sum(1 for item in request_history if item["model"] == "B")
    return {
        "total_predictions": total,
        "avg_confidence": round(avg_confidence, 4),
        "fake_pct": round((fake_count / total) * 100, 1),
        "real_pct": round(((total - fake_count) / total) * 100, 1),
        "avg_latency_ms": round(avg_latency, 1),
        "model_a_count": model_a_count,
        "model_b_count": model_b_count,
    }


@app.get("/dataset/stats")
def dataset_stats():
    """
    Serves precomputed dataset statistics from reports/dataset_stats.json.
    Generated offline by scripts/compute_dataset_stats.py — not computed
    per-request since train.csv is 92MB.
    """
    stats_path = "reports/dataset_stats.json"
    if not os.path.exists(stats_path):
        return {
            "error": "Dataset stats not yet computed.",
            "fix": "Run: python scripts/compute_dataset_stats.py"
        }
    with open(stats_path, encoding="utf-8") as f:
        return json_module.load(f)

@app.post("/predict")
def predict(article: Article):
    start_time = time.perf_counter()
    inputs = tokenizer(
        article.text,
        return_tensors="pt",
        truncation=True,
        max_length=256,
        padding=True,
    ).to(device)

    with torch.no_grad():
        logits = model(**inputs).logits

    pred = logits.argmax(-1).item()
    probs = torch.softmax(logits, dim=-1).squeeze().tolist()
    fake_prob = float(probs[0])
    real_prob = float(probs[1])
    confidence = max(fake_prob, real_prob)
    base_prediction = "REAL" if pred == 1 else "FAKE"
    label = _safe_label_from_confidence(base_prediction, confidence)
    top_words = extract_top_words(article.text, fake_prob, real_prob)
    model_used = "A" if random.random() < 0.7 else "B"
    latency_ms = int((time.perf_counter() - start_time) * 1000)

    # Prometheus counters
    prediction_counter.labels(prediction=base_prediction).inc()
    ab_model_counter.labels(model=model_used).inc()
    if label in ("UNCERTAIN", "LOW CONFIDENCE"):
        low_confidence_counter.inc()

    request_history.append({
        "model": model_used,
        "latency_ms": latency_ms,
        "confidence": confidence,
        "prediction": base_prediction,
    })

    logger.info(
        "prediction=%s label=%s conf=%.4f model=%s latency_ms=%s",
        base_prediction, label, confidence, model_used, latency_ms,
    )

    return {
        "prediction": base_prediction,
        "label": label,
        "confidence": round(confidence, 4),
        "prob_fake": round(fake_prob, 4),
        "prob_real": round(real_prob, 4),
        "probabilities": {
            "fake": round(fake_prob, 4),
            "real": round(real_prob, 4),
        },
        "top_words": top_words,
        "model_used": model_used,
        "latency_ms": latency_ms,
        "ab_metrics": {
            "total_requests": len(request_history),
            "model_a_count": len([i for i in request_history if i["model"] == "A"]),
            "model_b_count": len([i for i in request_history if i["model"] == "B"]),
        },
    }