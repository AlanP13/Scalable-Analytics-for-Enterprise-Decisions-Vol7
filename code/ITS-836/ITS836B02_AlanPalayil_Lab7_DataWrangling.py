# Lab 7: Data Wrangling with Pandas - Cancer Dataset

import pandas as pd

# ============================================================
"""
1. Data Exploration
   1) Load the cancer dataset from Excel/CSV.
   2) Display column data types.
   3) Show summary statistics with describe().
   4) Group the data by 'class' and 'doctor_name'.
"""
print("="*100)
print("Part 1: Data Exploration")
print("="*100)

# 1) Read in the dataset Cancer.csv (starting from Lab 7 - Cancer.xls).

# Define the full file paths to the Excel and CSV versions.
# - excel_path: original Excel file provided for the lab
# - csv_path: CSV file we will create and reuse for future runs
excel_path = r'C:\Users\alanp\Downloads\Lab 7 - Cancer.xls'  # Excel file provided with the lab
csv_path = r'C:\Users\alanp\Downloads\Lab 7 - Cancer.csv'    # CSV version for analysis & submission

try:
    # Try loading the CSV if it already exists.
    # This makes subsequent runs faster since CSV loads a bit quicker than Excel.
    df = pd.read_csv(csv_path)
    print(f"Loaded dataset from existing CSV file: {csv_path}")
except FileNotFoundError:
    # If CSV doesn't exist, we fall back to loading from the Excel file.
    print(f"{csv_path} not found. Loading from Excel file: {excel_path}")
    df = pd.read_excel(excel_path)

    # IMPORTANT: Convert blank strings ("") to proper missing values (NaN / pd.NA)
    # Empty cells in Excel can show up as empty strings when read into pandas.
    # We want them treated as missing so that dropna() and isna() work correctly.
    df = df.replace("", pd.NA)

    # Save a clean CSV version for future runs and for submission as required by the lab.
    df.to_csv(csv_path, index=False)
    print(f"Excel file loaded, blanks converted to NaN, and saved as {csv_path}")

# Show the first few rows and the overall shape of the dataset as a quick sanity check.
print("\n1) First 5 rows of the dataset:")
print(df.head())
print("\nDataFrame shape (rows, columns):", df.shape, "\n")

# 2) Display the data types of each column.
print("2) Data types of each column:")
# dtypes shows whether columns are int, float, object (string), etc.
print(df.dtypes)
print("\n")

# 3) Use describe() to generate summary statistics.
print("3) Summary statistics using describe():")
# include='all' will try to provide statistics for both numeric and non-numeric columns.
print(df.describe(include="all"))
print("\n")

# 4) Group the dataset by 'class' and 'doctor_name'.
print("4) Group by 'class' and 'doctor_name' (showing count of rows per group):")

# groupby() allows us to group rows by combinations of 'class' and 'doctor_name'.
# .size() counts how many rows are in each group.
# reset_index(name="count") converts the groupby result back into a DataFrame with a 'count' column.
grouped = df.groupby(["class", "doctor_name"]).size().reset_index(name="count")
print(grouped.head(20))  # Show the first 20 grouped results
print("\n")

# ============================================================
"""
2. Handling Missing Values
   5) Summarize missing values.
   6) Drop all rows that contain any missing data.
   7) Show the number of unique values per column.
   8) Find duplicate 'patient_id' values and show which appears most often.
"""
print("="*100)
print("Part 2: Handling Missing Values")
print("="*100)

# 5) Provide a summary of missing values within the dataset.
print("5) Number of missing values per column:")

# isna().sum() on each column gives the count of missing values (NaN/pd.NA) per column.
missing_per_column = df.isna().sum()
# Summing again gives total missing values across the entire DataFrame.
total_missing = missing_per_column.sum()

print(missing_per_column)
print(f"\nTotal missing values in entire DataFrame: {total_missing}\n")

# 6) Drop all rows that contain missing data.
print("6) Dropping all rows that contain ANY missing values:")

# dropna() removes any row that has at least one missing value in any column.
# We store the result in df_clean and continue the rest of the analysis on this cleaned dataset.
df_clean = df.dropna()

print("Original shape:", df.shape)
print("Shape after dropna (df_clean):", df_clean.shape)
print("\n")

# 7) Summarize the number of unique values in each column.
print("7) Number of unique values in each column (in df_clean):")

# nunique() returns how many distinct values appear in each column.
# This is helpful to identify categorical columns or IDs with repeated entries.
unique_counts = df_clean.nunique()
print(unique_counts)
print("\n# Interesting note: columns with very few unique values may be categorical (e.g., 'class').\n")

# 8) Find duplicate values in 'patient_id'. Which patient_id appears most frequently?
print("8) Duplicate 'patient_id' analysis (in df_clean):")

# value_counts() returns a Series where the index is patient_id and the values are their frequencies.
patient_counts = df_clean["patient_id"].value_counts()

print("Top 10 most frequent patient_id values:")
print(patient_counts.head(10))

# idxmax() returns the index (patient_id) with the maximum count (most frequent).
most_frequent_patient_id = patient_counts.idxmax()
# max() returns the maximum frequency value.
max_frequency = patient_counts.max()

print(f"\nMost frequent patient_id: {most_frequent_patient_id} (appears {max_frequency} times)\n")

# ============================================================
"""
3. Filtering Data
   9) Remove patients (rows) where 'patient_id' appears more than two times.
"""
print("="*100)
print("Part 3: Filtering Data")
print("="*100)

# 9) Remove patients (rows) where 'patient_id' appears more than two times.
print("9) Removing rows where patient_id appears more than two times:")

# First, compute how often each patient_id appears in df_clean using value_counts().
patient_freq = df_clean["patient_id"].value_counts()

# Then filter df_clean:
# - df_clean["patient_id"].map(patient_freq) looks up the frequency of each patient_id.
# - We keep only rows where frequency <= 2.
df_filtered = df_clean[df_clean["patient_id"].map(patient_freq) <= 2]

print("Shape before filtering:", df_clean.shape)
print("Shape after filtering (df_filtered):", df_filtered.shape)
print("\n")

# ============================================================
"""
4. Reshaping Data
   10) Create a 'categorical_df' with 'patient_id', 'doctor_name', and 'doctor_count'.
   11) Pivot so each doctor becomes a column indicating visits.
   12) Drop any multi-index levels from the columns.
   13) Display the one-hot encoded DataFrame.
   14) Merge this one-hot DataFrame back into the filtered dataset.
   15) Display the final combined DataFrame.
   16) Drop the original 'doctor_name' column.
"""
print("="*100)
print("Part 4: Reshaping Data")
print("="*100)

# 10) Create 'categorical_df' containing 'patient_id', 'doctor_name', and 'doctor_count' = 1.
print("10) Creating 'categorical_df' with patient_id, doctor_name, and doctor_count=1")

# We select only the columns we need: patient_id and doctor_name.
categorical_df = df_filtered[["patient_id", "doctor_name"]].copy()

# doctor_count is a new column where each row represents 1 visit to that doctor.
categorical_df["doctor_count"] = 1  # Each row indicates one visit to that doctor

print("First 10 rows of categorical_df:")
print(categorical_df.head(10))
print("\n")

# 11) Pivot so each doctor's name becomes a column; cells indicate visits; fill NaNs with 0.
print("11) Pivoting so each doctor_name becomes a column (one-hot style):")

# We use pivot_table to reshape the data:
# - index: patient_id (rows)
# - columns: doctor_name (new columns)
# - values: doctor_count (number of visits)
# - aggfunc='sum': if the same patient sees the same doctor multiple times, we sum them.
# - fill_value=0: if a patient never saw a particular doctor, that cell becomes 0.
doctor_pivot = categorical_df.pivot_table(
    index="patient_id",
    columns="doctor_name",
    values="doctor_count",
    aggfunc="sum",
    fill_value=0
)

print("Pivot table (first 10 rows):")
print(doctor_pivot.head(10))
print("\n")

# 12) Drop the multi-index from columns using droplevel() (if needed).
print("12) Dropping multi-level column index (if present):")

# Sometimes pivot_table can create a MultiIndex on columns.
# We check if doctor_pivot.columns is a MultiIndex and, if so, drop the top level.
if isinstance(doctor_pivot.columns, pd.MultiIndex):
    doctor_pivot.columns = doctor_pivot.columns.droplevel(0)

print("Columns after potential droplevel:")
print(doctor_pivot.columns)
print("\n")

# 13) Display the one-hot encoded DataFrame.
print("13) One-hot encoded doctor visit DataFrame (first 10 rows):")
print(doctor_pivot.head(10))
print("\n")

# 14) Join this one-hot encoded DataFrame back to the original dataset using merge().
print("14) Merging one-hot encoded doctor visits back into df_filtered:")

# We merge df_filtered (row-level cancer data) with doctor_pivot (doctor visit one-hot matrix) on patient_id.
# how='left' ensures all rows from df_filtered are preserved.
df_combined = df_filtered.merge(
    doctor_pivot,
    on="patient_id",
    how="left"
)

print("Combined DataFrame (first 10 rows):")
print(df_combined.head(10))
print("\n")

# 15) Display the final combined DataFrame.
print("15) Final combined DataFrame shape & sample:")
print("Shape:", df_combined.shape)
print(df_combined.head(10))
print("\n")

# 16) Drop the 'doctor_name' column from the combined DataFrame.
print("16) Dropping 'doctor_name' column from df_combined:")

# Since we now have one-hot columns for each doctor, the original doctor_name column
# (which stores only one doctor per row) is no longer needed.
if "doctor_name" in df_combined.columns:
    df_combined = df_combined.drop(columns=["doctor_name"])

print("Columns after dropping 'doctor_name':")
print(df_combined.columns)
print("\n")

# ============================================================
"""
5. Row-wise Operations
   17) Define a function celltypelabel(x) to label cells as 'normal' or 'abnormal'.
   18) Use apply() to create 'cell_type_label' and display the updated DataFrame.
"""
print("="*100)
print("Part 5: Row-wise Operations")
print("="*100)

# 17) Define celltypelabel(x) to classify rows as 'normal' or 'abnormal'.
print("17) Defining function 'celltypelabel'...")

def celltypelabel(x):
    """
    Classify a patient's cell as 'normal' or 'abnormal'.

    Rule:
      - If both cell_size_uniformity > 5 AND cell_shape_uniformity > 5,
        label as 'normal'.
      - Otherwise, label as 'abnormal'.

    The input 'x' is a single row (Series) when used with DataFrame.apply(axis=1).
    """
    if ((x["cell_size_uniformity"] > 5) &
        (x["cell_shape_uniformity"] > 5)):
        return "normal"
    else:
        return "abnormal"

print("Function 'celltypelabel' defined.\n")

# 18) Use apply() to create a new column 'cell_type_label'.
print("18) Creating 'cell_type_label' using apply(celltypelabel):")

# apply(celltypelabel, axis=1) applies the function row-by-row.
# Each row gets labeled as "normal" or "abnormal" based on the rule defined above.
df_combined["cell_type_label"] = df_combined.apply(celltypelabel, axis=1)

print("Updated DataFrame with 'cell_type_label' (first 10 rows):")
print(df_combined.head(10))
print("\n")

print("=== End of Lab 7 Cancer Script ===")
