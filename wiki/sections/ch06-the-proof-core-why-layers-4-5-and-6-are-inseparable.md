---
title: "The Proof Core: Why Layers 4, 5, and 6 Are Inseparable"
slug: ch06-the-proof-core-why-layers-4-5-and-6-are-inseparable
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2815, 2832]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 371
---

## The Proof Core: Why Layers 4, 5, and 6 Are Inseparable

At this point in our tour of the seven-layer stack, a structural observation is unavoidable. The boundaries between Layer 4 (arithmetization), Layer 5 (proof system), and Layer 6 (cryptographic primitives) are not clean lines. They are gradients.

Consider the design decisions involved in building a proof system:

- The **finite field** (Layer 6) determines which arithmetic is fast. Mersenne-31 enables SIMD-friendly 32-bit operations. Goldilocks enables efficient 64-bit operations on GPUs. BN254 requires expensive 254-bit multi-precision arithmetic. The field choice propagates upward through every layer.

- The **commitment scheme** (Layer 6) determines the trust model and proof size. KZG commitments (from pairings, Layer 6) give constant-size proofs but require a trusted setup. FRI commitments (from hash functions, Layer 6) give logarithmic proofs with transparency. Ajtai commitments (from lattices, Layer 6) give post-quantum security with larger proofs. The commitment scheme shapes the proof system architecture.

- The **arithmetization** (Layer 4) determines which constraints the proof system must handle. R1CS, CCS, AIR, PLONKish -- each format has different properties, and the proof system must be designed to handle the chosen format efficiently. CCS folding (HyperNova) requires the sumcheck protocol. AIR proofs (STARKs) require FRI. The arithmetization and the proof system co-evolve.

These three choices -- field, commitment, arithmetization -- form a tightly coupled triad. Change one, and the other two must adapt. This is why we call them the "proof core": they function as a single design unit, even though our seven-layer model places them in separate layers.

The layered model is still useful for understanding. It separates concerns that are conceptually distinct: what the mathematics *is* (Layer 6), how computation is *encoded* (Layer 4), and how the encoding is *verified* (Layer 5). But the reader should understand that in practice, these layers are designed together, optimized together, and constrained by each other's choices. A proof system is not assembled from independent components like bricks in a wall. It is forged as a single alloy, where the properties of each ingredient determine the properties of the whole. Chapter 10 redraws the seven-layer model as a directed acyclic graph, and the proof core is the densest cluster of edges in that graph.

---


## Summary

Layers 4 (arithmetization), 5 (proof system), and 6 (cryptographic primitives) co-evolve as a tightly coupled triad: field choice determines arithmetic speed, commitment scheme determines trust model and proof size, and arithmetization format determines which proof protocol applies. These three are the "proof core" -- a single design unit forged together, not assembled from independent components.

## Key claims

- Field choice (Layer 6) propagates through all layers: M31 enables SIMD 32-bit; Goldilocks enables GPU 64-bit; BN254 requires expensive multi-precision arithmetic.
- Commitment scheme (Layer 6) determines trust model: KZG (constant-size, trusted setup), FRI (logarithmic, transparent), Ajtai (post-quantum, larger).
- Arithmetization (Layer 4) determines proof protocol: CCS folding requires sumcheck; AIR/STARKs require FRI.
- Field, commitment, and arithmetization form an inseparable triad; changing one requires adapting the other two.
- Chapter 10 redraws the seven-layer model as a DAG; the proof core is the densest cluster of edges.

## Entities

- [[kzg]]
- [[fri]]
- [[ajtai]]
- [[lattice]]
- [[mersenne]]
- [[goldilocks]]
- [[bn254]]
- [[hypernova]]
- [[starks]]
- [[plonk]]

## Dependencies

- [[ch05-layer-4-arithmetization]] — arithmetization (Layer 4) is one leg of the triad
- [[ch07-four-families-of-commitment-schemes]] — commitment schemes (Layer 6) are the second leg
- [[ch06-the-three-families]] — the three proof system families are instantiations of different triad choices
- [[ch10-the-causal-web-why-it-is-a-dag-not-a-stack]] — Chapter 10 formalizes the DAG view referenced here

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [none] X — no issues found.

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-real-time-ethereum-proving]]
- Next: [[ch06-fiat-shamir-vulnerabilities]]
