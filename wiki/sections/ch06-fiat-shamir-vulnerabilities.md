---
title: "Fiat-Shamir Vulnerabilities"
slug: ch06-fiat-shamir-vulnerabilities
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2839, 2854]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 479
---

## Fiat-Shamir Vulnerabilities

Every proof system we have discussed relies on a technique called the Fiat-Shamir transform to convert an interactive protocol into a non-interactive one. In the interactive version, the verifier sends random challenges to the prover. In the non-interactive version, the prover generates the challenges by hashing the protocol's transcript -- all previous messages -- into pseudorandom values. This eliminates the need for the verifier to be online during proving.

The Fiat-Shamir transform is simple in principle but treacherous in practice. The transcript that gets hashed must include *everything* that the verifier would have seen in the interactive version. If the prover omits anything -- a public input, a commitment, a previous challenge -- then the resulting hash is not a faithful simulation of the interactive protocol, and soundness can break.

### Frozen Heart and Fiat-Shamir Vulnerabilities

Why does this matter at Layer 5 specifically? Because the Fiat-Shamir transform is the *binding* mechanism between prover and verifier. In the interactive version of any proof protocol, the verifier generates fresh random challenges that force the prover to commit before seeing what will be checked. The Fiat-Shamir transform replaces these live challenges with hash-derived challenges -- but only if the hash input includes *every* public value the verifier would have seen. The transcript is the contract between the two parties. Omit a single term, and the prover can retroactively choose commitments that satisfy whatever challenges arise. The mathematical proof of soundness assumes the transcript is complete. The implementation must deliver on that assumption, term by term, or the proof of soundness is vacated.

This is not a theoretical concern. The "Frozen Heart" vulnerability class, disclosed by Trail of Bits in 2022, affected six independent implementations across three proof systems. The "Last Challenge Attack" of 2024 compromised gnark's PLONK verifier, used by multiple Ethereum rollups. In early 2025, Solana's ZK ElGamal implementation repeated the pattern. Chapter 8 catalogs these incidents in forensic detail -- what was omitted, how the forgery was constructed, and what the governance implications are for on-chain verification. Here at Layer 5, the lesson is narrower but no less urgent: the gap between a proof system's mathematical specification and its implementation is where real-world attacks live.

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

- [P1] (B) Three vulnerability incidents cited as fact (Frozen Heart 2022, Last Challenge Attack 2024, Solana ZK ElGamal 2025) with no sources in the "Sources cited" section; Trail of Bits Frozen Heart disclosure and the gnark PLONK bug report should be cited
- [P2] (A) "Last Challenge Attack of 2024 compromised gnark's PLONK verifier, used by multiple Ethereum rollups" — the specific rollups affected are not named; either name them or soften to "at least one Ethereum rollup"
- [P3] (E) SP1 Hypercube's 62-opcode formal verification is mentioned as "state of the art" but without explaining what a formal verification of opcodes does and does not cover; a sentence distinguishing opcode-constraint verification from full Fiat-Shamir-to-field-arithmetic stack verification would help readers calibrate the claim

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-the-proof-core-why-layers-4-5-and-6-are-inseparable]]
- Next: [[ch06-case-study-midnight-s-sealed-certificate]]
