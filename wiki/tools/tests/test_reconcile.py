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
