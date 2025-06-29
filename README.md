# 🗂️ Data Collection & Preprocessing Pipeline

This repository is part of our ET6 Collaborative Data Science Project on digital mental health support. It provides scripts to scrape, clean, and label Reddit comments for three target apps: **Wysa**, **Replika**, and **Calm**.

---

## 📦 Folder Contents

* `requirements.txt`
* `config.example.yaml`
* `reddit_research.py`
* `data_prep.py`
* `label_helpfulness.py`
* `merge_labels.py`
* `analyze_helpfulness.py`

> **Note:** Do **not** commit `config.yaml`—it contains your private credentials.

---

## 🚀 Getting Started

### 1. Setup Python Environment

```bash
# Create & activate virtual environment
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Credentials

1. Copy the example file:

   ```bash
   cp config.example.yaml config.yaml
   ```
2. Open `config.yaml` and fill in your Reddit API credentials:

   ```yaml
   reddit:
     client_id:     "<YOUR_CLIENT_ID>"
     client_secret: "<YOUR_CLIENT_SECRET>"
     user_agent:    "<YOUR_USER_AGENT>"
   ```

---

## 🛠️ Pipeline Overview

1. **Scrape & Label** (`reddit_research.py`):

   * Fetch comments and upvote scores from Reddit.
   * Automatically label top 20% as “helpful” and bottom 20% as “unhelpful”.
   * Outputs: `reddit_posts.csv`, `reddit_posts_labeled.csv`

2. **Clean & Sample** (`data_prep.py`):

   * Deduplicate, filter for English, convert timestamps, normalize text.
   * Produce a 200-row sample for spot-checking.
   * Outputs: `reddit_posts_clean.csv`, `annotation_sample.csv`

3. **Merge Labels** (`merge_labels.py`):

   * Combine `helpful_label` into the cleaned dataset.
   * Output: `reddit_posts_clean_labeled.csv`

4. **Analysis** (`analyze_helpfulness.py`):

   * Compute VADER sentiment and high-risk flags.
   * Compare metrics by “helpful” vs “unhelpful”.

---

## 🎯 Usage Examples

**Run full pipeline:**

```bash
python reddit_research.py
python data_prep.py --input reddit_posts.csv --cleaned reddit_posts_clean.csv --sample annotation_sample.csv --sample-size 200
python merge_labels.py
python analyze_helpfulness.py
```

---

**Enjoy exploring community sentiment and safety patterns in digital mental health support!**
