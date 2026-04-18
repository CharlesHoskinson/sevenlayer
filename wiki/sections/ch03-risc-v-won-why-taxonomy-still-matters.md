---
title: "RISC-V Won. Why Taxonomy Still Matters."
slug: ch03-risc-v-won-why-taxonomy-still-matters
chapter: 3
chapter_title: "Choreographing the Act"
heading_level: 2
source_lines: [761, 792]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 375
---

## RISC-V Won. Why Taxonomy Still Matters.

Chapter 2 closed with a question: who writes the script? The answer is the developer -- but the language she writes in determines what mistakes she can make, and some mistakes break everything.

If RISC-V has won -- if eight of ten major zero-knowledge virtual machines now target the same general-purpose instruction set -- why bother presenting a taxonomy of competing philosophies at all? Why not just say "write Rust, compile to RISC-V, the proof system handles the rest"?

Because the taxonomy is not about which instruction set the machine runs. It is about what *the developer sees*. And what the developer sees determines what bugs the developer makes. Those bugs -- not cryptographic breaks, not quantum computers, not governance attacks -- are the single largest source of real-world failures in zero-knowledge systems. Sixty-seven percent of all known SNARK vulnerabilities are under-constrained circuits: programs where the developer said less than they meant, and the proof system happily proved false statements as a result.

The language layer is where the magician writes the choreography for the act. The choice of notation determines what mistakes are possible. Some notations let the performer accidentally step into the audience's view. Others physically prevent it. That distinction is worth understanding, even in a world where RISC-V has won the instruction set war.

> **The Running Example: A Sudoku Proof**
>
> To ground the abstractions that follow, we will trace a single computation through every layer of the stack. The computation: proving you know the solution to a 4x4 Sudoku puzzle without revealing it.
>
> The puzzle has these givens:
>
> ```
> +---+---+---+---+
> | 1 |   |   | 4 |
> +---+---+---+---+
> |   | 4 | 1 |   |
> +---+---+---+---+
> |   | 1 |   |   |
> +---+---+---+---+
> | 4 |   |   | 1 |
> +---+---+---+---+
> ```
>
> The program checks: every row contains {1,2,3,4} with no repeats, every column contains {1,2,3,4}, every 2x2 box contains {1,2,3,4}, and every filled cell matches the given clue. The prover knows the solution. The verifier knows only the puzzle. At Layer 2, this is a program. We follow it through every layer to come.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
