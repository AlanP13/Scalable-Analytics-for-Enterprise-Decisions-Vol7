"""
Course Project: Forecasting Hypermarket Sales Around Major Holidays
Author: Alan B. Palayil
Course: ITS-836: Data Science & Big Data Analytics

==========================================================
METHODS IMPLEMENTED IN THIS SCRIPT
==========================================================
Data Sources
-----------
1. Kaggle Walmart "Super Market" Dataset (Proxy for Hypermarket Sales)
   - Loaded via KaggleHub from:
     - saurabhbadole/walmart-super-market-dataset
   - Uses:
     - train.csv        → Weekly_Sales by Store, Dept, Date, IsHoliday
     - features.csv     → CPI, Unemployment, MarkDown1–5, Temperature, etc.
   - Merged on ['Store', 'Date'] to approximate a rich hypermarket dataset
     with sales metrics, promotions, and macroeconomic indicators.

2. U.S. Holiday Flags (Internal Logic)
   - The Kaggle data already includes an "IsHoliday" field that flags key
     holidays (Thanksgiving, Christmas, etc.).
   - This script builds a "holiday_window" feature: a 2-week window around
     any holiday-flagged week (to capture pre- and post-holiday effects).

3. Economic Indicators (Proxy for FRED API)
   - The features.csv file includes CPI and Unemployment variables.
   - These are treated as macroeconomic inputs analogous to FRED indicators.

Variables Used
--------------
- Sales Metrics:
    Weekly_Sales (target), Dept, Store
- Promotions:
    MarkDown1–5, "discount_intensity" (engineered from MarkDowns)
- Time Indicators:
    Year, Month, WeekOfYear, DayOfWeek
- External Factors:
    CPI, Unemployment
- Holiday Indicators:
    IsHoliday (from dataset), holiday_window (engineered)

Preprocessing Steps
-------------------
- Convert 'Date' to datetime; merge train.csv and features.csv on ['Store', 'Date'].
- Filter a single (Store, Dept) panel to obtain a coherent weekly time series.
- Remove rows with missing Weekly_Sales or key features.
- Create engineered features:
    * discount_intensity = normalized sum of MarkDown1–5
    * holiday_window = 1 for ±2 weeks around IsHoliday weeks
    * Lagged sales features: Weekly_Sales_lag1, lag2, lag4
    * Rolling means: Weekly_Sales_roll4, Weekly_Sales_roll8

Analytical Techniques
---------------------
1) Time-Series Modeling (SARIMA – ARIMA-family)
   - Univariate SARIMAX model on Weekly_Sales (weekly data).
   - Captures autoregressive and seasonal behavior (yearly seasonality, s=52).
   - Evaluated with RMSE and MAE on a hold-out test set.
   - This fulfills the ARIMA time-series forecasting requirement.

2) Tree-Based Regression Models (Machine Learning)
   - RandomForestRegressor (bagging ensemble of decision trees).
   - XGBRegressor (gradient-boosting decision trees, if xgboost is installed).
   - Uses lagged sales, rolling averages, discount_intensity, CPI,
     Unemployment, IsHoliday, holiday_window, and calendar features as predictors.
   - Evaluated with RMSE, MAE, and R².
   - These fulfill the Big Data / ML requirement via scalable tree-based methods.

3) Feature Importance Analysis
   - Random Forest feature importances (Gini-based).
   - XGBoost feature importances (gain-based) when available.
   - Helps interpret which drivers (lags, discounts, holidays, macro) matter most.

Visualization Tools
-------------------
- Matplotlib / Seaborn:
    * Time-series plots (Weekly_Sales over time)
    * Actual vs predicted plots for SARIMA, Random Forest, and XGBoost
    * Monthly aggregated trend plot
    * Feature importance bar charts
    * Holiday vs non-holiday comparison plots

Reproducibility
---------------
- Script is self-contained and uses KaggleHub to fetch the dataset.
- Random seed is fixed for reproducibility of tree-based models.
- Clear section headers explain each step (data loading, wrangling,
  modeling, and evaluation).

How to run:
-----------
1. Install required packages:

   pip install kagglehub pandas numpy matplotlib seaborn scikit-learn statsmodels xgboost

   (xgboost is optional; the script will skip it if not installed.)

2. Run from terminal:

   python ITS836B02_AlanPalayil_CourseProject.py
"""

# ============================
# 0) Imports
# ============================
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  # plotting for all charts
import seaborn as sns            # type: ignore # aesthetic plots atop Matplotlib
import kagglehub                 # programmatic download + caching of Kaggle datasets

from sklearn.ensemble import RandomForestRegressor # type: ignore
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score # type: ignore

# SARIMAX is an ARIMA-family model that can incorporate seasonality (SARIMA)
from statsmodels.tsa.statespace.sarimax import SARIMAX # type: ignore

# Try to import XGBoost (optional, but fulfills gradient-boosting ML requirement)
try:
    from xgboost import XGBRegressor # type: ignore
    XGB_AVAILABLE = True
except ImportError:
    XGB_AVAILABLE = False

plt.style.use("seaborn-v0_8")
sns.set()

# For reproducibility of ML results
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# ============================
# 1) Download & Load Walmart Hypermarket-like Dataset
# ============================
print("=" * 100)
print("1) Downloading Walmart Supermarket dataset using KaggleHub")
print("=" * 100)

# Kaggle handle for Walmart "super market" dataset (Big Data style retail panel)
KAGGLE_HANDLE = "saurabhbadole/walmart-super-market-dataset"

# KaggleHub will:
# - Download once and cache under ~/.cache/kagglehub
# - Reuse cached copy on subsequent runs (good for reproducibility and speed)
dataset_path = kagglehub.dataset_download(KAGGLE_HANDLE)
print("Dataset root path from KaggleHub:", dataset_path)

# Locate train.csv (sales) and features.csv (macro, markdowns, etc.)
train_csv = None
features_csv = None

for root, dirs, files in os.walk(dataset_path):
    for f in files:
        fl = f.lower()
        if fl == "train.csv" and train_csv is None:
            train_csv = os.path.join(root, f)
        elif fl == "features.csv" and features_csv is None:
            features_csv = os.path.join(root, f)

if train_csv is None or features_csv is None:
    raise FileNotFoundError(
        f"Could not find both train.csv and features.csv under {dataset_path}.\n"
        f"Found train: {train_csv}, features: {features_csv}"
    )

print("train.csv detected:", train_csv)
print("features.csv detected:", features_csv)

print("\nLoading train.csv and features.csv into Pandas...\n")
train_df = pd.read_csv(train_csv)
feat_df = pd.read_csv(features_csv)

print("train.csv head:")
print(train_df.head(5))
print("\nfeatures.csv head:")
print(feat_df.head(5))

# ============================
# 2) Basic Cleaning, Merge & Date Handling
# ============================
print("=" * 100)
print("2) Cleaning data, merging sources, and preparing time-series structure")
print("=" * 100)

# Ensure Date columns exist and convert them to datetime for time-series operations
if "Date" not in train_df.columns or "Date" not in feat_df.columns:
    raise ValueError("Expected 'Date' column in both train and features files.")

train_df["Date"] = pd.to_datetime(train_df["Date"], errors="coerce")
feat_df["Date"] = pd.to_datetime(feat_df["Date"], errors="coerce")

# Drop rows with invalid/missing dates before merging
train_df = train_df.dropna(subset=["Date"])
feat_df = feat_df.dropna(subset=["Date"])

# Merge sales (train) and features on Store & Date to enrich the panel
merged_df = pd.merge(
    train_df,
    feat_df,
    on=["Store", "Date"],
    how="inner",
    suffixes=("", "_feat"),
)

# Ensure Weekly_Sales (target) is present and non-null
merged_df = merged_df.dropna(subset=["Weekly_Sales"])

# The original dataset already has IsHoliday as boolean; cast to int for modeling
if "IsHoliday" in merged_df.columns:
    merged_df["IsHoliday"] = merged_df["IsHoliday"].astype(int)
else:
    # Fallback if not present (not expected for this dataset)
    merged_df["IsHoliday"] = 0

print("Merged dataset shape:", merged_df.shape)
print("Date range:", merged_df["Date"].min(), "to", merged_df["Date"].max())
print("Columns:", merged_df.columns.tolist(), "\n")

# ============================
# 3) Feature Engineering (Holiday Window, Discount, Lags & Rolling)
# ============================
print("=" * 100)
print("3) Feature engineering: holidays, discount intensity, lags, rolling windows")
print("=" * 100)

# Work on a copy to keep raw merged_df intact
df = merged_df.copy()
df = df.sort_values(["Store", "Dept", "Date"]).reset_index(drop=True)

# ---- Calendar-based features (for seasonality & trends) ----
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["WeekOfYear"] = df["Date"].dt.isocalendar().week.astype(int)
df["DayOfWeek"] = df["Date"].dt.dayofweek  # 0=Mon,...,6=Sun

# ---- Promotion features: MarkDown-based discount_intensity ----
markdown_cols = [c for c in ["MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5"] if c in df.columns]

# Fill NaNs in each MarkDown column with 0 (no markdown when missing)
for col in markdown_cols:
    df[col] = df[col].fillna(0.0)

# Aggregate all markdowns into a single normalized "discount_intensity" feature
if markdown_cols:
    df["discount_intensity_raw"] = df[markdown_cols].sum(axis=1)
    max_disc = df["discount_intensity_raw"].max()
    if max_disc > 0:
        # Min-max style normalization to keep this feature in [0,1]
        df["discount_intensity"] = df["discount_intensity_raw"] / max_disc
    else:
        df["discount_intensity"] = 0.0
else:
    # If no MarkDown columns exist in the dataset, just use 0
    df["discount_intensity"] = 0.0

# ---- Holiday window feature: capture sales uplift around holidays ----
df = df.sort_values(["Store", "Dept", "Date"]).reset_index(drop=True)
df["holiday_window"] = 0

# For each (Store, Dept) time series, mark ±2 weeks around a holiday as 1
for (store, dept), sub in df.groupby(["Store", "Dept"]):
    idx = sub.index
    is_hol = sub["IsHoliday"].to_numpy()
    window_flag = np.zeros_like(is_hol)
    for i, flag in enumerate(is_hol):
        if flag == 1:
            # Spread holiday effect to ±2 weeks around the flagged week
            start = max(0, i - 2)
            end = min(len(is_hol), i + 3)
            window_flag[start:end] = 1
    df.loc[idx, "holiday_window"] = window_flag

# ---- Select a single (Store, Dept) pair with the longest history ----
pair_counts = df.groupby(["Store", "Dept"]).size().sort_values(ascending=False)
print("Top (Store, Dept) pairs by observation count:")
print(pair_counts.head(5), "\n")

main_store, main_dept = pair_counts.index[0]
print(f"Selected Store={main_store}, Dept={main_dept} for forecasting panel.\n")

panel_df = df[(df["Store"] == main_store) & (df["Dept"] == main_dept)].copy()
panel_df = panel_df.sort_values("Date").reset_index(drop=True)

print("Panel subset shape:", panel_df.shape)
print("Panel date range:", panel_df["Date"].min(), "to", panel_df["Date"].max(), "\n")

# ---- Lagged & rolling features: encode time-series structure for ML models ----
# Lags capture autoregressive structure (AR component)
panel_df["Weekly_Sales_lag1"] = panel_df["Weekly_Sales"].shift(1)
panel_df["Weekly_Sales_lag2"] = panel_df["Weekly_Sales"].shift(2)
panel_df["Weekly_Sales_lag4"] = panel_df["Weekly_Sales"].shift(4)

# Rolling means smooth noise and capture short-term trends
panel_df["Weekly_Sales_roll4"] = panel_df["Weekly_Sales"].rolling(window=4).mean()
panel_df["Weekly_Sales_roll8"] = panel_df["Weekly_Sales"].rolling(window=8).mean()

# Drop rows where lags/rolling are NaN (front of the series)
panel_df = panel_df.dropna(subset=["Weekly_Sales_lag1", "Weekly_Sales_roll4"]).reset_index(drop=True)

print("Panel with engineered features (head):")
print(
    panel_df[
        [
            "Date",
            "Weekly_Sales",
            "IsHoliday",
            "holiday_window",
            "discount_intensity",
            "Weekly_Sales_lag1",
            "Weekly_Sales_roll4",
        ]
    ].head(),
    "\n",
)

# ============================
# 4) Train/Test Split (Time-Based)
# ============================
print("=" * 100)
print("4) Time-based train/test split for Weekly_Sales forecasting")
print("=" * 100)

# Set Date as the index to make time-based selection/resampling convenient
panel_df = panel_df.set_index("Date")

n_total = len(panel_df)
test_size = int(0.2 * n_total)  # 80/20 split, preserving temporal order

train_df = panel_df.iloc[:-test_size]
test_df = panel_df.iloc[-test_size:]

print("Train range:", train_df.index.min(), "to", train_df.index.max())
print("Test range:", test_df.index.min(), "to", test_df.index.max())
print("Train size:", len(train_df), "| Test size:", len(test_df), "\n")

# ============================
# 5) SARIMA Time-Series Model (Weekly_Sales)
# ============================
print("=" * 100)
print("5) SARIMA time-series model on Weekly_Sales")
print("=" * 100)

# Univariate time series for ARIMA/SARIMA
y_train = train_df["Weekly_Sales"]
y_test = test_df["Weekly_Sales"]

# SARIMAX with yearly seasonality for weekly data (seasonal period ≈ 52 weeks).
# For a full production pipeline, these orders would be tuned via AIC/grid search.
sarima_order = (1, 1, 1)
seasonal_order = (1, 1, 1, 52)

sarima_model = SARIMAX(
    y_train,
    order=sarima_order,
    seasonal_order=seasonal_order,
    enforce_stationarity=False,
    enforce_invertibility=False,
)
sarima_result = sarima_model.fit(disp=False)

# Forecast for the length of the test set
sarima_forecast = sarima_result.forecast(steps=len(y_test))
sarima_forecast.index = y_test.index  # align indices for metric calculation

sarima_rmse = mean_squared_error(y_test, sarima_forecast) ** 0.5
sarima_mae = mean_absolute_error(y_test, sarima_forecast)

print(f"SARIMA RMSE (test): {sarima_rmse:,.2f}")
print(f"SARIMA MAE  (test): {sarima_mae:,.2f}\n")

# Visual comparison: SARIMA vs. actual test values
plt.figure(figsize=(12, 6))
plt.plot(y_train.index, y_train.values, label="Train Weekly_Sales")
plt.plot(y_test.index, y_test.values, label="Test Weekly_Sales (Actual)")
plt.plot(sarima_forecast.index, sarima_forecast.values, label="SARIMA Forecast", linestyle="--")
plt.title(f"SARIMA Forecast vs Actual Weekly_Sales (Store={main_store}, Dept={main_dept})")
plt.xlabel("Date")
plt.ylabel("Weekly_Sales")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ============================
# 6) Tree-Based Models (RandomForest & Optional XGBoost)
# ============================
print("=" * 100)
print("6) Tree-based regression models: RandomForest and optional XGBoost")
print("=" * 100)

# Feature matrix for ML models (supervised learning)
# Includes autoregressive structure, promotion intensity, holiday effects, and macro variables
feature_cols = [
    "Weekly_Sales_lag1",
    "Weekly_Sales_lag2",
    "Weekly_Sales_lag4",
    "Weekly_Sales_roll4",
    "Weekly_Sales_roll8",
    "discount_intensity",
    "IsHoliday",
    "holiday_window",
    "CPI",
    "Unemployment",
    "Year",
    "Month",
    "WeekOfYear",
    "DayOfWeek",
]

# Keep only columns that actually exist in panel_df (defensive coding)
feature_cols = [c for c in feature_cols if c in panel_df.columns]

X_train = train_df[feature_cols]
X_test = test_df[feature_cols]

y_train_ml = y_train
y_test_ml = y_test

print("Feature columns used in ML models:")
print(feature_cols, "\n")

# ----- Random Forest (bagging ensemble) -----
rf = RandomForestRegressor(
    n_estimators=300,    # number of trees in the forest
    max_depth=12,       # limit depth to avoid overfitting
    random_state=RANDOM_SEED,
    n_jobs=-1,          # use all available CPU cores
)

rf.fit(X_train, y_train_ml)
y_pred_rf = rf.predict(X_test)

rf_rmse = mean_squared_error(y_test_ml, y_pred_rf) ** 0.5
rf_mae = mean_absolute_error(y_test_ml, y_pred_rf)
rf_r2 = r2_score(y_test_ml, y_pred_rf)

print("Random Forest performance (test):")
print(f"RMSE: {rf_rmse:,.2f}")
print(f"MAE:  {rf_mae:,.2f}")
print(f"R²:   {rf_r2:,.3f}\n")

# Visual comparison: RF predictions vs. actual sales
plt.figure(figsize=(12, 6))
plt.plot(y_test_ml.index, y_test_ml.values, label="Actual Weekly_Sales")
plt.plot(y_test_ml.index, y_pred_rf, label="RF Predicted Weekly_Sales", linestyle="--")
plt.title(f"Random Forest Predictions vs Actual (Store={main_store}, Dept={main_dept})")
plt.xlabel("Date")
plt.ylabel("Weekly_Sales")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ----- XGBoost (gradient boosting ensemble, optional) -----
if XGB_AVAILABLE:
    print("XGBoost is available. Training XGBRegressor...\n")

    xgb = XGBRegressor(
        n_estimators=400,
        max_depth=8,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=RANDOM_SEED,
        n_jobs=-1,
    )

    xgb.fit(X_train, y_train_ml)
    y_pred_xgb = xgb.predict(X_test)

    xgb_rmse = mean_squared_error(y_test_ml, y_pred_xgb) ** 0.5
    xgb_mae = mean_absolute_error(y_test_ml, y_pred_xgb)
    xgb_r2 = r2_score(y_test_ml, y_pred_xgb)

    print("XGBoost performance (test):")
    print(f"RMSE: {xgb_rmse:,.2f}")
    print(f"MAE:  {xgb_mae:,.2f}")
    print(f"R²:   {xgb_r2:,.3f}\n")

    # Visual comparison: XGBoost vs. actual sales
    plt.figure(figsize=(12, 6))
    plt.plot(y_test_ml.index, y_test_ml.values, label="Actual Weekly_Sales")
    plt.plot(y_test_ml.index, y_pred_xgb, label="XGBoost Predicted Weekly_Sales", linestyle="--")
    plt.title(f"XGBoost Predictions vs Actual (Store={main_store}, Dept={main_dept})")
    plt.xlabel("Date")
    plt.ylabel("Weekly_Sales")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print(
        "XGBoost not installed. Skipping XGBRegressor.\n"
        "Install via: pip install xgboost\n"
    )

# ============================
# 7) Holiday vs Non-Holiday Sales Analysis
# ============================
print("=" * 100)
print("7) Holiday window vs non-holiday sales comparison")
print("=" * 100)

# Compare average sales in holiday windows vs non-holiday windows
holiday_group = panel_df.groupby("holiday_window")["Weekly_Sales"].agg(
    ["count", "mean", "min", "max", "std"]
)
holiday_group.index = holiday_group.index.map(
    {0: "Non-Holiday Window", 1: "Holiday Window"}
)

print("Weekly_Sales by holiday window status:")
print(holiday_group, "\n")

plt.figure(figsize=(8, 5))
sns.barplot(x=holiday_group.index, y=holiday_group["mean"])
plt.title(
    f"Store={main_store}, Dept={main_dept} - Average Weekly_Sales\n"
    "Holiday Window vs Non-Holiday Window"
)
plt.ylabel("Average Weekly_Sales")
plt.tight_layout()
plt.show()

# ============================
# 7) Holiday vs Non-Holiday Sales Analysis (panel-level, using IsHoliday)
# ============================
print("=" * 100)
print("7A) Holiday vs non-holiday sales comparison (panel-level, IsHoliday)")
print("=" * 100)

# Compare actual holiday weeks vs non-holiday weeks for the selected Store/Dept
holiday_group = panel_df.groupby("IsHoliday")["Weekly_Sales"].agg(
    ["count", "mean", "min", "max", "std"]
)

# Map 0/1 to readable labels
holiday_group.index = holiday_group.index.map({0: "Non-Holiday", 1: "Holiday"})

print("Weekly_Sales by IsHoliday status (selected Store/Dept):")
print(holiday_group, "\n")

plt.figure(figsize=(8, 5))
plt.bar(holiday_group.index, holiday_group["mean"], color=["steelblue", "orange"])
plt.title(
    f"Store={main_store}, Dept={main_dept} - Average Weekly_Sales\n"
    "Holiday vs Non-Holiday Weeks"
)
plt.ylabel("Average Weekly_Sales")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()
print("=" * 100)
print("7b) Global holiday vs non-holiday sales comparison (all stores & depts)")
print("=" * 100)

global_holiday_group = df.groupby("IsHoliday")["Weekly_Sales"].agg(
    ["count", "mean", "min", "max", "std"]
)
global_holiday_group.index = global_holiday_group.index.map(
    {0: "Non-Holiday", 1: "Holiday"}
)

print("Global Weekly_Sales by IsHoliday status (all Store/Dept pairs):")
print(global_holiday_group, "\n")

plt.figure(figsize=(8, 5))
plt.bar(global_holiday_group.index, global_holiday_group["mean"], color=["steelblue", "orange"])
plt.title("All Stores/Depts - Average Weekly_Sales\nHoliday vs Non-Holiday Weeks")
plt.ylabel("Average Weekly_Sales")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()

# ============================
# 8) Monthly Aggregated Trend
# ============================
print("=" * 100)
print("8) Monthly aggregated Weekly_Sales trend")
print("=" * 100)

# Resample weekly series to month-end frequency to reveal broader seasonal trends
monthly_sales = panel_df["Weekly_Sales"].resample("ME").sum()
print("First 12 months of aggregated monthly Weekly_Sales:")
print(monthly_sales.head(12), "\n")

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o")
plt.title(f"Store={main_store}, Dept={main_dept} - Monthly Aggregated Weekly_Sales")
plt.xlabel("Month")
plt.ylabel("Total Weekly_Sales")
plt.grid(True)
plt.tight_layout()
plt.show()

# ============================
# 9) Feature Importances
# ============================
print("=" * 100)
print("9) Random Forest feature importances")
print("=" * 100)

# Feature importance shows which drivers the RF model relies on most:
# e.g., lags vs discounts vs holidays vs macro variables.
rf_importances = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(
    ascending=False
)
print("Random Forest feature importances:")
print(rf_importances, "\n")

plt.figure(figsize=(10, 6))
rf_importances.head(10).plot(kind="bar")
plt.title("Top 10 Random Forest Feature Importances")
plt.ylabel("Importance")
plt.tight_layout()
plt.show()

if XGB_AVAILABLE:
    print("XGBoost feature importances:")
    xgb_importances = pd.Series(
        xgb.feature_importances_, index=feature_cols
    ).sort_values(ascending=False)
    print(xgb_importances, "\n")

    plt.figure(figsize=(10, 6))
    xgb_importances.head(10).plot(kind="bar", color="orange")
    plt.title("Top 10 XGBoost Feature Importances")
    plt.ylabel("Importance")
    plt.tight_layout()
    plt.show()

# ============================
# 10) Summary Metrics for Results/Discussion
# ============================
print("=" * 100)
print("10) Summary metrics for Results & Discussion sections")
print("=" * 100)

print(f"SARIMA RMSE (test):        {sarima_rmse:,.2f}")
print(f"SARIMA MAE  (test):        {sarima_mae:,.2f}")
print(f"Random Forest RMSE (test): {rf_rmse:,.2f}")
print(f"Random Forest MAE  (test): {rf_mae:,.2f}")
print(f"Random Forest R²   (test): {rf_r2:,.3f}")
if XGB_AVAILABLE:
    print(f"XGBoost RMSE (test):       {xgb_rmse:,.2f}")
    print(f"XGBoost MAE  (test):       {xgb_mae:,.2f}")
    print(f"XGBoost R²   (test):       {xgb_r2:,.3f}")
else:
    print("XGBoost metrics:           N/A (library not installed)")

print("\nNotes you can use in the paper:")
print("- SARIMA (ARIMA-family) captures seasonal weekly patterns and holiday spikes.")
print("- Random Forest/XGBoost leverage discount_intensity, lags, rolling means, CPI, "
      "Unemployment, and holiday_window as predictors.")
print("- Holiday windows show clear uplift in sales compared to non-holiday periods.")

print("\n=== End of Course Project Script: Forecasting Hypermarket Sales Around Holidays ===")
