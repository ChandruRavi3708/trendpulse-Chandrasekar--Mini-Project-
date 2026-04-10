import requests
import time
import os
import json
from datetime import datetime

# Base URLs for HackerNews API
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Required header
headers = {"User-Agent": "TrendPulse/1.0"}

# Category keyword mapping
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Store collected stories
collected_stories = []

def fetch_top_story_ids(limit=500):
    """Fetch top story IDs from HackerNews"""
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        response.raise_for_status()
        return response.json()[:limit]
    except Exception as e:
        print(f"Failed to fetch top stories: {e}")
        return []

def fetch_story(story_id):
    """Fetch individual story details"""
    try:
        response = requests.get(ITEM_URL.format(story_id), headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch story {story_id}: {e}")
        return None

def assign_category(title):
    """Assign category based on keywords"""
    if not title:
        return None

    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return None  # Ignore if no category matches

def main():
    story_ids = fetch_top_story_ids()

    # Track count per category
    category_counts = {category: 0 for category in CATEGORIES}

    for category in CATEGORIES:
        print(f"\nProcessing category: {category}")

        for story_id in story_ids:
            if category_counts[category] >= 25:
                break

            story = fetch_story(story_id)

            if not story or "title" not in story:
                continue

            assigned_category = assign_category(story["title"])

            # Only collect if category matches current loop
            if assigned_category == category:
                story_data = {
                    "post_id": story.get("id"),
                    "title": story.get("title"),
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                collected_stories.append(story_data)
                category_counts[category] += 1

        # Sleep AFTER each category loop (important requirement)
        time.sleep(2)

    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # File name with current date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save JSON file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_stories, f, indent=4)

    print(f"\nCollected {len(collected_stories)} stories. Saved to {filename}")


if __name__ == "__main__":
    main()