---
title: "The Landscape Table (March 2026)"
slug: ch11-the-landscape-table-march-2026
chapter: 11
chapter_title: "zkVMs -- The Universal Stage"
heading_level: 2
source_lines: [4576, 4610]
source_commit: 9cb1d67a71f09c510cc06fa9493948e145a8f31a
status: reviewed
word_count: 626
---

## The Landscape Table (March 2026)

The numbers tell the story concisely. Eight of ten major zkVMs now target RISC-V. Only Stwo (Cairo) and zkWASM (WebAssembly) hold out -- and even StarkWare's ecosystem hedges via Kakarot's EVM-on-Stwo path. The Ethereum Foundation declared the speed race "effectively won" in December 2025 and pivoted to 128-bit provable security by end of 2026 [55].

(Midnight is excluded from this table because it is not a zkVM -- it is a privacy-first smart contract platform where ZK proofs are the execution model, not an optimization layer. Its full seven-layer audit appears in Chapter 12.)

| | SP1 Hypercube | RISC Zero | Jolt | Stwo | Airbender | ZisK | Pico Prism |
|---|---|---|---|---|---|---|---|
| **Org** | Succinct | RISC Zero | a16z | StarkWare | Matter Labs | SilentSig (ZisK, ex-Polygon Hermez team) | Brevis |
| **ISA** | RISC-V (RV32IM) | RISC-V (RV32IM) | RISC-V (RV32I) | Cairo (custom) | RISC-V (RV32IM) | RISC-V 64 | RISC-V (RV32IM) |
| **Arithmetization** | Multilinear AIR + LogUp-GKR | AIR (DEEP-ALI) | R1CS + Lasso lookups | Circle AIR + LogUp | AIR (degree-2) | AIR / PIL | AIR (Plonky3) |
| **Proof system** | Multilinear STARK | FRI STARK | Spartan sumcheck | Circle STARK | DEEP STARK | STARK (recursive) | STARK (Plonky3) |
| **Field** | BabyBear (31-bit) | BabyBear (31-bit) | BN254 (256-bit) | M31 (31-bit) | M31 (31-bit) | Goldilocks (64-bit) | BabyBear / M31 |
| **SNARK wrap** | Groth16 | Groth16 | Planned | None (native) | Groth16 | Groth16 | Groth16 |
| **Eth block** | 6.9 s / 16 GPU | 44 s / cluster | N/A | N/A (Cairo) | 35 s / 1 GPU | 6.6 s / 24 GPU | 6.9 s / 16 GPU |
| **Maturity** | Production | Production | Beta | Production | Production | Adv. testnet | Production |

**Glossary.** *ISA* = instruction set architecture, the fundamental language a processor understands. *Arithmetization* = the method of translating computation into mathematical equations. *AIR* = Algebraic Intermediate Representation, encoding computation as polynomial constraints over an execution trace. *LogUp-GKR* = a sumcheck-based lookup argument. *Circle STARK* = a STARK adapted to the circle group of a Mersenne prime. *SNARK wrap* = compressing a large transparent proof into a small proof for cheap on-chain verification. *Field* = a set of numbers with special arithmetic properties; "31-bit" and "64-bit" refer to element size, with smaller fields enabling faster operations on modern hardware.

ZisK's ownership deserves a footnote: the project spun out of Polygon's Hermez team after the zkEVM shutdown (Chapter 3); the table names the sponsoring organization, while the project brand is ZisK.

Three systems dropped from the table deserve brief mention. Nexus 3.0 abandoned Nova-based folding for a Stwo backend after a roughly 1000x speed penalty from classical folding -- a telling result for the practical viability of folding in production zkVMs. Valida uses a custom stack-based ISA designed from scratch for ZK proving, with no independent large-scale benchmarks. zkWASM is the only remaining PLONKish/KZG outlier, targeting WebAssembly rather than RISC-V.

For architects choosing a zkVM, the landscape table describes *what exists*. The rubric below describes *how to choose*:

| Goal | Recommended | Rationale |
|------|-------------|-----------|
| General-purpose execution | SP1 Hypercube, RISC Zero | RISC-V, mature tooling, broadest Rust ecosystem support |
| Maximum throughput | SP1 Hypercube, Airbender | Best Ethereum block proving benchmarks (6.9s, 21.8M cycles/sec) |
| ZK-native efficiency | Stwo (Cairo) | Purpose-built ISA eliminates translation overhead; Starknet-native |
| Post-quantum trajectory | Neo/SuperNeo (watch) | Lattice-based, CCS-native, 127-bit PQ security; 3-5 year horizon |
| Lookup-heavy design | Jolt | Lasso decomposable lookups; sumcheck-native; avoids NTT bottleneck |
| Minimum trusted setup | Stwo, Pico Prism | Fully transparent (hash-based FRI); no ceremony required |
| Formal verification | SP1 | 62 RISC-V opcodes verified against Sail spec; strongest correctness guarantees |


## Summary

As of March 2026, eight of ten major zkVMs target RISC-V; Cairo (Stwo) and WebAssembly (zkWASM) are the holdouts. The Ethereum Foundation declared the speed race won in December 2025 and pivoted to 128-bit provable security. A selection rubric maps system goals to recommended platforms.

## Key claims

- 8 of 10 major zkVMs target RISC-V as of March 2026.
- EF declared speed race "effectively won" December 2025; new target: 128-bit provable security by end of 2026.
- SP1 Hypercube and ZisK achieve Ethereum block proving at 6.9 s and 6.6 s respectively on 16–24 RTX 5090 GPUs.
- Airbender proves an Ethereum block in 35 s on a single H100 GPU.
- Nexus 3.0 abandoned Nova folding after observing a 1000x speed penalty vs. Stwo backend.
- Midnight is excluded from this table (it is not a zkVM; Chapter 12 audits it).
- SP1 has 62 RISC-V opcodes formally verified against the Sail specification.

## Entities

- [[airbender]]
- [[arithmetization]]
- [[babybear]]
- [[bn254]]
- [[ceremony]]
- [[circle stark]]
- [[fri]]
- [[goldilocks]]
- [[groth16]]
- [[jolt]]
- [[kzg]]
- [[lasso]]
- [[lattice]]
- [[logup]]
- [[mersenne]]
- [[midnight]]
- [[nova]]
- [[ntt]]
- [[plonky3]]
- [[plonk]]
- [[spartan]]
- [[starknet]]
- [[zisk]]

## Dependencies

- [[ch11-three-zkvms-through-seven-layers]] — deep-dives SP1, Stwo, and Jolt rows of this table
- [[ch11-the-proof-core-triad]] — explains why field/commitment/arithmetization columns cluster
- [[ch11-performance-the-cost-collapse]] — performance numbers behind Eth-block column
- [[ch11-risc-v-convergence]] — explains the 8-of-10 RISC-V result
- [[ch10-the-three-path-table]] — prior chapter's path taxonomy maps onto this table

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P2] (B) No sources cited for any benchmark numbers (Eth block times, GPU configs) or the EF "speed race won" declaration (December 2025). These are high-value claims that need traceability.
- [P2] (B) "SP1 has 62 RISC-V opcodes formally verified against the Sail specification" — no source; this specific count needs a citation to the SP1 formal verification work.
- [P2] (D) "Neo/SuperNeo (watch)" appears in the selection rubric without introduction — these systems are not in the landscape table above and are not defined anywhere in this section. Reader has no context for the recommendation.
- [P3] (B) "Nexus 3.0 abandoned Nova-based folding... 1000x speed penalty" — no citation; this is a strong empirical claim about a competitor's technical decision.

## Links

- Up: [[11-zkvms-the-universal-stage]]
- Prev: [[ch11-zkvms-across-the-stack]]
- Next: [[ch11-three-zkvms-through-seven-layers]]
