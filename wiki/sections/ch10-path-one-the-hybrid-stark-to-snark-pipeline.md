---
title: "Path One: The Hybrid STARK-to-SNARK Pipeline"
slug: ch10-path-one-the-hybrid-stark-to-snark-pipeline
chapter: 10
chapter_title: "The Synthesis -- Three Paths, Not Two"
heading_level: 2
source_lines: [4377, 4392]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 485
---

## Path One: The Hybrid STARK-to-SNARK Pipeline

The dominant production pattern in 2026 is not SNARK. It is not STARK. It is STARK *wrapped in* SNARK.

Here is how the trick works. A prover generates a STARK proof -- transparent, no trusted setup, post-quantum by construction, but large (50-200 KB) and expensive to verify on-chain (1-5 million gas on Ethereum). This STARK proof is then compressed through recursive aggregation and finally wrapped in a Groth16 SNARK proof -- tiny (192 bytes), cheap to verify on-chain (~250-300K gas), but requiring a trusted setup ceremony (the Powers-of-Tau).

Think of it as a two-act show. In the first act, the magician performs behind a glass wall -- everything is transparent, no trapdoors, no hidden compartments. In the second act, the performance is photographed, and the photograph is sealed in a tamper-proof envelope small enough to slip under a door. The audience in the theater (the blockchain) only sees the envelope. But anyone who opens it can verify that it faithfully captures the transparent performance.

Every major production system does this or plans to. SP1 Hypercube generates multilinear STARK proofs over the BabyBear field, recursively compresses them, then wraps the result in Groth16 over BN254 for Ethereum verification. Stwo generates Circle STARK proofs over the Mersenne-31 field, aggregates them via SHARP, then wraps to Groth16 via Herodotus for Ethereum settlement. RISC Zero, Airbender, ZisK, Pico Prism -- all follow the same pattern. Even StarkWare, the company that built its identity on transparent proving, wraps to Groth16 for Ethereum L1 because the gas economics demand it.

The wrapping pipeline is not a Layer 5 phenomenon. It pierces three layers simultaneously: Layer 5 (the proof system switches from STARK to SNARK), Layer 6 (the field transitions from BabyBear or M31 to BN254), and Layer 7 (the verification target shifts from prover-internal consistency to EVM smart contract). This vertical shaft through the stack is invisible in the original framing, which treats STARKs and SNARKs as competing alternatives occupying the same layer.

Why did this happen? Economics. Pure and simple. A raw STARK verification costs 1-5 million gas on Ethereum -- roughly $5-$25 at typical gas prices. A Groth16 verification costs ~250K gas -- roughly $0.50-$1.00. When you amortize this across thousands of transactions per batch, the difference is enormous. The inner STARK gives you transparency and post-quantum readiness. The outer SNARK gives you on-chain affordability. The combination gives you both.

The hybrid path has a structural weakness that deserves a name: the outer Groth16 wrapper is not post-quantum. Even though the inner STARK is quantum-resistant, the final on-chain verification depends on BN254 pairings, which Shor's algorithm breaks in polynomial time. The chain of trust is only as strong as its weakest link. Today's hybrid systems are transparent and fast on the inside, but they inherit quantum vulnerability from their verification wrapper. The glass wall is strong. The envelope has an expiration date.


## Summary

The dominant production pattern in 2026 is STARK wrapped in Groth16: a transparent, large inner proof compressed into a 192-byte outer proof for cheap on-chain verification. Every major production zkVM — SP1, Stwo, RISC Zero, Airbender, ZisK, Pico Prism — follows this pattern because Ethereum gas economics make raw STARK verification ($5–$25) unaffordable versus Groth16 (~$0.50–$1.00). The structural weakness is that the outer Groth16 wrapper is not post-quantum, making the entire chain quantum-vulnerable despite a quantum-resistant inner STARK.

## Key claims

- Raw STARK proofs are 50–200 KB and cost 1–5 million gas (~$5–$25) to verify on Ethereum.
- Groth16 proofs are 192 bytes and cost ~250–300K gas (~$0.50–$1.00) to verify on Ethereum.
- SP1 Hypercube: multilinear STARK over BabyBear → recursive compression → Groth16 over BN254.
- Stwo: Circle STARK over Mersenne-31 → SHARP aggregation → Groth16 via Herodotus for Ethereum.
- RISC Zero, Airbender, ZisK, and Pico Prism all follow the same hybrid pipeline.
- Even StarkWare wraps to Groth16 for Ethereum L1 settlement.
- The wrapping pipeline simultaneously touches Layer 5 (proof system switch), Layer 6 (field transition BabyBear/M31 → BN254), and Layer 7 (verification target shifts to EVM).
- The outer Groth16 wrapper is not post-quantum; BN254 pairings are broken by Shor's algorithm.

## Entities

- [[airbender]]
- [[babybear]]
- [[bn254]]
- [[ceremony]]
- [[circle stark]]
- [[groth16]]
- [[mersenne]]
- [[pico]]
- [[prism]]
- [[starks]]
- [[zisk]]

## Dependencies

- [[ch02-two-ways-to-build-a-stage]] — foundational SNARK vs STARK tradeoffs
- [[ch06-the-hybrid-pipeline]] — earlier detailed treatment of the STARK-to-SNARK pipeline
- [[ch07-the-quantum-threat-horizon]] — BN254 quantum vulnerability context
- [[ch08-the-price-of-a-verdict]] — Ethereum gas economics driving the pattern

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

## Links

- Up: [[10-the-synthesis-three-paths-not-two]]
- Prev: [[ch10-the-map-redrawn]]
- Next: [[ch10-path-two-pure-transparent]]
