---
title: "The Landscape Table (March 2026)"
slug: ch11-the-landscape-table-march-2026
chapter: 11
chapter_title: "zkVMs -- The Universal Stage"
heading_level: 2
source_lines: [4557, 4589]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 626
---

## The Landscape Table (March 2026)

The numbers tell the story concisely. Eight of ten major zkVMs now target RISC-V. Only Stwo (Cairo) and zkWASM (WebAssembly) hold out -- and even StarkWare's ecosystem hedges via Kakarot's EVM-on-Stwo path. The Ethereum Foundation declared the speed race "effectively won" in December 2025 and pivoted to 128-bit provable security by end of 2026.

(Midnight is excluded from this table because it is not a zkVM -- it is a privacy-first smart contract platform where ZK proofs are the execution model, not an optimization layer. Its full seven-layer audit appears in Chapter 12.)

| | SP1 Hypercube | RISC Zero | Jolt | Stwo | Airbender | ZisK | Pico Prism |
|---|---|---|---|---|---|---|---|
| **Org** | Succinct | RISC Zero | a16z | StarkWare | Matter Labs | SilentSig | Brevis |
| **ISA** | RISC-V (RV32IM) | RISC-V (RV32IM) | RISC-V (RV32I) | Cairo (custom) | RISC-V (RV32IM) | RISC-V 64 | RISC-V (RV32IM) |
| **Arithmetization** | Multilinear AIR + LogUp-GKR | AIR (DEEP-ALI) | R1CS + Lasso lookups | Circle AIR + LogUp | AIR (degree-2) | AIR / PIL | AIR (Plonky3) |
| **Proof system** | Multilinear STARK | FRI STARK | Spartan sumcheck | Circle STARK | DEEP STARK | STARK (recursive) | STARK (Plonky3) |
| **Field** | BabyBear (31-bit) | BabyBear (31-bit) | BN254 (256-bit) | M31 (31-bit) | M31 (31-bit) | Goldilocks (64-bit) | BabyBear / M31 |
| **SNARK wrap** | Groth16 | Groth16 | Planned | None (native) | Groth16 | Groth16 | Groth16 |
| **Eth block** | 6.9 s / 16 GPU | 44 s / cluster | N/A | N/A (Cairo) | 35 s / 1 GPU | 6.6 s / 24 GPU | 6.9 s / 16 GPU |
| **Maturity** | Production | Production | Beta | Production | Production | Adv. testnet | Production |

**Glossary.** *ISA* = instruction set architecture, the fundamental language a processor understands. *Arithmetization* = the method of translating computation into mathematical equations. *AIR* = Algebraic Intermediate Representation, encoding computation as polynomial constraints over an execution trace. *LogUp-GKR* = a sumcheck-based lookup argument. *Circle STARK* = a STARK adapted to work over the circle group of a Mersenne prime. *SNARK wrap* = compressing a large transparent proof into a small proof for cheap on-chain verification. *Field* = a set of numbers with special arithmetic properties; "31-bit" and "64-bit" refer to element size, with smaller fields enabling faster operations on modern hardware.

Three systems dropped from this table deserve brief mention. Nexus 3.0 abandoned Nova-based folding for a Stwo backend after observing a 1000x speed penalty from classical folding -- a telling result for the practical viability of folding in production zkVMs. Valida uses a custom stack-based ISA designed from scratch for ZK proving, with no independent large-scale benchmarks. zkWASM is the only remaining PLONKish/KZG outlier, targeting WebAssembly rather than RISC-V.

For architects choosing a zkVM, the landscape table above describes *what exists*. The rubric below describes *how to choose*:

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

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
