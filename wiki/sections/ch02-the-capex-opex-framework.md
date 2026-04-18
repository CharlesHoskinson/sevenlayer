---
title: "The Capex/Opex Framework"
slug: ch02-the-capex-opex-framework
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [536, 555]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 511
---

## The Capex/Opex Framework

The most useful lens for understanding setup economics is the capital expenditure / operating expenditure distinction.

**Ceremony costs are capex.** The Ethereum KZG ceremony required approximately $2-5 million in coordination, engineering, and security auditing. This is a one-time cost. Because the resulting SRS is universal, every system that uses it amortizes that cost. With fifty or more rollups sharing the same SRS, the per-rollup cost converges to approximately $60,000 -- trivial relative to the annual operating budget of any serious blockchain project.

**Per-proof costs are opex.** Once the stage is built, the cost that matters is the cost of each proof. Here the gap between trusted and transparent setups opens wide:

- **Groth16 on-chain verification**: approximately 200,000-300,000 gas, which at typical Ethereum gas prices translates to about $0.50-$1.00. This is the cheapest on-chain verification available. Groth16 proofs are exactly 192 bytes -- three elliptic curve group elements. Smaller than a tweet.
- **Raw STARK on-chain verification**: approximately 2-5 million gas, translating to $5-$25. STARK proofs run roughly 100 KB -- about 500 times larger than Groth16 proofs.

To see what this means in practice, consider a rollup operator posting 1,000 proofs per day to Ethereum. With Groth16, each verification costs roughly 200,000 gas -- about $0.75 at typical prices. That is $750 per day, roughly $274,000 per year. With raw STARKs posted directly on-chain, each verification costs roughly 3 million gas -- about $11. That is $11,000 per day, roughly $4 million per year. The ceremony costs $2-5 million. But the annual savings from using Groth16 over raw STARKs are $3.7 million. The payback period is under 18 months. After that, it is pure savings.

These numbers explain why trusted setups persist despite their trust assumptions. The argument is not philosophical. It is economic. And it explains why the dominant production pattern in 2026 is neither pure trusted nor pure transparent, but *hybrid*: use a transparent STARK as the inner proof (no ceremony required, post-quantum security for the computation), then wrap it in a Groth16 or KZG-based outer proof for cheap on-chain verification. You get the transparency of STARKs and the economics of SNARKs.

Every major production system follows this pattern. SP1 Hypercube generates STARK proofs over a small, fast field (BabyBear, 31 bits per number), recursively compresses them, and wraps the result in Groth16 for Ethereum verification. Stwo does the same over the Mersenne-31 field. RISC Zero, Airbender, ZisK -- all follow the same architecture. Even StarkWare, the company that built its identity on transparent proving, wraps to Groth16 for Ethereum settlement because the gas economics demand it.

The cost of this hybrid approach is complexity: you maintain two proof systems, two fields, and a "field-crossing" circuit that bridges the small inner field to the large outer field. The outer wrapper still requires a trusted setup (the KZG ceremony). But the inner proof -- where the actual computation is verified -- is fully transparent. If a post-quantum on-chain verifier ever becomes practical, the outer Groth16 layer can be dropped, and the entire pipeline becomes transparent end-to-end.



## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
