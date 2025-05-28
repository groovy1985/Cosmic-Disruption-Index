# generate_weekly_note_cdi.py

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
        f.write("# Weekly Disruption Digest (KZ+HX Edition)\n\n---\n\n")
        for entry in logs:
            meta = entry.get("meta", {})
            hx = meta.get("hx_signature", {})
            f.write(f"## {entry['id']}\n")
            f.write(f"“{entry['fragment']}”\n\n")
            f.write(f"- 🕯 嘘: {meta.get('false_element', 'N/A')}｜真: {meta.get('true_element', 'N/A')}\n")
            f.write(
                f"- HX: DIS={hx.get('DIS', '?')}, MIR={hx.get('MIR', '?')}, "
                f"EMO={hx.get('EMO', '?')}, ETH={hx.get('ETH', '?')}, WET={hx.get('WET', '?')}\n\n"
            )
            f.write("---\n\n")
    print(f"[+] Weekly note saved to: {path}")

if __name__ == "__main__":
    logs = collect_week_logs()
    if logs:
        save_note_summary(logs)
    else:
        print("[!] No recent disruption logs found.")
