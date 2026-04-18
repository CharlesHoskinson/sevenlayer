---
title: "Path Two: Pure Transparent"
slug: ch10-path-two-pure-transparent
chapter: 10
chapter_title: "The Synthesis -- Three Paths, Not Two"
heading_level: 2
source_lines: [4393, 4404]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 316
---

## Path Two: Pure Transparent

The Ethereum Foundation has staked a different position. For the L1 zkEVM -- the project to prove every Ethereum block in zero knowledge -- the mandate is explicit: no trusted setup, period. This is not a preference; it is a requirement. The reasoning is straightforward: Ethereum's base layer cannot depend on a trusted ceremony that quantum computers will eventually break. The stage must be made of glass, all the way down.

This mandate forces a different engineering path. Pure transparent systems use only hash-based commitments (FRI, Merkle trees) and avoid all pairing-based cryptography. The cost is larger proofs and more expensive on-chain verification. The benefit is that no ceremony is ever needed, no toxic waste exists, and the security assumptions survive quantum computing (assuming hash functions with sufficient output size).

The EF's December 2025 pivot is instructive. Having declared the speed race "effectively won" -- four teams proved >99% of Ethereum blocks within the 12-second slot time -- the Foundation shifted its 2026 targets to security: 100-bit provable security by May 2026, 128-bit by December 2026. The new primary metric is energy consumption per proof (kWh), not raw speed. The Foundation explicitly rejects reliance on unproven mathematical conjectures (proximity gap assumptions) for production soundness.

This matters because it validates a specific engineering philosophy: formal provable security over empirical performance. SP1 Hypercube already eliminates proximity gap conjectures in its multilinear STARK. The EF's security-first stance means that systems with strong formal guarantees will be preferred for the most security-critical application in the ecosystem -- proving the base layer itself.

Brevis's Pico Prism occupies an interesting position on this path. Built on Plonky3 with hash-based FRI commitments, it achieves 99%+ real-time proving on 16 RTX 5090 GPUs while remaining fully transparent. For non-Ethereum-L1 applications that still need on-chain verification, it wraps to Groth16 -- but the inner pipeline is transparent end to end.


## Summary

The Ethereum Foundation's L1 zkEVM mandate requires no trusted setup — no ceremony, no toxic waste, no pairing-based cryptography — end to end. Following the EF's December 2025 declaration that the speed race was "effectively won" (>99% of blocks proved within the 12-second slot time), security became the primary metric: 100-bit provable security by May 2026 and 128-bit by December 2026, with energy per proof (kWh) replacing raw throughput as the headline number. Brevis's Pico Prism illustrates that pure transparency is production-viable at non-L1 scale while still wrapping to Groth16 for external settlement.

## Key claims

- Ethereum Foundation L1 mandate: no trusted setup, no pairing-based cryptography, period.
- By December 2025 the EF declared the proving speed race "effectively won": >99% of blocks proved within the 12-second slot time.
- EF 2026 security targets: 100-bit provable security by May 2026; 128-bit by December 2026.
- New primary metric: energy consumption per proof (kWh), not raw proving speed.
- EF explicitly rejects reliance on unproven proximity gap conjectures for production soundness.
- SP1 Hypercube already eliminates proximity gap conjectures in its multilinear STARK.
- Brevis Pico Prism: pure FRI/Plonky3 pipeline on 16 RTX 5090 GPUs achieves 99%+ real-time Ethereum block proving while remaining fully transparent; wraps to Groth16 only for external on-chain settlement.

## Entities

- [[ceremony]]
- [[fri]]
- [[pico]]
- [[plonky3]]
- [[prism]]
- [[starks]]

## Dependencies

- [[ch02-two-ways-to-build-a-stage]] — the original transparent vs. trusted setup framing
- [[ch06-from-speed-race-to-security-race]] — EF's pivot from speed to security metrics
- [[ch07-the-quantum-threat-horizon]] — why hash-based commitments survive quantum attack
- [[ch08-on-chain-verification-in-2026]] — verification cost context for pure transparent systems

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [P1] B Three specific claims lack citations: (1) the EF's "December 2025 pivot" and its exact security targets (100-bit by May 2026, 128-bit by December 2026); (2) SP1 Hypercube eliminating proximity gap conjectures; (3) Brevis Pico Prism achieving 99%+ real-time proving on 16 RTX 5090 GPUs. The bibliography (ref 55: Kadianakis, December 2025) covers the EF security post but is not cited in-section.

## Links

- Up: [[10-the-synthesis-three-paths-not-two]]
- Prev: [[ch10-path-one-the-hybrid-stark-to-snark-pipeline]]
- Next: [[ch10-path-three-post-quantum-folding]]
