---
title: "Path Three: Post-Quantum Folding"
slug: ch10-path-three-post-quantum-folding
chapter: 10
chapter_title: "The Synthesis -- Three Paths, Not Two"
heading_level: 2
source_lines: [4409, 4420]
source_commit: 53f41415d307dcd4ed73d852dfd6aa97146e882f
status: reviewed
word_count: 352
---

## Path Three: Post-Quantum Folding

The third path is the newest and least traveled. It abandons both pairing-based cryptography and hash-based commitments in favor of lattice-based constructions that provide additive homomorphism (enabling folding), post-quantum security, and increasingly competitive proof sizes.

The key systems are LatticeFold (Boneh and Chen, ASIACRYPT 2025), LatticeFold+ (CRYPTO 2025), Neo and SuperNeo (Nguyen and Setty, ePrint 2025/294 [21] -- SuperNeo extends Neo to non-uniform IVC, the lattice analog of SuperNova, and is presented in the same paper), and Symphony (Chen, ePrint 2025/1905). These systems use Module-SIS commitments -- lattice-based structures whose hardness underpins NIST's FIPS 204 signature standard (ML-DSA) [64]. For context, the broader Module-LWE/SIS family also supports FIPS 203's ML-KEM (encapsulation, Module-LWE) and FIPS 205's SLH-DSA (stateless hash-based signatures) [25]. The folding constructions rely specifically on the Module-SIS hardness that FIPS 204 validates, and they achieve folding over polynomial rings without discrete logarithms or pairings.

The proof sizes are larger than Groth16 but rapidly improving: Greyhound (Nguyen and Seiler, CRYPTO 2024 [65]) achieves roughly 50 KB proofs with lattice-based commitments, and LaBRADOR (CRYPTO 2023) reports roughly 58 KB. Orders of magnitude larger than Groth16's 192 bytes, but competitive with raw STARK proofs. The trajectory suggests lattice-based schemes may reach practical production within three to five years.

Why does this path matter? Because it is the only path that survives quantum computing without caveats. The hybrid path (Path One) is quantum-vulnerable at the verification wrapper. The pure transparent path (Path Two) relies on hash functions whose collision resistance degrades under Grover-style and BHT-style quantum attacks -- SHA-256 drops from 128-bit classical collision resistance toward roughly 85-bit quantum collision resistance in the BHT model. The lattice path rests on Module-LWE/SIS, the same assumption family NIST chose for its post-quantum standards. It does not merely survive the quantum era. It was built for it.

The post-quantum folding path maps directly onto the Layer 6 analysis from Chapter 7. That chapter presented a trilemma: algebraic functionality, post-quantum security, and succinctness -- pick two. Lattice-based commitments provide additive homomorphism (enabling folding, a form of algebraic functionality), post-quantum security, and increasingly competitive succinctness. The trilemma is not being sidestepped; it is being actively compressed. Whether it can be fully dissolved remains open -- KZG's $O(1)$ proof size with full homomorphism has no post-quantum match yet. But the gaps narrow with each paper.


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

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

## Links

- Up: [[10-the-synthesis-three-paths-not-two]]
- Prev: [[ch10-path-two-pure-transparent]]
- Next: [[ch10-the-three-path-table]]
