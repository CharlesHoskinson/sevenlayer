"""Check Phase 1+2 done criteria and print a summary."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def status_of(f: Path) -> str:
    text = f.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return "no-frontmatter"
    for line in m.group(1).splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing-status"


def has_section(f: Path, heading: str) -> bool:
    text = f.read_text(encoding="utf-8")
    pat = re.compile(rf"^## {re.escape(heading)}\s*\n((?:.*\n){{0,3}})", re.MULTILINE)
    m = pat.search(text)
    if not m:
        return False
    content = m.group(1).strip()
    return bool(content) and not content.startswith("## ")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--wiki", type=Path, required=True)
    args = p.parse_args()
    wiki = args.wiki
    sections = list((wiki / "sections").glob("*.md"))

    statuses = Counter(status_of(f) for f in sections)
    print(f"Sections: {len(sections)}")
    for s, n in statuses.most_common():
        print(f"  status={s}: {n}")

    required = ["Summary", "Key claims", "Entities", "Dependencies",
                "Sources cited", "Open questions", "Improvement notes", "Links"]
    gaps = {h: 0 for h in required}
    for f in sections:
        for h in required:
            if not has_section(f, h):
                gaps[h] += 1
    print("\nUnpopulated-section counts:")
    for h, n in gaps.items():
        print(f"  {h}: {n}")

    required_paths = [
        wiki / "INDEX.md",
        wiki / "IMPROVEMENT_BACKLOG.md",
        wiki / "GLOSSARY.md",
        wiki / "BIBLIOGRAPHY.md",
        wiki / "_meta" / "section-manifest.json",
        wiki / "_meta" / "entity-map.json",
    ]
    missing_paths = [p for p in required_paths if not p.exists()]
    if missing_paths:
        print("\nMISSING TOP-LEVEL FILES:")
        for p in missing_paths:
            print(f"  {p}")

    concepts = list((wiki / "concepts").glob("*.md"))
    chapters = list((wiki / "chapters").glob("*.md"))
    print(f"\nChapter hubs: {len(chapters)}")
    print(f"Concept hubs: {len(concepts)}")

    done_ok = (
        statuses.get("drafted", 0) == len(sections)
        and all(n == 0 for n in gaps.values())
        and not missing_paths
        and len(chapters) == 14
        and len(concepts) >= 15
    )
    print(f"\nDONE CRITERIA: {'PASS' if done_ok else 'FAIL'}")
    return 0 if done_ok else 1


if __name__ == "__main__":
    sys.exit(main())
