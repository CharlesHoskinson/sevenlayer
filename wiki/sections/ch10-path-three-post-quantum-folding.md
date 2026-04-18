---
title: "Path Three: Post-Quantum Folding"
slug: ch10-path-three-post-quantum-folding
chapter: 10
chapter_title: "The Synthesis -- Three Paths, Not Two"
heading_level: 2
source_lines: [4405, 4416]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 352
---

## Path Three: Post-Quantum Folding

The third path is the newest and least traveled. It abandons both pairing-based cryptography and hash-based commitments in favor of lattice-based constructions that provide additive homomorphism (enabling folding), post-quantum security, and increasingly competitive proof sizes.

The key systems are LatticeFold (Boneh & Chen, ASIACRYPT 2025), LatticeFold+ (CRYPTO 2025), Neo/SuperNeo (Nguyen & Setty, ePrint 2025/294), and Symphony (Chen, ePrint 2025/1905). These systems use Module-SIS commitments -- lattice-based structures whose hardness NIST has validated through the FIPS 203/204 standardization process -- to achieve folding over polynomial rings without relying on discrete logarithms or pairings.

The proof sizes are larger than Groth16 but rapidly improving: Greyhound (Nguyen & Seiler, CRYPTO 2024) achieves ~50 KB proofs with lattice-based commitments, and LaBRADOR (CRYPTO 2023) achieves ~58 KB. These are orders of magnitude larger than Groth16's 192 bytes but competitive with raw STARK proofs. The performance trajectory suggests that lattice-based schemes may reach practical production within 3-5 years.

Why does this path matter? Because it is the only path that survives quantum computing without any caveats. The hybrid path (Path One) is quantum-vulnerable at the verification wrapper. The pure transparent path (Path Two) relies on hash functions whose collision resistance degrades under quantum attack (SHA-256 drops from 128-bit classical to ~85-bit quantum collision resistance via the BHT algorithm). The lattice path relies on Module-LWE/SIS, which is believed to be quantum-resistant by design -- the same assumption family that NIST chose for its post-quantum standards. This path does not merely survive the quantum era. It was built for it.

The post-quantum folding path has a structural advantage that maps directly onto the Layer 6 analysis from Chapter 7. That chapter presented a trilemma: algebraic functionality, post-quantum security, and succinctness -- pick two. Lattice-based commitments provide additive homomorphism (enabling folding, which is a form of algebraic functionality), post-quantum security, and increasingly competitive succinctness. The trilemma is not being sidestepped; it is being actively compressed. Whether it can be fully dissolved remains an open question -- KZG's $O(1)$ proof size with full homomorphism has no post-quantum match yet. But the gaps are narrowing with each paper.


## Summary

The third path abandons both pairing-based and hash-based cryptography in favor of lattice-based constructions (Module-SIS) that provide additive homomorphism for folding alongside post-quantum security. Proof sizes — ~50–58 KB for Greyhound and LaBRADOR — are orders of magnitude larger than Groth16's 192 bytes but competitive with raw STARK proofs, and the performance trajectory suggests practical production within 3–5 years. This path is the only one that survives quantum computing without caveats: Path One's Groth16 wrapper and Path Two's hash functions both degrade under quantum attack, while Module-LWE/SIS is NIST-validated for the post-quantum era.

## Key claims

- Key systems: LatticeFold (Boneh & Chen, ASIACRYPT 2025), LatticeFold+ (CRYPTO 2025), Neo/SuperNeo (Nguyen & Setty, ePrint 2025/294), Symphony (Chen, ePrint 2025/1905).
- Commitment basis: Module-SIS, whose hardness NIST validated via FIPS 203/204 standardization.
- Greyhound (Nguyen & Seiler, CRYPTO 2024): ~50 KB proofs with lattice-based commitments.
- LaBRADOR (CRYPTO 2023): ~58 KB proofs.
- Both are orders of magnitude larger than Groth16 (192 bytes) but competitive with raw STARK proofs.
- Path One is quantum-vulnerable at the Groth16 wrapper; Path Two's SHA-256 drops from 128-bit classical to ~85-bit quantum collision resistance via the BHT algorithm.
- Module-LWE/SIS is the same assumption family NIST chose for its post-quantum standards.
- The Chapter 7 trilemma (algebraic functionality vs. post-quantum security vs. succinctness) is being actively compressed but not yet fully dissolved — KZG's O(1) proof size with full homomorphism has no post-quantum match yet.

## Entities

- [[boneh]]
- [[folding]]
- [[groth16]]
- [[kzg]]
- [[lattice]]
- [[latticefold]]
- [[nist]]
- [[setty]]
- [[symphony]]

## Dependencies

- [[ch06-the-post-quantum-horizon]] — earlier survey of lattice-based proof systems
- [[ch07-the-trilemma-and-its-dissolution]] — the trilemma (algebraic functionality, PQ security, succinctness) this path compresses
- [[ch07-lattice-based-proving]] — Module-SIS commitment construction detail
- [[ch07-three-hardness-assumptions-three-worlds]] — hardness landscape context

## Sources cited

- Boneh & Chen — LatticeFold, ASIACRYPT 2025
- LatticeFold+, CRYPTO 2025
- Nguyen & Setty — Neo/SuperNeo, ePrint 2025/294
- Chen — Symphony, ePrint 2025/1905
- Nguyen & Seiler — Greyhound, CRYPTO 2024
- LaBRADOR, CRYPTO 2023
- NIST FIPS 203/204

## Open questions

- Whether the Chapter 7 trilemma can be fully dissolved (KZG-level O(1) succinctness + post-quantum security) remains unresolved.

## Improvement notes

- [P1] A/B "FIPS 203/204 standardization process" cited as validating Module-SIS is imprecise: FIPS 203 standardizes ML-KEM (Module-LWE based key encapsulation), FIPS 204 standardizes ML-DSA (a signature based on Module-LWE/SIS). Module-SIS specifically underpins FIPS 204 and the relevant hash-based signature in FIPS 205 (SLH-DSA). Citing both 203 and 204 as the Module-SIS validation conflates the KEM and signature standards. Should specify FIPS 204 (and FIPS 205 for context).
- [P2] B Greyhound is cited as "Nguyen & Seiler, CRYPTO 2024" but has no BIBLIOGRAPHY.md entry — only ch07-lattice-based-proving references it by name without a full citation. Needs a bibliography entry.
- [P2] B "Neo/SuperNeo" — bibliography ref 21 covers Neo (Nguyen & Setty, ePrint 2025/294) but "SuperNeo" is not documented anywhere else in the wiki. Either a distinct paper needing its own citation, or an informal name that should be clarified.

## Links

- Up: [[10-the-synthesis-three-paths-not-two]]
- Prev: [[ch10-path-two-pure-transparent]]
- Next: [[ch10-the-three-path-table]]
