---
title: "Encoding the Performance"
chapter: 5
kind: chapter-hub
status: untouched
---

# Chapter 5: Encoding the Performance

## Sections

- [[ch05-layer-4-arithmetization]]
- [[ch05-the-spreadsheet-metaphor-and-where-it-works]]
- [[ch05-the-constraint-system-evolution-r1cs-air-plonkish]]
- [[ch05-ccs-the-rosetta-stone]]
- [[ch05-the-sumcheck-protocol-the-hidden-foundation]]
- [[ch05-lookup-arguments]]
- [[ch05-the-overhead-tax-10-000x-to-50-000x]]
- [[ch05-midnight-s-zkir-a-concrete-layer-4]]
- [[ch05-where-the-layers-collapse]]
- [[ch05-where-the-analogies-break]]

## Audit rollup

**Totals: P0=0, P1=7, P2=16, P3=9**

### P1 issues (must fix before ship)

1. (A) `ch05-the-spreadsheet-metaphor` — Sudoku uniqueness-group count wrong: 12 groups × 6 pairs = 72, not 8 × 6 = 48. Total constraint count and R1CS expansion figure are incorrect.
2. (A) `ch05-the-constraint-system-evolution` — Groth16 proof size stated as "~128 bytes" in body vs. "192 bytes" in Summary; both figures appear in the same section and contradict each other.
3. (A) `ch05-the-constraint-system-evolution` — AIR constraint-count table conflates constraint *description* size with prover work; the "~30,000" entry implies 1,000× prover savings that AIR does not deliver, which is corrected only in a footnote that contradicts the table cell.
4. (A) `ch05-lookup-arguments` — 32-bit ADD example uses $c=4$ chunks (= 12 field elements) but concludes "approximately 18 field elements per instruction," which belongs to the 64-bit variant with $c=6$. The mixed 32-bit/64-bit arithmetic is not distinguished clearly.
5. (A) `ch05-the-overhead-tax` — Airbender overhead multiplier in table (8,000×) is inconsistent with its 35 s proof time against a 100 ms native baseline (should be ~350×). The baseline for the 8,000× figure is unstated.
6. (A) `ch05-the-overhead-tax` — Midnight overhead stated as 1,000,000× in body text and 4,000,000× in table/Key claims. One figure is wrong.
7. (A) `ch05-midnight-s-zkir` — BLS12-381 scalar field described as "~$2^{253}$" in one place and "255 bits" in another within the same section. The correct figure is 255 bits.

### Top 5 patterns across the chapter

1. **Numerical inconsistency between body and summary/table** — affects 4 sections (constraint-evolution, overhead-tax ×2, ZKIR). Proof sizes and overhead multipliers appear in two places and disagree.
2. **Missing citations for empirical claims** — `ch05-the-overhead-tax` cites no sources despite quoting specific benchmark figures (SP1 Hypercube 6.9 s, Stwo ~10 s, Airbender ~35 s). `ch05-where-the-layers-collapse` cites no sources for Cairo's design history.
3. **AI-smell phrases** — "key insight that makes the entire field possible" (ch05-layer-4-arithmetization); "one that Penrose would appreciate" (ch05-ccs); "internal combustion engine" analogy (ch05-sumcheck). These add no information and read as padding.
4. **Constraint-count comparisons mixing different dimensions** — AIR table entry (description size vs. trace size), Jolt 32-bit vs. 64-bit ADD example, Groth16 byte count — all require readers to track an unstated dimension to interpret correctly.
5. **Redundant restatement across sections** — the under-constrained circuits principle restated in ZKIR (already in ch03); the Sudoku uniqueness misleading point restated in ch05-where-the-analogies-break (already in ch05-layer-4-arithmetization); the R1CS-as-CCS derivation appears in full twice in ch05-ccs.
