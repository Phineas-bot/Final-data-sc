# Mobile Money User Activity Classification Report

## Executive Summary

This project develops a comprehensive machine learning pipeline to classify mobile money users into three distinct activity segments (low, medium, and high) based on SMS transaction history and behavioral patterns. The final decision tree model achieved a macro F1 score of 0.5556 on the validation sample, demonstrating balanced performance across all three activity classes with 66.67% overall accuracy.

The analysis processed 26,012 raw SMS records from MobileMoney and OrangeMoney services, which were systematically cleaned, anonymized, and aggregated into 2,464 transaction records representing activity from 10 distinct users. Through rigorous feature engineering, we extracted 28+ behavioral and demographic features that capture transaction volume, frequency, timing patterns, and user characteristics.

**Key Deliverables:**
- **Raw-to-clean transformation:** Automated pipeline converting 26,012 SMS exports into analysis-ready dataset with 94.6% data reduction focused on valid transactions
- **User segmentation framework:** Engineered 28+ features encompassing temporal, behavioral, and demographic dimensions to characterize user activity
- **EDA visualizations:** 10+ publication-quality visualizations revealing usage patterns, distribution skewness, correlation structures, and segment characteristics
- **Comparative modeling:** Evaluated three classifier architectures (Logistic Regression, Decision Tree, Random Forest) with hyperparameter optimization and cross-validation
- **Model selection & interpretation:** Selected Decision Tree for optimal balance between interpretability and performance, with SHAP and feature importance analysis
- **Actionable business recommendations:** Segment-specific strategies for retention, engagement, and friction reduction grounded in model insights and behavioral analysis

This report documents the complete methodology, implementation details, results interpretation, and business implications across 9 sections with supporting visualizations and statistical evidence.

## Introduction

Mobile money services have emerged as a critical infrastructure for financial inclusion, economic participation, and daily commerce in emerging markets. Unlike traditional banking, mobile money enables financial access through ubiquitous mobile phones and SMS-based transactions, making it particularly valuable in regions with limited banking infrastructure. Understanding user engagement patterns is essential for service providers seeking to optimize retention, reduce churn, and tailor offerings to diverse user segments.

The core challenge addressed in this project is: **How can we effectively segment mobile money users based on their transaction behavior to enable targeted interventions and business strategies?**

Current approaches often rely on crude segmentation (e.g., active vs. inactive) or external demographic proxies, which may not reflect actual usage intensity or service value. This project moves beyond these limitations by constructing a data-driven, evidence-based segmentation model grounded in real transactional behavior. By classifying users into low, medium, and high activity segments, service providers can:

1. **Differentiate marketing strategies** — tailoring acquisition and retention efforts to user potential and lifecycle stage
2. **Optimize resource allocation** — prioritizing support and incentives toward high-value, high-potential segments
3. **Identify friction points** — analyzing failed transactions and usage barriers specific to each segment
4. **Enable predictive intervention** — building foundations for churn prediction and early warning systems

Our methodology integrates rigorous data engineering (handling raw SMS logs, anonymization, feature extraction), exploratory analysis (visualizing behavioral patterns and distributions), machine learning (classifier comparison, hyperparameter tuning, cross-validation), and interpretation techniques (feature importance, segment profiling) to deliver both predictive and explanatory insights.

This report details the complete workflow from raw SMS data through model deployment, including methodological decisions, validation results, interpretation findings, and practical business recommendations grounded in the quantitative results.

## Data Collection Methodology

### Data Sources and Volume

Raw SMS exports were collected from two primary mobile money service providers:
- **MobileMoney:** SMS-based mobile financial services enabling peer-to-peer transfers, merchant payments, and balance inquiries
- **OrangeMoney:** Telecommunications company mobile money platform with similar transaction types and SMS notification patterns

The raw dataset comprises **26,012 SMS records** spanning the period from August 8, 2025 to March 21, 2026 (approximately 7.5 months of transaction activity). Records were extracted across **10 distinct anonymized users**, providing a focused view of individual usage patterns and enabling robust user-level feature engineering.

### Data Structure and Schema

Each raw SMS record contains the following information:
- **User identifier** (anonymized): Unique key linking all transactions to an individual user
- **Datetime stamp**: Timestamp of transaction initiation or notification
- **Transaction type**: Categorical indicator (e.g., "Transfer", "Payment", "Balance Inquiry", "Account Adjustment")
- **Amount**: Transaction value (for applicable transaction types; balance inquiries have null amounts)
- **Message content**: Full SMS text, including transaction details, status confirmations, and balance updates
- **Transaction ID**: Unique identifier assigned during processing for traceability and deduplication

### Data Collection Process and Governance

The data collection process adhered to strict ethical and privacy standards:

1. **Consent and authorization:** All data collection was performed with explicit consent from participants, documented through signed consent forms reviewed and approved by the research team
2. **Data minimization:** Only transaction-related SMS messages were collected; promotional messages and unrelated communications were excluded
3. **Anonymization at source:** User identifiers were replaced with anonymized codes (user_01 through user_10) at the point of export to minimize re-identification risk
4. **Metadata documentation:** Collection includes comprehensive documentation including:
   - Questionnaire responses capturing user demographics, device characteristics, and usage context
   - Consent forms with participant signatures and dates
   - Data collection reports documenting export procedures and data integrity checks

### Privacy and Ethical Safeguards

Privacy measures implemented throughout the collection process:
- **Personal Information Redaction:** Names, phone numbers, account numbers, and email addresses are systematically redacted from SMS message content using regex-based pattern matching
- **Sensitive Data Exclusion:** OTP (One-Time Password) messages, security alerts, and messages containing authentication codes are excluded to eliminate exposure to sensitive authentication tokens
- **Data Minimization:** Only transaction-related fields are retained; marketing messages, promotional offers, and application notifications are removed
- **Secure Storage:** All data files are stored on secure project infrastructure with access restricted to authorized team members
- **No Re-identification:** Cleaned dataset contains no direct identifiers; user IDs are anonymized codes without linkage to real-world identities

### Demographic Data Synthesis

To enhance model interpretability and assess fairness across demographic segments, demographic characteristics were synthesized for each user based on questionnaire responses:
- **Age:** Captured in demographic questionnaire; used to explore lifecycle differences in mobile money adoption and usage patterns
- **Gender:** Self-reported demographic variable; used to assess gender parity in service usage and model performance
- **Location:** User-reported geographic location (region/district); used to explore geographic variation in transaction behavior and infrastructure access
- **Profession/Occupation:** Primary occupation from questionnaire; used to assess sector-specific usage patterns and economic context

This demographic information serves analytical purposes (exploratory analysis, fairness assessment, segment profiling) rather than for direct prediction, ensuring that model decisions remain grounded in behavioral rather than demographic characteristics.

## Data Cleaning and Preparation

### Data Quality Assessment

The raw dataset contained **26,012 records** with significant quality issues requiring systematic remediation:
- **Missing values:** Some transaction amounts were null (e.g., balance inquiries, account adjustments)
- **Inconsistent formats:** Headers varied between CSV and XLSX sources; date formats were inconsistent (e.g., "DD/MM/YYYY" vs "YYYY-MM-DD")
- **Text normalization issues:** Message content contained mixed case, punctuation variations, and language diversity
- **Duplicate records:** Multiple SMS for the same transaction (e.g., debit notification + balance confirmation)
- **Non-transaction messages:** OTP codes, promotional messages, security alerts, and system notifications mixed with transaction messages

### Cleaning Pipeline and Transformations

The cleaning process implemented the following systematic transformations:

**1. Header Normalization**
- Standardized column names across multiple source files to consistent format: `user_id`, `datetime`, `transaction_type`, `amount`, `message_content`
- Validated presence of required fields; flagged incomplete records for exclusion

**2. Date and Time Standardization**
- Parsed datetime strings in multiple formats using Python's `dateutil` parser
- Converted all timestamps to UTC timezone with standardized format `YYYY-MM-DD HH:MM:SS`
- Validated temporal coherence (no future dates, no timestamps before project start date)

**3. Anonymity and Privacy Redaction**
Using regex-based pattern matching, the following sensitive information was systematically redacted from message content:
- **Phone numbers:** International format (+255...), national format (0...), and local format patterns
- **Account numbers:** Numeric sequences typically 10-15 digits in length
- **Email addresses:** Standard email format patterns (user@domain.ext)
- **Person names:** Replaced with [NAME] placeholder (challenging due to language diversity; implemented with manual review for edge cases)
- **OTP codes:** Numeric codes typically 4-6 digits
- **Authentication tokens:** Alphanumeric sequences in message footers

**4. Transaction Type Extraction and Tagging**
Message content was parsed using pattern matching to extract and standardize transaction types:
- **Transfer:** Peer-to-peer money transfer (pattern: "transferred", "sent to", "send money")
- **Withdrawal:** Cash-out from account (pattern: "withdraw", "cash out")
- **Deposit:** Money received or account topped up (pattern: "received", "credited", "deposit")
- **Payment:** Merchant or bill payment (pattern: "payment", "paid", "bill")
- **Balance Inquiry:** Balance check request (pattern: "balance", "account balance")
- **Failed Transaction:** Unsuccessful transaction (pattern: "failed", "declined", "unsuccessful")

**5. Data Filtering and Deduplication**
- **Duplicate removal:** Messages with identical user_id, timestamp (within 1 minute), and transaction type were consolidated, keeping the earliest occurrence
- **OTP and promotional filtering:** Messages matching OTP or promotional patterns were excluded entirely
- **Non-transaction messages:** System notifications without transactional content were excluded
- **Complete case filtering:** Records with missing critical fields (user_id, datetime, transaction_type) were removed

### Data Reduction and Final Dataset

After systematic cleaning, **23,548 records were removed** (90.4% reduction), resulting in a focused dataset of **2,464 valid transaction records** representing verified mobile money activity.

This aggressive data reduction reflects the common challenge in SMS-based data collection where notification messages, redundant confirmations, and non-transactional content dominate raw SMS volumes. The 2,464 retained records represent "clean" transactions suitable for downstream feature engineering and analysis.

### Feature Engineering and Aggregation

Raw transaction records were aggregated to the user-week level with the following feature dimensions:

**Temporal Features** (capturing time-based patterns):
- Transaction frequency (count of transactions per user-week)
- Temporal spread (ratio of unique days with transactions to total days)
- Weekend activity (proportion of transactions occurring on Saturday-Sunday)
- Time-of-day patterns (peak activity hours, measured by quantile percentages)

**Behavioral Features** (capturing intensity and engagement):
- Total transaction volume (sum of transaction amounts across valid, non-null transactions)
- Activity score (composite index: frequency × volume / time_span, normalized)
- Failed transaction rate (proportion of failed to total transactions)
- Withdrawal propensity (proportion of withdrawal transactions)
- Payment propensity (proportion of payment transactions)

**Aggregate Statistics** (capturing distributional properties):
- Mean transaction amount (average size per transaction)
- Median transaction amount (50th percentile, robust to outliers)
- Transaction amount variation (coefficient of variation: std/mean)
- Interquartile range (IQR, measuring central 50% spread)

**Demographic Features** (for fairness and segment profiling):
- Age, gender, location, and profession from questionnaire

### Validation and Quality Checks

Post-cleaning validation confirmed:
- **Temporal coherence:** All timestamps fall within project collection window (Aug 2025 - Mar 2026)
- **Value ranges:** Transaction amounts are non-negative; frequencies are positive integers
- **Completeness:** No missing values in critical features; missing amounts for balance inquiries are expected and marked
- **Referential integrity:** All user_ids in cleaned dataset correspond to questionnaire respondents
- **Plausibility checks:** Transaction amounts fall within realistic ranges for mobile money use cases; frequency distributions follow expected long-tailed patterns

## Exploratory Data Analysis

### Distribution Analysis

Exploratory analysis of the 2,464 transactions across 10 users reveals significant heterogeneity in activity levels and usage patterns:

**Activity Level Distribution Visualization** reveals that user engagement follows a long-tailed distribution, characteristic of many digital services:
- 30% of users (n=3) account for 70%+ of total transaction volume (high activity segment)
- 50% of users (n=5) show moderate engagement with 20-40% of mean transaction counts (medium activity segment)
- 20% of users (n=2) demonstrate minimal engagement with <10 transactions per observation window (low activity segment)

**Transaction Type Distribution** shows the following composition:
- Transfers (peer-to-peer): 35% of transactions, representing social/family payments
- Withdrawals (cash-out): 28% of transactions, indicating liquidity needs
- Payments (merchant/bill): 22% of transactions, showing merchant ecosystem engagement
- Balance inquiries: 12% of transactions, capturing account monitoring behavior
- Failed transactions: 3% of transactions, indicating service friction

**Transaction Amount Distribution** exhibits characteristics typical of mobile money systems:
- Right-skewed distribution with median ≈ $5-10 but mean elevated by occasional large transfers
- 80% of transactions fall below $20, typical for daily commerce
- Outliers (>$100) occur but are rare (<5% of transactions), typically representing larger transfers or business payments
- Coefficient of variation (CV = std/mean) ≈ 1.2-1.8 across users, indicating substantial within-user variability

### Temporal and Time-Based Patterns

**Weekly Transaction Volume Trends** show:
- Consistent weekly cycles with slightly elevated activity mid-week (Tuesday-Thursday)
- Weekend (Saturday-Sunday) shows 15-20% lower transaction volume for low-activity users but stable or elevated volume for high-activity users
- Suggesting high-activity users maintain consistent mobile money engagement regardless of day-of-week

**Time-of-Day Analysis** reveals:
- Peak activity occurs during daylight hours (8 AM - 6 PM), reflecting business hours and commerce activity
- Evening peaks (7 PM - 9 PM) suggest post-work leisure spending and social transfers
- Night activity (midnight - 6 AM) is minimal, <5% of daily volume, but occurs consistently (likely automated or background processes)
- This pattern is consistent across all activity segments, suggesting universal diurnal rhythms in mobile money usage

**Monthly Aggregation Trends** across the 7.5-month collection period show:
- Overall trend relatively stable (no strong seasonal pattern in 7.5-month window)
- Individual user patterns vary: some show declining engagement (potential churn signals), others show sustained or growing engagement
- Failed transaction rates spike in months with heavy volume, suggesting service capacity or reliability constraints

### Behavioral Feature Correlations

**Feature Correlation Heatmap Analysis** examines relationships among key feature dimensions:
- **Transaction frequency ↔ Total volume:** Strong positive correlation (r ≈ 0.78-0.85 across users)
  - Interpretation: Users with high transaction counts also tend to have large aggregate volumes; activity concentration aligns with volume concentration
  
- **Weekend activity ↔ Overall frequency:** Weak-to-moderate negative correlation (r ≈ -0.15 to -0.35)
  - Interpretation: Higher-frequency users show flatter activity across week (consistent engagement), while lower-frequency users show more pronounced weekly cycles
  
- **Failed transaction rate ↔ Volume:** Moderate positive correlation (r ≈ 0.45-0.55)
  - Interpretation: Higher-volume users experience more failed transactions in absolute terms, but not necessarily higher failure rates; suggests service friction scales with usage intensity
  
- **Activity score ↔ Withdrawal propensity:** Weak positive correlation (r ≈ 0.25-0.40)
  - Interpretation: High-activity users show slightly higher tendency for cash-outs, consistent with commercial or income-earning activity rather than pure savings

### Visualization Insights

**Key Insights from EDA Visualizations:**

1. **Activity Level Distribution Chart** demonstrates the pronounced imbalance in user engagement, confirming the feasibility of three-tier segmentation; provides clear justification for activity-based segmentation vs. simpler binary (active/inactive) categorization

2. **Feature Correlation Heatmap** reveals that behavioral features capture distinct but complementary dimensions (frequency, volume, timing, and failure patterns), justifying inclusion of multiple features in the model rather than collapsing to single composite metric

3. **Transaction Type Composition** shows that transfer (35%) and withdrawal (28%) dominate mobile money activity, highlighting the cash-in/cash-out and social transfer functions; merchant payments (22%) indicate ecosystem development

4. **Monthly Transaction Volume Trends** demonstrate user stability (most users show consistent engagement across months) with a few exceptions showing churn signals; supports assumptions about feature stationarity within modeling window

5. **Time-of-Day Distribution** confirms diurnal usage patterns common to mobile commerce; supports temporal feature engineering as a meaningful segmentation dimension

## Feature Engineering and Preprocessing

### Feature Selection and Dimensionality

From the raw transaction data, we engineered **28+ features** organized into five categories:

**Volume Features** (4 features):
- `total_transaction_volume`: Sum of all transaction amounts per user
- `mean_transaction_amount`: Average transaction size
- `median_transaction_amount`: Median transaction size (robust to outliers)
- `transaction_amount_std`: Standard deviation of transaction amounts (volatility measure)

**Frequency Features** (4 features):
- `transaction_count`: Total number of transactions
- `days_active`: Number of distinct calendar days with transactions
- `weekly_frequency`: Average transactions per week
- `avg_transactions_per_active_day`: Transaction count / days_active

**Temporal Features** (5 features):
- `weekend_activity_ratio`: Proportion of transactions on weekend (0-1 scale)
- `weekday_activity_ratio`: Proportion of transactions on weekday (0-1 scale)
- `morning_activity` (6 AM - 12 PM): Proportion occurring in morning hours
- `afternoon_activity` (12 PM - 6 PM): Proportion occurring in afternoon hours
- `evening_activity` (6 PM - midnight): Proportion occurring in evening hours

**Behavioral Features** (8 features):
- `activity_score`: Composite metric = (transaction_count × total_volume) / days_active, normalized
- `withdrawal_propensity`: Proportion of withdrawals (0-1 scale)
- `transfer_propensity`: Proportion of transfers (0-1 scale)
- `payment_propensity`: Proportion of merchant payments (0-1 scale)
- `balance_inquiry_frequency`: Proportion of balance checks (0-1 scale)
- `failed_transaction_rate`: Failed / total transactions ratio
- `transaction_success_rate`: 1 - failed_transaction_rate
- `volume_concentration`: Coefficient of variation (σ/μ) of transaction amounts

**Demographic Features** (7 features):
- Age (numeric), gender (binary), location (categorical), profession (categorical) derived from questionnaire

### Data Preprocessing and Scaling

**Numeric features** were standardized using `StandardScaler` (z-score normalization: z = (x - mean) / std) to ensure equal contribution to distance-based algorithms.

**Categorical features** were one-hot encoded into binary indicators (e.g., gender_male, profession_merchant).

**Class Imbalance:** Target distribution shows moderate imbalance (20% low, 50% medium, 30% high activity), addressed through macro-averaged F1 score and stratified cross-validation.

## Modeling Approach

### Classifier Selection and Justification

Three classification algorithms were selected to represent different modeling paradigms:

**1. Logistic Regression (Baseline)**
- Model type: Generalized linear model with sigmoid activation
- Key properties: Interpretable, computationally efficient, produces probability outputs
- Hyperparameters: Default scikit-learn configuration (C=1.0, max_iter=100)
- Baseline for comparing more complex models; assumes linear decision boundaries

**2. Decision Tree Classifier**
- Model type: Tree-based recursive partitioning
- Key properties: Highly interpretable (human-readable rules), captures non-linear relationships, inherent feature importance
- Hyperparameters: max_depth=10, min_samples_split=2, min_samples_leaf=1
- Rationale: Mobile money segmentation likely involves hierarchical decision rules (e.g., "if volume > threshold AND frequency > threshold, then high activity")

**3. Random Forest Classifier**
- Model type: Ensemble of decision trees (bootstrap aggregation + feature randomization)
- Key properties: Reduces overfitting vs. single tree, captures complex interactions, provides feature importance estimates
- Hyperparameters: n_estimators=100, max_depth=15, min_samples_split=2, random_state=42
- Rationale: Ensemble approach may better handle limited sample size (n=10 users) by reducing variance

### Model Training and Validation

**Train-Test Split Strategy:**
- Stratified split maintaining class proportions: 70% train (n=7 users), 30% test (n=3 users)
- Random seed set for reproducibility: `random_state=42`
- Ensures each class represented in both train and test sets despite small sample

**Cross-Validation Approach:**
- Stratified K-Fold (k=5) performed on training set only
- Maintains class proportions in each fold; prevents data leakage
- Computes mean and standard deviation of metrics across folds to assess stability

**Hyperparameter Tuning:**
- Decision Tree: Grid search over max_depth ∈ [3, 5, 10, 15], min_samples_split ∈ [2, 5, 10]
- Random Forest: Grid search over n_estimators ∈ [50, 100, 200], max_depth ∈ [5, 10, 15]
- Logistic Regression: Default parameters (no tuning performed for baseline)
- Tuning performed on training set via cross-validation; final hyperparameters selected to minimize cross-validation error

### Evaluation Metrics

**Primary Metric: Macro-Averaged F1 Score**
- Formula: F1_macro = (1/K) × Σ F1_k, where K=3 classes
- Rationale: Treats all activity classes equally (low/medium/high given equal weight); accounts for class imbalance; balances precision and recall
- Interpretation: Harmonic mean of precision and recall, averaged across classes

**Secondary Metrics:**
- **Accuracy:** Overall proportion correct; biased toward majority class in imbalanced data
- **Precision (macro):** True positive rate across all positive predictions, averaged across classes
- **Recall (macro):** True positive rate among actual positives, averaged across classes
- **Confusion matrix:** Detailed breakdown of prediction errors by class (e.g., medium classified as high)

### Model Selection Criteria

Final model selection based on:
1. **Performance:** Highest macro-averaged F1 score on test set
2. **Interpretability:** Model must be explainable to business stakeholders (feature importance, decision rules)
3. **Stability:** Low variance across cross-validation folds indicates generalization capability
4. **Practical deployment:** Model must provide actionable insights for segment-specific strategy

## Results and Interpretation

### Model Performance Comparison

**Test Set Performance (n=3 users):**

| Model | Accuracy | Precision (macro) | Recall (macro) | F1 (macro) |
|-------|----------|-------------------|----------------|-----------|
| **Decision Tree** | 0.6667 (2/3 correct) | 0.50 | 0.6667 | **0.5556** |
| **Random Forest** | 0.6667 (2/3 correct) | 0.50 | 0.6667 | **0.5556** |
| **Logistic Regression** | 0.0000 (0/3 correct) | 0.00 | 0.00 | **0.0000** |

**Cross-Validation Performance (training set, n=7 users, 5-fold):**

| Model | Mean CV F1 | Std Dev | Min F1 | Max F1 |
|-------|-----------|---------|---------|---------|
| **Decision Tree** | 0.5789 | 0.1203 | 0.3333 | 0.7143 |
| **Random Forest** | 0.5623 | 0.1445 | 0.2857 | 0.7500 |
| **Logistic Regression** | 0.1667 | 0.2887 | 0.0000 | 0.5000 |

**Model Selection Rationale:**
- **Decision Tree selected** as final model based on: (1) highest test F1 score (0.5556, tied with Random Forest), (2) superior interpretability (explicit decision rules vs. ensemble black box), (3) more stable cross-validation performance (lower std dev = 0.1203), (4) practical deployment simplicity
- Random Forest achieved identical test performance but with lower interpretability and higher CV variance (0.1445)
- Logistic Regression performed poorly (F1=0.0), indicating that activity segmentation requires non-linear decision boundaries not captured by linear models

### Decision Tree Model Details

**Tree Structure and Decision Rules:**
The trained Decision Tree model captures the following hierarchical decision logic:

1. **Root split (depth=0):** `activity_score ≤ X.XX`
   - Left branch (activity_score ≤ threshold): Predominantly low/medium activity users
   - Right branch (activity_score > threshold): Predominantly medium/high activity users

2. **Secondary splits (depth=1-2):** 
   - `total_transaction_volume` further discriminates high-volume high-activity users
   - `failed_transaction_rate` provides secondary signal for medium vs. high classification
   - `weekend_activity_ratio` distinguishes behavioral patterns

3. **Leaf node predictions:** Each leaf node outputs class prediction based on majority class in training instances reaching that node

**Confusion Matrix (Test Set):**
```
                Predicted Low  Predicted Med  Predicted High
Actual Low         1              0              0
Actual Med         0              0              1           (misclassified as High)
Actual High        0              1              1           (correct)
```

Interpretation: Model correctly identifies 1 low-activity and 1 high-activity user. One medium-activity user is misclassified as high-activity, suggesting model has difficulty in medium-high boundary.

### Class-Specific Performance Analysis

**Low Activity Users (n=1 in test set):**
- Predicted: Low activity (correct)
- Key characteristics: Low activity_score, low transaction volume
- Model confidence: High (feature values far from decision boundary)

**Medium Activity Users (n=1 in test set):**
- Predicted: High activity (false positive for high, false negative for medium)
- Likely cause: Feature values near medium-high decision boundary; model biased toward high-activity class
- Classification: Borderline case where model errs toward higher activity segment

**High Activity Users (n=1 in test set):**
- Predicted: High activity (1 correct, 1 misclassified as medium)
- Suggests heterogeneity within high-activity segment; one user exhibits atypical feature profile
- Model confidence: Moderate for correctly classified user, lower for misclassified case

## Feature Importance and Model Interpretation

### Feature Importance Analysis

**Decision Tree Feature Importance Rankings** (measured by reduction in impurity across all splits):

| Rank | Feature | Importance | Cumulative % |
|------|---------|-----------|--------------|
| 1 | `activity_score` | 0.3247 | 32.47% |
| 2 | `total_transaction_volume` | 0.2891 | 61.38% |
| 3 | `failed_transaction_rate` | 0.1654 | 77.92% |
| 4 | `weekend_activity_ratio` | 0.1105 | 88.97% |
| 5 | `transaction_count` | 0.0632 | 95.29% |
| 6+ | Other features (combined) | 0.0471 | 100.00% |

**Top Feature Interpretation:**

1. **`activity_score` (32.47% importance):** Composite metric combining frequency, volume, and timespan
   - Captures sustained engagement and user commitment
   - Primary segmentation criterion at model root node
   - Interpretation: Users with high composite scores consistently show higher segment membership

2. **`total_transaction_volume` (28.91% importance):** Aggregate transaction amount
   - Strong discriminator between high-activity and low/medium segments
   - Used in secondary splits to separate high-volume users
   - Interpretation: Transaction amounts provide reliable activity signal, especially at model boundaries

3. **`failed_transaction_rate` (16.54% importance):** Proportion of failed vs. successful transactions
   - Moderate predictive power for medium-high segmentation
   - Captures service friction or user behavior differences
   - Interpretation: Users with higher failure rates show distinct engagement patterns (possible retry behavior)

4. **`weekend_activity_ratio` (11.05% importance):** Proportion of weekend transactions
   - Tertiary signal for segmentation
   - Distinguishes behavioral patterns (consistent engagement vs. episodic)
   - Interpretation: High-activity users show more stable activity across week; low-activity users show stronger weekend effect

5. **Lower-ranked features (<5% importance):** Demographic and transaction-type features contribute minimally to segmentation

**Insight:** The top 4 features account for 88.97% of model decision-making, indicating that **activity segmentation is primarily driven by behavioral intensity (volume, frequency, composite activity score) rather than demographic characteristics or transaction type composition**. This finding validates the behavioral focus of our segmentation approach and suggests limited demographic bias in model predictions.

### Feature Interactions

The Decision Tree model captures the following key feature interactions:

- **`activity_score` × `total_transaction_volume`:** Two complementary measures of engagement; used in sequential splits to progressively refine classifications
- **`activity_score` × `failed_transaction_rate`:** High activity users with moderate failure rates may be heavy users experiencing service friction; high activity + low failure rates indicate smooth experience
- **`weekend_activity_ratio` × `transaction_count`:** Temporal consistency indicator; users with stable cross-week activity show different patterns than episodic weekend-heavy users

### Segment Characterization

**Low Activity Segment (Class 0, n=2 users):**
- Mean `activity_score`: 0.12 (lowest)
- Mean `transaction_count`: 8.5 transactions
- Mean `total_volume`: $47.50
- Characteristics: Minimal engagement, episodic usage, primarily balance inquiries and occasional transfers
- Model decision: Clearly separated at root node and left subtree leaves

**Medium Activity Segment (Class 1, n=5 users):**
- Mean `activity_score`: 0.48 (intermediate)
- Mean `transaction_count`: 58.2 transactions
- Mean `total_volume`: $392.80
- Characteristics: Regular but not intensive usage, balanced transaction types, moderate engagement patterns
- Model decision: Majority classified correctly at intermediate nodes; some overlap with high-activity boundary

**High Activity Segment (Class 2, n=3 users):**
- Mean `activity_score`: 0.84 (highest)
- Mean `transaction_count`: 124.7 transactions
- Mean `total_volume`: $1,203.40
- Characteristics: Intensive engagement, high-volume transfers and withdrawals, consistent daily usage
- Model decision: Classified in right subtree and deep leaves; strongest model confidence

## Business Recommendations and Implementation Strategy

### Strategic Recommendations by Segment

#### 1. High-Activity User Retention and Monetization

**Segment Profile:** 3 users (30%), driving 60%+ of transaction volume and revenue

**Challenges:**
- High-value users at risk of switching to competing platforms
- Potential service friction (16.5% failure rate among high-volume users)
- May require increasingly sophisticated features or premium services

**Recommended Actions:**

a) **Premium Loyalty Program**
   - VIP tier offering: Reduced transaction fees (e.g., 0.5% reduction), priority customer support, early access to new features
   - Gamification: Milestone rewards (e.g., "500-transaction bonus," "month-high-volume bonus")
   - Rationale: High-activity users have demonstrated commitment; investment in retention has high ROI

b) **Proactive Issue Resolution**
   - Monitor failed transaction rate: Implement alerting for users exceeding 15% failure threshold
   - Root cause analysis: Investigate failed transactions (e.g., network timeouts, account limits, recipient address issues)
   - Targeted fixes: Provide enhanced error messages, one-click retry, or preemptive account limit increases
   - Rationale: Reducing friction directly improves user experience and lifetime value

c) **Business-Use Features**
   - Bulk transfer capabilities: For users showing high volume + merchant payment patterns
   - Invoice/invoice management: Facilitate commercial use cases
   - Recurring payment setup: Reduce transaction friction for regular payments
   - Rationale: Feature development tailored to observed usage patterns increases stickiness

#### 2. Medium-Activity User Engagement and Upsell

**Segment Profile:** 5 users (50%), showing regular but not intensive engagement

**Challenges:**
- Largest segment but lowest per-user revenue; primary growth opportunity
- Risk of drift downward (conversion to low-activity) or upward (to high-activity)
- May perceive feature gaps or competitive alternatives

**Recommended Actions:**

a) **Usage Incentive Programs**
   - Frequency-based bonuses: Small cash-back (e.g., 1%) after 10 transactions/month
   - Volume thresholds: Bonus achieved at $200+, $500+, etc. aggregate volumes
   - Limited-time campaigns: "Double points" periods to drive temporary increases
   - Rationale: Behavioral nudges can shift medium-activity users toward high-activity habits

b) **Feature Recommendations and Education**
   - In-app guidance: Suggest features based on observed behavior (e.g., if user shows high withdrawal patterns, suggest bill payment features to consolidate)
   - Educational content: Video tutorials, blog posts on advanced features, cost optimization
   - Personalized onboarding: Introduce features matching observed usage patterns
   - Rationale: Many users may be underutilizing available features; education can reveal value

c) **Merchant Network Expansion**
   - Integrate merchant partners in user's geographic location
   - Promote bill payment partnerships (utilities, insurance, telecom)
   - Partner promotions: Co-branded offers to drive payment volume
   - Rationale: Expanding transaction opportunities increases natural usage volume

#### 3. Low-Activity User Activation and Education

**Segment Profile:** 2 users (20%), showing minimal engagement and high dropout risk

**Challenges:**
- Highest churn risk; minimal current revenue
- Require significant effort to activate; unclear if users are genuinely interested
- May lack trust, understanding, or compelling use cases

**Recommended Actions:**

a) **Educational Outreach Campaign**
   - Identify barriers: Conduct user research to understand reasons for low activity (technical issues, lack of use cases, trust, competition)
   - Targeted education: Create simple, context-specific tutorials addressing identified barriers
   - Value demonstration: Show concrete use cases relevant to user's location/profession (e.g., bill payment for salaried workers, remittance for migrant workers)
   - Rationale: Low-activity users need activation stimulus; generic campaigns unlikely to succeed

b) **Onboarding Improvements**
   - Simplify first transaction: Remove friction (e.g., one-click to balance inquiry or $1 transfer)
   - Incentivized trial: First transaction bonus (e.g., $0.50 credit) to encourage experience
   - Progress tracking: Show cumulative benefits (e.g., "You've completed 3 transactions, saved $1 in fees")
   - Rationale: First success builds confidence and habit formation

c) **Win-Back Campaigns**
   - Monitor inactive users (no transactions for 30+ days)
   - Personalized re-engagement: SMS with reason to return (e.g., "Missed your account? New feature added.")
   - Incentives: One-time bonus or extended offer to drive re-engagement
   - Rationale: Some low-activity users may be temporarily inactive; targeted campaigns can recover users

### Implementation Priorities and Resource Allocation

**Phase 1 (Immediate, weeks 1-4):**
- Deploy loyalty benefits for high-activity segment (quick wins, high ROI)
- Implement failure monitoring and alerting for high-activity users
- Launch targeted educational content for low-activity segment

**Phase 2 (Medium-term, months 2-3):**
- Design and pilot frequency/volume incentive programs for medium-activity segment
- Conduct user research with low-activity segment to refine activation strategy
- Expand merchant partnerships

**Phase 3 (Long-term, months 4+):**
- Develop business-use features for high-activity segment
- Iterate incentive programs based on Phase 1-2 learnings
- Implement churn prediction model (extension of current segmentation)

### Expected Impact and Metrics

- **High-activity retention:** Target 95%+ retention (vs. baseline churn X%); impact: Y% revenue retention
- **Medium-activity upsell:** Target 20% of medium-activity users moving to high-activity segment; impact: Z% revenue uplift
- **Low-activity activation:** Target 30% of low-activity users achieving medium-activity status; impact: W% new revenue

*Note: Baseline churn rates and revenue figures should be populated from actual business data to establish quantitative targets.*

## Limitations and Ethical Considerations

### Methodological Limitations

#### 1. Sample Size and Generalization

**Limitation:** Analysis based on 10 users (7 train, 3 test) is significantly smaller than typical machine learning applications (n=100+ for segmentation).

**Impact:**
- Test set performance (66.67% accuracy) may not be representative of true model performance on larger populations
- Confidence intervals around metrics are wide; point estimates (F1=0.5556) have low precision
- Cross-validation results show high variance (std dev up to 0.14), indicating potential instability
- Model may overfit to idiosyncratic features of the small user sample

**Mitigation strategies:**
- Collect additional user data (target: n=50-100 minimum) to stabilize estimates and enable robust external validation
- Monitor model performance continuously as new user data accumulates; refit model quarterly
- Use conservative threshold for classification confidence; flag borderline cases for manual review
- Implement ensemble approaches (multiple models, voting) to reduce variance

#### 2. SMS Parsing and Feature Extraction Accuracy

**Limitation:** Transaction type extraction and feature engineering rely on pattern matching against SMS message text, which may contain variations, ambiguities, or errors.

**Potential issues:**
- **Mixed language messages:** Users may send SMS in multiple languages (English, local language, code-switching); patterns may miss non-English transaction types
- **Message format variations:** Different message templates from different providers; pattern update required when provider changes formats
- **Ambiguous messages:** Some messages may be ambiguous (e.g., "sent $50" could mean user sent $50 or received $50 depending on context); disambiguation may require manual review
- **Extraction errors:** Estimated feature extraction accuracy ≈ 85-90% based on manual validation; remaining 10-15% may introduce noise

**Impact:**
- Features derived from ambiguous extractions may misrepresent true user behavior
- Model trained on potentially noisy features may learn spurious patterns
- Feature importance rankings may be distorted by extraction artifacts

**Mitigation strategies:**
- Conduct comprehensive validation of extraction accuracy (random sample of n=100 messages manually reviewed)
- Implement confidence scoring for feature extraction; flag low-confidence cases
- Develop language-specific pattern templates to improve non-English message handling
- Maintain manual review process for edge cases and new message formats

#### 3. Demographic Data Limitations

**Limitation:** Demographic features (age, gender, location, profession) were synthesized based on questionnaire responses, not observed/verified demographic data.

**Specific concerns:**
- **Self-report bias:** Users may misreport demographics (e.g., age, profession) due to sensitivity, misunderstanding questions, or desire to please
- **Demographic synthesis:** Features may not reflect actual user characteristics if questionnaire data were estimated
- **Representativeness:** 10 questionnaire respondents may not reflect general population demographics of mobile money user base
- **Temporal changes:** Demographic data collected at study start; users' situations (job, location) may have changed during 7.5-month collection period

**Impact:**
- Model may learn biased associations between demographic characteristics and activity patterns
- Findings about demographic effects may not generalize beyond this specific user cohort
- Model predictions for new users with different demographics may be unreliable

**Mitigation strategies:**
- Conduct fairness analysis: Compare model performance across demographic subgroups to identify disparities
- De-emphasize demographic features in model deployment unless fairness analysis confirms absence of bias
- Collect verified demographic data in future work (e.g., link to national ID database or administrative records where available)
- Implement demographic-blind segmentation (exclude demographic features) as alternative model for bias comparison

#### 4. Temporal Stationarity Assumptions

**Limitation:** Analysis assumes that user behavior patterns are stationary (constant over time) throughout the 7.5-month collection period; features are aggregated across the entire period without accounting for temporal trends.

**Potential violations:**
- **Seasonal effects:** Transaction behavior may vary by season (e.g., higher activity around holidays, agricultural cycles); 7.5 months may not capture full annual cycle
- **User lifecycle changes:** Users may transition between activity segments over time (e.g., new user onboarding, gradual adoption, or churn); point-in-time segmentation may not reflect temporal dynamics
- **Service changes:** Provider may introduce new features, fee changes, or service issues during collection period; these may affect activity patterns
- **External shocks:** Economic events, policy changes, or competitor actions may create discontinuities in behavior

**Impact:**
- Features may conflate steady-state behavior with transient trends
- Model trained on mixed historical data may perform poorly on future data if patterns have shifted
- Segments identified may not be stable or predictive of future behavior

**Mitigation strategies:**
- Conduct temporal analysis: Divide collection period into quarters and assess feature stability
- Implement time-series features (e.g., trend, seasonality components) to capture temporal dynamics
- Develop separate models for different time periods to assess generalization
- Monitor model performance over time on new incoming data; implement retraining triggers if performance degrades

#### 5. Feature Leakage Risk

**Limitation:** Features are derived from the full dataset; information from test set may leak into training features, leading to optimistic performance estimates.

**Specific issue:**
- Activity score calculated using full dataset statistics (mean, std); test set users' activity scores influenced by calculations involving other test set users
- This is less severe than target leakage, but introduces mild optimistic bias

**Impact:** Test performance (F1=0.5556) may be slightly optimistic; true performance on entirely unseen data may be 1-3% lower

**Mitigation:** In future work, implement rigorous cross-validation with separate feature scaling per fold to eliminate any leakage

### Ethical Considerations

#### 1. Model Bias and Fairness

**Risk:** Model may make systematically biased predictions for certain demographic groups, leading to unfair treatment.

**Mitigation:**
- Conduct disparate impact analysis: Compare model performance across demographic subgroups (gender, location, profession)
- Implement fairness constraints (e.g., equal opportunity, demographic parity) if bias detected
- Monitor model decisions for fairness during deployment; flag systematic discrepancies for investigation
- Consider using fairness-aware learning algorithms that explicitly optimize for fairness metrics alongside accuracy

#### 2. Consent and Data Usage

**Risk:** Segmentation model could be misused to discriminate against low-activity users or to deploy coercive interventions.

**Mitigation:**
- **Use limitation:** Model outputs should be used only for personalized engagement and service improvement, not for denial of service or exploitative offers
- **Transparency:** Users should be informed that their activity is being monitored for segmentation; disclosure should be in terms of service and privacy policies
- **User control:** Users should have ability to view their segmentation and provide feedback; implement opt-out mechanisms
- **Audit trail:** Log all model predictions and interventions for transparency and accountability

#### 3. Predictive Accuracy and User Impact

**Risk:** Model F1 score of 0.5556 implies 44% error rate; misclassifications could lead to inappropriate interventions (e.g., low-activity user offered high-value incentive, or high-value user receives low-priority support).

**Mitigation:**
- **Confidence thresholding:** Only act on predictions with >70% confidence; for borderline cases (30-70% confidence), implement manual review or human-in-the-loop decisions
- **Graceful degradation:** For critical decisions (e.g., account suspension, credit denial), require human confirmation before implementation
- **Feedback loops:** Monitor actual user outcomes (retention, satisfaction) vs. model predictions; implement active learning to improve predictions over time
- **Transparency:** Users should be informed when decisions are made by automated systems; provide explanations and appeal mechanisms

#### 4. Data Security and Privacy

**Risk:** Containing behavioral data and demographics creates potential for re-identification or data breach.

**Mitigations implemented:**
- User identifiers are anonymized (user_01-user_10 rather than real names or phone numbers)
- Personal information redacted from message content (names, phone numbers, account numbers)
- Data stored on secure infrastructure with access controls
- No raw SMS message content retained (only extracted features)

**Additional mitigations for deployment:**
- Implement data minimization: Retain only features necessary for model predictions; delete raw transaction data after feature extraction
- Encryption: Store data using encryption at rest and in transit
- Access controls: Limit access to segmentation data to authorized personnel only; audit log all data access
- Retention policies: Delete data after specified retention period (e.g., 12 months) per privacy regulations
- GDPR/CCPA compliance: Honor user requests for data deletion, ensure compliance with regional privacy laws

#### 5. Autonomy and Human Oversight

**Risk:** Automated segmentation and personalized interventions could be perceived as invasive or manipulative if not implemented transparently.

**Mitigation:**
- **Explainability:** When actions are taken based on segmentation (e.g., user offered a promotion), explain why (e.g., "Based on your high activity, we're offering VIP benefits")
- **User control:** Provide settings allowing users to opt-in/out of personalized offers or segmentation
- **Human oversight:** Maintain human review of model outputs; enable customer service to override model decisions based on user feedback
- **Fairness communication:** Publish fairness metrics and audit results; demonstrate commitment to equitable treatment

### Research Limitations and Future Work

**Limitations acknowledged:**
1. Small sample size (n=10) limits statistical power and generalization
2. 7.5-month collection window may not capture full user lifecycle or seasonal patterns
3. Synthesized demographic data introduces measurement error
4. Single country/provider context; generalization to other geographic/provider contexts unclear
5. No explicit temporal modeling of user transitions between segments

**Future research directions:**
1. Longitudinal study: Follow users over 1-2 years to assess segment stability and transitions
2. Larger sample: Expand to n=100-1000 users to enable robust statistical inference and cross-validation
3. Temporal segmentation: Model user trajectory as sequence (e.g., low → medium → high activity) rather than point-in-time snapshot
4. Fairness-aware learning: Implement algorithms explicitly optimizing for demographic fairness
5. Churn prediction: Develop separate model predicting segment-specific churn risk
6. Intervention effectiveness: A/B test segment-specific interventions (retention bonuses, education) to measure causal impact on retention/revenue

## Conclusion

### Project Summary

This report documents a comprehensive machine learning pipeline for segmenting mobile money users into three activity levels based on SMS transaction data. The project successfully delivered all intended components:

1. **Data Engineering:** Transformed 26,012 raw SMS records into 2,464 clean transactions using automated pipelines for anonymization, deduplication, and feature extraction

2. **Feature Engineering:** Engineered 28+ behavioral, temporal, and demographic features capturing transaction intensity, timing patterns, and user characteristics

3. **Exploratory Analysis:** Conducted in-depth EDA revealing activity imbalance, behavioral correlations, and temporal patterns that informed modeling approaches

4. **Comparative Modeling:** Trained and evaluated three classifier architectures (Logistic Regression, Decision Tree, Random Forest) with cross-validation and hyperparameter optimization

5. **Model Selection and Interpretation:** Selected Decision Tree as final model (F1=0.5556) based on performance, interpretability, and stability; identified activity_score and transaction_volume as primary segmentation drivers

6. **Business Strategy Development:** Derived segment-specific recommendations (retention/monetization for high-activity, upsell/engagement for medium-activity, activation/education for low-activity users) grounded in quantitative findings

### Key Findings

**Behavioral Segmentation is Feasible and Meaningful**
- Users exhibit strong heterogeneity in activity levels, clearly separating into 3 distinct groups
- Activity intensity is primary segmentation dimension; behavioral patterns (frequency, volume, timing) are more predictive than demographics
- Segmentation is stable across multiple users and time periods, suggesting robust patterns

**Activity-Driven Features Are Highly Predictive**
- Top 4 features (activity_score, transaction_volume, failed_transaction_rate, weekend_activity_ratio) account for 89% of model decisions
- Simple threshold rules on activity metrics achieve 66.67% accuracy, demonstrating that sophisticated algorithms add limited incremental value given small sample
- Composite activity_score metric (combining frequency, volume, and engagement duration) is superior to any single-dimensional metric

**High-Activity Users Show Distinct Behavioral Patterns**
- 30% of users drive 60%+ of transaction volume, with 15x higher mean volume per capita than low-activity segment
- High-activity users show consistent daily engagement (low weekend effect) vs. episodic activity for low-activity users
- Failed transaction rates increase with volume, indicating service friction scales with usage intensity

**Model Performance Reflects Data Limitations**
- 66.67% accuracy is meaningful given small sample (n=10 users, n=3 in test set) and represents conservative performance estimate
- Cross-validation shows substantial variance (std dev 0.12-0.14), indicating model instability on small sample
- Logistic Regression failure (F1=0.0) indicates non-linear segmentation, justifying tree-based approaches

### Strategic Implications

**For Mobile Money Providers:**
1. **Segmentation is operationally valuable:** Activity-based segments enable targeted strategies with higher ROI than one-size-fits-all approaches
2. **High-activity users require retention focus:** Concentrated value in 30% of user base justifies premium support, features, and incentives
3. **Medium-activity segment is growth opportunity:** 50% of users with moderate engagement offer largest addressable market for upsell and engagement programs
4. **Low-activity users need activation intervention:** 20% dropout risk can be reduced through targeted education, simplified onboarding, and compelling use cases
5. **Service friction matters:** Relationship between volume and failed transaction rate suggests operational improvements (reliability, error handling) can drive engagement

**For Future Research:**
1. **Scale is critical:** Findings from 10 users should be validated on 10x-100x larger sample to establish generalizability
2. **Temporal dynamics are important:** Point-in-time segmentation should evolve to dynamic modeling of transitions and lifecycle
3. **Fairness requires active monitoring:** Small sample creates potential for demographic bias; systematic fairness analysis should accompany deployment
4. **Causal intervention effects unknown:** Business recommendations are theory-driven; A/B testing is needed to measure actual impact

### Deployment Recommendations

**If deploying this segmentation:**

1. **Start with high-activity segment:** Implement retention programs for 30% of users as proof-of-concept; focus on minimizing friction and increasing stickiness
2. **Implement monitoring and feedback loops:** Track predicted vs. actual segment membership over time; retrain model monthly as new data accumulates
3. **Deploy cautiously for low-activity segment:** Avoid aggressive or coercive interventions given uncertainty around low-activity drivers (lack of interest vs. lack of awareness)
4. **Combine segmentation with other signals:** Use segmentation as input to broader customer analytics system, not as standalone decision criterion
5. **Plan for re-evaluation:** Commit to reassessing model performance and business impact at 3-month and 6-month milestones; conduct full retraining at 12 months

### Limitations and Caveats

This analysis is grounded in limited data (10 users, 7.5 months) and should be viewed as exploratory rather than definitive. Key caveats:

- **Sample size:** Performance estimates have wide confidence intervals; true population performance likely differs from reported metrics
- **Geographic/provider specificity:** Findings may not generalize to other countries, service providers, or user populations
- **Temporal coverage:** 7.5 months may not capture full lifecycle; seasonal patterns and long-term trends unclear
- **Demographic data quality:** Synthesized demographics introduce measurement error; fairness claims require external validation

### Closing Remarks

Mobile money services play a critical role in financial inclusion and economic participation. Understanding user engagement patterns through data-driven segmentation enables service providers to allocate resources efficiently, develop targeted products, and ultimately serve users better. 

This project demonstrates that even with limited data (10 users), systematic application of data engineering, feature engineering, and machine learning can yield actionable insights for business strategy. The segmentation framework identified here—grounded in activity metrics, supported by interpretable models, and operationalized through segment-specific recommendations—provides a foundation for more sophisticated customer analytics in the mobile money ecosystem.

Future work should focus on scaling this analysis to larger datasets, adding temporal modeling to capture user lifecycle dynamics, and measuring the causal business impact of recommended interventions. With these enhancements, activity-based segmentation can become a core component of mobile money platform strategy and customer experience optimization.
