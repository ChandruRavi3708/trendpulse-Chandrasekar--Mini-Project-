import pandas as pd
import numpy as np
import os

# File path
file_path = "data/trends_clean.csv"

# -----------------------------
# 1 — LOAD AND EXPLORE
# -----------------------------

try:
    df = pd.read_csv(file_path)
    print(f"Loaded data: {df.shape}")
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# First 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Average score and comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {int(avg_score)}")
print(f"Average comments: {int(avg_comments)}")

# -----------------------------
# 2 — NUMPY ANALYSIS
# -----------------------------

scores = df["score"].values
comments = df["num_comments"].values

print("\n--- NumPy Stats ---")

# Mean, median, std
print(f"Mean score   : {int(np.mean(scores))}")
print(f"Median score : {int(np.median(scores))}")
print(f"Std deviation: {int(np.std(scores))}")

# Max & Min
print(f"Max score    : {int(np.max(scores))}")
print(f"Min score    : {int(np.min(scores))}")

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Most commented story
max_comments_idx = np.argmax(comments)
top_story_title = df.iloc[max_comments_idx]["title"]
top_story_comments = comments[max_comments_idx]

print(f'\nMost commented story: "{top_story_title}" — {top_story_comments} comments')

# -----------------------------
# 3 — ADD NEW COLUMNS
# -----------------------------

# Engagement = comments / (score + 1)
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# is_popular = True if score > average
df["is_popular"] = df["score"] > avg_score

# -----------------------------
# 4 — SAVE RESULT
# -----------------------------

os.makedirs("data", exist_ok=True)

output_file = "data/trends_analysed.csv"
df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")