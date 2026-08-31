"""Fetch the hop-2 (snowball) reference candidates with Scrapling.

Reads references/snowball/hop2-fetchlist.json, downloads each URL (ePrint and
arXiv entries as PDFs, DOI/web entries as whatever they serve), saves under
references/snowball/hop2/, and appends manifest entries following the repo's
existing snowball convention (snowball_round, discovered_from, status).
Failures are recorded, never silently skipped.
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from scrapling.fetchers import Fetcher

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "references" / "manifest.json"
FETCHLIST = REPO / "references" / "snowball" / "hop2-fetchlist.json"
OUTDIR = REPO / "references" / "snowball" / "hop2"

IMPERSONATE = ("safari", "chrome", "firefox")


def slug_for(url: str) -> str:
    m = re.search(r"eprint\.iacr\.org/(\d{4})/(\d+)", url)
    if m:
        return f"eprint-{m.group(1)}-{m.group(2)}"
    m = re.search(r"arxiv\.org/pdf/(\d{4}\.\d{4,5})", url)
    if m:
        return f"arxiv-{m.group(1).replace('.', '-')}"
    m = re.search(r"doi\.org/(.+)", url)
    if m:
        return "doi-" + re.sub(r"[^a-z0-9]+", "-", m.group(1).lower())[:60].strip("-")
    tail = re.sub(r"[^a-z0-9]+", "-", url.split("//", 1)[-1].lower())[:60]
    return tail.strip("-")


def fetch(url: str):
    last = None
    for imp in IMPERSONATE:
        try:
            r = Fetcher.get(url, timeout=60, impersonate=imp)
        except Exception as exc:  # transport error: one retry with next profile
            last = exc
            time.sleep(1.5)
            continue
        last = r
        if r.status == 200:
            return r
        if r.status != 403:
            return r
        time.sleep(1.5)
    return last


def main() -> int:
    fl = json.loads(FETCHLIST.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    next_id = max(e["id"] for e in manifest) + 1
    OUTDIR.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    for i, cand in enumerate(fl):
        url = cand["url"]
        get_url = url + ".pdf" if re.fullmatch(
            r"https://eprint\.iacr\.org/\d{4}/\d+", url) else url
        slug = slug_for(url)
        r = fetch(get_url)
        status = "failed"
        dest = None
        if hasattr(r, "status") and r.status == 200:
            body = r.body
            if body[:5] == b"%PDF-":
                dest = OUTDIR / f"ref-{next_id:03d}-{slug}.pdf"
                dest.write_bytes(body)
                status = "ok"
            elif body.strip():
                dest = OUTDIR / f"ref-{next_id:03d}-{slug}.html"
                dest.write_bytes(body)
                low = body[:4000].lower()
                status = "ok" if b"just a moment" not in low else "blocked"
        entry = {
            "id": next_id,
            "slug": slug,
            "citation": f"(hop-2 snowball) {url}",
            "chapters": [],
            "type": "paper" if (dest and dest.suffix == ".pdf") else "web",
            "url": url,
            "file": str(dest.relative_to(REPO)) if dest else None,
            "status": status,
            "discovered_from": cand["cited_by"][0],
            "cited_by_count": cand["n_docs"],
            "snowball_round": 0,
            "fetched": "2026-08-30",
        }
        manifest.append(entry)
        if status == "ok":
            ok += 1
        else:
            fail += 1
        code = getattr(r, "status", r)
        print(f"[{i+1}/{len(fl)}] {status.upper():7s} {code} {url[:70]}")
        next_id += 1
        time.sleep(1.2)

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    print(f"\n=== hop-2 fetch: {ok} ok, {fail} failed of {len(fl)} ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
