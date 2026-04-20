---
title: "The Synthesis -- Three Paths, Not Two"
chapter: 10
kind: chapter-hub
status: reviewed
---

# Chapter 10: The Synthesis -- Three Paths, Not Two

## Sections

- [[ch10-the-binary-that-broke]]
- [[ch10-the-map-redrawn]]
- [[ch10-path-one-the-hybrid-stark-to-snark-pipeline]]
- [[ch10-path-two-pure-transparent]]
- [[ch10-path-three-post-quantum-folding]]
- [[ch10-the-three-path-table]]
- [[ch10-the-causal-web-why-it-is-a-dag-not-a-stack]]
- [[ch10-trust-decomposition-seven-weaker-assumptions]]
- [[ch10-trustless-versus-trust-minimized]]

## Revision status

Phase 3 revision applied 2026-04-19 per `wiki/drafts/ch10-v2.md`. 1 P0 + 5 P1 resolved (plus Layer 4/5 enumeration expansion in the closing section). Draft preserved. P2 (4) and P3 (2) deferred.

**Key corrections:** Frozen Heart count corrected to six implementations across three proof systems (Dusk/Iden3/gnark/ING/SECBIT/Adjoint — consistent with ch08); "via Herodotus" removed (Herodotus is storage-proofs, not a wrapping pipeline); Module-SIS validation tied specifically to FIPS 204 (not 203); EF December 2025 pivot cited to Kadianakis; Brevis Pico Prism sourced inline; DAG "two hops" claim softened; Tornado Cash Layer 2 example replaced with Zcash InternalH (CVE-2019-7167); closing trust-assumption enumeration expanded from 5 to all 7 layers.

## Audit rollup (pre-revision)

| Section | Findings |
|---------|----------|
| ch10-the-binary-that-broke | No issues. |
| ch10-the-map-redrawn | [P2] C — DAG diagram visually undercounts its 14-edge claim. |
| ch10-path-one-the-hybrid-stark-to-snark-pipeline | [P1] B — no sources for system-specific claims; Herodotus attribution suspect. [P2] A — Pico/Prism entity split. |
| ch10-path-two-pure-transparent | [P1] B — EF pivot date, SP1 proximity-gap claim, Brevis hardware spec all uncited. |
| ch10-path-three-post-quantum-folding | [P1] A/B — FIPS 203/204 attribution for Module-SIS imprecise (204 is the right standard). [P2] B — Greyhound missing from bibliography; "SuperNeo" undocumented. |
| ch10-the-three-path-table | [P3] C — "alternative verification" in Pure Transparent row unexplained. |
| ch10-the-causal-web-why-it-is-a-dag-not-a-stack | [P1] A — "every layer within two hops" claim appears false (Layer 1→Layer 3 is 3 hops). [P3] B — Penrose reference lacks page number. |
| ch10-trust-decomposition-seven-weaker-assumptions | [P0] D — Frozen Heart count is wrong (says 3, canonical source says 6) and named implementations don't match ch08. [P1] A — Tornado Cash Layer 2 example conflates circuit bug with governance exploit. [P2] E — Layer 2/4 isolation from Layer 6 failure needs one more sentence of reasoning. |
| ch10-trustless-versus-trust-minimized | [P1] A — body paragraph lists 5 trust assumptions but section claims 7; Layers 4 and 5 missing from inline enumeration. |

**P0: 1 — P1: 5 — P2: 4 — P3: 2**
