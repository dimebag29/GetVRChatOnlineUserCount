import time
import traceback
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

URL = "https://api.vrchat.cloud/api/1/visits"
SUMMARY_FILE = Path("summary.txt")

try:
    req = Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0 (GitHub Actions)"
        },
    )

    try:
        with urlopen(req, timeout=10) as response:
            text = response.read().decode("utf-8").strip()
    except HTTPError as e:
        raise RuntimeError(f"HTTP Error {e.code}") from e
    except URLError as e:
        raise RuntimeError(f"URL Error: {e.reason}") from e

    try:
        visits = int(text)
    except ValueError:
        raise RuntimeError(f"Response is not an integer: {text!r}")

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

except Exception:
    traceback.print_exc()
    raise
