import os
import json
from datetime import datetime

LOG_DIR = "logs"  # ← ここを変更
OUTPUT_DIR = "zine_monthly"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def collect_month_logs():
    now = datetime.utcnow()
    month_prefix = now.strftime("cdi_kz_%Y-%m")
    logs = []

    for fname in sorted(os.listdir(LOG_DIR)):
        if fname.startswith(month_prefix) and fname.endswith(".json"):
            fpath = os.path.join(LOG_DIR, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                logs.extend(json.load(f))
    return logs

def save_zine_summary(logs):
    date_str = datetime.utcnow().strftime("%Y-%m")
    path = os.path.join(OUTPUT_DIR, f"zine-cdi-{date_str}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("# 📚 Monthly Disruption ZINE (KZ+HX Edition)\n\n---\n\n")
        for entry in logs:
            f.write(f"## {entry['id']}\n")
            f.write(f"“{entry['fragment']}”\n\n")
            f.write(f"- 🕯 嘘: {entry['meta']['false_element']}｜真: {entry['meta']['true_element']}\n")
            hx = entry['meta']['hx_signature']
            f.write(f"- HX: DIS={hx['DIS']}, MIR={hx['MIR']}, EMO={hx['EMO']}, ETH={hx['ETH']}, WET={hx['WET']}\n\n")
            f.write("---\n\n")
    print(f"[+] Monthly ZINE saved to: {path}")

if __name__ == "__main__":
    logs = collect_month_logs()
    if logs:
        save_zine_summary(logs)
    else:
        print("[!] No logs found for this month.")
