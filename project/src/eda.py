from __future__ import annotations

import argparse
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.config import DEFAULT_PATHS


sns.set_theme(style="whitegrid")


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_plot(fig: plt.Figure, output_dir: Path, filename: str) -> None:
    output_path = output_dir / filename
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logging.info("Saved plot: %s", output_path)


def load_inputs(features_path: Path, transactions_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    features = pd.read_csv(features_path)
    transactions = pd.read_csv(transactions_path, parse_dates=["datetime"])
    return features, transactions


def plot_activity_distribution(features: pd.DataFrame, output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=features, x="activity_level", order=["low", "medium", "high"], ax=ax)
    ax.set_title("Distribution of Activity Levels")
    ax.set_xlabel("Activity Level")
    ax.set_ylabel("User Count")
    save_plot(fig, output_dir, "activity_level_distribution.png")


def plot_transactions_by_type(transactions: pd.DataFrame, output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(7, 4))
    order = transactions["transaction_type"].value_counts().index
    sns.countplot(data=transactions, y="transaction_type", order=order, ax=ax)
    ax.set_title("Transactions by Type")
    ax.set_xlabel("Count")
    ax.set_ylabel("Transaction Type")
    save_plot(fig, output_dir, "transactions_by_type.png")


def plot_avg_amount_by_activity(features: pd.DataFrame, output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=features, x="activity_level", y="avg_transaction_amount", ax=ax)
    ax.set_title("Average Transaction Amount by Activity Level")
    ax.set_xlabel("Activity Level")
    ax.set_ylabel("Avg Amount (XAF)")
    save_plot(fig, output_dir, "avg_amount_by_activity.png")


def plot_volume_vs_frequency(features: pd.DataFrame, output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=features,
        x="transactions_per_month",
        y="total_transaction_volume",
        hue="activity_level",
        ax=ax,
    )
    ax.set_title("Transaction Volume vs Frequency")
    ax.set_xlabel("Transactions per Month")
    ax.set_ylabel("Total Volume (XAF)")
    save_plot(fig, output_dir, "volume_vs_frequency.png")


def plot_correlation_heatmap(features: pd.DataFrame, output_dir: Path) -> None:
    numeric_cols = features.select_dtypes(include=[np.number])
    corr = numeric_cols.corr().round(2)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, cmap="coolwarm", annot=False, ax=ax)
    ax.set_title("Feature Correlation Heatmap")
    save_plot(fig, output_dir, "feature_correlation_heatmap.png")


def plot_time_series(transactions: pd.DataFrame, output_dir: Path) -> None:
    monthly = (
        transactions.set_index("datetime")
        .groupby(pd.Grouper(freq="ME"))
        .size()
        .reset_index(name="transaction_count")
    )
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(monthly["datetime"], monthly["transaction_count"], marker="o")
    ax.set_title("Monthly Transaction Volume")
    ax.set_xlabel("Month")
    ax.set_ylabel("Transaction Count")
    save_plot(fig, output_dir, "monthly_transaction_volume.png")


def plot_weekend_activity(features: pd.DataFrame, output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(features["weekend_ratio"].fillna(0), bins=20, ax=ax)
    ax.set_title("Weekend Activity Ratio Distribution")
    ax.set_xlabel("Weekend Ratio")
    ax.set_ylabel("User Count")
    save_plot(fig, output_dir, "weekend_activity_ratio.png")


def plot_business_usage(features: pd.DataFrame, output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.countplot(data=features, x="business_usage", ax=ax)
    ax.set_title("Business Usage Indicator")
    ax.set_xlabel("Business Usage (1=Yes)")
    ax.set_ylabel("User Count")
    save_plot(fig, output_dir, "business_usage_indicator.png")


def plot_activity_score_distribution(features: pd.DataFrame, output_dir: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(features["activity_score"], bins=20, kde=True, ax=ax)
    ax.set_title("Activity Score Distribution")
    ax.set_xlabel("Activity Score")
    ax.set_ylabel("User Count")
    save_plot(fig, output_dir, "activity_score_distribution.png")


def save_summary(features: pd.DataFrame, output_path: Path) -> None:
    summary = features.describe(include="all").transpose()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path)
    logging.info("Saved EDA summary table to %s", output_path)


def run_eda(features_path: Path, transactions_path: Path, output_dir: Path, summary_path: Path) -> None:
    ensure_dir(output_dir)
    features, transactions = load_inputs(features_path, transactions_path)

    plot_activity_distribution(features, output_dir)
    plot_transactions_by_type(transactions, output_dir)
    plot_avg_amount_by_activity(features, output_dir)
    plot_volume_vs_frequency(features, output_dir)
    plot_correlation_heatmap(features, output_dir)
    plot_time_series(transactions, output_dir)
    plot_weekend_activity(features, output_dir)
    plot_business_usage(features, output_dir)
    plot_activity_score_distribution(features, output_dir)

    save_summary(features, summary_path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run EDA and save figures.")
    parser.add_argument(
        "--features",
        type=Path,
        default=DEFAULT_PATHS.processed_dir / "user_features.csv",
        help="Input user feature CSV.",
    )
    parser.add_argument(
        "--transactions",
        type=Path,
        default=DEFAULT_PATHS.processed_dir / "transactions_cleaned.csv",
        help="Input cleaned transactions CSV.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_PATHS.project_root / "outputs" / "figures",
        help="Directory for plots.",
    )
    parser.add_argument(
        "--summary",
        type=Path,
        default=DEFAULT_PATHS.project_root / "outputs" / "eda_summary.csv",
        help="Output EDA summary CSV.",
    )
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()
    run_eda(args.features, args.transactions, args.output_dir, args.summary)


if __name__ == "__main__":
    main()
