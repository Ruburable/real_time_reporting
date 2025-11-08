import os
import time
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries

# Load API  key
load_dotenv()
api_key = os.getenv("ALPHAVANTAGE_API_KEY")
ts = TimeSeries(key=api_key, output_format='pandas')

# Load portfolio
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
output_file = "portfolio_quotes.csv"

# Define helpers
def fetch_quote(symbol: str):
    try:
        data, _ = ts.get_quote_endpoint(symbol)
        price = float(data["05. price"].iloc[0])
        ts_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{ts_str}] {symbol} = ${price:.2f}")
        return {"timestamp": ts_str, "symbol": symbol, "price": price}
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return None

def append_to_csv(records):
    if not records:
        return
    df = pd.DataFrame(records)
    df.to_csv(output_file, mode='a', header=not os.path.exists(output_file), index=False)

# Run data collection loop
print(f"Starting Alpha Vantage portfolio tracker for {tickers}")

try:
    while True:
        records = []
        for symbol in tickers:
            rec = fetch_quote(symbol)
            if rec:
                records.append(rec)
            time.sleep(1.2)
        append_to_csv(records)
        print(f"Cycle complete at {datetime.utcnow().strftime('%H:%M:%S')} — waiting 60s...\n")
        time.sleep(60)
except KeyboardInterrupt:
    print("Stopped by user.")
