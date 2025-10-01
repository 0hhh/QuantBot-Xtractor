"""
Visualization Module for Quant-Xtractor
Generates:
1. Signal Trends over Time
2. Tweet Volume by Hour
3. Engagement Distribution
4. Top Hashtags
"""

import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


def plot_signal_trend(signals_file, plot_file):
    """Plot signal trends from signals.json"""
    df = pd.read_json(signals_file)
    if df.empty or "hour" not in df.columns:
        print("[WARN] No signals to plot")
        return

    plt.figure(figsize=(10, 5))
    for col in df.columns:
        if col != "hour":
            plt.plot(df["hour"], df[col], label=col)

    plt.legend()
    plt.title("Signal Trends Over Time")
    plt.xlabel("Time")
    plt.ylabel("Signal Value")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.close()
    print(f"[INFO] Plot saved → {plot_file}")


def plot_tweet_volume(df, plot_file):
    """Plot tweet volume by hour"""
    df["hour"] = pd.to_datetime(df["timestamp"]).dt.floor("h")
    volume = df.groupby("hour").size().reset_index(name="tweet_count")

    if volume.empty:
        print("[WARN] No tweet volume data to plot")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(volume["hour"], volume["tweet_count"], marker="o", label="Tweet Volume")
    plt.title("Tweet Volume by Hour")
    plt.xlabel("Time")
    plt.ylabel("Number of Tweets")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.close()
    print(f"[INFO] Plot saved → {plot_file}")


def plot_engagement_distribution(df, plot_file):
    """Plot histogram of likes, retweets, and replies"""
    if df.empty:
        print("[WARN] No engagement data to plot")
        return

    plt.figure(figsize=(10, 5))
    plt.hist(df["likes"], bins=30, alpha=0.5, label="Likes")
    plt.hist(df["retweets"], bins=30, alpha=0.5, label="Retweets")
    plt.hist(df["replies"], bins=30, alpha=0.5, label="Replies")
    plt.title("Engagement Distribution")
    plt.xlabel("Count")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.close()
    print(f"[INFO] Plot saved → {plot_file}")


def plot_top_hashtags(df, plot_file, top_n=10):
    """Plot top hashtags from the dataset"""
    if df.empty or "hashtags" not in df.columns:
        print("[WARN] No hashtags to plot")
        return

    all_hashtags = sum(df["hashtags"].tolist(), [])
    counter = Counter(all_hashtags)
    if not counter:
        print("[WARN] No hashtags found")
        return

    top_tags = counter.most_common(top_n)
    labels, counts = zip(*top_tags)

    plt.figure(figsize=(8, 5))
    plt.bar(labels, counts)
    plt.title(f"Top {top_n} Hashtags in Market Tweets")
    plt.xlabel("Hashtag")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.close()
    print(f"[INFO] Plot saved → {plot_file}")
