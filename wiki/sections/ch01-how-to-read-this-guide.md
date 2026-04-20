---
title: "How to Read This Guide"
slug: ch01-how-to-read-this-guide
chapter: 1
chapter_title: "The Promise of Provable and Programmable Secrets"
heading_level: 2
source_lines: [359, 371]
source_commit: 6e757843ed29aa50ce4558719452a86510ed0d20
status: finalized
word_count: 301
---

## How to Read This Guide

Not every reader needs every layer at the same depth. If you have limited time, read Chapter 1, the opening of Chapter 2, the opening of Chapter 8, the Chapter 11 landscape table, and Chapter 14 -- which catalogs seven open research questions and the system-level tradeoffs that frame each one. That sequence takes roughly forty-five minutes and leaves you able to evaluate vendor claims, explain ZK proofs to a non-technical audience, and ask the right questions about governance and quantum risk. (The Glossary at the front of the book serves as a quick-reference companion for any term introduced in later chapters.)

Engineers working toward implementation should read Chapters 1–2 in full, the core sections of Chapters 3–5, Chapter 6 through "Folding: The Snowball," Chapter 7 through "Four Families of Commitment Schemes," Chapter 8 through "Governance: The Achilles Heel," and Chapters 10, 11, and 13. That is roughly two hours of close reading and covers every layer in enough depth to make design decisions.

Researchers and auditors should read the full text and then work through the seven open questions in Chapter 14. The active research fronts are the folding genealogy (Chapter 6), the lattice revolution (Chapter 7), the CCS unification ("CCS: The Rosetta Stone," Chapter 5), and the proof core triad (Chapters 6, 10, and 11).

Regardless of path: do not skip Chapter 2 or the trust decomposition in Chapter 10. The first is where the deepest trust decisions live. The second is the book's thesis in its most complete form -- seven assumptions, fourteen causal edges, three architectural paths, each with a different failure profile. Everything between here and there is building the case.

The field is crossing three sequential frontiers -- and the three forces described in this chapter map onto them directly. *Performance* (2023–2025) is largely crossed: the cost collapse from $80 to $0.04 per proof, and the real-time block proving achieved by SP1 Hypercube and Stwo, mark a threshold. *Security* (2026–2028) is the current frontier: formal verification, 128-bit provable security, post-quantum readiness. *Privacy* (2027+) is approaching: compiler-enforced disclosure boundaries, constant-time implementations, metadata protection. Where you enter this story depends on which frontier matters most to your work.

---

## Summary

Three reading paths calibrate depth to role: Executive (~45 min), Engineer (~2 hours), Researcher (~4+ hours). All paths must include Chapter 2 and the trust decomposition in Chapter 10. The field is crossing three sequential frontiers — Performance (largely done by 2025), Security (2026–2028), Privacy (2027+) — and entry point depends on which frontier matters most.

## Key claims

- Executive Path: Chapter 1, opening of Chapter 2, opening of Chapter 8, Chapter 11 landscape table, Chapter 14 (~45 minutes).
- Engineer Path: Chapters 1–2 in full, Chapters 3–5 core sections, Chapter 6 through "Folding: The Snowball," Chapter 7 through "Four Families," Chapters 10, 11, 13 (~2 hours).
- Researcher Path: everything, plus seven open questions in Chapter 14 (~4+ hours).
- Do not skip Chapter 2 or the trust decomposition in Chapter 10 regardless of path.
- Performance frontier (2023–2025): real-time proving achieved, costs sub-cent.
- Security frontier (2026–2028): formal verification, 128-bit provable security, post-quantum readiness.
- Privacy frontier (2027+): compiler-enforced disclosure boundaries, constant-time implementations, metadata protection.

## Entities

- [[folding]]
- [[lattice]]

## Dependencies

- [[ch01-the-deepest-question]] — seven-layer trust analysis that motivates why Chapter 2 and Chapter 10 are mandatory
- [[ch01-three-converging-forces]] — the three sequential frontiers described there are the same three used to orient entry points here

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_All P0/P1/P2/P3 findings resolved in Phase 3 revisions (2026-04-18 through 2026-04-20)._

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [none] B — all claims in this section are definitional/structural with no quantitative assertions requiring citation beyond what is covered in other sections.

## Links

- Up: [[01-the-promise-of-provable-and-programmable-secrets]]
- Prev: [[ch01-the-first-decision]]
- Next: —
