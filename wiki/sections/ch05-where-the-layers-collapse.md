---
title: "Where the Layers Collapse"
slug: ch05-where-the-layers-collapse
chapter: 5
chapter_title: "Encoding the Performance"
heading_level: 2
source_lines: [2311, 2340]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 657
---

## Where the Layers Collapse

This chapter has presented arithmetization as a distinct layer. But the evidence from real systems shows that the boundary between Layer 4 and its neighbors is porous.

### Layers 3 and 4: Jolt's Merger

In Jolt, witness generation *is* the arithmetization. Every instruction in the execution trace is decomposed into lookups on small subtables. The decomposition happens simultaneously with trace generation -- there is no meaningful step where "first you generate the witness, then you arithmetize it." The two processes are fused.

This has concrete implications. When the Feynman analysis asked "if Layers 3 and 4 collapse into one in Jolt, does the seven-layer model actually work?", the answer is that the model is descriptive, not prescriptive. It identifies conceptual concerns (witness generation, constraint encoding) that are always present, even when the implementation fuses them.

### Layers 2 and 4: Cairo's Co-Design

Cairo, StarkWare's ZK-native language, was designed specifically so that its instruction set would map efficiently to AIR constraints. The ISA *is* the constraint system. Language design (Layer 2) was dictated by arithmetization efficiency (Layer 4).

The dependency runs opposite to the top-down model the book follows. In Cairo's case, the constraint system came first, and the language was designed to match it. Cairo's memory model is "write-once" -- once a value is written to an address, it cannot be overwritten -- because write-once memory is much cheaper to prove in AIR constraints than read-write memory. A conventional language designer would never choose a write-once memory model. But the constraint system designer knows that proving memory consistency for write-once memory requires a simple sorted-access check (much cheaper than Merkle trees or fingerprinting), so the language was shaped to match. The pedagogical order (language before arithmetization) hides a real engineering dependency. Cairo was not "compiled to" AIR; it was "born from" AIR.

### The Proof Core: Layers 4, 5, and 6

The most significant cross-layer dependency is the "proof core" -- the inseparable triad of {finite field, polynomial commitment scheme, polynomial representation} that straddles Layers 4, 5, and 6.

Choose a 31-bit field (Layer 6) and you get fast arithmetic but need FRI-based commitments (Layer 5) and AIR or multilinear representations (Layer 4). Choose a 254-bit pairing-friendly field (Layer 6) and you can use KZG commitments (Layer 5) with univariate polynomials in Lagrange basis (Layer 4). Choose a lattice-based commitment over a 64-bit Goldilocks field (Layer 6) and you get post-quantum security with CCS-native constraints (Layer 4) and sumcheck-based folding (Layer 5).

These are not three independent choices. They are one choice with three manifestations. The seven-layer model usefully separates the *concerns* (what is being encoded? how is it committed? what field operations are available?) even when the *implementations* cannot be separated.

This is the collapse we warned about in Chapter 1. The seven-layer model is a pedagogical map. The engineering territory has three layers at the proof core, not seven, and the edges between them are bidirectional. Hold both models as you read: the pedagogical stack (useful for learning each concern in isolation) and the engineering DAG (useful for building real systems). Chapter 10 will draw the honest map -- seven nodes, fourteen directed edges, no pretense of independence.

A concrete example of this coupling: RISC Zero originally used a 254-bit field with KZG commitments and R1CS constraints. In 2023, they migrated to BabyBear (31-bit field) with FRI commitments and AIR constraints. The migration was not "swap out the field and keep everything else." It required simultaneously changing the field (Layer 6), the commitment scheme (Layer 5), and the constraint format (Layer 4) -- because none of the three could be changed independently. BabyBear does not support KZG (which needs a pairing-friendly curve), and FRI does not work naturally with R1CS (which lacks the evaluation-domain structure that FRI requires). The three layers moved as a unit, confirming that the "proof core" is a single design decision dressed up as three.

---


## Summary

Three concrete cross-layer collapses show the seven-layer model is descriptive, not prescriptive. In Jolt, witness generation and arithmetization are fused. In Cairo, the instruction set was designed to match AIR constraints. The proof core (field, commitment scheme, polynomial representation) is a single coupled design decision that spans Layers 4, 5, and 6 — changing any one component requires changing all three.

## Key claims

- Jolt: witness generation is arithmetization; decomposition into subtable lookups happens simultaneously with trace generation.
- Cairo: write-once memory model was chosen because it dramatically reduces AIR memory-consistency constraint cost vs. read-write memory.
- Proof-core triad: {31-bit field, FRI, AIR/multilinear} vs. {254-bit field, KZG, univariate Lagrange} vs. {64-bit Goldilocks, lattice, CCS+sumcheck} — three coherent bundles, not three independent choices.
- RISC Zero's 2023 migration changed field (BN254 → BabyBear), commitment scheme (KZG → FRI), and constraint format (R1CS → AIR) simultaneously — the three components cannot move independently.
- The seven-layer model separates concerns; the engineering reality has bidirectional edges between Layers 4, 5, and 6. Chapter 10 draws the honest DAG.

## Entities

- [[babybear]]
- [[bn254]]
- [[folding]]
- [[fri]]
- [[goldilocks]]
- [[jolt]]
- [[kzg]]
- [[lattice]]
- [[mersenne]]

## Dependencies

- [[ch05-lookup-arguments]] — Jolt's architecture is the Layer 3/4 collapse example
- [[ch05-the-sumcheck-protocol-the-hidden-foundation]] — sumcheck is the Layer 5 component of the proof core
- [[ch05-the-overhead-tax-10-000x-to-50-000x]] — field and commitment choice drive the overhead numbers
- [[ch05-midnight-s-zkir-a-concrete-layer-4]] — Midnight's BLS12-381 choice is a proof-core decision

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

## Links

- Up: [[05-encoding-the-performance]]
- Prev: [[ch05-midnight-s-zkir-a-concrete-layer-4]]
- Next: [[ch05-where-the-analogies-break]]
