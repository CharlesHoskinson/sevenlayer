---
title: "The First Decision"
slug: ch01-the-first-decision
chapter: 1
chapter_title: "The Promise of Provable and Programmable Secrets"
heading_level: 2
source_lines: [334, 366]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
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

In 2016, the Zcash ceremony involved six participants, each generating a share of the secret parameters and then destroying their share. If even one of the six was honest, the system is secure. By 2023, the Ethereum KZG Summoning had scaled that to six figures -- the same principle, applied at the population level. The alternative -- transparent setups that require no ceremony at all -- avoids the problem entirely, at a cost in proof size and verification expense.

That question -- trusted setup or transparent setup, ceremony or glass stage, hidden trapdoors or none -- is the subject of Chapter 2. It is the first fork in the road. Its consequences echo through every layer that follows.



## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
