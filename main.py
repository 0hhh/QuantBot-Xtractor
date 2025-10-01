"""
Main Pipeline for Quant-Xtractor
"""

import json
from pathlib import Path
import pandas as pd
from scraper import scrape_hashtag
from cleaner import clean_and_save
from signals import build_signals
from plotter import plot_signal_trend,plot_tweet_volume,plot_engagement_distribution,plot_top_hashtags

# Paths
DATA_RAW = Path("data/raw")
DATA_PROCESSED = Path("data/processed")
DATA_ANALYSIS = Path("data/analysis")
for p in [DATA_RAW, DATA_PROCESSED, DATA_ANALYSIS]:
    p.mkdir(parents=True, exist_ok=True)


def main():
    print("[START] Quant-Xtractor pipeline")

    # Load hashtags
    with open("hashtags.json", "r") as f:
        hashtags = json.load(f)["hashtags"]

    all_data = []
    for tag in hashtags:
        df = scrape_hashtag(tag, limit=500)   # 500 × 6 hashtags ≈ 3000 tweets
        if not df.empty:
            outfile = DATA_RAW / f"{tag}.parquet"
            df.to_parquet(outfile, index=False)
            all_data.append(df)

    if not all_data:
        print("[ERROR] No tweets collected. Exiting.")
        return

    merged = pd.concat(all_data, ignore_index=True)
    merged_file = DATA_RAW / "all_hashtags.parquet"
    merged.to_parquet(merged_file, index=False)
    print(f"[INFO] Raw data collected → {len(merged)} tweets")

    # Clean
    cleaned_file = DATA_PROCESSED / "cleaned.parquet"
    cleaned = clean_and_save(merged, cleaned_file)

    # Signals
    signals_file = DATA_ANALYSIS / "signals.json"
    build_signals(cleaned, signals_file)

    # # Plot
    # plot_file = DATA_ANALYSIS / "signal_plot.png"
    # plot_signal_trend(signals_file, plot_file)
    # Plots
    plot_signal_trend(signals_file, DATA_ANALYSIS / "signal_plot.png")
    plot_tweet_volume(cleaned, DATA_ANALYSIS / "tweet_volume.png")
    plot_engagement_distribution(cleaned, DATA_ANALYSIS / "engagement_distribution.png")
    plot_top_hashtags(cleaned, DATA_ANALYSIS / "top_hashtags.png")
    print("[END] Pipeline finished successfully")


if __name__ == "__main__":
    main()
