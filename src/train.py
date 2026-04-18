import mlflow, mlflow.sklearn
import pandas as pd
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
from sklearn.metrics import accuracy_score

mlflow.set_experiment("fakenews-detection")

train_df = pd.read_csv("data/processed/train.csv").dropna()
test_df  = pd.read_csv("data/processed/test.csv").dropna()

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

def tokenize(batch):
    return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=256)

train_ds = Dataset.from_pandas(train_df).map(tokenize, batched=True)
test_ds  = Dataset.from_pandas(test_df).map(tokenize, batched=True)
train_ds = train_ds.rename_column("label","labels").with_format("torch")
test_ds  = test_ds.rename_column("label","labels").with_format("torch")

model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)

args = TrainingArguments("models/distilbert-run", num_train_epochs=2, per_device_train_batch_size=16, evaluation_strategy="epoch", save_strategy="epoch", load_best_model_at_end=True)

def compute_metrics(p):
    preds = p.predictions.argmax(-1)
    return {"accuracy": accuracy_score(p.label_ids, preds)}

with mlflow.start_run():
    mlflow.log_params({"model":"distilbert-base-uncased","epochs":2,"batch_size":16})
    trainer = Trainer(model=model, args=args, train_dataset=train_ds, eval_dataset=test_ds, compute_metrics=compute_metrics)
    trainer.train()
    results = trainer.evaluate()
    mlflow.log_metrics(results)
    model.save_pretrained("models/saved")
    tokenizer.save_pretrained("models/saved")
    print("Done. Accuracy:", results["eval_accuracy"])