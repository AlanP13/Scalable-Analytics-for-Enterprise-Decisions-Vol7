"""
Lab 11 - Linear Regression (Insurance Dataset)
Author: Alan B. Palayil
Course: ITS-836 – Data Science & Big Data Analytics

This script:
- Loads the 'Lab 11 - Insurance.xls' dataset
- Summarizes the data
- Builds two regression models:
    RQ1: charges ~ bmi (simple linear regression)
    RQ2: charges ~ age + smoker (multiple linear regression)
- Produces basic plots for regression diagnostics
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore
import statsmodels.api as sm  # type: ignore

plt.style.use("seaborn-v0_8")

# ============================================================
# 1) Load the dataset
# ============================================================

# Adjust the path if needed
file_path = rfile_path = r"C:\Users\alanp\Downloads\Lab 11 - Insurance.xls"


print("=" * 80)
print("Loading Insurance dataset from Excel")
print("=" * 80)

df = pd.read_excel(file_path)

print("\nFirst 10 rows:")
print(df.head(10))

print("\nDataset info:")
print(df.info())

print("\nSummary statistics:")
print(df.describe(include="all"))

# NOTE: Adjust these column names if your actual file uses different labels
# Common expectation for this kind of dataset:
#   age (numeric), bmi (numeric), smoker (yes/no), charges (numeric)

# Make a working copy and drop rows with missing values in required columns
required_cols = ["age", "bmi", "smoker", "charges"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found. Check your Excel headers and update the script.")

df_clean = df[required_cols].dropna().copy()

# Encode smoker as binary (0 = non-smoker, 1 = smoker)
df_clean["smoker_flag"] = df_clean["smoker"].map({"no": 0, "yes": 1})
if df_clean["smoker_flag"].isna().any():
    print("\nWarning: Some 'smoker' values were not 'yes'/'no'. Check data cleanliness.")
    df_clean = df_clean.dropna(subset=["smoker_flag"])

# ============================================================
# 2) Research Question 1: charges ~ bmi (simple linear regression)
# ============================================================

print("\n" + "=" * 80)
print("RQ1: Is there a linear relationship between BMI and medical charges?")
print("=" * 80)

# Scatter plot with regression line
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df_clean, x="bmi", y="charges", alpha=0.6)
plt.title("Scatter Plot: Charges vs BMI")
plt.xlabel("BMI")
plt.ylabel("Charges")
plt.tight_layout()
plt.savefig("RQ1_scatter_charges_vs_bmi.png")
plt.show()

# Prepare data for statsmodels (add constant for intercept)
X1 = sm.add_constant(df_clean["bmi"])
y = df_clean["charges"]

model1 = sm.OLS(y, X1).fit()
print("\nSimple Linear Regression Summary (charges ~ bmi):")
print(model1.summary())

# Regression line plot
plt.figure(figsize=(8, 6))
sns.regplot(data=df_clean, x="bmi", y="charges", line_kws={"color": "red"})
plt.title("Linear Regression: Charges ~ BMI")
plt.xlabel("BMI")
plt.ylabel("Charges")
plt.tight_layout()
plt.savefig("RQ1_regline_charges_vs_bmi.png")
plt.show()

# Residuals vs Fitted for RQ1
fitted1 = model1.fittedvalues
residuals1 = model1.resid

plt.figure(figsize=(8, 6))
sns.scatterplot(x=fitted1, y=residuals1, alpha=0.6)
plt.axhline(0, color="red", linestyle="--")
plt.title("RQ1: Residuals vs Fitted Values")
plt.xlabel("Fitted values (Predicted Charges)")
plt.ylabel("Residuals")
plt.tight_layout()
plt.savefig("RQ1_residuals_vs_fitted.png")
plt.show()

# Histogram of residuals for RQ1
plt.figure(figsize=(8, 6))
sns.histplot(residuals1, kde=True)
plt.title("RQ1: Distribution of Residuals")
plt.xlabel("Residuals")
plt.tight_layout()
plt.savefig("RQ1_residuals_hist.png")
plt.show()

# ============================================================
# 3) Research Question 2: charges ~ age + smoker (multiple regression)
# ============================================================

print("\n" + "=" * 80)
print("RQ2: Does smoker status affect charges after controlling for age?")
print("=" * 80)

# Prepare predictors
X2 = df_clean[["age", "smoker_flag"]]
X2 = sm.add_constant(X2)  # add intercept

model2 = sm.OLS(y, X2).fit()
print("\nMultiple Linear Regression Summary (charges ~ age + smoker_flag):")
print(model2.summary())

# 2D visualization idea: charges vs age colored by smoker
plt.figure(figsize=(8, 6))
sns.scatterplot(
    data=df_clean,
    x="age",
    y="charges",
    hue="smoker",
    alpha=0.6
)
plt.title("Charges vs Age by Smoker Status")
plt.xlabel("Age")
plt.ylabel("Charges")
plt.legend(title="Smoker")
plt.tight_layout()
plt.savefig("RQ2_scatter_charges_vs_age_smoker.png")
plt.show()

# Residuals vs Fitted for RQ2
fitted2 = model2.fittedvalues
residuals2 = model2.resid

plt.figure(figsize=(8, 6))
sns.scatterplot(x=fitted2, y=residuals2, alpha=0.6)
plt.axhline(0, color="red", linestyle="--")
plt.title("RQ2: Residuals vs Fitted Values")
plt.xlabel("Fitted values (Predicted Charges)")
plt.ylabel("Residuals")
plt.tight_layout()
plt.savefig("RQ2_residuals_vs_fitted.png")
plt.show()

# Histogram of residuals for RQ2
plt.figure(figsize=(8, 6))
sns.histplot(residuals2, kde=True)
plt.title("RQ2: Distribution of Residuals")
plt.xlabel("Residuals")
plt.tight_layout()
plt.savefig("RQ2_residuals_hist.png")
plt.show()

print("\n=== End of Lab 11 – Linear Regression (Insurance Dataset) ===")
