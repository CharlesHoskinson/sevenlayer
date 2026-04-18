---
title: "From Circuits to Virtual Machines: A Brief Evolution"
slug: ch03-from-circuits-to-virtual-machines-a-brief-evolution
chapter: 3
chapter_title: "Choreographing the Act"
heading_level: 2
source_lines: [793, 816]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 575
---

## From Circuits to Virtual Machines: A Brief Evolution

To understand where we are, we need to understand where we came from.

The first generation of zero-knowledge programming looked nothing like programming. In 2018, if you wanted to prove a computation in zero knowledge, you wrote *circuits* -- not programs, but direct descriptions of mathematical relationships. The dominant tool was Circom, a domain-specific language created by Jordi Baylina and the iden3 team. In Circom, you did not write `if balance >= amount then approve`. You wrote constraint templates: mathematical equations that the proof system would verify. The developer was simultaneously writing two programs in one file -- one that computed the witness (the private data), and one that generated the constraints (the mathematical rules). These two programs had to agree perfectly on every input. When they did not, the result was an under-constrained circuit: a proof system that would certify false statements as true.

Imagine asking a playwright to write both the script and the stage directions in a single document, using two different notations that had to be perfectly synchronized, with no compiler to check whether they matched. That is what early ZK development felt like.

Circom was powerful. It gave developers complete control over the constraint system. But that control came at a cost. The Chaliasos SoK confirmed the scale of the problem: 95 of 141 catalogued vulnerabilities were under-constrained circuits -- the epidemic described at the opening of this chapter. The Tornado Cash bug was a single character: `=` where `<==` was needed. One character. Complete soundness break. A malicious prover could generate proofs for false statements, and the verifier would accept them.

The second generation asked a different question: what if the developer never saw the constraints at all? What if they wrote a program in a language they already knew, and a compiler handled the translation to mathematics?

Cairo, created by StarkWare in 2021, pioneered this approach. Cairo defined a new instruction set architecture -- a virtual CPU designed from the ground up so that every instruction's execution could be efficiently encoded as polynomial constraints. The developer wrote programs. The compiler generated constraints. The proof system verified the constraints. The developer never touched a mathematical equation.

But Cairo required learning a new language, a new toolchain, a new way of thinking about computation. The programs you had already written -- in Rust, in C++, in Python -- could not run on Cairo. You had to rewrite everything.

The third generation asked the obvious follow-up: what if we proved a processor that developers already targeted? What if the instruction set was not some exotic ZK-native design, but plain RISC-V -- the open standard that Rust, C, and C++ compilers already produce code for?

This is the generation we live in now. SP1 (Succinct), RISC Zero, Airbender (ZKsync), ZisK (the team formerly known as Polygon Hermez), and Pico Prism all prove RISC-V execution. The developer writes standard Rust. The compiler targets standard RISC-V. The proof system proves the execution trace. The developer may never know they are working with zero-knowledge proofs at all.

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

## Links

- Up: [[03-choreographing-the-act]]
- Prev: [[ch03-risc-v-won-why-taxonomy-still-matters]]
- Next: [[ch03-the-four-philosophies]]
