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
# Bullets appear as: - [P1] (A) text  or  - [none] (B) text  or  - [none] X text
BULLET_RE = re.compile(
    r"^\s*-\s*\[(P[0-3]|none)\]\s*\(?\s*([A-E]|none|X)\)?\s*[—\-–]?\s*(.*?)\s*$"
)

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
