"""Build section-manifest.json from the book source.

Walks `proving-nothing.md`, records every `##` heading inside a numbered
chapter, produces JSON with (chapter, chapter_title, title, slug,
heading_level, source_lines).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CHAPTER_RE = re.compile(r"^# Chapter (\d+):\s*(.+?)\s*$")
SECTION_RE = re.compile(r"^## (.+?)\s*$")


def slugify(text: str) -> str:
    """Kebab-case slug: lowercase, alphanumeric + hyphens only."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def build(book_path: Path) -> dict:
    lines = book_path.read_text(encoding="utf-8").splitlines()
    sections: list[dict] = []
    current_chapter: int | None = None
    current_chapter_title: str | None = None
    pending: dict | None = None

    for idx, raw in enumerate(lines, start=1):
        m_ch = CHAPTER_RE.match(raw)
        if m_ch:
            # close any pending section at line before chapter
            if pending is not None:
                pending["source_lines"][1] = idx - 1
                sections.append(pending)
                pending = None
            current_chapter = int(m_ch.group(1))
            current_chapter_title = m_ch.group(2).strip()
            continue

        if current_chapter is None:
            continue

        m_sec = SECTION_RE.match(raw)
        if m_sec:
            if pending is not None:
                pending["source_lines"][1] = idx - 1
                sections.append(pending)
            title = m_sec.group(1).strip()
            pending = {
                "chapter": current_chapter,
                "chapter_title": current_chapter_title,
                "title": title,
                "slug": f"ch{current_chapter:02d}-{slugify(title)}",
                "heading_level": 2,
                "source_lines": [idx, -1],
            }

    if pending is not None:
        pending["source_lines"][1] = len(lines)
        sections.append(pending)

    return {"sections": sections, "total": len(sections)}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--book", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    data = build(args.book)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
