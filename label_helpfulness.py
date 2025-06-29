#!/usr/bin/env python3
"""
label_helpfulness.py

Label Reddit comments as “helpful” or “unhelpful” based on community upvotes,
using quantile thresholds.

Requirements:
    pip install pandas argparse

Usage:
    python label_helpfulness.py \
      --input reddit_posts_clean.csv \
      --output reddit_posts_labeled.csv \
      --high-q 0.80 \
      --low-q 0.20
"""

import argparse
import pandas as pd

def label_helpful(score: float, high: float, low: float) -> int | None:
    """
    Assign a label based on score:
      - 1 if score >= high threshold
      - 0 if score <= low threshold
      - None otherwise
    """
    if score >= high:
        return 1
    if score <= low:
        return 0
    return None

def main():
    parser = argparse.ArgumentParser(
        description="Label Reddit comments as helpful/unhelpful based on comment_score."
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to cleaned Reddit CSV with 'comment_score' column"
    )
    parser.add_argument(
        "--output", required=True,
        help="Path to write labeled CSV"
    )
    parser.add_argument(
        "--high-q", type=float, default=0.80,
        help="Quantile for helpful threshold (default 0.80)"
    )
    parser.add_argument(
        "--low-q", type=float, default=0.20,
        help="Quantile for unhelpful threshold (default 0.20)"
    )
    args = parser.parse_args()

    # 1. Load data
    df = pd.read_csv(args.input)

    # 2. Compute cutoffs
    cutoff_high = df["comment_score"].quantile(args.high_q)
    cutoff_low  = df["comment_score"].quantile(args.low_q)

    # 3. Label each comment
    df["helpful_label"] = df["comment_score"].apply(
        lambda s: label_helpful(s, cutoff_high, cutoff_low)
    )

    # 4. Filter out neutral (None) labels
    labeled_df = df[df["helpful_label"].notnull()].copy()

    # 5. Save to output CSV
    labeled_df.to_csv(args.output, index=False)
    total = len(labeled_df)
    helpful = int(labeled_df["helpful_label"].sum())
    unhelpful = total - helpful
    print(f"Saved {total} labeled rows to {args.output} "
        f"({helpful} helpful, {unhelpful} unhelpful)")

if __name__ == "__main__":
    main()
