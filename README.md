# 📈 Live Stock Portfolio Tracker

This project continuously extracts live stock price data, visualizes portfolio performance, and presents it in an automatically updating dashboard.

It uses the **[Alpha Vantage API](https://www.alphavantage.co/)** for market data — you’ll need your own API key stored in a local `.env` file.

---

## 🚀 Project Overview

### 1. `extract.py`
- Connects to the Alpha Vantage API using an API key stored in `.env`.
- Downloads stock price data for up to 5 predefined stocks.
- Fetches data every minute, respecting Alpha Vantage’s free-tier rate limits.
- Saves all price data to `portfolio_quotes.csv`.

### 2. `visualise.py`
- Continuously reads `portfolio_quotes.csv` and updates live visualizations.
- Uses a dark Seaborn theme for clarity and readability.
- Produces:
  - Individual stock performance plots.
  - Combined portfolio performance (normalized for comparison).
- Saves each new visualization as `out/portfolio_live.png` — overwriting the previous one for efficiency.

### 3. `output.py`
- Creates an HTML dashboard (`out/dashboard.html`) that displays the most recent plot.
- Automatically refreshes every 15 seconds using a meta refresh tag.
- Provides a dark, minimalistic layout matching the visualization style.
- The HTML can be opened locally in any browser to monitor portfolio performance live.

### 4. `main.py`
- Master controller script.
- Runs all services (`extract.py`, `visualise.py`, and `output.py`) simultaneously.
- Monitors processes and automatically restarts any that crash.
- Allows for safe termination with Ctrl+C.
- Ensures that all outputs are written to the `out/` directory.
