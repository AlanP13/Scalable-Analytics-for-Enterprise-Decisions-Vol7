"""
MSDS-532 Final Project – Topic 2
Vehicle Price Prediction using Extremely Randomized Trees Regression

Purpose:
Import, clean, explore, and model vehicle advertisement data to determine
the most influential attributes when predicting vehicle advertised price.

Final version with automatic dependency installation.

Alan Biju Palayil
June 2026
"""

# ----------------------------------------------------------
# AUTO INSTALL REQUIRED LIBRARIES
# ----------------------------------------------------------

import sys
import subprocess


def install(package):
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", package]
    )


required_packages = {
    "pandas": "pandas",
    "numpy": "numpy",
    "pyreadr": "pyreadr",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "sklearn": "scikit-learn"
}


for module_name, pip_name in required_packages.items():
    try:
        __import__(module_name)
    except ImportError:
        print(f"Installing missing package: {pip_name}")
        install(pip_name)


# ----------------------------------------------------------
# IMPORT LIBRARIES
# ----------------------------------------------------------

import pandas as pd # type: ignore
import numpy as np # type: ignore
import pyreadr # type: ignore

import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore

from sklearn.model_selection import train_test_split # pyright: ignore[reportMissingModuleSource]
from sklearn.ensemble import ExtraTreesRegressor # pyright: ignore[reportMissingModuleSource]
from sklearn.metrics import r2_score # pyright: ignore[reportMissingModuleSource]
from sklearn.metrics import mean_squared_error # pyright: ignore[reportMissingModuleSource]
from sklearn.inspection import permutation_importance # pyright: ignore[reportMissingModuleSource]


# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------

from pathlib import Path

print("\nLoading RData file...")

script_folder = Path(__file__).resolve().parent
rdata_file = script_folder / "Topic_2_car_ads_fp.RData"

if not rdata_file.exists():
    print("\nERROR: RData file not found.")
    print(f"Expected location: {rdata_file}")
    raise FileNotFoundError(rdata_file)

# Read RData
result = pyreadr.read_r(str(rdata_file))

print("\nObjects found inside RData:")
print(result.keys())

# Extract dataframe from first object in file
df = list(result.values())[0]

print("\nPreview:")
print(df.head())

print("\nShape before cleaning:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# ----------------------------------------------------------
# CLEAN DATA
# ----------------------------------------------------------

print("\nCleaning data...")

models_keep = ["L200", "Q3", "CX-5", "XC90"]
df = df[df["Genmodel"].isin(models_keep)]

body_keep = ["SUV", "Pickup"]
df = df[df["Bodytype"].isin(body_keep)]

fuel_keep = ["Petrol", "Diesel"]
df = df[df["Fuel_type"].isin(fuel_keep)]

top_colors = df["Color"].value_counts().nlargest(6).index
df = df[df["Color"].isin(top_colors)]

df = df.dropna()

df = df[
    [
        "Genmodel",
        "Reg_year",
        "Color",
        "Bodytype",
        "Runned_Miles",
        "Gearbox",
        "Fuel_type",
        "Price"
    ]
]

print("\nCleaned shape:")
print(df.shape)

# ----------------------------------------------------------
# EXPLORATORY DATA ANALYSIS
# ----------------------------------------------------------

print("\nSummary statistics:")
print(df.describe())


# Histogram
plt.figure(figsize=(10,6))
sns.histplot(df["Price"], bins=40, kde=True)
plt.xlabel("Advertised Price")
plt.tight_layout()
plt.show()


# Boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="Genmodel", y="Price")
plt.title("Vehicle Price by Model")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()


# ----------------------------------------------------------
# MODEL PREP
# ----------------------------------------------------------

target = "Price"

X = df.drop(columns=[target])
y = df[target]

X = pd.get_dummies(X, drop_first=True)


# ----------------------------------------------------------
# TRAIN TEST SPLIT
# ----------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# ----------------------------------------------------------
# MODEL
# ----------------------------------------------------------

print("\nTraining model...")

model = ExtraTreesRegressor(
    n_estimators=300,
    random_state=42
)

model.fit(X_train, y_train)


# ----------------------------------------------------------
# EVALUATION
# ----------------------------------------------------------

train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)

train_r2 = r2_score(y_train, train_predictions)
test_r2 = r2_score(y_test, test_predictions)

train_rmse = np.sqrt(
    mean_squared_error(y_train, train_predictions)
)

test_rmse = np.sqrt(
    mean_squared_error(y_test, test_predictions)
)

print("\n-----------------------------")
print("MODEL RESULTS")
print("-----------------------------")

print(f"Training R²: {train_r2:.4f}")
print(f"Testing R²: {test_r2:.4f}")
print(f"Training RMSE: {train_rmse:.2f}")
print(f"Testing RMSE: {test_rmse:.2f}")


# ----------------------------------------------------------
# FEATURE IMPORTANCE
# ----------------------------------------------------------

print("\nCalculating feature importance...")

perm_importance = permutation_importance(
    model,
    X_test,
    y_test,
    n_repeats=3,
    random_state=42,
    n_jobs=-1
)

importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": perm_importance.importances_mean
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nTop 10 Most Important Features:")
print(importance_df.head(10))


plt.figure(figsize=(12, 8))
sns.barplot(
    data=importance_df.head(10),
    x="Importance",
    y="Feature"
)

plt.title(
    "Top 10 Most Influential Attributes for Predicting Vehicle Price"
)

plt.tight_layout()
plt.show()


print("\nDone.")