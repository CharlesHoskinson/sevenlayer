---
title: "Midnight's ZKIR: A Concrete Layer 4"
slug: ch05-midnight-s-zkir-a-concrete-layer-4
chapter: 5
chapter_title: "Encoding the Performance"
heading_level: 2
source_lines: [2229, 2310]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 1203
---

## Midnight's ZKIR: A Concrete Layer 4

Abstract discussions of constraint systems benefit from a concrete example. Midnight's ZKIR (Zero-Knowledge Intermediate Representation) provides one -- and it reveals that real-world arithmetization carries more structure than the mathematical formalism might suggest.

### The 24-Opcode DAG

ZKIR is not itself a constraint system. It is a typed instruction-level intermediate representation that sits *above* the constraint system in the compilation stack:

```
Compact (source language)
    |
    v
Compact IR (typed AST)
    |
    v
ZKIR (instruction DAG)  <-- This is what we are examining
    |
    v
PLONKish constraints (Halo2-style)
    |
    v
ZK proof (over BLS12-381)
```

A ZKIR circuit is a directed acyclic graph of 24 base instructions organized into eight categories:

- **Arithmetic** (3 opcodes): `add`, `mul`, `neg` -- basic field arithmetic modulo the BLS12-381 scalar field (approximately $2^{253}$). There is no subtraction opcode; the compiler implements a - b as add(a, neg(b)).
- **Constraints** (4 opcodes): `assert`, `constrain_eq`, `constrain_bits`, `constrain_to_boolean` -- the enforcement mechanism.
- **Comparison** (2 opcodes): `test_eq`, `less_than` -- produce boolean results without enforcing them.
- **Control flow** (2 opcodes): `cond_select`, `copy` -- conditional multiplexing and variable aliasing.
- **Type encoding** (3 opcodes): `reconstitute_field`, `encode`, `decode` -- type-level serialization.
- **Division** (1 opcode): `div_mod_power_of_two` -- integer-style division for byte extraction.
- **Cryptographic** (5 opcodes): `transient_hash`, `persistent_hash`, `ec_mul_generator`, `ec_mul`, `hash_to_curve` -- elliptic curve and hash operations over the Jubjub curve embedded in BLS12-381.
- **I/O** (4 opcodes): `private_input`, `public_input`, `output`, `impact` -- the boundary between circuit and ledger state.

Each instruction consumes inputs (field elements or references to earlier instruction outputs) and produces outputs. The DAG structure emerges from data dependencies: instruction i depends on instruction j if it references j's output. Variables are numbered sequentially (0, 1, 2, ...), and instructions can only reference outputs of earlier instructions.

### constrain_eq and constrain_bits: The Enforcement Backbone

Two opcodes embody the fundamental challenge of arithmetization: ensuring that abstract mathematical objects faithfully represent concrete computational values.

**constrain_eq** enforces that two field elements are identical. It produces no output. If the values differ, the circuit rejects. This is the fundamental correctness enforcement mechanism -- it appears after computations to verify results, in transcript verification to bind circuit values to on-chain state, and as the implicit check inside assertions.

There is a critical distinction between `constrain_eq` (which *enforces* equality and fails the circuit if violated) and `test_eq` (which *produces* a boolean result without enforcement). The Compact compiler uses `test_eq` for equality comparisons in program logic and `constrain_eq` for internal correctness checks. Confusing the two is precisely the kind of constraint error that causes the under-constrained vulnerabilities discussed in Chapter 3.

**constrain_bits** enforces that a field element lies within a range $[0, 2^N - 1]$. This is essential because ZKIR values are elements of the BLS12-381 scalar field -- numbers up to approximately $2^{253}$. But Compact types often have bounded ranges: `Uint<8>` must be in [0, 255], `Uint<32>` in $[0, 2^{32} - 1]$, `Boolean` must be exactly 0 or 1.

Without `constrain_bits`, a malicious prover could substitute any $253$-bit field element where an $8$-bit value was expected. If a circuit adds two `Uint<8>` values, the honest result is at most 510 -- but without range checking, a prover could claim the result is an arbitrary 253-bit number, potentially extracting value or corrupting state. Every `Uint<N>` value in compiled Compact code includes a corresponding `constrain_bits` to enforce the range constraint.

A general principle is at work: in constraint systems, everything that is *not* explicitly constrained is implicitly *allowed*. The prover will satisfy exactly the constraints you write, and nothing more. If you forget a constraint, the prover is free to exploit the gap. This is why under-constrained circuits are the dominant failure mode in ZK systems.

### Where ZKIR Sits in the Taxonomy

ZKIR's relationship to the standard constraint system taxonomy is instructive:

| Property | R1CS | AIR | PLONKish | CCS | ZKIR |
|----------|------|-----|----------|-----|------|
| Basic unit | Rank-1 constraint | Transition polynomial | Custom gate + wiring | Matrix-vector product | Typed instruction |
| Structure | Flat constraint list | Uniform trace | Gate array + permutation | Matrix equation | DAG of instructions |
| Abstraction level | Low | Low | Medium | Medium | **High** |
| Proof system binding | Groth16, Spartan | STARKs | Halo2, PLONK | Any IOP | PLONKish (via backend) |

ZKIR is not a competitor to R1CS, AIR, PLONKish, or CCS. It operates at a higher abstraction level. The `verify_sudoku` circuit from Chapter 3's Compact example would compile to a ZKIR graph of approximately 200-300 instruction nodes -- each range check, each distinctness assertion, each comparison against a given clue becomes a typed instruction that the backend later lowers to PLONKish gates. Each ZKIR opcode *generates* one or more underlying PLONKish constraints: `add` generates an addition gate, `mul` generates a multiplication gate, `constrain_bits` generates range-check constraints (potentially many gates for N-bit range), `ec_mul` generates a full scalar multiplication circuit (many internal gates), `persistent_hash` generates a hash circuit (many internal gates).

The ZKIR-to-PLONKish lowering is handled by the proof system backend. ZKIR documents the *semantic* layer -- what the circuit means. The actual arithmetization into PLONK gates happens below, invisible to the Compact developer.

Midnight's design philosophy becomes clear at this boundary. In Circom, the developer writes constraints directly. In SP1, the zkVM generates constraints automatically from the RISC-V execution trace. In Midnight, the Compact compiler produces ZKIR instructions that carry type information and semantic meaning (including blockchain-specific operations like ledger reads and writes), and the backend translates these into PLONKish constraints. The developer never touches the constraint system.

A ZKIR circuit could, in principle, be lowered to CCS instead of PLONKish. The typed instruction set would need to be decomposed into the matrix-vector product form that CCS requires. Whether Midnight's proof system will eventually migrate from PLONKish to CCS depends on the maturity of CCS-based proof systems and the availability of lattice-based folding schemes for production use -- a question that connects Layer 4 directly to the post-quantum considerations at Layer 6.

### The BLS12-381 Field Consequence

ZKIR operates over the BLS12-381 scalar field: a prime of approximately $2^{253}$, requiring 255 bits to represent. This is roughly 4x wider than the Goldilocks field (64-bit) used by Neo and Plonky2, and approximately 8x wider than the BabyBear (31-bit) or Mersenne-31 (31-bit) fields used by SP1, RISC Zero, and Stwo.

The large field is necessary for Midnight's architectural choices. BLS12-381 is a pairing-friendly curve, enabling KZG polynomial commitments and Groth16 verification. The Jubjub twisted Edwards curve embeds natively in BLS12-381's scalar field, enabling in-circuit elliptic curve operations for Pedersen commitments and key derivation. The mature ecosystem (Zcash, Ethereum 2.0) provides audited tooling.

But the large field is also the primary performance cost. Each field operation operates on 255-bit numbers using multi-precision arithmetic, while BabyBear or M31 operations use single-register native arithmetic. This is why Midnight's proof generation takes the order of 20 seconds per circuit (see Chapter 6 for exact measurements) -- acceptable for privacy-preserving blockchain transactions, but orders of magnitude slower than what small-field STARK systems achieve.

The field choice at Layer 6 determines the arithmetic cost at Layer 4. There is no escaping this dependency.

---


## Summary

Midnight's ZKIR (Zero-Knowledge Intermediate Representation) is a 24-opcode typed instruction DAG sitting above PLONKish constraints in the Compact compiler stack. It provides a high-abstraction layer 4 where the Compact developer writes contract logic while ZKIR opcodes generate the underlying PLONKish gates. The BLS12-381 scalar field (~$2^{253}$) is necessary for Jubjub curve embedding and KZG commitments but is the primary performance cost — ~20 s proof time per transaction.

## Key claims

- ZKIR has 24 opcodes in 8 categories: Arithmetic (3), Constraints (4), Comparison (2), Control flow (2), Type encoding (3), Division (1), Cryptographic (5), I/O (4).
- Compilation stack: Compact → Compact IR → ZKIR → PLONKish (Halo2-style) → ZK proof over BLS12-381.
- `constrain_eq` enforces equality and fails the circuit on violation; `test_eq` produces a boolean result without enforcement — confusing them produces under-constrained circuits.
- `constrain_bits` enforces a field element lies in $[0, 2^N-1]$; every `Uint<N>` value in Compact includes a corresponding range check.
- BLS12-381 scalar field: ~$2^{253}$, ~4x wider than Goldilocks (64-bit), ~8x wider than BabyBear/Mersenne-31 (31-bit).
- ZKIR could in principle target CCS instead of PLONKish; migration depends on lattice-based folding scheme maturity.
- In constraint systems, everything not explicitly constrained is implicitly allowed — the dominant failure mode is under-constrained circuits.

## Entities

- [[babybear]]
- [[bls12-381]]
- [[folding]]
- [[fri]]
- [[goldilocks]]
- [[groth16]]
- [[halo2]]
- [[jubjub]]
- [[kzg]]
- [[lattice]]
- [[mersenne]]
- [[midnight]]
- [[pedersen]]
- [[plonk]]
- [[small-field]]
- [[spartan]]
- [[starks]]
- [[sudoku]]
- [[zcash]]

## Dependencies

- [[ch05-the-constraint-system-evolution-r1cs-air-plonkish]] — ZKIR lowers to PLONKish; that taxonomy is prerequisite
- [[ch05-ccs-the-rosetta-stone]] — CCS migration path for ZKIR discussed
- [[ch05-the-overhead-tax-10-000x-to-50-000x]] — BLS12-381 field cost explains the 20-s proof time

## Sources cited

- Midnight ZKIR Reference (v2/v3), 119 oracle traces. Compact compiler v0.29.0.

## Open questions

None flagged by this section.

## Improvement notes

## Links

- Up: [[05-encoding-the-performance]]
- Prev: [[ch05-the-overhead-tax-10-000x-to-50-000x]]
- Next: [[ch05-where-the-layers-collapse]]
