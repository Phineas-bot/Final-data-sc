# EDA Summary

This exploratory analysis characterizes how mobile money users differ across the low, medium, and high activity segments.

## Key Patterns
- Activity levels are imbalanced: most users fall into the low or medium segments, while a small core of users account for the strongest usage signals.
- Total transaction volume grows rapidly with user activity, indicating a strong separation between low and high segments.
- Failed transaction attempts are concentrated among more active users and can signal friction points in the service.
- Weekend activity is higher for medium and high activity users, suggesting that active users rely on mobile money for both weekday and weekend needs.
- Balance checks and adjustments appear as consistent engagement signals across the dataset.

## Visualizations
- `activity_level_distribution.png`: shows how users are distributed across activity categories.
- `transactions_by_type.png`: compares the frequency of different SMS transaction types in the cleaned dataset.
- `volume_vs_frequency.png`: plots total transaction volume against monthly frequency by user segment.
- `feature_correlation_heatmap.png`: reveals the relationships between engineered user features.
- `monthly_transaction_volume.png`: displays the trend in transaction volume over time.
- `weekend_activity_ratio.png`: shows how weekend transaction balance differs by activity level.

## Summary Data
A compact `eda_summary.csv` file is also generated to store user and transaction counts used in the analysis.
