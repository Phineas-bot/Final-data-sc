# Mobile Money User Activity Classification

## Executive Summary

This project builds a reproducible pipeline to classify mobile money users into low, medium, and high activity segments using transaction behavior. We processed SMS export data from MobileMoney and OrangeMoney, engineered user-level features, and compared multiple models. The best-performing model was a decision tree with macro F1 of 0.5556. Findings highlight that transaction volume and activity score drive the classification most strongly.

## Introduction

Mobile money is a key financial channel in Cameroon. Understanding usage patterns can support segmentation, product design, and risk monitoring. This project focuses on classifying users into activity segments using transaction histories.

## Data Collection Methodology

- Sources: SMS exports from MobileMoney and OrangeMoney.
- Data types: transactions (receive, withdraw, transfer, payment, airtime), balance messages, adjustments, and failed attempts.
- Exclusions: OTP/login and promo/marketing messages.

## Data Quality and Cleaning

- Interim rows: 25,996
- Cleaned rows: 2,261
- User features: 14
- Cleaning removed duplicates, non-transactional noise, OTP, and promotions.
- Failed transactions were retained to reflect attempted activity.

## Feature Engineering

Key engineered features:

- total_transaction_volume
- total_transactions
- avg_transaction_amount
- transactions_per_month
- deposit_withdraw_ratio
- weekend_activity
- business_usage
- failed_transactions and failed_ratio

An activity score was computed with weighted normalization, then bucketed into low/medium/high using percentile thresholds.

## Exploratory Data Analysis

See outputs/figures for:

- Activity level distribution
- Transaction type distribution
- Volume vs frequency scatter
- Feature correlation heatmap
- Monthly volume trend

## Modeling Approach

Models trained:

- Logistic Regression
- Decision Tree
- Random Forest

Evaluation metrics: accuracy, precision, recall, F1 (macro). The decision tree was selected as best model.

## Results and Interpretation

Best model performance:

- Decision Tree macro F1: 0.5556

Top feature importances:

- total_transaction_volume
- activity_score

Interpretation:

- Higher volume and frequency strongly predict high activity users.
- Failed transaction attempts provide additional signal of usage intensity.

## Business Insights and Recommendations

- Reward high-volume users to improve retention.
- Promote bundles for payment-heavy users.
- Use failed attempt rates to detect friction and improve UX.

## Limitations and Ethics

- User count is low at the feature level, which limits generalization.
- SMS parsing may misclassify edge cases.
- Do not use model output for high-stakes decisions without additional validation.

## Conclusion

The project delivers a complete pipeline for user activity classification, with reproducible steps from raw SMS data to model evaluation. Future work should expand the user base and add richer demographic attributes.
