from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier

from src.config import DEFAULT_PATHS


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def load_features(features_path: Path) -> pd.DataFrame:
    return pd.read_csv(features_path)


def build_preprocessor(feature_df: pd.DataFrame) -> tuple[ColumnTransformer, list[str]]:
    target = "activity_level"
    drop_cols = {"user_id", "activity_level", "activity_threshold_low", "activity_threshold_high"}
    features = feature_df.drop(columns=[col for col in drop_cols if col in feature_df.columns])

    numeric_cols = features.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = [col for col in features.columns if col not in numeric_cols]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ]
    )
    return preprocessor, features.columns.tolist()


def evaluate_model(name: str, model: Pipeline, x_test: pd.DataFrame, y_test: pd.Series) -> dict:
    preds = model.predict(x_test)
    return {
        "model": name,
        "accuracy": accuracy_score(y_test, preds),
        "precision_macro": precision_score(y_test, preds, average="macro", zero_division=0),
        "recall_macro": recall_score(y_test, preds, average="macro", zero_division=0),
        "f1_macro": f1_score(y_test, preds, average="macro", zero_division=0),
    }


def save_classification_report(
    y_true: pd.Series,
    y_pred: np.ndarray,
    output_path: Path,
) -> None:
    report = classification_report(y_true, y_pred, zero_division=0, output_dict=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)


def save_confusion_matrix(
    y_true: pd.Series,
    y_pred: np.ndarray,
    labels: list[str],
    output_path: Path,
) -> None:
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    df = pd.DataFrame(cm, index=labels, columns=labels)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=True)


def run_modeling(features_path: Path, output_dir: Path, model_dir: Path) -> None:
    df = load_features(features_path)
    target = "activity_level"

    if target not in df.columns:
        raise ValueError("activity_level column missing from features dataset.")

    y = df[target]
    x = df.drop(columns=[target])

    preprocessor, _ = build_preprocessor(df)

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y if y.nunique() > 1 else None,
    )

    models = {
        "logistic_regression": LogisticRegression(max_iter=200, class_weight="balanced"),
        "decision_tree": DecisionTreeClassifier(random_state=42, class_weight="balanced"),
        "random_forest": RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced",
        ),
    }

    metrics: list[dict] = []
    best_model_name = ""
    best_score = -1.0
    best_pipeline: Pipeline | None = None

    for name, estimator in models.items():
        pipeline = Pipeline(
            steps=[("preprocessor", preprocessor), ("model", estimator)]
        )
        pipeline.fit(x_train, y_train)

        results = evaluate_model(name, pipeline, x_test, y_test)
        metrics.append(results)
        logging.info("%s f1_macro: %.4f", name, results["f1_macro"])

        if results["f1_macro"] > best_score:
            best_score = results["f1_macro"]
            best_model_name = name
            best_pipeline = pipeline

        preds = pipeline.predict(x_test)
        save_classification_report(
            y_test,
            preds,
            output_dir / f"{name}_classification_report.json",
        )
        save_confusion_matrix(
            y_test,
            preds,
            labels=sorted(y.unique()),
            output_path=output_dir / f"{name}_confusion_matrix.csv",
        )

    comparison = pd.DataFrame(metrics)
    output_dir.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(output_dir / "model_comparison.csv", index=False)

    if best_pipeline is None:
        raise RuntimeError("No model was trained successfully.")

    model_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_pipeline, model_dir / "best_model.joblib")

    with (output_dir / "best_model.json").open("w", encoding="utf-8") as handle:
        json.dump({"model": best_model_name, "f1_macro": best_score}, handle, indent=2)

    logging.info("Best model: %s", best_model_name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train and evaluate models.")
    parser.add_argument(
        "--features",
        type=Path,
        default=DEFAULT_PATHS.processed_dir / "user_features.csv",
        help="Input features CSV.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_PATHS.project_root / "outputs" / "modeling",
        help="Output directory for metrics.",
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=DEFAULT_PATHS.project_root / "models",
        help="Output directory for trained model.",
    )
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()
    run_modeling(args.features, args.output_dir, args.model_dir)


if __name__ == "__main__":
    main()
