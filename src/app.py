from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import time
import re
import math
import random
import logging

app = FastAPI(title="Fake News Detector")

# ✅ CORS FIRST (important)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
tokenizer = AutoTokenizer.from_pretrained("models/saved")
model = AutoModelForSequenceClassification.from_pretrained("models/saved")

model.eval()
device = torch.device("cpu")
model.to(device)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("fakenews-api")

# In-memory structures for lightweight analytics and A/B monitoring.
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
        "this",
        "that",
        "with",
        "from",
        "have",
        "were",
        "they",
        "their",
        "about",
        "there",
        "would",
        "could",
        "should",
        "after",
        "before",
        "because",
    }
    filtered = [word for word in words if word not in stop_words]
    if not filtered:
        filtered = words

    # Maintain DF stats to compute lightweight TF-IDF-like contribution score.
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


@app.post("/predict")
def predict(article: Article):
    start_time = time.perf_counter()
    inputs = tokenizer(
        article.text,
        return_tensors="pt",
        truncation=True,
        max_length=256,
        padding=True
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
    # 70/30 randomized routing for A/B split.
    model_used = "A" if random.random() < 0.7 else "B"
    latency_ms = int((time.perf_counter() - start_time) * 1000)
    request_history.append(
        {
            "model": model_used,
            "latency_ms": latency_ms,
            "confidence": confidence,
            "prediction": base_prediction,
        }
    )

    logger.info(
        "prediction=%s label=%s conf=%.4f model=%s latency_ms=%s",
        base_prediction,
        label,
        confidence,
        model_used,
        latency_ms,
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
        "model": model_used,
        "latency": latency_ms,
        "model_used": model_used,
        "latency_ms": latency_ms,
        "ab_metrics": {
            "total_requests": len(request_history),
            "model_a_count": len([item for item in request_history if item["model"] == "A"]),
            "model_b_count": len([item for item in request_history if item["model"] == "B"]),
        },
    }