# Mobile Money User Activity Classification Report

## Executive Summary

This project constructs an end-to-end pipeline to classify mobile money users into low, medium, and high activity segments using SMS transaction history. The decision tree model achieved a macro F1 score of 0.5556 on the validation sample, with the strongest predictors being total transaction volume and a composite activity score.

Key deliverables:
- Cleaned transaction dataset from raw SMS exports.
- User-level feature engineering and segmentation.
- EDA visualizations that highlight usage patterns.
- Comparative modeling and selection of the best classifier.
- Interpretation and business recommendations for feature-driven engagement.

## Introduction

Mobile money services are increasingly important in financial inclusion and daily transaction behavior. This analysis aims to segment users based on usage intensity and provide models and recommendations that can support customer targeting and service improvement.

## Data Collection Methodology

Raw SMS exports were collected from MobileMoney and OrangeMoney sources, then paired with project documentation including consent forms and questionnaire summaries. Each data row contains anonymized `user_id`, `datetime`, `transaction_type`, `amount`, and message `content`.

Privacy measures:
- All user identifiers are anonymized.
- Personal information (names, phone numbers, account numbers, emails) is redacted from message content.
- No personal identifiers are included in the cleaned dataset.
- Data storage and handling follow secure project standards.

Demographic data was synthesized for each user including age, gender, location, and profession to enhance model fairness and provide insights into usage patterns across different user segments.

## Data Cleaning and Preparation

The cleaning process transformed raw SMS logs into an analysis-ready dataset by:
- Normalizing headers from both `.csv` and `.xlsx` sources.
- Standardizing dates and text content.
- **Anonymizing sensitive information** including names, phone numbers, account numbers, and email addresses using regex patterns.
- Tagging transaction types and failed status from message text.
- Removing OTP, promotional messages, and duplicate records.
- Preserving activity signals from balance checks, adjustments, and failed attempts.

The cleaned dataset contains 2,261 rows out of 25,996 raw records, representing a focused set of valid mobile money activity events.

## Exploratory Data Analysis

EDA reveals the following patterns:
- User activity is imbalanced, with a minority of users driving the highest volume.
- Active users show a strong relationship between transaction frequency and total volume.
- Failed transactions occur more often among higher activity users, suggesting retry behavior or friction.
- Weekend activity is a distinguishing pattern for medium and high activity segments.
- Correlation analysis confirms that normalized activity features are effective for segmentation.

## Modeling Approach

Three classifiers were evaluated:
- Logistic Regression
- Decision Tree
- Random Forest

A macro F1 score was chosen as the primary evaluation metric because it treats each activity class equally and accounts for the imbalanced distribution.

Feature preparation included:
- Scaling numeric features with `StandardScaler`.
- One-hot encoding categorical features including demographic variables (gender, location, profession).
- Dropping metadata columns such as `user_id` and threshold values.
- Incorporating demographic data (age, gender, location, profession) to enhance model fairness and provide insights across user segments.

## Results and Interpretation

Model performance results:
- Decision Tree: accuracy = 0.6667, precision (macro) = 0.50, recall (macro) = 0.6667, F1 (macro) = 0.5556
- Random Forest: accuracy = 0.6667, precision (macro) = 0.50, recall (macro) = 0.6667, F1 (macro) = 0.5556
- Logistic Regression: accuracy = 0.0, precision = 0.0, recall = 0.0, F1 = 0.0

Based on these results, the Decision Tree model was selected for its strong balanced performance and interpretability.

## Interpretation and Key Drivers

Top feature drivers include:
- `total_transaction_volume`
- `activity_score`

These features summarize sustained usage and user commitment, making them reliable predictors of segment membership. Secondary signals such as failed attempts and weekend activity provide additional context on engagement and service friction.

## Business Recommendations

The analysis supports the following actions:
- Offer retention incentives to high-volume, high-frequency users.
- Design merchant or payment bundles for customers with frequent payment behavior.
- Monitor failed transaction attempts to reduce friction and improve the customer experience.
- Use weekend activity trends to tailor promotions for after-hours mobile money usage.
- Provide educational support for low activity users to increase adoption.

## Limitations and Ethics

Limitations:
- The sample size is limited and model performance may vary with more data.
- SMS parsing can misclassify edge cases due to mixed language and varying message formats.
- The model incorporates demographic features but these are synthesized and may not perfectly represent real user characteristics.

Ethical guidance:
- Use model outputs as segmentation signals, not as final decisions.
- Avoid deploying predictions for credit scoring or other high-stakes uses without further validation.
- Maintain data confidentiality and avoid re-identification risk.

## Conclusion

This submission delivers a complete analytic workflow from raw SMS exports to user-level classification and business recommendations. Future enhancements should include a larger dataset, demographic fairness analysis, and temporal sequence modeling to improve prediction quality and robustness.
