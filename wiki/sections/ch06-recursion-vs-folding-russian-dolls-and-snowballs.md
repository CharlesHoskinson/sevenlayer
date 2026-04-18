---
title: "Recursion vs. Folding: Russian Dolls and Snowballs"
slug: ch06-recursion-vs-folding-russian-dolls-and-snowballs
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2542, 2581]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 1078
---

## Recursion vs. Folding: Russian Dolls and Snowballs

Within any proof system architecture, there is a second design choice that matters just as much: how do you handle computation that happens in steps?

A blockchain processes blocks sequentially. A zkVM executes instructions one at a time. A rollup batches transactions and proves them in order. In every case, the prover needs to demonstrate not just "this single step is correct" but "every step from the beginning until now was correct." This is Incrementally Verifiable Computation (IVC), first formalized by Valiant in 2008, and it sits at the heart of how proof systems scale.

### Recursion: The Russian Doll

The first approach to IVC was recursive composition. The idea is deceptively simple: to prove that steps 1 through N are all correct, you prove step N is correct *and* that you have a valid proof that steps 1 through N-1 are correct. The verifier for steps 1 through N-1 is itself expressed as a circuit, and the proof for step N includes a verification of the previous proof.

Think of Russian nesting dolls. Each doll contains a smaller doll inside it, and that smaller doll contains an even smaller one. Opening the outermost doll and confirming it contains a properly formed inner doll gives you confidence in the entire chain. You never need to open all the dolls at once.

The problem is cost. The SNARK verifier is a complex circuit -- for pairing-based systems like Groth16, it involves millions of gates. Embedding a Groth16 verifier inside a Groth16 circuit means every step of computation must pay the cost of a full SNARK verification on top of the actual computation. Zexe (Bowe, Chiesa, Green, Miers, Mishra, Wu, 2018) demonstrated this approach using depth-2 recursion over a 2-chain of pairing-friendly curves, achieving constant-size 968-byte transactions regardless of offline computation. But the proving cost per step was enormous.

### Folding: The Snowball

In 2022, Abhiram Kothapalli, Srinath Setty, and Ioanna Tzialla published Nova, and the field changed direction overnight.

Nova introduced a fundamentally different approach: instead of proving each step and recursively verifying previous proofs, you *fold* two claims into one. Here is the intuition. In recursion, each step generates a complete proof, and the next step verifies it. In folding, each step generates a *claim* -- an incomplete, unverified assertion -- and combines it with the running claim from all previous steps. The combination is a random linear combination: the prover takes the two claims, the verifier picks a random challenge, and the prover produces a single new claim that is valid if and only if both original claims were valid. No full proof is ever generated during the accumulation phase. The certificate is not sealed along the way. Claims accumulate, and the expensive seal is deferred to the very end. Only when all steps have been folded together does the prover generate a single SNARK proof for the final accumulated claim.

The snowball analogy captures it precisely. Each new step is a handful of snow. Instead of building a separate snowman for each step (recursion), you pack the new snow onto the growing snowball (folding). The snowball gets slightly larger with each step, but you never have to build an entire snowman until the very end.

Nova's key technical insight was *relaxed R1CS*. This is where the mathematics earns its keep, and it is worth understanding why.

Standard R1CS says $Az \circ Bz = Cz$ (where $A$, $B$, $C$ are matrices and $z$ is the witness vector). Now suppose you try to combine two standard R1CS instances by taking a random linear combination: $(A(z_1 + r \cdot z_2)) \circ (B(z_1 + r \cdot z_2))$. When you expand this product, cross-terms appear -- terms involving both $z_1$ and $z_2$ multiplied together -- that do not fit the $Az \circ Bz = Cz$ format. The product of two linear combinations is quadratic, but R1CS demands bilinear structure. The cross-terms break the format.

This is the kind of obstacle that looks fatal until someone sees through it. Nova's insight was to relax the constraint. Instead of requiring $Az \circ Bz = Cz$ exactly, allow $Az \circ Bz = u \cdot Cz + E$, where $u$ is a scalar and $E$ is an error vector. When $u = 1$ and $E = 0$, you recover standard R1CS. But the relaxed form is closed under random linear combination: when you combine two relaxed instances, the cross-terms that would have destroyed the standard format are absorbed into the error vector E. The format survives. The scalar $u$ tracks the linear combination's coefficient, and $E$ accumulates the algebraic debris that would otherwise break the structure.

The folding verifier is tiny -- one scalar multiplication plus hashing, roughly 10,000 multiplication gates -- compared to millions for a full SNARK verifier. This is the breakthrough: fold cheaply at every step, prove expensively only once at the end. The per-step overhead of IVC dropped by orders of magnitude.

### The Snowball Does Not Fall Apart

The natural worry about the snowball analogy is: snowballs fall apart. What is the failure mode of folding?

The answer involves a subtlety that trips up even experienced cryptographers. Folding does not provide soundness on its own. It provides a *reduction*: if the folded claim is valid, then both original claims were valid (with overwhelming probability over the verifier's random challenge). But "valid" here means "satisfies the relaxed constraint system." The final proof -- the "decider" SNARK at the end of the chain -- is what provides soundness. If the underlying commitment scheme is binding and the random challenges are honestly generated, then a cheating prover cannot produce a valid folded claim for an invalid computation. The security proof works backward: a valid final claim implies all intermediate claims were valid, which implies all computation steps were correct.

The practical penalty comes from the size of the accumulated instance. In classical Nova, the error vector E grows with each folding step. The 10,000-gate figure for Nova's folding verifier is specifically the cost of the non-native scalar multiplication required when working over a 2-cycle of curves. CycleFold (Kothapalli and Setty, 2023) delegated this scalar multiplication to a co-processor circuit on the secondary curve, where it can be computed natively in approximately 1,500 gates. The folding verifier itself -- the hash and the random linear combination -- is much cheaper. But the fundamental architecture remains: fold cheaply, prove expensively but only once, at the end.

---


## Summary

Incrementally Verifiable Computation has two approaches: recursion (each step generates a proof verified by the next step -- Russian dolls) and folding (steps accumulate unverified claims via random linear combination, sealed by a single final decider -- a growing snowball). Nova's relaxed R1CS makes folding tractable: the per-step verifier costs ~10,000 gates vs. millions for full SNARK recursion.

## Key claims

- IVC was formalized by Valiant (2008); it is the mechanism behind zkVMs, rollups, and any multi-step computation proof.
- Recursive composition (Zexe, 2018) achieves constant 968-byte proofs but incurs full SNARK verifier cost (~millions of gates) per step.
- Nova (Kothapalli, Setty, Tzialla, 2022) introduced folding via relaxed R1CS: $Az \circ Bz = u \cdot Cz + E$, closed under random linear combinations.
- Folding verifier: ~10,000 gates (one scalar multiplication + hashing); full SNARK verifier: millions of gates.
- Folding defers the expensive proof ("decider") to the very end; claims accumulate cheaply at each step.
- CycleFold (Kothapalli and Setty, 2023) reduced the folding verifier's non-native scalar multiplication to ~1,500 gates.
- Folding alone does not provide soundness; the decider SNARK at the end of the chain does.

## Entities

- [[nova]]
- [[folding]]
- [[groth16]]

## Dependencies

- [[ch06-the-hybrid-pipeline]] — hybrid pipeline introduces recursion; this section explains the two strategies
- [[ch06-the-folding-genealogy]] — traces how Nova evolved into HyperNova, Neo, Symphony
- [[ch05-ccs-the-rosetta-stone]] — relaxed R1CS and CCS are explained in Chapter 5
- [[ch06-snark-recursion-vs-folding-the-full-picture]] — later section gives decision rules for choosing between them

## Sources cited

- Kothapalli, Setty, Tzialla, "Nova: Recursive Zero-Knowledge Arguments from Folding Schemes," CRYPTO 2022.
- Kothapalli, Setty, "CycleFold: Folding-scheme-based recursive arguments over a cycle of elliptic curves," ePrint 2023/1192.
- Bowe, Chiesa, Green, Miers, Mishra, Wu, "Zexe: Enabling Decentralized Private Computation," IEEE S&P 2020.

## Open questions

None flagged by this section.

## Improvement notes

- [P1] (A) Body text says Zexe "2018" but the sources section correctly lists "IEEE S&P 2020"; the ePrint date (2018) and the venue year (2020) are conflated — the body should say "Bowe et al. (S&P 2020)" or "introduced in a 2018 preprint, published S&P 2020"
- [P2] (C) "This is the kind of obstacle that looks fatal until someone sees through it" — AI smell (narrative flourish)
- [P2] (C) "It is worth understanding why" — AI smell
- [P3] (E) The "Snowball Does Not Fall Apart" subsection correctly explains that folding alone does not provide soundness, but does not mention that the accumulated error vector E can grow unboundedly in the basic Nova construction — relevant for readers who go on to read about SuperNova/HyperNova improvements

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-the-hybrid-pipeline]]
- Next: [[ch06-the-folding-genealogy]]
