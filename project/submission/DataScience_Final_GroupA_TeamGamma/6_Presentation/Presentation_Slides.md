# Mobile Money User Activity Classification
## CSC 3221 - Introduction to Data Science
## Group A Team Gamma
## May 6, 2026

---

# Problem Statement & Objectives

## Problem
Mobile money services are transforming financial inclusion in Cameroon, but service providers lack insights into user behavior patterns for targeted product development and risk management.

## Objectives
- Classify users into behavioral segments (Low/Medium/High activity)
- Build reproducible ML pipeline from SMS data to predictions
- Provide actionable business insights for service optimization
- Demonstrate ethical data collection and privacy protection

---

# Data Sources & Collection Ethics

## Data Sources
- **Primary:** SMS exports from MTN MobileMoney and Orange Money
- **Volume:** 26,012 raw SMS messages from 10 users
- **Period:** August 2025 - March 2026
- **Types:** Transactions, balances, adjustments, failed attempts

## Ethical Considerations
- **Consent:** Explicit participant consent with detailed forms
- **Anonymization:** Regex patterns remove personal identifiers
- **Privacy:** No sensitive financial data retained
- **Storage:** Secure local storage with access controls

---

# Data Cleaning Pipeline

## 5-Phase Cleaning Process
1. **Text Parsing:** Extract transaction details from SMS format
2. **Anonymization:** Remove phone numbers, names, account details
3. **Deduplication:** Eliminate duplicate messages
4. **Type Classification:** Categorize transactions (deposit/withdraw/transfer/payment/airtime)
5. **Validation:** Cross-check amounts and maintain data integrity

## Results
- **Input:** 26,012 raw SMS messages
- **Output:** 2,464 cleaned transactions
- **Reduction:** 90.5% data volume reduction
- **Quality:** 100% transaction type accuracy

---

# Feature Engineering Highlights

## User-Level Features (14 total)
- **Volume Metrics:** total_transaction_volume, avg_transaction_amount
- **Frequency Metrics:** total_transactions, transactions_per_month
- **Behavioral Ratios:** deposit_withdraw_ratio, failed_ratio
- **Temporal Patterns:** weekend_activity, months_active
- **Usage Categories:** business_usage, airtime_amount

## Activity Score Computation
```
Activity Score = (0.4 × Volume) + (0.3 × Frequency) + (0.2 × Diversity) + (0.1 × Recency)
```
- **Low:** Bottom 33% (Score < 0.33)
- **Medium:** Middle 33% (0.33 ≤ Score < 0.67)
- **High:** Top 33% (Score ≥ 0.67)

---

# EDA: Activity Distribution

## User Segmentation Results
- **Low Activity:** 4 users (40%)
- **Medium Activity:** 3 users (30%)
- **High Activity:** 3 users (30%)

## Key Patterns
- **Volume Range:** ₣2,500 - ₣1,250,000 (500x difference)
- **Transaction Range:** 12 - 892 transactions
- **High Activity Users:** 75% of total transaction volume
- **Long-tail Effect:** Few users drive majority of activity

---

# EDA: Volume vs Frequency

## Scatter Plot Insights
- **Strong Positive Correlation:** r = 0.87
- **High Activity Cluster:** Volume > ₣500K, Transactions > 400
- **Medium Activity Cluster:** Volume ₣50K-₣500K, Transactions 50-400
- **Low Activity Cluster:** Volume < ₣50K, Transactions < 50

## Business Implications
- **Power Users:** Small group drives significant revenue
- **Growth Opportunity:** Medium users represent expansion potential
- **Retention Focus:** High-volume users require premium service

---

# Modeling Approach & Metrics

## Models Evaluated
- **Logistic Regression:** Baseline linear model
- **Decision Tree:** Interpretable tree-based model
- **Random Forest:** Ensemble method for robustness

## Evaluation Framework
- **Cross-validation:** 5-fold stratified CV
- **Primary Metric:** Macro F1-score (balanced across classes)
- **Secondary Metrics:** Accuracy, Precision, Recall
- **Validation:** Holdout test set (33% of data)

---

# Best Model & Feature Importance

## Decision Tree Performance
- **Accuracy:** 66.67%
- **Macro F1:** 0.556
- **Class Performance:**
  - Low Activity: F1 = 0.67
  - Medium Activity: F1 = 0.50
  - High Activity: F1 = 0.50

## Top Features (50% importance each)
1. **total_transaction_volume** (50.0%)
2. **activity_score** (50.0%)

## Model Interpretation
- Volume and activity score are equally predictive
- Tree depth: 3 levels (interpretable)
- No overfitting detected in validation

---

# Business Insights & Recommendations

## Key Findings
- **Revenue Concentration:** Top 30% users generate 75% of transaction volume
- **Usage Patterns:** Business payments and transfers dominate high-activity users
- **Risk Indicators:** Failed transaction rates correlate with activity levels

## Recommendations
1. **Loyalty Program:** Reward high-volume users with premium features
2. **Targeted Marketing:** Promote business bundles to medium-activity users
3. **UX Improvement:** Reduce failed transactions through better error handling
4. **Product Development:** Design features for power users (bulk transfers, analytics)

---

# Limitations & Ethics

## Technical Limitations
- **Sample Size:** Only 10 users limits generalizability
- **Time Period:** 8-month window may miss seasonal patterns
- **SMS Parsing:** Potential misclassification of complex messages
- **Feature Scope:** Limited to transaction data only

## Ethical Considerations
- **Privacy Protection:** Complete anonymization of personal data
- **Bias Awareness:** Model may reflect existing usage patterns
- **Responsible Use:** Not suitable for high-stakes financial decisions
- **Transparency:** Full documentation of methodology and limitations

---

# Conclusion & Q&A

## Project Achievements
- ✅ Complete ML pipeline: SMS → Predictions
- ✅ Ethical data collection with privacy protection
- ✅ Actionable business insights delivered
- ✅ Reproducible methodology documented

## Key Takeaways
- Mobile money user behavior shows clear segmentation patterns
- Transaction volume and frequency are strongest predictors
- Small user group drives majority of platform activity
- Ethical data science enables responsible insights

## Future Work
- Expand user base for better generalizability
- Add demographic and psychographic features
- Implement real-time classification system
- Validate findings with additional data sources

## Questions?
Thank you for your attention!
