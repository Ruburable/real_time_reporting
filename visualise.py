import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os
from datetime import datetime

# load style
sns.set_theme(style="darkgrid")
plt.style.use("dark_background")

# config
data_file = "portfolio_quotes.csv"
refresh_interval = 15  # seconds between updates
window_size = 100      # number of timestamps to display
out_dir = "out"

def plot_live():
    if not os.path.exists(data_file):
        print(f"Waiting for {data_file} to be created by extract.py ...")
        while not os.path.exists(data_file):
            time.sleep(5)

    os.makedirs(out_dir, exist_ok=True)
    print(f"Starting live visualization... (Ctrl+C to stop)\nSaving plots to: {out_dir}/")

    while True:
        try:
            df = pd.read_csv(data_file)
            if df.empty:
                print("No data yet — waiting...")
                time.sleep(refresh_interval)
                continue

            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values(['symbol', 'timestamp'])

            # normalize prices per stock
            normalized_list = []
            for sym in df['symbol'].unique():
                sub = df[df['symbol'] == sym].copy()
                sub['normalized_price'] = sub['price'] / sub['price'].iloc[0]
                normalized_list.append(sub)
            normalized = pd.concat(normalized_list)

            # keep only recent window
            unique_times = df['timestamp'].drop_duplicates().sort_values()
            if len(unique_times) > window_size:
                recent_times = unique_times.iloc[-window_size:]
                df = df[df['timestamp'].isin(recent_times)]
                normalized = normalized[normalized['timestamp'].isin(recent_times)]

            symbols = df['symbol'].unique()
            fig, axes = plt.subplots(len(symbols) + 1, 1,
                                     figsize=(10, 3.5 * (len(symbols) + 1)),
                                     sharex=True)
            if len(symbols) == 1:
                axes = [axes]

            # plot each stock
            for i, sym in enumerate(symbols):
                sub = df[df['symbol'] == sym]
                sns.lineplot(ax=axes[i], data=sub, x='timestamp', y='price', color='cyan')
                axes[i].set_title(f"{sym} Price", fontsize=12, color='white')
                axes[i].set_ylabel("Price ($)", color='white')
                axes[i].tick_params(axis='x', colors='white')
                axes[i].tick_params(axis='y', colors='white')

            # portfolio performance
            portfolio = (
                normalized.groupby('timestamp')['normalized_price']
                .mean()
                .reset_index()
            )
            sns.lineplot(ax=axes[-1], data=portfolio, x='timestamp', y='normalized_price', color='lime')
            axes[-1].set_title("Portfolio Performance (Normalized)", fontsize=12, color='white')
            axes[-1].set_ylabel("Relative Value", color='white')
            axes[-1].tick_params(axis='x', colors='white')
            axes[-1].tick_params(axis='y', colors='white')

            fig.suptitle(
                f"Live Portfolio Tracker — {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
                fontsize=14, color='white'
            )
            plt.tight_layout(rect=[0, 0, 1, 0.97])

            # save to folder
            out_path = os.path.join(out_dir, "portfolio_live.png")
            fig.savefig(out_path, dpi=150, bbox_inches="tight")
            print(f"Plot updated: {out_path}")

            plt.show(block=False)
            plt.pause(refresh_interval)
            plt.close(fig)

        except KeyboardInterrupt:
            print("Visualization stopped by user.")
            break
        except Exception as e:
            print("Error during update:", e)
            time.sleep(refresh_interval)

if __name__ == "__main__":
    plot_live()