---
title: "Witness Generation Costs"
slug: ch04-witness-generation-costs
chapter: 4
chapter_title: "The Secret Performance"
heading_level: 2
source_lines: [1259, 1335]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 1966
---

## Witness Generation Costs

The paper that this book revises claimed witness generation accounted for 10-25% of total proving time. That figure was approximately correct in 2023, when the proving step was slow enough to dwarf everything else. It is no longer correct.

Modern GPU-accelerated provers have transformed the cost structure. When the cryptographic proving step runs on an NVIDIA H100 GPU -- or a cluster of them -- it becomes 10 to 100 times faster than on a CPU. Multi-scalar multiplications, the traditional bottleneck, have been optimized to the point where number-theoretic transforms (NTTs -- the finite-field version of the Fast Fourier Transform) now account for up to 90% of GPU proving time. And NTTs themselves have been accelerated through pipelining, with systems like BatchZK achieving over 3,000 times speedup over CPU baselines for Merkle tree commitment operations.

But witness generation did not ride this wave. It remains CPU-bound. Sequential. Memory-intensive. Accelerate the proving step by 10x and leave witness generation unchanged, and watch the proportions shift:

Before GPU acceleration: witness generation takes 2 seconds, proving takes 8 seconds. Witness share: 20%.

After GPU acceleration: witness generation still takes 2 seconds, proving takes 0.8 seconds. Witness share: 71%.

Welcome to the Witness Gap -- and it is growing, not shrinking. Every improvement to the proving step makes the witness gap worse by proportion. The field has been optimizing the fast part and ignoring the slow part.

To feel the scale: our 4x4 Sudoku produces a witness of roughly 80 field elements. Trivial. A 9x9 Sudoku -- the kind you find in a newspaper -- produces thousands. An Ethereum block produces billions. The witness for a single Ethereum block, fully materialized, can exceed 100 gigabytes of RAM. The gap between "toy example" and "production workload" is not a gentle slope. It is a cliff.

The numbers from recent profiling studies confirm this. ZKPOG, the first end-to-end GPU acceleration system that treats witness generation as a first-class optimization target, demonstrated that moving witness generation to the GPU can yield 3-10x speedups. But this requires different parallelization strategies than proving. Proving parallelizes naturally because polynomial arithmetic is regular and data-independent. Witness generation requires analyzing the circuit's dependency graph, topologically sorting gates to identify independent clusters, and mapping irregular computation patterns onto GPU hardware. The parallelism is there, but extracting it is harder.

BatchZK took a different approach: pipelining. Instead of generating the entire witness first and then proving, BatchZK overlaps witness generation with proof computation. The witness is generated in chunks and fed into the prover as a stream. This significantly improves GPU utilization throughout the pipeline compared to sequential approaches where the GPU sits idle during witness generation.

The most radical proposal comes from Nair, Thaler, and Zhu, who showed that the Jolt zkVM can be implemented with *streaming witness generation* -- the prover never materializes the full witness in memory. Instead, it generates witness chunks on the fly, consumes them immediately in the sum-check protocol, and discards them. Checkpoints at regular intervals enable parallel regeneration. The space requirement drops from linear in the trace length to the square root of the trace length, with less than 2x time overhead. For a computation with $2^{35}$ cycles, this means roughly 100 GB of working memory instead of terabytes.

A third approach attacks the problem from the constraint side rather than the computation side. Ozdemir, Laufer, and Boneh developed new algebraic interactive proofs for RAM consistency checking -- the process of verifying that memory reads and writes in the execution trace are consistent. Memory checking dominates zkVM witness generation cost because the standard approach (Merkle tree commitments) requires approximately $600 \cdot A \cdot \log(N)$ constraints for A accesses to N-sized memory. Each Poseidon hash in the Merkle tree costs roughly 300 field multiplications. Their approach reduces this to $3N + 2A + O(1)$ constraints -- up to 51.3x fewer for persistent memory and even more for sparse memory. By shrinking the constraint count for memory operations, this work proportionally shrinks the witness that must be generated, since memory-related witness entries often dominate the total witness size.

These are not theoretical proposals. They represent the frontier of a field that has finally recognized where the real bottleneck lives.

### The Bottleneck That Flipped

The before-and-after illustrates a pattern that recurs throughout engineering: the phenomenon where solving one problem promotes the next problem to dominance.

In 2023, a typical zero-knowledge proof for a moderately complex computation -- say, verifying a batch of Ethereum transactions -- took approximately 10 seconds end to end. Of those 10 seconds, approximately 2 seconds were spent on witness generation: emulating the virtual machine, recording every register value, logging every memory access, building the complete execution trace. The remaining 8 seconds were spent on the cryptographic proving step: computing multi-scalar exponentiations, performing number-theoretic transforms, building polynomial commitments. The witness generation share was 20%. It was a minor cost. Nobody optimized it because the proving step was the obvious target.

The field poured billions of dollars into making the proving step faster. GPU implementations replaced CPU implementations. Custom NTT kernels exploited the butterfly structure of the transform. Batched MSM algorithms amortized curve operations across thousands of scalar multiplications. Pipeline architectures overlapped memory transfers with computation. It worked. By 2025, GPU acceleration had reduced the proving step from 8 seconds to 0.8 seconds -- a 10x improvement, and some systems achieved 100x.

Witness generation was still 2 seconds.

The arithmetic is pitiless. Before: 2 / (2 + 8) = 20%. After: 2 / (2 + 0.8) = 71%. The proving step had become a solved problem. The witness step had become the problem. And the worse the proving step got (in the sense of "faster"), the more dominant the witness step became. At 100x GPU acceleration, the proving step drops to 0.08 seconds, and witness generation accounts for 96% of total time. At that point, further GPU optimization yields approximately zero improvement to the end-to-end latency. You could make the proving step infinitely fast and the proof would still take 2 seconds.

This is Amdahl's Law applied to zero-knowledge proofs. Amdahl's Law states that the speedup of a program is limited by the fraction of the program that cannot be parallelized. If witness generation accounts for 71% of total time and cannot be parallelized (because VM emulation is inherently sequential), then even infinite parallelization of the remaining 29% yields at most a 3.4x overall speedup. The bottleneck is not a bottleneck you can throw hardware at. It is a bottleneck in the structure of the computation itself.

### Why Witness Generation Resists Parallelization

The reason witness generation is sequential is not an accident of implementation. It is a consequence of what witness generation *is*.

Consider a RISC-V program executing inside a zkVM. Each instruction reads from registers, performs an operation, and writes the result to a register. The next instruction reads from registers that may have been written by the previous instruction. The program counter advances by one. Branches depend on comparison results that were just computed. Memory loads depend on addresses that were just calculated.

This is a dependency chain. Instruction 1000 cannot execute before instruction 999 because instruction 1000 might read a register that instruction 999 wrote. Instruction 999 cannot execute before instruction 998 for the same reason. The entire execution trace is a single sequential thread of dependencies, from the first instruction to the last.

Compare this to the proving step. A number-theoretic transform operates on a vector of field elements. Each butterfly operation in the transform reads two elements, computes two outputs, and writes them back. The butterfly operations within a single stage of the transform are *independent* -- they read and write disjoint memory locations. This means they can execute in parallel across thousands of GPU cores. The parallelism is not extracted by clever engineering; it is inherent in the mathematical structure of the transform.

Witness generation has no such structure. The "butterfly" of VM emulation is a single instruction, and each instruction depends on the previous one. There is no way to execute instruction 1000 before instruction 999 completes, because you do not know what instruction 1000 *is* until instruction 999 has updated the program counter. A branch instruction at position 999 could send execution to position 1000 or to position 5000 or anywhere else. You cannot know until the branch condition is evaluated.

This is why three different research groups attacked the problem from three different angles -- each targeting a different dimension of the sequential bottleneck.

**Pipelining (BatchZK).** Instead of generating the entire witness first and then proving, BatchZK overlaps the two phases. The witness is generated in chunks: the first chunk of the execution trace is produced, then immediately fed to the GPU prover while the CPU generates the next chunk. The GPU is never idle. The CPU is never idle. The total wall-clock time drops because the two phases execute concurrently. But the witness generation itself is not faster -- only the overlap is new. Pipelining does not solve the sequential bottleneck; it hides it behind the proving step.

**Streaming (Nair, Thaler, Zhu).** The streaming approach attacks the memory dimension. Instead of materializing the full witness -- which for large computations can require hundreds of gigabytes of RAM -- the streaming prover generates witness chunks on demand, feeds them into the sum-check protocol, and discards them. Checkpoints at regular intervals (every $\sqrt{T}$ steps) allow the prover to restart from any checkpoint, enabling a form of parallelism: different proving threads can work on different segments of the trace, each regenerating its segment from the nearest checkpoint. The space requirement drops from $O(T)$ to $O(\sqrt{T})$, and the time overhead is less than 2x. For a computation with $2^{35}$ cycles, this means roughly 100 GB of working memory instead of terabytes.

**Algebraic RAM reduction (Ozdemir, Laufer, Boneh).** The most radical approach does not try to make witness generation faster or smaller. It tries to make the witness *simpler*. Memory checking -- verifying that memory reads and writes in the execution trace are consistent -- is the dominant cost in zkVM witness generation because the standard approach uses Merkle trees. Each memory access requires a Poseidon hash, and each Poseidon hash costs approximately 300 field multiplications. For a program with A memory accesses to N-sized memory, the standard approach requires approximately $600 \cdot A \cdot \log(N)$ constraints. Ozdemir et al. replace Merkle tree checking with algebraic interactive proofs that require only $3N + 2A + O(1)$ constraints -- up to 51.3x fewer. Fewer constraints means a smaller witness for the memory-checking portion, which often dominates the total witness.

Each approach has trade-offs. Pipelining requires careful synchronization between the CPU witness generator and the GPU prover. Streaming requires checkpoint management and sacrifices some proving speed for memory savings. Algebraic RAM reduction requires new interactive proof protocols that are not yet implemented in production systems. But together, they represent the first serious engineering effort to close the witness gap -- the gap that the field spent years ignoring because the proving step was the shinier problem.

The key performance numbers tell the story:

| Metric | Value | Source |
|---|---|---|
| Witness generation share (with GPU proving) | 50-70% of total time | ZKPOG |
| NTT share of GPU proving time | up to 90% | ZKProphet |
| GPU pipeline speedup over CPU (sum-check protocol) | 3,040x | BatchZK |
| GPU pipeline speedup over CPU (Merkle tree) | 793x | BatchZK |
| GPU pipeline memory per proof | 0.08-0.44 GB | BatchZK |
| Streaming prover space reduction | $O(\sqrt{KT})$ | Nair et al. |
| RAM constraint reduction | up to 51.3x | Ozdemir et al. |
| ZKPOG end-to-end GPU speedup | 22.8x average | ZKPOG |

---


## Summary

GPU acceleration reduced proving time 10–100× but left witness generation unchanged, pushing its share of total time from ~20% to 50–70% — Amdahl's Law applied to ZK. Three research directions attack this: pipelining (BatchZK overlaps witness and proving phases), streaming (Nair, Thaler, Zhu reduce space to $O(\sqrt{T})$), and algebraic RAM reduction (Ozdemir, Laufer, Boneh cut memory-checking constraints up to 51.3×).

## Key claims

- Witness generation share rose from ~20% to ~71% after 10× GPU acceleration; at 100× acceleration it reaches ~96%.
- NTTs account for up to 90% of GPU proving time (ZKProphet).
- BatchZK achieves 3,040× GPU speedup over CPU for the sum-check protocol and 793× for Merkle tree operations.
- Streaming witness generation (Nair et al.) reduces space from $O(T)$ to $O(\sqrt{KT})$ with <2× time overhead.
- Algebraic RAM reduction (Ozdemir, Laufer, Boneh) cuts constraints from $600 \cdot A \cdot \log(N)$ to $3N+2A+O(1)$ — up to 51.3× fewer.
- ZKPOG achieves 22.8× average end-to-end GPU speedup by treating witness generation as a first-class target.
- Amdahl's Law: if witness generation is 71% of total time and cannot be parallelized, infinite proving acceleration yields at most 3.4× overall speedup.

## Entities

- [[boneh]]
- [[h100]]
- [[jolt]]
- [[ntt]]
- [[ntts]]
- [[nvidia]]
- [[poseidon]]
- [[sudoku]]

## Dependencies

- [[ch04-execution-traces]] — establishes what the witness is and why generation is sequential
- [[ch04-memory-the-binding-constraint]] — the memory dimension of the same bottleneck
- [[ch05-the-overhead-tax-10-000x-to-50-000x]] — proving-step costs that the Witness Gap now exceeds
- [[ch05-the-sumcheck-protocol-the-hidden-foundation]] — sumcheck is the protocol that streaming feeds

## Sources cited

- ZKPOG (end-to-end GPU acceleration, 22.8× speedup, 50–70% witness share)
- ZKProphet (NTT share up to 90% of GPU proving time)
- BatchZK (3,040× sum-check speedup, 793× Merkle tree speedup, 0.08–0.44 GB memory per proof)
- Nair, Thaler, Zhu — streaming prover, $O(\sqrt{KT})$ space
- Ozdemir, Laufer, Boneh — algebraic RAM reduction, up to 51.3×

## Open questions

None flagged by this section.

## Improvement notes

- [P1] (A) The table row "GPU pipeline speedup over CPU (sum-check protocol): 3,040x — BatchZK" conflicts with the prose, which calls it "3,000 times speedup" at one point and "3,040x" in the table; the prose rounds to 3,000 but the table is more precise. Reconcile to a single figure throughout.
- [P1] (A) The streaming space bound is stated as $O(\sqrt{KT})$ in the Key claims and table but as $O(\sqrt{T})$ in the prose body. These are not equivalent unless K=1; if K is a checkpoint granularity parameter, define it or use a consistent notation throughout.
- [P2] (A) "An Ethereum block produces billions [of field elements]" then "can exceed 100 gigabytes of RAM" — the RAM figure covers materialized field elements at specific field sizes; the text doesn't mention the field size (e.g., 64-bit Goldilocks vs. 254-bit BN254 elements differ 4×). Adding the field size would make the RAM estimate verifiable.
- [P2] (B) ZKPOG, ZKProphet, BatchZK, Nair/Thaler/Zhu, and Ozdemir/Laufer/Boneh are all cited by name without publication years or venues. At minimum, years should appear in the Sources cited block; the prose treats all five as equally recent without dating them.
- [P2] (C) "Welcome to the Witness Gap — and it is growing, not shrinking." The em-dash and exclamatory register is a light AI-smell; tighten to a declarative statement.
- [P3] (E) The section does not mention whether pipelining (BatchZK) requires a specific proof system or is system-agnostic. The streaming approach (Jolt/sum-check) is explicitly tied to the sum-check protocol, but BatchZK's applicability is not bounded.

## Links

- Up: [[04-the-secret-performance]]
- Prev: [[ch04-execution-traces]]
- Next: [[ch04-memory-the-binding-constraint]]
