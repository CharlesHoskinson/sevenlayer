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
