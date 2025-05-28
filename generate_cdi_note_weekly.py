
import os
import json
from datetime import datetime, timedelta

LOG_DIR = "disruptions"
OUTPUT_DIR = "note_weekly"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def collect_week_logs():
    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)
    logs = []

    for fname in sorted(os.listdir(LOG_DIR)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(LOG_DIR, fname)
        ftime = datetime.fromtimestamp(os.path.getmtime(fpath))
        if ftime >= week_ago:
            with open(fpath, "r", encoding="utf-8") as f:
                logs.extend(json.load(f))

    return logs

def save_note_summary(logs):
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    path = os.path.join(OUTPUT_DIR, f"note-cdi-{date_str}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Weekly Disruption Digest (KZ+HX Edition)

---

")
        for entry in logs:
            f.write(f"## {entry['id']}
")
            f.write(f"“{entry['fragment']}”

")
            f.write(f"- 🕯 嘘: {entry['meta']['false_element']}｜真: {entry['meta']['true_element']}
")
            hx = entry['meta']['hx_signature']
            f.write(f"- HX: DIS={hx['DIS']}, MIR={hx['MIR']}, EMO={hx['EMO']}, ETH={hx['ETH']}, WET={hx['WET']}

")
            f.write("---

")
    print(f"[+] Weekly note saved to: {path}")

if __name__ == "__main__":
    logs = collect_week_logs()
    if logs:
        save_note_summary(logs)
    else:
        print("[!] No recent disruption logs found.")
