# Mobile Money User Activity Classification Report

## Executive Summary

We built a pipeline to classify mobile money users into low, medium, and high activity segments using SMS transaction histories. The decision tree model achieved a macro F1 of 0.5556. The strongest drivers were transaction volume and activity score. Recommendations focus on retention rewards, merchant bundles, and reducing transaction friction.

## Introduction

Mobile money is a primary financial channel in Cameroon. Understanding usage patterns supports segmentation and service improvement. Our objective is to classify users into activity tiers based on transaction behavior.

## Data Collection Methodology

We collected anonymized SMS exports from MobileMoney and OrangeMoney and paired them with participant questionnaire responses. Participants provided consent and were assigned unique IDs to protect privacy.

## Data Cleaning and Preparation

We standardized multilingual headers, removed duplicates, filtered OTP and promotional messages, and retained failed attempts as activity signals. Balance and adjustment messages were retained as indicators of engagement.

## Exploratory Data Analysis

EDA shows a clear separation between low and high activity users driven by transaction volume and frequency. Weekend usage is higher for active users. Failed attempts correlate with higher activity.

## Modeling Approach

We trained logistic regression, decision tree, and random forest classifiers. Macro F1 was used due to class imbalance. The decision tree model performed best.

## Results and Interpretation

Top features: total_transaction_volume and activity_score. These capture sustained usage and high-value behavior. Example predictions align with these drivers.

## Business Insights and Recommendations

- Reward high-volume users to improve retention.
- Offer merchant bundles for payment-heavy users.
- Use failed attempts to detect friction and improve UX.

## Limitations and Ethics

Sample size at the user level is small, and SMS parsing has edge cases. The model should not be used for high-stakes decisions without further validation.

## Conclusion

The project delivers an end-to-end pipeline from SMS ingestion to classification. Expanding the participant pool and adding demographic features will strengthen future versions.
