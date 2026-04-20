---
title: "The Structured Reference String"
slug: ch02-the-structured-reference-string
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [396, 420]
source_commit: 6e757843ed29aa50ce4558719452a86510ed0d20
status: finalized
word_count: 998
---

## The Structured Reference String

Before we discuss who builds the stage, we need to understand what it is.

A note on the arithmetic that underlies everything in this book. All numbers in a zero-knowledge system live in a *finite field* -- a set of numbers where arithmetic wraps around, like a clock. On a clock with 7 hours, 5 + 4 = 2, because 9 wraps past 7. Multiplication works the same way: 3 × 5 = 1, because 15 wraps to 1. This makes the mathematics compact enough to verify quickly. Every time you see "field element," "field arithmetic," or "field size" in the chapters that follow, this is what it means: clock arithmetic with a very large clock.

A *Structured Reference String* (SRS) is a list of specially constructed numbers. These numbers are points on an elliptic curve -- a type of mathematical curve with a remarkable property.

Picture a smooth curve drawn on a sheet of graph paper, defined by an equation like $y^2 = x^3 + ax + b$. Two points on this curve can be "added" together using a geometric rule: draw a straight line through the two points, find where the line intersects the curve a third time, and reflect that intersection across the horizontal axis. The result is a new point on the same curve. This operation is easy to perform -- draw the line, find the intersection, reflect. But *reversing* it is extraordinarily hard: given only the final point, there is no efficient way to figure out which two points were added to produce it, or how many times a point was added to itself. This asymmetry -- easy forward, impossible backward -- is the discrete logarithm problem, the mathematical one-way street on which most of modern cryptography depends.

The SRS exploits this asymmetry. It is a sequence of curve points, each derived from the previous one by a secret multiplication. Think of it as a ruler with very precise markings that everyone uses to measure, but that no one can reverse-engineer to discover how the markings were made. The markings let you measure certain things (verify polynomial evaluations). They do not let you reconstruct the manufacturing process (recover the secret value from the markings). The scheme that makes this possible was invented by Kate, Zaverucha, and Goldberg in 2010 [Kate, Zaverucha, Goldberg, "Constant-Size Commitments to Polynomials and Their Applications," *ASIACRYPT 2010*] and is universally known as KZG, after the authors' initials. KZG uses a special algebraic operation called a *bilinear pairing* -- a function that checks relationships between encrypted values without revealing them. Chapter 7 explains the mathematics in detail; for now: pairings let the verifier check polynomial identities without ever seeing the polynomial.

What does the SRS let a verifier *do*? A proof arrives. The verifier looks up the SRS (which is public), feeds the proof and the SRS into a verification equation, and checks whether the equation holds. The equation involves a pairing: a function that takes two curve points and produces a single number, with a property that preserves certain algebraic relationships between the inputs in the output. The verifier can check that two encrypted values are correctly related -- that the prover's computation was honest -- without ever seeing the values themselves. If the pairing check passes, the proof is valid. If it fails, someone cheated. The entire verification takes milliseconds.

The SRS itself is not a proof. It is shared infrastructure. A KZG opening proof -- a single commitment and a single opening -- is one $\mathbb{G}_1$ point, 48 bytes on BLS12-381. Groth16, a different proof system that also builds on the KZG-style SRS, produces proofs of three group elements (two in $\mathbb{G}_1$, one in $\mathbb{G}_2$), for a total of 192 bytes. PLONK produces proofs in the range of 800 bytes to a few kilobytes, depending on the variant. One stage, many performances. The SRS is the ruler. Each proof system chooses how much to write on it.

A *circuit* is the mathematical representation of the computation being proved -- the blueprint that specifies which arithmetic operations happen in what order. (Not an electrical circuit. A mathematical one. The term is borrowed from hardware design, where logic gates are wired together, because the structure is similar: inputs flow through operations to produce outputs.) The circuit is verified against the SRS. The Ethereum KZG SRS contains roughly 65 million curve points, stored as a file of several gigabytes -- roughly the size of a high-definition movie. That file is the stage. The scale -- 65 million points -- reflects the BN254 and BLS12-381 curve choices discussed in the later sections on BN254's eroding security margin. Every ZK rollup, every privacy protocol, every identity proof that uses KZG commitments performs its verification against those 65 million points.

The secret value used to generate the SRS is called the *trapdoor*. In the zero-knowledge community, it has acquired a more evocative name: *toxic waste*. The metaphor is precise. Like radioactive material, the trapdoor is dangerous if it persists and must be destroyed after it has served its purpose. If anyone -- anyone at all -- retains knowledge of the trapdoor, they can forge proofs of false statements. They can prove that $2 + 2 = 5$, that an empty bank account holds a billion dollars, that an invalid transaction is valid. No one would be able to tell the forged proof from a real one.

The SRS is the stage. The toxic waste is the spare key to the stage's trapdoor. And the ceremony is the manufacturing process designed to ensure that the spare key is destroyed.

The analogy to physical infrastructure is not casual. A traditional stage in a theater is inspected before every show -- you check the trapdoors, test the rigging, verify the load-bearing capacity of the catwalk. The SRS cannot be inspected in the same way, because you cannot test whether the toxic waste was destroyed without knowing it. You can verify that the SRS *has the right structure* -- that the points are consistent, that the powers-of-tau sequence is well-formed -- but you cannot verify that *nobody remembers the secret*. The structure is checkable. The secrecy is not. This is the fundamental tension of trusted setups, and it is the reason the field has invested enormous effort in both making ceremonies more trustworthy and building alternatives that require no ceremony at all.



## Summary

A Structured Reference String (SRS) is a sequence of elliptic curve points — each derived from a secret trapdoor via the KZG scheme — that acts as the public mathematical stage for all subsequent proofs. The trapdoor is called "toxic waste": if anyone retains it, they can forge arbitrary proofs, but the structure of the SRS can be verified without knowing the secret. Verifiers use bilinear pairings to check polynomial identities against the SRS in milliseconds, never seeing the underlying values.

## Key claims

- The SRS exploits the discrete logarithm problem: easy to step forward along an elliptic curve, impossible to reverse.
- The KZG scheme was invented by Kate, Zaverucha, and Goldberg in 2010.
- The Ethereum KZG SRS contains roughly 65 million curve points, stored as a several-gigabyte file.
- Proofs verified against the SRS are 192 bytes (three curve points) for Groth16.
- The SRS structure is publicly checkable; the secrecy of the trapdoor is not checkable — this is the fundamental tension of trusted setups.

## Entities

- [[kzg]]

## Dependencies

- [[ch02-the-fair-shuffle-problem]] — motivates why the SRS needs a ceremony
- [[ch02-two-ways-to-build-a-stage]] — the transparent alternative that needs no trapdoor

## Sources cited

- Kate, Zaverucha, Goldberg, 2010 (KZG polynomial commitment scheme)

## Open questions

None flagged by this section.

## Improvement notes

_All P0/P1/P2/P3 findings resolved in Phase 3 revisions (2026-04-18 through 2026-04-20)._

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [none] (D) No contradictions with other chapters found.

## Links

- Up: [[02-building-the-stage]]
- Prev: [[ch02-the-fair-shuffle-problem]]
- Next: [[ch02-two-ways-to-build-a-stage]]
