---
title: "From Speed Race to Security Race"
slug: ch06-from-speed-race-to-security-race
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2973, 2984]
source_commit: 199f27399ce5c5a87123a37bf3c457a226778185
status: reviewed
word_count: 285
---

## From Speed Race to Security Race

The story of Layer 5 over the last three years is a story of two races.

The first race was about speed. From 2022 to 2025, the question was: can you prove computation fast enough for it to matter? Can you prove an Ethereum block before the next block arrives? Can you bring the cost below a dollar, below a dime, below a penny? This race has been substantially won. Real-time proving is operational. Costs are in the single-digit cents. The hardware stack -- GPUs, SIMD, and potentially FPGAs and ASICs -- has been mobilized.

The second race is about security. The Ethereum Foundation's December 2025 announcement marked the pivot: the target shifted from "prove fast" to "prove with 128-bit provable security." This means not just believing the proof system is secure, but having a formal proof that a computationally bounded adversary cannot forge proofs with probability better than $2^{-128}$. It means formally verifying the implementation against the specification. It means accounting for the gap between the random oracle model (where Fiat-Shamir uses ideal hash functions) and reality (where Fiat-Shamir uses SHA-256 or Poseidon).

SP1 Hypercube's formal verification of all 62 RISC-V opcode constraints against the RISC-V Sail specification is a milestone in this second race. It demonstrates that production proof systems can achieve the level of formal rigor that was previously associated only with academic papers. But verifying opcodes is only the beginning. The full stack -- from the Fiat-Shamir transform through the polynomial commitment scheme through the field arithmetic -- must be verified end-to-end. This is a harder problem, and it is the one that will define Layer 5's trajectory over the next several years.

---


## Summary

Layer 5's arc from 2022--2025 was the speed race: real-time Ethereum proving, costs to single-digit cents. The December 2025 Ethereum Foundation pivot marks the start of the security race: 128-bit provable security, formal verification of implementations end-to-end. SP1 Hypercube's 62-opcode formal verification is a milestone, but the full Fiat-Shamir→commitment→field arithmetic stack remains to be verified.

## Key claims

- Speed race (2022--2025): real-time proving achieved, costs in single-digit cents, hardware stack mobilized.
- Security race (2025 onward): Ethereum Foundation targets 128-bit provable security, formal implementation verification.
- SP1 Hypercube formally verified all 62 RISC-V opcodes against the RISC-V Sail specification -- current state of the art.
- Gap: random oracle model (Fiat-Shamir with ideal hash) vs. reality (SHA-256 / Poseidon) remains unformalized.
- Full end-to-end stack verification (Fiat-Shamir + commitment + field arithmetic) is the open challenge defining the next phase.

## Entities

- [[fiat-shamir]]
- [[poseidon]]

## Dependencies

- [[ch06-real-time-ethereum-proving]] — speed race benchmarks and Ethereum Foundation pivot establish context
- [[ch06-fiat-shamir-vulnerabilities]] — Fiat-Shamir gap is the specific security target named here
- [[ch06-the-post-quantum-horizon]] — PQ security is another dimension of the security race
- [[ch06-the-sealed-certificate]] — chapter closing section follows

## Sources cited

None in this section.

## Open questions

- Full end-to-end formal verification of the Layer 5 stack (Fiat-Shamir transform through field arithmetic) is explicitly flagged as the open problem defining the next several years.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P2] (E) Very short (285 words); the section largely restates conclusions from ch06-real-time-ethereum-proving without adding new content; either extend with the random oracle model gap (mentioned but not developed) or merge with ch06-real-time-ethereum-proving
- [P2] (B) No sources cited; the Ethereum Foundation December 2025 announcement should have a reference (blog post, EIP, or public statement)
- [P3] (C) "This is a harder problem, and it is the one that will define Layer 5's trajectory" — mild forward-prediction AI flourish; could be cut without loss

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-the-post-quantum-horizon]]
- Next: [[ch06-the-sealed-certificate]]
