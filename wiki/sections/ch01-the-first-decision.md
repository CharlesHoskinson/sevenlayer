---
title: "The First Decision"
slug: ch01-the-first-decision
chapter: 1
chapter_title: "The Promise of Provable and Programmable Secrets"
heading_level: 2
source_lines: [336, 368]
source_commit: b933209bc74dbc4253ecfd9814aa87712b628a3e
status: reviewed
word_count: 572
---

## The First Decision

A running example will ground every abstraction from Chapter 3 through Chapter 6: a 4x4 Sudoku puzzle. It is the computation we prove at each layer -- first as a program, then as a witness, then as 72 polynomial constraints, then as a sealed certificate, and finally as a verified proof. The same small puzzle, viewed through four different lenses.

Why Sudoku? Because it is small enough to hold in your head (sixteen cells, four values), complex enough to exercise every layer of the proof stack (range checks, uniqueness constraints, boundary conditions), and familiar enough that no mathematical background is needed to understand what a valid solution looks like. When the constraint system in Chapter 5 checks that every row contains {1, 2, 3, 4} with no repeats, you will be able to verify the logic yourself -- and that is precisely the point. The running example is not decoration. It is a test: if the explanation makes sense for Sudoku, it makes sense in general.

Over the next four chapters, you will watch this puzzle undergo a series of transformations. First it becomes a program: sixteen variables, a handful of rules, written in a language the proof system can understand. Then it becomes a witness: a completed grid that only the prover can see, with every intermediate computation recorded. Then it becomes 72 polynomial equations -- the mathematical encoding that replaces human intuition with algebraic structure. And finally it becomes a proof: a handful of numbers, smaller than this sentence, that convinces any stranger the solution exists. Each transformation strips away one more layer of human readability and replaces it with mathematical certainty. By the end, the puzzle will be unrecognizable. That is exactly the point.

Here is the puzzle. Eight cells are given; eight are blank:

```
+---+---+---+---+
| 1 |   |   | 4 |
+---+---+---+---+
|   | 4 | 1 |   |
+---+---+---+---+
|   | 1 |   |   |
+---+---+---+---+
| 4 |   |   | 1 |
+---+---+---+---+
```

Each row, each column, and each 2x2 box must contain {1, 2, 3, 4} exactly once. You can probably solve it in your head. The prover will solve it, too -- and then prove the solution is correct without showing you a single filled-in cell.

Now we need to build the stage.

Every magic show requires one. In zero-knowledge proof systems, "building the stage" means creating the mathematical parameters that both characters will use -- the prover to generate proofs, the verifier to check them. This step happens before any proof is ever created. The most important question about the stage is not how it is built but *who builds it, and whether you have to trust them*.

The ceremonies scaled from intimate to planetary in seven years. In 2016, the Zcash Sprout ceremony involved six participants, each generating a share of the secret parameters and then destroying their share; if even one of the six was honest, the system was secure. Two years later, the Zcash Sapling ceremony used the BGM17 multi-party protocol and grew to roughly ninety contributors, proving the trick could scale past a small team. By 2023, the Ethereum KZG Summoning had scaled that to six figures -- 141,416 participants, same principle, applied at the population level. The alternative -- transparent setups that require no ceremony at all -- avoids the problem entirely, at a cost in proof size and verification expense.

That question -- trusted setup or transparent setup, ceremony or glass stage, hidden trapdoors or none -- is the subject of Chapter 2. It is the first fork in the road. Its consequences echo through every layer that follows.



## Summary

A 4×4 Sudoku puzzle — 16 cells, four values, 72 polynomial constraints — serves as the running example through Chapters 3–6, tracing each layer of the proof stack in miniature. "Building the stage" (the mathematical parameters both prover and verifier use) is the first fork in any ZK design: trusted setup (ceremony) or transparent setup, each with distinct cost and trust trade-offs.

## Key claims

- The Sudoku example is chosen because it is small enough to hold in your head, complex enough to exercise every layer, and requires no mathematical background.
- The same 4×4 Sudoku undergoes four transformations: program → witness → 72 polynomial constraints → a compact proof.
- The 2016 Zcash ceremony involved 6 participants; if any one was honest, the system is secure.
- Ethereum's KZG Summoning scaled the same principle to 141,416 participants by 2023.
- Transparent setups avoid the ceremony entirely at a cost in proof size and verification expense.
- Trusted vs. transparent setup is the first fork in the road; its consequences echo through every layer.

## Entities

- [[ceremony]]
- [[kzg]]
- [[sudoku]]
- [[zcash]]

## Dependencies

- [[ch01-the-seven-layers-at-a-glance]] — Layer 1 (setup) introduced as the first layer
- [[ch01-the-deepest-question]] — Layer-by-layer trust analysis that frames why setup choice matters

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [P2] (B) No source is cited for either the Zcash Sprout ceremony details or the Ethereum KZG Summoning participant count; add a reference to the KZG ceremony attestation page or the Ethereum Foundation blog post.
- [P2] (C) "Eight cells are given; eight are blank" — the puzzle ASCII art shows a 4×4 grid; the claim that "eight cells are given" is correct (1, 4, 4, 1, 1, 4, 1 — actually count: top row: 1,_,_,4 = 2 given; row 2: _,4,1,_ = 2 given; row 3: _,1,_,_ = 1 given; row 4: 4,_,_,1 = 2 given = 7 given, not 8). Verify the cell count.
- [P3] (E) The section introduces "transparent setup" as the alternative but gives only one sentence on the trade-off; a brief mention of FRI-based systems (STARKs) as the canonical transparent approach would reduce the abstraction here without adding length.
- [none] D — no cross-chapter contradictions found beyond those noted above.

## Links

- Up: [[01-the-promise-of-provable-and-programmable-secrets]]
- Prev: [[ch01-the-deepest-question]]
- Next: [[ch01-how-to-read-this-guide]]
