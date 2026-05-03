from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import DEFAULT_PATHS


BUSINESS_RE = re.compile(
    r"\b(?:sarl|ltd|limited|company|merchant|enterprise|ets|intouch|mtnc|orange)\b",
    re.IGNORECASE,
)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def add_time_fields(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df["month"] = df["datetime"].dt.to_period("M").astype(str)
    df["is_weekend"] = df["datetime"].dt.dayofweek >= 5
    return df


def flag_business_usage(df: pd.DataFrame) -> pd.Series:
    text = (df["contact"].fillna("") + " " + df["content"].fillna(""))
    return text.str.contains(BUSINESS_RE)


def compute_user_features(df: pd.DataFrame) -> pd.DataFrame:
    df = add_time_fields(df)
    df["is_business_txn"] = flag_business_usage(df)

    base = df.groupby("user_id")

    summary = base.agg(
        total_transactions=("amount", "count"),
        total_transaction_volume=("amount", "sum"),
        avg_transaction_amount=("amount", "mean"),
        deposit_amount=("amount", lambda s: s[df.loc[s.index, "transaction_type"] == "receive"].sum()),
        withdraw_amount=("amount", lambda s: s[df.loc[s.index, "transaction_type"] == "withdraw"].sum()),
        transfer_amount=("amount", lambda s: s[df.loc[s.index, "transaction_type"] == "transfer"].sum()),
        payment_amount=("amount", lambda s: s[df.loc[s.index, "transaction_type"] == "payment"].sum()),
        airtime_amount=("amount", lambda s: s[df.loc[s.index, "transaction_type"] == "airtime"].sum()),
        weekend_txn_count=("is_weekend", "sum"),
        business_txn_count=("is_business_txn", "sum"),
        months_active=("month", "nunique"),
    ).reset_index()

    summary["transactions_per_month"] = (
        summary["total_transactions"] / summary["months_active"].replace(0, 1)
    )
    summary["deposit_withdraw_ratio"] = summary["deposit_amount"] / (
        summary["withdraw_amount"] + 1.0
    )
    summary["weekend_ratio"] = summary["weekend_txn_count"] / summary["total_transactions"]
    summary["weekend_activity"] = (summary["weekend_ratio"] >= 0.2).astype(int)

    payment_ratio = summary["payment_amount"] / summary["total_transaction_volume"].replace(0, np.nan)
    summary["business_usage"] = (
        (summary["business_txn_count"] > 0) | (payment_ratio.fillna(0) >= 0.3)
    ).astype(int)

    return summary


def min_max_scale(series: pd.Series) -> pd.Series:
    min_val = series.min()
    max_val = series.max()
    if min_val == max_val:
        return pd.Series(0.5, index=series.index)
    return (series - min_val) / (max_val - min_val)


def add_activity_score(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["volume_norm"] = min_max_scale(df["total_transaction_volume"].fillna(0))
    df["count_norm"] = min_max_scale(df["total_transactions"].fillna(0))
    df["avg_amount_norm"] = min_max_scale(df["avg_transaction_amount"].fillna(0))
    df["freq_norm"] = min_max_scale(df["transactions_per_month"].fillna(0))

    df["activity_score"] = (
        0.35 * df["volume_norm"]
        + 0.25 * df["count_norm"]
        + 0.20 * df["avg_amount_norm"]
        + 0.20 * df["freq_norm"]
    )
    return df


def label_activity_levels(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    low_thr = df["activity_score"].quantile(0.33)
    high_thr = df["activity_score"].quantile(0.66)

    conditions = [
        df["activity_score"] < low_thr,
        (df["activity_score"] >= low_thr) & (df["activity_score"] < high_thr),
        df["activity_score"] >= high_thr,
    ]
    labels = ["low", "medium", "high"]
    df["activity_level"] = np.select(conditions, labels, default="medium")
    df["activity_threshold_low"] = low_thr
    df["activity_threshold_high"] = high_thr
    return df


def run_feature_engineering(input_path: Path, output_path: Path) -> None:
    df = pd.read_csv(input_path)
    features = compute_user_features(df)
    features = add_activity_score(features)
    features = label_activity_levels(features)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    features.to_csv(output_path, index=False)
    logging.info("Feature dataset saved to %s", output_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create user-level features.")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_PATHS.processed_dir / "transactions_cleaned.csv",
        help="Input cleaned transactions CSV.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_PATHS.processed_dir / "user_features.csv",
        help="Output user-level feature CSV.",
    )
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()
    run_feature_engineering(args.input, args.output)


if __name__ == "__main__":
    main()
