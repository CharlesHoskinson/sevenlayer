# Sevenlayer Wiki — Design Spec

**Date:** 2026-04-18
**Status:** Draft, pending user review
**Scope:** Map `proving-nothing.md` into a structured wiki, then drive a chapter-by-chapter improvement loop off of it.

## Goal

Turn the 5,511-line single-file book `C:/Users/charl/sevenlayer/proving-nothing.md` into a navigable, machine-readable wiki that serves two purposes:

1. **Map** — every `##` section of the book becomes a node with verbatim body + rich metadata.
2. **Surface for improvement** — each node carries audit findings across five dimensions, so a chapter-by-chapter revision loop has an explicit work queue instead of prose judgment alone.

The wiki lives at `C:/Users/charl/sevenlayer/wiki/` in the same git repo as the book.

## Design decisions (as locked with the user)

| # | Decision | Choice |
|---|----------|--------|
| 1 | Wiki granularity | Section-level (every `##` heading = one node, ~85 nodes) |
| 2 | Location | `C:/Users/charl/sevenlayer/wiki/` (inside the book's repo) |
| 3 | Link format | Obsidian `[[wiki-links]]` + portable-markdown sidecar index |
| 4 | Node schema | Rich (improvement-ready) — summary, key claims, entities, dependencies, sources cited, open questions, improvement notes, status |
| 5 | Improvement dimensions | All five — accuracy (A), citations (B), clarity (C), coherence (D), depth (E) |
| 6 | Extraction strategy | Two-phase — parallel mechanical extract, then enrichment pass with global visibility |
| 7 | Done criteria for mapping | Structural + per-chapter audit + prioritized `IMPROVEMENT_BACKLOG.md` |

## Directory layout

```
C:/Users/charl/sevenlayer/wiki/
├── README.md                      # Entry point, navigation overview
├── INDEX.md                       # Portable-markdown sidecar (every wiki link also as [text](path.md))
├── IMPROVEMENT_BACKLOG.md         # Prioritized issue queue from Phase-2 audit
├── GLOSSARY.md                    # Extracted from book front-matter
├── BIBLIOGRAPHY.md                # Extracted from book back-matter
├── chapters/                      # 14 thin hub pages (TOC + audit rollup per chapter)
│   ├── 01-promise.md
│   ├── 02-layer1-setup.md
│   └── … (through 14)
├── sections/                      # ~85 canonical content nodes
│   ├── ch01-the-trick.md
│   ├── ch01-the-proof-at-the-door.md
│   └── …
├── concepts/                      # ~15 cross-cutting entity hubs
│   ├── midnight.md
│   ├── sudoku-running-example.md
│   ├── seven-layer-model.md
│   ├── three-paths.md
│   ├── fourteen-edge-dag.md
│   ├── groth16.md
│   ├── plonk.md
│   ├── starks.md
│   ├── folding-genealogy.md
│   ├── lattice-revolution.md
│   ├── fiat-shamir.md
│   ├── hardness-assumptions.md
│   ├── small-field-revolution.md
│   ├── ceremony-141416.md
│   └── governance-attacks.md
└── _meta/
    ├── schema.md                  # Canonical node template
    ├── section-manifest.json      # Authoritative work assignment for Phase 1
    ├── entity-map.json            # Where each concept appears (built in Phase 2.1)
    ├── extraction-log.md          # Phase-1 agent logs
    └── enrichment-log.md          # Phase-2 agent logs
```

**Slug rule:** `chNN-kebab-case-of-heading`. Chapter hubs use `NN-short-title.md`. Concept hubs use `kebab-slug.md`.

## Node schema (section pages)

Every `sections/*.md` file follows this template verbatim:

```markdown
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
- **Accuracy (A):** …
- **Citations (B):** …
- **Clarity (C):** …
- **Coherence (D):** …
- **Depth (E):** …

## Body
(verbatim section text — authoritative source until rewritten)

## Links
- Up: [[chapters/02-layer1-setup]]
- Prev: [[ch02-preceding-section-slug]]
- Next: [[ch02-following-section-slug]]
```

Chapter hubs and concept hubs share the frontmatter but replace `## Body` with navigation + audit rollup (chapters) or synthesis + cross-reference tables (concepts).

## Phase 1 — Parallel extraction

**Preparation (main agent, sequential):**
1. Create the directory tree above.
2. Scan `proving-nothing.md` once to build `_meta/section-manifest.json` — every `##` heading with chapter number, heading text, slug, and line range. This is the authoritative work assignment.
3. Write `_meta/schema.md` (the node template).
4. Commit: `chore: scaffold wiki skeleton`.

**Dispatch (single message, 14 parallel Explore-type subagents):**
Each agent receives its chapter number, manifest slice, path to `schema.md`, target directory, source file path, and source commit sha. Each produces:
- One `chNN-<slug>.md` per section in its chapter, with frontmatter mechanically populated and verbatim body. All rich fields left as empty placeholder headings (`## Summary`, `## Key claims`, etc.). Status: `untouched`.
- One `chapters/NN-<slug>.md` stub listing its sections.
- A log line to `_meta/extraction-log.md`.

Agents do **not** touch other chapters, do **not** follow cross-references, do **not** write wiki links. Isolated, deterministic, idempotent.

**Reconciliation (main agent, sequential):**
1. Verify every manifest entry produced a file.
2. Confirm no line-range overlaps or gaps.
3. Build initial `INDEX.md` from filesystem listing.
4. Commit: `wiki: phase 1 extraction — 14 chapters, N sections`.

**Failure handling:** extractors are idempotent via the manifest. Rerun only failed chapters.

## Phase 2 — Enrichment + audit

Enrichment needs global visibility, so parallelism is structured.

**2.1 — Global index (main agent, sequential):**
- Read every section file, build `_meta/entity-map.json`: for each recurring entity, list every section that mentions it.
- Seed with ~15 entities from the book's running examples + case studies (Midnight, Sudoku, Groth16, PLONK, STARKs, KZG, FRI, lattice/Ajtai, folding schemes, Fiat-Shamir, small-field revolution, ceremony-141416, governance attacks, Zcash timing, Tornado Cash).
- Auto-detect additional candidates: any capitalized proper noun or acronym appearing in ≥4 sections.
- Commit.

**2.2 — Chapter-parallel enrichment (14 parallel agents):**
Each agent fills, for every section in its chapter: `## Summary`, `## Key claims`, `## Entities` (from entity-map), `## Dependencies`, `## Sources cited`, `## Open questions`, `## Links`. Status transitions `untouched → drafted`. Does **not** yet write `## Improvement notes`.

**2.3 — Concept hubs (main agent, sequential):**
From `entity-map.json`, generate each `concepts/<entity>.md`: summary, canonical definition (may pull from `GLOSSARY.md`), "Where it appears" linking every mentioning section, "Major claims across the book" rollup. Commit.

**2.4 — Per-chapter audit (14 parallel agents):**
Each agent ingests its chapter's sections + all concept hubs + other chapters' summaries. For every section it writes `## Improvement notes` across the five dimensions with severity tags `P0 | P1 | P2 | P3`. Also writes a chapter-level audit report into the chapter hub.

**2.5 — Backlog synthesis (main agent, sequential):**
Roll up all improvement notes into `IMPROVEMENT_BACKLOG.md`: ranked by severity, grouped by chapter, linked to section nodes, status column for loop tracking.

**2.6 — Done criteria:**
- Every section status = `drafted` (not `untouched`).
- Every section has populated rich fields including improvement notes.
- `INDEX.md` complete with both `[[wiki-link]]` and portable-path columns.
- `IMPROVEMENT_BACKLOG.md` exists with prioritized entries.
- Git tag `wiki-v1.0-mapped`.

## Phase 3 — Chapter-by-chapter improvement loop

**Unit of work:** one chapter per cycle. Section-level rewrites risk losing transitions.

**Order:** highest `P0`/`P1` density first, as ranked in `IMPROVEMENT_BACKLOG.md`.

**Cycle:**
1. **Brief.** Read chapter hub audit report. Pull all `P0`/`P1` backlog items scoped to this chapter. Pull the chapter's `## Dependencies` graph (which upstream concepts / sibling chapters are load-bearing).
2. **Research (parallel subagents).**
   - Per disputed claim (A): one research agent verifies against current sources, updates numbers/dates, chases primary citations.
   - Per missing citation (B): one agent walks `## Sources cited` and resolves ePrint IDs / DOIs / URLs.
   - Per thin topic (E): one agent produces a new-material draft at section granularity.
   - Clarity (C) and coherence (D) stay with the main agent.
3. **Rewrite.** Produce `wiki/drafts/chNN-<slug>-v2.md`. Retain the book's voice (terse, human, no AI smells per global CLAUDE.md). Every edit traceable to a backlog item or research finding.
4. **Self-review.** Diff v2 against current state in `proving-nothing.md`. Check: every `P0`/`P1` addressed? Any `## Key claims` across sections contradicted? Cross-chapter references still resolve?
5. **Code-review handoff.** Dispatch `superpowers:code-reviewer` against the draft with the audit report as spec. Fix inline.
6. **Apply.** Replace chapter's line range in `proving-nothing.md`. Update affected section nodes: `drafted → reviewed`, refresh `source_lines`, refresh body, clear addressed improvement notes, bump `source_commit`. Update chapter hub audit report.
7. **Commit.** `book: revise ch NN — <short summary>`. Tag `wiki-ch-NN-revised`. Update `IMPROVEMENT_BACKLOG.md`.
8. **Rebuild artifacts.** Rerun `build_pdf.py` / `build_kindle.py`. Flag any build failure.

**Stop conditions:**
- All 14 chapters cycled through at least once.
- `IMPROVEMENT_BACKLOG.md` has zero open `P0`/`P1` items.
- Every section status = `reviewed` or `finalized`.

**Escape hatches:**
- If a chapter rewrite reveals a cross-chapter structural problem, pause the loop, log a cross-chapter issue to the backlog, resolve it, resume.
- A chapter hub can be manually tagged `status: finalized` to skip revision.

## Constraints carried from the environment

- Git repo exists at `C:/Users/charl/sevenlayer/`. Commit messages: terse, human style. **No AI attribution, no Co-Authored-By lines** (per user's global `CLAUDE.md`).
- No AI smells in any prose output: no "Main theorem:", no "**Proof strategy:**", no "key insight", no numbered proof steps, no excessive formatting.
- All commands must use Unix shell syntax (bash on Windows).
- Use `py C:\Users\charl\.claude\tools\scratchpad.py` at session boundaries to persist state.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Extractor produces inconsistent files (wrong line ranges, drift) | Manifest-driven extraction + reconciliation step that verifies ranges |
| Enrichment agent hallucinates cross-references | `entity-map.json` is authoritative; dependencies must link to real node slugs |
| Audit agents over-flag style in factually fine passages | Improvement notes carry severity tags; improvement loop only acts on `P0`/`P1` |
| Chapter rewrite breaks cross-references | Step 4 self-review diffs against `## Key claims` of dependent sections |
| Build pipeline breaks after text surgery | Step 8 rebuilds artifacts and flags failures immediately |
| Main file surgery corrupts the book | Each rewrite is a single commit; revert is always one `git reset` away |
| Work pauses mid-phase across sessions | Status fields in frontmatter + `IMPROVEMENT_BACKLOG.md` make state durable |

## Out of scope (for this spec)

- The actual content of the revised chapters. That is Phase 3 runtime output, not specification.
- Translation to other languages.
- Web publishing. The wiki is Obsidian-navigable and GitHub-renderable; no hosted site is required.
- Automated fact-checking beyond research-agent queries. Human review remains the final gate.

## Success criteria

End state of the mapping work (Phases 1 + 2):
- `wiki/` exists with the directory layout above.
- ~85 section nodes, 14 chapter hubs, ~15 concept hubs, all cross-linked.
- Every section has rich fields populated and an improvement note set.
- `IMPROVEMENT_BACKLOG.md` ranks outstanding work.
- Git tag `wiki-v1.0-mapped`.

End state of the improvement work (Phase 3):
- `proving-nothing.md` rewritten chapter by chapter with every `P0`/`P1` finding resolved.
- Every section status = `reviewed` or `finalized`.
- Build artifacts (PDF, EPUB, Kindle) regenerated.
- Git tag `book-v2.0-revised`.
