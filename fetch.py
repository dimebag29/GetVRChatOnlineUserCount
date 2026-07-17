import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

URL = "https://api.vrchat.cloud/api/1/visits"
SUMMARY_FILE = Path("summary.txt")

req = Request(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0 (GitHub Actions)"
    },
)

try:
    with urlopen(req, timeout=10) as response:
        text = response.read().decode("utf-8").strip()
except (HTTPError, URLError):
    text = "0"

try:
    visits = int(text)
except ValueError:
    visits = 0

line = f"{int(time.time())}_{visits}"

lines = []

if SUMMARY_FILE.exists():
    lines = [
        l.rstrip("\n")
        for l in SUMMARY_FILE.read_text(encoding="utf-8").splitlines()
        if l.strip()
    ]

lines.append(line)

# 最新105120行だけ残す
lines = lines[-105120:]

SUMMARY_FILE.write_text(
    "\n".join(lines) + "\n",
    encoding="utf-8"
)
