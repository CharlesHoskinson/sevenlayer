---
title: "Three Hardness Assumptions, Three Worlds"
slug: ch07-three-hardness-assumptions-three-worlds
chapter: 7
chapter_title: "Layer 6 -- The Deep Craft"
heading_level: 2
source_lines: [3019, 3056]
source_commit: b1af061f6d0ec9177d90a6358d9d31da9edfe0c5
status: reviewed
word_count: 945
---

## Three Hardness Assumptions, Three Worlds

Every cryptographic system rests on a *hardness assumption*: a belief that a specific mathematical problem cannot be solved efficiently. The entire security guarantee is conditional. "This proof system is sound" really means "this proof system is sound *assuming* that problem X is hard." If someone finds a fast algorithm for problem X, the security guarantee vanishes. Not slowly. Immediately.

There is a useful way to think about this. A hardness assumption is like a combination lock. Classical computers try every combination one at a time -- for a lock with a trillion trillion combinations, they will never finish. Quantum computers do not try faster. They exploit the lock's internal structure to narrow the possibilities. Shor's algorithm does exactly this to the discrete logarithm problem: it uses quantum interference to find the answer directly. The lock opens. For hash-based problems, quantum computers get a modest advantage but the lock still holds if you make it big enough. For lattice problems (Module-SIS), no one has found a quantum trick that exploits the lock's structure at all. The tumblers do not vibrate. The lock holds.

Three hardness assumptions dominate zero-knowledge cryptography. Each creates a different world of possibilities and constraints.

### The Discrete Logarithm Problem

The oldest and most widely deployed assumption. Given a number $g$ and a value $h = g^x$, find $x$. On ordinary computers, the best known algorithms require roughly $2^{128}$ operations for carefully chosen groups -- effectively impossible. This assumption powers all elliptic curve cryptography, which in turn powers KZG commitments, Groth16 proofs, PLONK, and every pairing-based SNARK.

The DLP (Discrete Logarithm Problem -- the mathematical puzzle of figuring out how many times a number was multiplied by itself to produce a given result, which is easy to state but very hard to solve) world offers deep algebraic richness. Elliptic curve groups have a bilinear pairing operation -- a special function that takes two curve points and produces an element in a "target group." This pairing is the engine behind KZG polynomial commitments, which produce constant-size proofs (a single curve point, about 48 bytes) and enable constant-time verification (one pairing check). Nothing else in cryptography achieves this combination of succinctness and speed.

The cost is existential. A quantum computer running Shor's algorithm solves the discrete logarithm problem in polynomial time. Not "might solve" -- *does solve*, given enough qubits. The DLP world has an expiration date. We do not know the day. But the clock is ticking, and the hands do not run backward.

### Collision-Resistant Hash Functions

A completely different kind of assumption. A hash function takes arbitrary input and produces a fixed-size output. "Collision resistance" means it is hard to find two different inputs that produce the same output. SHA-256, BLAKE3, and Poseidon are all collision-resistant hash functions (we believe).

The CRHF world is simpler and more conservative. Hash functions require no algebraic structure -- no groups, no pairings, no special number theory. This simplicity is both a strength (fewer assumptions to break) and a weakness (fewer mathematical tools to work with). FRI-based commitment schemes and STARKs live in this world. They are transparent (no trusted setup) and plausibly post-quantum, since hash functions are not broken by Shor's algorithm.

But "plausibly post-quantum" deserves scrutiny, and scrutiny reveals cracks. Grover's algorithm gives a quantum computer a quadratic speedup for brute-force search, halving the effective security level of hash preimage resistance: a 256-bit hash drops to 128-bit quantum security. More subtly, the BHT algorithm [Brassard, Høyer, Tapp, "Quantum cryptanalysis of hash and claw-free functions," LATIN 1998, LNCS 1380, pp. 163--169; arxiv quant-ph/9705002] can reduce collision resistance by a factor of three: SHA-256's 128-bit classical collision resistance becomes roughly 85-bit quantum collision resistance, though this attack requires impractical amounts of quantum random-access memory. And the FRI protocol's post-quantum security depends on the soundness of the Fiat-Shamir transform in the quantum random oracle model -- a reduction that is known but carries non-tight security bounds.

The honest statement is that hash-based systems *probably* survive quantum computers with appropriate parameter adjustments, but the unqualified claim that they are "post-quantum secure" gives false confidence. Intellectual honesty demands we say: this is not yet fully understood.

### Module-SIS (Module Short Integer Solution)

The newest and most mathematically demanding assumption. Given a matrix $M$ over a polynomial ring, find a short nonzero vector $z$ such that $M \cdot z = 0$. "Short" means the coefficients of $z$ are small. The best known algorithms (both classical and quantum) require exponential time for properly chosen parameters.

Module-SIS is the foundation of lattice-based cryptography -- the family that the post-quantum community has rallied around. NIST's post-quantum standards (FIPS 203, 204, and 205, published August 2024) are built on lattice problems. The assumption has been studied for over two decades, and no quantum algorithm significantly outperforms classical ones against it.

The lattice world offers a distinctive property: *module homomorphism*. An Ajtai commitment (the lattice analogue of a Pedersen commitment -- a Pedersen commitment is a cryptographic method for "sealing" a number using elliptic curve arithmetic, so the committed value can be verified later but cannot be changed after commitment) satisfies the equation $\rho \cdot \text{Com}(Z) = \text{Com}(\rho \cdot Z)$, where $\rho$ is a ring element. This is the algebraic structure that makes lattice-based folding schemes possible. It is weaker than what pairings provide (no bilinear map to a target group) but stronger than what hash functions provide (which have no algebraic structure at all).

The upshot is that lattice-based schemes occupy a useful middle ground: they have enough algebraic structure for folding and efficient composition, plus post-quantum security, plus transparent setup. Whether they can match the succinctness of pairing-based schemes is the open research question -- and the answer is converging toward "close enough."

---


## Summary

Three hardness assumptions underpin all ZK cryptography: DLP (powers all pairing-based SNARKs, broken by Shor's), collision-resistant hash functions (underpins STARKs/FRI, weakened but likely survivable by quantum computers with parameter adjustment), and Module-SIS (lattice-based, no known quantum advantage). Each assumption creates a distinct world of algebraic possibilities, performance trade-offs, and security lifespans.

## Key claims

- DLP provides bilinear pairings enabling constant-size KZG proofs, but Shor's algorithm breaks it in polynomial time given enough qubits.
- CRHF-based systems (FRI, STARKs) are "plausibly post-quantum" but not proven so; Grover halves security level and BHT reduces collision resistance to ~85-bit quantum security for SHA-256.
- FRI's post-quantum security depends on Fiat-Shamir soundness in the quantum random oracle model — valid but non-tight.
- Module-SIS hardness has been studied for over two decades with no quantum algorithm significantly outperforming classical ones.
- Lattice schemes occupy a middle ground: algebraic structure sufficient for folding, post-quantum security, transparent setup.
- NIST FIPS 203, 204, 205 (August 2024) standardize lattice-based primitives, validating Module-LWE/Module-SIS as the post-quantum foundation.

## Entities

- [[ajtai]]
- [[fiat-shamir]]
- [[fri]]
- [[groth16]]
- [[kzg]]
- [[lattice]]
- [[nist]]
- [[pedersen]]
- [[plonk]]
- [[poseidon]]

## Dependencies

- [[ch07-the-laws-that-break]] — introduces the framing motivating this taxonomy
- [[ch07-four-families-of-commitment-schemes]] — the concrete schemes built on these three worlds
- [[ch07-lattice-based-proving]] — deep dive on the Module-SIS world
- [[ch02-the-quantum-shelf-life]] — earlier discussion of quantum timelines

## Sources cited

- Brassard, Hoyer, Tapp (BHT algorithm) — quantum collision resistance reduction
- NIST FIPS 203, 204, 205 (August 2024) — post-quantum standards based on Module-LWE/Module-SIS

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P2] (A) "Grover's algorithm gives a quantum computer a quadratic speedup for brute-force search, halving the effective security level" — accurate for preimage resistance; the halving framing is slightly imprecise because Grover applies to search, not all hash security properties equally. The subsequent BHT discussion partially corrects this but the leading sentence could mislead.
- [P2] (A) BHT "roughly 85-bit quantum collision resistance" for SHA-256 — the BHT exponent is 2n/3; for n=256 that gives ~170-bit quantum security if QRAM is ignored, or the classical 128-bit bound if QRAM cost is folded in. The "85-bit" figure is non-standard and the parenthetical "(though this attack requires impractical amounts of quantum random-access memory)" partially negates the claim; clarify whether 85-bit is a realistic bound or a theoretical worst-case.
- [P3] (C) Parenthetical asides in the Module-SIS paragraph (two nested parentheticals explaining Pedersen commitments) create cluttered prose; the Pedersen aside could link to [[pedersen]] instead.

## Links

- Up: [[07-the-deep-craft]]
- Prev: [[ch07-the-laws-that-break]]
- Next: [[ch07-four-families-of-commitment-schemes]]
