---
title: "Execution Traces"
slug: ch04-execution-traces
chapter: 4
chapter_title: "The Secret Performance"
heading_level: 2
source_lines: [1208, 1252]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 751
---

## Execution Traces

Start with the simplest possible example. You want to prove you know a number whose square is 25. The witness is that number: 5. The proof convinces the verifier that you know such a number, without revealing that the number is 5. The verifier learns "this person knows a square root of 25." The verifier does not learn "the number is 5." (In fact, the verifier does not even learn whether you chose 5 or -5 -- both are valid witnesses for the same statement.)

Now scale up. You want to prove that an Ethereum state transition is valid -- that a block of transactions, when applied to the current state, produces the claimed new state. The witness is not a single number. It is the *entire execution trace*: every memory access, every register value, every instruction execution, every intermediate hash computation, every storage read and write. For a complex Ethereum block, this means millions of steps, each with dozens of columns of data. The execution trace for a block proved by SP1 or RISC Zero might contain billions of field elements.

The witness is, in the most literal sense, a complete recording of everything that happened during the computation. Think of it as a security camera that films the magician backstage: it captures not just the final result but every intermediate movement, every prop placement, every sleight of hand. The recording exists so that the proof system can later verify that every step was consistent with the rules -- without the verifier ever watching the footage.

Here is what a witness looks like for a trivial computation: proving that $x^2 + x = 12$ where $x = 3$.

| Step | Operation | Result |
|------|-----------|--------|
| 1 | Load x | 3 |
| 2 | $t_1 = x \times x$ | 9 |
| 3 | $t_2 = t_1 + x$ | 12 |
| 4 | Assert $t_2 = 12$ | ✓ |

Four field elements. Four rows in the trace table. Each intermediate value is a cell the prover must fill in and the constraint system must verify. For a real zkVM executing a RISC-V program, the trace has columns for every register (32 registers), the program counter, the current instruction, memory addresses accessed, and intermediate ALU results -- thousands of columns, millions of rows, but the same fundamental structure: a table where each row is one clock cycle of execution.

This distinction between the *computation* (what the magician does) and the *recording* (the witness) matters more than it looks. The computation might take milliseconds. The recording is vastly larger because it includes every intermediate value. And generating the recording -- running the computation while capturing every detail -- is the expensive part.

> **The Running Example: The Sudoku Witness**
>
> For our 4x4 Sudoku, the witness is the completed grid -- sixteen field elements:
>
> ```
> +---+---+---+---+
> | 1 | 2 | 3 | 4 |
> +---+---+---+---+
> | 3 | 4 | 1 | 2 |
> +---+---+---+---+
> | 2 | 1 | 4 | 3 |
> +---+---+---+---+
> | 4 | 3 | 2 | 1 |
> +---+---+---+---+
> ```
>
> The execution trace records every check: "cell (0,0) = 1, matches given? yes. Row 0 sum = 10, all distinct? yes. Column 0 = {1,3,2,4}, all distinct? yes. Box (0,0) = {1,2,3,4}, all distinct? yes." Sixteen values, plus every intermediate comparison and boolean result -- roughly 80 field elements in total. The verifier never sees this grid. The verifier sees only the original puzzle (the public input) and, eventually, the proof.

In a zkVM like SP1 or RISC Zero, witness generation means *emulating the entire RISC-V processor*. Every instruction is fetched, decoded, and executed. Every register update is recorded. Every memory access is logged. This is full virtual machine emulation, step by step, sequentially. It cannot be easily parallelized because each instruction depends on the state left by the previous instruction. The program counter moves forward one step at a time, and the witness generator must follow.

Here is why witness generation is CPU-bound. Polynomial arithmetic -- the core of the proving step -- is naturally parallel. Number-theoretic transforms, multi-scalar multiplications, and polynomial evaluations split naturally across thousands of GPU cores. But VM emulation is inherently sequential. The next instruction depends on the current instruction's result. You cannot execute instruction 1,000 before you know the outcome of instruction 999.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
