---
title: "Maturity and Readiness"
slug: ch07-maturity-and-readiness
chapter: 7
chapter_title: "Layer 6 -- The Deep Craft"
heading_level: 2
source_lines: [3467, 3482]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 228
---

## Maturity and Readiness

As of early 2026, the picture looks like this:

**Deployed and battle-tested:** KZG (BN254 and BLS12-381), FRI/STARK (Goldilocks, BabyBear, M31), IPA/Bulletproofs (Pasta curves). These power every production ZK system -- Ethereum rollups, Zcash, Midnight, Starknet.

**Peer-reviewed and prototyped:** LatticeFold (ASIACRYPT 2025, presentation by Boneh and Chen), LatticeFold+ (CRYPTO 2025). Neo has an active implementation in Rust (the Nightstream repository, 15 crates). Concrete benchmarks are emerging but sparse.

**Proposed and promising:** Symphony (ePrint 2025/1905, no implementation yet). The high-arity folding concept is validated theoretically but awaits engineering.

**Standards in place:** NIST FIPS 203/204/205 (August 2024) standardize lattice-based key encapsulation and signatures. No standard yet exists for lattice-based zero-knowledge proof systems, but the parameter selection methodology (the lattice estimator) is well established.

The adoption trajectory suggests lattice-based proof systems will move from research prototypes to production-ready systems in 2026-2027, with Neo/Nightstream among the first to target production deployment. The specific blockers are concrete: GPU-optimized lattice arithmetic (matrix-vector products and NTTs over cyclotomic rings are parallelizable but no one has written production-grade GPU kernels for them yet), head-to-head benchmarking against Groth16 and Stwo at the same circuit sizes (to quantify the real-world cost of post-quantum security), and audit tooling for lattice parameter selection (the lattice estimator gives security levels, but auditors need standardized methods to validate parameter choices the way they validate elliptic curve parameters today).

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
