import os
import json
from datetime import datetime, timedelta

LOG_DIR = "logs"
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
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # 単一エントリ形式に対応
                if isinstance(data, dict) and "disrupted_text" in data:
                    logs.append({
                        "id": fname.replace(".json", ""),
                        "timestamp": ftime.isoformat(),
                        "fragment": data["disrupted_text"],
                        "meta": {
                            "false_element": "(unspecified)",
                            "true_element": "(unspecified)",
                            "hx_signature": {
                                "DIS": 18,
                                "MIR": 17,
                                "EMO": 19,
                                "ETH": 16,
                                "WET": 18
                            }
                        }
                    })
            except Exception as e:
                print(f"[!] Skipped {fname}: {e}")
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
