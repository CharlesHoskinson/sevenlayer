---
title: "The `disclose()` Boundary: Midnight's Witness Architecture"
slug: ch04-the-disclose-boundary-midnight-s-witness-architecture
chapter: 4
chapter_title: "The Secret Performance"
heading_level: 2
source_lines: [1489, 1550]
source_commit: b3ed881318761d3fd0e65ead7ea58e3f6536ccf9
status: reviewed
word_count: 1045
---

## The `disclose()` Boundary: Midnight's Witness Architecture

Midnight's approach to witness generation illustrates both the power and the subtlety of the witness/circuit separation. (Note: the architecture described here is specific to Midnight's Compact/ZKIR stack. Other ZK systems handle witness generation differently -- RISC-V zkVMs generate witnesses by emulating a processor, while Circom circuits have separate witness calculator programs.)

In Compact, the two worlds are sharply delineated:

| Property | Witnesses | Circuits |
|---|---|---|
| Where they run | Off-chain (user's browser or node) | Compiled to ZKIR, proven locally, verified on-chain |
| What they can do | Arbitrary computation (JavaScript) | Only ZK-provable computation (field arithmetic, hashing, comparisons) |
| What they access | Private state, external APIs, databases | Only circuit inputs (public and disclosed private values) |
| Privacy | Completely private -- never leaves the device | Proven but not revealed |

Witness functions are *declared* in Compact but *implemented* in TypeScript:

```typescript
witness get_secret(): Bytes<32>;  // declared in Compact
```

```javascript
// implemented in TypeScript
const witnesses = {
  get_secret: (ctx) => [ctx.privateState, secretKey]
};
```

Each witness function receives the current context -- including a `privateState` object that persists across invocations -- and returns a tuple of the updated private state and the witness value. This means witnesses can maintain state, query external services, read databases, and perform arbitrary computation. They are full JavaScript programs, not circuit-compatible snippets.

The `disclose()` operator is the *sole gateway* from the witness world to the circuit world. Without it, witness values are invisible to the circuit, the proof, and the chain. With it, the value enters the circuit as a `private_input` in the ZKIR -- the verifier never sees the value, but the constraints verify properties about it.

The compiled ZKIR circuit has two transcript channels that encode this separation physically:

The `publicTranscript` records every ledger operation -- reads, writes, comparisons -- as a sequence of VM operations. The on-chain verifier sees this transcript and checks that it is consistent with the proof. If the developer's circuit reads a counter value from the ledger, that read appears in the public transcript. If the circuit increments the counter, that increment appears. The public transcript is the complete audit trail of on-chain state changes.

The `privateTranscriptOutputs` contains the witness values that entered the circuit through `disclose()`. Only the prover sees these. They are consumed during proof generation by `private_input` instructions in the ZKIR and then discarded. The ZKIR checker verifies that both transcripts are fully consumed -- no extra values, no missing values, no tampering.

This two-transcript model achieves something precise: the verifier knows *what changed* on the ledger (from the public transcript) and is convinced that the changes are valid (from the ZK proof), but does not know *why* the changes were made (the private inputs that drove the computation). The "what" is public. The "why" is private.

In practice, the pipeline for a Midnight transaction involves four sequential steps:

1. `contracts.callTx()` reads current ledger state via the indexer, executes the circuit locally with current state and private witnesses, and produces an unproven transaction.

2. `proofProvider.proveTx()` generates the ZK proof -- the dominant latency step, as detailed in Chapter 6 -- producing a proven transaction.

3. `walletProvider.balanceTx()` binds the transaction, runs token balancing (unshielded, shielded, and dust), signs UTXO inputs with Schnorr signatures (Midnight uses a Cardano-native Schnorr scheme over the Ed25519 curve, distinct from Bitcoin's BIP-340), and merges the balancing transaction with the original.

4. `midnightProvider.submitTx()` submits to the blockchain, where the node verifies the ZK proof, checks that the public transcript matches the ledger state, and applies the state transition.

At no point do witnesses cross the network. The developer guide states this explicitly: "Witnesses stay local. Never sent to chain."

The side-channel implications matter here. The cryptographic proving step runs for roughly the same time regardless of witness values because the constraint count is fixed per circuit; only the witness computation phase varies with the witnesses. The fixed-cost proving step dominates total transaction time, which provides incidental timing uniformity -- any variation in witness computation is drowned out by the long proving tail. But a dedicated attacker measuring sub-second variations in the witness computation phase could still extract information. And the documentation does not address cache timing, network timing (when a user queries the indexer immediately before submitting a transaction, the timing correlation reveals which contract state they are acting on), or transaction structure analysis (the number of segments in a transaction could reveal which circuit was called). As established in the Side-Channel Attacks section above, these implementation-level channels exist independently of the cryptographic proof's zero-knowledge property.

Privacy on Midnight is genuine at the cryptographic level. At the implementation level, the runtime side-channel surface is unexamined -- a gap that is not unique to Midnight but is notable given the project's otherwise rigorous compile-time privacy guarantees.

One accidental privacy benefit: the fixed cost of the PLONK proving step provides natural timing padding. Midnight's developer documentation and community reports (Midnight developer forum, 2025) describe typical proof generation times of 20-60 seconds on desktop hardware; whether the witness contains a trivial secret or a complex multi-step computation, the proof generation time sits within that band. An observer measuring transaction timing cannot easily distinguish between different witness computations. The padding is natural but not designed. A dedicated attacker measuring sub-second timing variations in the pre-proof witness phase might still extract information. But the tens-of-seconds proving step provides a large, fixed-duration buffer that dominates the total transaction time.

The developer guide's demonstration of the private voting dApp provides a concrete end-to-end example. The off-chain witness construction computes Poseidon hashes using the same `persistentHash` function available in both the Compact circuit and the JavaScript SDK. The voter provides their secret key, vote choice, Merkle sibling hash, and direction flag as witnesses. The circuit reconstructs the Merkle root from these witnesses and asserts it matches the on-chain root. The circuit also computes a nullifier -- `persistentHash([pad(32, "nullf:"), secret_key])` -- using domain separation so that the nullifier hash and the voter's attestation hash are cryptographically unlinkable. The nullifier is disclosed (it must appear on-chain to prevent double-voting), but it cannot be traced back to the voter's identity.

What the on-chain verifier sees per vote: a nullifier hash and updated vote tallies. What the verifier does not see: which voter, their exact identity, or which Merkle leaf they occupy. The privacy boundary is sharp, and it is enforced at every level: by the compiler (disclosure analysis), by the ZKIR checker (transcript integrity), and by the cryptographic construction (domain-separated hashing).

---


## Summary

Midnight's Compact language enforces the witness/circuit boundary via a `disclose()` operator: witness functions are arbitrary TypeScript programs running off-chain that never reach the chain; `disclose()` is the sole gateway that moves a value into the ZKIR circuit as a `private_input`. A two-transcript model (publicTranscript for ledger changes, privateTranscriptOutputs for witness values) ensures the verifier sees what changed but not why. The 18-second PLONK proving step provides accidental timing uniformity, but Midnight's implementation-level side-channel analysis is undocumented.

## Key claims

- Witness functions are implemented in TypeScript, declared in Compact, and never leave the user's device.
- `disclose()` is the sole gateway from the witness world into the ZKIR circuit.
- The publicTranscript records all ledger operations; the privateTranscriptOutputs contains witness values consumed during proving and then discarded.
- The ZKIR checker verifies both transcripts are fully consumed — no extra values, no missing values, no tampering.
- A Midnight transaction follows four steps: `callTx` → `proveTx` → `balanceTx` → `submitTx`.
- The 18-second PLONK proving step provides natural (unintentional) timing padding that masks witness computation variation.
- Domain-separated Poseidon hashing (`persistentHash`) makes nullifiers cryptographically unlinkable to voter identity.
- Midnight has the most rigorous compile-time privacy guarantees (disclosure analysis) but the least documented runtime privacy analysis.

## Entities

- [[midnight]]
- [[plonk]]
- [[poseidon]]
- [[sdk]]
- [[utxo]]

## Dependencies

- [[ch03-compact-s-disclosure-analysis]] — the compile-time disclosure analysis that enforces the boundary
- [[ch03-midnight-compiler-ir-circuit]] — ZKIR structure the `disclose()` operator targets
- [[ch04-side-channel-attacks-when-the-walls-leak]] — the implementation-level leakage Midnight does not address
- [[ch05-midnight-s-zkir-a-concrete-layer-4]] — ZKIR internals including `private_input` instruction

## Sources cited

- Midnight developer guide (witness/circuit separation, `disclose()` operator, transaction pipeline)
- Midnight private voting dApp example (Poseidon-based nullifier construction)

## Open questions

- Network timing correlation: a user who queries the indexer immediately before submitting a transaction may reveal which contract state they are acting on — not analyzed in Midnight documentation.
- Transaction structure analysis (segment count could reveal which circuit was called) is not addressed.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [P3] (E) The section notes that "the number of segments in a transaction could reveal which circuit was called" as an open question but does not explain what "segments" are in the ZKIR model. Readers need a brief definition or a forward pointer to ch05-midnight-s-zkir-a-concrete-layer-4.

## Links

- Up: [[04-the-secret-performance]]
- Prev: [[ch04-witness-constraint-divergence]]
- Next: [[ch04-the-witness-as-a-multi-dimensional-problem]]
