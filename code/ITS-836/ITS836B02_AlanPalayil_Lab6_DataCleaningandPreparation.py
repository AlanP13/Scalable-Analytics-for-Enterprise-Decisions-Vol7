import pandas as pd
# Step 1: Load the .xls and convert to .csv for consistency and upload
print("="*100)
print("1) Loading Excel file and converting to CSV")
print("="*100)
xls_path = r'C:\Users\alanp\Downloads\Lab 6 - Chipotle.xls'
csv_path = r'C:\Users\alanp\Downloads\Lab 6 - Chipotle.csv'

# Load Excel using pandas
df = pd.read_excel(xls_path)
print(f"Loaded {xls_path} successfully.")

# Save to CSV
df.to_csv(csv_path, index=False)
print(f"Converted to CSV and saved as {csv_path}.")

# Display first few rows and shape for verification
print("DataFrame shape:", df.shape)
print("First 5 rows:")
print(df.head())
print("\n")

# Step 2: Convert 'item_price' column to numeric type
print("="*100)
print("2) Converting 'item_price' to numeric type")
print("="*100)

# Check original type
print("Original dtype of 'item_price':", df["item_price"].dtype)

# Clean and convert
df["item_price"] = (
    df["item_price"]
    .astype(str)                   # ensure string for replacement
    .str.replace("$", "", regex=False)  # remove dollar
    .str.strip()
    .astype(float)                 # convert to float
)

print("New dtype of 'item_price':", df["item_price"].dtype)
print("First 5 cleaned prices:")
print(df["item_price"].head())
print("\n")

# Step 3 & 4: Average prices for 'chicken' vs 'steak' items
print("="*100)
print("3) Average price for 'chicken' items")
print("="*100)

chicken_avg = df[df["item_name"].str.contains("chicken", case=False, na=False)]["item_price"].mean()
print(f"Average 'chicken' price: ${round(chicken_avg, 2)}\n")

print("="*100)
print("4) Average price for 'steak' items")
print("="*100)
steak_avg = df[df["item_name"].str.contains("steak", case=False, na=False)]["item_price"].mean()
print(f"Average 'steak' price: ${round(steak_avg, 2)}\n")

# Step 5: Compare total revenue from 'chicken' vs 'steak'
print("="*100)
print("5) Total Revenue Comparison")
print("="*100)

chicken_revenue = df[df["item_name"].str.contains("chicken", case=False, na=False)]["item_price"].sum()
steak_revenue = df[df["item_name"].str.contains("steak", case=False, na=False)]["item_price"].sum()

print(f"Total 'chicken' revenue: ${round(chicken_revenue, 2)}")
print(f"Total 'steak' revenue: ${round(steak_revenue, 2)}")

if chicken_revenue > steak_revenue:
    print("Chicken generates more revenue.")
elif steak_revenue > chicken_revenue:
    print("Steak generates more revenue.")
else:
    print("Chicken and steak generate equal revenue.")
print("\n")

# Step 6: Missing value analysis
print("="*100)
print("6) Missing Value Analysis")
print("="*100)

total_missing = df.isna().sum().sum()
missing_per_column = df.isna().sum()

print(f"Total missing values in dataset: {total_missing}\n")
print("Missing values per column:")
print(missing_per_column)