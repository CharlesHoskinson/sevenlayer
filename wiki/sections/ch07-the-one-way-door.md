---
title: "The One-Way Door"
slug: ch07-the-one-way-door
chapter: 7
chapter_title: "Layer 6 -- The Deep Craft"
heading_level: 2
source_lines: [3483, 3510]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 534
---

## The One-Way Door

Layer 6 is unlike any other layer in the stack. Layers above it can be upgraded, swapped, and optimized. A rollup can change its sequencer, rewrite its compiler, switch arithmetization formats, even adopt a new proof system -- all without changing the cryptographic foundations. But the foundations themselves are effectively permanent.

The Cascade Effect above asks *what to choose*. This section asks *when the choice becomes irreversible*. For architects making this one-way decision, the following rubric distills the tradeoffs:

| Field | Size | PQ Status | Commitment Options | Sweet Spot |
|-------|------|-----------|-------------------|------------|
| BN254 | 254-bit | Quantum-vulnerable | KZG (cheapest EVM verification) | Legacy Ethereum rollups; Groth16 wrapper |
| BLS12-381 | 253-bit | Quantum-vulnerable | KZG (higher security margin) | Privacy systems needing pairings (Midnight, Zcash) |
| BabyBear | 31-bit | Hash-PQ; lattice-PQ | FRI, Ajtai | Maximum prover speed; RISC-V zkVMs (SP1, RISC Zero) |
| Mersenne-31 | 31-bit | Hash-PQ | FRI (Circle STARK) | Fastest arithmetic; Stwo/Starknet ecosystem |
| Goldilocks | 64-bit | Hash-PQ; lattice-PQ | FRI, Ajtai | Balance of speed and precision; Neo/Nightstream |

The finite field determines the commitment scheme. The commitment scheme determines the proof system family. The hardness assumption determines the security lifespan. These choices are made once, at the beginning, and they propagate upward through every component with the inexorability of mathematical structure.

This is why the quantum threat is not a problem that can be deferred until quantum computers actually exist. A system deployed in 2026 with BN254 foundations will still be running in 2036. If a CRQC arrives in 2035, that system will have spent its final years accumulating a public record of commitments and proofs that can be retroactively broken. The HNDL threat means the privacy guarantees were never real -- they were deferred revelations, secrets written in ink that merely required a light that had not yet been invented.

The lattice revolution is a construction project, not an academic exercise. It is building new foundations that can support the same architectural weight as pairing-based cryptography -- folding, recursion, efficient composition -- without the quantum expiration date. The trilemma that seemed permanent is being dissolved not by discovering new mathematics but by engineering better constructions from mathematics that has existed for decades.

The laws of physics do not change. But our understanding of which mathematical problems are hard does change, and a quantum computer represents a discontinuous shift in that understanding. The systems that survive will be the ones whose foundations were chosen with that shift in mind.

---

The physical laws are set. The field is chosen, the commitment scheme determined, the hardness assumption staked. Everything from here upward -- the proof system, the arithmetization, the language, the setup -- inherits the possibilities and constraints of this foundation. But none of it matters until someone checks the proof. Layer 7 is where the mathematics meets its audience: on a blockchain, in a smart contract, through a governance structure that can override everything we have built. The next chapter examines the verdict -- and the uncomfortable truth that the audience's judgment is only as trustworthy as the institution that seats them.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
