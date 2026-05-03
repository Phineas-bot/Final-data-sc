from __future__ import annotations

import argparse
import logging
from pathlib import Path

from src.cleaning import run_cleaning
from src.config import DEFAULT_PATHS
from src.eda import run_eda
from src.feature_engineering import run_feature_engineering
from src.interpretation import run_interpretation
from src.modeling import run_modeling
from src.pipeline import run_pipeline


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run full data science pipeline.")
    parser.add_argument(
        "--skip-eda",
        action="store_true",
        help="Skip EDA plots generation.",
    )
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()

    interim_path = DEFAULT_PATHS.interim_dir / "transactions_interim.csv"
    cleaned_path = DEFAULT_PATHS.processed_dir / "transactions_cleaned.csv"
    features_path = DEFAULT_PATHS.processed_dir / "user_features.csv"

    run_pipeline(DEFAULT_PATHS.raw_input_dirs, interim_path)
    run_cleaning(
        interim_path,
        cleaned_path,
        DEFAULT_PATHS.project_root / "outputs" / "data_quality_report.csv",
    )
    run_feature_engineering(cleaned_path, features_path)

    if not args.skip_eda:
        run_eda(
            features_path,
            cleaned_path,
            DEFAULT_PATHS.project_root / "outputs" / "figures",
            DEFAULT_PATHS.project_root / "outputs" / "eda_summary.csv",
        )

    run_modeling(
        features_path,
        DEFAULT_PATHS.project_root / "outputs" / "modeling",
        DEFAULT_PATHS.project_root / "models",
    )
    run_interpretation(
        features_path,
        DEFAULT_PATHS.project_root / "models" / "best_model.joblib",
        DEFAULT_PATHS.project_root / "outputs" / "interpretation",
    )


if __name__ == "__main__":
    main()
