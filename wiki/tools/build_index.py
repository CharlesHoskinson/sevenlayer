"""Build INDEX.md from the current wiki filesystem state.

Produces a table per directory with three columns:
title | wiki-link | relative-path
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def read_title(md: Path) -> str:
    text = md.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if m:
        for line in m.group(1).splitlines():
            if line.startswith("title:"):
                return line.split(":", 1)[1].strip().strip('"')
    return md.stem


def section_of(dir_label: str, dir_path: Path, wiki_root: Path) -> list[str]:
    files = sorted(dir_path.glob("*.md"))
    if not files:
        return [f"## {dir_label}\n\n_(empty)_\n"]
    out = [f"## {dir_label}\n",
           "| Title | Wiki link | Path |",
           "|-------|-----------|------|"]
    for f in files:
        title = read_title(f)
        rel = f.relative_to(wiki_root).as_posix()
        wiki = f"[[{f.stem}]]"
        out.append(f"| {title} | {wiki} | [{rel}](./{rel}) |")
    out.append("")
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--wiki", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()

    lines = ["# Sevenlayer Wiki Index",
             "",
             "Sidecar index with both Obsidian-style `[[wiki-links]]` and portable markdown paths.",
             ""]
    lines += section_of("Chapters", args.wiki / "chapters", args.wiki)
    lines += section_of("Sections", args.wiki / "sections", args.wiki)
    lines += section_of("Concepts", args.wiki / "concepts", args.wiki)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
