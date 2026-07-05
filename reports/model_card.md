# Model Card — Fake News Detector

## Model Details
- **Model type**: DistilBERT fine-tuned for sequence classification
- **Current version**: v3.0
- **Training date**: April 2026
- **Framework**: HuggingFace Transformers

## Intended Use
- Detecting potentially fake or real news articles
- Educational and research purposes — MLOps pipeline demonstration
- Not intended as a sole arbiter of truth (see Limitations)

## Training Data
- Source: Kaggle Fake and Real News Dataset
- Size: 42,826 articles (balanced — 21,413 fake, 21,413 real)
- Labels: 0 = Fake, 1 = Real
- Domain: US political news (2016–2018)
- Reuters dateline signature removed during preprocessing to prevent
  the model from learning source identity instead of content

## Performance
- Training accuracy: 99.9%
- External validation accuracy: 71% (5/7 manually verified samples)
- The gap between training and external accuracy is expected and
  disclosed intentionally — see Limitations

## Limitations
- Trained on US political news only — not validated on satire,
  opinion pieces, or non-English content
- External validation (71%) is meaningfully lower than training
  accuracy (99.9%) — model is overconfident on out-of-distribution text
- Dataset reflects news patterns from 2016–2018 — current news may
  differ enough to require retraining (drift score: 0.832)

## Ethical Considerations
- Should not be used as the sole arbiter of news authenticity
- Human review recommended for borderline predictions — API explicitly
  returns "UNCERTAIN" label below 0.85 confidence for this reason
- Confidence scores always communicated alongside predictions

## Drift Monitoring
- Implemented using Evidently AI (see src/monitor.py)
- Drift score threshold: 0.5
- Last measured drift score on simulated newer data: 0.832
  (retraining recommended)

## Governance
- No personal data used in training or inference
- Dataset publicly available under open license
- GDPR compliant — no user data stored during inference

## Version History
| Version | Key change |
|---|---|
| v1.0 | Initial DistilBERT fine-tune, 5,000 sampled articles |
| v2.0 | Expanded to full 42,826-article balanced dataset |
| v3.0 | Removed Reuters dateline; added dropout 0.3, weight decay 0.01, early stopping |

Full audit trail: see reports/governance_audit.json