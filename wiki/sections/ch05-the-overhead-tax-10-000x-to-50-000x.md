---
title: "The Overhead Tax: 10,000x to 50,000x"
slug: ch05-the-overhead-tax-10-000x-to-50-000x
chapter: 5
chapter_title: "Encoding the Performance"
heading_level: 2
source_lines: [2099, 2216]
source_commit: 53f41415d307dcd4ed73d852dfd6aa97146e882f
status: reviewed
word_count: 3325
---

## The Overhead Tax: 10,000x to 50,000x

We have spent this chapter describing how computation is encoded as mathematics. Now we must confront the cost.

A computation that runs natively in 1 millisecond -- executing instructions directly on a processor at billions of operations per second -- takes 10 to 50 seconds to prove in a zkVM. That is an overhead of 10,000x to 50,000x. Where does this multiplier come from?

The answer is not a single bottleneck but three interlocking sources of overhead that multiply together. Each source has its own physics, its own improvement trajectory, and its own fundamental limits. Understanding the decomposition matters because it determines which engineering improvements will matter most for which applications.

### Source 1: Field Arithmetic Encoding

Native computation uses 32-bit or 64-bit integers with hardware-accelerated arithmetic. A single addition or multiplication takes one CPU cycle -- roughly 0.3 nanoseconds on a modern processor.

ZK computation uses finite field arithmetic. If the proof system requires a 254-bit prime field (as BLS12-381 and BN254 do), every "addition" becomes multi-precision arithmetic over four 64-bit machine words. Each field multiplication requires a Barrett or Montgomery reduction. The per-operation cost is roughly 10 to 100 times higher than native integer arithmetic, depending on the field size.

The small-field revolution -- BabyBear (31-bit), Mersenne-31 (31-bit), Goldilocks (64-bit) -- addresses this directly. A 31-bit field element fits in a single 32-bit register; a 64-bit Goldilocks element fits in a single machine word. Arithmetic in these fields runs 10x to 100x faster than in 254-bit fields. But even in the smallest fields, the overhead of field arithmetic versus native integer operations remains significant.

The Mersenne-31 field is particularly elegant. Its modulus is $2^{31} - 1$, which is a Mersenne prime. Reduction modulo $2^{31} - 1$ is exceptionally fast: after computing the product of two 31-bit numbers (yielding a 62-bit result), you split the result into a high part and a low part at bit position 31, and add them together. If the sum exceeds $2^{31} - 1$, subtract once. Two shifts and two additions -- faster than any other prime modular reduction. This is why SP1 and Stwo chose Mersenne-31 as their base field: the per-operation cost is nearly as fast as native 32-bit integer arithmetic, closing the gap between "native" and "field" computation to a factor of roughly 3x to 5x.

### Source 2: Constraint Expansion

A single native instruction (say, a 64-bit addition) becomes multiple constraints in the arithmetized form. The addition itself is one constraint, but proving that the operands are within the correct range (range checks), that the memory was read correctly (memory consistency), and that the instruction was selected properly (opcode decoding) can require dozens to hundreds of additional constraints. This multiplicative blowup is the most counter-intuitive aspect of arithmetization: the "interesting" computation (the actual addition) accounts for a tiny fraction of the total constraint count. The vast majority of constraints are devoted to proving that the computational environment is correctly maintained -- that registers hold the right values, that memory is consistent, that the instruction pointer advanced correctly.

To make this tangible, here is a rough breakdown of the constraints required to prove a single ADD instruction in a typical zkVM (based on published analyses of RISC Zero and SP1 architectures):

- **Instruction decode**: the prover must prove that the opcode field of the instruction word equals the ADD opcode. This requires extracting bit fields and constraining them -- roughly 5 to 10 constraints.
- **Register read**: the prover must prove it correctly read the values of the source registers (rs1 and rs2) from the register file. Memory consistency for each read requires 3 to 5 constraints (depending on the memory-checking technique).
- **Arithmetic operation**: the actual addition is 1 constraint.
- **Overflow handling**: the result must be reduced modulo $2^{32}$ (for 32-bit RISC-V). This requires proving that the result fits in 32 bits -- a range check costing 32 constraints (one per bit) in naive approaches, or fewer with lookup-based range checks.
- **Register write**: the prover must prove it correctly wrote the result to the destination register (rd). Another 3 to 5 memory consistency constraints.
- **Program counter update**: the prover must prove that the PC advanced by 4 (the size of one instruction). 2 to 3 constraints.

Total: roughly 50 to 80 constraints for a single ADD instruction that, on a real CPU, takes one clock cycle. The arithmetic itself (the actual addition) accounts for exactly 1 of those constraints. The other 49 to 79 are bookkeeping: proving that the right values were read from the right places, that the result was stored correctly, and that the instruction was decoded properly. This bookkeeping overhead is the dominant cost in constraint expansion.

Memory consistency is particularly expensive. In a native processor, reading from memory is a single operation -- the cache or main memory returns the value, and the hardware guarantees it is the value that was most recently written to that address. The CPU does not need to *prove* this; the hardware enforces it physically. In a constraint system, there is no hardware. The prover claims "I read value 42 from address 0x1000," and the verifier has no way to check this claim without a mathematical argument.

Classical approaches use Merkle tree hashing -- roughly 300 multiplication constraints per Poseidon hash invocation -- to authenticate every memory access. The idea: maintain a Merkle tree over the entire memory state. Before each read, prove that the value at the target address is consistent with the Merkle root. After each write, update the Merkle tree and prove the new root is correct. Each access requires a Merkle proof (log-depth hash chain), and each hash costs hundreds of constraints. For a program with millions of memory accesses, this becomes the dominant cost.

Ozdemir and others have demonstrated algebraic approaches that reduce memory checking costs by 50x to 150x by replacing Merkle proofs with "offline memory checking" -- a technique where the prover accumulates a fingerprint of all reads and writes, and the verifier checks that the fingerprint is consistent at the end. No per-access Merkle proofs, just a global consistency check. This is the approach used by Jolt and by SP1's latest architecture. But even the improved methods add substantial overhead compared to native memory access, which costs exactly zero proof constraints.

### Source 3: Polynomial Commitment

After the constraints are constructed, the prover must commit to the polynomial representations and prove their evaluations. The commitment step is where the "zero-knowledge" part happens: the prover seals the polynomials into cryptographic commitments that reveal nothing about the underlying values, then proves properties of the committed polynomials without opening them. In absolute wall-clock time, this is the dominant step -- NTTs alone consume 40-60% of GPU proving time. Note that the roles differ by metric: constraint expansion (Source 2) causes the largest *multiplicative* blowup relative to native execution (the 50x-100x factor that turns one CPU instruction into dozens of constraints), while polynomial commitment (Source 3) causes the largest *absolute* wall-clock cost for any computation of non-trivial size.

The commitment process typically involves Number Theoretic Transforms (NTTs) -- the finite-field analog of the Fast Fourier Transform -- which can consume up to 90% of GPU proving time. Multi-scalar multiplications (MSMs) for group-based commitments add further cost. For FRI-based systems (used with STARKs), the commitment involves building Merkle trees over polynomial evaluations and performing multiple rounds of degree-halving with random challenges. For KZG-based systems (used with PLONK and Groth16), the commitment involves computing elliptic curve group operations -- MSMs of size proportional to the polynomial degree.

The three sources multiply. If field encoding costs 10x, constraint expansion costs 50x, and polynomial commitment costs 10x, the total overhead is not $70\times$ but $5{,}000\times$. This multiplicative composition is why the overhead is so large and why improvements in any single source yield modest overall gains. Reducing field encoding overhead by 10x (moving from 254-bit to 31-bit fields) and reducing constraint expansion by 2x (using lookup-based approaches) yields a combined 20x improvement -- meaningful, but still leaving a 250x overhead. All three sources must be attacked simultaneously.

### Is the Overhead Fundamental?

No. Every source of overhead is under active attack by engineering and mathematical innovation:

- **Field size**: The shift from 254-bit to 31-bit fields reduced per-operation cost by roughly 100x. A 31-bit field multiplication is a single machine word multiply followed by a modular reduction -- roughly 2 to 3 clock cycles versus the 50 to 100 cycles required for a 254-bit Montgomery multiplication.
- **Memory checking**: Algebraic memory checking (Ozdemir et al.) reduces overhead by 50-150x versus Merkle-based approaches. Instead of hashing at every memory access, algebraic techniques use offline fingerprinting -- accumulating a running product that can be checked at the end of the execution.
- **Bit-level encoding**: Binius (Irreducible, 2025) reduces embedding overhead by 100x for bit-heavy workloads by working directly over binary tower fields, where a single bit *is* a field element (no embedding required).
- **Hardware acceleration**: GPU-based provers (BatchZK, ZKProphet) achieve throughput improvements of 10x to 100x through massive parallelism in NTT and MSM computations.
- **Lookup-based architectures**: Jolt eliminates many constraint expansion costs by replacing polynomial constraints with table lookups. The 50-80 constraints per instruction in a traditional zkVM drop to roughly 18 field element commitments per 64-bit RISC-V instruction.
- **Folding schemes**: Nova, HyperNova, and Neo amortize the cost of proving many similar statements by "folding" them into a single accumulated instance. Instead of proving each step independently, the prover maintains a running accumulation that grows by a constant amount per step.

The cumulative effect is multiplicative. If small fields give 100x, algebraic memory checking gives 50x, and GPU acceleration gives 10x, the combined improvement is not 160x but potentially 50,000x -- enough to close much of the gap between native and proven computation. The catch is that these improvements compound only if they apply to the same bottleneck; in practice, eliminating one bottleneck exposes the next. But the engineering trajectory points down.

### What the Overhead Feels Like in Practice

Abstract multipliers are hard to internalize. The practical rule of thumb: if your native Rust program runs in 1 millisecond, budget 10 to 50 seconds for the proof. If it runs in 100 milliseconds, budget 1 to 5 minutes. The overhead is not linear -- it compresses at scale because fixed costs amortize -- but these ballpark numbers are what developers encounter in practice. Here are three concrete examples that reveal the texture of the overhead tax.

**The single addition.** A function that adds two 64-bit integers takes approximately 1 nanosecond on a modern CPU -- one clock cycle, one instruction, done. The same addition, proven in zero knowledge, requires: encoding the addition as a field operation (the 64-bit integer must be represented as one or more field elements, with range checks to prove it fits in 64 bits), committing to the input and output values (a polynomial commitment involving a multi-scalar multiplication or hash-based Merkle path), and generating a proof that the commitment is consistent with the constraint (running the full SNARK or STARK prover pipeline). Total time: 10 to 100 microseconds, depending on the proof system. Overhead: 10,000x to 100,000x. A single addition -- the simplest possible computation -- pays the full fixed cost of the proof machinery.

**The Ethereum block.** An Ethereum block execution takes roughly 100 milliseconds of native computation: verifying signatures, executing smart contract bytecode, updating the state trie. Proving the same block in a zkEVM takes 6 to 35 seconds on GPU clusters (SP1 v2 blog post, Succinct Labs, 2025; RISC Zero v1.0 benchmark announcement, 2025; Stwo Ethereum proving benchmark, StarkWare, 2025). Overhead: 60x to 350x. This is far less than the theoretical 10,000x to 50,000x because GPU parallelism and algorithmic optimizations have eaten most of the overhead for large computations. The NTTs and MSMs that dominate prover time are embarrassingly parallel -- they decompose into millions of independent operations that map naturally onto GPU architectures with thousands of cores.

**The Midnight transaction.** A Midnight shielded transfer involves a Compact smart contract that reads and updates token balances behind zero-knowledge proofs. The native computation -- checking a balance, subtracting from one account, adding to another -- would take a few tens of microseconds in any programming language. We take **20 microseconds** as the reference native baseline: the arithmetic of a handful of balance operations running on a modern CPU. Proving the same transaction in Midnight's ZK pipeline takes approximately 20 seconds: the Compact compiler (v0.29.0) produces ZKIR instructions, the backend lowers them to PLONKish constraints over BLS12-381 using a Halo2-based backend (as documented in the Midnight ZKIR Reference v2/v3), and the prover generates the proof. Overhead against that 20 microsecond arithmetic baseline: $20\text{ s} / 20\text{ us} = 1{,}000{,}000\times$. The comparison is deliberately stark because the proof is doing far more than the arithmetic -- it is proving that the balance update is consistent with the entire ledger state, that the sender has sufficient funds, that the nullifier has not been previously spent, and that the cryptographic commitments are correctly formed. The "computation" being proved is not the balance update itself but the entire integrity argument surrounding it. Against that broader security computation, the overhead is more like 1,000x.

**The gap between the three.** A single addition suffers 10,000x to 100,000x overhead. An Ethereum block suffers 60x to 350x. A Midnight transaction suffers a nominal 1,000,000x on the pure arithmetic but a more reasonable 1,000x when measured against the full security computation it replaces. The difference is not a measurement error. It reflects a fundamental asymmetry in the cost structure: zero-knowledge proving has large fixed costs (setting up the polynomial commitment, running the Fiat-Shamir transcript, computing the proof) and relatively small marginal costs per additional constraint. A single addition amortizes those fixed costs over one operation. An Ethereum block -- with millions of constraints -- amortizes them over millions. The per-constraint overhead might be identical, but the ratio of total proving time to native execution time drops as the computation grows.

A table makes the pattern visible. All rows compare proof time against the stated native baseline in the "Why" column:

| Computation | Native time | Proof time | Overhead | Why |
|-------------|-------------|------------|----------|-----|
| Single 64-bit addition | ~1 ns | 10-100 us | 10,000-100,000x | Fixed costs dominate |
| SHA-256 hash (one block) | ~300 ns | 1-10 ms | 3,000-30,000x | Constraint expansion for bitwise ops |
| Ethereum block execution | ~100 ms | 6-35 s | 60-350x | GPU parallelism amortizes fixed costs |
| Midnight shielded transfer | ~20 us (raw arithmetic) | ~20 s | ~1,000,000x (arithmetic baseline) | Large cryptographic circuit, BLS12-381 field |

Overhead is not uniform. Small computations suffer disproportionately. Large computations amortize the fixed costs. Computations over large fields (BLS12-381 at 255 bits) pay more per operation than those over small fields (BabyBear at 31 bits). And computations that are inherently bitwise (hashes, comparisons) pay more than those that are inherently arithmetic (field operations, polynomial evaluations).

This is why zkVMs are viable for block-level proving (where the overhead is 100x to 500x, manageable with GPU clusters) but impractical for individual function calls (where the overhead is 10,000x to 100,000x, making a 1-microsecond function take 100 milliseconds to prove). The economics of zero-knowledge computation favor batching -- proving large computations in bulk rather than small computations one at a time.

Where does the time actually go for a block-level proof? In a typical GPU-based zkEVM prover (SP1, RISC Zero, or similar systems as measured in 2025 benchmarks), the breakdown looks roughly like this:

- **NTT (Number Theoretic Transform):** 40-60% of total proving time. The finite-field analog of the FFT, used to convert polynomials between coefficient and evaluation representations. These are the workhorses of polynomial commitment. An NTT of size $2^{24}$ involves roughly $24 \cdot 2^{24} = 400$ million field multiplications -- each of which, even in a fast 31-bit field, takes a few nanoseconds.
- **Polynomial commitment (MSM or hash-based):** 15-30% of total proving time. For KZG-based systems, multi-scalar multiplications over elliptic curves. For FRI-based systems, Merkle tree construction over hash evaluations. FRI commitments require hashing the polynomial evaluations into a Merkle tree, then performing multiple rounds of folding (each requiring NTTs of decreasing size) and opening consistency proofs.
- **Witness generation and constraint evaluation:** 10-20% of total proving time. Filling in the execution trace and checking that all constraints are satisfied. This is the "spreadsheet" work: computing the values for every cell and verifying that every rule holds.
- **Memory and communication overhead:** 5-15%. Moving data between CPU and GPU, allocating buffers, serializing proof elements. For large proofs, the witness can be several gigabytes, and transferring it across the PCIe bus takes non-trivial time.

The dominance of NTT explains why GPU parallelism helps so much: NTTs decompose into independent butterfly operations that map directly onto GPU warp-level parallelism. A single NVIDIA A100 GPU can perform NTTs over $2^{24}$ field elements in under 100 milliseconds -- a task that would take several seconds on a CPU. The algorithmic improvements from 2024 to 2026 (circle STARKs, WHIR, lattice-based schemes that avoid NTTs entirely) are systematically attacking this bottleneck.

One emerging approach eliminates NTTs from the core verification step. Sumcheck-based proof systems (like Spartan, HyperNova, and Jolt) work with multilinear polynomials over the Boolean hypercube rather than univariate polynomials over multiplicative subgroups. The sumcheck reduction itself does not require NTTs: the prover performs structured summations that decompose into independent, parallel operations without the butterfly dependency pattern of NTTs. Whether NTTs are avoided altogether depends on the commitment scheme used alongside sumcheck -- some multilinear commitment schemes (such as Hyrax or Brakedown) do not require NTTs, while others may still involve NTT-like transforms internally. But the sumcheck step itself is NTT-free, which is why sumcheck-based architectures are gaining ground: they move the bottleneck from NTTs to summations that are even more GPU-friendly.

This asymmetry also explains why recursive proof composition matters so much. If you can batch thousands of small proofs into one large proof, and then prove the large proof recursively, you move the computation into the regime where amortization works in your favor. The fixed costs are paid once; the marginal costs scale linearly. Recursion is an overhead-amortization strategy, not merely a proof-size optimization.

The implications for system design are immediate. If you are building a zkVM for general-purpose computation, you should optimize for large batch sizes: prove an entire block at once, not individual transactions. If you are building a privacy-preserving application (like Midnight), where each transaction requires its own proof, you should invest in reducing the fixed costs: smaller fields, faster commitment schemes, and more efficient constraint systems. The overhead tax is not one number. It is a function of computation size, field choice, constraint system, and proof system -- and the design space offers different tradeoffs for different applications.

The 10,000-50,000x overhead of 2024 is not a permanent feature of provable computation. It is the current state of a rapidly improving engineering frontier. A reasonable projection is that overhead will decrease to 1,000-5,000x within two to three years for general-purpose zkVMs, with application-specific circuits already achieving lower ratios. Whether it can ever approach 100x or below for general computation remains an open research question.

The trajectory is visible in the benchmarks. In 2022, proving a single Ethereum block took minutes on specialized hardware. By 2024, it took 30 to 60 seconds on GPU clusters. By early 2026, the fastest systems (SP1 Hypercube, RISC Zero 1.0) demonstrate 6 to 15 seconds for the same workload, with further improvements expected as circle STARKs, WHIR, and lattice-based commitments reach production maturity. Each generation of improvements comes from a different source: the move from 254-bit to 31-bit fields (2022-2023), the adoption of LogUp-GKR for lookups (2023-2024), the shift to sumcheck-based architectures (2024-2025), and GPU kernel optimization for NTTs and MSMs (ongoing). The overhead is falling not because of one breakthrough but because of compounding engineering progress across every layer of the stack.

For architects comparing systems, the following table normalizes the overhead by system and field, using Ethereum block proving as the benchmark workload. The "overhead" column measures proof time against an Ethereum block native execution time of ~100 ms. The Airbender figure, drawn from ZKsync's June 2025 announcement of a single-H100 prover, is shown on the same Ethereum block baseline as the other rows; earlier reports that quoted an "~8,000x" multiplier used a different, smaller native baseline (roughly single-transaction arithmetic in the low-millisecond range) and are not comparable to the block-level numbers in this table.

| System | Base Field | Eth Block Time | Approx. Overhead (vs ~100 ms block) | Year | Key Innovation |
|--------|-----------|----------------|-------------------------------------|------|----------------|
| RISC Zero (v0.x) | BN254 (254-bit) | ~60 s (GPU) | ~600x | 2023 | First general-purpose zkVM |
| SP1 (v1) | BabyBear (31-bit) | ~15 s (16 GPU) | ~150x | 2024 | Small-field + multilinear STARK |
| SP1 Hypercube | BabyBear (31-bit) | 6.9 s (16 GPU) | ~70x | 2025 | Sumcheck + precompiles |
| Stwo | Mersenne-31 (31-bit) | ~10 s (cluster) | ~100x | 2025 | Circle STARK + 940x vs. Stone |
| Airbender | BabyBear (31-bit) | ~35 s (1 H100) | ~350x | 2025 | Single-GPU design |

(The earlier draft of this chapter gave Airbender as "~8,000x" overhead; that number was measured against a single-transaction baseline, not the 100 ms block baseline used here. Both interpretations are defensible; we use the block baseline throughout this table so the rows are comparable.)

---


## Summary

The 10,000x–50,000x proving overhead over native execution comes from three multiplicative sources: field arithmetic encoding (10–100x), constraint expansion per instruction (50–100x), and polynomial commitment (10–50x). None of the sources is fundamental: small fields, algebraic memory checking, lookup architectures, and GPU parallelism are each attacking one component, with the combined trajectory pointing toward 1,000–5,000x by 2027–2028.

## Key claims

- Ethereum block proving: native ~100 ms; best 2025/2026 zkVMs (SP1 Hypercube, Stwo) achieve 6–15 s on 16-GPU clusters, ~60–350x overhead.
- Midnight shielded transfer: ~20 s proof time over BLS12-381; nominal ~4,000,000x vs. raw arithmetic, ~1,000x vs. full security computation it replaces.
- Single 64-bit ADD: 10,000–100,000x overhead (fixed costs dominate small computations).
- Field arithmetic: 254-bit primes require multi-precision arithmetic (~50–100 cycles/op); Mersenne-31 requires ~2–3 cycles/op — roughly 100x faster.
- NTT dominates proving time at 40–60%; polynomial commitment (MSM/FRI) 15–30%; witness generation 10–20%.
- Algebraic memory checking (Ozdemir et al.) reduces per-access cost by 50–150x vs. Merkle proofs.
- Binius (Irreducible, 2025): 100x reduction in bit-level embedding overhead using binary tower fields.
- Benchmark table: RISC Zero v0.x ~60 s (BN254); SP1 v1 ~15 s (BabyBear); SP1 Hypercube 6.9 s; Stwo ~10 s (Mersenne-31); Airbender ~35 s (single H100).

## Entities

- [[airbender]]
- [[babybear]]
- [[bn254]]
- [[bls12-381]]
- [[circle stark]]
- [[fiat-shamir]]
- [[folding]]
- [[goldilocks]]
- [[groth16]]
- [[h100]]
- [[halo2]]
- [[hypernova]]
- [[jolt]]
- [[logup]]
- [[mersenne]]
- [[midnight]]
- [[nova]]
- [[ntt]]
- [[ntts]]
- [[nvidia]]
- [[plonk]]
- [[poseidon]]
- [[small-field]]
- [[spartan]]
- [[starks]]

## Dependencies

- [[ch05-lookup-arguments]] — Jolt's lookup-based architecture is one overhead reduction strategy
- [[ch05-the-sumcheck-protocol-the-hidden-foundation]] — sumcheck-based systems avoid NTTs
- [[ch05-midnight-s-zkir-a-concrete-layer-4]] — Midnight transaction example grounds the abstract numbers
- [[ch05-where-the-layers-collapse]] — field/commitment/constraint co-design is the overhead context

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [P3] (E) The section does not discuss proving hardware costs (dollar cost per proof), which is directly relevant to the economic viability argument. A one-paragraph note on approximate USD cost per Ethereum block proof on GPU clusters would ground the overhead discussion in practical deployment terms.

## Links

- Up: [[05-encoding-the-performance]]
- Prev: [[ch05-lookup-arguments]]
- Next: [[ch05-midnight-s-zkir-a-concrete-layer-4]]
