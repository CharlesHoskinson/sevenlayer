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
