"""
Twitter Scraper using snscrape (with fallback)
"""

import snscrape.modules.twitter as sntwitter
import pandas as pd
import re
from pathlib import Path

SAMPLE_FILE = Path("data/raw/sample_tweets.parquet")


def scrape_from_snscrape(hashtag: str, limit: int = 100):
    """Scrape tweets for a given hashtag using snscrape."""
    query = f"#{hashtag}"
    tweets = []
    try:
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
            if i >= limit:
                break
            content = tweet.content or ""
            mentions = re.findall(r"@(\w+)", content)
            hashtags = re.findall(r"#(\w+)", content)
            tweets.append({
                "search_hashtag": hashtag,
                "username": tweet.user.username,
                "timestamp": tweet.date,
                "content": content,
                "mentions": mentions,
                "hashtags": hashtags,
                "likes": tweet.likeCount,
                "replies": tweet.replyCount,
                "retweets": tweet.retweetCount,
            })
        return pd.DataFrame(tweets)
    except Exception as e:
        print(f"[ERROR] snscrape failed for #{hashtag}: {e}")
        return pd.DataFrame()


def scrape_hashtag(hashtag: str, limit: int = 100):
    """Scrape tweets, fallback to sample dataset if needed."""
    df = scrape_from_snscrape(hashtag, limit)
    if not df.empty:
        print(f"[INFO] Collected {len(df)} live tweets for #{hashtag}")
        return df
    if SAMPLE_FILE.exists():
        print(f"[WARN] Using cached sample for #{hashtag}")
        sample = pd.read_parquet(SAMPLE_FILE)
        return sample[sample["search_hashtag"] == hashtag].head(limit)
    print(f"[ERROR] No tweets available for #{hashtag}")
    return pd.DataFrame()
