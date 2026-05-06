# Model Comparison Report

## Models Evaluated
- Logistic Regression
- Decision Tree
- Random Forest

## Evaluation Metrics
To account for class imbalance among low, medium, and high activity users, we compared models using:
- Accuracy
- Precision (macro)
- Recall (macro)
- F1-score (macro)

## Results Summary
- Decision Tree: accuracy = 0.6667, precision (macro) = 0.50, recall (macro) = 0.6667, F1 (macro) = 0.5556
- Random Forest: accuracy = 0.6667, precision (macro) = 0.50, recall (macro) = 0.6667, F1 (macro) = 0.5556
- Logistic Regression: accuracy = 0.0, precision (macro) = 0.0, recall (macro) = 0.0, F1 (macro) = 0.0

Both tree-based models outperformed logistic regression on this dataset, likely because they can better handle skewed feature distributions and class separation in the engineered feature space.

## Selected Model
The Decision Tree model was selected as the best model based on macro F1 and interpretability.

See `model_comparison.csv` for the full metric table and class-level details.
