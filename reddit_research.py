#!/usr/bin/env python3
"""
reddit_research.py

Full script to scrape Reddit posts/comments mentioning our target apps (Wysa, Replika, Calm),
then label comments as “helpful” or “unhelpful” based on community scores.

Requirements:
  pip install praw pandas pyyaml tqdm

Usage:
  1. Create config.yaml with your Reddit API credentials.
  2. python reddit_research.py
"""

import yaml
import praw
import pandas as pd
from tqdm import tqdm

# ----------------------------------------------------------------------------
# 1. Load configuration
# ----------------------------------------------------------------------------
def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

config = load_config()

reddit = praw.Reddit(
    client_id=config['reddit']['client_id'],
    client_secret=config['reddit']['client_secret'],
    user_agent=config['reddit']['user_agent']
)

# ----------------------------------------------------------------------------
# 2. Define target apps and subreddits
# ----------------------------------------------------------------------------
app_subreddits = {
    'Replika': ['Replika'],
    'Wysa':    ['Wysa'],
    'Calm':    ['CalmApp', 'Calm']
}
other_subreddits = ['mentalhealth', 'Anxiety', 'lonely']
MAX_POSTS_PER_SUB = 100

# ----------------------------------------------------------------------------
# 3. Scrape posts and comments
# ----------------------------------------------------------------------------
rows = []
seen_post_ids = set()

def scrape_from_subreddit(app_name, subreddit_name, limit):
    """Scrape hot posts from a specific subreddit."""
    try:
        for post in reddit.subreddit(subreddit_name).hot(limit=limit):
            if post.id in seen_post_ids:
                continue
            seen_post_ids.add(post.id)
            post.comments.replace_more(limit=0)
            for comment in post.comments.list():
                rows.append({
                    'app_name':      app_name,
                    'subreddit':     subreddit_name,
                    'post_id':       post.id,
                    'post_title':    post.title,
                    'post_body':     post.selftext,
                    'comment_id':    comment.id,
                    'comment_body':  comment.body,
                    'comment_score': comment.score,
                    'source':        'Reddit',
                    'created_utc':   comment.created_utc,
                    'author':        str(comment.author)
                })
    except Exception as e:
        print(f"Error scraping r/{subreddit_name}: {e}")

def search_and_scrape(app_name, subreddit_name, query, limit):
    """Search within a subreddit for mentions of the app."""
    try:
        for post in reddit.subreddit(subreddit_name).search(query, limit=limit):
            if post.id in seen_post_ids:
                continue
            seen_post_ids.add(post.id)
            post.comments.replace_more(limit=0)
            for comment in post.comments.list():
                rows.append({
                    'app_name':      app_name,
                    'subreddit':     subreddit_name,
                    'post_id':       post.id,
                    'post_title':    post.title,
                    'post_body':     post.selftext,
                    'comment_id':    comment.id,
                    'comment_body':  comment.body,
                    'comment_score': comment.score,
                    'source':        'Reddit',
                    'created_utc':   comment.created_utc,
                    'author':        str(comment.author)
                })
    except Exception as e:
        print(f"Error searching r/{subreddit_name} for '{query}': {e}")

# Execute scraping
for app, subs in app_subreddits.items():
    print(f"\n=== Scraping priority subreddits for {app} ===")
    for sub in subs:
        scrape_from_subreddit(app, sub, MAX_POSTS_PER_SUB)
    print(f"\n=== Searching other subreddits for {app} ===")
    for sub in other_subreddits:
        search_and_scrape(app, sub, app, MAX_POSTS_PER_SUB)

# ----------------------------------------------------------------------------
# 4. Save raw data
# ----------------------------------------------------------------------------
df = pd.DataFrame(rows)
df.sort_values(['app_name','subreddit','created_utc'], inplace=True)
raw_path = "reddit_posts.csv"
df.to_csv(raw_path, index=False)
print(f"Scraped {len(df)} rows and saved to {raw_path}")

# ----------------------------------------------------------------------------
# 5. Label helpfulness based on comment_score
# ----------------------------------------------------------------------------
# Determine community-based thresholds
high_q = 0.80
low_q  = 0.20
cutoff_high = df['comment_score'].quantile(high_q)
cutoff_low  = df['comment_score'].quantile(low_q)

# Assign labels

def label_helpful(score):
    if score >= cutoff_high:
        return 1    # helpful
    if score <= cutoff_low:
        return 0    # unhelpful
    return None     # neutral

# Apply and filter
df['helpful_label'] = df['comment_score'].apply(label_helpful)
labeled_df = df[df['helpful_label'].notnull()]

# Save labeled data
labeled_path = "reddit_posts_labeled.csv"
labeled_df.to_csv(labeled_path, index=False)
print(f"Labeled data saved to {labeled_path} ({len(labeled_df)} rows)")
labeled_path = "reddit_posts_labeled.csv"
labeled_df.to_csv(labeled_path, index=False)
print(f"Labeled data saved to {labeled_path} ({len(labeled_df)} rows)")