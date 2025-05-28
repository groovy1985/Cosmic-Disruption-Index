
import os
import json
from datetime import datetime

DISRUPT_DIR = "disruptions"
SUMMARY_DIR = "summaries"
README_PATH = "README.md"

os.makedirs(SUMMARY_DIR, exist_ok=True)

# === 最新のCDIファイル取得 ===
files = [f for f in os.listdir(DISRUPT_DIR) if f.endswith(".json")]
files.sort(reverse=True)
if not files:
    print("[!] No disruption files found.")
    exit(1)

latest_path = os.path.join(DISRUPT_DIR, files[0])
with open(latest_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# === HXスコアでTop3抽出（MIR + DIS優先） ===
def hx_score(entry):
    sig = entry["meta"]["hx_signature"]
    return sig["MIR"] + sig["DIS"]

top3 = sorted(data, key=hx_score, reverse=True)[:3]

# === README.md 更新ブロック ===
readme_block = "## 🌀 Top 3 Disruptive Fragments (KZ-HX Mode)

"
for entry in top3:
    frag = entry["fragment"]
    hx = entry["meta"]["hx_signature"]
    readme_block += (
        f"- **{entry['id']}**  
"
        f"  “{frag}”  
"
        f"  🔻 HX: DIS={hx['DIS']}｜MIR={hx['MIR']}｜WET={hx['WET']}  
"
        f"  🕯 嘘: {entry['meta']['false_element']}｜真: {entry['meta']['true_element']}

"
    )

# === README.md 書き換え処理 ===
if os.path.exists(README_PATH):
    with open(README_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
else:
    lines = ["# Cosmic Disruption Index

"]

start = None
for i, line in enumerate(lines):
    if "## 🌀 Top 3 Disruptive Fragments" in line:
        start = i
        break

if start is not None:
    end = start + 1
    while end < len(lines) and not lines[end].startswith("## "):
        end += 1
    new_lines = lines[:start] + [readme_block] + lines[end:]
else:
    new_lines = lines + ["
"] + [readme_block]

with open(README_PATH, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("[+] README.md updated.")

# === 日次 summary 出力 ===
date_str = datetime.utcnow().strftime("%Y-%m-%d")
summary_path = os.path.join(SUMMARY_DIR, f"cdi_summary_{date_str}.md")

with open(summary_path, "w", encoding="utf-8") as f:
    f.write(f"# 🌐 Cosmic Disruption Log | {date_str}

")
    for entry in data:
        hx = entry["meta"]["hx_signature"]
        f.write(f"## {entry['id']}
")
        f.write(f"**Fragment**: “{entry['fragment']}”

")
        f.write(f"**True**: {entry['meta']['true_element']}
")
        f.write(f"**False**: {entry['meta']['false_element']}

")
        f.write(f"**HX Signature**: DIS={hx['DIS']}, MIR={hx['MIR']}, WET={hx['WET']}, EMO={hx['EMO']}, ETH={hx['ETH']}

")
        f.write("---

")

print(f"[+] Summary saved to {summary_path}")
