# Interpretation Report

## Top Predictive Features
The feature importance analysis identifies the strongest signals used by the model:
- `total_transaction_volume`
- `activity_score`

## What the Model Learns
- High activity users are primarily distinguished by large cumulative transaction volumes and frequent use.
- The engineered `activity_score` captures the combined effect of normalized volume, frequency, and average transaction size, making it a powerful composite indicator.
- Failed transaction attempts and weekend activity serve as secondary signals, helping the model distinguish engaged users who experience friction or use services outside of business hours.

## Interpretation Notes
- The model places most weight on sustained volume, which aligns with the business goal of identifying high-value mobile money users.
- Activity score is a robust signal because it reduces the noise of raw transaction counts and scales across users with different behaviors.
- Features with low importance in this analysis may still contain valuable information if the dataset grows larger or includes demographic context.

## Supporting Artifacts
See `feature_importance.csv` for the ordered importance values.
See `example_predictions.csv` for sample predictions and how the model classified users across segments.
