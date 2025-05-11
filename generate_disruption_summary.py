import os
import json
from datetime import datetime

# 最新の disruption_*.json を取得
files = [f for f in os.listdir("disruptions") if f.endswith(".json")]
files.sort(reverse=True)
latest_path = os.path.join("disruptions", files[0])

# 読み込み
with open(latest_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Top 3 の抽出
top3 = sorted(data, key=lambda x: x["score"], reverse=True)[:3]

# README 更新対象ブロック作成
readme_block = "## 🌌 Latest Top 3 Disruptions\n\n"
for entry in top3:
    readme_block += (
        f"- **{entry['id']}** | Score: {entry['score']}  \n"
        f"  “{entry['fragment']}”  \n"
        f"  *Ref:* {entry['meta']['fake_ref']}\n\n"
    )

# README.md 読み込み・書き換え
readme_path = "README.md"
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
else:
    lines = ["# Cosmic Disruption Index\n\n"]

start = None
for i, line in enumerate(lines):
    if "## 🌌 Latest Top 3 Disruptions" in line:
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

# 日次 summary 保存
date_str = datetime.utcnow().strftime("%Y-%m-%d")
summary_path = os.path.join("summaries", f"disruption_summary_{date_str}.md")
os.makedirs("summaries", exist_ok=True)

with open(summary_path, "w", encoding="utf-8") as f:
    f.write(f"# 🌐 Cosmic Disruption Log | {date_str}\n\n")
    for entry in data:
        f.write(f"## {entry['id']} | Score: {entry['score']}\n")
        f.write(f"**Timestamp**: {entry['timestamp']}\n\n")
        f.write(f"**Fragment**: _{entry['fragment']}_\n\n")
        f.write(f"**Fake Reference**: {entry['meta']['fake_ref']}\n\n")
        f.write("---\n\n")
