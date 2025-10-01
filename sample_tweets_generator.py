"""
Generate fallback sample tweets dataset
"""

import pandas as pd
import datetime as dt
import random
from pathlib import Path

hashtags = ["nifty50", "sensex", "banknifty", "intraday", "nifty", "indianstockmarket"]

def generate_sample():
    data = []
    now = dt.datetime.utcnow()
    for tag in hashtags:
        for i in range(200):
            content = f"Sample tweet {i} about #{tag} market moves."
            data.append({
                "search_hashtag": tag,
                "username": f"user_{random.randint(1, 500)}",
                "timestamp": (now - dt.timedelta(minutes=random.randint(0, 1440))),
                "content": content,
                "mentions": [],
                "hashtags": [tag],
                "likes": random.randint(0, 100),
                "replies": random.randint(0, 50),
                "retweets": random.randint(0, 30),
            })
    df = pd.DataFrame(data)
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    df.to_parquet("data/raw/sample_tweets.parquet", index=False)
    print("[INFO] Sample tweets saved to data/raw/sample_tweets.parquet")

if __name__ == "__main__":
    generate_sample()
