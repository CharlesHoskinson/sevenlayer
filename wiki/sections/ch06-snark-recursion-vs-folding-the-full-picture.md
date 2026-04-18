---
title: "SNARK Recursion vs. Folding: The Full Picture"
slug: ch06-snark-recursion-vs-folding-the-full-picture
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2916, 2950]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
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

Recursion suits short computation chains with per-step proof requirements and mature tooling; folding suits long VM execution chains where per-step SNARK verification overhead is unacceptable. The crossover is approximately 1,000--10,000 steps. In practice the boundary dissolves: production systems fold cheaply in the inner loop and apply a single SNARK decider (Spartan, Groth16) at the end.

## Key claims

- Recursion wins for: short chains (<~1,000 steps), per-step proof requirements, mature tooling (e.g., Midnight).
- Folding wins for: long chains (>~10,000 steps), zkVMs, post-quantum (lattice folding), parallel proving (ProtoGalaxy).
- Folding per-step cost: $O(|F|)$ + ~1,500 gates (CycleFold); recursion per-step cost: $O(|F| + |V|)$ where $|V|$ may be millions.
- Nova uses Spartan as its decider SNARK.
- Mangrove (Nguyen, Datta, Chen, Tyagi, Boneh, 2024): k-arity PCD tree with folding at leaves, SNARK at root.
- Dominant production architecture: folding inner loop + single SNARK decider compression.
- Crossover point (1,000--10,000 steps) varies by constraint system, field size, and hardware.

## Entities

- [[nova]]
- [[folding]]
- [[groth16]]
- [[plonk]]
- [[halo2]]
- [[spartan]]
- [[symphony]]
- [[boneh]]
- [[ipa]]
- [[midnight]]

## Dependencies

- [[ch06-recursion-vs-folding-russian-dolls-and-snowballs]] — introduces the recursion vs. folding distinction
- [[ch06-the-folding-genealogy]] — genealogy of folding schemes referenced in this section
- [[ch06-case-study-midnight-s-sealed-certificate]] — Midnight's recursion approach is contrasted here
- [[ch06-the-post-quantum-horizon]] — lattice-based folding for post-quantum is one of the folding win conditions

## Sources cited

- Nguyen, Datta, Chen, Tyagi, Boneh, "Mangrove: A Scalable Framework for Folding-based SNARKs," ePrint 2024.

## Open questions

None flagged by this section.

## Improvement notes

- [P2] (D) The 1,000–10,000 step crossover threshold is stated twice: once mid-section and then again in the final paragraph, nearly verbatim; one occurrence should be cut
- [P2] (B) Mangrove citation lists "Nguyen, Datta, Chen, Tyagi, Boneh, 2024" — the ePrint should be cited with its number; also the author order should be verified against the actual paper
- [P3] (A) "Halo 2 does for its IPA-based verification" — Midnight's Halo 2 deployment uses KZG not IPA (as correctly noted in ch06-case-study-midnight); saying Halo 2 has a "cheap IPA-based verifier" without qualification is inconsistent with the Midnight case study

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-case-study-midnight-s-sealed-certificate]]
- Next: [[ch06-the-post-quantum-horizon]]
