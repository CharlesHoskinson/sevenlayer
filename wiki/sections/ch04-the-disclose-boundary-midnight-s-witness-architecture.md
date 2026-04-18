---
title: "The `disclose()` Boundary: Midnight's Witness Architecture"
slug: ch04-the-disclose-boundary-midnight-s-witness-architecture
chapter: 4
chapter_title: "The Secret Performance"
heading_level: 2
source_lines: [1500, 1561]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
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

3. `walletProvider.balanceTx()` binds the transaction, runs token balancing (unshielded, shielded, and dust), signs UTXO inputs with BIP-340 Schnorr signatures, and merges the balancing transaction with the original.

4. `midnightProvider.submitTx()` submits to the blockchain, where the node verifies the ZK proof, checks that the public transcript matches the ledger state, and applies the state transition.

At no point do witnesses cross the network. The developer guide states this explicitly: "Witnesses stay local. Never sent to chain."

The side-channel implications matter here. Proof generation takes a fixed amount of time regardless of witness values -- dominated by the cryptographic proving step, not the witness computation. This provides natural but unintentional timing uniformity: the fixed cost of proof generation drowns out any timing variation in witness computation. But the documentation does not address cache timing, network timing (when a user queries the indexer immediately before submitting a transaction, the timing correlation reveals which contract state they are acting on), or transaction structure analysis (the number of segments in a transaction could reveal which circuit was called).

Privacy on Midnight is genuine at the cryptographic level. It is unexamined at the implementation level. This is not a criticism unique to Midnight -- it applies to every privacy-preserving system in production. But it is worth noting that the same project that provides the most rigorous compile-time privacy guarantees (disclosure analysis) has the least documented runtime privacy analysis.

One accidental privacy benefit: the fixed cost of proof generation -- dominated by the PLONK proving step -- provides natural timing padding. Whether the witness contains a trivial secret or a complex multi-step computation, the proof generation time is approximately the same. An observer measuring transaction timing cannot easily distinguish between different witness computations. The padding is natural but not designed. A dedicated attacker measuring sub-second timing variations in the witness computation phase (which occurs before proof generation) might still extract information. But the 18-second proving step provides a large, fixed-duration buffer that dominates the total transaction time.

The developer guide's demonstration of the private voting dApp provides a concrete end-to-end example. The off-chain witness construction computes Poseidon hashes using the same `persistentHash` function available in both the Compact circuit and the JavaScript SDK. The voter provides their secret key, vote choice, Merkle sibling hash, and direction flag as witnesses. The circuit reconstructs the Merkle root from these witnesses and asserts it matches the on-chain root. The circuit also computes a nullifier -- `persistentHash([pad(32, "nullf:"), secret_key])` -- using domain separation so that the nullifier hash and the voter's attestation hash are cryptographically unlinkable. The nullifier is disclosed (it must appear on-chain to prevent double-voting), but it cannot be traced back to the voter's identity.

What the on-chain verifier sees per vote: a nullifier hash and updated vote tallies. What the verifier does not see: which voter, their exact identity, or which Merkle leaf they occupy. The privacy boundary is sharp, and it is enforced at every level: by the compiler (disclosure analysis), by the ZKIR checker (transcript integrity), and by the cryptographic construction (domain-separated hashing).

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
