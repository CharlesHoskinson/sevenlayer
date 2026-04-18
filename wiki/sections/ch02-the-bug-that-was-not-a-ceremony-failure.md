---
title: "The Bug That Was Not a Ceremony Failure"
slug: ch02-the-bug-that-was-not-a-ceremony-failure
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [604, 616]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 350
---

## The Bug That Was Not a Ceremony Failure

In 2019, a vulnerability designated CVE-2019-7167 surfaced in the BCTV14 construction used by Zcash [BCTV14]. The bug was devastating: it would have allowed unlimited counterfeiting of Zcash tokens. And it had nothing to do with the trusted setup ceremony.

The flaw lived in the cryptographic construction itself. The BCTV14 protocol's SRS included additional group elements beyond what the proof system strictly needed. These extra elements were included for generality, but they created an opening: an attacker could combine them to produce forged proofs for statements outside the intended circuit. Specifically, the attacker could craft a proof that would pass verification even though the underlying computation was never performed. The counterfeiting was not approximate. It was exact. Forged proofs would be indistinguishable from legitimate ones.

The vulnerability had existed for roughly three years, from the system's deployment in 2016 until its discovery in early 2019. During that time, the mathematical security proof in the original BCTV14 paper had a gap -- a step in the argument that assumed something about the SRS elements that was not, in fact, guaranteed. The Zcash ceremony could have been conducted perfectly -- every participant honest, every piece of toxic waste destroyed -- and the system would still have been vulnerable, because the construction itself was flawed.

This case study carries a lesson that extends far beyond Layer 1: *ceremony integrity is necessary but not sufficient*. You can build a perfect stage and still get the show wrong. The construction must be correct independently of the ceremony. Security is not a chain where one strong link compensates for a weak one. It is a conjunction: every link must hold simultaneously.

Sean Bowe and Ariel Gabizon discovered the bug before anyone exploited it. The team deployed a fix transparently. But the episode foreshadows a pattern that Chapter 3 will document in detail: 67% of real-world zero-knowledge vulnerabilities are not in the ceremony or the cryptography. They are in the mathematical specification -- the script, not the stage. The BCTV14 bug is the first concrete example of that statistic.



## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
