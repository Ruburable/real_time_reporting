import os
from datetime import datetime

OUT_DIR = "out"
PLOT_FILE = "portfolio_live.png"
HTML_FILE = os.path.join(OUT_DIR, "dashboard.html")

def create_dashboard():
    os.makedirs(OUT_DIR, exist_ok=True)
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="15">
    <title>Live Portfolio Dashboard</title>
    <style>
        body {{
            background-color: #0e1117;
            color: #eaeaea;
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 0;
            padding: 2rem;
        }}
        img {{
            width: 90%;
            max-width: 1200px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        }}
        .timestamp {{
            margin-top: 10px;
            font-size: 0.9em;
            color: #888;
        }}
    </style>
</head>
<body>
    <h1>Live Portfolio Dashboard</h1>
    <img src="{PLOT_FILE}?t={datetime.utcnow().timestamp()}" alt="Portfolio Plot">
    <div class="timestamp">Last refreshed: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}</div>
</body>
</html>
"""
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Dashboard generated: {HTML_FILE}")

if __name__ == "__main__":
    create_dashboard()
