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


---

### **2️⃣ visualise.py — Live Visualization**
- Monitors the CSV produced by `extract.py` and updates visualizations automatically.  
- Generates **live-updating line charts** for each stock and an aggregated portfolio view.  
- Can save the latest plots (e.g., in `images/`) for reporting or dashboard integration.

**Example visuals:**
- Real-time line charts per ticker  
- Combined portfolio trend (normalized performance)  
- Optional alert markers for large price changes  

---

### **3️⃣ output.py — Automated Summary Deck**
- Consolidates visuals and summary statistics into an **auto-updating presentation deck**.  
- Imports charts from `visualise.py` and compiles them into a `.pptx` or `.pdf` report.  
- Refreshes automatically whenever new data or visuals are available.  

**Includes key metrics:**
- Latest prices per ticker  
- Daily percentage changes  
- Portfolio summary statistics  

---

## ⚙️ Notes
- The project uses the **Alpha Vantage API** for live financial data.  
- Users must have an **API key stored securely in a `.env` file**:
