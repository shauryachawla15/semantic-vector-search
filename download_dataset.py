# download_dataset.py
import os
from sklearn.datasets import fetch_20newsgroups

# Paths
DATA_DIR = "data/docs"

os.makedirs(DATA_DIR, exist_ok=True)

print("Downloading dataset...")
dataset = fetch_20newsgroups(subset='train')

print("Saving documents...")
for i, text in enumerate(dataset.data[:200]):  # limit to 200 files
    file_path = os.path.join(DATA_DIR, f"doc_{i:04d}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)

print(f"Saved {min(200, len(dataset.data))} documents to {DATA_DIR}")
