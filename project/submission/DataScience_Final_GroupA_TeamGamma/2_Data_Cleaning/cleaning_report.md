# Data Cleaning Report

## Overview
The cleaning stage prepared raw SMS export data for analysis by removing noise, standardizing message labels, and preserving the transaction behavior most relevant to mobile money activity.

## Issues Identified
- Missing values in critical fields such as `datetime`, `content`, and `amount`.
- Duplicate notifications appearing across multiple SMS export files.
- Non-behavioral content such as OTP codes, login verification, and promotional offers.
- Inconsistent formatting across data sources, including mixed English and French phrases.

## Cleaning Strategy
- Loaded anonymized SMS exports and standardized message text for reliable pattern detection.
- Identified failed or declined transactions using failure-related terms in the SMS content.
- Inferred transaction types from text when the provided `transaction_type` was ambiguous or missing.
- Filtered out OTP and promotional messages because they do not represent transactional behavior.
- Preserved balance checks and adjustment messages as signals of user engagement.
- Retained failed attempts as important evidence of attempted activity.

## Data Quality Measures
- Removed rows that lacked essential date/time or content information.
- Dropped exact duplicate records using `user_id`, `datetime`, `content`, `amount`, and `transaction_type`.
- Applied numeric conversion to amount fields and removed negative transaction values.
- Assigned a clean `status` label to support later segmentation and feature engineering.

## Results
- Raw rows: 25,996
- Cleaned rows: 2,261
- Drop rate: 91.30%
- The cleaned dataset balances noise reduction with the need to preserve meaningful behavior signals.

## Notes
- The final cleaned data is saved as `cleaned_data.csv`.
- The `data_quality_report.csv` file provides per-column missing-rate diagnostics.
