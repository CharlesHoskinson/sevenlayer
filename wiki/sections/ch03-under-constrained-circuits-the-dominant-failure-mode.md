---
title: "Under-Constrained Circuits: The Dominant Failure Mode"
slug: ch03-under-constrained-circuits-the-dominant-failure-mode
chapter: 3
chapter_title: "Choreographing the Act"
heading_level: 2
source_lines: [1080, 1107]
source_commit: bcc3759e2dfc992ab66b2b1f5f18bbcff59f5d65
status: reviewed
word_count: 651
---

## Under-Constrained Circuits: The Dominant Failure Mode

Here is the fact that should keep every ZK developer awake at night: the most common way a zero-knowledge system fails in practice is not a cryptographic break. It is not a quantum computer. It is not a governance attack. It is a bug in the program.

The under-constrained vulnerability epidemic documented at the opening of this chapter -- 95 of 141 real-world bugs, per Chaliasos et al. (USENIX Security 2024) -- is not an abstraction. To understand why it happens at this scale, you need to understand the dual-track problem.

In Circom -- the most widely deployed ZK language by project count -- every line of code simultaneously describes two things: how to *compute* a value (witness generation), and how to *constrain* that value (the mathematical rule the proof system enforces). These two descriptions use different operators. The arrow `<--` computes a value. The triple-equals `===` constrains it. The combined operator `<==` does both.

The Tornado Cash bug was this: a developer used `=` (JavaScript assignment) where `<==` (constrained assignment) was needed. The witness generator computed the correct value. The constraint system did not enforce it. A malicious prover could substitute any value, and the proof would still verify. One character. Complete soundness break.

This is not a rare edge case. ZKAP (Wen et al., "Practical Security Analysis of Zero-Knowledge Proof Circuits," USENIX Security 2024, ePrint 2023/190) is a static analysis framework that introduced a Circuit Dependence Graph abstraction to detect vulnerabilities in Circom circuits. It found 34 previously unknown vulnerabilities across 258 circuits in 15 open-source projects. Its analysis identified three root causes:

First, *nondeterministic signals* -- circuit outputs that can take multiple values for a given input because constraints are missing. Twenty-four percent of ZKAP's findings fell in this category.

Second, *unsafe component usage* -- sub-circuits invoked without properly constraining their inputs or outputs. This created gaps where values passed between components were computed but not verified.

Third, *constraint-computation discrepancies* -- places where the witness generator and the constraint system diverged. Division is the classic example: in witness generation, division computes a quotient. In constraints, division is expressed as multiplication (if $a/b = c$, the constraint is $b \cdot c = a$). When the divisor can be zero, these two formulations behave differently. Division-by-zero was the single most common vulnerability class in ZKAP's findings, accounting for 41% of all bugs.

The defensive tooling is evolving. Picus -- also called QED^2 -- uses SMT-based techniques to automatically detect under-constrained circuits in R1CS, reducing the under-constrainedness problem to queries on systems of polynomial equations over finite fields (Pailoor et al., "Automated Detection of Under-Constrained Circuits in Zero-Knowledge Proofs," PLDI 2023, ePrint 2023/512). ZKAP's Circuit Dependence Graph abstraction -- combining data flow edges (witness computation) with constraint edges (R1CS) -- achieved an F1 score of 0.82, compared to 0.64 for the earlier Circomspect tool. zkFuzz (Takahashi et al., "zkFuzz: Foundation and Framework for Effective Fuzzing of Zero-Knowledge Circuits," IEEE S&P 2026, arXiv 2504.11961), a fuzz-testing framework for ZK circuits, found 66 bugs including 38 zero-days. MTZK (Xiao et al., "MTZK: Testing and Exploring Bugs in Zero-Knowledge (ZK) Compilers," NDSS 2025), a metamorphic testing framework aimed at the compilers themselves rather than individual circuits, discovered 21 bugs across four industrial ZK compilers -- 15 of which were patched by the maintainers.

But these tools share a limitation: they work primarily on Circom circuits (and, in MTZK's case, a handful of industrial compilers). The Rust-based systems that dominate production -- halo2 (used by Scroll and ZK Bridge projects), Plonky3 (used by SP1), and custom constraint systems in RISC Zero and Jolt -- are not covered. Stwo, despite sharing an ecosystem vocabulary with the Plonky family, builds on Circle STARKs over the Mersenne-31 field, not Plonky3. The most common ZK bug class has automated detection for the oldest ZK language but not for most of the systems where new code is being written.

NAVe, a formal verification tool for Noir programs announced in 2025, begins to close this gap. It formalizes Noir's ACIR intermediate representation and uses the cvc5 SMT solver to verify program properties. But formal verification at scale -- for circuits with millions of constraints -- remains beyond current tools. The combination of compile-time prevention (refinement types, disclosure analysis) and post-hoc verification (static analysis, formal methods) could provide comprehensive coverage, but no system achieves both today.

The evidence is clear: the most common failure mode in zero-knowledge systems is not a failure of cryptography. It is a failure of software engineering. The magician's choreography has a typo, and the proof system performs the typo faithfully.

---


## Summary

Under-constrained circuits — where the witness generator computes a value the constraint system does not enforce — account for 95 of 141 catalogued real-world ZK vulnerabilities. Static analysis tools (ZKAP, Picus, zkFuzz) exist for Circom but not for the Rust-based systems (halo2, Plonky3, Jolt) where production code is now written.

## Key claims

- 95 of 141 real-world ZK vulnerabilities (Chaliasos SoK) are under-constrained circuits.
- Tornado Cash: one `=` instead of `<==` caused a complete soundness break.
- ZKAP found 34 previously unknown vulnerabilities in 258 circuits across 15 projects; F1 score 0.82 vs 0.64 for Circomspect.
- Division-by-zero accounts for 41% of ZKAP's findings.
- zkFuzz found 66 bugs including 38 zero-days; MTZK found 21 bugs across 4 ZK compilers.
- Automated detection tools cover Circom but not halo2, Plonky3, or Jolt.
- NAVe (2025) formalizes Noir's ACIR using cvc5; full-scale formal verification for millions of constraints is not yet practical.

## Entities

- [[halo2]]
- [[jolt]]
- [[plonk]]
- [[plonky3]]
- [[tornado cash]]

## Dependencies

- [[ch03-risc-v-won-why-taxonomy-still-matters]] — introduces the 67% SNARK vulnerability statistic this section expands
- [[ch03-from-circuits-to-virtual-machines-a-brief-evolution]] — establishes Circom's dual-track architecture as root cause
- [[ch03-compact-s-disclosure-analysis]] — the compile-time prevention approach that addresses this failure mode

## Sources cited

- Chaliasos SoK: 95 of 141 catalogued vulnerabilities were under-constrained circuits.
- ZKAP: 34 previously unknown vulnerabilities in 258 circuits, 15 projects; F1 0.82.
- zkFuzz: 66 bugs, 38 zero-days.
- MTZK: 21 bugs across 4 ZK compilers.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [P2] (B) "NAVe, a formal verification tool for Noir programs announced in 2025" — no citation; no venue or author.
- [P2] (D) The claim "95 of 141 real-world bugs" in the body conflicts with "67% of all known SNARK vulnerabilities" in section 1 (ch03-risc-v-won). 95/141 = 67.4%, so the figures are arithmetically consistent, but section 1 rounds to 67% while this section uses the raw count. The two phrasings — "real-world bugs" here vs "all known SNARK vulnerabilities" in section 1 — describe the same dataset differently; ensure the scope label is consistent.
- [P2] (C) "The magician's choreography has a typo, and the proof system performs the typo faithfully" — the theatrical metaphor closing is fine, but the phrase "performs the typo" is imprecise (the system doesn't perform a typo; it enforces under-specified constraints). Minor clarity issue.
- [P3] (E) The section correctly notes that automated detection tools cover Circom but not halo2, Plonky3, or Jolt, yet it does not explain *why* — namely that R1CS analysis tools don't generalize to PLONKish or AIR constraint systems. Adding one sentence on the structural reason would strengthen the claim.

## Links

- Up: [[03-choreographing-the-act]]
- Prev: [[ch03-the-developer-s-actual-experience]]
- Next: [[ch03-compact-s-disclosure-analysis]]
