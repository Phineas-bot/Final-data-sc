# Performance Summary

## Best Model
The Decision Tree classifier was selected as the best-performing model for this dataset.

## Performance Metrics
- Accuracy: 0.6667
- Precision (macro): 0.50
- Recall (macro): 0.6667
- F1 (macro): 0.5556

## Interpretation
- The model is able to correctly classify approximately two-thirds of users overall.
- Macro precision and recall show balanced performance across the three activity segments.
- The moderate F1 score indicates that the model captures useful activity signals, but there is room to improve with additional training data and more advanced feature engineering.

## Next Steps
- Validate the model on an expanded dataset to improve robustness.
- Monitor misclassifications, especially between medium and high activity users, to refine thresholds and model features.

See `model_comparison.csv` for the complete comparison of evaluated algorithms.
