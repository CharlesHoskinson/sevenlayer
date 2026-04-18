# Sevenlayer Wiki Mapping — Implementation Plan (Phases 1 + 2)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Map `proving-nothing.md` into a structured wiki at `C:/Users/charl/sevenlayer/wiki/` — ~85 section nodes, 14 chapter hubs, ~15 concept hubs, each with rich metadata and prioritized improvement audit.

**Architecture:** Manifest-driven parallel extraction (Phase 1), then globally-indexed enrichment + audit (Phase 2). Small Python tools handle mechanical work (manifest, entity-map, reconciliation, backlog). Subagents handle content-aware work (summaries, dependencies, audit notes).

**Tech Stack:** Python 3 stdlib for tooling (re, json, pathlib). Obsidian-flavored markdown for wiki files. Git for state tracking. `general-purpose` subagents dispatched via the `Agent` tool for parallel content work.

**Spec:** `docs/superpowers/specs/2026-04-18-sevenlayer-wiki-design.md` (commits `7eaf3e6`, `9b37ead`).

**Worktree note:** Phases 1-2 create files in disjoint paths (each chapter's agents write only to their own slice of `wiki/sections/`). No write conflicts are possible, so a shared workspace is used. Phase 3 (not in this plan) will use isolated worktrees per agent per the user's preference.

**Commit identity:** `Charles Hoskinson <charles.hoskinson@gmail.com>`, passed via `-c user.name=... -c user.email=...` on every commit (the repo has no local or global git identity set). Never run `git config` to persist the identity.

## File structure

Files this plan creates:

```
C:/Users/charl/sevenlayer/
├── wiki/
│   ├── README.md
│   ├── INDEX.md
│   ├── IMPROVEMENT_BACKLOG.md
│   ├── GLOSSARY.md
│   ├── BIBLIOGRAPHY.md
│   ├── chapters/        (14 files)
│   ├── sections/        (~85 files)
│   ├── concepts/        (~15 files)
│   └── _meta/
│       ├── schema.md
│       ├── section-manifest.json
│       ├── entity-map.json
│       ├── extraction-log.md
│       └── enrichment-log.md
└── wiki/tools/
    ├── build_manifest.py
    ├── build_entity_map.py
    ├── build_index.py
    ├── build_concept_hubs.py
    ├── build_backlog.py
    ├── reconcile.py
    ├── stats.py
    └── tests/
        ├── test_build_manifest.py
        ├── test_build_entity_map.py
        └── test_reconcile.py
```

Each tool has one clear responsibility. Tools are small, focused, and independently testable.

---

### Task 1: Scaffold wiki skeleton

**Files:**
- Create: `C:/Users/charl/sevenlayer/wiki/README.md`
- Create: `C:/Users/charl/sevenlayer/wiki/_meta/schema.md`
- Create: `C:/Users/charl/sevenlayer/wiki/_meta/extraction-log.md`
- Create: `C:/Users/charl/sevenlayer/wiki/_meta/enrichment-log.md`
- Create: `C:/Users/charl/sevenlayer/wiki/chapters/.gitkeep`
- Create: `C:/Users/charl/sevenlayer/wiki/sections/.gitkeep`
- Create: `C:/Users/charl/sevenlayer/wiki/concepts/.gitkeep`
- Create: `C:/Users/charl/sevenlayer/wiki/tools/.gitkeep`

- [ ] **Step 1: Create the directory tree**

Run:
```bash
mkdir -p C:/Users/charl/sevenlayer/wiki/{chapters,sections,concepts,_meta,tools,tools/tests}
touch C:/Users/charl/sevenlayer/wiki/chapters/.gitkeep \
      C:/Users/charl/sevenlayer/wiki/sections/.gitkeep \
      C:/Users/charl/sevenlayer/wiki/concepts/.gitkeep \
      C:/Users/charl/sevenlayer/wiki/tools/.gitkeep \
      C:/Users/charl/sevenlayer/wiki/tools/tests/.gitkeep
```

- [ ] **Step 2: Write `wiki/README.md`**

```markdown
# Sevenlayer Wiki

Wiki mapping of `proving-nothing.md` into ~85 section nodes, 14 chapter hubs, ~15 concept hubs.

## Navigation

- [Index (portable links)](./INDEX.md) — markdown links, renders on GitHub.
- Obsidian users: open this folder as a vault; use `[[wiki-links]]` directly.
- Chapter hubs: `./chapters/NN-slug.md` — TOC + audit rollup per chapter.
- Section nodes: `./sections/chNN-slug.md` — canonical content.
- Concept hubs: `./concepts/slug.md` — cross-cutting entity pages (Midnight, Groth16, etc.).
- [Improvement backlog](./IMPROVEMENT_BACKLOG.md) — prioritized queue from the Phase-2 audit.
- [Glossary](./GLOSSARY.md), [Bibliography](./BIBLIOGRAPHY.md).

## Status

Each node has a `status` field in its frontmatter: `untouched | drafted | reviewed | finalized`.

See [`_meta/schema.md`](./_meta/schema.md) for the node template.
```

- [ ] **Step 3: Write `wiki/_meta/schema.md`**

```markdown
# Node Schema

Every `sections/*.md` file uses this template verbatim. Chapter hubs and concept hubs share the frontmatter but replace `## Body` with navigation/synthesis content.

## Section page template

\`\`\`markdown
---
title: "The Fair Shuffle Problem"
slug: ch02-the-fair-shuffle-problem
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [391, 429]
source_commit: <git sha at extraction>
status: untouched                    # untouched | drafted | reviewed | finalized
word_count: 612
---

# The Fair Shuffle Problem

## Summary
2-3 sentence TL;DR.

## Key claims
- Claim 1 (quantitative where present)
- Claim 2

## Entities
- [[midnight]]
- [[ceremony-141416]]

## Dependencies
- [[ch01-the-proof-at-the-door]] — completeness/soundness/zero-knowledge
- [[hardness-assumptions]]

## Sources cited
- Wang, Cohney, Bonneau 2025 — ePrint 2025/064

## Open questions
Flagged by the section itself as unresolved.

## Improvement notes
Populated in Phase 2.4:
- **Accuracy (A):** ...
- **Citations (B):** ...
- **Clarity (C):** ...
- **Coherence (D):** ...
- **Depth (E):** ...

## Body
(verbatim section text — authoritative source until rewritten)

## Links
- Up: [[chapters/02-layer1-setup]]
- Prev: [[ch02-preceding-section-slug]]
- Next: [[ch02-following-section-slug]]
\`\`\`

## Slug rule

`chNN-kebab-case-of-heading`. Chapter hubs: `NN-short-title.md`. Concept hubs: `kebab-slug.md`.

## Status transitions

- `untouched` → Phase 1 extraction output, frontmatter + body only
- `drafted` → Phase 2.2 enrichment complete, rich fields filled
- `reviewed` → Phase 3 improvement cycle complete for this section
- `finalized` → manually tagged; section skipped for future revisions
```

- [ ] **Step 4: Write empty log files**

```bash
printf "# Extraction log\n\nPhase 1 subagent completion records.\n\n" > C:/Users/charl/sevenlayer/wiki/_meta/extraction-log.md
printf "# Enrichment log\n\nPhase 2 subagent completion records.\n\n" > C:/Users/charl/sevenlayer/wiki/_meta/enrichment-log.md
```

- [ ] **Step 5: Commit scaffolding**

```bash
cd C:/Users/charl/sevenlayer
git add wiki/
git -c user.name="Charles Hoskinson" -c user.email="charles.hoskinson@gmail.com" \
  commit -m "chore: scaffold wiki skeleton"
```

Expected: commit succeeds, all files tracked.

---

### Task 2: Write the section-manifest builder with tests

**Files:**
- Create: `C:/Users/charl/sevenlayer/wiki/tools/build_manifest.py`
- Create: `C:/Users/charl/sevenlayer/wiki/tools/tests/test_build_manifest.py`

- [ ] **Step 1: Write the failing test**

Write to `wiki/tools/tests/test_build_manifest.py`:

```python
"""Tests for build_manifest.py."""
import json
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent
ROOT = TOOLS_DIR.parent.parent
BOOK = ROOT / "proving-nothing.md"


def test_manifest_has_expected_chapter_count(tmp_path):
    """The book has 14 chapters; manifest must list entries for each."""
    out = tmp_path / "section-manifest.json"
    subprocess.run(
        [sys.executable, str(TOOLS_DIR / "build_manifest.py"),
         "--book", str(BOOK), "--out", str(out)],
        check=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    chapters = sorted({entry["chapter"] for entry in data["sections"]})
    assert chapters == list(range(1, 15)), chapters


def test_manifest_slug_is_kebab_chnn(tmp_path):
    """Every slug matches chNN-kebab-case pattern."""
    import re
    out = tmp_path / "section-manifest.json"
    subprocess.run(
        [sys.executable, str(TOOLS_DIR / "build_manifest.py"),
         "--book", str(BOOK), "--out", str(out)],
        check=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    slug_re = re.compile(r"^ch\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
    bad = [e["slug"] for e in data["sections"] if not slug_re.match(e["slug"])]
    assert not bad, f"malformed slugs: {bad[:10]}"


def test_manifest_line_ranges_are_monotone(tmp_path):
    """source_lines ranges are non-overlapping and ordered."""
    out = tmp_path / "section-manifest.json"
    subprocess.run(
        [sys.executable, str(TOOLS_DIR / "build_manifest.py"),
         "--book", str(BOOK), "--out", str(out)],
        check=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    prev_end = 0
    for entry in data["sections"]:
        start, end = entry["source_lines"]
        assert start > prev_end, f"overlap/out-of-order at {entry['slug']}"
        assert end >= start, f"invalid range at {entry['slug']}"
        prev_end = end


def test_manifest_captures_part_divider_before_chapter(tmp_path):
    """'# Part II: The Craft' divider must not itself become a section."""
    out = tmp_path / "section-manifest.json"
    subprocess.run(
        [sys.executable, str(TOOLS_DIR / "build_manifest.py"),
         "--book", str(BOOK), "--out", str(out)],
        check=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    titles = [e["title"] for e in data["sections"]]
    assert "Part II: The Craft" not in titles
    assert "Part I: The Invitation" not in titles
```

- [ ] **Step 2: Run the test and confirm it fails**

Run:
```bash
cd C:/Users/charl/sevenlayer/wiki/tools
python -m pytest tests/test_build_manifest.py -v
```

Expected: all four tests FAIL (script doesn't exist yet).

- [ ] **Step 3: Write `build_manifest.py`**

```python
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
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run:
```bash
cd C:/Users/charl/sevenlayer/wiki/tools
python -m pytest tests/test_build_manifest.py -v
```

Expected: 4 PASSED.

- [ ] **Step 5: Build the real manifest and sanity-check**

Run:
```bash
cd C:/Users/charl/sevenlayer
python wiki/tools/build_manifest.py \
  --book proving-nothing.md \
  --out wiki/_meta/section-manifest.json
python -c "
import json
d = json.load(open('wiki/_meta/section-manifest.json', encoding='utf-8'))
print('total sections:', d['total'])
from collections import Counter
c = Counter(s['chapter'] for s in d['sections'])
for ch in sorted(c): print(f'  ch{ch:02d}: {c[ch]} sections')
"
```

Expected: total in the range 70-100; every chapter 1-14 has ≥1 section. If a chapter shows 0, investigate before proceeding.

- [ ] **Step 6: Commit**

```bash
cd C:/Users/charl/sevenlayer
git add wiki/tools/build_manifest.py wiki/tools/tests/test_build_manifest.py wiki/_meta/section-manifest.json
git -c user.name="Charles Hoskinson" -c user.email="charles.hoskinson@gmail.com" \
  commit -m "wiki: section manifest builder + manifest"
```

---

### Task 3: Extract glossary and bibliography

**Files:**
- Create: `C:/Users/charl/sevenlayer/wiki/GLOSSARY.md`
- Create: `C:/Users/charl/sevenlayer/wiki/BIBLIOGRAPHY.md`
- Create: `C:/Users/charl/sevenlayer/wiki/tools/extract_frontback.py`

- [ ] **Step 1: Write `extract_frontback.py`**

```python
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
```

- [ ] **Step 2: Run it**

```bash
cd C:/Users/charl/sevenlayer
python wiki/tools/extract_frontback.py \
  --book proving-nothing.md \
  --glossary-out wiki/GLOSSARY.md \
  --bibliography-out wiki/BIBLIOGRAPHY.md
head -5 wiki/GLOSSARY.md
head -5 wiki/BIBLIOGRAPHY.md
```

Expected: both files start with their respective `#` headings, non-empty.

- [ ] **Step 3: Commit**

```bash
cd C:/Users/charl/sevenlayer
git add wiki/tools/extract_frontback.py wiki/GLOSSARY.md wiki/BIBLIOGRAPHY.md
git -c user.name="Charles Hoskinson" -c user.email="charles.hoskinson@gmail.com" \
  commit -m "wiki: extract glossary and bibliography"
```

---

### Task 4: Dispatch 14 parallel extraction agents (Phase 1 core)

**Files:**
- Create: ~85 files under `C:/Users/charl/sevenlayer/wiki/sections/ch*.md`
- Create: 14 files under `C:/Users/charl/sevenlayer/wiki/chapters/NN-*.md`
- Append: `C:/Users/charl/sevenlayer/wiki/_meta/extraction-log.md`

- [ ] **Step 1: Record the source commit sha for frontmatter**

Run:
```bash
cd C:/Users/charl/sevenlayer
SHA=$(git rev-parse HEAD)
echo "$SHA" > wiki/_meta/.source-commit
echo "Using source_commit=$SHA"
```

- [ ] **Step 2: Dispatch all 14 agents in a single message with 14 parallel `Agent` tool calls**

Each agent gets this prompt template (substitute `<N>` for chapter number, `<CHAPTER_TITLE>` from the manifest):

```
Extract chapter <N> sections from C:/Users/charl/sevenlayer/proving-nothing.md into the wiki.

Read these inputs:
1. The book: C:/Users/charl/sevenlayer/proving-nothing.md
2. The manifest: C:/Users/charl/sevenlayer/wiki/_meta/section-manifest.json — filter to entries with chapter == <N>. Each entry gives you title, slug, source_lines.
3. The schema: C:/Users/charl/sevenlayer/wiki/_meta/schema.md
4. The source commit: read C:/Users/charl/sevenlayer/wiki/_meta/.source-commit

For each manifest entry matching chapter <N>:

a. Write C:/Users/charl/sevenlayer/wiki/sections/<slug>.md with:
   - YAML frontmatter filled with: title, slug, chapter (<N>), chapter_title (<CHAPTER_TITLE>), heading_level (2), source_lines (from manifest), source_commit (from .source-commit file), status ("untouched"), word_count (count whitespace-separated tokens in body).
   - Body is the verbatim text from the book at source_lines[0]..source_lines[1] INCLUSIVE, starting at the ## heading line. Do NOT trim, reformat, or "fix" the body. Preserve every blank line.
   - Below the body, append empty placeholder sections in this order, each on its own line: "## Summary", "## Key claims", "## Entities", "## Dependencies", "## Sources cited", "## Open questions", "## Improvement notes", "## Links". Each heading followed by one blank line. No content under them yet.

b. Also write C:/Users/charl/sevenlayer/wiki/chapters/<NN>-<kebab-chapter-title>.md (kebab-case of CHAPTER_TITLE, strip "Layer N --" etc., keep it short) with:
   - Frontmatter: title (CHAPTER_TITLE), chapter (<N>), status ("untouched")
   - A "## Sections" markdown list of [[wiki-links]] to each of this chapter's sections in order.
   - An empty "## Audit rollup" section.

c. After writing all files, append one line to C:/Users/charl/sevenlayer/wiki/_meta/extraction-log.md:
   "- chapter <N>: <count> sections extracted, <slug list>"

Rules:
- Write files only. Never read or modify files outside this chapter's slugs or the single log append.
- Preserve the book's text verbatim inside the body. No paraphrase, no trimming, no re-wrapping.
- If you encounter a section whose source_lines don't line up with a ## heading in the book, stop and report the discrepancy rather than guessing.

Report when done: "<N> sections written for chapter <N>."
```

**Orchestrator action:** issue these as 14 `Agent` tool calls in ONE message. Each call uses `subagent_type: general-purpose`, a distinct `name` like `ch01-extractor` through `ch14-extractor`, and a `description` like "Extract chapter <N>".

- [ ] **Step 3: Verify every agent reported success**

Check the tool results in the same message. Every agent should say "<M> sections written for chapter <N>." with M matching the manifest count. If any agent failed or reported a discrepancy, rerun only that chapter's agent with the same prompt.

- [ ] **Step 4: Commit**

```bash
cd C:/Users/charl/sevenlayer
rm wiki/_meta/.source-commit
git add wiki/sections/ wiki/chapters/ wiki/_meta/extraction-log.md
git -c user.name="Charles Hoskinson" -c user.email="charles.hoskinson@gmail.com" \
  commit -m "wiki: phase 1 extraction"
```

---

### Task 5: Reconciliation check

**Files:**
- Create: `C:/Users/charl/sevenlayer/wiki/tools/reconcile.py`
- Create: `C:/Users/charl/sevenlayer/wiki/tools/tests/test_reconcile.py`

- [ ] **Step 1: Write the failing test**

`wiki/tools/tests/test_reconcile.py`:

```python
"""Tests for reconcile.py."""
import json
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent
ROOT = TOOLS_DIR.parent.parent
WIKI = ROOT / "wiki"


def test_reconcile_returns_zero_on_real_wiki():
    """Real wiki state must reconcile cleanly after Task 4."""
    r = subprocess.run(
        [sys.executable, str(TOOLS_DIR / "reconcile.py"),
         "--manifest", str(WIKI / "_meta" / "section-manifest.json"),
         "--sections", str(WIKI / "sections")],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr


def test_reconcile_detects_missing_file(tmp_path):
    """If a manifest entry has no corresponding section file, exit non-zero."""
    manifest = tmp_path / "m.json"
    manifest.write_text(json.dumps({
        "sections": [
            {"slug": "ch99-nonexistent", "chapter": 99, "title": "x",
             "chapter_title": "x", "heading_level": 2, "source_lines": [1, 2]}
        ],
        "total": 1,
    }))
    empty_sections = tmp_path / "sections"
    empty_sections.mkdir()
    r = subprocess.run(
        [sys.executable, str(TOOLS_DIR / "reconcile.py"),
         "--manifest", str(manifest),
         "--sections", str(empty_sections)],
        capture_output=True, text=True,
    )
    assert r.returncode != 0
    assert "missing" in r.stdout.lower() or "missing" in r.stderr.lower()
```

- [ ] **Step 2: Run the test, see the real-wiki test fail because script doesn't exist**

```bash
cd C:/Users/charl/sevenlayer/wiki/tools
python -m pytest tests/test_reconcile.py -v
```

Expected: both tests FAIL (script not yet written).

- [ ] **Step 3: Write `reconcile.py`**

```python
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
```

- [ ] **Step 4: Run the tests**

```bash
cd C:/Users/charl/sevenlayer/wiki/tools
python -m pytest tests/test_reconcile.py -v
```

Expected: both PASSED.

- [ ] **Step 5: Run reconciliation on the real wiki**

```bash
cd C:/Users/charl/sevenlayer
python wiki/tools/reconcile.py \
  --manifest wiki/_meta/section-manifest.json \
  --sections wiki/sections
```

Expected: `OK: N sections reconciled`. If it fails, return to Task 4 step 3 for the failing chapter and re-dispatch.

- [ ] **Step 6: Commit**

```bash
cd C:/Users/charl/sevenlayer
git add wiki/tools/reconcile.py wiki/tools/tests/test_reconcile.py
git -c user.name="Charles Hoskinson" -c user.email="charles.hoskinson@gmail.com" \
  commit -m "wiki: reconciliation tool"
```

---

### Task 6: Build initial INDEX.md

**Files:**
- Create: `C:/Users/charl/sevenlayer/wiki/tools/build_index.py`
- Create: `C:/Users/charl/sevenlayer/wiki/INDEX.md`

- [ ] **Step 1: Write `build_index.py`**

```python
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
```

- [ ] **Step 2: Run it**

```bash
cd C:/Users/charl/sevenlayer
python wiki/tools/build_index.py --wiki wiki --out wiki/INDEX.md
head -30 wiki/INDEX.md
```

Expected: INDEX.md populated with all chapters, sections listed. Concepts section will show `_(empty)_` — that's expected until Task 10.

- [ ] **Step 3: Commit**

```bash
cd C:/Users/charl/sevenlayer
git add wiki/tools/build_index.py wiki/INDEX.md
git -c user.name="Charles Hoskinson" -c user.email="charles.hoskinson@gmail.com" \
  commit -m "wiki: build INDEX.md sidecar"
```

---

### Task 7: Build entity map (Phase 2.1)

**Files:**
- Create: `C:/Users/charl/sevenlayer/wiki/tools/build_entity_map.py`
- Create: `C:/Users/charl/sevenlayer/wiki/tools/tests/test_build_entity_map.py`
- Create: `C:/Users/charl/sevenlayer/wiki/_meta/entity-map.json`

- [ ] **Step 1: Write the failing test**

`wiki/tools/tests/test_build_entity_map.py`:

```python
"""Tests for build_entity_map.py."""
import json
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent
ROOT = TOOLS_DIR.parent.parent
WIKI = ROOT / "wiki"


def test_midnight_appears_in_many_sections(tmp_path):
    """Midnight is a book-wide running example; must span chapters 2, 3, 4, 6, 7, 8, 12."""
    out = tmp_path / "entity-map.json"
    subprocess.run(
        [sys.executable, str(TOOLS_DIR / "build_entity_map.py"),
         "--sections", str(WIKI / "sections"),
         "--seeds", "midnight", "--out", str(out)],
        check=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    chapters = {int(slug[2:4]) for slug in data["midnight"]}
    # Midnight is explicitly analyzed in chapters 2, 3, 4, 6, 7, 8, 12
    required = {2, 3, 4, 12}
    missing = required - chapters
    assert not missing, f"missing chapters for Midnight: {missing}"


def test_seeds_are_always_emitted(tmp_path):
    """Seed entities appear in the output even if empty."""
    out = tmp_path / "entity-map.json"
    subprocess.run(
        [sys.executable, str(TOOLS_DIR / "build_entity_map.py"),
         "--sections", str(WIKI / "sections"),
         "--seeds", "bogusterm", "--out", str(out)],
        check=True,
    )
    data = json.loads(out.read_text(encoding="utf-8"))
    assert "bogusterm" in data
```

- [ ] **Step 2: Run the test and confirm it fails**

```bash
cd C:/Users/charl/sevenlayer/wiki/tools
python -m pytest tests/test_build_entity_map.py -v
```

Expected: FAIL, script missing.

- [ ] **Step 3: Write `build_entity_map.py`**

```python
"""Build entity-map.json: which sections mention which entities.

Seeds are case-insensitive substring matches against section body text.
Auto-discovery finds proper-noun-ish tokens (capitalized or ALL-CAPS acronyms)
that appear in >= 4 distinct sections.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


DEFAULT_SEEDS = [
    "midnight", "sudoku", "groth16", "plonk", "starks", "kzg", "fri",
    "lattice", "ajtai", "folding", "nova", "hypernova", "fiat-shamir",
    "small-field", "mersenne", "babybear", "goldilocks",
    "ceremony", "tornado cash", "beanstalk", "zcash", "poseidon",
    "circle stark", "jolt", "lasso", "logup", "spartan", "halo2",
    "bls12-381", "bn254", "jubjub",
]

BODY_RE = re.compile(r"^## Body\s*\n(.*?)(?=^## )", re.DOTALL | re.MULTILINE)
TOKEN_RE = re.compile(r"\b([A-Z][A-Za-z0-9]{2,}|[A-Z]{2,}[0-9]*)\b")


def extract_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = BODY_RE.search(text + "\n## SENTINEL\n")
    return m.group(1) if m else text


def build(sections_dir: Path, seeds: list[str]) -> dict[str, list[str]]:
    bodies: dict[str, str] = {}
    for f in sorted(sections_dir.glob("*.md")):
        bodies[f.stem] = extract_body(f).lower()

    out: dict[str, list[str]] = {}
    for seed in seeds:
        s = seed.lower()
        hits = sorted(slug for slug, body in bodies.items() if s in body)
        out[seed] = hits

    # Auto-discovery: proper-noun-ish tokens in >= 4 sections
    token_sections: dict[str, set[str]] = defaultdict(set)
    for f in sorted(sections_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        for m in TOKEN_RE.finditer(text):
            tok = m.group(1)
            token_sections[tok].add(f.stem)
    for tok, slugs in token_sections.items():
        key = tok.lower()
        if len(slugs) >= 4 and key not in out:
            out[key] = sorted(slugs)

    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sections", type=Path, required=True)
    p.add_argument("--seeds", nargs="*", default=DEFAULT_SEEDS)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    data = build(args.sections, args.seeds)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(data)} entities mapped to {sum(len(v) for v in data.values())} total hits")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run the tests**

```bash
cd C:/Users/charl/sevenlayer/wiki/tools
python -m pytest tests/test_build_entity_map.py -v
```

Expected: both PASSED.

- [ ] **Step 5: Build the real entity map**

```bash
cd C:/Users/charl/sevenlayer
python wiki/tools/build_entity_map.py \
  --sections wiki/sections \
  --out wiki/_meta/entity-map.json
python -c "
import json
d = json.load(open('wiki/_meta/entity-map.json', encoding='utf-8'))
print('entities:', len(d))
top = sorted(d.items(), key=lambda kv: -len(kv[1]))[:15]
for k, v in top: print(f'  {k}: {len(v)} sections')
"
```

Expected: 20-60 entities; Midnight and at least one of {Groth16, STARKs, KZG} in the top 15.

- [ ] **Step 6: Commit**

```bash
cd C:/Users/charl/sevenlayer
git add wiki/tools/build_entity_map.py wiki/tools/tests/test_build_entity_map.py wiki/_meta/entity-map.json
git -c user.name="Charles Hoskinson" -c user.email="charles.hoskinson@gmail.com" \
  commit -m "wiki: entity map builder + entity-map.json"
```

---

### Task 8: Dispatch 14 parallel enrichment agents (Phase 2.2)

**Files:**
- Modify: ~85 files under `wiki/sections/` (fill rich fields, except `## Improvement notes`)
- Append: `wiki/_meta/enrichment-log.md`

- [ ] **Step 1: Record source commit for log**

```bash
cd C:/Users/charl/sevenlayer
SHA=$(git rev-parse HEAD)
echo "$SHA" > wiki/_meta/.enrichment-commit
```

- [ ] **Step 2: Dispatch 14 parallel agents in one message**

Each agent prompt (substitute `<N>`):

```
Enrich chapter <N> section nodes in C:/Users/charl/sevenlayer/wiki/sections/.

Read these inputs:
1. Every file C:/Users/charl/sevenlayer/wiki/sections/ch<NN>-*.md (two-digit NN).
2. The entity map: C:/Users/charl/sevenlayer/wiki/_meta/entity-map.json (JSON: entity → list of slugs).
3. The glossary: C:/Users/charl/sevenlayer/wiki/GLOSSARY.md.
4. The manifest: C:/Users/charl/sevenlayer/wiki/_meta/section-manifest.json (for chapter ordering).

For each chapter-<N> section file:

a. Under "## Summary" write a 2-3 sentence TL;DR of the body. Be terse. No AI smells ("key insight", "crucial to note", etc.). No introductory framing. Start with the claim.

b. Under "## Key claims" write 3-8 bullets, one per substantive claim in the body. Include quantitative detail where the body has it (numbers, percentages, dollar amounts).

c. Under "## Entities" list every entity from entity-map.json whose slug list contains THIS section's slug. Format: "- [[entity-name]]". Sort alphabetically.

d. Under "## Dependencies" list concepts this section assumes the reader already understands. Each is a wiki link to either another section slug or a concept slug (concepts are named like the entity keys in entity-map.json). Add a one-line annotation after each link describing what's depended on. Dependencies should be real (present in the book) — do not invent them. Typical dependency count: 2-6.

e. Under "## Sources cited" list citations that appear IN THIS SECTION's body (named authors, ePrint IDs, paper titles, URLs). Do not speculate — only what the section itself cites. If none, write "None in this section.".

f. Under "## Open questions" list things the section itself flags as unresolved or gestures at without settling. If none, write "None flagged by this section.".

g. Under "## Links" write:
   - "Up: [[chapters/<NN>-<chapter-slug>]]" (find the chapter file in C:/Users/charl/sevenlayer/wiki/chapters/)
   - "Prev: [[<previous section slug in this chapter>]]" or "Prev: —" for the first section in the chapter
   - "Next: [[<next section slug in this chapter>]]" or "Next: —" for the last section in the chapter
   Use the manifest to determine ordering.

h. Leave "## Improvement notes" empty for now — it's filled in Task 10.

i. Update the file's frontmatter: set status to "drafted".

After all files in chapter <N> are enriched, append one line to C:/Users/charl/sevenlayer/wiki/_meta/enrichment-log.md:
"- chapter <N> enriched: <count> sections, commit <sha from .enrichment-commit>"

Rules:
- Never touch files outside wiki/sections/ch<NN>-*.md or the single log append.
- Preserve the existing "## Body" content exactly. Do not re-read or copy-edit the body.
- If you encounter a section whose body is missing or appears truncated, stop and report rather than guessing.

Report when done: "chapter <N> enriched: <count> sections."
```

**Orchestrator action:** 14 `Agent` tool calls in ONE message, `subagent_type: general-purpose`, names `ch01-enricher` through `ch14-enricher`.

- [ ] **Step 3: Verify every agent reported success**

If any failed, rerun only the failing chapter's agent.

- [ ] **Step 4: Spot-check three sections manually**

```bash
cd C:/Users/charl/sevenlayer
for slug in ch01-the-trick ch05-ccs-the-rosetta-stone ch12-midnight-at-a-glance; do
  echo "=== $slug ==="
  grep -A2 "## Summary" wiki/sections/$slug.md | head -5
  grep -c "^- \[\[" wiki/sections/$slug.md
  grep "^status:" wiki/sections/$slug.md
done
```

Expected: each file has non-empty Summary, a handful of `[[...]]` links, and `status: drafted`.

- [ ] **Step 5: Commit**

```bash
cd C:/Users/charl/sevenlayer
rm wiki/_meta/.enrichment-commit
git add wiki/sections/ wiki/_meta/enrichment-log.md
git -c user.name="Charles Hoskinson" -c user.email="charles.hoskinson@gmail.com" \
  commit -m "wiki: phase 2.2 enrichment"
```

---

### Task 9: Generate concept hubs (Phase 2.3)

**Files:**
- Create: `C:/Users/charl/sevenlayer/wiki/tools/build_concept_hubs.py`
- Create: `C:/Users/charl/sevenlayer/wiki/concepts/*.md` (one per seed entity)

- [ ] **Step 1: Write `build_concept_hubs.py`**

```python
"""Generate one concepts/<entity>.md hub per seed entity.

Each hub contains:
- Frontmatter with slug, status (untouched).
- Summary placeholder.
- "Canonical definition" — pulled from GLOSSARY.md if the entity's display name matches a glossary term.
- "Where it appears" — table of slug → title for every section in entity-map.json[entity].
- "Major claims across the book" — placeholder (filled later by hand or in Phase 3).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SEED_DISPLAY = {
    "midnight": "Midnight",
    "sudoku": "Sudoku running example",
    "groth16": "Groth16",
    "plonk": "PLONK",
    "starks": "STARKs",
    "kzg": "KZG",
    "fri": "FRI",
    "lattice": "Lattice cryptography",
    "ajtai": "Ajtai commitments",
    "folding": "Folding schemes",
    "nova": "Nova",
    "hypernova": "HyperNova",
    "fiat-shamir": "Fiat-Shamir transform",
    "small-field": "Small-field revolution",
    "mersenne": "Mersenne-31 / M31",
    "babybear": "BabyBear",
    "goldilocks": "Goldilocks field",
    "ceremony": "Trusted setup ceremonies",
    "tornado cash": "Tornado Cash",
    "beanstalk": "Beanstalk",
    "zcash": "Zcash",
    "poseidon": "Poseidon hash",
    "circle stark": "Circle STARKs",
    "jolt": "Jolt zkVM",
    "lasso": "Lasso",
    "logup": "LogUp",
    "spartan": "Spartan",
    "halo2": "Halo 2",
    "bls12-381": "BLS12-381",
    "bn254": "BN254",
    "jubjub": "Jubjub curve",
}

FRONTMATTER_TITLE = re.compile(r'^title:\s*"?(.+?)"?\s*$', re.MULTILINE)


def slugify(key: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", key.lower()).strip("-")


def section_title(section_file: Path) -> str:
    text = section_file.read_text(encoding="utf-8")
    m = FRONTMATTER_TITLE.search(text)
    return m.group(1) if m else section_file.stem


def glossary_term(glossary_text: str, display: str) -> str | None:
    # Match "**<display>** -- ..." lines (or variants with " /")
    for line in glossary_text.splitlines():
        if line.startswith(f"**{display}**") or line.startswith(f"**{display.split()[0]}"):
            return line.split("--", 1)[1].strip() if "--" in line else line
    return None


def build(entity_map: dict[str, list[str]], sections_dir: Path,
          glossary_text: str, out_dir: Path, keys: list[str]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for key in keys:
        slugs = entity_map.get(key, [])
        display = SEED_DISPLAY.get(key, key.title())
        slug = slugify(key)
        frontmatter = (
            "---\n"
            f'title: "{display}"\n'
            f"slug: {slug}\n"
            "kind: concept\n"
            "status: untouched\n"
            "---\n\n"
        )
        body = [f"# {display}", ""]
        body += ["## Summary", "_(1-2 paragraph synthesis; fill during Phase 3)_", ""]
        canon = glossary_term(glossary_text, display)
        body += ["## Canonical definition",
                 canon if canon else "_(not in glossary; define during Phase 3)_",
                 ""]
        body += ["## Where it appears", "",
                 "| Slug | Title |", "|------|-------|"]
        if slugs:
            for s in slugs:
                f = sections_dir / f"{s}.md"
                title = section_title(f) if f.exists() else s
                body.append(f"| [[{s}]] | {title} |")
        else:
            body.append("| _(none)_ | |")
        body += ["", "## Major claims across the book",
                 "_(synthesis; fill during Phase 3)_", ""]
        (out_dir / f"{slug}.md").write_text(frontmatter + "\n".join(body) + "\n", encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--entity-map", type=Path, required=True)
    p.add_argument("--sections", type=Path, required=True)
    p.add_argument("--glossary", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--keys", nargs="*", default=list(SEED_DISPLAY.keys()))
    args = p.parse_args()
    entity_map = json.loads(args.entity_map.read_text(encoding="utf-8"))
    glossary_text = args.glossary.read_text(encoding="utf-8")
    build(entity_map, args.sections, glossary_text, args.out, args.keys)
    print(f"wrote {len(args.keys)} concept hubs to {args.out}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it**

```bash
cd C:/Users/charl/sevenlayer
python wiki/tools/build_concept_hubs.py \
  --entity-map wiki/_meta/entity-map.json \
  --sections wiki/sections \
  --glossary wiki/GLOSSARY.md \
  --out wiki/concepts
ls wiki/concepts/ | wc -l
head -25 wiki/concepts/midnight.md
```

Expected: ~30 concept files; `midnight.md` has a populated "Where it appears" table with ≥10 rows.

- [ ] **Step 3: Regenerate INDEX.md to include concepts**

```bash
cd C:/Users/charl/sevenlayer
python wiki/tools/build_index.py --wiki wiki --out wiki/INDEX.md
```

- [ ] **Step 4: Commit**

```bash
cd C:/Users/charl/sevenlayer
git add wiki/tools/build_concept_hubs.py wiki/concepts/ wiki/INDEX.md
git -c user.name="Charles Hoskinson" -c user.email="charles.hoskinson@gmail.com" \
  commit -m "wiki: phase 2.3 concept hubs"
```

---

### Task 10: Dispatch 14 parallel audit agents (Phase 2.4)

**Files:**
- Modify: all section files (fill `## Improvement notes`)
- Modify: all chapter hub files (fill `## Audit rollup`)

- [ ] **Step 1: Dispatch 14 parallel audit agents in one message**

Each agent prompt (substitute `<N>`):

```
Audit chapter <N> of the Sevenlayer wiki.

Read these inputs:
1. C:/Users/charl/sevenlayer/wiki/sections/ch<NN>-*.md (all section files for this chapter).
2. C:/Users/charl/sevenlayer/wiki/concepts/ (all concept hubs — for cross-chapter context).
3. C:/Users/charl/sevenlayer/wiki/chapters/<NN>-*.md (this chapter's hub).
4. Other chapters' summary sections by scanning C:/Users/charl/sevenlayer/wiki/sections/ch*-*.md for their "## Summary" blocks (just the summaries, to spot contradictions).

For each chapter-<N> section file, replace the contents of "## Improvement notes" with bullets across five dimensions. Each bullet is prefixed by a severity tag in brackets and the dimension letter.

Dimensions:
- A. Accuracy & currency — outdated figures, wrong attributions, unverified claims.
- B. Citations & sources — quantitative claim with no reference, missing ePrint/DOI, broken URL.
- C. Clarity & style — verbose passages, AI smells (e.g., "key insight", "it is worth noting", numbered proof-style lists, excessive bolding), weak transitions, repetition.
- D. Structural coherence — contradicts another chapter or concept hub, inconsistent terminology, numbers that don't reconcile.
- E. Depth / new material — thin treatment, missing subtopic, surface-level claim that should be expanded.

Severity:
- P0 — factual error or contradiction; must fix before revision ships.
- P1 — major gap or serious style issue; address in Phase 3.
- P2 — minor polish; nice-to-have.
- P3 — note for future, not a blocker.

Format each bullet:
"- [P?] (A|B|C|D|E) <finding, 1-2 sentences, with inline quote or line reference when possible>"

If a dimension has no findings, write:
"- [none] A — no issues found."

Keep the list honest. If a section is solid, a short list is the correct output. If a section has deep problems, write more bullets.

After finishing all sections in chapter <N>, append to C:/Users/charl/sevenlayer/wiki/chapters/<NN>-*.md under "## Audit rollup":
- Total findings by severity (e.g., "P0: 2, P1: 7, P2: 12, P3: 4")
- Top 5 most severe findings across the chapter, each with section slug and quoted bullet
- Any cross-section patterns (e.g., "recurring AI smell: 'key insight' used in 4 sections")

Rules:
- Never modify "## Body" or any other field.
- Do not touch files outside wiki/sections/ch<NN>-*.md and wiki/chapters/<NN>-*.md.
- Status in frontmatter stays "drafted" (unchanged).

Report when done: "chapter <N> audited: P0=<a>, P1=<b>, P2=<c>, P3=<d>."
```

**Orchestrator action:** 14 `Agent` tool calls in ONE message, `subagent_type: general-purpose`, names `ch01-auditor` through `ch14-auditor`.

- [ ] **Step 2: Collect the counts**

From the agent reports, record each chapter's P0/P1/P2/P3 totals. These feed Task 11.

- [ ] **Step 3: Commit**

```bash
cd C:/Users/charl/sevenlayer
git add wiki/sections/ wiki/chapters/
git -c user.name="Charles Hoskinson" -c user.email="charles.hoskinson@gmail.com" \
  commit -m "wiki: phase 2.4 audit"
```

---

### Task 11: Synthesize IMPROVEMENT_BACKLOG.md (Phase 2.5)

**Files:**
- Create: `C:/Users/charl/sevenlayer/wiki/tools/build_backlog.py`
- Create: `C:/Users/charl/sevenlayer/wiki/IMPROVEMENT_BACKLOG.md`

- [ ] **Step 1: Write `build_backlog.py`**

```python
"""Walk every section's `## Improvement notes` and produce the backlog."""
from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
IMPROVEMENT_RE = re.compile(
    r"^## Improvement notes\s*\n(.*?)(?=^## )", re.DOTALL | re.MULTILINE
)
BULLET_RE = re.compile(r"^\s*-\s*\[(P[0-3]|none)\]\s*([A-E]|none)\s*[—\-–]?\s*(.*?)\s*$")

SEVERITY_ORDER = ["P0", "P1", "P2", "P3"]


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER_RE.match(text)
    out: dict = {}
    if not m:
        return out
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out


def collect(sections_dir: Path) -> list[dict]:
    findings: list[dict] = []
    for f in sorted(sections_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        m = IMPROVEMENT_RE.search(text + "\n## SENTINEL\n")
        if not m:
            continue
        block = m.group(1)
        for line in block.splitlines():
            bm = BULLET_RE.match(line)
            if not bm:
                continue
            sev, dim, body = bm.group(1), bm.group(2), bm.group(3)
            if sev == "none":
                continue
            findings.append({
                "slug": f.stem,
                "chapter": int(fm.get("chapter", 0)),
                "title": fm.get("title", f.stem),
                "severity": sev,
                "dimension": dim,
                "finding": body,
            })
    return findings


def render(findings: list[dict]) -> str:
    by_sev: dict[str, list[dict]] = defaultdict(list)
    for f in findings:
        by_sev[f["severity"]].append(f)

    lines = ["# Improvement Backlog", "",
             "Auto-generated from `## Improvement notes` in every section.",
             "Regenerate with `python wiki/tools/build_backlog.py`.", ""]
    total = len(findings)
    lines.append(f"**Totals:** {total} open findings — " +
                 ", ".join(f"{s}: {len(by_sev[s])}" for s in SEVERITY_ORDER))
    lines.append("")

    for sev in SEVERITY_ORDER:
        items = by_sev[sev]
        if not items:
            continue
        lines += [f"## {sev} ({len(items)})", "",
                  "| Status | Ch | Slug | Dim | Finding |",
                  "|--------|----|------|-----|---------|"]
        items.sort(key=lambda x: (x["chapter"], x["slug"]))
        for f in items:
            one = f["finding"].replace("|", "\\|")
            lines.append(
                f"| [ ] | {f['chapter']:02d} | [[{f['slug']}]] | {f['dimension']} | {one} |"
            )
        lines.append("")

    lines += ["## Per-chapter density", "",
              "| Ch | P0 | P1 | P2 | P3 | Total |",
              "|----|----|----|----|----|-------|"]
    per_ch: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for f in findings:
        per_ch[f["chapter"]][f["severity"]] += 1
    for ch in sorted(per_ch):
        row = per_ch[ch]
        t = sum(row.values())
        lines.append(
            f"| {ch:02d} | {row['P0']} | {row['P1']} | {row['P2']} | {row['P3']} | {t} |"
        )
    lines.append("")
    lines += ["## Revision order (by P0+P1 density, descending)", ""]
    ranked = sorted(per_ch.items(), key=lambda kv: -(kv[1]["P0"] + kv[1]["P1"]))
    for ch, row in ranked:
        lines.append(f"- Chapter {ch:02d}: P0+P1 = {row['P0'] + row['P1']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sections", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    findings = collect(args.sections)
    args.out.write_text(render(findings), encoding="utf-8")
    print(f"wrote {args.out} ({len(findings)} findings)")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run it**

```bash
cd C:/Users/charl/sevenlayer
python wiki/tools/build_backlog.py \
  --sections wiki/sections \
  --out wiki/IMPROVEMENT_BACKLOG.md
head -40 wiki/IMPROVEMENT_BACKLOG.md
```

Expected: populated tables. The "Revision order" at the bottom tells Phase 3 which chapter to start with.

- [ ] **Step 3: Commit**

```bash
cd C:/Users/charl/sevenlayer
git add wiki/tools/build_backlog.py wiki/IMPROVEMENT_BACKLOG.md
git -c user.name="Charles Hoskinson" -c user.email="charles.hoskinson@gmail.com" \
  commit -m "wiki: phase 2.5 improvement backlog"
```

---

### Task 12: Final verification and tag

**Files:**
- Create: `C:/Users/charl/sevenlayer/wiki/tools/stats.py`

- [ ] **Step 1: Write `stats.py`**

```python
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
    # A section is "populated" if the heading exists and the line following
    # it is not empty within the next 3 lines.
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
```

- [ ] **Step 2: Run it**

```bash
cd C:/Users/charl/sevenlayer
python wiki/tools/stats.py --wiki wiki
```

Expected output:
- Total sections 70-100, all `status=drafted`.
- Every required section populated (gap counts all zero).
- 14 chapter hubs, ≥15 concept hubs.
- All required files present.
- `DONE CRITERIA: PASS`.

If it prints FAIL, identify the failing criterion and go back to the relevant task. Do NOT tag until PASS.

- [ ] **Step 3: Commit stats.py and tag**

```bash
cd C:/Users/charl/sevenlayer
git add wiki/tools/stats.py
git -c user.name="Charles Hoskinson" -c user.email="charles.hoskinson@gmail.com" \
  commit -m "wiki: done-criteria stats tool"
git tag wiki-v1.0-mapped
echo "Wiki mapping complete. Phase 3 improvement loop is handled by a separate plan."
```

---

## Self-review (post-write)

**Spec coverage check:**
- Directory layout (spec §3) → Task 1 ✓
- Node schema (spec §4) → schema.md in Task 1, applied by Tasks 4 & 8 ✓
- Phase 1 preparation (spec §5 prep steps 1-4) → Tasks 1, 2, 3 ✓ (step 3 of spec "Write `_meta/schema.md`" is Task 1 step 3)
- Phase 1 dispatch (spec §5) → Task 4 ✓
- Phase 1 reconciliation (spec §5) → Task 5 (verify) + Task 6 (INDEX.md) ✓
- Phase 2.1 entity map (spec §6.1) → Task 7 ✓
- Phase 2.2 enrichment (spec §6.2) → Task 8 ✓
- Phase 2.3 concept hubs (spec §6.3) → Task 9 ✓
- Phase 2.4 audit (spec §6.4) → Task 10 ✓
- Phase 2.5 backlog (spec §6.5) → Task 11 ✓
- Phase 2.6 done criteria (spec §6.6) → Task 12 ✓

**Placeholder scan:** no `TBD`/`TODO`/"fill in later"/"similar to Task N" in the plan itself. The concept hub generator writes intentional placeholders ("_(fill during Phase 3)_") into hub pages — but those are Phase 3 work, not plan placeholders.

**Type consistency:** status values (`untouched` → `drafted` → `reviewed` → `finalized`) used identically in Tasks 1, 4, 8, 12. Slug format (`chNN-kebab`) consistent across manifest, sections, reconcile. Severity tags (`P0..P3`) consistent between audit prompt (Task 10) and backlog parser (Task 11).

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-04-18-sevenlayer-wiki-mapping.md`. Two execution options:

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks, fast iteration.
2. **Inline Execution** — execute tasks in this session using executing-plans, batch execution with checkpoints.

Which approach?
