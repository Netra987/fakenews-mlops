from fastapi import FastAPI
from pydantic import BaseModel
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

app = FastAPI(title="Fake News Detector")
tokenizer = DistilBertTokenizer.from_pretrained("models/saved")
model = DistilBertForSequenceClassification.from_pretrained("models/saved")
model.eval()

class Article(BaseModel):
    text: str

@app.post("/predict")
def predict(article: Article):
    inputs = tokenizer(article.text, return_tensors="pt", truncation=True, max_length=256, padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits
    pred = logits.argmax(-1).item()
    confidence = torch.softmax(logits, dim=-1).max().item()
    return {"prediction": "real" if pred == 1 else "fake", "confidence": round(confidence, 4)}