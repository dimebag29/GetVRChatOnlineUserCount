import time
from pathlib import Path
from urllib.request import urlopen

URL = "https://api.vrchat.cloud/api/1/visits"

SUMMARY_FILE = Path("summary.txt")

with urlopen(URL, timeout=10) as response:
    text = response.read().decode("utf-8").strip()

line = f"{int(time.time())}_{text}"

lines = []

if SUMMARY_FILE.exists():
    lines = [
        l.rstrip("\n")
        for l in SUMMARY_FILE.read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]

lines.append(line)

# 最新5行だけ残す
lines = lines[-5:]

SUMMARY_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
