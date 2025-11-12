import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os
from datetime import datetime
import subprocess

sns.set_theme(style="darkgrid")
plt.style.use("dark_background")

data_file = "portfolio_quotes.csv"
refresh_interval = 10
window_size = 100
out_dir = "out"

def plot_live():
    if not os.path.exists(data_file):
        print(f"Waiting for {data_file} to be created by extract.py ...")
        while not os.path.exists(data_file):
            time.sleep(5)

    os.makedirs(out_dir, exist_ok=True)
    print(f"Starting live visualization...\nSaving plots to: {out_dir}/")

    while True:
        try:
            df = pd.read_csv(data_file)
            if df.empty:
                print("No data yet — waiting...")
                time.sleep(refresh_interval)
                continue

            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values(['symbol', 'timestamp'])
            symbols = df['symbol'].unique()

            normalized_list = []
            for sym in symbols:
                sub = df[df['symbol'] == sym].copy()
                sub['normalized_price'] = sub['price'] / sub['price'].iloc[0]
                normalized_list.append(sub)
            normalized = pd.concat(normalized_list)

            unique_times = df['timestamp'].drop_duplicates().sort_values()
            if len(unique_times) > window_size:
                recent_times = unique_times.iloc[-window_size:]
                df = df[df['timestamp'].isin(recent_times)]
                normalized = normalized[normalized['timestamp'].isin(recent_times)]

            fig, axes = plt.subplots(len(symbols) + 1, 1,
                                     figsize=(10, 3.5 * (len(symbols) + 1)),
                                     sharex=True)
            if len(symbols) == 1:
                axes = [axes]

            for i, sym in enumerate(symbols):
                sub = df[df['symbol'] == sym].reset_index(drop=True)
                axes[i].set_title(f"{sym} Price", fontsize=12, color='white')
                axes[i].set_ylabel("Price ($)", color='white')
                axes[i].tick_params(axis='x', colors='white')
                axes[i].tick_params(axis='y', colors='white')

                for j in range(1, len(sub)):
                    prev_price = sub.loc[j - 1, 'price']
                    curr_price = sub.loc[j, 'price']
                    color = 'green' if curr_price > prev_price else 'red' if curr_price < prev_price else 'gray'
                    axes[i].plot(sub.loc[j - 1:j, 'timestamp'], sub.loc[j - 1:j, 'price'], color=color, linewidth=1.8)

                if not sub.empty:
                    last = sub.iloc[-1]
                    axes[i].scatter(last['timestamp'], last['price'], color='white', s=30, edgecolor='black', zorder=5)
                    axes[i].text(last['timestamp'], last['price'], f" {last['source']}", color='white', fontsize=8, va='center')

            portfolio = normalized.groupby('timestamp')['normalized_price'].mean().reset_index()
            sns.lineplot(ax=axes[-1], data=portfolio, x='timestamp', y='normalized_price', color='lime')
            axes[-1].set_title("Portfolio Performance (Normalized)", fontsize=12, color='white')
            axes[-1].set_ylabel("Relative Value", color='white')
            axes[-1].tick_params(axis='x', colors='white')
            axes[-1].tick_params(axis='y', colors='white')

            fig.suptitle(f"Live Portfolio Tracker — {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
                         fontsize=14, color='white')
            plt.tight_layout(rect=[0, 0, 1, 0.97])

            out_path = os.path.join(out_dir, "portfolio_live.png")
            fig.savefig(out_path, dpi=150, bbox_inches="tight")
            plt.close(fig)

            subprocess.run(["python", "output.py"], check=False)
            print(f"Plot and dashboard updated: {out_path}")

            time.sleep(refresh_interval)

        except KeyboardInterrupt:
            print("Visualization stopped by user.")
            break
        except Exception as e:
            print("Error during update:", e)
            time.sleep(refresh_interval)

if __name__ == "__main__":
    plot_live()
