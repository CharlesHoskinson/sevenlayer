---
title: "zkVMs -- The Universal Stage"
chapter: 11
kind: chapter-hub
status: reviewed
---

# Chapter 11: zkVMs -- The Universal Stage

## Sections

- [[ch11-zkvms-across-the-stack]]
- [[ch11-the-landscape-table-march-2026]]
- [[ch11-three-zkvms-through-seven-layers]]
- [[ch11-the-proof-core-triad]]
- [[ch11-performance-the-cost-collapse]]
- [[ch11-risc-v-convergence]]
- [[ch11-the-stage-is-set]]

## Revision status

Phase 3 revision applied 2026-04-19 per `wiki/drafts/ch11-v2.md`. 1 P0 + 3 P1 resolved. Draft preserved. P2 (10) and P3 (5) deferred.

**Key corrections:** Jolt Layer 1 re-labeled **transparent** (Hyrax is no-trusted-setup, classical-security via DLP on BN254); performance section citations added (SP1 Hypercube [52], Airbender [53], ethproofs / Castle Labs [43/44], EF pivot [55]); ZisK org softened to "SilentSig (ZisK, ex-Polygon Hermez team)" with uncertain ownership details dropped (we couldn't independently verify the Baylina/GmbH claims); Stwo 100x (end-to-end pipeline) vs 125x (raw M31 field arithmetic) clarified across Layer 5 and Layer 6 entries.

## Audit rollup (pre-revision)

Audited 2026-04-18. P0=1, P1=2, P2=10, P3=5.

| Section | Findings |
|---------|----------|
| ch11-zkvms-across-the-stack | P2 B: Polygon zkEVM shutdown unsourced; P2 B: no citations for cross-layer causal claims |
| ch11-the-landscape-table-march-2026 | P1 A: ZisK org "SilentSig" likely wrong; P2 B: all benchmark/EF claims unsourced; P2 B: SP1 opcode count unsourced; P2 D: Neo/SuperNeo undefined in rubric; P3 B: Nexus 1000x claim unsourced |
| ch11-three-zkvms-through-seven-layers | P0 A: Jolt Layer 1 wrongly labelled "Trusted" (Hyrax is transparent); P1 A: 100x vs 125x speedup discrepancy for Stwo/Stone; P2 B: 60-70% witness estimate unsourced; P2 B: Gassmann et al. missing venue; P3 C: 39 vs 62 opcode counts unexplained |
| ch11-the-proof-core-triad | P2 A: multilinear PCS assigned Layer 6 twice, inconsistent with layer taxonomy; P3 B: no citations for triad clustering claim |
| ch11-performance-the-cost-collapse | P1 B: entire section's quantitative claims unsourced; P2 A: 45x multiplier inconsistent with $1.69→$0.04 (≈42x); P3 A: "2,000-fold" cross-ref to ch6 unverified |
| ch11-risc-v-convergence | P2 C: "generational outlier" vague; P2 B: Gassmann et al. missing venue; P3 C: ARM "proprietary" oversimplified |
| ch11-the-stage-is-set | P2 D: Philosophy A/B/C labels undefined inline; P2 A: proof core attributed to Ch10, first appears in Ch6; P3 D: Goldilocks in field cascade but absent from proof core triad |
