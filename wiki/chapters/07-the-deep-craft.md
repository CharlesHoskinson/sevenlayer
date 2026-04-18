---
title: "Layer 6 -- The Deep Craft"
chapter: 7
kind: chapter-hub
status: untouched
---

# Chapter 7: Layer 6 -- The Deep Craft

## Sections

- [[ch07-the-laws-that-break]]
- [[ch07-three-hardness-assumptions-three-worlds]]
- [[ch07-four-families-of-commitment-schemes]]
- [[ch07-the-trilemma-and-its-dissolution]]
- [[ch07-small-fields]]
- [[ch07-the-quantum-threat-horizon]]
- [[ch07-lattice-based-proving]]
- [[ch07-case-study-midnight]]
- [[ch07-the-cascade-effect]]
- [[ch07-algebraic-vs-traditional-hash-functions]]
- [[ch07-the-structural-advantage-of-lattices]]
- [[ch07-maturity-and-readiness]]
- [[ch07-the-one-way-door]]

## Audit rollup

**Totals:** P0=3, P1=4, P2=21, P3=9

**P0 issues (fix before ship)**

1. `ch07-small-fields` — BLS12-381 described as "~253-bit prime"; scalar field r is 255 bits. Error repeats in `ch07-case-study-midnight` and `ch07-the-one-way-door`.
2. `ch07-case-study-midnight` — Same BLS12-381 bit-length error as above (the shared root of all three P0 flags is one wrong number propagated through three sections).
3. `ch07-the-one-way-door` — Field rubric table repeats the "253-bit" error.

**P1 issues (major)**

1. `ch07-three-hardness-assumptions-three-worlds` — BHT citation incomplete (no venue/year); "85-bit" quantum collision bound is non-standard and partially negated by the QRAM caveat — needs clarification or removal.
2. `ch07-the-trilemma-and-its-dissolution` — "The original paper presented a 'cryptographic primitives trilemma'" cites no paper; either cite the source or reframe as original synthesis.
3. `ch07-algebraic-vs-traditional-hash-functions` — Incorrectly attributes lookup-table S-boxes as an inherent property of Poseidon; Poseidon uses power-map S-boxes. Side-channel risk is implementation-specific, not algorithmic.
4. `ch07-the-structural-advantage-of-lattices` — Curve-cycle recursion attributed to Zexe; canonical example is Halo (Bowe, Grigg, Hopwood 2019) / Mina Protocol. Zexe does not require curve cycles.

**Top 5 patterns across ch07**

1. **BLS12-381 bit-length error** — "~253-bit" appears in three sections; scalar field r is 255 bits. Single-source fix needed.
2. **Missing citations for key quantitative claims** — FRI/IPA/KZG proof-size figures, BHT 85-bit bound, Poseidon parameter revisions, and curve-cycle overhead claims all lack primary sources.
3. **"Original paper" attribution gaps** — The trilemma framing, FRI domain folklore, and several performance benchmarks reference unnamed works; these should be sourced or flagged as author synthesis.
4. **Algorithm vs. implementation conflation** — The Poseidon/lookup-table side-channel claim conflates algorithmic design with a specific implementation optimization; a similar risk exists in the FRI section's security discussion.
5. **LatticeFold date ambiguity** — "2024" ePrint vs "ASIACRYPT 2025" conference venue is inconsistently handled across `ch07-lattice-based-proving` and `ch07-maturity-and-readiness`.
