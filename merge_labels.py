#!/usr/bin/env python3
"""
merge_labels.py

Merge the community-derived helpfulness labels into your cleaned dataset.

Usage:
  python merge_labels.py
"""

import pandas as pd

# 1. Load your cleaned and labeled CSVs
clean = pd.read_csv("reddit_posts_clean.csv")
labels = pd.read_csv("reddit_posts_labeled.csv")[["comment_id","helpful_label"]]

# 2. Merge on comment_id
merged = clean.merge(labels, on="comment_id", how="inner")

# 3. Save the merged file
out_path = "reddit_posts_clean_labeled.csv"
merged.to_csv(out_path, index=False)
print(f"Merged data saved to {out_path} ({len(merged)} rows)")
