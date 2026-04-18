import pandas as pd

def test_processed_data_exists():
    df = pd.read_csv("data/processed/train.csv")
    assert len(df) > 0
    assert "label" in df.columns

def test_no_missing_labels():
    df = pd.read_csv("data/processed/train.csv")
    assert df["label"].isnull().sum() == 0

def test_label_values_are_binary():
    df = pd.read_csv("data/processed/train.csv")
    assert set(df["label"].unique()).issubset({0, 1})