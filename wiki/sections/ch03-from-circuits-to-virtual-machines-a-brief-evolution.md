---
title: "From Circuits to Virtual Machines: A Brief Evolution"
slug: ch03-from-circuits-to-virtual-machines-a-brief-evolution
chapter: 3
chapter_title: "Choreographing the Act"
heading_level: 2
source_lines: [801, 826]
source_commit: c9e43022aec66b2d2daf6a69767a4389b8d854c8
status: reviewed
word_count: 575
---

## From Circuits to Virtual Machines: A Brief Evolution

To understand where we are, we need to understand where we came from.

The first generation of zero-knowledge programming looked nothing like programming. In 2018, if you wanted to prove a computation in zero knowledge, you wrote *circuits* -- not programs, but direct descriptions of mathematical relationships. The dominant tool was Circom, a domain-specific language created by Jordi Baylina and the iden3 team. In Circom, you did not write `if balance >= amount then approve`. You wrote constraint templates: mathematical equations that the proof system would verify. The developer was simultaneously writing two programs in one file -- one that computed the witness (the private data), and one that generated the constraints (the mathematical rules). These two programs had to agree perfectly on every input. When they did not, the result was an under-constrained circuit: a proof system that would certify false statements as true.

Imagine asking a playwright to write both the script and the stage directions in a single document, using two different notations that had to be perfectly synchronized, with no compiler to check whether they matched. That is what early ZK development felt like.

Circom was powerful. It gave developers complete control over the constraint system. But that control came at a cost. Chaliasos et al., in "SoK: What Don't We Know? Understanding Security Vulnerabilities in SNARKs" (USENIX Security 2024), catalogued the scale of the problem: 95 of 141 real-world vulnerabilities were under-constrained circuits -- the epidemic described at the opening of this chapter. The Tornado Cash bug was a single character: `=` where `<==` was needed. One character. Complete soundness break. A malicious prover could generate proofs for false statements, and the verifier would accept them.

The second generation asked a different question: what if the developer never saw the constraints at all? What if they wrote a program in a language they already knew, and a compiler handled the translation to mathematics?

Cairo, created by StarkWare in 2021, pioneered this approach. Cairo defined a new instruction set architecture -- a virtual CPU designed from the ground up so that every instruction's execution could be efficiently encoded as polynomial constraints. The developer wrote programs. The compiler generated constraints. The proof system verified the constraints. The developer never touched a mathematical equation.

Cairo settled on the so-called Stark prime -- $p = 2^{251} + 17 \cdot 2^{192} + 1$ -- a 252-bit field chosen to hold elliptic-curve scalars natively. This was a *large-field* STARK. A later wave of provers went the other way: *small-field* STARKs working over 64-bit Goldilocks ($2^{64} - 2^{32} + 1$), 31-bit BabyBear, or Mersenne-31 (M31). Goldilocks arrived with Plonky2, moved through Plonky3, and now underpins RISC Zero; BabyBear and M31 power SP1 and Stwo respectively. The arithmetic shrank because the hardware did not: 32-bit integer multiply is a native CPU instruction, and small-field STARKs exploit that fact. Cairo was the large-field template. Goldilocks-class provers are the small-field descendants.

But Cairo required learning a new language, a new toolchain, a new way of thinking about computation. The programs you had already written -- in Rust, in C++, in Python -- could not run on Cairo. You had to rewrite everything.

The third generation asked the obvious follow-up: what if we proved a processor that developers already targeted? What if the instruction set was not some exotic ZK-native design, but plain RISC-V -- the open standard that Rust, C, and C++ compilers already produce code for?

This is the generation we live in now. SP1 (Succinct), RISC Zero, Airbender (ZKsync), ZisK (the team formerly known as Polygon Hermez), Jolt, and Pico Prism all prove RISC-V execution. The developer writes standard Rust. The compiler targets standard RISC-V. The proof system proves the execution trace. The developer may never know they are working with zero-knowledge proofs at all.

But this triumphant narrative -- circuits to custom VMs to RISC-V -- leaves out a fourth thread. There is another approach, one that does not fit the evolutionary story. It does not prove a processor at all. It proves *state transitions*. And its compiler does something no instruction-set-based approach can do: it prevents privacy leaks at compile time.

---


## Summary

ZK programming evolved in three generations: hand-written Circom circuits (2018), ZK-native ISAs like Cairo (2021), and RISC-V-targeting zkVMs (present). Each generation hid more mathematical detail from the developer, but a fourth thread — application-specific DSLs that prove state transitions and enforce privacy at compile time — does not fit the linear story.

## Key claims

- First generation (Circom, ~2018): developer writes dual-track code — witness computation and constraints in one file; 95 of 141 catalogued vulnerabilities were under-constrained circuits (Chaliasos SoK).
- Tornado Cash exploit: one character (`=` instead of `<==`) caused a complete soundness break.
- Second generation (Cairo, 2021): compiler hides constraints; developer writes programs, not equations.
- Third generation (SP1, RISC Zero, Airbender, ZisK, Pico Prism): prove standard RISC-V execution; developer writes plain Rust.
- A fourth, non-evolutionary thread proves state transitions and enforces privacy at compile time.

## Entities

- [[airbender]]
- [[pico]]
- [[polygon]]
- [[prism]]
- [[tornado cash]]
- [[zisk]]

## Dependencies

- [[ch03-risc-v-won-why-taxonomy-still-matters]] — frames why language choice matters despite RISC-V convergence
- [[ch03-the-four-philosophies]] — expands the four-philosophy taxonomy sketched here
- [[ch03-under-constrained-circuits-the-dominant-failure-mode]] — quantifies the Circom vulnerability epidemic referenced here

## Sources cited

- Chaliasos SoK: 95 of 141 catalogued vulnerabilities were under-constrained circuits.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [P2] (A) Cairo's creation date is given as 2021; the Cairo whitepaper appeared in late 2021 but an earlier prototype shipped in 2020. "Created by StarkWare in 2021" may be defensible but should be qualified as the public/whitepaper release date.
- [P2] (C) "Imagine asking a playwright to write both the script and the stage directions in a single document…" — the theater metaphor is used heavily in chapter 1; its reuse here without advancement adds padding rather than insight.
- [P2] (D) The Tornado Cash bug description ("The witness generator computed the correct value. The constraint system did not enforce it") is correct here, but `ch03-under-constrained-circuits` describes the same bug in more detail. The two accounts should agree on framing; currently section 2 says "one character" while section 5 also says "one character" — consistent, but the duplication of the anecdote across two sections is unnecessary.
- [P3] (E) No mention of Circom's successor tools (Circom 2, circom-plus) or how the field has responded since 2018; the evolution narrative stops at the third generation without noting ongoing Circom development.

## Links

- Up: [[03-choreographing-the-act]]
- Prev: [[ch03-risc-v-won-why-taxonomy-still-matters]]
- Next: [[ch03-the-four-philosophies]]
