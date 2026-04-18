---
title: "The Proof Core: Why Layers 4, 5, and 6 Are Inseparable"
slug: ch06-the-proof-core-why-layers-4-5-and-6-are-inseparable
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2806, 2823]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
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

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
