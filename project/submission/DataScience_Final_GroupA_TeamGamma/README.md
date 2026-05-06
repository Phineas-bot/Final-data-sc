# DataScience_Final_GroupA_TeamGamma

## Group Members

- **Member 1** (ID: M001): Data collection, questionnaire, consent form
- **Member 2** (ID: M002): Data cleaning, feature engineering
- **Member 3** (ID: M003): EDA, visualization
- **Member 4** (ID: M004): Modeling, evaluation
- **Member 5** (ID: M005): Interpretation, reporting

## Project Title

Mobile Money User Activity Classification

## Brief Description

This project implements a comprehensive machine learning pipeline to classify mobile money users into three distinct activity segments (low, medium, and high) based on SMS transaction history from MobileMoney and OrangeMoney services. The analysis processes 26,012 raw SMS messages, resulting in 2,464 cleaned transaction records across 10 users. Using behavioral features including transaction volume, frequency, temporal patterns, and demographic characteristics, a Decision Tree classifier achieves 66.67% accuracy in segmenting users. The project demonstrates end-to-end data science methodology from ethical data collection through model deployment, providing actionable insights for mobile money service providers to optimize user engagement, retention, and service design.

## File Structure Explanation

```
DataScience_Final_GroupA_TeamGamma/
├── 1_Data_Collection/
│   ├── consent_form.pdf          # Participant consent documentation
│   ├── data_collection_report.md # Data collection methodology and procedures
│   ├── questionnaire.md          # Survey instrument used for data collection
│   └── raw_data.csv             # Original SMS transaction data
├── 2_Data_Cleaning/
│   ├── cleaning_notebook.ipynb  # Jupyter notebook with data cleaning code
│   ├── cleaned_data.csv         # Processed and anonymized transaction dataset
│   ├── cleaning_report.md       # Detailed cleaning methodology and results
│   └── data_quality_report.csv  # Data quality metrics and validation
├── 3_EDA/
│   ├── eda_notebook.ipynb       # Exploratory data analysis notebook
│   ├── eda_summary.md           # Comprehensive EDA findings and insights
│   ├── eda_summary.csv          # Summary statistics and aggregations
│   └── *.png                    # Visualization files (6 charts total)
├── 4_Modeling/
│   ├── modeling_notebook.ipynb  # Machine learning implementation
│   ├── best_model.joblib        # Trained Decision Tree model
│   ├── performance_summary.md   # Model evaluation and performance analysis
│   ├── model_comparison.csv     # Comparative model performance metrics
│   └── user_features.csv        # Engineered features for modeling
├── 5_Interpretation/
│   ├── interpretation_report.md # Model interpretation and feature importance
│   ├── business_recommendations.md # Actionable business insights
│   ├── feature_importance.csv   # Feature importance rankings
│   ├── example_predictions.csv  # Sample model predictions
│   └── limitations_ethics.md    # Project limitations and ethical considerations
├── 6_Presentation/
│   ├── Presentation_Slides.pdf  # Final presentation slides
│   └── requirements.txt         # Python dependencies (copy)
├── CONTRIBUTIONS.md             # Detailed team member contributions
├── Project_Report.pdf           # Comprehensive final report
└── README.md                    # This file
```

## How to Run the Code

### Prerequisites

- Python 3.8 or higher
- Jupyter Notebook/Lab
- Git (for version control)

### Setup Instructions

1. **Clone or Download the Project:**

   ```bash
   # If using git
   git clone <repository-url>
   cd DataScience_Final_GroupA_TeamGamma
   ```
2. **Create Virtual Environment:**

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
4. **Run the Analysis Pipeline:**

   **Option A: Run Individual Notebooks (Recommended for Understanding)**

   ```bash
   # Start Jupyter Lab
   jupyter lab

   # Then open notebooks in order:
   # 1. 2_Data_Cleaning/cleaning_notebook.ipynb
   # 2. 3_EDA/eda_notebook.ipynb
   # 3. 4_Modeling/modeling_notebook.ipynb
   ```

   **Option B: Run Complete Pipeline (Automated)**

   ```bash
   # Execute the main pipeline script (if available)
   python src/run_pipeline.py
   ```

### Expected Output

- Cleaned dataset: `2_Data_Cleaning/cleaned_data.csv`
- EDA visualizations: `3_EDA/*.png`
- Trained model: `4_Modeling/best_model.joblib`
- Performance metrics: `4_Modeling/model_comparison.csv`
- Feature importance: `5_Interpretation/feature_importance.csv`

### Troubleshooting

- **Import Errors:** Ensure all dependencies are installed with `pip install -r requirements.txt`
- **Jupyter Issues:** Try `jupyter notebook` if `jupyter lab` fails
- **Memory Issues:** The dataset is small (<3K records) so memory shouldn't be an issue
- **Path Issues:** Ensure you're running notebooks from the project root directory

## Dependencies/Requirements

### Python Packages

```
pandas>=1.3.0          # Data manipulation and analysis
numpy>=1.21.0          # Numerical computing
matplotlib>=3.4.0      # Data visualization
seaborn>=0.11.0        # Statistical data visualization
scikit-learn>=1.0.0    # Machine learning algorithms
openpyxl>=3.0.0        # Excel file handling
```

### System Requirements

- **Operating System:** Windows 10+, macOS 10.15+, or Linux
- **RAM:** Minimum 4GB, Recommended 8GB
- **Storage:** 500MB free space
- **Python Version:** 3.8 or higher

### Installation Command

```bash
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl
```

### Optional Dependencies

- `jupyterlab` or `notebook` for interactive development
- `joblib` for model serialization (included with scikit-learn)

---

**Course:** CSC 3221 - Introduction to Data Science
**Instructor:** Dr. Fotsing Kuethe
**Submission Date:** May 3, 2026
