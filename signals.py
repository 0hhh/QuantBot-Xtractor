"""
Feature Engineering
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


def build_signals(df: pd.DataFrame, outfile: str):
    """Convert text into signals and save as JSON"""
    tfidf = TfidfVectorizer(max_features=500)
    X = tfidf.fit_transform(df["clean_content"])
    svd = TruncatedSVD(n_components=5, random_state=42)
    reduced = svd.fit_transform(X)

    for i in range(reduced.shape[1]):
        df[f"signal_{i+1}"] = reduced[:, i]

    df["hour"] = pd.to_datetime(df["timestamp"]).dt.floor("h")

    # Mean + confidence interval
    signals = (
        df.groupby("hour")[[f"signal_{i+1}" for i in range(reduced.shape[1])]]
        .agg(["mean", "std"])
        .reset_index()
    )

    signals.to_json(outfile, orient="records", date_format="iso")
    print(f"[INFO] Signals extracted and saved → {outfile}")
    return signals
