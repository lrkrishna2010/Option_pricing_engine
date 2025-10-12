# save_data.py

from src.data_loader import get_price_data

tickers = ["AAPL", "MSFT", "GOOG", "AMZN"]
data = get_price_data(tickers, start="2022-01-01")

# Save to CSV
data.to_csv("data/sample_data.csv")
print("Saved sample_data.csv")
