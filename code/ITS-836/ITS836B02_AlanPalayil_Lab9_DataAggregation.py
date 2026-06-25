# Lab 9 - Data Aggregation with Kaggle Medicinal Plants Dataset (Selected via ChatGPT)
import kagglehub # type: ignore
import pandas as pd
import os

# =====================================================================
print("=" * 100)
print("2) Locate a dataset using AI + Load into Pandas + Show first 10 rows")
print("=" * 100)

# Kaggle dataset handle
KAGGLE_HANDLE = "edwardgaibor/pfaf-medical-plants-use-dataset"
# KaggleHub will download once, then reuse the cached copy on future runs
dataset_path = kagglehub.dataset_download(KAGGLE_HANDLE)
print("Dataset root path from KaggleHub:", dataset_path)
# Recursively search for the first CSV file under dataset_path
csv_path = None
for root, dirs, files in os.walk(dataset_path):
    for f in files:
        if f.lower().endswith(".csv"):
            csv_path = os.path.join(root, f)
            break
    if csv_path is not None:
        break
if csv_path is None:
    raise FileNotFoundError("No CSV files found anywhere under the dataset folder.")
print("CSV file detected:", csv_path)
# Load CSV into Pandas
print("\nLoading dataset into Pandas...\n")
df = pd.read_csv(csv_path)
print("First 10 rows:")
print(df.head(10))
print("\nDataFrame shape:", df.shape)
print("\nColumns:", df.columns.tolist())
# Detect numeric columns
numeric_cols = df.select_dtypes(include="number").columns.tolist()
print("\nNumeric columns detected:", numeric_cols)

# =====================================================================
print("=" * 100)
print("3) Applying Pandas aggregation functions to numeric columns")
print("=" * 100)

# If there are no numeric columns, print message and skip
if not numeric_cols:
    print("No numeric columns found.\n")

else:
    """
    Apply multiple aggregation functions to each numeric column.
    We build a dictionary where:
    - Key = column name
    - Value = list of functions to apply to that column
    Note:
    - lambda s: s.iloc[0] → gives the first value (equivalent to first())
    - lambda s: s.iloc[-1] → gives the last value (equivalent to last())
    - Other functions (mean, std, var, etc.) are built-in Pandas aggregations.
    """
    agg_result = df[numeric_cols].agg(
        {
            col: [
                "count",                  # number of non-null values
                (lambda s: s.iloc[0]),    # first value in the column
                (lambda s: s.iloc[-1]),   # last value in the column
                "mean",                   # average value
                "median",                 # middle value
                "min",                    # minimum
                "max",                    # maximum
                "std",                    # standard deviation
                "var",                    # variance
                "sum",                    # total sum
            ]
            for col in numeric_cols
        }
    ).T  # Transpose for readability (columns become rows)

    # Display final aggregated table
    print("Aggregation results:")
    print(agg_result)
    print("\n")

# =====================================================================
print("=" * 100)
print("4) Perform groupby() using a meaningful categorical column")
print("=" * 100)

# Identify all categorical columns (object dtype typically represents text categories)
cat_cols = df.select_dtypes(include="object").columns.tolist()
# Initialize variable to store our selected grouping column
group_col = None
"""
Choose a "reasonable" categorical column:
- Must have at least 2 unique categories (otherwise pointless)
- Should not exceed ~20 categories (too many groups becomes noisy)    
"""
for col in cat_cols:
    if 2 <= df[col].nunique() <= 20:
         # first matching column is selected
        group_col = col   
        # stop searching once a suitable column is found  
        break                 
# If no valid categorical column exists, print message
if group_col is None:
    print("No suitable categorical column found for groupby().")
else:
    # Inform the user which column we'll use for grouping
    print(f"Using '{group_col}' for groupby analysis.\n")
    # Ensure there is at least one numeric column available to aggregate
    if numeric_cols:
        # Choose the first numeric column for demonstration
        target_num_col = numeric_cols[0]
        print(f"Grouping by '{group_col}' using numeric column '{target_num_col}':\n")
        """
        Perform groupby:
        - Group by the selected categorical column
        - Aggregate the numeric column with useful statistical metrics
        - Sort by mean in descending order for easier interpretation
        """
        grouped_stats = (
            df.groupby(group_col)[target_num_col]
              .agg(["count", "mean", "min", "max", "std"])
              .sort_values("mean", ascending=False)
        )
        # Display results
        print("Groupby results (sorted by mean):")
        print(grouped_stats)
        print()
    else:
        # If no numeric columns exist, we cannot compute group statistics
        print("No numeric columns available for groupby.\n")

# =====================================================================
print("=" * 100)
print("5) Reflection Summary Instructions")
print("=" * 100)

print("In this lab, I used ChatGPT assistance to locate, load, and analyze a publicly available medicinal plants dataset from Kaggle. The dataset contained 17,950 records and 27 columns related to plant characteristics, edibility ratings, medicinal ratings, and botanical information. Using ChatGPT to guide dataset selection and clarify each step made the overall workflow faster and more intuitive.")

print("=== End of Lab 9 Data Aggregation ===")
