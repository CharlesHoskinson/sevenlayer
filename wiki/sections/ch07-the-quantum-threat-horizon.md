---
title: "The Quantum Threat Horizon"
slug: ch07-the-quantum-threat-horizon
chapter: 7
chapter_title: "Layer 6 -- The Deep Craft"
heading_level: 2
source_lines: [3229, 3278]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 640
---

## The Quantum Threat Horizon

The question is not whether quantum computers will break DLP-based cryptography. The question is when.

### What Shor's Algorithm Does

Shor's algorithm, published in 1994, solves the discrete logarithm problem in polynomial time on a quantum computer. Given $g$ and $h = g^x$, it finds $x$ using roughly $O(n^3)$ quantum gates, where $n$ is the bit length of the group order. For BLS12-381, this requires approximately 2,500 logical qubits. Each logical qubit requires thousands of physical qubits for error correction, meaning the actual hardware requirement is on the order of millions of physical qubits -- roughly three orders of magnitude beyond current devices, which have demonstrated only a few thousand physical qubits.

When a cryptographically relevant quantum computer (CRQC) exists, the consequences are immediate and total:

- Every KZG commitment ever published becomes forgeable.
- Every Groth16 proof ever verified becomes suspect.
- Every elliptic curve signature (including BLS signatures and ECDSA) breaks.
- Every Pedersen commitment loses its binding property.
- Every system built on pairing-based cryptography fails simultaneously.

The failure mode is not gradual degradation. It is a cliff. One day the lock holds. The next day every lock of that type, everywhere, opens at once.

### The Timeline

Estimates for when a CRQC will exist vary widely:

- **Optimistic (some industry forecasts, 2024):** "Q-Day" by 2030.
- **Conservative (academic consensus):** 2032-2035.
- **NIST IR 8547 (November 2024):** Recommends that all federal agencies deprecate pre-quantum cryptographic algorithms by 2035.

NIST's position is the most policy-relevant. In August 2024, NIST published three post-quantum cryptography standards: FIPS 203 (ML-KEM, a key encapsulation mechanism based on Module-LWE), FIPS 204 (ML-DSA, a digital signature based on Module-LWE), and FIPS 205 (SLH-DSA, a stateless hash-based signature). These are not draft standards or proposals -- they are finalized, mandatory standards for federal systems.

The IR 8547 guidance document sets a deadline: by 2035, federal systems must have migrated away from RSA, ECDSA, and all DLP-based cryptography. The reasoning is straightforward: if a CRQC arrives in 2035 and a migration takes 5-10 years, you need to start migrating now.

### The HNDL Threat

The most insidious quantum threat is not future code-breaking but present data collection. "Harvest Now, Decrypt Later" (HNDL) describes the strategy of recording encrypted communications today for decryption by future quantum computers. A Federal Reserve discussion paper (FEDS 2025-093) explicitly identified HNDL as a risk to financial infrastructure.

For zero-knowledge systems, the HNDL analogue is this: an adversary records all on-chain data -- commitments, proofs, public inputs -- today, waiting for a quantum computer to extract the underlying secrets. In a system like Zcash or Midnight, where commitments hide transaction amounts and sender/receiver identities, a future CRQC could retroactively de-anonymize the entire transaction history.

The concern is not theoretical. The blockchain is a permanent, public record. Nothing posted to Ethereum or any other blockchain can be deleted. Every BLS12-381 commitment, every BN254 proof, every elliptic curve public key is preserved forever, waiting. The data is patient. A quantum computer needs only to be built once.

### Deployed Systems at Risk

Any zero-knowledge system deployed today that relies on DLP-based cryptography faces a choice:

1. **Accept the expiration date.** Acknowledge that the system's security guarantees have a finite lifespan and plan accordingly. This is the pragmatic approach for systems that do not require long-term privacy (e.g., rollups where the transactions are already publicly visible).

2. **Migrate proactively.** Begin transitioning to post-quantum primitives before a CRQC exists. This is the only option for systems that provide long-term privacy guarantees (e.g., shielded transactions, confidential identity systems).

3. **Ignore the problem.** Hope that quantum computers take longer than expected, or that "crypto-agility" will allow a rapid migration when the time comes. This is the most common approach -- and the most dangerous, because "crypto-agility" in practice means "complete architectural redesign."

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
