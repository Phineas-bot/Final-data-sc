# Mobile Money User Activity Classification

## Overview

This project builds a reproducible pipeline to classify mobile money users into low, medium, and high activity segments based on transaction history. It includes data ingestion, cleaning, feature engineering, EDA, model training, and interpretation outputs.

## Project Structure

- data/raw: raw input CSVs (optional local copy)
- data/interim: interim transaction dataset
- data/processed: cleaned transactions and user features
- notebooks: optional notebooks
- src: pipeline scripts
- models: trained models
- outputs: figures, reports, metrics
- report: written summaries and insights

## Setup

1. Create a virtual environment.
2. Install dependencies:

```
pip install -r requirements.txt
```

## Run Full Pipeline

```
python -m src.run_pipeline
```

To skip EDA plots:

```
python -m src.run_pipeline --skip-eda
```

## Key Outputs

- outputs/data_quality_report.csv
- outputs/eda_summary.csv
- outputs/figures/*.png
- outputs/modeling/model_comparison.csv
- models/best_model.joblib
- outputs/interpretation/feature_importance.csv

## Notes

- Raw SMS export CSVs are read from raw_datasets by default.
- Ensure the raw_datasets folder is available at the workspace root.
