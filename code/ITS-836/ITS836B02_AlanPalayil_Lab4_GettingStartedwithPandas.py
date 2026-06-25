import pandas as pd

# Part 1: Working with Series
print("="*100)
print("Part 1: Working with Series")
print("="*100)
# 1. Create and display a one-dimensional array-like object (Series). Using any numerical or string data.
print("1) Creating a simple Series:")
s1 = pd.Series([10, 20, 30, 40, 50], name="ExampleSeries")
print(s1)
# 2. Create two Series and perform arithmetic operations
print("2) Arithmetic with two Series:")
s2 = pd.Series([2, 4, 6, 8, 10], name="s2")
s3 = pd.Series([1, 3, 5, 7, 9], name="s3")
print("Series s2:")
print(s2)
print("\nSeries s3:")
print(s3)
print("\nAddition (s2 + s3):")
print(s2 + s3)
print("\nSubtraction (s2 - s3):")
print(s2 - s3)
print("\nMultiplication (s2 * s3):")
print(s2 * s3)
print("\nDivision (s2 / s3):")
print(s2 / s3)

# Part 2: Working with the Automobile Dataset
print("="*100)
print("Part 2: Working with the Automobile Dataset")
print("="*100)
# 3. Load the dataset 'Lab 4 - Automobile.xls' using Pandas. Make sure the Excel file is in the same folder as this script.
# Ask user for a custom file path (optional)
user_input = input("Enter the full path to 'Lab 4 - Automobile.xls' (or press Enter to use the default path): ").strip()
# Default fallback path
default_path = r"C:\Users\alanp\Downloads\Lab 4 - Automobile.xls"
# Use the user-provided path if not empty; otherwise use default
file_path = user_input if user_input else default_path
print(f"Using file path: {file_path}")
# Load the Excel file
df = pd.read_excel(file_path)
print("3) Loaded Automobile dataset.")
print("Shape of DataFrame:", df.shape)
# 4. Print the first five and last five rows to understand the structure.
print("4) First 5 rows:")
print(df.head())
print("\nLast 5 rows:")
print(df.tail())
# 5. Remove any records containing '?', 'n.a', or NaN values. We first replace '?' and 'n.a' with NaN, then drop rows with NaN.
print("5) Cleaning data: replacing '?', 'n.a' with NaN and dropping rows with any NaN values.")
df_clean = df.replace(['?', 'n.a'], pd.NA)  # Replace string missing indicators with NA
df_clean = df_clean.dropna()                # Drop any row with NA
print("Shape before cleaning:", df.shape)
print("Shape after cleaning:", df_clean.shape)
# Save cleaned DataFrame to a new CSV file
cleaned_file = "Lab4_Automobile_cleaned.csv"
df_clean.to_csv(cleaned_file, index=False)
print(f"Cleaned data saved to: {cleaned_file}")
# 6. Find and print the most expensive car in the dataset. Show both the price and the company name.
print("6) Most expensive car (price + company):")
# Try to identify likely columns for price and company.
# Adjust these names if your file uses different ones. e.g., 'price' and 'make', or 'Price' and 'Company'
# Here we try common variants.
possible_price_cols = ['price', 'Price', 'PRICE']
possible_company_cols = ['company', 'Company', 'make', 'Make', 'MAKE']
price_col = None
company_col = None
for c in df_clean.columns:
    if c in possible_price_cols:
        price_col = c
    if c in possible_company_cols:
        company_col = c
print("Detected price column:", price_col)
print("Detected company column:", company_col)
# Convert price to numeric in case it's stored as string
df_clean[price_col] = pd.to_numeric(df_clean[price_col])
max_price_idx = df_clean[price_col].idxmax()
most_expensive_row = df_clean.loc[max_price_idx]
print("Most expensive car row:")
print(most_expensive_row)
print(f"\nMost expensive car company: {most_expensive_row[company_col]}")
print(f"Most expensive car price: {most_expensive_row[price_col]}")
# 7. Print all the details of cars manufactured by Toyota.
print("7) All cars manufactured by Toyota:")
toyota_cars = df_clean[df_clean[company_col].str.lower() == "toyota"]
print(toyota_cars)
# 8. Count and display the total number of cars per company.
print("8) Total number of cars per company:")
cars_per_company = df_clean[company_col].value_counts()
print(cars_per_company)
# 9. Display the most expensive car from each company.
print("9) Most expensive car from each company:")
# We group by company and get index of max price per group.
idx = df_clean.groupby(company_col)[price_col].idxmax()
most_expensive_per_company = df_clean.loc[idx, [company_col, price_col]]
print(most_expensive_per_company)
# 10. Calculate the average mileage (fuel efficiency) for each car company. Column name for mileage may vary (e.g., 'average-mileage', 'average_mpg', etc.)
print("10) Average mileage for each car company:")
possible_mileage_cols = ['average-mileage', 'average_mileage', 'avg_mileage', 'city-mpg', 'highway-mpg']
mileage_col = None
for c in df_clean.columns:
    if c in possible_mileage_cols:
        mileage_col = c
        break
print("Detected mileage column:", mileage_col)
if mileage_col is not None:
    df_clean[mileage_col] = pd.to_numeric(df_clean[mileage_col])
    avg_mileage = df_clean.groupby(company_col)[mileage_col].mean()
    print(avg_mileage)
else:
    print("Mileage column not found. Please check your dataset column names.")
# 11. Sort all cars in ascending order based on the price column and display the result.
print("11) Cars sorted by price (ascending):")
sorted_by_price = df_clean.sort_values(by=price_col, ascending=True)
print(sorted_by_price[[company_col, price_col]].head(20))  # Show first 20 for brevity

# Part 3: Combining DataFrames
print("="*100)
print("Part 3: Combining DataFrames")
print("="*100)
# 12. Create two DataFrames from dictionaries and concatenate them.
GermanCars = {
    'Company': ['Ford', 'Mercedes', 'BMV', 'Audi'],
    'Price':   [23845, 171995, 135925, 71400]
}
japaneseCars = {
    'Company': ['Toyota', 'Honda', 'Nissan', 'Mitsubishi '],
    'Price':   [29995, 23600, 61500, 58900]
}
print("12) Concatenating German and Japanese car DataFrames:")
df_german = pd.DataFrame(GermanCars)
df_japanese = pd.DataFrame(japaneseCars)
print("German cars:")
print(df_german)
print("\nJapanese cars:")
print(df_japanese)
df_all = pd.concat([df_german, df_japanese], ignore_index=True)
print("\nConcatenated DataFrame (German + Japanese):")
print(df_all)
# 13. Create and merge the Car_Price and Car_Horsepower DataFrames on Company
Car_Price = {
    'Company': ['Toyota', 'Honda', 'BMV', 'Audi'],
    'Price':   [23845, 17995, 135925, 71400]
}
car_Horsepower = {
    'Company':   ['Toyota', 'Honda', 'BMV', 'Audi'],
    'horsepower': [141, 80, 182, 160]
}
print("13) Merging Car_Price and Car_Horsepower on 'Company':")
df_price = pd.DataFrame(Car_Price)
df_hp = pd.DataFrame(car_Horsepower)
print("Car_Price DataFrame:")
print(df_price)
print("\nCar_Horsepower DataFrame:")
print(df_hp)
merged_df = pd.merge(df_price, df_hp, on='Company')
print("\nMerged DataFrame:")
print(merged_df)