---
title: "Small Fields"
slug: ch07-small-fields
chapter: 7
chapter_title: "Layer 6 -- The Deep Craft"
heading_level: 2
source_lines: [3176, 3228]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 961
---

## Small Fields

If the commitment scheme is the "which family" decision, the finite field is the "which numbers" decision. And this choice -- seemingly a detail buried deep in the mathematics -- turns out to determine nearly everything about performance.

A finite field is a set of numbers equipped with addition and multiplication that "wrap around" at a fixed boundary, called the *modulus* or *prime*. Every value in a zero-knowledge circuit is an element of some finite field. Every arithmetic operation is performed modulo the field's prime. The choice of prime cascades upward through every layer of the system. It is one of those decisions that seems technical and narrow when you make it, and then turns out to have been the most important decision you made.

### The Old World: BN254 and BLS12-381

For most of the 2010s, the ZK world standardized on two large primes:

**BN254** (Barreto-Naehrig curve, 254-bit prime). This was the first widely deployed pairing-friendly curve. Ethereum embedded BN254 pairing operations as EVM precompiles in 2017, making it the de facto standard for on-chain Groth16 verification. Every deployed Groth16 verifier on Ethereum -- including those used by the major rollups -- runs over BN254.

**BLS12-381** (Barreto-Lynn-Scott curve, ~253-bit prime). Introduced later with a higher security margin and better pairing efficiency. Used by Zcash, Filecoin, Midnight, and the Ethereum KZG ceremony (EIP-4844).

Both are enormous primes -- 254 and 253 bits respectively. Arithmetic on 254-bit numbers requires multiple machine words on any existing processor. A single multiplication takes several CPU instructions and cannot exploit the native 32-bit or 64-bit arithmetic units that modern hardware is optimized for.

### The Security Erosion Problem

BN254 was originally believed to provide 128-bit security -- meaning an attacker would need roughly $2^{128}$ operations to break the discrete logarithm. But advances in the Tower Number Field Sieve (Tower NFS) [Kim and Barbulescu, "Extended Tower Number Field Sieve," Mathematics of Computation, 2016; Guillevic, "Comparing the pairing efficiency over composite-order and prime-order elliptic curves," ACNS 2013] have revised this estimate downward to approximately 100 bits. This does not mean BN254 is broken -- $2^{100}$ operations is still astronomically expensive -- but it means the security margin is significantly thinner than designed.

This matters because BN254 is embedded in Ethereum's EVM precompiles. Changing the precompiled curves requires a hard fork. Every Groth16 verifier on Ethereum depends on BN254. The security erosion is not academic -- it affects the most widely deployed zero-knowledge infrastructure in the world.

BLS12-381 is not affected by Tower NFS and retains its 128-bit security estimate. But it is also not immune to future cryptanalytic advances. And neither curve survives a quantum computer.

### The New World: BabyBear, M31, Goldilocks

Starting around 2022, a radical idea took hold: *use much smaller primes*.

**BabyBear** ($p = 2^{31} - 2^{27} + 1$, a 31-bit prime). Fits in a single 32-bit machine word. Arithmetic is native on every modern CPU and GPU. Used by RISC Zero and Plonky3.

**Mersenne-31 / M31** ($p = 2^{31} - 1$, a 31-bit Mersenne prime). The simplest possible arithmetic -- reduction modulo a Mersenne prime is a single addition. Used by StarkWare's Stwo and Circle STARKs.

**Goldilocks** ($p = 2^{64} - 2^{32} + 1$, a 64-bit prime). Fits in a single 64-bit machine word. Has high 2-adicity -- meaning $2^{32}$ divides $p - 1$, which tells you the field supports efficient radix-2 NTTs (the finite-field Fast Fourier Transform that dominates prover computation) with domain sizes up to $2^{32}$. Used by Polygon's Plonky2 and by Neo/Nightstream.

The performance impact is not incremental. It is a factor of 100. Arithmetic on 31-bit numbers is roughly 100 times faster than arithmetic on 254-bit numbers [Haboeck, Levit, and Papini, "Circle STARKs," ePrint 2024/278; confirmed by SP1 Hypercube benchmarks, Succinct Labs, 2025]. This is not algorithmic improvement -- it is the raw physics of computer hardware. A 31-bit multiply is one CPU instruction. A 254-bit multiply is an entire subroutine involving carry propagation, multi-limb multiplication, and modular reduction.

This single insight -- that smaller fields make faster provers -- catalyzed the performance explosion in zero-knowledge proving. Circle STARKs over M31 (Stwo) achieve throughputs that were unimaginable with BN254-based systems. Plonky2 over Goldilocks enabled the first practical recursive STARKs.

But smaller fields introduce a subtlety that Penrose would appreciate for its geometric elegance. A single 31-bit field element provides only 31 bits of security against certain attacks. To achieve 128-bit security, systems use *extension fields*. An extension field is built by the same trick as complex numbers: you take a small field and add extra "dimensions" to your arithmetic, and the security grows with the dimension. The cost is slightly more expensive arithmetic per operation -- but each operation now works in a larger, more secure space -- enlarging $\mathbb{F}_p$ to $\mathbb{F}_{p^k}$ for some small $k$. In Stwo, the extension degree is 4, giving effectively 124 bits. In Neo, the extension is $\mathbb{F}_{q^2}$ over Goldilocks, giving 128 bits. The extension adds complexity but the arithmetic is still vastly cheaper than native 254-bit operations.

### Why This Choice Is a One-Way Door

The field choice is perhaps the most consequential "one-way door" decision in zero-knowledge system design. It cascades through every layer:

- The field determines which commitment schemes are efficient (pairing-friendly fields for KZG, STARK-friendly fields for FRI, cyclotomic fields for lattice schemes).
- The commitment scheme determines which proof systems work (KZG enables Groth16/PLONK, FRI enables STARKs, Ajtai enables lattice folding).
- The proof system determines the arithmetization format (PLONK gates, AIR, CCS).
- The arithmetization determines which programs can be efficiently proved.

Changing the field after deployment means rewriting the compiler, the prover, the verifier, the standard library, and every circuit. It is not a parameter change. It is a complete system redesign.

---


## Summary

The finite field choice is the "which numbers" decision that cascades through every layer above it. Switching from 254-bit primes (BN254, BLS12-381) to 31- or 64-bit primes (BabyBear, M31, Goldilocks) yields roughly 100× faster prover arithmetic because multiplications become single CPU instructions; security is recovered via extension fields. BN254's security margin has additionally eroded from 128 bits to ~100 bits via Tower NFS advances, but it cannot be changed without an Ethereum hard fork.

## Key claims

- BN254: 254-bit prime, embedded in Ethereum EVM precompiles (2017), now estimated at ~100-bit security (down from 128) via Tower NFS [Kim and Barbulescu, 2016].
- BLS12-381: ~253-bit prime, retains 128-bit security estimate; used by Zcash, Filecoin, Midnight, EIP-4844.
- BabyBear ($2^{31} - 2^{27} + 1$, 31-bit): SIMD-friendly; natural FRI commitment; used by RISC Zero and Plonky3.
- Mersenne-31 ($2^{31} - 1$): cheapest modular reduction (single addition); Circle STARKs; used by Stwo.
- Goldilocks ($2^{64} - 2^{32} + 1$, 64-bit): native 64-bit arithmetic; high 2-adicity ($2^{32}$) for large NTT domains; used by Plonky2 and Neo/Nightstream.
- 31-bit arithmetic is ~100× faster than 254-bit arithmetic [Haboeck, Levit, Papini, Circle STARKs ePrint 2024/278; SP1 Hypercube benchmarks, Succinct Labs, 2025].
- Extension fields (degree 2–4) restore security: Stwo uses degree-4 (~124 bits); Neo uses $\mathbb{F}_{q^2}$ over Goldilocks (128 bits).
- Field choice is a one-way door: it determines commitment scheme, proof system, arithmetization, and compiler.

## Entities

- [[babybear]]
- [[bls12-381]]
- [[bn254]]
- [[ceremony]]
- [[goldilocks]]
- [[mersenne]]
- [[ntt]]
- [[plonky3]]
- [[small-field]]

## Dependencies

- [[ch07-four-families-of-commitment-schemes]] — which commitment schemes pair with which fields
- [[ch07-the-cascade-effect]] — how this field choice propagates upward
- [[ch06-circle-starks-and-stwo-a-generational-leap]] — M31 in production (Stwo)
- [[ch02-bn254-s-eroding-security-margin]] — earlier treatment of the BN254 erosion

## Sources cited

- Kim and Barbulescu, "Extended Tower Number Field Sieve," Mathematics of Computation, 2016 — BN254 security revision to ~100 bits
- Haboeck, Levit, Papini, "Circle STARKs," ePrint 2024/278 — 100× performance claim for 31-bit vs 254-bit arithmetic
- SP1 Hypercube benchmarks, Succinct Labs, 2025 — confirming 100× figure

## Open questions

None flagged by this section.

## Improvement notes

## Links

- Up: [[07-the-deep-craft]]
- Prev: [[ch07-the-trilemma-and-its-dissolution]]
- Next: [[ch07-the-quantum-threat-horizon]]
