---
title: "The Bug That Was Not a Ceremony Failure"
slug: ch02-the-bug-that-was-not-a-ceremony-failure
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [598, 610]
source_commit: 53f41415d307dcd4ed73d852dfd6aa97146e882f
status: reviewed
word_count: 350
---

## The Bug That Was Not a Ceremony Failure

In 2019, a vulnerability designated CVE-2019-7167 surfaced in the BCTV14 construction used by Zcash. The bug was devastating: it would have allowed unlimited counterfeiting of Zcash tokens. And it had nothing to do with the trusted setup ceremony.

The flaw lived in the cryptographic construction itself. The BCTV14 protocol's SRS included additional group elements beyond what the proof system strictly needed. These extra elements were included for generality, but they created an opening: an attacker could combine them to produce forged proofs for statements outside the intended circuit. Specifically, the attacker could craft a proof that would pass verification even though the underlying computation was never performed. The counterfeiting was not approximate. It was exact. Forged proofs would be indistinguishable from legitimate ones.

The vulnerability had existed for roughly three years, from the system's deployment in 2016 until its discovery in early 2019. During that time, the mathematical security proof in the original BCTV14 paper had a gap -- a step in the argument that assumed something about the SRS elements that was not, in fact, guaranteed. The Zcash ceremony could have been conducted perfectly -- every participant honest, every piece of toxic waste destroyed -- and the system would still have been vulnerable, because the construction itself was flawed.

This case study carries a lesson that extends far beyond Layer 1: *ceremony integrity is necessary but not sufficient*. You can build a perfect stage and still get the show wrong. The construction must be correct independently of the ceremony. Security is not a chain where one strong link compensates for a weak one. It is a conjunction: every link must hold simultaneously.

Sean Bowe, Ariel Gabizon, and Daira Hopwood discovered the bug before anyone exploited it, and disclosed it coordinated with the Zcash team [Electric Coin Company, "Zcash Counterfeiting Vulnerability Successfully Remediated," February 2019; CVE-2019-7167]. The team deployed a fix transparently. But the episode foreshadows a pattern that Chapter 3 will document in detail: 67% of real-world zero-knowledge vulnerabilities are not in the ceremony or the cryptography. They are in the mathematical specification -- the script, not the stage [Chaliasos et al., "SoK: What Don't We Know? Understanding Security Vulnerabilities in SNARKs," USENIX Security 2024]. The BCTV14 bug is the first concrete example of that statistic.



## Summary

CVE-2019-7167 in Zcash's BCTV14 construction allowed unlimited token counterfeiting despite a correctly conducted ceremony: the flaw was in the cryptographic specification, not the trusted setup. The extra SRS elements included for generality created an opening for forged proofs that would pass verification, exploitable from deployment in 2016 until discovery in early 2019. Ceremony integrity is necessary but not sufficient — the construction must be independently correct.

## Key claims

- CVE-2019-7167 would have allowed exact, undetectable counterfeiting of Zcash tokens.
- The vulnerability existed for approximately 3 years (2016–2019) before Sean Bowe and Ariel Gabizon discovered it.
- The flaw was in the BCTV14 mathematical specification: extra SRS elements allowed proof forgery outside the intended circuit.
- A perfect ceremony with all toxic waste destroyed would not have prevented this attack.
- 67% of real-world zero-knowledge vulnerabilities are in the mathematical specification, not the ceremony or cryptography.

## Entities

- [[ceremony]]
- [[gabizon]]
- [[groth16]]
- [[zcash]]

## Dependencies

- [[ch02-the-structured-reference-string]] — defines the SRS elements whose over-inclusion created the attack surface
- [[ch02-the-141-416-person-question]] — establishes that ceremony quality alone does not guarantee system security

## Sources cited

- BCTV14 construction (referenced as CVE-2019-7167)

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [none] (C) No AI-smell or style issues found.
- [none] (D) No structural contradictions found.

## Links

- Up: [[02-building-the-stage]]
- Prev: [[ch02-the-141-416-person-question]]
- Next: [[ch02-universal-versus-circuit-specific-setups]]
