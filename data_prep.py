#!/usr/bin/env python3
"""
Clean raw Reddit data and generate an annotation sample.

Usage:
  python data_prep.py \
    --input reddit_posts.csv \
    --cleaned reddit_posts_clean.csv \
    --sample annotation_sample.csv \
    --sample-size 200
"""

import pandas as pd
import argparse
import re


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw dataframe:
    - Drop duplicate comments per app
    - Filter to ASCII-only (English) text
    - Convert UNIX timestamp to datetime
    - Create a cleaned text column (lowercase, strip URLs/punctuation)
    """
    # Drop duplicates
    df = df.drop_duplicates(subset=["app_name", "comment_id"]).copy()

    # Filter ASCII-only comments
    df = df[df["comment_body"].str.match(r"^[\x00-\x7F]+$", na=False)]

    # Convert timestamp to datetime
    df["datetime"] = pd.to_datetime(df["created_utc"], unit="s")

    # Clean text for NLP
    df["cleaned"] = (
        df["comment_body"]
        .str.lower()
        .str.replace(r"http\S+", "", regex=True)
        .str.replace(r"[^a-z0-9\s]", "", regex=True)
        .str.strip()
    )

    return df


def sample_annotation(df: pd.DataFrame, size: int) -> pd.DataFrame:
    """
    Return a reproducible random sample of the given size.
    """
    return df.sample(n=size, random_state=42)


def main():
    parser = argparse.ArgumentParser(
        description="Clean Reddit data and generate an annotation sample."
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to raw reddit_posts.csv"
    )
    parser.add_argument(
        "--cleaned", required=True,
        help="Path to output cleaned CSV"
    )
    parser.add_argument(
        "--sample", required=True,
        help="Path to output annotation sample CSV"
    )
    parser.add_argument(
        "--sample-size", type=int, default=200,
        help="Number of rows to include in the annotation sample"
    )
    args = parser.parse_args()

    # Load raw data
    df_raw = pd.read_csv(args.input)

    # Clean data
    df_clean = clean_data(df_raw)
    df_clean.to_csv(args.cleaned, index=False)
    print(f"Cleaned data saved to {args.cleaned} (rows: {len(df_clean)})")

    # Generate annotation sample
    df_sample = sample_annotation(df_clean, args.sample_size)
    df_sample.to_csv(args.sample, index=False)
    print(f"Annotation sample ({args.sample_size} rows) saved to {args.sample}")


if __name__ == "__main__":
    main()
