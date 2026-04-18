---
title: "The Three-Path Table"
slug: ch10-the-three-path-table
chapter: 10
chapter_title: "The Synthesis -- Three Paths, Not Two"
heading_level: 2
source_lines: [4417, 4424]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 108
---

## The Three-Path Table

| Path | Setup | Inner Primitive | Outer Verification | PQ Status | Production Status |
|------|-------|----------------|-------------------|-----------|-------------------|
| **Hybrid STARK-to-SNARK** | STARK inner (transparent) + Groth16 outer (trusted) | Hash-based FRI / Merkle | BN254 pairing (~250K gas) | Inner: quantum-safe; Outer: quantum-vulnerable | Dominant production default |
| **Pure Transparent** | Transparent only | Hash-based FRI, no pairings | Large on-chain proof or alternative verification | Quantum-safe (with sufficient hash output) | Ethereum L1 mandate; advancing |
| **Post-Quantum Folding** | Transparent (lattice-based) | Module-SIS commitments | Lattice verification (higher cost) | Quantum-safe by design | Research frontier; 3-5 year horizon |


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
