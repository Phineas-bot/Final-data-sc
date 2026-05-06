# Review Notes

## Data Coverage

- Interim rows: 25,996
- Cleaned rows: 2,261
- User feature rows: 14
- Inputs include CSV and XLSX exports (MobileMoney + OrangeMoney)

## Modeling Snapshot

- Best model: Decision Tree
- Macro F1: 0.5556
- Logistic Regression macro F1: 0.0000
- Random Forest macro F1: 0.5556

## Key Observations

- The small number of user rows (14) suggests many files belong to the same user or lack user-level identifiers.
- Heavy filtering removed a large portion of SMS messages that are not behavioral transactions.
- Feature importance is concentrated in volume-based features.

## Recommended Next Checks

- Confirm user identifiers and ensure multiple users are represented.
- Validate class balance for activity levels.
- Review confusion matrices for class-specific errors.
