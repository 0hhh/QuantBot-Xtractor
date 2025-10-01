"""
Data Cleaning
"""

import pandas as pd
import re
from unidecode import unidecode


def clean_and_save(df: pd.DataFrame, outfile: str):
    """Clean, normalize and save tweets to parquet"""
    df = df.drop_duplicates(subset=["content"])

    def normalize(text):
        text = unidecode(str(text))
        text = re.sub(r"http\S+", "", text)  # remove URLs
        text = re.sub(r"[^a-zA-Z0-9#@ ]", " ", text)  # keep alphanumeric
        return text.lower().strip()

    df["clean_content"] = df["content"].apply(normalize)
    df.to_parquet(outfile, index=False)
    print(f"[INFO] Cleaned data saved → {outfile}")
    return df
