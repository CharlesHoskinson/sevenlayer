---
title: "The Seven Questions That Remain Open"
slug: ch14-the-seven-questions-that-remain-open
chapter: 14
chapter_title: "Open Questions and the Road Ahead"
heading_level: 2
source_lines: [5180, 5350]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 6042
---

## The Seven Questions That Remain Open

Richard Feynman had a test for understanding. If you cannot explain something simply, you do not understand it. If you can explain it simply and then find the place where your explanation breaks down, you have found the frontier.

We have spent thirteen chapters explaining zero-knowledge proofs -- layer by layer, system by system, from the stage to the audience. Now we arrive at the places where the explanation breaks down. These are not rhetorical questions. They are research problems with measurable progress and no current solution. Each one is an open door. Consider this an invitation to walk through.

### Question 1: Can witness generation be made fully parallel on GPUs?

Witness generation involves dependency chains -- each intermediate value may depend on previous ones in a directed acyclic graph that resists naive parallelism. When cryptographic proving moves to GPUs (achieving 10-50x speedups via NTT and MSM parallelism), witness generation remains CPU-bound, creating the Witness Gap. ZKPOG (2025) demonstrated 22.8x speedups by restructuring witness computation for GPU execution, but the general problem -- making arbitrary computation graphs GPU-friendly -- remains open.

The Witness Gap grows with every proving speedup, as Chapter 4 documented: accelerate the cryptographic step and the CPU-bound witness share swells to dominate total latency. The asymptotic state of zkVM performance may be entirely witness-bound. The backstage preparation may always take longer than the performance. Or perhaps not -- but no one has proven otherwise.

The concrete stakes are worth spelling out. If witness generation stays fundamentally sequential, then proving costs plateau regardless of how many GPUs you throw at the problem. You could have a warehouse of A100s computing NTTs in perfect lockstep, and the entire pipeline would still wait on a single CPU thread chasing a dependency chain through the execution trace. The fastest GPU prover in the world is only as fast as the slowest CPU witness generator feeding it. This is Amdahl's Law wearing a cryptographic costume.

ZKPOG's approach -- restructuring the witness computation's dependency graph so that independent sub-computations can be dispatched to GPU threads -- works when the graph has enough independent width. Many real circuits do. A Merkle tree hash has natural parallelism at each level. An elliptic curve multi-scalar multiplication decomposes into independent scalar-point products. But general computation does not cooperate this neatly. A loop where iteration $n$ depends on the result of iteration $n-1$ is inherently sequential, and no amount of clever scheduling changes that.

This creates a mismatch between two kinds of parallelism. Polynomial arithmetic -- NTTs, MSMs, commitment evaluations -- exhibits *regular* parallelism: the same operation applied uniformly to millions of independent data points. GPUs were designed for exactly this. Witness generation exhibits *irregular* parallelism: the computation graph's shape depends on the specific program, the specific input, and the specific execution path taken. GPUs were emphatically not designed for this. Regular parallelism maps to SIMT execution. Irregular parallelism maps to task-graph scheduling, which is the domain of CPU thread pools, not GPU warps.

The dependency graph approach points toward a middle path: analyze the witness computation ahead of time, identify the parallel width at each stage, and schedule GPU work only where the width justifies the dispatch overhead. But this requires a compiler that understands both the circuit semantics and the GPU memory hierarchy -- a compiler that does not yet exist in production. The gap between "this is possible in principle" and "this ships in a proving pipeline" is measured in years of compiler engineering.

What makes this question thrilling rather than depressing is that the bottleneck is *not* fundamental. Sequential witness generation is a property of current architectures, not a property of the underlying mathematics. The witness is a function of the public input and the private input. Nothing about that function requires sequential evaluation. The sequentiality comes from how we *describe* the computation (as a step-by-step trace), not from the computation itself. Whoever figures out how to describe the same computation in a form that exposes its inherent parallelism -- without changing the circuit it proves -- will unlock the next order-of-magnitude proving speedup. The NTT revolution happened when people stopped thinking of polynomials as coefficient lists and started thinking of them as evaluation vectors. The witness revolution will happen when someone finds the equivalent change of representation for execution traces.

The teams attacking this problem from different angles include: ZKPOG (GPU-accelerated witness computation with dependency graph analysis), Jolt/a16z (streaming witness generation that never materializes the full trace, from Nair, Thaler, and Zhu), BatchZK (pipelined witness-prove overlap that keeps the GPU busy while the CPU generates the next chunk), and Ozdemir, Laufer, and Boneh (algebraic RAM reductions that shrink the witness itself by 51x for memory operations). As documented in Chapter 4, witness generation accounts for 50-70% of total proving time in modern GPU-accelerated systems. The question is solved when that share drops below 20% on commodity hardware (Tier 2: an RTX 4090 workstation, not a data center cluster).

**Executive Risk:** Proving costs plateau regardless of GPU investment. Hardware budgets may hit diminishing returns before witness generation is parallelized. **Timeline:** 2-4 years for resolution.

### Question 2: What is the proven lower bound on post-quantum proof size?

Chapter 7 presented a trilemma: algebraic functionality, post-quantum security, and succinctness -- pick two. But is this a fundamental limitation or a reflection of current constructions? No paper proves that $O(1)$-size post-quantum proofs are impossible. The lattice-based schemes are achieving 50-100 KB proofs with post-quantum security, approaching practical territory. But whether there exists a post-quantum polynomial commitment scheme with $O(1)$ proof size and $O(1)$ verification time -- matching KZG's properties under lattice assumptions -- is unknown.

The ideal PCS problem comes into view: find a commitment scheme that is transparent (no trusted setup), produces constant-size proofs, enables constant-time verification, and relies only on post-quantum assumptions. If such a scheme exists, it would collapse the three-path framework of Chapter 10 into a single path. If it provably cannot exist, the three paths are permanent. Either answer would reshape the field. Neither answer exists today.

To appreciate the gap, consider the numbers side by side. A KZG polynomial commitment produces a proof that is a single elliptic curve point: 48 bytes. A Groth16 proof -- the entire argument of knowledge, not just the commitment -- fits in 192 bytes. These are absurdly small. They are small because the pairing structure of elliptic curves allows the verifier to check a polynomial identity with a single bilinear map evaluation. No redundancy. No repetition. Just one algebraic equation that either holds or doesn't.

Now look at the post-quantum world. The best lattice-based proofs run 50-100 KB. Hash-based proofs (STARKs) run larger still -- hundreds of kilobytes to low megabytes before recursion compresses them. The gap is three orders of magnitude. A KZG proof fits in a tweet. A lattice proof fills a small PDF. Why?

The reason is structural, not incidental. Pairing-based schemes exploit a specific algebraic trick: the pairing $e(g, h)$ lets you check multiplicative relations between committed values without revealing the values themselves. This trick compresses verification into a constant number of pairing evaluations, regardless of the polynomial's degree. Lattice-based schemes have no analogous trick. Their security rests on the hardness of finding short vectors in high-dimensional lattices -- a problem that is (probably) hard even for quantum computers, but that does not offer the same algebraic leverage. Verification requires checking that a vector is short, and the proof that a vector is short inherently requires transmitting information proportional to the vector's dimension.

The Wee-Wu line of results suggests that this gap may have deep roots. Their work on compact functional encryption and related primitives shows that certain cryptographic tasks require specific algebraic structure (pairings, or their lattice analogues) to achieve compactness, and that this structure is hard to instantiate from lattice assumptions without blowup. The barrier is not a proof of impossibility -- nobody has shown that $O(1)$-size post-quantum proofs *cannot* exist. But the barrier results suggest that if such proofs exist, they will require fundamentally new algebraic ideas, not incremental improvements to existing lattice techniques.

What would a proof of impossibility mean? It would mean the ZK field permanently bifurcates: fast-and-small proofs (pairing-based, quantum-vulnerable) versus large-and-safe proofs (lattice-based, quantum-resistant), with no bridge between them. Every system would need to choose a lane. The STARK-to-SNARK wrapping strategy described in Chapter 10 -- use hash-based proofs for soundness, then compress the proof with a pairing-based scheme for on-chain verification -- would be the permanent architecture, not a temporary compromise. The three paths would harden into the three permanent roads.

Conversely, if someone constructs a post-quantum scheme with $O(1)$ proof size, it would be the most important result in applied cryptography since Groth16. It would mean the entire field's current architecture -- the wrapping, the recursion, the careful balancing of proof size against verification cost -- is a temporary artifact of our incomplete understanding, not a fundamental constraint. Every ZK engineer is implicitly betting on which answer is correct. The field has placed most of its chips on "the gap is permanent" and built its infrastructure accordingly. If that bet is wrong, the infrastructure will need to be rebuilt. If that bet is right, the infrastructure is the final form. Either way, someone needs to settle the question. The mathematics is patient, but the engineering decisions are being made now.

**Executive Risk:** Permanent bifurcation of the ZK ecosystem into pre-quantum and post-quantum paths with no migration bridge. Systems deployed today on pairing-based foundations face mandatory replacement, not upgrade. **Timeline:** 5-10 years for theoretical resolution; practical deployment 3-5 years after.

### Question 3: When will Stage 2 bind?

L2Beat's Stages framework defines when ZK rollup governance can override cryptographic guarantees: Stage 0 (centrally controlled), Stage 1 (limited governance overrides with 7-day exit windows), Stage 2 (fully decentralized with 30-day exit windows and no governance override).

As of early 2026, most ZK rollups are Stage 0 or Stage 1. This means governance can override the proof system. A Stage 0 rollup could have 256-bit security and it would not matter if one person can push a verifier upgrade. The cryptographic guarantees of Layers 1-6 do not actually bind until a system reaches Stage 2. The magic trick is perfect, but the theater manager can rewrite the ending.

When will Stage 2 happen? Nobody knows, because Stage 2 requires resolving deep engineering challenges (bug-free verifier contracts, escape hatches that work in practice, proof submission that cannot be censored) and deep governance challenges (who decides when a system is ready, and what happens when a critical bug is found post-lock). The path forward likely involves multiple independent verifier implementations that cross-check each other, formal verification of the verifier contract's core logic, and mandatory exit windows long enough for users to withdraw if they disagree with a governance decision. Each of these is technically feasible; none has been fully achieved. This is the question where mathematics ends and human institutions begin.

Consider what Stage 2 actually looks like in practice. Picture a ZK rollup where no single entity -- not the founding team, not a multisig, not a governance token majority -- can push a verifier upgrade without triggering a mandatory 30-day exit window. During that window, every user can inspect the proposed change, compare the old and new verifier contracts, and withdraw their funds to L1 if they disagree. Multiple independent verifier implementations -- written by different teams, in different languages, tested against different fuzzing suites -- cross-check each other's results. If any implementation disagrees with the others, the system halts and the dispute resolution mechanism activates. The verifier contract itself has been formally verified: not just audited by humans who might miss an edge case, but proven correct by a theorem prover that has checked every execution path.

That is the goal. Now consider the tensions that make it hard.

The first tension is between immutability and patchability. An immutable verifier contract cannot be captured by governance -- but it also cannot be patched when a critical bug is discovered. And critical bugs *will* be discovered. The history of smart contract security is unambiguous on this point: every contract of sufficient complexity has bugs, and the bugs are found on timelines measured in months to years, not days. A Stage 2 system that locks its verifier contract is betting that the contract is bug-free. That bet has never been won at scale. A Stage 2 system that retains upgrade capability, even with time-locks, is betting that the governance process cannot be captured. That bet has been lost repeatedly in traditional finance. The equilibrium, if it exists, involves a narrow corridor: upgrades are possible, but only through a process so slow and so transparent that capture is impractical.

The second tension is between safety and liveness. A system with 30-day exit windows is safe -- users can always leave. But if a critical vulnerability is discovered and exploited, 30 days is an eternity. An attacker who finds a soundness bug can drain the rollup in a single transaction. The users' 30-day exit window is worthless if the funds have already been stolen. This suggests that Stage 2 needs not just exit windows but also emergency circuit-breakers -- but a circuit-breaker is a governance override, which is exactly what Stage 2 is supposed to eliminate. The circle closes on itself.

The third tension is economic. Multiple independent verifier implementations are expensive. Formal verification is expensive. Long exit windows impose opportunity costs on users. Who pays? In a Stage 0 system, the founding team pays for everything and recoups the cost through token appreciation or sequencer fees. In a Stage 2 system, the costs must be borne by the protocol itself, which means they are ultimately borne by users through fees or inflation. The economic question is whether the security premium of Stage 2 is worth the cost -- and the answer depends on how much value the rollup secures. A rollup holding $10 billion has a very different cost-benefit calculus than a rollup holding $10 million.

The honest answer may be that Stage 2 is not a destination but a spectrum. Different systems will reach different points on that spectrum depending on their value secured, their user base's risk tolerance, and the maturity of their verifier contract. The first true Stage 2 system will likely be a rollup that has been in production for years, has undergone multiple independent audits and formal verification efforts, and secures enough value to justify the engineering cost. It will be boring. It will be slow. It will be the most important thing in the ecosystem. The question is not *whether* it will happen, but whether the incentives align for it to happen before a catastrophic failure forces it to happen. The field should prefer the former.

**Executive Risk:** Governance override negates all cryptographic guarantees. Over $20B in TVL sits in systems where a multisig can replace the verifier. This is the single largest unresolved risk in ZK infrastructure. **Timeline:** 1-3 years for first Stage 2 rollups.

### Question 4: When will "trustless" become real?

The trust decomposition in Chapter 10 identified seven independent assumptions underlying ZK systems. To make the conjunction concrete, here they are:

1. **Layer 1 (Setup):** At least one of N ceremony participants was honest, or the transparent setup's hash function is collision-resistant.
2. **Layer 2 (Circuit):** The circuit was correctly written — no under-constrained bugs, no missing range checks.
3. **Layer 3 (Hardware):** The prover's hardware does not leak witness data through timing, cache, or electromagnetic channels.
4. **Layer 4 (Arithmetization):** The encoding from computation to polynomial constraints is faithful — every valid computation satisfies the constraints, and no invalid computation does.
5. **Layer 5 (Proof System):** The proof system is sound — the Fiat-Shamir transcript is complete, the security reduction is tight.
6. **Layer 6 (Math):** The underlying hardness assumptions (discrete log, collision resistance, Module-SIS) actually hold.
7. **Layer 7 (Governance):** The governance structure will not override the cryptography — no multisig replaces the verifier, no admin key drains the contract.

Today, every deployed system requires trusting all seven simultaneously. The trajectory points toward progressive reduction:

- Under-constrained circuits (Layer 2): formal verification tools (Picus, ZKAP, Coda) are reducing but not eliminating the vulnerability class catalogued in Chapter 3; the tools catch many but not all.
- Fiat-Shamir bugs (Layer 5): standardization of transcript protocols and automated fuzzing (ARGUZZ found 11 bugs across 6 zkVMs) are addressing the implementation gap.
- Governance override (Layer 7): Stage 2 maturation will eventually remove governance as an attack surface.
- Quantum vulnerability (Layer 6): lattice-based and hash-based primitives provide migration paths.

But "trustless" -- meaning zero residual trust assumptions -- requires proving that hardware does not leak (impossible without information-theoretic security), proving that all software is correct (requiring formal verification of the entire stack), and proving that mathematical hardness assumptions hold (which is inherently impossible -- hardness is a conjecture, not a theorem).

The honest trajectory: trust will continue to decrease, asymptotically approaching but never reaching zero. "Trust-minimized, and getting better every day" is the accurate description. Like Zeno's arrow, the gap closes by half with each advance. Zero is not the destination. The asymptote is the destination, and it is a good one.

But the Zeno metaphor deserves to be pushed harder, because it reveals something the optimistic narrative glosses over. Each layer's trust assumption is shrinking independently. Layer 2 gets safer as formal verification improves. Layer 5 gets safer as transcript standardization matures. Layer 6 gets safer as lattice assumptions are studied. Layer 7 gets safer as governance decentralizes. Viewed individually, each trend is encouraging. But the system's overall trustworthiness is not the average of its layers -- it is the *conjunction*. All seven must hold simultaneously. If any single layer fails, the system fails.

This is the Zeno's paradox of trust in its precise form. Suppose each layer independently has a 99% chance of holding its trust assumption. Seven independent layers at 99% each give a system-level confidence of $0.99^7 \approx 93.2\%$. Improve each layer to 99.9% and the system reaches 99.3%. Improve to 99.99% and you get 99.93%. The system-level confidence always trails the weakest layer, and the gap between layer-level confidence and system-level confidence grows with the number of layers. Adding layers -- which is what happens as the stack matures and new trust assumptions are identified -- makes the individual layers stronger but the conjunction weaker.

This is not a reason for despair. It is a reason for precision. The trajectory toward trust-minimization is real, but the conjunction effect means that "almost trustless" is a category error. A system with six perfect layers and one compromised layer is not "mostly trustless" -- it is compromised. The chain is as strong as its weakest link, and a seven-link chain has seven opportunities for weakness.

The practical implication is that the field needs to track system-level trust, not layer-level trust. A dashboard showing "Layer 2: formally verified, Layer 5: standardized transcripts, Layer 6: post-quantum ready, Layer 7: Stage 1.5" tells you about components. It does not tell you about the system. The system-level question is: what is the probability that *all seven* hold simultaneously for *this specific deployment* with *this specific configuration*? Nobody can answer that question today. Developing the methodology to answer it -- a kind of actuarial science for cryptographic trust -- is itself an open research problem. What would such a discipline look like? It would assign per-layer failure probabilities based on empirical evidence: Layer 2 failure rate derived from the historical frequency of under-constrained bugs per circuit (67% of all SNARK vulnerabilities, per the Chaliasos SoK); Layer 5 failure rate derived from Fiat-Shamir implementation bugs (Frozen Heart affected 6 implementations across 3 proof systems); Layer 7 failure rate derived from governance attacks (Beanstalk and Tornado Cash as data points). It would compute the conjunction probability for specific deployments. And it would flag the most dangerous failure mode: simultaneous failure of Layer 2 and Layer 7, where a buggy circuit (Layer 2) is exploited through a governance override (Layer 7), making the theft both undetectable by the proof system and unrecoverable through governance. This is the conjunction scenario that no individual layer analysis would catch.

The deepest version of this question is philosophical, not technical. Is there a fundamental lower bound on residual trust, the way there is a fundamental lower bound on measurement uncertainty in quantum mechanics? Can we prove that *any* computational system, no matter how carefully designed, must retain some irreducible trust assumption? The answer is almost certainly yes -- you always trust that the laws of physics haven't changed, that your hardware is computing what you think it's computing, that the mathematical axioms underlying the proofs are consistent. But articulating exactly where that floor sits, and how close current systems are to reaching it, would transform "trust-minimized" from a vague aspiration into a measurable engineering target. The person who defines that floor will have done for cryptographic trust what Shannon did for information capacity: turned an intuition into a theorem with a number attached to it.

**Executive Risk:** Marketing claims exceed technical reality. Organizations deploying 'trustless' systems inherit seven trust assumptions they may not have assessed. Due diligence must enumerate all seven. **Timeline:** Ongoing.

### Question 5: How do streaming witness approaches interact with folding?

Nair et al. (2025) demonstrated streaming witness generation that uses space proportional to trace width (registers) rather than trace length (steps). This is essential for proving long computations without requiring hundreds of gigabytes of RAM. But folding schemes (Nova, HyperNova, LatticeFold) accumulate state across folding steps -- the accumulated instance grows with each fold. How streaming witnesses interact with accumulating folding state is an open architectural question.

This matters because folding and streaming attack different bottlenecks: folding reduces prover time by avoiding redundant computation; streaming reduces prover memory by generating witness chunks on-the-fly. An architecture that combines both would be strictly superior to either alone, but the interaction is non-trivial. Two good ideas that have not yet learned to dance together.

The architectural tension runs deeper than a scheduling problem. It is a fundamental conflict between two strategies for managing state.

Folding *accumulates* state. Each folding step takes the current accumulated instance and a new instance and produces a new accumulated instance that absorbs both. In Nova, this means the error vector $\mathbf{E}$ grows -- or more precisely, the relaxed R1CS instance carries forward information about all previous folding steps. In LatticeFold, the accumulated witness includes norm-bounded vectors whose bounds increase with each fold. The accumulator is the memory of the system. It remembers everything that has been folded into it. That memory is what makes folding powerful: the verifier checks a single accumulated instance at the end, rather than checking each step individually. But that memory has a cost. The accumulated state must be stored, updated, and eventually opened. It cannot be discarded mid-computation.

Streaming *discards* state. The entire point of streaming witness generation is to produce a chunk of the witness, use it, and then forget it. The prover's memory footprint stays proportional to the width of the computation (how many registers the program uses) rather than its length (how many steps the program takes). A streaming prover for a billion-step computation uses the same memory as a streaming prover for a million-step computation. That is the magic. But it works only if the prover can forget the past. The moment you require the prover to retain information about earlier chunks -- which is exactly what folding demands -- the streaming property degrades.

The crux is this: folding needs the prover to remember the accumulated error from all previous steps. Streaming needs the prover to forget the witness from all previous steps. These are not the same thing. The accumulated error is a compact summary (a single relaxed instance), while the witness is a massive expansion (the full execution trace). In principle, you can stream the witness while retaining only the accumulated instance. In practice, the folding step itself requires access to both the accumulated witness *and* the new witness chunk simultaneously, because the folding combiner must compute cross-terms between old and new. Those cross-terms are the technical barrier.

One possible resolution: a folding scheme where the cross-terms can be computed incrementally, using only the compact accumulated instance and the current witness chunk, without ever materializing the full accumulated witness. This would require the cross-term computation to be decomposable into a streaming-friendly form -- which is a non-trivial algebraic constraint on the folding scheme's structure. Nova's cross-term involves an inner product between the accumulated witness and a matrix applied to the new witness. That inner product can, in principle, be computed in a streaming fashion if the matrix-vector product is streamed. But the accumulated witness itself is not compact; it is as large as the original witness. The circularity is apparent.

A different resolution: a layered architecture where streaming operates within each folding step and folding operates across steps. Generate the witness for step $k$ using streaming (small memory), fold it into the accumulator (small memory for the accumulator, large memory transiently for the fold), then discard the witness for step $k$ and move to step $k+1$. The peak memory is determined by the single-step witness size plus the accumulator size, not by the total trace length. This is closer to what practical implementations will likely achieve, but it requires that each folding step can be completed before the next witness chunk is generated -- which imposes a sequential dependency between folding and witness generation that limits parallelism.

Nobody has built an architecture that resolves all three constraints simultaneously: streaming memory, folding time-savings, and parallel execution. The system that does will dominate the proving market for the next generation of zkVMs. It is the kind of problem where the first correct solution will seem obvious in retrospect and impossible in prospect -- which is the surest sign that it is worth working on.

**Executive Risk:** Memory requirements constrain prover hardware to high-end data center configurations, limiting decentralization and increasing vendor lock-in. **Timeline:** 2-3 years for streaming witness architectures to mature.

### Question 6: Can constant-time ZK proving be made practical?

Side-channel attacks on ZK implementations -- timing attacks on Zcash's Groth16 prover ($R = 0.57$ correlation with transaction amounts), cache timing leakages in Poseidon/Reinforced Concrete/Tip5, electromagnetic emanation from field arithmetic -- demonstrate that "zero-knowledge" is a mathematical property, not an implementation guarantee. The proof reveals nothing in theory. The hardware whispers everything in practice.

Constant-time implementations exist (Monero's Bulletproofs prover achieves $R = 0.04$ correlation) but impose significant performance costs. GPU proving complicates this further: GPUs execute in SIMT (Single Instruction, Multiple Thread) mode, where thread divergence is observable. Constant-time code creates artificial thread divergence, reducing GPU utilization. The tension between side-channel resistance and hardware throughput has no known resolution. The backstage walls need to be soundproofed, but soundproofing slows down the preparation.

The GPU problem is worth understanding in detail, because it illustrates why this is not simply a matter of writing more careful code.

A GPU does not execute threads independently. It executes them in *warps* -- groups of 32 threads (on NVIDIA hardware) that share a single instruction pointer. When all 32 threads in a warp take the same branch, the warp executes at full speed. When threads diverge -- some taking the `if` branch, others taking the `else` branch -- the warp must execute *both* branches serially, masking out the threads that shouldn't participate in each branch. This is thread divergence, and it is the fundamental mechanism by which GPUs trade flexibility for throughput.

Constant-time code, by definition, must execute the same instructions regardless of the input. In a CPU, this means taking both branches and selecting the result with a conditional move -- a small overhead, typically 2x or less. In a GPU, this means *forcing* all 32 threads in a warp to execute both branches even when all 32 threads would naturally take the same branch. The constant-time requirement converts natural coherence (all threads agree) into artificial divergence (all threads must pretend to disagree). On a CPU, constant-time code is slower by a constant factor. On a GPU, constant-time code destroys the execution model's fundamental assumption.

The numbers are stark. A well-optimized GPU NTT can achieve 80-90% of theoretical throughput because the computation is uniform: every thread does the same butterfly operation on different data. A constant-time GPU implementation of the same NTT -- one that pads all branches to equal length and eliminates data-dependent memory access patterns -- drops to 30-50% throughput. The field arithmetic itself (modular addition, modular multiplication) can be made constant-time without much overhead, because it is naturally branchless. But the *control flow* of the proving algorithm -- which polynomials to evaluate, which commitment rounds to perform, how to handle edge cases in the MSM bucket accumulation -- is where the branches live, and where constant-time enforcement hurts.

This creates a stark engineering tradeoff. On one side: constant-time code on CPU. Viable, proven (Monero does it), but slow. A CPU prover is 10-50x slower than a GPU prover. On the other side: variable-time code on GPU. Fast, but the timing variations leak information about the witness through observable channels. The proving time itself becomes a side channel. An attacker who can measure how long your proof took can infer something about your private input -- exactly the information the zero-knowledge property is supposed to hide.

No current system offers both. No current system even articulates a clear path to offering both. The approaches being explored -- oblivious RAM for memory access patterns, garbled circuits for branching logic, hardware enclaves for execution isolation -- each solve part of the problem while introducing new trust assumptions. Oblivious RAM has logarithmic overhead that compounds badly at GPU scale. Garbled circuits are designed for two-party computation, not single-prover execution. Hardware enclaves (SGX, TrustZone) are the very kind of trusted hardware that ZK proofs were supposed to make unnecessary.

The resolution, when it comes, will likely involve a new hardware abstraction: a proving accelerator designed from the ground up for constant-time cryptographic computation, where the SIMT model is replaced by a model that treats uniform execution time as a feature rather than a constraint. Such hardware does not exist. Designing it is an open problem at the intersection of chip architecture, cryptographic engineering, and side-channel analysis. The person who designs it will need to understand all three. That is a rare combination, which is why the problem remains open.

**Executive Risk:** Privacy leaks through side channels in production. Proving time correlates with transaction characteristics (demonstrated $R = 0.57$ in Zcash). Systems marketed as 'private' may leak information to network observers. **Timeline:** 3-5 years for constant-time provers to become standard.

### Question 7: Is "seven" the right number of layers?

The evidence suggests that the seven-layer model is pedagogically useful but architecturally approximate. Layers 3 and 4 collapse in Jolt. Layers 4, 5, and 6 form an inseparable "proof core." STARK-to-SNARK wrapping pierces Layers 5, 6, and 7. Data availability and proof aggregation are substantial infrastructure layers not represented. Privacy is a cross-cutting concern, not a single-layer property.

The model might be better as four macro-layers: (1) Trust Setup, (2) Programming Model, (3) Proof Core {witness + arithmetization + proof system + primitives}, (4) On-Chain Settlement {verification + data availability + governance}. Or it might be better as nine layers, adding data availability and proof aggregation explicitly. Or seven might be exactly right for the pedagogical purpose it serves, with explicit acknowledgment that production systems do not respect the boundaries.

The question is not academic. The number of layers determines how people think about the system, which determines which design decisions they consider independent (and thus can optimize separately) versus coupled (and must co-design). Getting the decomposition wrong leads to suboptimal architectures. Getting it right enables the field to progress faster. The map shapes the territory.

The practical cost of a wrong decomposition is already visible. Consider Layers 4 and 5 in this book's model -- the arithmetization layer and the proof system layer. The model presents them as separate, and this separation is conceptually clean: one translates the program into equations, the other proves the equations are satisfied. Different teams can work on each. Different papers can advance each. Different benchmarks can measure each. The separation enables a division of labor that has served the field well.

But in practice, Layers 4 and 5 are deeply coupled. The arithmetization's structure determines which proof system can operate on it efficiently. R1CS works naturally with Groth16 and Nova. AIR works naturally with STARKs. CCS works naturally with HyperNova. Choosing an arithmetization *is* choosing a family of proof systems, and choosing a proof system constrains the arithmetization. Teams that optimize Layer 4 independently of Layer 5 -- designing a beautiful arithmetization and then discovering that no efficient proof system can consume it -- have wasted months of work. This has happened. It will happen again whenever the model's boundaries do not match reality's boundaries.

The same coupling appears between Layers 3 and 4. Jolt demonstrated this forcefully: in Jolt's architecture, the witness *is* the arithmetization. There is no separate "witness generation" step followed by a "constraint compilation" step. The lookup table that defines the instruction semantics simultaneously serves as the witness and the constraint. Trying to optimize "witness generation" and "arithmetization" separately in Jolt is like trying to optimize a coin's heads and tails independently. They are the same object viewed from two angles.

The four-macro-layer model -- Trust Setup, Programming Model, Proof Core, On-Chain Settlement -- has the virtue of grouping the coupled components together. The "Proof Core" macro-layer acknowledges that witness generation, arithmetization, the proof system, and the underlying primitives are a single coupled system that must be co-designed. But it loses granularity. It tells the proof-core team "this is all yours" without helping them understand the internal structure of their subsystem.

The nine-layer model -- adding data availability and proof aggregation as explicit layers -- has the virtue of representing real infrastructure that the seven-layer model ignores. Data availability is not a detail. It is a trust assumption as fundamental as any in the stack: if the data is not available, the proof is unverifiable in practice, regardless of its mathematical soundness. Proof aggregation -- the recursive composition of proofs into proofs-of-proofs -- is the mechanism that makes ZK rollups economically viable, and it introduces its own trust assumptions (the aggregation circuit must be correct, the recursive verifier must be sound). Omitting these from the model means omitting trust assumptions from the analysis, which defeats the model's purpose.

The right answer may not be a fixed number at all. It may be that the useful decomposition depends on the question you are asking. If you are asking "how does trust flow through a ZK system," seven layers (or nine, or four) provide different but complementary views. If you are asking "how should engineering teams be organized," the coupling structure matters more than the layer count. If you are asking "what can go wrong," the answer is a threat model, not a layer diagram, and the threat model cuts across every decomposition.

The OSI model survived not because seven was the right number of layers for networking -- it was widely criticized for being both too many and too few, depending on context -- but because it gave a generation of engineers a shared vocabulary. This book's seven-layer model will succeed or fail on the same terms. If it gives ZK engineers a shared vocabulary for discussing trust assumptions, it will have served its purpose even if no production system has exactly seven layers. If a better decomposition emerges -- one that captures the couplings, represents the missing layers, and scales from pedagogy to production -- it should replace this one without ceremony. The goal was never to be right about the number. The goal was to be useful about the structure.

**Executive Risk:** Low. This is a pedagogical question, not a deployment risk. The layer model is a communication tool; systems work regardless of how we categorize their components.


## Summary

Seven concrete research blockers define the field's near-term ceiling: GPU witness parallelism, post-quantum proof-size lower bounds, Stage 2 governance binding, reduction of trust assumptions, streaming-folding integration, constant-time proving, and the correct layer count. Each has quantified timelines and executive-level risk assessments; none is solved as of early 2026.

## Key claims

- Witness generation accounts for 50-70% of total GPU proving time; ZKPOG achieved 22.8x speedup but the general case remains open (timeline: 2-4 years)
- KZG proofs are 48 bytes; best lattice proofs are 50-100 KB — a 3-order-of-magnitude gap with no proven lower bound on whether $O(1)$ post-quantum proofs are possible
- As of early 2026, most ZK rollups are Stage 0 or Stage 1; >$20B TVL remains governance-overridable, negating Layers 1-6 cryptographic guarantees
- System-level trust is the conjunction of all seven layers: seven layers each at 99.9% reliability yield only 99.3% system confidence ($0.999^7$)
- Frozen Heart vulnerability affected 6 implementations across 3 proof systems; ARGUZZ found 11 bugs across 6 zkVMs
- Zcash's Groth16 prover exhibits $R = 0.57$ timing correlation with transaction amounts; Monero's Bulletproofs achieves $R = 0.04$ with constant-time implementation at higher CPU cost
- Layers 3-4 collapse in Jolt (witness = arithmetization); Layers 4-5-6 form an inseparable proof core — the seven-layer model is pedagogically useful but architecturally approximate

## Entities

- [[arithmetization]]
- [[beanstalk]]
- [[boneh]]
- [[bulletproofs]]
- [[fiat-shamir]]
- [[folding]]
- [[fri]]
- [[groth16]]
- [[hypernova]]
- [[jolt]]
- [[kzg]]
- [[l2beat]]
- [[lasso]]
- [[latticefold]]
- [[lattice]]
- [[nova]]
- [[ntt]]
- [[ntts]]
- [[nvidia]]
- [[poseidon]]
- [[setty]]
- [[starks]]
- [[tornado cash]]
- [[zcash]]

## Dependencies

- [[ch04-witness-generation-costs]] — establishes the 50-70% witness share in GPU proving pipelines that motivates Q1
- [[ch07-the-trilemma-and-its-dissolution]] — introduces the transparency/post-quantum/succinctness trilemma underlying Q2
- [[ch08-governance-the-achilles-heel]] — Stages framework (L2Beat) and governance-override risk behind Q3
- [[ch10-trust-decomposition-seven-weaker-assumptions]] — the seven-layer trust conjunction that Q4 quantifies
- [[ch06-the-folding-genealogy]] — Nova/HyperNova/LatticeFold state accumulation that makes Q5's streaming interaction non-trivial
- [[ch04-side-channel-attacks-when-the-walls-leak]] — Zcash timing correlation ($R = 0.57$) and GPU SIMT divergence problem behind Q6

## Sources cited

- Nair, Vineet, Justin Thaler, and Michael Zhu. "Proving CPU Executions in Small Space." ePrint 2025/611. [Q1, Q5]
- Ozdemir, Alex, Evan Laufer, and Dan Boneh. "Volatile and Persistent Memory for zkSNARKs via Algebraic Interactive Proofs." *IEEE S&P 2025*. ePrint 2024/979. [Q1]
- Pailoor, Shankara, et al. "Automated Detection of Under-Constrained Circuits in Zero-Knowledge Proofs." *PLDI 2023*. ePrint 2023/512. [Q4]
- Wen, Hongbo, et al. "Practical Security Analysis of Zero-Knowledge Proof Circuits." *USENIX Security 2024*. ePrint 2023/190. [Q4]
- Hochrainer, Christoph, Valentin Wustholz, and Maria Christakis. "Arguzz: Testing zkVMs for Soundness and Completeness Bugs." arXiv 2509.10819, 2025. [Q4]
- Wee, Hoeteck and David J. Wu. "Lattice-Based Functional Commitments: Fast Verification and Cryptanalysis." *ASIACRYPT 2023*. ePrint 2024/028. [Q2]
- L2Beat. "Stages Framework for L2 Maturity." https://l2beat.com/stages. Accessed March 2026. [Q3]
- Trail of Bits. "Frozen Heart: Forgery of Zero Knowledge Proofs." Blog post, April 2022. [Q4]
- Chaliasos, Stefanos, et al. "SoK: What Don't We Know? Understanding Security Vulnerabilities in SNARKs." *USENIX Security Symposium*, 2024. [Q4]

## Open questions

- Q1: Can witness generation be made fully parallel on GPUs? (Timeline: 2-4 years)
- Q2: What is the proven lower bound on post-quantum proof size? Is $O(1)$-size post-quantum proof possible? (Timeline: 5-10 years theoretical)
- Q3: When will Stage 2 governance binding occur for ZK rollups? (Timeline: 1-3 years)
- Q4: When will "trustless" become a measurable engineering target with a defined trust floor? (Timeline: ongoing)
- Q5: How do streaming witness approaches interact with folding scheme state accumulation? (Timeline: 2-3 years)
- Q6: Can constant-time ZK proving be made practical on GPU hardware? (Timeline: 3-5 years)
- Q7: Is seven the right number of layers, or should the model be four macro-layers, nine layers, or something else?

## Improvement notes

- [P1] (A) Q2 describes Wee-Wu's work as "compact functional encryption and related primitives" but ePrint 2024/028 is titled "Lattice-Based Functional Commitments: Fast Verification and Cryptanalysis" — not functional encryption. The characterisation is imprecise and should be corrected to functional commitments.
- [P2] (A) Q1 states GPU proving achieves "10-50x speedups via NTT and MSM parallelism"; ch04 consistently states "10 to 100 times faster." The upper bound is understated.
- [P3] (B) Wee-Wu citation lists venue as "ASIACRYPT 2023" with ePrint 2024/028 — the ePrint number postdates the conference year by a year. The ePrint number should be verified (likely 2023/xxx for a 2023 proceedings paper).
- [P3] (C) "ARGUZZ" in Q4 body text is inconsistent with "Arguzz" in the Sources cited block and the title in the bibliography. Use consistent capitalisation throughout.

## Links

- Up: [[14-open-questions-and-the-road-ahead]]
- Prev: —
- Next: [[ch14-the-three-frontiers]]
