---
title: "The Capex/Opex Framework"
slug: ch02-the-capex-opex-framework
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [542, 561]
source_commit: 11fdb9b24e8a6276b781005a7fe5f0c10a377012
status: reviewed
word_count: 511
---

## The Capex/Opex Framework

The most useful lens for understanding setup economics is the capital expenditure / operating expenditure distinction.

**Ceremony costs are capex.** The Ethereum KZG Summoning, run by the Ethereum Foundation over 208 days, cost an order of magnitude of a few million dollars in coordination, engineering, grants, and security auditing -- a figure consistent with the public grant round and the scale of the coordinating infrastructure [Ethereum Foundation, "KZG Ceremony Grant Round," December 2022; Ethereum Foundation, "Wrapping up the KZG Ceremony," January 2024]. Whatever the precise number, ceremonies like this are one-time events. Because the resulting SRS is universal, every system that builds on it amortizes the cost. L2Beat's registry lists dozens of live rollups as of early 2026, many of which verify Groth16 or KZG-based proofs against the same family of SRSes. Per-rollup, the amortized share of the ceremony cost is trivial relative to any serious project's annual budget.

**Per-proof costs are opex.** Once the stage is built, the cost that matters is the cost of each proof. Here the gap between trusted and transparent setups opens wide:

- **Groth16 on-chain verification**: approximately 200,000-300,000 gas, which at typical Ethereum gas prices translates to about $0.50-$1.00. This is the cheapest on-chain verification available. Groth16 proofs are exactly 192 bytes -- three elliptic curve group elements. Smaller than a tweet.
- **Raw STARK on-chain verification**: approximately 2-5 million gas, translating to $5-$25. STARK proofs run roughly 100 KB -- about 500 times larger than Groth16 proofs.

To see what this means in practice, consider a rollup operator posting 1,000 proofs per day to Ethereum. With Groth16, each verification costs roughly 200,000 gas -- about $0.75 at typical prices. That is $750 per day, roughly $274,000 per year. With raw STARKs posted directly on-chain, each verification costs roughly 3 million gas -- about $11. That is $11,000 per day, roughly $4 million per year. Against a ceremony cost in the low millions, the payback period for even a single operator is well under two years. After that, it is pure savings.

These numbers explain why trusted setups persist despite their trust assumptions. The argument is not philosophical. It is economic. And it explains why the dominant production pattern in 2026 is neither pure trusted nor pure transparent, but *hybrid*: use a transparent STARK as the inner proof (no ceremony required, post-quantum security for the computation), then wrap it in a Groth16 or KZG-based outer proof for cheap on-chain verification. You get the transparency of STARKs and the economics of SNARKs.

Every major production system follows this pattern. SP1 Hypercube generates STARK proofs over a small, fast field (BabyBear, 31 bits per number), recursively compresses them, and wraps the result in Groth16 for Ethereum verification. Stwo does the same over the Mersenne-31 field. RISC Zero, Airbender, ZisK -- all follow the same architecture. Even StarkWare, the company that built its identity on transparent proving, wraps to Groth16 for Ethereum settlement because the gas economics demand it.

The cost of this hybrid approach is complexity: you maintain two proof systems, two fields, and a "field-crossing" circuit that bridges the small inner field to the large outer field. The outer wrapper still requires a trusted setup (the KZG ceremony). But the inner proof -- where the actual computation is verified -- is fully transparent. If a post-quantum on-chain verifier ever becomes practical, the outer Groth16 layer can be dropped, and the entire pipeline becomes transparent end-to-end.



## Summary

Ceremony costs are one-time capital expenditure (~$2–5M for the Ethereum KZG setup); amortized across 50+ rollups, the per-rollup cost is ~$60K. Per-proof verification costs are the recurring operating expense: Groth16 runs ~200K–300K gas ($0.50–$1.00 on Ethereum) vs. raw STARK ~2–5M gas ($5–$25), making the ceremony's payback period under 18 months for a rollup posting 1,000 proofs/day. Every major 2026 production system uses a hybrid: transparent STARK inner proof wrapped in Groth16 for on-chain economics.

## Key claims

- Ethereum KZG ceremony coordination cost: approximately $2–5 million one-time.
- With 50+ rollups sharing the SRS, per-rollup amortized ceremony cost: ~$60,000.
- Groth16 on-chain verification: ~200,000–300,000 gas, ~$0.50–$1.00 per proof; 192 bytes.
- Raw STARK on-chain verification: ~2–5 million gas, ~$5–$25 per proof; ~100 KB.
- At 1,000 proofs/day, Groth16 costs ~$274K/year vs. STARKs ~$4M/year; ceremony payback under 18 months.
- Hybrid architecture (STARK inner + Groth16 outer): used by SP1 Hypercube, Stwo, RISC Zero, Airbender, ZisK.
- SP1 Hypercube and Stwo use BabyBear (31-bit) and Mersenne-31 fields respectively for the inner STARK.

## Entities

- [[airbender]]
- [[babybear]]
- [[ceremony]]
- [[groth16]]
- [[mersenne]]
- [[starks]]
- [[zisk]]

## Dependencies

- [[ch02-two-ways-to-build-a-stage]] — establishes the trusted vs. transparent spectrum
- [[ch02-the-structured-reference-string]] — defines the SRS whose cost is being amortized

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [P2] (A) The STARK verification gas estimate (~2–5M gas) and Groth16 estimate (~200K–300K gas) are Ethereum mainnet figures; gas costs fluctuate significantly and the text should note the date or price assumption (the section mentions "typical Ethereum gas prices" without anchoring).
- [none] (B) No citation issues beyond those noted in A.
- [P2] (C) "Smaller than a tweet" (192 bytes) is a recurring motif across multiple sections; it is used more naturally here than elsewhere, but the phrase's repetition across the wiki creates slight staleness.
- [none] (D) No structural contradictions found.
- [P3] (E) The section names SP1 Hypercube and Stwo but does not note that the SP1 Hypercube benchmark (6.9 s) and Stwo benchmark (~10 s) referenced in ch05 are already available; a cross-reference to the overhead-tax section would let readers see actual numbers.

## Links

- Up: [[02-building-the-stage]]
- Prev: [[ch02-two-ways-to-build-a-stage]]
- Next: [[ch02-the-141-416-person-question]]
