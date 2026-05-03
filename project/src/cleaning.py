from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path

import numpy as np
import pandas as pd

from src.config import DEFAULT_PATHS


AIRTIME_RE = re.compile(r"\bairtime\b", re.IGNORECASE)
FAILED_RE = re.compile(
    r"failed|rejected|echec|echoue|annule|canceled|cancelled",
    re.IGNORECASE,
)


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def normalize_text(value: str | float | int | None) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return ""
    return str(value).strip().lower()


def assign_status(content: str) -> str:
    normalized = normalize_text(content)
    if FAILED_RE.search(normalized):
        return "failed"
    return "success"


def assign_transaction_type(row: pd.Series) -> str:
    content = normalize_text(row.get("content"))
    current = normalize_text(row.get("transaction_type"))
    if AIRTIME_RE.search(content):
        return "airtime"
    return current or "other"


def build_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    total_rows = len(df)
    missing = df.isna().sum().rename("missing_count")
    missing_pct = (missing / total_rows * 100).round(2).rename("missing_pct")
    report = pd.concat([missing, missing_pct], axis=1).reset_index()
    report = report.rename(columns={"index": "column"})
    return report


def clean_transactions(interim: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    df = interim.copy()

    df["status"] = df["content"].apply(assign_status)
    df["transaction_type"] = df.apply(assign_transaction_type, axis=1)
    df["direction"] = df["direction"].astype(str).str.strip().str.lower()
    df["contact"] = df["contact"].astype(str).str.strip()

    pre_count = len(df)
    df = df.dropna(subset=["datetime", "content"])
    df = df.drop_duplicates(
        subset=["user_id", "datetime", "content", "amount", "transaction_type"],
        keep="first",
    )

    df = df[df["status"] == "success"]

    keep_types = {"receive", "withdraw", "transfer", "payment", "airtime"}
    df = df[df["transaction_type"].isin(keep_types)]

    df = df[(df["amount"].fillna(0) >= 0)]
    df = df.dropna(subset=["amount"])

    summary = {
        "rows_before": float(pre_count),
        "rows_after": float(len(df)),
        "drop_pct": float((pre_count - len(df)) / max(pre_count, 1) * 100),
        "amount_mean": float(df["amount"].mean()) if not df.empty else 0.0,
        "amount_median": float(df["amount"].median()) if not df.empty else 0.0,
    }

    return df, summary


def run_cleaning(interim_path: Path, output_path: Path, report_path: Path) -> None:
    interim = pd.read_csv(interim_path, parse_dates=["datetime"])
    quality = build_quality_report(interim)

    cleaned, summary = clean_transactions(interim)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    cleaned.to_csv(output_path, index=False)
    quality.to_csv(report_path, index=False)

    logging.info("Cleaned data saved to %s", output_path)
    logging.info("Quality report saved to %s", report_path)
    logging.info("Rows before: %s", summary["rows_before"])
    logging.info("Rows after: %s", summary["rows_after"])
    logging.info("Drop percent: %.2f", summary["drop_pct"])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean interim transactions.")
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_PATHS.interim_dir / "transactions_interim.csv",
        help="Input interim CSV path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_PATHS.processed_dir / "transactions_cleaned.csv",
        help="Output cleaned CSV path.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_PATHS.project_root / "outputs" / "data_quality_report.csv",
        help="Output data quality report CSV path.",
    )
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()
    run_cleaning(args.input, args.output, args.report)


if __name__ == "__main__":
    main()
