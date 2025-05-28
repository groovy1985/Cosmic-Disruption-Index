import os
import json
from datetime import datetime

# === 最新の JSON ファイルを取得 ===
files = [f for f in os.listdir("disruptions") if f.startswith("cdi_kz_") and f.endswith(".json")]
files.sort(reverse=True)

if not files:
    raise FileNotFoundError("No CDI-KZ disruption logs found in 'disruptions/'")

latest_path = os.path.join("disruptions", files[0])

with open(latest_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# === KZ-HX スコアで Top3 抽出 ===
def hx_score(entry):
    try:
        sig = entry["meta"].get("hx_signature", 0)
        return float(sig)
    except:
        return 0

top3 = sorted(data, key=hx_score, reverse=True)[:3]

# === README 書き換え用ブロック作成 ===
readme_block = "## 🌀 Top 3 Disruptive Fragments (KZ-HX Mode)\n\n"
for entry in top3:
    frag = entry["fragment"]
    hx = entry["meta"].get("hx_signature", "?")
    ref = entry["meta"].get("fake_ref", "Unknown Reference")
    readme_block += (
        f"- **{entry['id']}** | HX: {hx}  \n"
        f"  “{frag}”  \n"
        f"  *Ref:* {ref}\n\n"
    )

# === README.md の更新 ===
readme_path = "README.md"
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
else:
    lines = ["# Cosmic Disruption Index\n\n"]

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
    new_lines = lines + ["\n"] + [readme_block]

with open(readme_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

# === 日次 summary を .md として保存 ===
date_str = datetime.utcnow().strftime("%Y-%m-%d")
summary_path = os.path.join("summaries", f"cdi_summary_{date_str}.md")
os.makedirs("summaries", exist_ok=True)

with open(summary_path, "w", encoding="utf-8") as f:
    f.write(f"# 🌐 Cosmic Disruption Log | {date_str}\n\n")
    for entry in data:
        frag = entry["fragment"]
        hx = entry["meta"].get("hx_signature", "?")
        ref = entry["meta"].get("fake_ref", "Unknown Reference")
        f.write(f"## {entry['id']} | HX: {hx}\n")
        f.write(f"**Timestamp**: {entry['timestamp']}\n\n")
        f.write(f"**Fragment**: _{frag}_\n\n")
        f.write(f"**Fake Reference**: {ref}\n\n")
        f.write("---\n\n")

