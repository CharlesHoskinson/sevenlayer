---
title: "From Speed Race to Security Race"
slug: ch06-from-speed-race-to-security-race
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2953, 2964]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 285
---

## From Speed Race to Security Race

The story of Layer 5 over the last three years is a story of two races.

The first race was about speed. From 2022 to 2025, the question was: can you prove computation fast enough for it to matter? Can you prove an Ethereum block before the next block arrives? Can you bring the cost below a dollar, below a dime, below a penny? This race has been substantially won. Real-time proving is operational. Costs are in the single-digit cents. The hardware stack -- GPUs, SIMD, and potentially FPGAs and ASICs -- has been mobilized.

The second race is about security. The Ethereum Foundation's December 2025 announcement marked the pivot: the target shifted from "prove fast" to "prove with 128-bit provable security." This means not just believing the proof system is secure, but having a formal proof that a computationally bounded adversary cannot forge proofs with probability better than $2^{-128}$. It means formally verifying the implementation against the specification. It means accounting for the gap between the random oracle model (where Fiat-Shamir uses ideal hash functions) and reality (where Fiat-Shamir uses SHA-256 or Poseidon).

SP1 Hypercube's formal verification of all 62 RISC-V opcode constraints against the RISC-V Sail specification is a milestone in this second race. It demonstrates that production proof systems can achieve the level of formal rigor that was previously associated only with academic papers. But verifying opcodes is only the beginning. The full stack -- from the Fiat-Shamir transform through the polynomial commitment scheme through the field arithmetic -- must be verified end-to-end. This is a harder problem, and it is the one that will define Layer 5's trajectory over the next several years.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
