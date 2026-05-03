You are a senior data scientist and machine learning engineer.

Your task is to design and implement a complete end-to-end data science project for a university assignment.

PROJECT TITLE:
Mobile Money User Activity Classification System

OBJECTIVE:
Build a machine learning system that classifies users into three categories:

- Low Activity
- Medium Activity
- High Activity

based on their mobile money transaction behavior.

---

PHASE 1 — DATA HANDLING

1. Load datasets from folder : raw_datasets 
2. Perform data cleaning:

   - Handle missing values (use appropriate strategies: drop or impute)
   - Remove duplicates
   - Normalize inconsistent formats
   - Convert categorical ranges into numeric values
     Example:
     "0-10k" → 5000
     "10k-50k" → 30000
3. Encode categorical variables:

   - Occupation
   - Usage type (personal/business/bills)
   - Weekend usage (Yes/No → 1/0)

---

PHASE 2 — FEATURE ENGINEERING

Create new features:

- transactions_per_month
- avg_transaction_amount
- total_transaction_volume
- deposit_withdraw_ratio
- weekend_activity (binary)
- business_usage (binary)

Create an ACTIVITY SCORE using a weighted formula.

Then define target variable:

LOW: score < threshold_1
MEDIUM: threshold_1 ≤ score < threshold_2
HIGH: score ≥ threshold_2

Make thresholds data-driven (e.g., percentiles).

---

PHASE 3 — EXPLORATORY DATA ANALYSIS

Generate clear and professional visualizations:

- Distribution of activity levels
- Transactions vs occupation
- Avg amount vs activity level
- Correlation heatmap

Include interpretation for each plot.

---

PHASE 4 — MODELING

Split dataset:

- Train: 80%
- Test: 20%

Train the following models:

1. Logistic Regression
2. Decision Tree
3. Random Forest

For each model:

- Train
- Predict
- Evaluate

---

PHASE 5 — EVALUATION

Compute:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

Compare models and identify the best one.

---

PHASE 6 — MODEL INTERPRETATION

- Show feature importance (for tree-based models)
- Explain what drives high activity users

---

PHASE 7 — OUTPUTS

Generate:

1. Cleaned dataset
2. Final dataset with features
3. Trained models
4. Visualizations (saved as PNG files)
5. Evaluation report

---

PHASE 8 — BUSINESS INSIGHTS

Generate a section explaining:

- Key behavioral patterns of users
- What defines high-value users
- Recommendations for telecom/mobile money companies

---

PHASE 9 — PROJECT STRUCTURE

Organize project as:

/project
  ├── data/
  ├── notebooks/
  ├── src/
  ├── models/
  ├── outputs/
  ├── report/

---

PHASE 10 — DOCUMENTATION

Generate:

1. A professional README.md including:

   - Project overview
   - Setup instructions
   - Methodology
   - Results
2. A structured report (Markdown or PDF-ready)

---

TECH STACK:

- Python
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn

---

CODE QUALITY REQUIREMENTS:

- Modular, clean, well-commented code
- Functions for each pipeline stage
- No hardcoding
- Reproducible pipeline

---

BONUS (IMPORTANT):

- Add a simple CLI or script to run the full pipeline
- Ensure code runs from start to finish without manual intervention

---

DELIVERABLE:

A complete, clean, professional, reproducible data science project ready for submission and presentation.
