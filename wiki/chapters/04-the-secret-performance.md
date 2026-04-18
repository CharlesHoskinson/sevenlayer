---
title: "The Secret Performance"
chapter: 4
kind: chapter-hub
status: reviewed
---

# Chapter 4: The Secret Performance

## Sections

- [[ch04-the-hidden-bottleneck]]
- [[ch04-execution-traces]]
- [[ch04-witness-generation-costs]]
- [[ch04-memory-the-binding-constraint]]
- [[ch04-side-channel-attacks-when-the-walls-leak]]
- [[ch04-witness-constraint-divergence]]
- [[ch04-the-disclose-boundary-midnight-s-witness-architecture]]
- [[ch04-the-witness-as-a-multi-dimensional-problem]]

## Revision status

Phase 3 revision applied 2026-04-18 per `wiki/drafts/ch04-v2.md`. 1 P0 + 10 P1 resolved. Draft preserved. P2 (18) and P3 (6) deferred.

**Notes:** Poseidon S-box correctly characterized as a field power map ($x^5/x^7$); cache-timing vulnerability re-attributed to Reinforced Concrete's Bars table. Midnight proving-time figure softened to "20-60 seconds on desktop hardware" — no formal benchmark page exists at `docs.midnight.network`; sourced to Midnight community/forum reports.

## Audit rollup (pre-revision)

**Totals:** P0=1, P1=9, P2=18, P3=6 — 34 findings across 8 sections.

**By section:**

| Section | P0 | P1 | P2 | P3 |
|---|---|---|---|---|
| ch04-the-hidden-bottleneck | 0 | 1 | 1 | 2 |
| ch04-execution-traces | 0 | 0 | 2 | 3 |
| ch04-witness-generation-costs | 0 | 2 | 3 | 1 |
| ch04-memory-the-binding-constraint | 0 | 2 | 4 | 2 |
| ch04-side-channel-attacks-when-the-walls-leak | 1 | 2 | 2 | 1 |
| ch04-witness-constraint-divergence | 0 | 2 | 3 | 1 |
| ch04-the-disclose-boundary-midnight-s-witness-architecture | 0 | 2 | 2 | 2 |
| ch04-the-witness-as-a-multi-dimensional-problem | 0 | 0 | 3 | 2 |

**Top 5 findings:**

1. **(P0, A) Poseidon S-box / cache-timing misattribution** (ch04-side-channel-attacks): the text attributes lookup-table cache timing to Poseidon's S-box, but the Mukherjee et al. attack targets Reinforced Concrete's "Bars" function. Poseidon uses a power-map S-box, not a lookup table. This is a factual error in a security-critical section.
2. **(P1, A) Streaming space bound inconsistency** (ch04-witness-generation-costs): $O(\sqrt{T})$ in prose vs. $O(\sqrt{KT})$ in table and Key claims. These are distinct bounds; K should be defined or notation unified.
3. **(P1, A) Midnight 18-second proving figure, uncited** (ch04-the-disclose-boundary): a specific latency benchmark repeated twice with no source. Likely from a Midnight developer blog or testnet report; needs a dated reference.
4. **(P1, A) Jolt + ZKM conflated under one 128 GB figure** (ch04-memory-the-binding-constraint): two different systems attributed a single shared RAM requirement without per-system citations.
5. **(P1, A) CVE-2025-52484 severity underspecified** (ch04-witness-constraint-divergence): the register-operand confusion is described without identifying the affected instruction class, making it impossible to assess exploitability from the section alone.

**Patterns:**

- **Citation gaps dominate P1/P2.** Seven of the nine P1 findings are accuracy or citation issues where a specific number or claim lacks a verifiable source. The section is technically dense and the claims are specific enough to check.
- **Poseidon/hash-function conflation** is a recurring risk: multiple sections use "Poseidon" as shorthand for ZK-friendly hashing in general; the side-channel section crosses into inaccuracy by attributing Reinforced Concrete's behavior to Poseidon.
- **Hardware pricing as prose** creates temporal fragility: prices in ch04-memory-the-binding-constraint will age badly without explicit "as of [date]" anchors and sourcing.
- **AI-register phrases** appear in three sections ("Read that again", "The mathematics is beautiful. The engineering is brutal.", "detective story" sub-framing, "Welcome to the Witness Gap — and it is growing"). These are minor but consistent.
- **Layer numbering in closing transition** of ch04-the-witness-as-a-multi-dimensional-problem needs cross-check: the chapter consistently labels witness generation Layer 3, but the closing paragraph refers to the next subject as "Layer 4" without making clear that arithmetization is being named, not a section number.
