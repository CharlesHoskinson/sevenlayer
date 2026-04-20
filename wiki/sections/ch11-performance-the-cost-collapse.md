---
title: "Performance: The Cost Collapse"
slug: ch11-performance-the-cost-collapse
chapter: 11
chapter_title: "zkVMs -- The Universal Stage"
heading_level: 2
source_lines: [4721, 4749]
source_commit: 9cb1d67a71f09c510cc06fa9493948e145a8f31a
status: reviewed
word_count: 458
---

## Performance: The Cost Collapse

The performance trajectory of zkVMs over the past 24 months is one of the steepest cost collapses in applied cryptography. It deserves to be stated plainly.

**Real-time Ethereum proving is solved.** Four independent teams proved over 99% of mainnet blocks within the 12-second slot time by late 2025:

| System | Hardware | Avg Block Time | % Blocks < 12s |
|--------|----------|---------------|-----------------|
| SP1 Hypercube | 16x RTX 5090 | 6.9 s [52] | 99.7% |
| ZisK | 24x RTX 5090 | 6.6 s | 99.7% |
| Pico Prism | 16x RTX 5090 | 6.9 s | 99%+ |
| OpenVM 2.0 | 16x RTX 5090 | < 12 s (p99) | ~99%+ |

Airbender proves a block in 35 seconds on a *single* H100 GPU -- the fastest single-GPU result, at 21.8 million cycles per second at the base STARK layer [53].

**Cost trajectory.** The 2,000-fold cost collapse described in Chapter 6 continued to accelerate: within 2025 alone, a further 45x reduction (from $1.69 to roughly $0.04 per block) [43, 44]. Roughly 10x per year, driven by algorithmic improvements, GPU optimization, and competition. A real-time proving cluster runs $60,000-$100,000: sixteen RTX 5090 GPUs (~$32K), dual-socket server, 512 GB RAM. For less than the price of a suburban house, you can prove every Ethereum block in real time.

**The Witness Gap grows with acceleration.** As GPU provers drove cryptographic proving time down 10-50x, witness generation -- still CPU-bound -- became the dominant bottleneck. The proportional shift described in Chapter 4 is now the defining structural constraint of zkVM performance: witness generation in a zkVM equals full VM emulation, which resists the parallelism that NTT and MSM exploit so effectively. The magician's backstage preparation now takes longer than sealing the proof.

Active optimization research is attacking this gap from multiple directions. ZKPoG reports substantial GPU speedups for witness generation, moving the CPU-bound stage onto the accelerator. OpenVM 2.0's SWIRL prover pairs with a new ahead-of-time compiler that executes RISC-V at near-native 3.8 GHz, reporting a 7.8x speedup over an optimized interpreter on CoreMark and dropping Ethereum block 24M execution from 1.8s to 0.5s. Nexus 3.0 abandoned the Nova folding pipeline for a Stwo-backed M31 architecture, citing a roughly 1000x practical penalty from classical folding.

**The EF security pivot (December 2025) [55].** The Ethereum Foundation declared the speed race won and shifted focus:
- May 2026 target: 100-bit provable security across all zkEVM teams
- December 2026 target: 128-bit provable security, sub-300 KB proofs
- New primary metric: energy per proof (kWh), replacing raw speed
- The EF rejects unproven conjectures (proximity gap assumptions) for production soundness

This pivot validates systems with strong formal security guarantees. It also shifts the competitive axis from "who can prove fastest" to "who can prove most securely" -- precisely where lattice-based and tensor-code approaches hold structural advantages. The race for speed is over. The race for rigor has begun.


## Summary

By late 2025, four independent teams achieved real-time Ethereum block proving (>99% of blocks under 12 s). The 2025 cost reduction reached 45x within the year alone, bringing cluster cost to $60K–$100K. The Ethereum Foundation responded by pivoting the primary metric from speed to 128-bit provable security, due December 2026.

## Key claims

- SP1 Hypercube, ZisK, Pico Prism, and OpenVM 2.0 each prove >99% of Ethereum mainnet blocks within the 12 s slot.
- ZisK achieves 6.6 s average block time on 24x RTX 5090 GPUs.
- Airbender: 35 s per block on a single H100 GPU at 21.8 million cycles/second.
- 2025 alone: 45x cost reduction ($1.69 → $0.04 per block); ~10x per year trend.
- Real-time proving cluster cost: $60K–$100K (16x RTX 5090 ~$32K + server + 512 GB RAM).
- Witness generation is now the dominant bottleneck; ZKPOG achieves up to 52x GPU speedup for witness generation.
- EF December 2025 pivot: 128-bit provable security by end of 2026; energy per proof becomes primary metric.
- EF rejects proximity gap conjectures for production soundness.

## Entities

- [[airbender]]
- [[h100]]
- [[lattice]]
- [[ntt]]
- [[zisk]]

## Dependencies

- [[ch11-the-landscape-table-march-2026]] — the benchmark table this section narrates
- [[ch06-real-time-ethereum-proving]] — Chapter 6's treatment of the same trajectory
- [[ch04-witness-generation-costs]] — Witness Gap established there
- [[ch10-path-one-the-hybrid-stark-to-snark-pipeline]] — pipeline context for GPU proving

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P2] (A) "a further 45x reduction (from $1.69 to four cents per block)" — $1.69 ÷ $0.04 = 42.25x, not 45x; the stated multiplier is inconsistent with the stated prices.
- [P3] (A) "the 2,000-fold cost collapse described in Chapter 6" — needs verification that ch6 uses this exact figure; if ch6 says a different number, this is an internal inconsistency.

## Links

- Up: [[11-zkvms-the-universal-stage]]
- Prev: [[ch11-the-proof-core-triad]]
- Next: [[ch11-risc-v-convergence]]
