import time
import traceback
from pathlib import Path
from urllib.request import Request, urlopen

URL = "https://api.vrchat.cloud/api/1/visits"
SUMMARY_FILE = Path("summary.txt")

try:
    req = Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/139.0 Safari/537.36",
            "Accept": "*/*",
            "Referer": "https://vrchat.com/"
        }
    )

    with urlopen(req, timeout=10) as response:
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
    lines = lines[-5:]

    SUMMARY_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

except Exception:
    traceback.print_exc()
    raise
