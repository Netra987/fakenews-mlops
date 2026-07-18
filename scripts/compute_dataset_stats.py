import json
import os
import re
from collections import Counter
import pandas as pd

STOPWORDS = {
    "this", "that", "with", "from", "have", "were", "they", "their",
    "about", "there", "would", "could", "should", "after", "before",
    "because", "said", "also", "will", "what", "when", "more", "than",
    "been", "says", "where", "some", "into", "your",
}


def main():
    print("Reading train.csv...")
    train = pd.read_csv("data/processed/train.csv").dropna()
    total = len(train)
    fake_count = int((train["label"] == 0).sum())
    real_count = int((train["label"] == 1).sum())
    word_counts = train["text"].apply(lambda t: len(str(t).split()))
    avg_length = round(float(word_counts.mean()), 1)
    print("Computing top words...")
    all_words = []
    for text in train["text"]:
        words = re.findall(r"\b[a-zA-Z]{4,}\b", str(text).lower())
        all_words.extend(w for w in words if w not in STOPWORDS)
    top_words = [w for w, _ in Counter(all_words).most_common(8)]
    stats = {
        "total_articles": total,
        "class_distribution": {
            "fake": {"count": fake_count, "percentage": round(fake_count / total * 100, 1)},
            "real": {"count": real_count, "percentage": round(real_count / total * 100, 1)},
        },
        "avg_article_length_words": avg_length,
        "top_frequent_words": top_words,
    }
    os.makedirs("reports", exist_ok=True)
    with open("reports/dataset_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"Done: {total} articles, {fake_count} fake, {real_count} real")
    print(f"Avg length: {avg_length} words")
    print(f"Top words: {top_words}")
    print("Saved to reports/dataset_stats.json")


if __name__ == "__main__":
    main()