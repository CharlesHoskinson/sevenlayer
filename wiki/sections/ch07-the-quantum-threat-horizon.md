---
title: "The Quantum Threat Horizon"
slug: ch07-the-quantum-threat-horizon
chapter: 7
chapter_title: "Layer 6 -- The Deep Craft"
heading_level: 2
source_lines: [3248, 3297]
source_commit: b1af061f6d0ec9177d90a6358d9d31da9edfe0c5
status: reviewed
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

A cryptographically relevant quantum computer (CRQC) would simultaneously break every KZG commitment, Groth16 proof, elliptic curve signature, and Pedersen commitment ever published — not gradually but as a cliff event. The HNDL (Harvest Now, Decrypt Later) threat means on-chain data recorded today is vulnerable retroactively. NIST IR 8547 (November 2024) requires federal agencies to deprecate pre-quantum algorithms by 2035.

## Key claims

- Shor's algorithm requires ~2,500 logical qubits for BLS12-381; error correction means millions of physical qubits — ~3 orders of magnitude beyond current devices.
- When a CRQC exists: KZG forgeable, Groth16 suspect, all pairing-based systems fail simultaneously.
- Timeline estimates: optimistic "Q-Day" by 2030; academic consensus 2032–2035; NIST IR 8547 (November 2024) recommends federal migration complete by 2035.
- NIST published FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA) in August 2024 — finalized mandatory standards.
- HNDL: blockchain records are permanent and public; every BLS12-381 commitment and BN254 proof is preserved waiting for a future CRQC.
- Federal Reserve FEDS 2025-093 explicitly identified HNDL as a risk to financial infrastructure.
- Three response options: accept expiration, migrate proactively, or ignore — with "crypto-agility" being practically equivalent to "complete architectural redesign."

## Entities

- [[bls12-381]]
- [[bn254]]
- [[groth16]]
- [[kzg]]
- [[nist]]
- [[pedersen]]
- [[zcash]]

## Dependencies

- [[ch07-three-hardness-assumptions-three-worlds]] — Shor's impact on DLP explained there
- [[ch07-lattice-based-proving]] — the alternative being built against this threat
- [[ch07-the-one-way-door]] — why migration is not "crypto-agility" but full redesign
- [[ch02-the-quantum-shelf-life]] — earlier overview of quantum timeline and shelf-life framing

## Sources cited

- NIST IR 8547 (November 2024) — federal deprecation deadline 2035
- NIST FIPS 203, 204, 205 (August 2024) — finalized post-quantum standards
- Federal Reserve FEDS 2025-093 — HNDL risk to financial infrastructure

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P2] (A) "~2,500 logical qubits for BLS12-381" — Webber et al. (2022, "The impact of hardware specifications on reaching quantum advantage") estimated ~2,330 logical qubits for 256-bit elliptic curve; "~2,500" is a reasonable approximation but no citation is provided. The key claims repeat this figure without source.
- [P2] (A) "current devices, which have demonstrated only a few thousand physical qubits" — as of late 2024 IBM Condor reached 1,121 qubits and Google Willow 105 qubits; "a few thousand" overstates current state unless referring to planned near-term devices. Should say "low hundreds to low thousands" or cite specific device benchmarks.
- [P2] (B) Federal Reserve FEDS 2025-093 is cited for the HNDL claim but no title or URL is given; this is a specific government document that should have a full citation for verifiability.
- [P3] (C) The three-option framing (accept/migrate/ignore) uses "hope that…quantum computers take longer than expected" for option 3 — slightly editorializing; functional but could be stated more neutrally.

## Links

- Up: [[07-the-deep-craft]]
- Prev: [[ch07-small-fields]]
- Next: [[ch07-lattice-based-proving]]
