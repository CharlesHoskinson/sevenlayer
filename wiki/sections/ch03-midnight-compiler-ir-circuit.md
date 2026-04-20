---
title: "Midnight: Compiler, IR, Circuit"
slug: ch03-midnight-compiler-ir-circuit
chapter: 3
chapter_title: "Choreographing the Act"
heading_level: 2
source_lines: [1153, 1204]
source_commit: 6e757843ed29aa50ce4558719452a86510ed0d20
status: finalized
word_count: 520
---

## Midnight: Compiler, IR, Circuit

Compact's three-part compilation architecture illustrates a principle that applies across all of Layer 2: the compilation target shapes the developer's world.

From a single `.compact` source file, the compiler produces three distinct artifacts:

**Artifact 1: ZKIR circuits.** ZKIR (Zero-Knowledge Intermediate Representation) is a JSON-formatted circuit description with 24 typed instructions organized into eight categories:

- *arithmetic* (3): `add`, `mul`, `neg`
- *constraints* (4): `assert`, `constrain_eq`, `constrain_bits`, `constrain_to_boolean`
- *comparison* (2): `test_eq`, `less_than`
- *control flow* (2): `cond_select`, `copy`
- *type encoding* (3): `reconstitute_field`, `encode`, `decode`
- *division* (1): `div_mod_power_of_two`
- *cryptographic* (5): `transient_hash`, `persistent_hash`, `ec_mul_generator`, `ec_mul`, `hash_to_curve`
- *I/O* (4): `private_input`, `public_input`, `output`, `impact`

A concrete ZKIR excerpt from a witness-disclosure circuit illustrates the structure:

```json
{
  "publicTranscript": [
    {"op": "public_input", "id": "puzzle_grid", "type": "u32[16]"},
    {"op": "assert", "constraint": "sudoku_valid", "inputs": ["solution_grid", "puzzle_grid"]}
  ],
  "privateTranscriptOutputs": [
    {"op": "private_input", "id": "solution_grid", "type": "u32[16]", "disclosure": "required"}
  ]
}
```

Every ZKIR circuit has two transcript channels. The `publicTranscript` records ledger operations -- reads, writes, comparisons -- visible to the on-chain verifier. The `privateTranscriptOutputs` contains witness-derived values visible only to the prover. The ZKIR checker verifies that the serialized public transcript matches exactly what the circuit computed. Tampering with either transcript causes rejection with specific, diagnostic error messages.

**Artifact 2: TypeScript bindings.** The compiler generates type-safe JavaScript/TypeScript API code that handles contract interaction from the dApp frontend. This includes witness provider interfaces (the functions that supply private inputs), serialization between TypeScript types and field elements, and the transaction construction and submission pipeline. The witness functions run off-chain with access to private state, external APIs, and databases -- computation that could never run inside a ZK circuit.

**Artifact 3: Proving keys.** Contract-specific cryptographic material for the PLONK-based proof system on BLS12-381. Different circuits produce different keys. The proof server requires these keys to generate proofs; validators require them to verify proofs.

This three-part split is not an implementation detail. It reflects the fundamental architecture of privacy-preserving computation: what can be proven (ZKIR), what runs privately (TypeScript), and what makes proofs possible (keys). No other ZK language produces all three from a single source file with first-class blockchain integration. Circom produces R1CS plus a witness generator but no blockchain API. Noir produces ACIR but no TypeScript bindings and no blockchain integration. Cairo's compiler produces Sierra bytecode, later lowered to CASM, but no privacy separation -- the execution trace is a runtime artifact, not a compiler output. Compact unifies the entire dApp development pipeline.

For a system architect, the lesson generalizes beyond Midnight: the choice of Layer 2 language is not just a choice of syntax. It is a choice of compilation target, developer tooling, privacy model, and deployment pipeline. The language shapes everything downstream.

---

The choreography is written. The developer has expressed their computation in a language -- whether Rust targeting RISC-V, Cairo targeting Starknet, or Compact targeting Midnight's ZKIR. The compiler has translated the program into a form the proof system can work with.

But the program is just the *plan*. It describes what the computation should do. It does not contain the private data. It does not contain the execution trace. It does not contain the secret.

Now the magician goes backstage. The curtain closes. The audience waits. Behind the curtain, the magician will run the computation with real data -- real bank balances, real identity credentials, real votes -- and record every step. This recording is the witness: the complete execution trace that later layers will prove properties about without ever revealing.

The recording is where the real cost lives. And it is where the real vulnerabilities hide.

---

## Summary

Compact compiles a single `.compact` source file into three artifacts: ZKIR circuits (24 typed instructions, two transcript channels), TypeScript bindings (dApp API and witness providers), and PLONK proving keys on BLS12-381. No other ZK language unifies all three from one source, making Layer 2 language choice a decision about the entire downstream toolchain.

## Key claims

- ZKIR has 24 typed instructions in 8 categories: arithmetic, constraints, control flow, type encoding, cryptographic operations, and I/O.
- Two transcript channels: `publicTranscript` (on-chain verifier visible) and `privateTranscriptOutputs` (prover only); tampering causes rejection.
- TypeScript bindings include witness provider interfaces, field serialization, and transaction submission pipeline.
- Proving keys are circuit-specific; the proof server and validators both require them.
- Circom outputs R1CS + witness generator (no API); Noir outputs ACIR (no bindings, no integration); Cairo outputs execution traces (no privacy separation).
- Language choice determines compilation target, tooling, privacy model, and deployment pipeline — not just syntax.

## Entities

- [[bls12-381]]
- [[midnight]]
- [[plonk]]
- [[starknet]]

## Dependencies

- [[ch03-compact-s-disclosure-analysis]] — the disclosure analysis pass that feeds into the ZKIR output
- [[ch03-the-four-philosophies]] — places Compact's three-artifact output in the Philosophy D context
- [[ch05-midnight-s-zkir-a-concrete-layer-4]] — Layer 4 view of ZKIR structure and instruction set

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_All P0/P1/P2/P3 findings resolved in Phase 3 revisions (2026-04-18 through 2026-04-20)._

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

## Links

- Up: [[03-choreographing-the-act]]
- Prev: [[ch03-compact-s-disclosure-analysis]]
- Next: —
