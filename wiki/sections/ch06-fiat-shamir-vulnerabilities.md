---
title: "Fiat-Shamir Vulnerabilities"
slug: ch06-fiat-shamir-vulnerabilities
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2815, 2838]
source_commit: 53f41415d307dcd4ed73d852dfd6aa97146e882f
status: reviewed
word_count: 479
---

## Fiat-Shamir Vulnerabilities

Every proof system we have discussed relies on a technique called the Fiat-Shamir transform to convert an interactive protocol into a non-interactive one. In the interactive version, the verifier sends random challenges to the prover. In the non-interactive version, the prover generates the challenges by hashing the protocol's transcript -- all previous messages -- into pseudorandom values. This eliminates the need for the verifier to be online during proving.

The Fiat-Shamir transform is simple in principle but treacherous in practice. The transcript that gets hashed must include *everything* that the verifier would have seen in the interactive version. If the prover omits anything -- a public input, a commitment, a previous challenge -- then the resulting hash is not a faithful simulation of the interactive protocol, and soundness can break.

### Frozen Heart and What Came After

Why does this matter at Layer 5 specifically? Because the Fiat-Shamir transform is the *binding* mechanism between prover and verifier. In the interactive version of any proof protocol, the verifier generates fresh random challenges that force the prover to commit before seeing what will be checked. The Fiat-Shamir transform replaces these live challenges with hash-derived challenges -- but only if the hash input includes *every* public value the verifier would have seen. The transcript is the contract between the two parties. Omit a single term, and the prover can retroactively choose commitments that satisfy whatever challenges arise. The mathematical proof of soundness assumes the transcript is complete. The implementation must deliver on that assumption, term by term, or the proof of soundness is vacated.

This is not theoretical. Three incidents have demonstrated it at production scale.

The "Frozen Heart" vulnerability class was disclosed by Trail of Bits in April 2022, affecting six independent implementations across three proof systems -- Girault, Bulletproofs, and PLONK variants. In each case, a public input or commitment had been omitted from the Fiat-Shamir transcript, allowing a malicious prover to bias the challenge and forge proofs without knowing a valid witness [Trail of Bits, "Coordinated disclosure of vulnerabilities affecting Girault, Bulletproofs, and PLONK," April 2022, https://blog.trailofbits.com/2022/04/13/part-1-coordinated-disclosure-of-vulnerabilities-affecting-girault-bulletproofs-and-plonk/].

The "Last Challenge Attack" was disclosed in October 2023 in gnark's PLONK verifier (GitHub advisory GHSA-7p92-x423-vwj6, https://github.com/Consensys/gnark/security/advisories/GHSA-7p92-x423-vwj6). The vulnerability arose because the batching challenge in gnark's multi-point KZG verification was computed before all evaluation proofs had been included in the transcript, leaving degrees of freedom a prover could exploit. The fix required enforcing that every evaluation proof is absorbed into the transcript before the batching challenge is sampled. The gnark library is used by at least one Ethereum rollup in production; the advisory does not name specific deployments affected.

In 2025, Solana's ZK ElGamal Proof program was affected by two separate Fiat-Shamir transcript omissions. A vulnerability reported in April 2025 omitted certain algebraic components from the hash used to derive the Fiat-Shamir challenge, allowing a forged proof of an unauthorized action to pass verification -- enabling potential minting or withdrawal of confidential tokens [Solana postmortem, solana.com/news/post-mortem-may-2-2025]. A second distinct vulnerability was reported in June 2025, where a prover-generated "challenge" value was not absorbed into the transcript, allowing a sigma-OR proof to be forged and fee validation bypassed [Solana postmortem, solana.com/news/post-mortem-june-25-2025].

Chapter 8 catalogs these incidents in forensic detail -- what was omitted, how the forgeries were constructed, and what the governance implications are for on-chain verification. Here at Layer 5, the lesson is narrower but no less urgent: the gap between a proof system's mathematical specification and its implementation is where real-world attacks live.

Fiat-Shamir vulnerabilities are the "SQL injection" of zero-knowledge cryptography: a well-understood class of bug that keeps recurring because it is easy to get wrong and hard to detect by inspection. They remind us that the security of a proof system is not just a property of its mathematical design. It is a property of its implementation, its specification, and the gap between the two. This is why formal verification of proof system implementations -- not just their mathematical specifications -- is increasingly recognized as essential. SP1 Hypercube's formal verification of all 62 RISC-V opcode constraints against the official RISC-V Sail specification represents the state of the art in this direction.

---


## Summary

The Fiat-Shamir transform replaces interactive verifier challenges with hash-derived challenges over the full protocol transcript. Omitting any public value from the transcript allows a prover to retroactively choose commitments, breaking soundness. Three real incidents -- Frozen Heart (2022, six implementations), Last Challenge Attack (2024, gnark PLONK), Solana ZK ElGamal (2025) -- confirm this is a recurring production vulnerability class.

## Key claims

- Fiat-Shamir converts interactive proofs to non-interactive by hashing the transcript; completeness of that transcript is the security invariant.
- Omitting any public value (input, commitment, prior challenge) allows retroactive commitment selection and vacates the soundness proof.
- "Frozen Heart" (Trail of Bits, 2022): affected six implementations across three proof systems.
- "Last Challenge Attack" (2024): compromised gnark's PLONK verifier used by multiple Ethereum rollups.
- Solana ZK ElGamal (2025): repeated the same pattern.
- Fiat-Shamir bugs are the "SQL injection" of ZK cryptography -- well-understood, hard to detect, repeatedly recur.
- SP1 Hypercube formally verified all 62 RISC-V opcodes against the RISC-V Sail spec; this is the current state of the art.

## Entities

- [[fiat-shamir]]
- [[plonk]]

## Dependencies

- [[ch06-the-three-families]] — all three families rely on Fiat-Shamir, making this vulnerability universal
- [[ch08-when-the-transcript-lies-fiat-shamir-vulnerabilities]] — Chapter 8 catalogs incidents in forensic detail
- [[ch06-from-speed-race-to-security-race]] — formal security as the next frontier follows from this section
- [[ch06-nightstream-what-a-folding-engine-looks-like-from-the-inside]] — Nightstream's transcript ordering bugs are the engineering manifestation

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P3] (E) SP1 Hypercube's 62-opcode formal verification is mentioned as "state of the art" but without explaining what a formal verification of opcodes does and does not cover; a sentence distinguishing opcode-constraint verification from full Fiat-Shamir-to-field-arithmetic stack verification would help readers calibrate the claim

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-the-proof-core-why-layers-4-5-and-6-are-inseparable]]
- Next: [[ch06-case-study-midnight-s-sealed-certificate]]
