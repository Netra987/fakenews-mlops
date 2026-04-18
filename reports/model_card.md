# Model Card — Fake News Detector

## Model Details
- **Model type**: DistilBERT fine-tuned for sequence classification
- **Version**: v1.0
- **Training date**: April 2026
- **Framework**: HuggingFace Transformers

## Intended Use
- Detecting potentially fake or real news articles
- Educational and research purposes
- MLOps pipeline demonstration

## Training Data
- Source: Kaggle Fake and Real News Dataset
- Size: 5,000 articles (sampled)
- Labels: 0 = Fake, 1 = Real
- Domain: US political news (2016–2018)

## Performance
- Accuracy: 99.9% on test set
- Evaluated using stratified train/test split (80/20)

## Limitations
- Trained on US political news only
- May not generalize to satire, opinion, or non-English content
- Dataset reflects news patterns from 2016–2018

## Ethical Considerations
- Model should not be used as sole arbiter of news authenticity
- Human review recommended for borderline predictions
- Confidence scores should be communicated alongside predictions

## Drift Monitoring
- Drift detection implemented using Evidently AI
- Drift score threshold: 0.5
- Current drift score on simulated new data: 0.832 (retraining recommended)

## Governance
- No personal data used in training
- Dataset is publicly available under open license
- GDPR compliant — no user data stored during inference