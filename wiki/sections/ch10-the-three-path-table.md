---
title: "The Three-Path Table"
slug: ch10-the-three-path-table
chapter: 10
chapter_title: "The Synthesis -- Three Paths, Not Two"
heading_level: 2
source_lines: [4423, 4430]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 108
---

## The Three-Path Table

| Path | Setup | Inner Primitive | Outer Verification | PQ Status | Production Status |
|------|-------|----------------|-------------------|-----------|-------------------|
| **Hybrid STARK-to-SNARK** | STARK inner (transparent) + Groth16 outer (trusted) | Hash-based FRI / Merkle | BN254 pairing (~250K gas) | Inner: quantum-safe; Outer: quantum-vulnerable | Dominant production default |
| **Pure Transparent** | Transparent only | Hash-based FRI, no pairings | Large on-chain proof or alternative verification | Quantum-safe (with sufficient hash output) | Ethereum L1 mandate; advancing |
| **Post-Quantum Folding** | Transparent (lattice-based) | Module-SIS commitments | Lattice verification (higher cost) | Quantum-safe by design | Research frontier; 3-5 year horizon |


## Summary

A single comparison table summarizing the three production paths across setup type, inner primitive, outer verification, post-quantum status, and production readiness. Hybrid STARK-to-SNARK is the dominant production default; pure transparent is the Ethereum L1 mandate; post-quantum folding is a research frontier on a 3–5 year horizon.

## Key claims

- Hybrid STARK-to-SNARK: transparent inner + Groth16 outer (trusted); BN254 ~250K gas; inner quantum-safe, outer quantum-vulnerable; dominant production default.
- Pure Transparent: transparent only; hash-based FRI, no pairings; large on-chain proof or alternative verification; quantum-safe with sufficient hash output; Ethereum L1 mandate.
- Post-Quantum Folding: transparent lattice-based; Module-SIS commitments; higher-cost lattice verification; quantum-safe by design; research frontier, 3–5 year horizon.

## Entities

- [[bn254]]
- [[folding]]
- [[fri]]
- [[groth16]]
- [[lattice]]
- [[starks]]

## Dependencies

- [[ch10-path-one-the-hybrid-stark-to-snark-pipeline]] — detailed treatment of Path One
- [[ch10-path-two-pure-transparent]] — detailed treatment of Path Two
- [[ch10-path-three-post-quantum-folding]] — detailed treatment of Path Three

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [P3] C "Pure Transparent" row: "Large on-chain proof or alternative verification" is vague — no explanation of what "alternative verification" means (recursive aggregation to a non-BN254 verifier? off-chain settlement?). Could be sharpened.

## Links

- Up: [[10-the-synthesis-three-paths-not-two]]
- Prev: [[ch10-path-three-post-quantum-folding]]
- Next: [[ch10-the-causal-web-why-it-is-a-dag-not-a-stack]]
