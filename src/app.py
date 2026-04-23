from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

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

@app.post("/predict")
def predict(article: Article):
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
    confidence = torch.softmax(logits, dim=-1).max().item()

    return {
        "prediction": "real" if pred == 1 else "fake",
        "confidence": round(confidence, 4)
    }