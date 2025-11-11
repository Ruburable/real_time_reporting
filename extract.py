import os
import time
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import requests

# Load API keys
load_dotenv()
AV_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
FMP_API_KEY = os.getenv("FMP_API_KEY")

# Portfolio
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
output_file = "portfolio_quotes.csv"

# Clear previous data
if os.path.exists(output_file):
    os.remove(output_file)
    print(f"Previous output file '{output_file}' removed. Starting fresh session.")
else:
    print("No existing data found. Starting new session.")

# Alpha Vantage fetcher
def fetch_av_quote(symbol: str):
    url = (
        f"https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE&symbol={symbol}&apikey={AV_API_KEY}"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json().get("Global Quote", {})
    if not data or "05. price" not in data:
        raise ValueError("Invalid or empty response from Alpha Vantage")
    return float(data["05. price"])

# Financial Modeling Prep (stable endpoint)
def fetch_fmp_quotes(symbols):
    prices = {}
    for symbol in symbols:
        url = (
            f"https://financialmodelingprep.com/stable/quote-short"
            f"?symbol={symbol}&apikey={FMP_API_KEY}"
        )
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            print(f"No data returned for {symbol} from FMP.")
            continue
        prices[symbol] = float(data[0]["price"])
        time.sleep(0.3)
    return prices

# Save records
def append_to_csv(records):
    if not records:
        return
    df = pd.DataFrame(records)
    df.to_csv(output_file, mode="a", header=not os.path.exists(output_file), index=False)

# Main alternating loop
print(f"Starting alternating data collection for {tickers}")
use_av = True  # Start with Alpha Vantage

try:
    while True:
        ts_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        source = "Alpha Vantage" if use_av else "FMP"
        print(f"\n[{ts_str}] Fetching data from {source}...")

        records = []

        if use_av:
            for symbol in tickers:
                try:
                    price = fetch_av_quote(symbol)
                    print(f"{symbol} (AV) = ${price:.2f}")
                    records.append({
                        "timestamp": ts_str,
                        "symbol": symbol,
                        "price": price,
                        "source": "AV"
                    })
                except Exception as e:
                    print(f"Error fetching {symbol} from AV: {e}")
                time.sleep(1.2)  # short delay between Alpha Vantage requests
        else:
            try:
                prices = fetch_fmp_quotes(tickers)
                for symbol, price in prices.items():
                    print(f"{symbol} (FMP) = ${price:.2f}")
                    records.append({
                        "timestamp": ts_str,
                        "symbol": symbol,
                        "price": price,
                        "source": "FMP"
                    })
            except Exception as e:
                print(f"Error fetching from FMP: {e}")

        append_to_csv(records)
        print(f"[{datetime.utcnow().strftime('%H:%M:%S')}] Cycle complete. Switching source in 30s...\n")

        use_av = not use_av
        time.sleep(30)

except KeyboardInterrupt:
    print("Stopped by user.")
