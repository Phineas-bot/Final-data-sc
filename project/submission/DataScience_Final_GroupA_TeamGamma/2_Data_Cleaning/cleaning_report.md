# Data Cleaning Report

## Issues Found
- Missing values in content, amount, or timestamps.
- Duplicate SMS exports across multiple files.
- Non-behavioral messages such as OTP and promotions.
- Inconsistent language and formatting (English/French).

## Cleaning Actions
- Removed duplicates based on user, datetime, content, and amount.
- Standardized dates, times, and currency values.
- Normalized column headers from CSV and XLSX sources.
- Excluded OTP and promotional messages.
- Retained failed/declined transactions as attempted activity.
- Included balance and adjustment messages as activity signals.

## Outlier Handling
- Negative amounts were removed.
- Extreme values were retained to preserve high-activity users but flagged in EDA.

## Summary Statistics
- Raw rows: 25,996
- Cleaned rows: 2,261
- Drop rate: 91.30 percent

See data_quality_report.csv for missing-value rates.
