"""
Tests for the FastAPI prediction service.

WHY WE MOCK THE MODEL:
The real DistilBERT model is 255MB and lives outside the repo
(DVC + Google Drive). CI can't download it. So we replace the
model loader with a fake that returns predictable outputs.
This lets us test the API's behavior — correct status codes,
correct JSON shape, valid value ranges — without needing real
model weights anywhere.

This is standard practice: unit tests test behavior, not whether
your model is accurate. Model accuracy is tested separately through
your governance_audit.json validation metrics.
"""
import sys
import os
from unittest.mock import patch, MagicMock
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

@pytest.fixture
def client():
    """
    Builds a TestClient with HuggingFace API calls mocked out.
    No model loading needed — we mock the HTTP call to HF Inference API.
    """
    with patch("src.app.hf_requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = [
            [
                {"label": "LABEL_0", "score": 0.05},
                {"label": "LABEL_1", "score": 0.95},
            ]
        ]
        mock_post.return_value = mock_response

        from fastapi.testclient import TestClient
        from src.app import app
        yield TestClient(app)


        


# ─────────────────────────────────────────────
# Tests for POST /predict
# ─────────────────────────────────────────────

def test_predict_returns_200(client):
    """Basic smoke test — does the endpoint respond at all?"""
    response = client.post("/predict", json={"text": "Scientists confirm new findings."})
    assert response.status_code == 200


def test_predict_response_has_all_expected_keys(client):
    """
    Tests the API contract — if you add or rename a field in app.py,
    this test breaks immediately and tells you to update the frontend too.
    """
    response = client.post("/predict", json={"text": "Scientists confirm new findings."})
    data = response.json()
    expected_keys = {
        "prediction",
        "label",
        "confidence",
        "prob_fake",
        "prob_real",
        "probabilities",
        "top_words",
        "model_used",
        "latency_ms",
        "ab_metrics",
    }
    missing = expected_keys - data.keys()
    assert not missing, f"Response missing these keys: {missing}"


def test_predict_confidence_is_between_0_and_1(client):
    """
    Confidence must be a valid probability. If this fails it means
    the softmax output or rounding logic broke.
    """
    response = client.post("/predict", json={"text": "Breaking news from the capital."})
    data = response.json()
    assert 0.0 <= data["confidence"] <= 1.0, (
        f"Confidence {data['confidence']} is outside [0, 1]"
    )


def test_predict_prediction_is_real_or_fake(client):
    """
    prediction must be exactly one of two values — nothing else.
    Catches typos like "Real" instead of "REAL".
    """
    response = client.post("/predict", json={"text": "Local weather expected sunny."})
    data = response.json()
    assert data["prediction"] in ("REAL", "FAKE"), (
        f"Unexpected prediction value: {data['prediction']}"
    )


def test_predict_latency_ms_is_non_negative_integer(client):
    """
    latency_ms must be an int >= 0. Catches unit errors
    (e.g. accidentally returning seconds instead of milliseconds
    which would give a float like 0.144).
    """
    response = client.post("/predict", json={"text": "Some news article text here."})
    data = response.json()
    assert isinstance(data["latency_ms"], int), (
        f"latency_ms should be int, got {type(data['latency_ms'])}"
    )
    assert data["latency_ms"] >= 0


def test_predict_top_words_is_list_of_dicts(client):
    """
    top_words must be a list of dicts with 'word' and 'impact' keys.
    The ExplanationPanel and ChartsPanel in the frontend depend on this shape.
    """
    response = client.post("/predict", json={"text": "Scientists confirmed major discovery today."})
    data = response.json()
    assert isinstance(data["top_words"], list)
    for item in data["top_words"]:
        assert "word" in item, f"top_words item missing 'word' key: {item}"
        assert "impact" in item, f"top_words item missing 'impact' key: {item}"


def test_predict_prob_fake_and_real_sum_to_one(client):
    """
    Softmax probabilities must sum to 1.0 (within floating point tolerance).
    If this fails, the probability calculation in app.py is broken.
    """
    response = client.post("/predict", json={"text": "Government announces new policy."})
    data = response.json()
    total = round(data["prob_fake"] + data["prob_real"], 3)
    assert total == 1.0, f"prob_fake + prob_real = {total}, expected 1.0"


def test_predict_empty_text_does_not_crash(client):
    """
    Empty input should return 200 or 422 (validation error) — never 500.
    A 500 means your code crashed, which is always wrong for a production API.
    """
    response = client.post("/predict", json={"text": ""})
    assert response.status_code in (200, 422), (
        f"Empty text caused a crash: status {response.status_code}"
    )


def test_predict_missing_text_field_returns_422(client):
    """
    Pydantic validation should reject requests with no 'text' field.
    422 = Unprocessable Entity — FastAPI's standard validation error code.
    """
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_predict_model_used_is_a_or_b(client):
    """
    A/B routing should only produce "A" or "B" — nothing else.
    """
    response = client.post("/predict", json={"text": "Election results announced today."})
    data = response.json()
    assert data["model_used"] in ("A", "B"), (
        f"model_used should be A or B, got: {data['model_used']}"
    )


# ─────────────────────────────────────────────
# Tests for GET /metrics
# ─────────────────────────────────────────────

def test_metrics_endpoint_returns_200(client):
    """Prometheus /metrics endpoint must be reachable."""
    response = client.get("/metrics")
    assert response.status_code == 200


def test_metrics_endpoint_contains_fakenews_counters(client):
    """
    Our custom domain metrics must appear in the output.
    If this fails it means the Counter definitions were removed from app.py.
    """
    # Make a prediction first so counters have data
    client.post("/predict", json={"text": "Test article for metrics check."})
    response = client.get("/metrics")
    assert "fakenews_predictions_total" in response.text
    assert "fakenews_model_ab_total" in response.text