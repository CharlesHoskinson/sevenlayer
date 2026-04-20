---
title: "When the Transcript Lies: Fiat-Shamir Vulnerabilities"
slug: ch08-when-the-transcript-lies-fiat-shamir-vulnerabilities
chapter: 8
chapter_title: "Layer 7 -- The Verdict"
heading_level: 2
source_lines: [3642, 3692]
source_commit: 5128bf4915b60448d50f9712ef2a308ac9d40765
status: reviewed
word_count: 891
---

## When the Transcript Lies: Fiat-Shamir Vulnerabilities

Chapter 6 introduced the Fiat-Shamir transform as the mechanism that seals Layer 5 proofs into non-interactive certificates, and flagged the binding requirement: the hash must include every public value the verifier would have seen. This section examines what happens when that requirement is violated in production -- and why the consequences are uniquely catastrophic at Layer 7, where on-chain verifiers are permissionless and exploitation is automated.

The Fiat-Shamir heuristic is the mechanism that converts an interactive proof (where the verifier asks random questions in real time) into a non-interactive one (where the prover simulates the verifier's questions using a hash function). Every non-interactive ZK proof deployed on a blockchain uses Fiat-Shamir. It is the invisible thread that holds the entire verification model together.

And it is the single most dangerous implementation surface in the entire stack.

### Frozen Heart (2022)

In April 2022, Trail of Bits disclosed a vulnerability class they called "Frozen Heart" (a backronym: Forging Of Zero kNowledge proofs). The error was simple. Devastatingly simple. Multiple independent implementations of ZK proof systems omitted public inputs from the Fiat-Shamir hash computation.

The implementations affected were not obscure academic prototypes. They were production-grade libraries used by real projects:

- **Dusk Network** (PLONK implementation)
- **Iden3/SnarkJS** (Groth16, used by Circom)
- **ConsenSys/gnark** (PLONK implementation)
- **ING Bank's zkrp** (Bulletproofs)
- **SECBIT Labs' ckb-zkp** (Groth16)
- **Adjoint Inc.'s bulletproofs** (Bulletproofs)

Six implementations. Three different proof systems. Four different organizations. All made the same mistake: they left the public inputs out of the hash that generates the verifier's challenges.

The consequence is total soundness failure. A malicious prover can forge proofs for *arbitrary false statements*. Not with some small probability. With certainty. The "proof" passes verification because the challenges are no longer bound to the specific statement being proved. The sealed certificate attests to nothing. It is wax without an impression.

The rule that was violated is not subtle: the Fiat-Shamir hash must include *all* public values from the ZK statement and *all* public values computed during the proof. Every commitment, every public input, every piece of data that the verifier would have seen in the interactive version must go into the hash. Omit any of it, and the binding between challenge and statement dissolves.

### The Last Challenge Attack (2024)

The Last Challenge Attack, discovered during an audit of Linea's PLONK verifier in the gnark library, is a more surgical variant of the same disease. In KZG-based proof systems, the verifier often batches multiple polynomial evaluations using a random "batching challenge" derived via Fiat-Shamir. The Last Challenge Attack exploits the case where this batching challenge is computed from a *truncated* transcript -- one that excludes the evaluation proofs themselves.

The attack is elegant in the way that a perfectly executed heist is elegant. The malicious prover sets arbitrary (false) public inputs and proof components, computes the batching challenge from the truncated transcript, then solves a linear system for the missing evaluation proofs. The vulnerable verifier accepts the forged proof with probability 1.

Not "with high probability." With certainty. The forged proof is deterministically constructed to pass verification. The audience has been compromised not by force but by omission -- a single value left out of a hash, and the entire edifice of mathematical certainty collapses.

The gnark advisory (GHSA-7p92-x423-vwj6) confirmed the vulnerability. The fix was straightforward: compute the batching challenge only *after* all evaluation proofs are included in the transcript. But the vulnerability existed in a production-quality library used by multiple rollup teams.

### Solana ZK ElGamal (2025)

The pattern repeated in early 2025 on Solana, where the ZK ElGamal implementation -- used for confidential token transfers -- was found to have a Fiat-Shamir transcript that omitted the prover's challenge from the hash computation. The omission meant that an attacker could construct a proof of a false statement (for example, that a transfer of zero tokens was actually a transfer of a million tokens) and the on-chain verifier would accept it. The fix, as with Frozen Heart and the Last Challenge Attack, was to include the missing value in the transcript hash. Same class of error. Same catastrophic consequence. Same one-line fix. The same lesson, unlearned for the third time.

### The Pattern

These are not isolated incidents. They are symptoms of a structural problem: the Fiat-Shamir heuristic is easy to describe ("hash everything the verifier would see") and remarkably easy to get wrong in implementation. The specification says "include all public values." The implementation omits one, because it seemed redundant, or because it made the code cleaner, or because the developer did not understand *why* it needed to be there.

For on-chain verifiers, this class of vulnerability is uniquely dangerous. An on-chain verifier is permissionless -- anyone can submit a proof. If the verifier's Fiat-Shamir transcript is incomplete, exploitation is automated and instantaneous. There is no human in the loop to notice that something looks wrong. The forged proof passes the smart contract's checks, the state transition is accepted, and the attacker drains whatever value the rollup is protecting.

Every on-chain SNARK verifier -- Groth16, PLONK, FFLONK, any KZG-based scheme -- must be audited specifically and primarily for Fiat-Shamir transcript completeness. This should be the first check in any security review, not an item buried in a general audit report.

---


## Summary

Omitting public inputs from the Fiat-Shamir hash causes total soundness failure: a malicious prover can forge proofs for arbitrary false statements with certainty. Three independent incidents (Frozen Heart 2022, Last Challenge Attack 2024, Solana ZK ElGamal 2025) hit different systems but share an identical root cause, making Fiat-Shamir transcript completeness the first-order audit check for every on-chain SNARK verifier.

## Key claims

- The Fiat-Shamir heuristic converts interactive proofs to non-interactive; every blockchain ZK proof uses it.
- Frozen Heart (April 2022): six production implementations across three proof systems (PLONK, Groth16, Bulletproofs) omitted public inputs from the hash — total soundness failure in all cases.
- Affected libraries: Dusk Network (PLONK), Iden3/SnarkJS (Groth16), ConsenSys/gnark (PLONK), ING Bank zkrp (Bulletproofs), SECBIT Labs ckb-zkp (Groth16), Adjoint Inc. bulletproofs.
- Last Challenge Attack (2024): gnark's KZG batching challenge computed from a truncated transcript; attacker solves a linear system to forge proof with probability 1. (gnark advisory GHSA-7p92-x423-vwj6)
- Solana ZK ElGamal (2025): prover's challenge omitted from transcript hash; zero-token transfer provable as million-token transfer.
- On-chain verifiers are permissionless — exploitation is automated and instantaneous with no human review loop.

## Entities

- [[fiat-shamir]]
- [[groth16]]
- [[plonk]]
- [[kzg]]
- [[bulletproofs]]

## Dependencies

- [[ch06-fiat-shamir-vulnerabilities]] — earlier treatment of the transform mechanism
- [[ch08-the-social-layer]] — Layer 7 framing; implementation bugs are one of four concerns
- [[ch08-who-verifies-the-verifier]] — supply-chain attack surface including library bugs
- [[ch08-on-chain-verification-in-2026]] — current audit posture

## Sources cited

- Trail of Bits, "Frozen Heart" disclosure (April 2022)
- gnark advisory GHSA-7p92-x423-vwj6 (Last Challenge Attack, 2024)
- Solana ZK ElGamal vulnerability report (early 2025)

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [none] X — no issues found.

## Links

- Up: [[08-the-verdict]]
- Prev: [[ch08-the-price-of-a-verdict]]
- Next: [[ch08-governance-the-achilles-heel]]
