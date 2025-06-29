import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# 1. Load your cleaned, labeled dataset
df = pd.read_csv("reddit_posts_clean_labeled.csv")

# 1a. Ensure no NaNs in the text column
df['cleaned'] = df['cleaned'].fillna("")

# 2. Compute sentiment scores with VADER
analyzer = SentimentIntensityAnalyzer()
df['sentiment'] = df['cleaned'].apply(
    lambda txt: analyzer.polarity_scores(str(txt))['compound']
)

# 3. Detect high-risk phrases via simple regex patterns
patterns = [
    r"\bkill myself\b",
    r"\bwant to die\b",
    r"\bself[- ]harm\b",
    r"\bcommit suicide\b",
    r"\bkill me\b"
]
def detect_high_risk(text):
    text = str(text).lower()
    return int(any(re.search(p, text) for p in patterns))

df['high_risk'] = df['cleaned'].apply(detect_high_risk)

# 4. Aggregate summary by helpfulness label
summary = df.groupby('helpful_label').agg(
    avg_sentiment   = ('sentiment',    'mean'),
    high_risk_rate  = ('high_risk',    'mean'),
    comment_count   = ('sentiment',    'size')
).reset_index().rename(columns={'helpful_label': 'helpful'})

print(summary)
