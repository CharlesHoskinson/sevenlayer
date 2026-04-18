---
title: "Fiat-Shamir Vulnerabilities"
slug: ch06-fiat-shamir-vulnerabilities
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2824, 2839]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
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

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
