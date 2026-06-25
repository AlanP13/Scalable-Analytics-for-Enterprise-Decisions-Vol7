# Lab 10 - Time Series Analysis (Apple Stock Prices)
import yfinance as yf # type: ignore
import pandas as pd
import matplotlib.pyplot as plt # type: ignore

# =====================================================================
print("="*100)
print("1) Downloading AAPL stock price time-series data")
print("="*100)

# Ensure plots render nicely
plt.style.use("seaborn-v0_8")
# Download 5 years of Apple stock data
df = yf.download("AAPL", period="5y")

# =====================================================================
print("="*100)
print("2) Displaying first 10 rows and DataFrame info")
print("="*100)

print("\nFirst 10 rows of dataset:")
print(df.head(10))
print("\nDataFrame Info:")
print(df.info())

# =====================================================================
print("="*100)
print("3) Convert index to datetime")
print("="*100)

print("\nAlready in datetime format but included for instruction")

# =====================================================================
print("="*100)
print("4) Set the datetime column as the index of your DataFrame.")
print("="*100)

df.index = pd.to_datetime(df.index)
print("\nDatetime index set successfully. Index type:", type(df.index))

# =====================================================================
print("="*100)
print("5) Generate and plot a time series line graph using matplotlib seaborn plotstyle.")
print("="*100)

plt.figure(figsize=(12,6))
plt.plot(df["Close"], label="AAPL Close Price")
plt.title("AAPL Closing Price Over Time")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.show()

# =====================================================================
print("="*100)
print("6) Use rolling averages (30-day windows) to smooth the data")
print("="*100)

df["30day_MA"] = df["Close"].rolling(window=30).mean()
plt.figure(figsize=(12,6))
plt.plot(df["Close"], label="Close Price", alpha=0.5)
plt.plot(df["30day_MA"], label="30-Day Moving Average", linewidth=2)
plt.title("AAPL Price with 30-Day Moving Average")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.show()

# =====================================================================
print("="*100)
print("7) Resample the data (by month) and visualize changes in trends.")
print("="*100)

monthly = df["Close"].resample("M").mean()
plt.figure(figsize=(12,6))
plt.plot(monthly, label="Monthly Average Close Price", color="purple")
plt.title("AAPL Monthly Trend")
plt.xlabel("Month")
plt.ylabel("Avg Closing Price")
plt.legend()
plt.grid(True)
plt.show()

# =====================================================================
print("="*100)
print("8) Check for any seasonal patterns, outliers, or anomalies using visual inspection and AI insights")
print("="*100)

plt.figure(figsize=(12,6))
plt.plot(df["Close"], label="Close Price", alpha=0.6)
plt.scatter(df["Close"].idxmax(), df["Close"].max(), color="red", label="Peak", s=80)
plt.scatter(df["Close"].idxmin(), df["Close"].min(), color="blue", label="Low", s=80)
plt.title("AAPL Price – Highlighting Peaks & Lows")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.grid(True)
plt.show()

print("="*100)
print("9) Suggested Forecasting Models (from AI Guidance)")
print("="*100)

print("""
ChatGPT suggested the following forecasting models for financial time-series:
- ARIMA / SARIMA (short-term, autoregressive behavior)
- Prophet (handles seasonality + daily/weekly/yearly structure)
- LSTM Neural Networks (deep learning for sequential data)
- Holt-Winters Triple Exponential Smoothing (trend+seasonality)
""")
