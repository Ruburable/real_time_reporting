# 📈 Real-Time US Stock Portfolio Tracker

A lightweight Python project for **tracking, visualizing, and summarizing** live U.S. stock prices using the **Alpha Vantage API**.  
The project consists of three core modules:

---

## 🧩 Project Overview

### **1️⃣ extract.py — Data Extraction**
- Connects to the **Alpha Vantage API** (requires API key in a `.env` file).  
- Fetches the latest prices for up to **5 U.S. stocks** once per minute.  
- Stores results in a continuously growing CSV file (`portfolio_quotes.csv`).  
- Prints real-time updates to the console.

### **2️⃣ visualise.py — Live Visualization**
- Monitors the CSV produced by `extract.py` and updates visualisations automatically.  
- Generates **live-updating line charts** every 5 seconds for each stock and an aggregated portfolio view.

**Available visuals:**
- Real-time line charts per ticker  
- Combined portfolio trend (normalized performance)

---