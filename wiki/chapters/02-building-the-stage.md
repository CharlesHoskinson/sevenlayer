---
title: "Layer 1 -- Building the Stage"
chapter: 2
kind: chapter-hub
status: untouched
---

# Chapter 2: Layer 1 -- Building the Stage

## Sections

- [[ch02-the-fair-shuffle-problem]]
- [[ch02-the-structured-reference-string]]
- [[ch02-two-ways-to-build-a-stage]]
- [[ch02-the-capex-opex-framework]]
- [[ch02-the-141-416-person-question]]
- [[ch02-the-bug-that-was-not-a-ceremony-failure]]
- [[ch02-universal-versus-circuit-specific-setups]]
- [[ch02-the-quantum-shelf-life]]
- [[ch02-bn254-s-eroding-security-margin]]
- [[ch02-the-adopt-framework]]
- [[ch02-midnight-s-bls12-381-stage]]
- [[ch02-option-value-analysis]]
- [[ch02-the-setup-tradeoff]]

## Audit rollup

### Severity totals

| Severity | Count |
|---|---|
| P0 | 1 |
| P1 | 13 |
| P2 | 19 |
| P3 | 9 |

### Top 5 findings

1. **[P0] ch02-the-bug-that-was-not-a-ceremony-failure (A)** — CVE-2019-7167 discoverers listed as Bowe and Gabizon; Daira Hopwood is omitted from the official disclosure. Fix before ship.

2. **[P1] ch02-the-structured-reference-string (A)** — The 192-byte proof size is attributed to the KZG/SRS verification scheme, but KZG opening proofs are 48 bytes; 192 bytes is specific to Groth16 (2 G1 + 1 G2). The text blurs two distinct constructs, creating a likely misconception for readers.

3. **[P1] ch02-two-ways-to-build-a-stage (A)** — Bulletproofs proof size given as "~700 bytes" in the setup spectrum table; ch07-four-families-of-commitment-schemes gives IPA/Bulletproofs as O(log n), ~1–5 KB — a direct cross-chapter numerical contradiction. The 700-byte figure holds only for tiny circuits.

4. **[P1] ch02-the-quantum-shelf-life (A)** — The section conflates NIST IR 8547's 2035 *deprecation deadline* with a *CRQC arrival estimate*; NIST does not predict when CRQCs will arrive. This overstates NIST's position and is repeated across the chapter (also affects ch02-option-value-analysis).

5. **[P1] ch02-the-setup-tradeoff (D)** — The 67% under-constrained-circuits statistic is used as a concluding data point without a citation; other chapters (ch01, ch03) source it to Chaliasos et al., USENIX Security 2024. Inconsistent citation practice across the book.

### Cross-section patterns

- **Citation gaps throughout.** Most sections rely on approximate or incomplete citations (no venue, no DOI, no ePrint number). The Wang, Cohney, Bonneau 2025 SoK; Kim & Barbulescu 2016; Menezes, Sarkar, Singh 2016; BGM17; and the Midnight April 2025 announcement all lack traceable references. This is a Phase 3 sweep.

- **Midnight Pluto-Eris → BLS12-381 switch.** The April 2025 date appears in three sections (ch02-the-quantum-shelf-life, ch02-midnight-s-bls12-381-stage, ch02-the-setup-tradeoff) without a source. A single canonical footnote in ch02-midnight-s-bls12-381-stage should cover all three.

- **NIST 2035 conflation.** The deprecation-deadline-as-CRQC-arrival-estimate error propagates through ch02-the-quantum-shelf-life and ch02-option-value-analysis. A single corrected formulation ("NIST targets 2035 for deprecation, independent of when CRQCs actually arrive") should be templated and applied to both.

- **KZG vs. Groth16 proof size.** The 192-byte figure is used correctly in most places but ch02-the-structured-reference-string conflates it with the KZG scheme's own proof size (48 bytes per ch07). Ch05-where-the-analogies-break separately claims "128-byte proofs" for Groth16 — an error in a different chapter that may propagate back to ch02 readers via cross-references.

- **Unsourced economic figures.** The $2–5M ceremony cost, $60K per-rollup amortization, and $50M migration cost are all presented as precise estimates with no methodology. These appear in ch02-the-capex-opex-framework and ch02-option-value-analysis; they need either a cited source or explicit labeling as illustrative estimates.
