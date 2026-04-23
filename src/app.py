from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import time
import re

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

class Article(BaseModel):
    text: str


def extract_top_words(text: str, fake_prob: float, real_prob: float):
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

    frequency = {}
    for word in filtered:
        frequency[word] = frequency.get(word, 0) + 1

    max_freq = max(frequency.values()) if frequency else 1
    prediction_weight = max(fake_prob, real_prob)
    scored_words = [
        {
            "word": word,
            "impact": round((count / max_freq) * prediction_weight, 3),
        }
        for word, count in frequency.items()
    ]
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
    top_words = extract_top_words(article.text, fake_prob, real_prob)
    model_used = "A" if sum(ord(char) for char in article.text) % 2 == 0 else "B"
    latency_ms = int((time.perf_counter() - start_time) * 1000)

    return {
        "prediction": "REAL" if pred == 1 else "FAKE",
        "confidence": round(confidence, 4),
        "probabilities": {
            "fake": round(fake_prob, 4),
            "real": round(real_prob, 4),
        },
        "top_words": top_words,
        "model_used": model_used,
        "latency_ms": latency_ms,
    }