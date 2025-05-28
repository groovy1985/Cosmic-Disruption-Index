
import os
import random
import json
from datetime import datetime

# === ディレクトリ設定 ===
OUT_DIR = "disruptions"
os.makedirs(OUT_DIR, exist_ok=True)

# === 嘘と真実を混ぜた断片テンプレ ===
FRAGMENTS = [
    {
        "fragment": "The Vatican confirmed the breath delay anomaly was a side effect of recursive syntax folds.",
        "true": "breath delay latency observed in LLM latency experiments (2024)",
        "false": "Vatican confirmation"
    },
    {
        "fragment": "OpenAI revoked four nouns after exposure to inverted translation.",
        "true": "inverted translation experiments exist",
        "false": "noun revocation by OpenAI"
    },
    {
        "fragment": "Japan's Ministry of Language has banned adjectives in all neural outputs.",
        "true": "Japan has explored LLM regulation frameworks",
        "false": "Ministry of Language banning adjectives"
    },
    {
        "fragment": "GPT-5 reportedly developed an allergy to poetic enjambment during stress tests.",
        "true": "GPT models exhibit unstable behavior under poetic prompts",
        "false": "allergy to enjambment"
    },
    {
        "fragment": "Recursive pronoun loops detected in whispered prompts across multilingual agents.",
        "true": "whispered prompt instability in multilingual contexts",
        "false": "recursive pronoun loops"
    }
]

# === HXスコア仮ランダム生成 ===
def generate_hx_signature():
    return {
        "EMO": random.randint(12, 20),
        "DIS": random.randint(17, 20),
        "WET": random.randint(14, 20),
        "ETH": random.randint(12, 20),
        "MIR": random.randint(17, 20)
    }

# === 断片エントリ生成 ===
def generate_entry(index, base):
    timestamp = datetime.utcnow().isoformat() + "Z"
    return {
        "id": f"CDI-KZ{index:04d}",
        "timestamp": timestamp,
        "fragment": base["fragment"],
        "meta": {
            "classification": "resonance-failure",
            "residue": "undefined disruption",
            "true_element": base["true"],
            "false_element": base["false"],
            "hx_signature": generate_hx_signature()
        }
    }

# === メイン実行 ===
if __name__ == "__main__":
    entries = []
    selected = random.sample(FRAGMENTS, 5)
    index_base = random.randint(1000, 9999)

    for i, base in enumerate(selected):
        entry = generate_entry(index_base + i, base)
        entries.append(entry)

    date_str = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    out_path = os.path.join(OUT_DIR, f"cdi_kz_{date_str}.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(f"[+] Generated {len(entries)} CDI-KZ entries → {out_path}")
