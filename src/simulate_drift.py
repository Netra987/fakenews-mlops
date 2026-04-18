import pandas as pd, numpy as np

ref = pd.read_csv("data/processed/test.csv")
drifted = ref.copy()
drifted["text"] = drifted["text"].apply(lambda x: x + " breaking exclusive leaked sources confirm")
drifted["label"] = np.random.choice([0,1], size=len(drifted))
drifted.to_csv("data/processed/drifted.csv", index=False)
print("Drifted dataset created")