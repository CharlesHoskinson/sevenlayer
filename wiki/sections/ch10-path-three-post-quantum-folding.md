---
title: "Path Three: Post-Quantum Folding"
slug: ch10-path-three-post-quantum-folding
chapter: 10
chapter_title: "The Synthesis -- Three Paths, Not Two"
heading_level: 2
source_lines: [4405, 4416]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 352
---

## Path Three: Post-Quantum Folding

The third path is the newest and least traveled. It abandons both pairing-based cryptography and hash-based commitments in favor of lattice-based constructions that provide additive homomorphism (enabling folding), post-quantum security, and increasingly competitive proof sizes.

The key systems are LatticeFold (Boneh & Chen, ASIACRYPT 2025), LatticeFold+ (CRYPTO 2025), Neo/SuperNeo (Nguyen & Setty, ePrint 2025/294), and Symphony (Chen, ePrint 2025/1905). These systems use Module-SIS commitments -- lattice-based structures whose hardness NIST has validated through the FIPS 203/204 standardization process -- to achieve folding over polynomial rings without relying on discrete logarithms or pairings.

The proof sizes are larger than Groth16 but rapidly improving: Greyhound (Nguyen & Seiler, CRYPTO 2024) achieves ~50 KB proofs with lattice-based commitments, and LaBRADOR (CRYPTO 2023) achieves ~58 KB. These are orders of magnitude larger than Groth16's 192 bytes but competitive with raw STARK proofs. The performance trajectory suggests that lattice-based schemes may reach practical production within 3-5 years.

Why does this path matter? Because it is the only path that survives quantum computing without any caveats. The hybrid path (Path One) is quantum-vulnerable at the verification wrapper. The pure transparent path (Path Two) relies on hash functions whose collision resistance degrades under quantum attack (SHA-256 drops from 128-bit classical to ~85-bit quantum collision resistance via the BHT algorithm). The lattice path relies on Module-LWE/SIS, which is believed to be quantum-resistant by design -- the same assumption family that NIST chose for its post-quantum standards. This path does not merely survive the quantum era. It was built for it.

The post-quantum folding path has a structural advantage that maps directly onto the Layer 6 analysis from Chapter 7. That chapter presented a trilemma: algebraic functionality, post-quantum security, and succinctness -- pick two. Lattice-based commitments provide additive homomorphism (enabling folding, which is a form of algebraic functionality), post-quantum security, and increasingly competitive succinctness. The trilemma is not being sidestepped; it is being actively compressed. Whether it can be fully dissolved remains an open question -- KZG's $O(1)$ proof size with full homomorphism has no post-quantum match yet. But the gaps are narrowing with each paper.


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
