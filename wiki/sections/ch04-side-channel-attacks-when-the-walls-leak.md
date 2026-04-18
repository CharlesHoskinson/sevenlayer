---
title: "Side-Channel Attacks: When the Walls Leak"
slug: ch04-side-channel-attacks-when-the-walls-leak
chapter: 4
chapter_title: "The Secret Performance"
heading_level: 2
source_lines: [1393, 1474]
source_commit: 8b894477fca68f8420de3f8ba0e5301ba00fbb0a
status: reviewed
word_count: 2220
---

## Side-Channel Attacks: When the Walls Leak

The mathematical definition of zero-knowledge is precise: the proof reveals nothing about the witness beyond the truth of the statement being proved. But the mathematical definition describes the *proof*. It does not describe the *process of generating the proof*.

The process can leak.

The most vivid demonstration came in Tramer, Boneh, and Paterson's "Remote Side-Channel Attacks on Anonymous Transactions" (USENIX Security 2020). They showed that Zcash's Groth16 prover leaked information about transaction amounts through proof generation time. The attack was simple in concept: the prover's multi-scalar exponentiation (MSM) implementation optimized away terms where the witness coefficient was zero. More zeros in the binary representation of the transaction amount meant fewer curve multiplications, which meant faster proof generation. By measuring how long proof generation took -- remotely, across the network -- an attacker could estimate the Hamming weight of the transaction amount.

The correlation coefficient was R = 0.57. Not perfect, but far from zero. A timing measurement that should have been meaningless -- how long did the proof take? -- revealed information about the secret that the proof was supposed to protect.

Monero's Bulletproofs implementation was safe. The correlation was R = 0.04 -- essentially noise. The difference was architectural: Bulletproofs operates on both the binary decomposition of the amount *and its complement*, making the number of curve operations constant regardless of the value. The proof generation time was the same whether the amount was 1 or 1,000,000. Constant-time implementation is not an optimization. It is a security requirement.

### The Zcash Timing Attack: A Detective Story

The Zcash attack deserves to be told as the detective story it was, because the investigative method reveals how side-channel analysis works in practice -- and why it is so difficult to defend against.

The researchers began with a hypothesis: if the Groth16 prover's multi-scalar exponentiation skips zero-valued scalar multiplications, then the proof generation time should correlate with the number of nonzero bits in the witness. They did not need to break any cryptography. They did not need to find a flaw in the mathematics. They needed a stopwatch.

They set up a Zcash node and generated shielded transactions with known amounts. For each transaction, they measured the wall-clock time of the `r1cs_gg_ppzksnark_prover` function -- the core Groth16 proving routine in libsnark. They varied the transaction amount systematically, from round numbers like 1.000 ZEC (which has a simple binary representation with many trailing zeros) to numbers with many nonzero digits like 1.337 ZEC (which has a denser binary representation).

The pattern emerged immediately. Round numbers produced faster proofs. Dense numbers produced slower proofs. The relationship was not subtle. A transaction of exactly 1.000 ZEC generated a proof measurably faster than a transaction of 1.337 ZEC, because the scalar representation of 1.000 ZEC in the finite field contained more zero coefficients, and each zero coefficient allowed the MSM algorithm to skip a point addition.

The correlation coefficient was R = 0.57 -- not strong enough to determine the exact amount, but strong enough to distinguish broad categories. An attacker could not tell whether you sent 1.337 ZEC or 1.338 ZEC. But the attacker could distinguish "approximately 1 ZEC" from "approximately 100 ZEC" with meaningful confidence. The "zero-knowledge" proof leaked the order of magnitude of the transaction amount through the duration of its generation.

What makes this attack memorable is not its severity -- R = 0.57 is a partial leak, not a catastrophic one -- but what it reveals about the gap between mathematical proof and physical implementation. The Groth16 proof system is provably zero-knowledge. The mathematical proof of this property is correct. The implementation of the prover was not constant-time, and so the *process* of generating the proof leaked information that the *proof itself* was mathematically guaranteed to conceal. The proof was zero-knowledge. The prover was not.

The fix was straightforward: replace the variable-time MSM with a constant-time implementation that processes all scalar coefficients identically, whether they are zero or nonzero. The constant-time version is slower -- it performs multiplications that the variable-time version skips -- but it eliminates the timing channel. Zcash implemented this fix. The performance cost was real. The privacy gain was essential.

### The Poseidon Cache-Timing Attack

The second attack class is subtler, and in some ways more disturbing, because it targets a component that was specifically designed for zero-knowledge systems.

Poseidon is an "algebraic" hash function. Unlike SHA-256, which was designed for general-purpose hashing and happens to be usable (expensively) inside ZK circuits, Poseidon was built from the ground up to minimize the number of constraints required to express its computation as a polynomial relation. Where SHA-256 requires approximately 25,000 constraints per hash in a Groth16 circuit, Poseidon requires approximately 300. This 80x reduction in constraint count translates directly into faster proving and smaller proofs. Poseidon is, by design, the ideal hash function for zero-knowledge systems. Every major ZK project uses it or a close variant.

Poseidon's S-box -- the nonlinear component that provides cryptographic security -- is a power map: $x \mapsto x^5$ or $x \mapsto x^7$ over a large prime field, depending on the parameter choice. In software, this is computed as a sequence of field multiplications: one squaring, one more squaring, and a multiply gives $x^5$ in three multiplications; one further multiplication gives $x^7$. There are no lookup tables involved in Poseidon's S-box. That matters, because lookup tables are the structural ingredient that makes a primitive vulnerable to cache-timing attacks.

Mukherjee, Rechberger, and Schofnegger (2024) published the first systematic study of cache-timing leakages in zero-knowledge protocols. They examined ZK-friendly hash functions (Poseidon, Reinforced Concrete, Tip5, Monolith) and popular proof systems (Groth16, Plonky2, Plonky3, halo2, Circle STARKs). The hash function whose design exposes the cache-timing channel is *Reinforced Concrete*, not Poseidon. Reinforced Concrete's "Bars" function uses a 256 KB lookup table indexed by secret-dependent data. Those table lookups create cache access patterns that vary with the secret. In a shared cloud environment, where the attacker runs on the same physical machine as the prover, those patterns are observable.

The mechanics are familiar from decades of work against AES. Modern CPUs use a hierarchy of caches (L1, L2, L3) to speed up memory access. When a program accesses a memory location, the CPU loads the surrounding cache line (typically 64 bytes) into the L1 cache. Subsequent accesses to the same cache line are fast (a few cycles). Accesses that evict a different cache line become slow again (hundreds of cycles). An attacker sharing the same physical CPU -- a realistic scenario in cloud computing -- primes the cache with known data, waits for the victim's hash computation to execute, then probes to see which of the attacker's entries were evicted. The eviction pattern reveals which table entries the victim accessed, which reveals information about the internal state of the hash, which reveals information about the secret input.

Poseidon's power-map S-box has no such table. It leaks through different channels -- the Goldilocks field's conditional reduction after multiplication produces a timing signal on branch-dependent implementations -- but not through cache patterns on the S-box itself. The attack that broke Reinforced Concrete does not mechanically break Poseidon. The broader point survives: ZK-friendly hash functions were designed for *algebraic* efficiency -- minimizing constraints inside a circuit. Nobody designed them for *implementation* security outside the circuit. Each primitive has to be audited for its own side-channel surface, and the move toward lookup-based designs in some ZK-friendly constructions -- motivated by the algebraic efficiency gains that Lasso and Jolt demonstrated -- actively increases that surface.

The irony cuts deep: the very optimization that makes proving faster makes the proving process less private, for the subset of constructions that rely on tables.

### The Electromagnetic Channel

The third attack class operates at a physical level that most software engineers never consider.

Every electronic circuit, when it operates, produces electromagnetic emanations. A transistor switching from 0 to 1 consumes a different amount of current than a transistor remaining at 0. This current difference creates a magnetic field that propagates outward from the chip. The field is weak -- microwatts -- but it is measurable with equipment that costs a few hundred dollars: a near-field electromagnetic probe, a low-noise amplifier, and a digital oscilloscope.

Field operations in elliptic curve arithmetic are particularly vulnerable. When a prover computes a point addition on an elliptic curve, the specific operations performed (and their power consumption) depend on the coordinates of the points being added, which depend on the witness values. A modular multiplication where both operands are large consumes more power than one where an operand is small. A conditional branch (reduce or do not reduce after multiplication) produces a different electromagnetic signature depending on which path is taken.

Measuring these emanations from a few centimeters away -- close enough to touch the device but not close enough to require physical modification -- can reconstruct the scalar values used in multi-scalar exponentiation. This means reconstructing the witness coefficients. This means reconstructing the private inputs to the proof.

Electromagnetic side-channel attacks are a published, demonstrated attack class. They have been used to extract AES keys from smartcards, RSA private keys from laptops, and ECDSA signing keys from hardware security modules. The equipment required is modest: a near-field probe ($50-200), an amplifier ($100-500), and an oscilloscope ($500-5,000). A university research lab can mount this attack. A well-funded adversary can mount it from across a room using more sensitive antennas.

For zero-knowledge provers running on commodity hardware -- laptops, desktops, even data center servers without electromagnetic shielding -- the EM channel is an open question. No major ZK implementation has published an electromagnetic side-channel analysis. The attack surface is real, the equipment is cheap, and the countermeasures (electromagnetic shielding, randomized execution ordering, amplitude-flattening power regulation) are not part of any ZK prover's design requirements.

The three attack channels -- timing, cache, electromagnetic -- form a hierarchy of increasing physical intimacy. Timing attacks can be mounted remotely, across a network. Cache attacks require co-location on the same physical machine. Electromagnetic attacks require physical proximity to the hardware. But all three extract information from the same fundamental source: the fact that computation is a physical process, and physical processes leave physical traces. The mathematical abstraction of a zero-knowledge proof exists in a world of pure information. The implementation exists in a world of transistors, cache lines, and electromagnetic fields. The gap between those worlds is where privacy leaks.

Field arithmetic itself leaks. The Goldilocks field ($2^{64} - 2^{32} + 1$, a prime chosen for fast 64-bit arithmetic) uses conditional reductions after arithmetic operations. If the result exceeds the modulus, a reduction step is needed; if not, it is skipped. This conditional branch creates a timing signal. Assembly implementations with branch-free code mitigate this, but many deployed field arithmetic libraries use branch-dependent paths for performance.

The accurate assessment: "zero-knowledge" is a mathematical property of the *proof*. Implementation zero-knowledge depends on the hardware, the operating system, the runtime, and the network. The gap between "the proof reveals nothing" and "the timing reveals everything" is the gap between theory and practice. The backstage walls are thinner than the magician thinks.

For defensive implementation, the standard is clear:

- No zero-skipping optimizations in multi-scalar exponentiation.
- No secret-dependent table lookups in hash functions.
- Branch-free field arithmetic, especially for conditional reduction steps.
- Cache-aligned memory access patterns.
- Constant-time prover implementations throughout the pipeline.

These requirements conflict with performance optimization at almost every turn. Making a prover constant-time means foregoing shortcuts that can halve computation time. The tension between proving speed and implementation privacy is real and ongoing.

The interaction between side channels and GPU proving adds another dimension. GPU architectures use SIMT (Single Instruction, Multiple Threads) execution, where groups of 32 threads (warps on NVIDIA hardware) execute the same instruction simultaneously. Constant-time code requires all threads in a warp to follow the same execution path. When some threads need a conditional reduction and others do not, the warp must execute both paths, with inactive threads masking their results. This "thread divergence" reduces GPU utilization -- the very parallelism that makes GPUs fast for proving works against the constant-time requirement.

The open question is whether witness generation can be made fully constant-time on GPUs without unacceptable performance loss. The answer is not yet clear. What is clear is that any system claiming both GPU-accelerated proving and zero-knowledge must address this tension explicitly. Most do not.

For the reader who wants a single mental model: the backstage walls are made of different materials at different heights. The cryptographic walls (the proof itself) are mathematically perfect -- no information passes through. The implementation walls (the proving process) are made of timing signals, cache patterns, and memory access traces. They leak. Not catastrophically, not in every deployment, but measurably and exploitably in the wrong environment. The system architect's job is not to eliminate all leakage -- that may be impossible -- but to understand where the walls are thin and what information an attacker on the other side could extract.

---


## Summary

Zero-knowledge is a property of the proof, not the prover: the process of generating a proof can leak private information through timing, cache access patterns, and electromagnetic emanations. Tramer, Boneh, and Paterson showed Zcash's Groth16 prover leaked transaction amount magnitude via MSM timing (R=0.57); Mukherjee et al. (2024) showed ZK-friendly hash functions including Poseidon introduce cache-timing leakage through their lookup-table S-boxes; constant-time implementation is a security requirement that conflicts with performance optimization at nearly every turn.

## Key claims

- Zcash's Groth16 prover leaked transaction amount through MSM timing: R=0.57 correlation (Tramer, Boneh, Paterson 2020).
- Monero's Bulletproofs was safe: R=0.04, due to constant-time binary decomposition that includes both the value and its complement.
- Poseidon's S-box uses lookup tables indexed by secret-dependent state, creating observable cache access patterns in shared cloud environments.
- Mukherjee et al. (2024) examined Groth16, Plonky2, Plonky3, halo2, Circle STARKs — all have implementation-level privacy risks.
- The Goldilocks field's conditional reduction after arithmetic creates a timing signal; branch-free assembly is required.
- Electromagnetic side-channel attacks can reconstruct MSM scalar values (witness coefficients) from a few centimeters away with <$5,000 equipment.
- GPU SIMT execution conflicts with constant-time requirements: warp divergence reduces GPU utilization when threads take different branches.
- The move toward lookup-based ZK hash designs (motivated by Lasso/Jolt efficiency) actively increases the side-channel attack surface.

## Entities

- [[bulletproofs]]
- [[circle stark]]
- [[fri]]
- [[goldilocks]]
- [[groth16]]
- [[halo2]]
- [[jolt]]
- [[lasso]]
- [[nvidia]]
- [[plonk]]
- [[plonky3]]
- [[poseidon]]
- [[starks]]
- [[zcash]]

## Dependencies

- [[ch04-the-hidden-bottleneck]] — introduces the "thin walls" problem
- [[ch04-the-witness-as-a-multi-dimensional-problem]] — synthesizes side-channel as the Security Gap
- [[ch07-algebraic-vs-traditional-hash-functions]] — the algebraic vs. constant-time tension explored at Layer 6

## Sources cited

- Tramer, Boneh, Paterson — "Remote Side-Channel Attacks on Anonymous Transactions," USENIX Security 2020; Zcash timing attack, R=0.57
- Mukherjee, Rechberger, Schofnegger — cache-timing leakages in ZK protocols, 2024

## Open questions

- Whether witness generation can be made fully constant-time on GPUs without unacceptable performance loss is an open question (flagged explicitly in the section).

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [P2] (A) "EM attacks can reconstruct the scalar values used in multi-scalar exponentiation" is stated as "published, demonstrated" but no specific ZK-system EM attack paper is cited — only the general prior work on AES smartcards and ECDSA HSMs. The claim that ZK MSM is vulnerable to EM is extrapolated, not directly demonstrated in the literature cited.
- [P2] (C) The "detective story" sub-framing ("told as the detective story it was") is an AI-smell: framing a sub-section as a narrative genre. Retitle or remove the genre label.
- [P3] (E) The GPU SIMT thread-divergence paragraph is the only place in ch04 that connects side-channel defenses to GPU architecture. It raises an important open problem but does not cite any work that has measured the performance cost of constant-time GPU proving. Noting this gap explicitly would strengthen the open-questions section.

## Links

- Up: [[04-the-secret-performance]]
- Prev: [[ch04-memory-the-binding-constraint]]
- Next: [[ch04-witness-constraint-divergence]]
