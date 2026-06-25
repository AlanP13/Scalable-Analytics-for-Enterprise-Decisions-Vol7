"""
Lab 12 - Logistic Regression (Admit Dataset)
Author: Alan B. Palayil
Course: ITS-836 – Data Science & Big Data Analytics

This script:
- Loads 'Lab 12 - Admit.xls' (admissions dataset)
- Summarizes the data
- Builds a logistic regression model:
    admit (0/1) ~ gre + gpa + rank
- Evaluates model with accuracy, confusion matrix, classification report, ROC curve, and AUC
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore

from sklearn.model_selection import train_test_split  # type: ignore
from sklearn.preprocessing import StandardScaler  # type: ignore
from sklearn.linear_model import LogisticRegression  # type: ignore
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    roc_auc_score,
)  # type: ignore

plt.style.use("seaborn-v0_8")

# ============================================================
# 1) Load the dataset
# ============================================================

print("=" * 80)
print("Loading Admit dataset from Excel")
print("=" * 80)

# Adjust path if needed
file_path = r"C:\Users\alanp\Downloads\Lab 12 - Admit.xls"

df = pd.read_excel(file_path)

print("\nFirst 10 rows:")
print(df.head(10))

print("\nDataset info:")
print(df.info())

print("\nSummary statistics:")
print(df.describe(include="all"))

# Expected columns: 'admit', 'gre', 'gpa', 'rank'
required_cols = ["admit", "gre", "gpa", "rank"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found. Check your Excel headers.")

# Drop any rows with missing values in the required columns
df_clean = df[required_cols].dropna().copy()

print("\nNumber of rows after dropping missing values:", len(df_clean))
print("\nAdmission rate (proportion of admit=1):")
print(df_clean["admit"].value_counts(normalize=True))

# ============================================================
# 2) Basic EDA: Admission rate by rank
# ============================================================

print("\n" + "=" * 80)
print("Exploring admission probability by undergraduate rank")
print("=" * 80)

admit_by_rank = df_clean.groupby("rank")["admit"].mean()
print("\nAdmission rate by rank:")
print(admit_by_rank)

plt.figure(figsize=(6, 4))
admit_by_rank.plot(kind="bar")
plt.title("Admission Rate by Undergraduate Rank")
plt.xlabel("Rank (1 = best, 4 = worst)")
plt.ylabel("Proportion Admitted")
plt.tight_layout()
plt.savefig("admit_rate_by_rank.png")
plt.show()

# ============================================================
# 3) Prepare Data for Logistic Regression
# ============================================================

print("\n" + "=" * 80)
print("Preparing train/test data for logistic regression")
print("=" * 80)

X = df_clean[["gre", "gpa", "rank"]]
y = df_clean["admit"]

# Train/test split (70% train, 30% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

print("Train size:", X_train.shape[0])
print("Test size:", X_test.shape[0])

# ============================================================
# 4) Build Logistic Regression Model (with scaling)
# ============================================================

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

log_reg = LogisticRegression(
    random_state=42,
    max_iter=1000,
    solver="lbfgs"
)

log_reg.fit(X_train_scaled, y_train)

# Coefficients
coef_df = pd.DataFrame(
    {
        "feature": ["intercept"] + X.columns.tolist(),
        "coefficient": np.concatenate(([log_reg.intercept_[0]], log_reg.coef_[0])),
    }
)

print("\nLogistic Regression Coefficients:")
print(coef_df)

# ============================================================
# 5) Predictions and Evaluation
# ============================================================

print("\n" + "=" * 80)
print("Evaluating logistic regression model")
print("=" * 80)

# Predicted class labels
y_pred = log_reg.predict(X_test_scaled)

# Predicted probabilities (for ROC)
y_proba = log_reg.predict_proba(X_test_scaled)[:, 1]

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy on test set: {accuracy:.4f}")

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix:")
print(cm)

# Classification report (precision, recall, F1)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Plot confusion matrix
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
plt.title("Confusion Matrix - Logistic Regression (Admit)")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig("logreg_confusion_matrix.png")
plt.show()

# ROC curve & AUC
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
auc_score = roc_auc_score(y_test, y_proba)
print(f"\nROC AUC: {auc_score:.4f}")

plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, label=f"Logistic Regression (AUC = {auc_score:.3f})")
plt.plot([0, 1], [0, 1], "k--", label="Random Guess")
plt.title("ROC Curve - Logistic Regression (Admit)")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("logreg_roc_curve.png")
plt.show()

print("\n=== End of Lab 12 – Logistic Regression (Admit Dataset) ===")
