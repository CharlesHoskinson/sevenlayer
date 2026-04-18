"""Extract the glossary and bibliography sections from the book."""
from __future__ import annotations

import argparse
from pathlib import Path


GLOSSARY_HEADER = "# Glossary of Key Terms"
GLOSSARY_END = "# Part I:"

BIB_HEADER = "# Complete Bibliography"


def slice_between(text: str, start_marker: str, end_marker: str | None) -> str:
    start = text.find(start_marker)
    if start == -1:
        raise SystemExit(f"missing marker: {start_marker!r}")
    if end_marker is None:
        return text[start:]
    end = text.find(end_marker, start + len(start_marker))
    if end == -1:
        raise SystemExit(f"missing end marker: {end_marker!r}")
    return text[start:end]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--book", type=Path, required=True)
    p.add_argument("--glossary-out", type=Path, required=True)
    p.add_argument("--bibliography-out", type=Path, required=True)
    args = p.parse_args()

    text = args.book.read_text(encoding="utf-8")

    gloss = slice_between(text, GLOSSARY_HEADER, GLOSSARY_END).rstrip() + "\n"
    bib = slice_between(text, BIB_HEADER, None).rstrip() + "\n"

    args.glossary_out.write_text(gloss, encoding="utf-8")
    args.bibliography_out.write_text(bib, encoding="utf-8")
    print(f"glossary: {len(gloss)} chars, bibliography: {len(bib)} chars")


if __name__ == "__main__":
    main()
