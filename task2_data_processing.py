import pandas as pd
import os

# Path to your JSON file (make sure date matches your file)
file_path = "data/trends_20260410.json"

# 1 — Load JSON file into DataFrame
try:
    df = pd.read_json(file_path)
    print(f"Loaded {len(df)} stories from {file_path}")
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# -----------------------------
# 2 — CLEANING THE DATA
# -----------------------------

# Remove duplicate post_ids
before = len(df)
df = df.drop_duplicates(subset=["post_id"])
print(f"After removing duplicates: {len(df)}")

# Remove rows with missing critical values
before = len(df)
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# Convert score and num_comments to integers
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

# Remove low quality stories (score < 5)
before = len(df)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# Remove extra whitespace in title
df["title"] = df["title"].str.strip()

# -----------------------------
# 3 — SAVE TO CSV
# -----------------------------

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# -----------------------------
# SUMMARY
# -----------------------------

print("\nStories per category:")
print(df["category"].value_counts())