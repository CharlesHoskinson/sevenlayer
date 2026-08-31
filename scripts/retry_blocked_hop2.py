"""Retry hop-2 entries that anti-bot shells blocked, with Scrapling's
StealthyFetcher (Camoufox). Pages that still resist are listed for the
pixelshot fallback tier. Updates manifest statuses in place.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from scrapling.fetchers import StealthyFetcher

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "references" / "manifest.json"
STILL = REPO / "references" / "snowball" / "hop2-still-blocked.json"

SHELLS = ("client challenge", "just a moment", "captcha",
          "enable javascript and cookies", "access denied")


def real_page(html: str) -> bool:
    low = html[:6000].lower()
    if any(s in low for s in SHELLS):
        return False
    words = len(re.sub(r"<[^>]+>", " ", html).split())
    return words >= 150


def main() -> int:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    blocked = [e for e in m if e.get("status") == "blocked"
               and e.get("citation", "").startswith("(hop-2")]
    print(f"retrying {len(blocked)} blocked entries with StealthyFetcher")
    still = []
    fixed = 0
    for i, e in enumerate(blocked):
        url = e["url"]
        try:
            r = StealthyFetcher.fetch(url, headless=True, solve_cloudflare=True,
                                      timeout=90000, network_idle=True)
            html = r.html_content if hasattr(r, "html_content") else ""
            status_code = getattr(r, "status", "?")
        except Exception as exc:
            html, status_code = "", f"EXC {type(exc).__name__}"
        if html and real_page(html):
            dest = REPO / e["file"]
            dest.write_text(html, encoding="utf-8")
            e["status"] = "ok"
            e["note"] = "recovered via StealthyFetcher"
            fixed += 1
            print(f"[{i+1}/{len(blocked)}] RECOVERED {status_code} {url[:70]}")
        else:
            e["note"] = "still blocked after StealthyFetcher; pixelshot tier"
            still.append({"id": e["id"], "url": url, "file": e["file"]})
            print(f"[{i+1}/{len(blocked)}] STILL-BLOCKED {status_code} {url[:70]}")
        time.sleep(2.0)
    MANIFEST.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    STILL.write_text(json.dumps(still, indent=1) + "\n", encoding="utf-8")
    print(f"\n=== stealth retry: {fixed} recovered, {len(still)} for pixelshot ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
