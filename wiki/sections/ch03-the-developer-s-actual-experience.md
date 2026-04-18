---
title: "The Developer's Actual Experience"
slug: ch03-the-developer-s-actual-experience
chapter: 3
chapter_title: "Choreographing the Act"
heading_level: 2
source_lines: [1036, 1073]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 1190
---

## The Developer's Actual Experience

The taxonomy of philosophies describes how *architects* think about Layer 2. But what does a *developer* actually do?

The taxonomy describes how *architects* think about Layer 2. But what does a *developer* actually do once they have picked a language? The answer involves a lifecycle that most ZK documentation glosses over.

**Step 1: Write.** The developer writes source code. In SP1, this is standard Rust. In Circom, this is a template-based constraint description language. In Compact, this is TypeScript-like code with `witness` declarations and `circuit` exports. The writing experience varies enormously. An SP1 developer uses familiar tools -- VS Code, cargo, clippy. A Circom developer works in a specialized IDE with no debugger, no step-through execution, and error messages that refer to constraint indices rather than variable names.

**Step 2: Compile.** The compiler translates source code into a form the proof system can work with. For SP1, this means Rust to RISC-V machine code via the standard LLVM backend. For Circom, this means templates to R1CS constraint systems. For Compact, this means a 26-pass nanopass compilation pipeline -- "nanopass" because each pass makes one small, verifiable transformation -- that transforms the source through 26 intermediate languages -- from `Lsrc` through type checking (`Ltypes`), disclosure analysis (`Lnodisclose`), loop unrolling (`Lunrolled`), circuit flattening (`Lflattened`), and finally ZKIR output.

A critical finding from recent research: standard LLVM optimization passes (-O3) yield over 40% improvement when targeting zkVMs, compared to much larger gains on traditional CPUs. This is because LLVM's optimization heuristics are tuned for hardware features -- cache locality, branch prediction, instruction-level parallelism -- that do not exist in a zkVM. By refining a small set of LLVM passes to use a ZK-aware cost model, researchers achieved up to 45% on individual benchmarks (with average gains of 1-4%). The compiler is an underexplored optimization surface.

**Step 3: Test.** The developer tests their program. In the RISC-V world, this means running the program natively (without proof generation) and checking outputs. SP1 supports this directly: you can execute your Rust program on a standard CPU and verify correctness before paying the cost of proof generation. In Compact, the SDK provides a local execution oracle that simulates the blockchain environment -- block time, token balances, contract state -- without a running chain.

**Step 4: Prove.** The developer generates a proof. This is where the cost hits. Proof generation for a Compact circuit takes seconds to tens of seconds on local development hardware (detailed timings appear in Chapter 6). For an SP1 program, proving time depends on the number of RISC-V cycles executed -- a simple computation might take seconds; an Ethereum block might take minutes even on GPU clusters.

What does "prove" actually feel like? The experience is unlike anything else in software development. There is no analogy in web development, in systems programming, in machine learning training. It is its own thing, and it deserves honest description.

You run the prove command. In SP1, it is `cargo prove build` followed by `cargo prove`. In Circom, it is `snarkjs groth16 prove`. In Compact, the proof server at localhost:6300 handles it. Then you wait.

The wait is the defining experience. A computation that takes milliseconds to execute takes seconds or minutes to prove. Your CPU fans spin up. Your GPU memory fills. A progress bar crawls, or -- in many systems -- there is no progress bar at all. Just silence, then a result. You cannot step through the prover the way you step through a debugger. You cannot inspect intermediate state. The prover is a black box that accepts your witness and, after an uncomfortable pause, either produces a proof or fails.

The first time it works, the output is anticlimactic. A file appears -- a few hundred bytes for Groth16, a few hundred kilobytes for a STARK. You can hold the entire proof in a single network packet. The disproportion is disorienting: your computer just spent thirty seconds of full-throttle computation to produce something smaller than the paragraph you are reading. But that tiny file certifies every step. Every multiplication. Every memory access. Every constraint. If even one bit of the witness was wrong, the proof would not exist.

The first time it fails, the output is worse than unhelpful. Circom gives you constraint indices: "Constraint 4,217 is not satisfied." Not variable names. Not line numbers. Not a description of what went wrong. A constraint index that you must trace back, by hand, through the R1CS system to the source code. SP1 and Noir are better -- they surface Rust panics or assertion messages from the guest program -- but even there, debugging a proof failure often means reasoning backward from a polynomial identity to a logic error. The tooling is years behind what developers expect from mainstream languages.

The cost asymmetry is the thing that shapes development habits. Running your program natively (without proof) takes milliseconds. Running it with proof takes minutes. So you test obsessively before you prove, because every proof attempt is expensive in wall-clock time. The prove step becomes the inner loop's bottleneck -- not in compute cost (that is the prover operator's problem) but in iteration speed (that is the developer's problem).

**Step 5: Deploy.** The proven program is deployed. For rollup-based systems, this means posting the proof and public inputs to Ethereum. For Compact, this means deploying the ZKIR circuit, TypeScript bindings, and proving keys to Midnight's network. Contract deployment on Midnight's devnet is dominated by proof generation for the constructor circuit (see Chapter 6 for measured latencies).

**Step 6: Monitor.** In production, the developer monitors for correctness, performance, and security. This step is almost entirely undocumented in the ZK ecosystem. There are no standard monitoring tools for ZK deployments. No dashboards for constraint utilization. No alerting for proof generation failures. The gap between "deploy" and "done" is where real-world systems fail.

One emerging bright spot: LLM-assisted ZK development. The ZK-Coder system improved Circom circuit generation success rates from 20% (baseline large language model) to 88%. This suggests that the developer experience barrier -- the steep learning curve, the unfamiliar constraint semantics, the cryptic error messages -- may be partially addressable through AI tooling. But 88% is not 100%, and the 12% failure cases may be precisely the subtle under-constrainedness bugs that are hardest to detect. An LLM that generates a circuit with a missing constraint is more dangerous than an LLM that fails to generate a circuit at all.

The developer workflow reveals something about Layer 2: the *language* is the part the developer sees, but the *compiler* is the part that matters. A language with beautiful syntax and a buggy compiler is worse than an ugly language with a correct compiler. The field is beginning to understand this. CirC, a unifying compiler infrastructure from Stanford, demonstrated that the compilation problem for ZK circuits shares fundamental structure with SMT solving and software verification. The same optimizations -- constant folding, dead code elimination, common subexpression elimination -- apply across all targets. This suggests that investment in ZK compiler infrastructure could pay off disproportionately, improving every language simultaneously rather than optimizing each one independently.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
