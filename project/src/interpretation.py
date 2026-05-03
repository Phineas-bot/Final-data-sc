from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from src.config import DEFAULT_PATHS


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def load_model(model_path: Path) -> Pipeline:
    return joblib.load(model_path)


def get_feature_names(preprocessor, feature_df: pd.DataFrame) -> list[str]:
    numeric_cols = feature_df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = [col for col in feature_df.columns if col not in numeric_cols]

    cat_features = []
    if categorical_cols:
        encoder = preprocessor.named_transformers_["cat"]
        cat_features = encoder.get_feature_names_out(categorical_cols).tolist()

    return numeric_cols + cat_features


def extract_importance(model: Pipeline, x: pd.DataFrame) -> pd.DataFrame:
    preprocessor = model.named_steps["preprocessor"]
    estimator = model.named_steps["model"]

    feature_names = get_feature_names(preprocessor, x)

    if hasattr(estimator, "feature_importances_"):
        importances = estimator.feature_importances_
    elif hasattr(estimator, "coef_"):
        importances = np.mean(np.abs(estimator.coef_), axis=0)
    else:
        raise ValueError("Estimator does not support feature importance.")

    importance_df = pd.DataFrame(
        {"feature": feature_names, "importance": importances}
    ).sort_values(by="importance", ascending=False)

    return importance_df


def create_example_predictions(model: Pipeline, x: pd.DataFrame, count: int = 5) -> pd.DataFrame:
    sample = x.sample(n=min(count, len(x)), random_state=42).copy()
    sample["predicted_activity"] = model.predict(sample)
    return sample


def run_interpretation(features_path: Path, model_path: Path, output_dir: Path) -> None:
    df = pd.read_csv(features_path)
    if "activity_level" not in df.columns:
        raise ValueError("activity_level column missing in features.")

    drop_cols = {"activity_level", "user_id", "activity_threshold_low", "activity_threshold_high"}
    x = df.drop(columns=[col for col in drop_cols if col in df.columns])
    model = load_model(model_path)

    importance_df = extract_importance(model, x)
    example_preds = create_example_predictions(model, x)

    output_dir.mkdir(parents=True, exist_ok=True)
    importance_df.to_csv(output_dir / "feature_importance.csv", index=False)
    example_preds.to_csv(output_dir / "example_predictions.csv", index=False)

    metadata = {
        "top_features": importance_df.head(10)["feature"].tolist(),
        "note": "Importance derived from model coefficients or tree importances.",
    }
    with (output_dir / "interpretation_summary.json").open("w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2)

    logging.info("Saved interpretation outputs to %s", output_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Model interpretation outputs.")
    parser.add_argument(
        "--features",
        type=Path,
        default=DEFAULT_PATHS.processed_dir / "user_features.csv",
        help="Input features CSV.",
    )
    parser.add_argument(
        "--model",
        type=Path,
        default=DEFAULT_PATHS.project_root / "models" / "best_model.joblib",
        help="Input trained model path.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_PATHS.project_root / "outputs" / "interpretation",
        help="Output directory for interpretation files.",
    )
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()
    run_interpretation(args.features, args.model, args.output_dir)


if __name__ == "__main__":
    main()
