"""Harvest one-hop reference candidates from the chapter references' documents.

Reads every on-disk document belonging to a NON-snowball manifest entry,
extracts URL / arXiv / ePrint / DOI citations, normalizes and dedupes them
against the whole manifest, and writes a ranked candidate list to
references/snowball/hop2-candidates.json. Read-only over the corpus; writes
only the candidate file.
"""
from __future__ import annotations

import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "references" / "manifest.json"
OUT = REPO / "references" / "snowball" / "hop2-candidates.json"

SKIP_DOMAINS = (
    "creativecommons.org", "w3.org", "twitter.com", "x.com", "youtube.com",
    "youtu.be", "fonts.google", "github.com", "gitlab.com", "orcid.org",
    "crossref.org", "linkedin.com", "facebook.com", "medium.com/@",
    "mailto:", "localhost", "example.com", "ctan.org", "latex-project.org",
)

URL_RE = re.compile(r"https?://[^\s<>\)\]\"'}]+")
ARXIV_RE = re.compile(r"arXiv:\s*(\d{4}\.\d{4,5})(v\d+)?", re.IGNORECASE)
EPRINT_RE = re.compile(r"(?:eprint\.iacr\.org|ia\.cr)/(\d{4}/\d{3,4})")
DOI_RE = re.compile(r"\bdoi(?:\.org/|:)\s*(10\.\d{4,9}/[^\s<>\)\]\"']+)", re.IGNORECASE)


def norm(url: str) -> str:
    url = url.rstrip(".,;:)]}\"'")
    url = url.replace("http://", "https://")
    m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", url, re.I)
    if m:
        return f"https://arxiv.org/pdf/{m.group(1)}"
    m = EPRINT_RE.search(url)
    if m:
        return f"https://eprint.iacr.org/{m.group(1)}"
    m = DOI_RE.search(url)
    if m:
        return f"https://doi.org/{m.group(1).rstrip('.,;)')}"
    return url


def doc_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        r = subprocess.run(["pdftotext", "-q", str(path), "-"],
                           capture_output=True, text=True, errors="replace")
        return r.stdout
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    known = set()
    for e in manifest:
        if e.get("url"):
            known.add(norm(e["url"]))
            known.add(norm(e["url"]) + ".pdf")
    chapter_entries = [e for e in manifest if "snowball_round" not in e]

    hits: dict[str, set[str]] = defaultdict(set)
    counts: dict[str, int] = defaultdict(int)
    scanned = 0
    for e in chapter_entries:
        f = e.get("file")
        if not f or not (REPO / f).exists():
            continue
        text = doc_text(REPO / f)
        if not text.strip():
            continue
        scanned += 1
        found = set()
        for m in URL_RE.finditer(text):
            found.add(norm(m.group(0)))
        for m in ARXIV_RE.finditer(text):
            found.add(f"https://arxiv.org/pdf/{m.group(1)}")
        for m in EPRINT_RE.finditer(text):
            found.add(f"https://eprint.iacr.org/{m.group(1)}")
        for m in DOI_RE.finditer(text):
            found.add(f"https://doi.org/{m.group(1).rstrip('.,;)')}")
        for u in found:
            if any(d in u for d in SKIP_DOMAINS):
                continue
            if len(u) > 200 or "..." in u:
                continue
            if norm(u) in known or norm(u).removesuffix(".pdf") in known:
                continue
            hits[u].add(e["slug"])
            counts[u] += 1

    ranked = sorted(hits, key=lambda u: (-len(hits[u]), u))
    out = [{"url": u, "cited_by": sorted(hits[u]), "n_docs": len(hits[u])}
           for u in ranked]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"scanned {scanned} chapter-reference docs")
    print(f"unique new candidate URLs: {len(out)}")
    for row in out[:15]:
        print(f"  {row['n_docs']:2d}x {row['url'][:90]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
