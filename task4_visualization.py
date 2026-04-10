import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# 1 — SETUP
# -----------------------------

file_path = "data/trends_analysed.csv"

try:
    df = pd.read_csv(file_path)
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# Create outputs folder
os.makedirs("outputs", exist_ok=True)

# -----------------------------
# 2 — CHART 1: TOP 10 STORIES
# -----------------------------

# Get top 10 by score
top10 = df.sort_values(by="score", ascending=False).head(10)

# Shorten long titles
top10["short_title"] = top10["title"].apply(
    lambda x: x[:50] + "..." if len(x) > 50 else x
)

plt.figure(figsize=(8, 6))
plt.barh(top10["short_title"], top10["score"], color="skyblue")
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()  # highest on top

plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.close()

# -----------------------------
# 3 — CHART 2: CATEGORY COUNT
# -----------------------------

category_counts = df["category"].value_counts()

plt.figure(figsize=(6, 5))
colors = ["blue", "green", "red", "purple", "orange"]

plt.bar(category_counts.index, category_counts.values, color=colors)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.close()

# -----------------------------
# 4 — CHART 3: SCATTER PLOT
# -----------------------------

plt.figure(figsize=(6, 5))

# Split data based on popularity
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"],
            color="green", label="Popular", alpha=0.6)

plt.scatter(not_popular["score"], not_popular["num_comments"],
            color="red", label="Not Popular", alpha=0.6)

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")
plt.legend()

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.close()

# -----------------------------
# BONUS — DASHBOARD
# -----------------------------

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1 (Top stories)
axes[0].barh(top10["short_title"], top10["score"], color="skyblue")
axes[0].set_title("Top 10 Stories")
axes[0].set_xlabel("Score")
axes[0].invert_yaxis()

# Chart 2 (Categories)
axes[1].bar(category_counts.index, category_counts.values, color=colors)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")

# Chart 3 (Scatter)
axes[2].scatter(popular["score"], popular["num_comments"],
                color="green", label="Popular", alpha=0.6)
axes[2].scatter(not_popular["score"], not_popular["num_comments"],
                color="red", label="Not Popular", alpha=0.6)
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend()

plt.suptitle("TrendPulse Dashboard")

plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.close()

print("All charts saved in outputs/ folder.")