
import os
import json
from datetime import datetime

LOG_DIR = "disruptions"
OUTPUT_DIR = "zine_monthly"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def collect_month_logs():
    now = datetime.utcnow()
    logs = []

    for fname in sorted(os.listdir(LOG_DIR)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(LOG_DIR, fname)
        ftime = datetime.fromtimestamp(os.path.getmtime(fpath))
        if ftime.strftime("%Y-%m") == now.strftime("%Y-%m"):
            with open(fpath, "r", encoding="utf-8") as f:
                logs.extend(json.load(f))

    return logs

def save_zine(logs):
    date_str = datetime.utcnow().strftime("%Y-%m")
    path = os.path.join(OUTPUT_DIR, f"zine-cdi-{date_str}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Cosmic Disruption ZINE｜{date_str}

")
        f.write("_This ZINE is not for clarity, but for collapse._

---

")
        for entry in logs:
            f.write(f"## {entry['id']}
")
            f.write(f"“{entry['fragment']}”

")
            f.write(f"🕯 嘘: {entry['meta']['false_element']}｜真: {entry['meta']['true_element']}
")
            hx = entry['meta']['hx_signature']
            f.write(f"HX: DIS={hx['DIS']} MIR={hx['MIR']} WET={hx['WET']} EMO={hx['EMO']} ETH={hx['ETH']}

")
            f.write("---

")
    print(f"[+] Monthly ZINE saved to: {path}")

if __name__ == "__main__":
    logs = collect_month_logs()
    if logs:
        save_zine(logs)
    else:
        print("[!] No logs found for this month.")
