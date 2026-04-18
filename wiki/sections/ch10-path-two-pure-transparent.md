---
title: "Path Two: Pure Transparent"
slug: ch10-path-two-pure-transparent
chapter: 10
chapter_title: "The Synthesis -- Three Paths, Not Two"
heading_level: 2
source_lines: [4393, 4404]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 316
---

## Path Two: Pure Transparent

The Ethereum Foundation has staked a different position. For the L1 zkEVM -- the project to prove every Ethereum block in zero knowledge -- the mandate is explicit: no trusted setup, period. This is not a preference; it is a requirement. The reasoning is straightforward: Ethereum's base layer cannot depend on a trusted ceremony that quantum computers will eventually break. The stage must be made of glass, all the way down.

This mandate forces a different engineering path. Pure transparent systems use only hash-based commitments (FRI, Merkle trees) and avoid all pairing-based cryptography. The cost is larger proofs and more expensive on-chain verification. The benefit is that no ceremony is ever needed, no toxic waste exists, and the security assumptions survive quantum computing (assuming hash functions with sufficient output size).

The EF's December 2025 pivot is instructive. Having declared the speed race "effectively won" -- four teams proved >99% of Ethereum blocks within the 12-second slot time -- the Foundation shifted its 2026 targets to security: 100-bit provable security by May 2026, 128-bit by December 2026. The new primary metric is energy consumption per proof (kWh), not raw speed. The Foundation explicitly rejects reliance on unproven mathematical conjectures (proximity gap assumptions) for production soundness.

This matters because it validates a specific engineering philosophy: formal provable security over empirical performance. SP1 Hypercube already eliminates proximity gap conjectures in its multilinear STARK. The EF's security-first stance means that systems with strong formal guarantees will be preferred for the most security-critical application in the ecosystem -- proving the base layer itself.

Brevis's Pico Prism occupies an interesting position on this path. Built on Plonky3 with hash-based FRI commitments, it achieves 99%+ real-time proving on 16 RTX 5090 GPUs while remaining fully transparent. For non-Ethereum-L1 applications that still need on-chain verification, it wraps to Groth16 -- but the inner pipeline is transparent end to end.


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
