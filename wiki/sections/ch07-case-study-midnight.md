---
title: "Case Study: Midnight"
slug: ch07-case-study-midnight
chapter: 7
chapter_title: "Layer 6 -- The Deep Craft"
heading_level: 2
source_lines: [3333, 3394]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 785
---

## Case Study: Midnight

To see how Layer 6 choices play out in a real system, consider Midnight -- a privacy-focused blockchain built by Input Output Global (IOG), the company behind Cardano. Midnight makes every choice from the pairing-based, pre-quantum playbook. The consequences cascade through every layer.

### The Stack

**Scalar field:** BLS12-381, with a ~253-bit prime modulus $r$. Every value in Midnight's zero-knowledge circuits -- inputs, outputs, intermediate computations, token balances -- is an element of $\mathbb{F}_r$.

**Commitment scheme:** KZG, implied by the choice of BLS12-381 (a pairing-friendly curve). The wallet SDK caches BLS parameters locally (a structured reference string from a trusted setup ceremony). Proof size is constant. Verification is a single pairing check.

**Embedded curve:** Jubjub, a twisted Edwards curve whose order divides $r$. Jubjub lives "inside" BLS12-381's scalar field, enabling efficient elliptic curve operations (point addition, scalar multiplication, hash-to-curve) within zero-knowledge circuits without the overhead of non-native field arithmetic.

**Hash functions:** Poseidon-family algebraic hashes, represented at the ZKIR level as opaque opcodes (`transient_hash`, `persistent_hash`, `hash_to_curve`). Algebraic hash functions are dramatically more efficient inside ZK circuits than traditional hash functions like SHA-256, because their operations (field additions and multiplications) are native to the circuit's arithmetic.

**Token model:** UTXO-based shielded tokens (similar to Zcash Sapling). A coin is a triple (nonce, color, value) committed to a global Merkle tree via `persistent_hash`. Nullifiers prevent double-spending. Pedersen commitments on Jubjub hide transaction values.

### What Midnight Gets

Midnight occupies the "high algebraic functionality + high succinctness" corner of the design space. The pairing enables constant-size KZG proofs. Jubjub enables rich in-circuit elliptic curve operations (key derivation, Pedersen commitments, hash-to-curve) with native efficiency. The PLONK-like proof system compiles from a purpose-built language (Compact) through a 24-opcode instruction set (ZKIR). The standard library provides Merkle trees, shielded token circuits, and a full Zswap protocol for private token transfers.

The result is maximum algebraic functionality. Every cryptographic primitive -- hashing, commitment, key derivation, signature verification -- operates natively within the circuit's arithmetic. Nothing requires emulation or non-native field arithmetic.

### What Midnight Gives Up

Post-quantum resilience: none. Every component of Midnight's cryptographic stack depends on either the discrete logarithm problem (Jubjub key derivation, Pedersen commitments) or pairing-based assumptions (KZG proof verification). Shor's algorithm breaks all of it.

The vulnerability assessment is total:

| Component | Assumption | Post-Quantum Status |
|---|---|---|
| Proof verification (KZG) | q-SDH on BLS12-381 | Broken by Shor |
| Jubjub key derivation | ECDLP on Jubjub | Broken by Shor |
| Pedersen commitments | DLP on Jubjub | Broken by Shor (binding fails) |
| In-circuit hashing | CRHF (Poseidon) | Weakened but likely survivable |
| Merkle tree roots | CRHF | Likely survivable |
| Nullifiers | PRF | Likely survivable |

The proof system is the deepest vulnerability. Even if Midnight replaced its Pedersen commitments with hash-based constructions, and even if it switched from Jubjub key derivation to a lattice-based signature scheme, the proof verification mechanism is fundamentally tied to the BLS12-381 pairing. Changing it would require replacing KZG with a different commitment scheme, which would require changing the field, which would require rewriting the compiler, the standard library, the prover, the verifier, and the wallet SDK.

The one-way-door property is in full force. Midnight's choice of BLS12-381 is not a parameter that can be updated. It is the foundation on which every other component is built. A post-quantum migration for Midnight would not be an upgrade. It would be a new system.

### Midnight vs. Neo: Opposite Corners

The contrast with Neo/Nightstream makes the tradeoffs vivid:

| Dimension | Midnight | Neo/Nightstream |
|---|---|---|
| Field | BLS12-381, ~253 bits | Goldilocks, 64 bits |
| Ring | N/A (field-based) | $\mathbb{F}_q[X]/(\Phi_{81})$, degree 54 |
| Commitment | KZG (pairing) | Ajtai (lattice) |
| Hash | Poseidon (algebraic) | Ring-SIS (lattice) |
| Proof size | $O(1)$ curve points | $O(\log n)$ ring elements |
| PQ secure | No | Yes (127-bit) |
| EC in-circuit | Yes (Jubjub, native) | No (would need circuit emulation) |
| Trusted setup | Yes (powers-of-tau) | No |

Neo trades Midnight's in-circuit elliptic curve operations and constant-size proofs for post-quantum security, transparent setup, and a simpler recursive architecture (no curve cycles needed). Neither system dominates on every dimension. The question is which tradeoffs matter more for your threat model and time horizon.

For a system deployed today that needs maximum on-chain efficiency and whose privacy guarantees are measured in years (not decades), Midnight's choices are defensible. For a system that needs to protect sensitive data for 15 or more years, or that must comply with NIST's 2035 deprecation timeline, Neo's choices are the only viable path.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
