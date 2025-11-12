import os
import time
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import requests
import yfinance as yf

load_dotenv()
AV_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
FMP_API_KEY = os.getenv("FMP_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
TWELVE_API_KEY = os.getenv("TWELVE_API_KEY")

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
output_file = "portfolio_quotes.csv"

if os.path.exists(output_file):
    os.remove(output_file)
    print(f"Previous output file '{output_file}' removed.")
else:
    print("No existing data found. Starting new session.")

def fetch_av(symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={AV_API_KEY}"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    data = r.json().get("Global Quote", {})
    if not data or "05. price" not in data:
        raise ValueError("Empty AV response")
    return float(data["05. price"])

def fetch_fmp(symbols):
    prices = {}
    for s in symbols:
        url = f"https://financialmodelingprep.com/stable/quote-short?symbol={s}&apikey={FMP_API_KEY}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        if data:
            prices[s] = float(data[0]["price"])
        time.sleep(0.15)
    return prices

def fetch_finnhub(symbols):
    prices = {}
    for s in symbols:
        url = f"https://finnhub.io/api/v1/quote?symbol={s}&token={FINNHUB_API_KEY}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        if "c" in data and data["c"] != 0:
            prices[s] = float(data["c"])
        time.sleep(0.15)
    return prices

def fetch_twelvedata(symbols):
    prices = {}
    for s in symbols:
        url = f"https://api.twelvedata.com/price?symbol={s}&apikey={TWELVE_API_KEY}"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        if "price" in data:
            prices[s] = float(data["price"])
        time.sleep(0.15)
    return prices

def fetch_yfinance(symbols):
    prices = {}
    for s in symbols:
        try:
            ticker = yf.Ticker(s)
            p = ticker.fast_info.get("last_price")
            if p:
                prices[s] = float(p)
        except Exception:
            continue
    return prices

def append_to_csv(records):
    if not records:
        return
    df = pd.DataFrame(records)
    df.to_csv(output_file, mode="a", header=not os.path.exists(output_file), index=False)

providers = [
    ("AV", fetch_av),
    ("FMP", fetch_fmp),
    ("FINNHUB", fetch_finnhub),
    ("TWELVE", fetch_twelvedata),
    ("YF", fetch_yfinance),
]

active_providers = []
for name, func in providers:
    if name in ("YF",) or os.getenv(f"{name}_API_KEY"):
        active_providers.append((name, func))

if not active_providers:
    raise RuntimeError("No valid API keys found!")

print(f"Active data sources: {[p[0] for p in active_providers]}")
print("Starting rotation...\n")

provider_index = 0
INTERVAL_BETWEEN_PROVIDERS = 6
SLEEP_PER_STOCK_AV = 0.8

try:
    while True:
        ts_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        name, fetcher = active_providers[provider_index]
        print(f"[{ts_str}] {name}")

        records = []
        try:
            if name == "AV":
                for s in tickers:
                    try:
                        price = fetcher(s)
                        print(f"{s} ({name}) = ${price:.2f}")
                        records.append({
                            "timestamp": ts_str,
                            "symbol": s,
                            "price": price,
                            "source": name
                        })
                    except Exception as e:
                        print(f"Error {s} {name}: {e}")
                    time.sleep(SLEEP_PER_STOCK_AV)
            else:
                prices = fetcher(tickers)
                for s, price in prices.items():
                    print(f"{s} ({name}) = ${price:.2f}")
                    records.append({
                        "timestamp": ts_str,
                        "symbol": s,
                        "price": price,
                        "source": name
                    })
        except Exception as e:
            print(f"Provider {name} failed: {e}")

        append_to_csv(records)
        provider_index = (provider_index + 1) % len(active_providers)
        time.sleep(INTERVAL_BETWEEN_PROVIDERS)

except KeyboardInterrupt:
    print("Stopped by user.")
