---
title: "Three zkVMs Through Seven Layers"
slug: ch11-three-zkvms-through-seven-layers
chapter: 11
chapter_title: "zkVMs -- The Universal Stage"
heading_level: 2
source_lines: [4596, 4679]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 2326
---

## Three zkVMs Through Seven Layers

The best way to understand why the seven-layer model bends under zkVM pressure is to trace three representative systems through all seven layers. Watch how they cross the same territory by different routes.

### SP1 Hypercube: The General-Purpose Champion

**Layer 1 (Setup).** Hybrid -- transparent inner loop (hash-based Poseidon2 over BabyBear), trusted outer wrap (Groth16 over BN254). The KZG ceremony is for the wrapper only. This demonstrates that the trusted-or-transparent choice is actually "both."

**Layer 2 (ISA).** RISC-V (RV32IM). Developers write ordinary Rust; the compiler handles the rest. SP1 implements 39+ RISC-V instructions, with all 62 core opcodes formally verified against the official RISC-V Sail specification.

**Layer 3 (Witness).** Shard-based execution traces with continuations. Each shard is an independent proving unit; "shared challenges" enforce consistency at shard boundaries. This is where the Witness Gap lives -- SP1's witness generation is CPU-bound while its proving is GPU-accelerated, meaning witness generation consumes an estimated 60-70% of total proving time.

**Layer 4 (Arithmetization).** Multi-table AIR with LogUp-GKR cross-table lookups over multilinear polynomials. Each RISC-V instruction type has its own constraint table ("chip"). Precompiles (SHA-256, Keccak, secp256k1) are independent STARK tables connected via LogUp.

**Layer 5 (Proof).** Four-stage pipeline: core STARK proof per shard, recursive compression, shrink (field transition), Groth16 wrap. Proves 99.7% of Ethereum L1 blocks in under 12 seconds on 16 RTX 5090 GPUs.

**Layer 6 (Primitives).** BabyBear field (31-bit), Poseidon2 hash, Jagged PCS (commits only to occupied trace rows, eliminating padding waste), FRI-based commitment.

**Layer 7 (Verifier).** Groth16 on-chain verification at approximately 250-300K gas on any EVM chain. Live on Ethereum mainnet via the Succinct Prover Network.

**What makes SP1 architecturally distinctive.** SP1 Hypercube is an exercise in *factoring a monolithic problem into independent pieces and then reassembling them under a single algebraic umbrella*. The system's defining architectural idea is not any single layer but the interaction between three design choices that reinforce each other. First, the multi-table AIR architecture assigns each RISC-V opcode its own constraint table -- a "chip" -- so that the constraint degree and column count for a SHA-256 precompile need not compromise the constraint shape for a simple register-to-register add. Second, LogUp-GKR cross-table lookups bind these independent chips together using sumcheck over multilinear extensions, which avoids the quadratic blowup that a naive permutation argument would impose as chip count grows. Third, sharding with continuation challenges means that execution traces of arbitrary length can be sliced into fixed-size proving units, each provable in parallel on a separate GPU, with algebraic consistency enforced by shared random challenges drawn after the shards are committed.

The result is a system that scales *horizontally* in two independent dimensions: more instruction types (more chips) and longer executions (more shards). Adding a new precompile -- say, a BLS12-381 pairing for Ethereum validator operations -- requires only a new chip table and new LogUp entries; existing chips and the recursive compression pipeline remain unchanged. This modular extensibility explains why SP1 has accumulated over 39 instruction types and counting, whereas architectures with monolithic trace layouts face painful refactoring when adding even one new opcode.

The Jagged PCS matters just as much. Standard polynomial commitment schemes commit to a fixed-size domain, which means that a chip with 10,000 occupied rows in a shard of capacity $2^{20}$ wastes commitment work on a million empty rows. Jagged PCS commits only to the non-trivial portion, eliminating padding overhead. In practice, most shards have a few "hot" chips (ALU, memory) and many "cold" chips (uncommon opcodes). Without Jagged PCS, the cold chips would dominate commitment cost despite contributing almost nothing to the computation. With it, proving cost tracks actual computation, not worst-case table size.

SP1's four-stage pipeline -- core STARK per shard, recursive compression, field-transition shrink, Groth16 wrap -- is also a study in staged trust assumptions. The inner stages are fully transparent, hash-based, and post-quantum resilient. Only the final wrap introduces a trusted setup and classical-security assumption. If and when a post-quantum on-chain verifier becomes practical, SP1 can drop the Groth16 stage and expose the transparent inner proof directly. The architecture is built to survive the quantum transition, not merely to endure it.

### Stwo/Cairo: The ZK-Native ISA Champion

**Layer 1.** Fully transparent (hash-based). For Ethereum L1 settlement, a Groth16 wrapper exists via Herodotus, but the primary pipeline remains STARK-native.

**Layer 2.** Cairo -- a custom ISA designed to minimize arithmetization cost. Here the model's top-down flow inverts. The ISA *is* the constraint system, by design. Layer 4 requirements shaped Layer 2. The choreography was written to serve the stage machinery, not the other way around.

**Layer 3.** Cairo VM execution producing columnar M31 traces. The field choice is baked into the VM itself, not merely the proving step -- a deeper coupling than in RISC-V zkVMs.

**Layer 4.** Flat AIR with one component per instruction, LogUp cross-component lookups, mixed-degree constraints. Circle STARKs use the circle group over M31 (where $p+1 = 2^{31}$ is a power of two) to enable FFTs over a field that lacks large multiplicative subgroups.

**Layer 5.** Circle STARK with SHARP aggregation. Approximately 100x faster than its predecessor Stone. Live on Starknet mainnet since November 2025.

**Layer 6.** M31 field (31-bit). M31 arithmetic is approximately 125x faster than the 252-bit Stark field used by Stone. The field choice *created* the need for Circle STARKs -- the strongest example of Layer 6 forcing a Layer 5 invention.

**Layer 7.** Native STARK verification on Starknet (no wrapping needed). For Ethereum L1: SHARP-aggregated Groth16.

**What makes Stwo architecturally distinctive.** Stwo is what happens when you design the entire stack backward from a single mathematical insight: *the group of points on the circle $x^2 + y^2 = 1$ over a Mersenne prime has order $p+1$, and when $p = 2^{31} - 1$, that order is exactly $2^{31}$ -- a power of two*. This accident of number theory is the seed from which the entire Stwo architecture grows.

Conventional STARKs require a field with large multiplicative subgroups for FFT-based polynomial evaluation. The Mersenne prime $M31 = 2^{31} - 1$ has no such subgroups -- its multiplicative group has order $2^{31} - 2$, which factors badly. A naive approach would disqualify M31 from STARK construction entirely. Circle STARKs solve this by abandoning the multiplicative group in favor of the circle group, where the "FFT" becomes a circle-group analog (the Circle Number Theoretic Transform). The evaluation domain is the set of points on the unit circle over $\mathbb{F}_{M31}$, not the powers of a generator in $\mathbb{F}_{M31}^*$. This is not a minor algebraic substitution; it requires rethinking polynomial commitments, coset structures, and FRI queries from the ground up.

The payoff is a 125x speedup. M31 arithmetic -- 31-bit integer addition and multiplication with a single modular reduction -- maps directly onto 32-bit CPU and GPU instructions with no multi-precision overhead. A single SIMD lane processes one field element. Compare this with the 252-bit Stark field used by Stone, where each field multiplication requires multiple 64-bit limb operations and carry propagation. The measured 125x speedup over Stone is not a software optimization; it is a consequence of matching the algebraic structure to the hardware word size.

Cairo's role is just as distinctive. Where RISC-V zkVMs treat the ISA and the constraint system as separate concerns -- the ISA defines computation, the arithmetization encodes it -- Cairo *collapses the two*. A Cairo instruction is simultaneously a machine operation and a set of polynomial constraints. The compiler does not translate programs into constraints; it emits programs that *are* constraints. This eliminates the "arithmetization tax" that RISC-V zkVMs pay: the overhead of encoding a general-purpose instruction (designed for silicon hardware) into an algebraic form (designed for polynomial provers). Gassmann et al.'s finding that standard LLVM optimizations yield 40% improvement on RISC-V zkVMs -- because LLVM optimizes for caches and branch predictors that do not exist in ZK execution -- quantifies exactly the tax that Cairo avoids.

The SHARP (Shared Prover) aggregation layer adds a dimension absent from SP1 and Jolt: *amortization across applications*. SHARP batches proofs from multiple independent Starknet applications into a single recursive proof, so that the fixed cost of Ethereum L1 verification is shared among all applications that submit proofs in the same batch window. This is economic aggregation, not just cryptographic recursion. A small contract with ten transactions per hour pays a fraction of the L1 verification cost that it would bear alone. The theater shares its rent among all the acts on stage.

The trade-off is ecosystem lock-in. Cairo is not Rust, not C, not any language with a pre-existing developer community of millions. Every Cairo developer is a developer that StarkWare's ecosystem must recruit and train. The Kakarot project -- an EVM interpreter written in Cairo, running on Stwo -- is the architectural hedge: it lets Ethereum developers write Solidity while Cairo and Stwo handle the proving underneath. Whether this bridge is sturdy enough to carry mainstream adoption is the open strategic question.

### Jolt: The Lookup Singularity Pioneer

**Layer 1.** Trusted (Hyrax/Pedersen commitments), with transparent alternatives planned (Basefold in Jolt-b).

**Layer 2.** RISC-V (RV32I). Same as SP1, but the divergence begins at Layer 4.

**Layer 3.** Every instruction is decomposed into lookups on small subtables. Witness generation *is* the arithmetization -- no meaningful boundary exists between Layers 3 and 4. This is the first crack in the seven-layer model. The backstage preparation and the encoding of the trick are the same act.

**Layer 4.** Lookup-based arithmetization via Lasso. Instead of encoding each operation as constraints, the system verifies every step against pre-approved entries in a comprehensive reference table. A thin R1CS wrapper (~60 constraints per cycle) handles control flow via Spartan. This is a genuinely distinct paradigm from AIR, PLONKish, or CCS.

**Layer 5.** Sumcheck-based proving. No recursion in production; no STARK-to-SNARK wrapping pipeline. Approximately 6x faster than RISC Zero on initial benchmarks, but the gap has narrowed with GPU acceleration.

**Layer 6.** BN254 scalar field (256-bit). 256-bit field operations are approximately 100x more expensive per operation than 31-bit, but Jolt compensates by performing far fewer operations per CPU step.

**Layer 7.** No production on-chain verifier. This is Jolt's most significant gap relative to SP1 and Stwo. The trick is performed brilliantly, but the theater has no box office.

**What makes Jolt architecturally distinctive.** Jolt is the most radical of the three systems, because it asks a question that the other two never consider: *what if we stopped writing constraints entirely?* SP1 and Stwo both encode computation as polynomial constraints -- they differ in how they organize and evaluate those constraints, but both accept the premise that proving a computation means constraining it. Jolt rejects this premise. In Jolt, proving a computation means *looking it up*.

The core insight, which Jolt inherits from the Lasso lookup argument, is that any function on small inputs can be represented as a table. A 32-bit addition is a function from two 16-bit operands to a 17-bit result -- a table with $2^{32}$ entries. Proving that "a + b = c" does not require writing a constraint that the prover satisfies; it requires showing that the triple (a, b, c) appears in the addition table. The prover's obligation shifts from "solve this system of equations" to "demonstrate membership in this pre-computed set." This is not a small change in formalism. It is a different epistemology of computation.

The practical problem is that $2^{32}$-entry tables are too large to materialize. Lasso solves this by decomposing large lookups into combinations of small subtable lookups, using the algebraic structure of the operations themselves. Addition decomposes by limbs; bitwise operations decompose by individual bits; shifts decompose by position. Each subtable is small enough to commit to directly -- typically $2^{16}$ entries or fewer. The Lasso sumcheck protocol then proves that the decomposed lookups are consistent with the original instruction. The result is a system where the per-instruction proving cost scales with the *decomposability* of the instruction, not with the number of constraints needed to describe it.

This decomposition is why Jolt's Layer 3 and Layer 4 merge into a single act. In SP1, the witness (Layer 3) is an execution trace -- a table of register states and memory values at each cycle -- and the arithmetization (Layer 4) is a set of polynomial constraints that the trace must satisfy. These are conceptually and computationally distinct stages. In Jolt, the "witness" for each instruction *is* the lookup decomposition: the set of subtable indices and values that reconstruct the instruction's behavior. Generating the witness and performing the arithmetization are the same computation, executed in a single pass. There is no moment where "the trace is ready and now we constrain it." The trace is the constraint.

The choice of BN254 as the base field is worth examining. SP1 and Stwo chose 31-bit fields for raw throughput, accepting hash-based commitments and transparent proofs. Jolt chose a 256-bit elliptic-curve field, accepting 100x slower per-operation arithmetic, because BN254 enables Hyrax commitments -- a multi-scalar-multiplication-based polynomial commitment scheme with *no trusted setup* and *logarithmic* verification time. Hyrax commitments over BN254 are the reason Jolt avoids both a ceremony (unlike Groth16 wrappers) and hash-chain verification (unlike FRI). The field choice is not a performance concession; it is a commitment-scheme selection that happens to be expensive.

Jolt's current absence of a production on-chain verifier is not merely an engineering gap waiting to be filled. It reflects a deeper tension: the sumcheck-based proving paradigm produces proofs whose verification cost does not compress as neatly into the constant-size Groth16 format that Ethereum L1 expects. The planned Jolt-b variant, which replaces Hyrax with Basefold (a hash-based, transparent commitment scheme), would enable a more conventional STARK-to-SNARK wrapping pipeline. But this replacement changes Jolt's security model -- from discrete-log hardness to hash collision resistance -- and alters the system's identity. Whether Jolt can ship a verifier without becoming a different system is the question that will determine whether the lookup singularity remains a research landmark or becomes a production architecture.


## Summary

SP1, Stwo/Cairo, and Jolt each traverse the seven layers by a distinct route: SP1 via modular multi-table AIR with horizontal sharding; Stwo via a ZK-native ISA that collapses Layers 2 and 4; Jolt via lookup-based arithmetization that merges Layers 3 and 4. The seven-layer model does not break under this pressure -- it reveals that layers fuse differently in each design.

## Key claims

- SP1 witness generation consumes ~60-70% of total proving time (CPU-bound while proving is GPU-accelerated).
- SP1 Jagged PCS commits only to occupied trace rows, eliminating padding overhead.
- SP1 four-stage pipeline: core STARK per shard → recursive compression → field-transition shrink → Groth16 wrap.
- Stwo M31 field arithmetic is ~125x faster than the 252-bit Stark field used by Stone.
- Cairo Layer 4 requirements shaped Layer 2: the ISA is the constraint system.
- Gassmann et al. (2025) found standard LLVM optimizations yield >40% improvement on RISC-V zkVMs.
- Jolt Layers 3 and 4 merge: witness generation is the arithmetization (lookup decomposition).
- Jolt BN254 field ops are ~100x more expensive per operation than 31-bit fields.
- Jolt has no production on-chain verifier as of March 2026.
- SP1 99.7% of Ethereum L1 blocks proved under 12 s on 16 RTX 5090 GPUs.

## Entities

- [[arithmetization]]
- [[babybear]]
- [[bls12-381]]
- [[bn254]]
- [[circle stark]]
- [[ceremony]]
- [[fri]]
- [[groth16]]
- [[jolt]]
- [[kzg]]
- [[lasso]]
- [[logup]]
- [[mersenne]]
- [[midnight]]
- [[pedersen]]
- [[plonk]]
- [[poseidon]]
- [[spartan]]
- [[starks]]
- [[starknet]]

## Dependencies

- [[ch11-the-landscape-table-march-2026]] — this section elaborates the SP1/Stwo/Jolt rows
- [[ch11-the-proof-core-triad]] — the coupling observed here is formalized there
- [[ch10-path-one-the-hybrid-stark-to-snark-pipeline]] — SP1's four-stage pipeline in prior-chapter context
- [[ch06-circle-starks-and-stwo-a-generational-leap]] — Circle STARK background for the Stwo section
- [[ch05-lookup-arguments]] — Lasso and LogUp underpinning Jolt and SP1

## Sources cited

- Gassmann et al. (2025) — compiler optimization study finding >40% LLVM improvement on RISC-V zkVMs

## Open questions

- Can Jolt ship a production on-chain verifier without switching from sumcheck to a STARK-to-SNARK pipeline (Jolt-b)?

## Improvement notes

- [P0] (A) Jolt Layer 1 is described as "Trusted (Hyrax/Pedersen commitments)" — Hyrax is a *transparent*, trust-free polynomial commitment scheme based on inner-product arguments over elliptic curves; it requires no trusted setup. Labelling Jolt Layer 1 as "Trusted" is incorrect.
- [P1] (A) Speed comparison for Stwo: Layer 5 entry says "approximately 100x faster than its predecessor Stone" but Layer 6 entry says "M31 arithmetic is approximately 125x faster than the 252-bit Stark field used by Stone." These two figures refer to the same system comparison yet differ. One is likely a rounded figure for Stone's overall pipeline; the other for raw field arithmetic — but the distinction is not explained and the juxtaposition will confuse readers.
- [P2] (B) "SP1 witness generation consumes an estimated 60-70% of total proving time" — flagged as an estimate with no source. This specific proportion is a key claim about the Witness Gap and needs a citation.
- [P2] (B) "Gassmann et al. (2025)" cited without venue, journal, or DOI. This is the sole named source in the section and is referenced in multiple places; a full citation is needed.
- [P3] (C) "SP1 implements 39+ RISC-V instructions" (Layer 2) alongside "all 62 core opcodes formally verified" (same paragraph) — two different counts for different things but no explanation of the distinction, creating confusion.

## Links

- Up: [[11-zkvms-the-universal-stage]]
- Prev: [[ch11-the-landscape-table-march-2026]]
- Next: [[ch11-the-proof-core-triad]]
