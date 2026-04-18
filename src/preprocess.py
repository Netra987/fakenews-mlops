import pandas as pd
from sklearn.model_selection import train_test_split

fake = pd.read_csv("data/raw/Fake.csv")
real = pd.read_csv("data/raw/True.csv")
fake["label"] = 0
real["label"] = 1
df = pd.concat([fake, real]).sample(frac=1, random_state=42).reset_index(drop=True)
df = df[["title", "text", "label"]]
train, test = train_test_split(df, test_size=0.2, stratify=df["label"], random_state=42)
train.to_csv("data/processed/train.csv", index=False)
test.to_csv("data/processed/test.csv", index=False)
print(f"Train: {len(train)}, Test: {len(test)}")