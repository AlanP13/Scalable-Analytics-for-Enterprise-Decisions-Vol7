# Lab 8 - Treatment Data Analysis Script
import pandas as pd

# =====================================================================
print("="*100)
print("1) Loading Treatment Excel File and Converting to CSV")
print("="*100)

# Paths to the Excel and CSV files
xls_path = r"C:\Users\alanp\Downloads\Lab 8 - Treatment.xls"
csv_path = r"C:\Users\alanp\Downloads\Lab 8 - Treatment.csv"

# Load CSV if exists, otherwise load Excel and convert
try:
    df = pd.read_csv(csv_path)
    print(f"Loaded dataset from existing CSV file: {csv_path}")
except FileNotFoundError:
    print(f"CSV not found. Loading Excel file instead: {xls_path}")
    df = pd.read_excel(xls_path)
    df = df.replace("", pd.NA)       # Convert empty strings to NaN
    df.to_csv(csv_path, index=False)
    print(f"Converted Excel to CSV and saved as: {csv_path}")
# Preview dataset
print("DataFrame shape:", df.shape)
print("First 5 rows:")
print(df.head())
print("\n")
print("Column names:")
print(df.columns.tolist())
print("\n")

# =====================================================================
print("="*100)
print("2) Grouping dataset by 'Treatment'")
print("="*100)
treatment_group = df.groupby("Treatment")
print("Number of rows per Treatment:")
print(treatment_group.size())
print("\n")

# =====================================================================
print("="*100)
print("3) Distribution of 'RelativeFitness' per Treatment using describe()")
print("="*100)
treatment_relfit_desc = treatment_group["RelativeFitness"].describe()
print(treatment_relfit_desc)
print("\n")

# =====================================================================
print("="*100)
print("4) Grouping by both 'Treatment' and 'Group' and describing 'RelativeFitness'")
print("="*100)
treat_group_combo = df.groupby(["Treatment", "Group"])
treat_group_relfit_desc = treat_group_combo["RelativeFitness"].describe()
print(treat_group_relfit_desc)
print("\n")

# =====================================================================
print("="*100)
print("5) Aggregations of 'RelativeFitness' per Treatment")
print("="*100)
treatment_agg = treatment_group["RelativeFitness"].agg(
    ["mean", "max", "median", "sum", "std"]
)
print(treatment_agg)
print("\n")

# =====================================================================
print("="*100)
print("6) Additional Observations & Quick Checks")
print("="*100)
print("Number of unique values in each column:")
print(df.nunique())
print("\n")
print("Overall summary of 'RelativeFitness':")
print(df["RelativeFitness"].describe())
print("\n")

print("=== End of Lab 8 Treatment Script ===")