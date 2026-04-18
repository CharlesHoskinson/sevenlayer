---
title: "SNARK Recursion vs. Folding: The Full Picture"
slug: ch06-snark-recursion-vs-folding-the-full-picture
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2902, 2936]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 557
---

## SNARK Recursion vs. Folding: The Full Picture

Now that we have seen both approaches in action -- Midnight's recursive Halo 2 architecture and the folding genealogy leading to Neo and Symphony -- we can draw a more complete picture of how they compare.

### When Recursion Wins

Recursive proof composition is the right choice when:

- The chain of computation is short (tens of steps, not millions)
- The proof system already has a cheap verifier circuit (as Halo 2 does for its IPA-based verification)
- The application needs per-step proofs (every transaction gets its own proof, as in Midnight)
- The infrastructure is mature and the priority is correctness over performance

Recursion is conceptually simpler: each step produces a proof, and the next step verifies it. There are no accumulated instances to manage, no decider to run at the end, and no error vectors that grow with the chain length. For short chains and mature tooling, recursion is the pragmatic choice.

### When Folding Wins

Folding is the right choice when:

- The chain of computation is long (millions of VM steps)
- Per-step cost must be minimized (the overhead of a full SNARK verification per step is unacceptable)
- The application is a zkVM or rollup that processes large batches of transactions
- Post-quantum security is a requirement (lattice-based folding via Neo/Symphony)
- Parallel proving is needed (multi-instance folding via ProtoGalaxy enables tree-structured PCD)

The asymptotic advantage of folding is clear: $O(|F|)$ prover cost per step (where $|F|$ is the step circuit size) plus roughly 1,500 gates of folding overhead (with CycleFold), compared to $O(|F| + |V|)$ for recursion, where $|V|$ is the size of the verifier circuit (potentially millions of gates). For a zkVM executing millions of RISC-V instructions, this difference is the gap between practical and impractical.

### The Convergence

In practice, the distinction between recursion and folding is blurring. Most production systems use a hybrid: folding for the inner loop (accumulate computation steps cheaply), then a monolithic SNARK (Spartan, Groth16) as the "decider" that produces the final succinct proof. Nova uses Spartan as its decider. Mangrove (Nguyen, Datta, Chen, Tyagi, Boneh, 2024) builds a k-arity PCD tree where leaf nodes fold computation chunks and internal nodes merge folded instances, with a final SNARK for the NP statement. The boundary between "folding" and "recursion" dissolves into a pipeline where both techniques serve different stages.

The key decision variable is step count. For computations under approximately 1,000 steps, recursion with a fast inner proof system (Groth16 or PLONK) is competitive in both prover time and implementation complexity -- the per-step overhead of a full recursive proof is high but amortizes over few steps. For computations exceeding 10,000 steps -- the regime of zkVMs proving full program executions -- folding's $O(|F|)$ per-step cost with ~1,500 gates of folding overhead dominates recursion's $O(|F| + |V|)$ per-step cost, where $|V|$ is the verifier circuit size. The crossover region between 1,000 and 10,000 steps depends on the specific constraint system, field size, and hardware: folding wins earlier on small fields (where $|V|$ is relatively large compared to $|F|$) and later on pairing-friendly fields (where recursive verification is cheap). In practice, the distinction is blurring -- the dominant architecture uses folding for the inner accumulation loop and a single recursive SNARK compression as the final decider step.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
