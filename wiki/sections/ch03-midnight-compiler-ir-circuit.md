---
title: "Midnight: Compiler, IR, Circuit"
slug: ch03-midnight-compiler-ir-circuit
chapter: 3
chapter_title: "Choreographing the Act"
heading_level: 2
source_lines: [1158, 1187]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 520
---

## Midnight: Compiler, IR, Circuit

Compact's three-part compilation architecture illustrates a principle that applies across all of Layer 2: the compilation target shapes the developer's world.

From a single `.compact` source file, the compiler produces three distinct artifacts:

**Artifact 1: ZKIR circuits.** ZKIR (Zero-Knowledge Intermediate Representation) is a JSON-formatted circuit description with 24 typed instructions organized into eight categories: arithmetic (`add`, `mul`, `neg`), constraints (`assert`, `constrain_bits`, `constrain_eq`), control flow (`cond_select`, `copy`), type encoding (`decode`, `encode`), cryptographic operations (`ec_mul`, `hash_to_curve`, `persistent_hash`), and I/O (`impact`, `output`, `private_input`, `public_input`).

Every ZKIR circuit has two transcript channels. The `publicTranscript` records ledger operations -- reads, writes, comparisons -- visible to the on-chain verifier. The `privateTranscriptOutputs` contains witness-derived values visible only to the prover. The ZKIR checker verifies that the serialized public transcript matches exactly what the circuit computed. Tampering with either transcript causes rejection with specific, diagnostic error messages.

**Artifact 2: TypeScript bindings.** The compiler generates type-safe JavaScript/TypeScript API code that handles contract interaction from the dApp frontend. This includes witness provider interfaces (the functions that supply private inputs), serialization between TypeScript types and field elements, and the transaction construction and submission pipeline. The witness functions run off-chain with access to private state, external APIs, and databases -- computation that could never run inside a ZK circuit.

**Artifact 3: Proving keys.** Contract-specific cryptographic material for the PLONK-based proof system on BLS12-381. Different circuits produce different keys. The proof server requires these keys to generate proofs; validators require them to verify proofs.

This three-part split is not an implementation detail. It reflects the fundamental architecture of privacy-preserving computation: what can be proven (ZKIR), what runs privately (TypeScript), and what makes proofs possible (keys). No other ZK language produces all three from a single source file with first-class blockchain integration. Circom produces R1CS plus a witness generator but no blockchain API. Noir produces ACIR but no TypeScript bindings and no blockchain integration. Cairo produces execution traces but no privacy separation. Compact unifies the entire dApp development pipeline.

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

- [P1] (A) The body claims "24 typed instructions organized into eight categories" and then lists: arithmetic (3), constraints (3), control flow (2), type encoding (2), cryptographic operations (3), and I/O (4) = 17 instructions. Seven instructions are unaccounted for. Either the count is wrong or the category listing is incomplete; reconcile the total with the enumerated list.
- [P2] (A) "Cairo produces execution traces but no privacy separation" — Cairo's *compiler* does not produce execution traces; execution traces are a runtime artifact of the CairoVM. The compiler produces Sierra/CASM bytecode. The comparison is technically imprecise.
- [P2] (B) No citations in "Sources cited" for any of the ZKIR specifics (24 instructions, 8 categories, two transcript channels). These are verifiable implementation details that should reference Midnight's technical documentation or the Compact spec.
- [P2] (C) "No other ZK language generates all three from one source" is a strong uniqueness claim that appears in both this section and in `ch03-the-four-philosophies`. The repetition is intentional for emphasis but risks feeling like padding; consider consolidating.
- [P3] (E) The section describes ZKIR at the instruction-category level but never gives an example of a ZKIR JSON fragment. Given that the section is titled "Compiler, IR, Circuit," a small concrete ZKIR excerpt would ground the claim that it is "JSON-formatted" and show the two transcript channels in practice.

## Links

- Up: [[03-choreographing-the-act]]
- Prev: [[ch03-compact-s-disclosure-analysis]]
- Next: —
