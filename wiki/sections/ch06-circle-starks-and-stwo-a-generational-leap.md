---
title: "Circle STARKs and Stwo: A Generational Leap"
slug: ch06-circle-starks-and-stwo-a-generational-leap
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2734, 2794]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 1611
---

## Circle STARKs and Stwo: A Generational Leap

While the folding lineage was evolving, a parallel revolution was happening in the STARK world. In 2024, Haboeck (Polygon Labs), Levit, and Papini (StarkWare) published Circle STARKs, and their production implementation -- Stwo -- became the fastest proof system ever deployed.

The key insight is a change in the algebraic structure underlying the FFT, which is the computational backbone of every STARK prover. Traditional STARKs use multiplicative subgroups of finite fields for their FFT domains. These subgroups exist in large fields (like BN254's 254-bit field), but finding smooth-order subgroups in small fields is difficult. Circle STARKs replace the multiplicative subgroup with the *circle group* of a Mersenne prime field.

Why the circle group? The Mersenne-31 field ($M31 = 2^{31} - 1$) is a prime with a special property: the circle group $C(\mathbb{F}_p) = \{(x, y) : x^2 + y^2 = 1 \text{ over } \mathbb{F}_p\}$ has order $p + 1 = 2^{31}$, which is a perfect power of 2. This enables a radix-2 FFT (the Circle FFT, or CFFT) analogous to the standard Cooley-Tukey FFT but operating over circle points. Each FRI step halves the domain using the circle group's "squaring" map, and the entire protocol adapts naturally to the circle geometry.

Why does the field size matter so much? Because 31-bit numbers fit in a single 32-bit machine word. On modern CPUs with SIMD instructions, you can process 8 or 16 M31 elements in parallel per instruction. On GPUs, the advantage is even more dramatic. Arithmetic over M31 is roughly 100 times faster than arithmetic over BN254's 254-bit field. When your proof system spends most of its time doing field arithmetic, a 100x speedup in the field operations translates almost directly into a 100x speedup in proving.

The numbers confirm this. Stwo, StarkWare's production implementation of Circle STARKs, went live on Starknet mainnet in 2025. Every Starknet block is now proven by Stwo. The benchmarks:

- **940x throughput improvement** over Stone (StarkWare's previous prover)
- **50x improvement** over ethSTARK (the academic reference implementation)
- GPU acceleration via ICICLE-Stwo adds another 3.25x to 7x on top of the CPU SIMD backend
- Sub-second recursive proving is within reach: roughly 20 milliseconds for 10,000 Poseidon hash evaluations

These are not projections. This is production performance, running on mainnet, proving real blocks with real transactions. The gap between "academic proof system" and "deployed infrastructure" has closed.

### Why the Circle Group Matters

The phrase "circle group" sounds like an abstraction. It is not. It is a geometric fact about numbers that makes everything else possible, and it deserves a careful explanation.

Start with what came before. Traditional STARKs need a domain of points where they can evaluate polynomials -- a set of evenly-spaced "sampling points" that enable the FFT. In large fields like BN254, you find these points in the multiplicative group: pick a generator $g$, and the powers $g, g^2, g^3, \ldots, g^{2^k}$ form a subgroup of order $2^k$. These powers wrap around like hours on a clock face. The FFT works because the subgroup has smooth order (a power of 2), so the Cooley-Tukey butterfly decomposition applies perfectly.

But in small fields, this strategy collapses. The Mersenne-31 field has only $2^{31} - 2$ nonzero elements. Its multiplicative group has order $2^{31} - 2 = 2 \times 3 \times 357{,}913{,}941$. The largest power-of-2 subgroup has order just 2 -- it contains only {1, -1}. You cannot run an FFT of size $2^{24}$ over a group of size 2. The multiplicative group of M31 is, for FFT purposes, useless.

This is where the circle enters. Consider the set of all pairs $(x, y)$ in M31 that satisfy $x^2 + y^2 = 1$. This is the unit circle over the finite field -- not a continuous curve but a discrete set of points. The key fact: this set has exactly $p + 1 = 2^{31}$ points. Not $2^{31} - 2$. Not some awkward composite. Exactly $2^{31}$. A perfect power of 2.

The coincidence is not a coincidence. It is a theorem. For any Mersenne prime $p = 2^n - 1$, the circle group $C(\mathbb{F}_p)$ has order $p + 1 = 2^n$. This is because the circle group over $\mathbb{F}_p$ is isomorphic to the multiplicative group of $\mathbb{F}_{p^2}$ modulo $\mathbb{F}_p^*$ -- a quotient that inherits the 2-adic structure of $p + 1$. When $p$ is a Mersenne prime, that structure is maximally smooth: a pure power of 2.

This perfect power-of-2 structure gives you the cleanest possible FFT. The Circle FFT (CFFT) decomposes a polynomial evaluation over $2^{31}$ points into layers of half-size evaluations, just as the standard Cooley-Tukey FFT does over multiplicative subgroups. Each layer halves the domain. After 31 layers, you are done. No padding, no awkward leftovers, no compromises.

### The Squaring Map: Folding a Circle in Half

The FRI protocol -- the heart of every STARK's proof of low degree -- works by repeatedly halving the evaluation domain. At each step, the prover combines pairs of evaluations into single values, reducing the domain by a factor of 2. After enough steps, the polynomial is so small that the verifier can check it directly.

In a traditional STARK over a multiplicative group, the halving map is squaring: the map $x \mapsto x^2$ sends a subgroup of order $2^k$ to a subgroup of order $2^{k-1}$. Each element and its "twin" (its negation in the group) map to the same value, so the domain folds in half.

On the circle, the halving map is also a squaring -- but a *geometric* squaring. The circle has a group law: you can "add" two points by a formula analogous to angle addition. The squaring map sends a point to its double under this group law. Concretely, for a point $(x, y)$ on the circle $x^2 + y^2 = 1$, the doubling map sends $(x, y)$ to $(2x^2 - 1, 2xy)$. This map is 2-to-1: each image point has exactly two preimages. So the circle of $2^k$ points folds onto a circle of $2^{k-1}$ points.

The visual intuition is literal. Imagine folding a circle in half. The top half maps onto the bottom half. Each point on the bottom half corresponds to two points on the original circle -- one on top, one on bottom. The FRI protocol does exactly this, algebraically. At each step, the prover commits to evaluations on a circle, the verifier sends a random challenge, and the prover uses the challenge to combine each pair of evaluations (the point and its "fold partner") into a single value on the half-size circle. After $\log(n)$ steps, only a constant-size polynomial remains.

This geometric folding is why Circle STARKs achieve the same asymptotic efficiency as traditional STARKs -- $O(n \log n)$ prover time, $O(\log^2 n)$ verifier time, $O(\log^2 n)$ proof size -- while operating over a field where the elements are only 31 bits wide.

### Why 31-Bit Arithmetic Is So Fast

The final piece of the Circle STARK advantage is not algebraic but architectural. It concerns the physical reality of how modern processors handle numbers.

A 64-bit CPU register holds 64 bits. A 254-bit BN254 field element requires four 64-bit "limbs" and careful carry propagation between them. A single field multiplication over BN254 involves roughly 16 limb multiplications and a cascade of additions and carries -- effectively 20 to 30 machine instructions per field multiplication. This is multi-precision arithmetic, and it is inherently serial: each carry depends on the result of the previous limb multiplication.

A 31-bit M31 field element fits in a single 32-bit word. A single field multiplication is one 32-bit multiply followed by one modular reduction -- and because $M31 = 2^{31} - 1$ is a Mersenne prime, the reduction is a single addition and a conditional subtraction. Two machine instructions. The ratio is severe: 2 instructions for M31 versus 20-30 for BN254. A factor of 10 to 15, per operation.

But the advantage compounds under parallelism. A 64-bit register can hold two M31 elements side by side. An AVX-256 SIMD register holds eight. An AVX-512 register holds sixteen. A single SIMD instruction can multiply sixteen M31 elements simultaneously, producing sixteen field products in the time it takes to perform one BN254 multiplication. The theoretical throughput ratio is not 10x. It is 100x or more.

On a GPU, the effect is even more dramatic. A GPU's streaming multiprocessors are optimized for 32-bit integer and floating-point operations -- the native word size of graphics workloads. M31 arithmetic maps directly onto the hardware's sweet spot. BN254 arithmetic requires emulation using multiple 32-bit operations per limb, with register pressure and carry chains that reduce occupancy (the fraction of the GPU's compute units that are actively working). In practice, Stwo's GPU backend -- implemented via ICICLE -- achieves 3.25x to 7x additional speedup on top of the already-fast CPU SIMD implementation. The cumulative advantage of small-field arithmetic, from instruction-level to chip-level, is why Circle STARKs proved to be not a modest improvement over traditional STARKs but a qualitative jump.

The Mersenne prime M31 is not the only small field in production. BabyBear ($p = 2^{31} - 2^{27} + 1 = 15 \times 2^{27} + 1$) offers similar 31-bit arithmetic with a multiplicative group of smooth order ($2^{27}$ divides $p - 1$), enabling traditional multiplicative-subgroup FFTs rather than circle FFTs. SP1 uses BabyBear for its inner proof system. The choice between M31 and BabyBear is a choice between circle-group FFTs and multiplicative-group FFTs -- two paths to the same destination of fast, small-field proving. Both paths converge on the same insight: the biggest optimization in proof system engineering is not a cleverer algorithm. It is a smaller number.

---


## Summary

Circle STARKs (Haboeck, Levit, Papini, 2024) replace the multiplicative subgroup FFT with the circle group of the Mersenne-31 field, whose order is exactly $2^{31}$ -- a perfect power of 2 enabling a clean radix-2 FFT. Stwo, the production implementation deployed on Starknet mainnet in 2025, achieved a 940x throughput improvement over Stone because 31-bit arithmetic is ~100x faster than 254-bit arithmetic and maps directly onto CPU SIMD and GPU hardware.

## Key claims

- Mersenne-31 circle group has order $p+1 = 2^{31}$, enabling a clean radix-2 Circle FFT (CFFT).
- M31 multiplicative group order is $2^{31}-2 = 2 \times 3 \times 357{,}913{,}941$ -- useless for FFTs; the circle group fixes this.
- Stwo: 940x improvement over Stone, 50x over ethSTARK, live on Starknet mainnet 2025.
- ICICLE GPU backend adds 3.25x--7x on top of CPU SIMD.
- M31 field multiplication: 2 machine instructions vs. 20--30 for BN254; AVX-512 processes 16 M31 elements per instruction.
- BabyBear ($2^{31} - 2^{27} + 1$) is the alternative small field (used by SP1) with multiplicative-subgroup FFTs instead of circle FFTs.
- The biggest optimization is using a smaller number, not a cleverer algorithm.

## Entities

- [[circle stark]]
- [[starks]]
- [[fri]]
- [[mersenne]]
- [[babybear]]
- [[small-field]]
- [[poseidon]]
- [[starknet]]
- [[polygon]]
- [[folding]]
- [[bn254]]

## Dependencies

- [[ch06-the-three-families]] — STARKs family context for where Circle STARKs fit
- [[ch07-small-fields]] — detailed treatment of small-field arithmetic advantages
- [[ch06-the-hybrid-pipeline]] — Stwo is the inner prover in the hybrid pipeline
- [[ch06-real-time-ethereum-proving]] — Circle STARKs enabling real-time proving benchmarks follow

## Sources cited

- Haboeck, Levit, Papini, "Circle STARKs," ePrint 2024/278.

## Open questions

None flagged by this section.

## Improvement notes

- [P2] (C) "The key insight is a change in the algebraic structure" — "key insight" is an AI smell
- [P2] (B) ICICLE speedup range "3.25x to 7x" has no source; the Stwo/ICICLE benchmarks should be cited (StarkWare blog or the Circle STARKs paper)
- [P2] (B) "940x throughput improvement over Stone" is a very strong claim with a single source (the Circle STARKs ePrint); a secondary benchmark citation would strengthen it
- [P3] (A) The circle group isomorphism stated as "$C(\mathbb{F}_p)$ is isomorphic to the multiplicative group of $\mathbb{F}_{p^2}$ modulo $\mathbb{F}_p^*$" — technically the isomorphism is to the subgroup of norm-1 elements of $\mathbb{F}_{p^2}^*$; the stated quotient framing is informal and could mislead readers with algebraic background
- [P3] (E) The BabyBear comparison at the end is useful but brief; a sentence noting that BabyBear's multiplicative group of smooth order $2^{27}$ (not $2^{31}$) means its FFT domain is smaller than M31's circle group would sharpen the comparison

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-nightstream-what-a-folding-engine-looks-like-from-the-inside]]
- Next: [[ch06-real-time-ethereum-proving]]
