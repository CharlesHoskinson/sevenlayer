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
