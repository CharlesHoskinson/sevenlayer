---
title: "The Seven Layers at a Glance"
slug: ch01-the-seven-layers-at-a-glance
chapter: 1
chapter_title: "The Promise of Provable and Programmable Secrets"
heading_level: 2
source_lines: [280, 306]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 799
---

## The Seven Layers at a Glance

Every zero-knowledge system, from the simplest proof to the most complex rollup, decomposes into seven layers. These are not independent floors in a building. They are organs in a body -- deeply interdependent, each shaping what the others can do.

**Layer 1 -- The Setup (Building the Stage).** Before the magician can perform, someone must construct the mathematical parameters that make proving and verifying possible -- and who builds them, and whether you must trust them, determines the system's deepest guarantees. You will meet the 141,416 people who built the most widely used stage, and ask what happens if none of them were honest.

**Layer 2 -- The Language (Writing the Script).** The magician needs a script: a programming language in which to express the computation she wants to prove. Her choice of language determines what bugs she can make and what assurances the compiler can enforce. You will see how a single missing character -- one `=` sign -- broke Tornado Cash's entire soundness guarantee.

**Layer 3 -- The Witness (The Secret Backstage Preparation).** The magician goes backstage to run the computation with her private data, recording every step in an execution trace that no one else will ever see. This preparation, not the proof itself, is the most underestimated bottleneck in the entire stack. You will learn why a stopwatch held to a Zcash prover revealed the transaction amounts the mathematics promised to hide.

The first three layers are about *preparation* -- building the stage, writing the script, rehearsing backstage. The next two are about *transformation* -- converting human-readable computation into something mathematics can verify. The final two are about *foundations and consequences* -- the cryptographic bedrock the system rests on and the real-world stage where the proof faces its audience. This three-act structure mirrors the workflow of every team that builds a ZK system: design, encode, deploy.

**Layer 4 -- The Arithmetization (Encoding the Performance).** The backstage recording is transformed into a system of polynomial equations -- formulas built from addition and multiplication, like $3x^2 + 5x + 7$. Polynomials can encode complex rules compactly, and they have a mathematical property that makes cheating almost impossible to hide. The result is a puzzle that can be checked in seconds, even though solving it took hours. You will watch our 4x4 Sudoku become 72 polynomial constraints and discover why each constraint must hold at every point in a million-element field.

**Layer 5 -- The Proof System (Sealing the Certificate).** The magician compresses the entire puzzle into a compact, tamper-proof certificate using cryptographic machinery that guarantees soundness and zero-knowledge simultaneously. You will compare the two dominant families -- SNARKs and STARKs -- and see why a 192-byte proof and a 200-kilobyte proof can both be "succinct."

**Layer 6 -- The Cryptographic Bedrock.** Beneath the proof system lie the fundamental building blocks: elliptic curves, hash functions, and polynomial commitment schemes (methods for sealing a polynomial into a tamper-proof envelope). Their mathematical hardness assumptions are the bedrock on which everything above rests. You will confront the expiration date that quantum computers stamp on half of modern cryptography, and meet the lattice-based replacements racing to arrive in time.

**Layer 7 -- The Verification (The Audience's Verdict).** The audience checks the proof on a public stage -- a blockchain, a smart contract, a verifier endpoint -- and the economics, governance, and data availability of that stage determine whether the trick actually matters outside mathematics. You will watch a governance attack exploit a system whose code worked exactly as designed.

If you have ever wondered why ZK proofs cost what they cost, why some systems require elaborate ceremonies and others do not, or why a quantum computer threatens certain proof systems but not others -- these seven layers are where the answers live. Each chapter that follows unpacks one layer.

A warning: the dependencies between layers do not follow the numbering. The choice of cryptographic primitive (Layer 6) determines which proof systems are available (Layer 5). That determines which arithmetizations work (Layer 4). That shapes which languages are efficient (Layer 2). That constrains the setup (Layer 1). A single decision -- choosing a small, fast number system (the Goldilocks field) over a large, secure one (BLS12-381) -- can cascade through all seven layers and reshape the entire architecture.

In practice, some layers fuse. Jolt merges witness generation and arithmetization into a single lookup step. Cairo co-designs its language around its constraint system. Layers 4, 5, and 6 -- the "proof core" -- behave as one inseparable design unit in every production system. By Chapter 10, the model will be redrawn in its honest final form: a directed acyclic graph with fourteen causal edges, not seven tidy floors. The map is provisional. The territory is more tangled.



## Summary

Every zero-knowledge system decomposes into seven interdependent layers — setup, language, witness, arithmetization, proof system, cryptographic bedrock, and verification — whose dependencies do not follow their numbering. A single field choice (e.g., Goldilocks vs. BLS12-381) cascades through all seven. The seven-layer stack is a provisional map; by Chapter 10 it is redrawn as a DAG with fourteen causal edges.

## Key claims

- The seven layers are organs in a body, not independent floors — deeply interdependent.
- Layer 1 (setup): 141,416 participants built Ethereum's KZG stage; any one honest participant suffices for security.
- Layer 2 (language): a single missing `=` sign broke Tornado Cash's soundness.
- Layer 3 (witness): a stopwatch held to Zcash's Groth16 prover revealed transaction amounts.
- Layers 4–5 transform human-readable computation into polynomial equations; a 4×4 Sudoku becomes 72 polynomial constraints.
- A 192-byte SNARK proof and a 200-kilobyte STARK proof are both "succinct."
- Layer 6 choices (field, curve) cascade: choosing Goldilocks over BLS12-381 reshapes all seven layers.
- Jolt merges witness generation and arithmetization; Cairo co-designs language and constraint system — layers 4, 5, and 6 behave as one design unit in every production system.
- The final model (Chapter 10) has fourteen causal edges, not seven tidy floors.

## Entities

- [[arithmetization]]
- [[goldilocks]]
- [[jolt]]
- [[lattice]]
- [[starks]]
- [[sudoku]]
- [[tornado cash]]
- [[zcash]]

## Dependencies

- [[ch01-the-trick]] — the prover/verifier framing that motivates why layers exist
- [[ch01-the-phenomenon]] — SNARK/STARK distinction and succinct proof sizes introduced there
- [[ceremony]] — trusted-setup concept (Layer 1) referenced directly

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [P1] (A) "Layer 2 — a single `=` sign broke Tornado Cash's entire soundness guarantee" — the Tornado Cash bug involved using `=` (JavaScript assignment in a Circom template) where `<==` (constrained assignment) was needed, but calling it a single "missing `=` sign" is imprecise; it was an operator substitution (`=` for `<==`), not a missing character. The ch03 section correctly describes it; ch01 should match.
- [P1] (D) The "141,416" participant count is stated here as Layer 1 context but the chapter elsewhere (ch01-the-deepest-question, ch01-the-first-decision) attributes the same number to the Ethereum KZG ceremony and to Zcash's ceremony separately in ways that could confuse. Confirm every instance consistently refers to KZG 2023, not the Zcash Sprout ceremony (6 participants) or Sapling (~90 participants).
- [P2] (A) "A stopwatch held to a Zcash prover revealed the transaction amounts" — ch04-side-channel confirms the attack correlated proof-generation time with Hamming weight, allowing *estimation* of amounts; saying it "revealed" the amounts overstates the attack's precision (R = 0.57, not 1.0). Soften to "allowed inference of" or "correlated with."
- [P2] (C) The three-act structural description ("preparation … transformation … foundations and consequences") has a slightly formulaic, outline-style quality that interrupts the flow mid-section; integrating it as a transitional sentence rather than a standalone paragraph would read better.
- [P2] (E) Layer 6 description mentions quantum threat but does not name the specific hardness assumptions at stake (discrete log, hash collision resistance); the Entities list includes `[[lattice]]` but the body does not mention lattices, leaving the entity tag unanchored.
- [P3] (E) The DAG with "fourteen causal edges" is promised for Chapter 10 but no preview of what those edges represent is given; a one-sentence hint would build anticipation more concretely.

## Links

- Up: [[01-the-promise-of-provable-and-programmable-secrets]]
- Prev: [[ch01-three-converging-forces]]
- Next: [[ch01-the-deepest-question]]
