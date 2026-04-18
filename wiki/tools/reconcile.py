"""Verify that every manifest entry has a matching section file."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--sections", type=Path, required=True)
    args = p.parse_args()

    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    problems: list[str] = []

    expected_slugs = {entry["slug"] for entry in manifest["sections"]}
    actual_files = {p.stem for p in args.sections.glob("*.md")}

    missing = expected_slugs - actual_files
    extra = actual_files - expected_slugs
    if missing:
        problems.append(f"missing files for slugs: {sorted(missing)}")
    if extra:
        problems.append(f"extra files with no manifest entry: {sorted(extra)}")

    # line-range monotonicity per chapter
    by_ch: dict[int, list[dict]] = {}
    for entry in manifest["sections"]:
        by_ch.setdefault(entry["chapter"], []).append(entry)
    for ch, entries in by_ch.items():
        entries.sort(key=lambda e: e["source_lines"][0])
        prev = 0
        for e in entries:
            s, t = e["source_lines"]
            if s <= prev:
                problems.append(f"ch{ch}: overlap at {e['slug']}")
            if t < s:
                problems.append(f"ch{ch}: bad range at {e['slug']}")
            prev = t

    if problems:
        for p in problems:
            print(p)
        return 1
    print(f"OK: {len(expected_slugs)} sections reconciled")
    return 0


if __name__ == "__main__":
    sys.exit(main())
