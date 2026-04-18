# Node Schema

Every `sections/*.md` file uses this template verbatim. Chapter hubs and concept hubs share the frontmatter but replace `## Body` with navigation/synthesis content.

## Section page template

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
```

## Slug rule

`chNN-kebab-case-of-heading`. Chapter hubs: `NN-short-title.md`. Concept hubs: `kebab-slug.md`.

## Status transitions

- `untouched` → Phase 1 extraction output, frontmatter + body only
- `drafted` → Phase 2.2 enrichment complete, rich fields filled
- `reviewed` → Phase 3 improvement cycle complete for this section
- `finalized` → manually tagged; section skipped for future revisions
