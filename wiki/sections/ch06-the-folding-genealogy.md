---
title: "The Folding Genealogy"
slug: ch06-the-folding-genealogy
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2564, 2628]
source_commit: 53f41415d307dcd4ed73d852dfd6aa97146e882f
status: reviewed
word_count: 1197
---

## The Folding Genealogy

Folding is not a single technique. It is a research program that has produced a lineage of increasingly general schemes over the past four years. Understanding this lineage matters for seeing where proof systems are headed -- including the post-quantum frontier.

Before tracing each step, here is the map. Read it the way a naturalist reads a field guide: not to memorize every species, but to understand the territory they occupy. The folding genealogy advances along four independent axes:

- **Constraint generality:** R1CS (Nova) to CCS (HyperNova), covering all major arithmetizations.
- **Instance generality:** Single-instance (Nova) to multi-instance (ProtoGalaxy), enabling parallel proving.
- **Instruction generality:** Uniform IVC (Nova) to non-uniform IVC (SuperNova, SuperNeo), enabling VM execution.
- **Cryptographic generality:** Elliptic curves (Nova through CycleFold) to lattices (LatticeFold, Neo, Symphony), enabling post-quantum security.

Every scheme in the genealogy that follows advances along at least one of these axes.

### Nova (2022): The Origin

Kothapalli, Setty, and Tzialla. Folding for R1CS. The verifier performs one scalar multiplication plus hashing -- roughly 10,000 R1CS gates of recursive overhead. Prover cost is linear in the circuit size. This is the paper that made folding practical. Every subsequent folding scheme either extends, generalizes, or adapts Nova's core ideas.

### SuperNova (2022): Non-Uniform IVC

Kothapalli and Setty. Extended Nova to support multiple circuit types. Instead of one step function that repeats, SuperNova allows different step functions at each step -- exactly what you need for a virtual machine, where each instruction has a different circuit. The scheme maintains one running instance per instruction type and pays only for the circuit of the instruction actually executed. This is the "pay-per-instruction" property that makes folding-based zkVMs viable.

### HyperNova (2023): The Generalization Point

Kothapalli and Setty again. This paper is the pivot of the entire genealogy.

HyperNova generalized folding from R1CS to CCS -- Customizable Constraint Systems -- which subsume R1CS, PLONKish, and AIR in a single framework. The central enabler was the sumcheck protocol, introduced by Lund, Fortnow, Karloff, and Nisan (FOCS 1990; JACM 1992), one of the most elegant tools in theoretical computer science. It reduces the task of checking a sum over a large domain (say, $2^{20}$ evaluations of a multilinear polynomial) to checking a single evaluation at a random point. The verifier sends random challenges in each round; the prover responds with univariate polynomials. After $\log(n)$ rounds, the verifier has a single-point claim that can be checked directly.

HyperNova uses sumcheck to fold CCS instances without degree blowup. A CCS constraint has the form: sum of products of matrix-vector multiplications equals zero. This is inherently higher-degree than R1CS. Without sumcheck, folding such constraints would require the verifier to handle cross-terms whose degree grows with the constraint degree. Sumcheck reduces the multilinear CCS equation to a single-point evaluation, allowing the folded instance to retain its structure. The verifier cost remains $O(\log m)$ field operations plus one scalar multiplication -- essentially the same as Nova, despite handling a strictly more general constraint system.

HyperNova is the generalization point because everything after it works in the CCS framework. If Nova gave folding a body, HyperNova gave it a universal language. CCS is to constraint systems what SQL is to databases: a common tongue that lets you express any query regardless of the underlying storage engine.

### ProtoStar and ProtoGalaxy (2023): Alternative Paths

These two schemes took different approaches to generalizing folding. ProtoStar (Bunz and Chen, ePrint 2023/620) built a generic accumulation framework for any interactive argument satisfying "special soundness" -- a more abstract starting point than HyperNova's CCS-specific approach. ProtoGalaxy (Eagen and Gabizon, ePrint 2023/1106) introduced multi-instance folding: folding k instances simultaneously in a single round, rather than folding pairs sequentially. This enables high-arity proof-carrying data trees, which are needed for parallel proof generation.

Both contributed important ideas to the field, but the main trunk of the genealogy runs through HyperNova because CCS became the dominant constraint language.

### CycleFold (2023): The Practical Fix

Kothapalli and Setty. This is the engineering paper that made all the theoretical folding schemes practical over elliptic curves. The problem: Nova's folding verifier includes a scalar multiplication, which requires non-native field arithmetic when working over a 2-cycle of curves. CycleFold delegates this scalar multiplication to a co-processor circuit on the second curve, where it can be computed natively. This reduced the second-curve circuit from roughly 10,000 gates to 1,500. Not glamorous, but essential. CycleFold is the standard technique used in every practical implementation of Nova and HyperNova.

### LatticeFold (ASIACRYPT 2025): Crossing Into Post-Quantum Territory

Boneh and Chen (ePrint 2024/257), published at ASIACRYPT 2025. LatticeFold was the first folding scheme based on lattice assumptions rather than elliptic curve assumptions. This matters enormously, because lattice problems (Module-SIS, Module-LWE) are believed to resist quantum attacks, while elliptic curve discrete logarithm falls to Shor's algorithm.

LatticeFold replaced elliptic curve commitments with Ajtai-style lattice commitments: $\text{Commit}(A, m, r) = A \cdot [m; r] \bmod q$, where $A$ is a public matrix, $m$ is the message, and $r$ is randomness. These commitments are linearly homomorphic -- exactly the property that folding needs to combine instances via random linear combination. But LatticeFold worked over large fields ($q \approx 2^{128}$), which made arithmetic expensive. Its successor, LatticeFold+ (Boneh and Chen, CRYPTO 2025; ePrint 2025/247), addressed this with faster, shorter proofs.

### Neo (2025): Small Fields and Pay-Per-Bit

Wilson Nguyen and Srinath Setty. Neo adapted HyperNova's CCS folding to lattice-based commitments over small fields -- specifically the Goldilocks field ($q = 2^{64} - 2^{32} + 1$) with the cyclotomic ring $\mathbb{F}_q[X]/(\Phi_{81})$, where $\Phi_{81}(X) = X^{54} + X^{27} + 1$. Working over a 64-bit field instead of a 128-bit field makes arithmetic dramatically faster, particularly on GPUs where 64-bit integer operations are natively supported.

Neo introduced a property called "pay-per-bit commitments." In an Ajtai commitment, the cost of committing depends on the binary representation of the witness. Committing to a single bit costs 32 times less than committing to a 32-bit value. This means the prover can commit to a binary witness at a fraction of the cost of committing to field elements -- a property unique to the lattice setting that has no analog in elliptic curve commitments.

SuperNeo, presented within the same paper, extended Neo to non-uniform IVC (the lattice analog of SuperNova), supporting multiple instruction types for VM execution.

### Symphony (2026): Production-Grade Lattice Folding

Symphony independently extended lattice-based folding to high-arity settings and refined the protocol for practical deployment. Key additions included optimized Number Theoretic Transforms over the cyclotomic ring for fast polynomial multiplication, a GPU-friendly architecture (lattice operations -- matrix-vector products, NTTs -- parallelize naturally), and formal bridge theorems connecting the folding scheme's knowledge soundness to the underlying Module-SIS and Module-LWE assumptions. (Symphony is a 2026 result; as of this writing it circulates as a preprint and has not yet appeared in formal proceedings.)

Symphony demonstrated that lattice-based folding can be practical, not just theoretical. With GPU acceleration, it achieves practical proving times, closing the performance gap with elliptic-curve-based systems while maintaining plausible post-quantum security.

Each step in the genealogy broadened the reach of folding without sacrificing its fundamental advantage: logarithmic verifier cost and linear prover cost per step. The entire genealogy, from Nova to Symphony, spans just three years. This rate of progress is unusual even by the standards of a fast-moving field.

---


## Summary

The folding research lineage advances along four axes: constraint generality (R1CS→CCS), instance generality (single→multi), instruction generality (uniform→non-uniform IVC), and cryptographic generality (elliptic curves→lattices). Nova (2022) started it; HyperNova (2023) generalized to CCS via sumcheck; LatticeFold/Neo/Symphony (2024--2026) reached post-quantum security over small fields.

## Key claims

- Four axes of progress: constraint generality, instance generality, instruction generality, cryptographic generality.
- Nova (2022): R1CS folding, ~10,000-gate verifier, linear prover cost.
- SuperNova (2022): non-uniform IVC -- different circuits per VM instruction, pay-per-instruction.
- HyperNova (2023): generalized folding to CCS using sumcheck; verifier cost $O(\log m)$ plus one scalar multiplication.
- CycleFold (2023): reduced non-native scalar multiplication from ~10,000 to ~1,500 gates via secondary-curve co-processor.
- LatticeFold (Boneh and Chen, ASIACRYPT 2025): first lattice-based folding scheme, Ajtai commitments over $q \approx 2^{128}$.
- Neo (Nguyen and Setty, 2025): CCS folding over Goldilocks field with pay-per-bit commitments; SuperNeo adds non-uniform IVC.
- Symphony (2026): production-grade lattice folding with GPU-optimized NTTs and formal Module-SIS/Module-LWE soundness bridge.

## Entities

- [[nova]]
- [[hypernova]]
- [[folding]]
- [[lattice]]
- [[ajtai]]
- [[goldilocks]]
- [[ntts]]
- [[symphony]]
- [[setty]]
- [[boneh]]
- [[gabizon]]

## Dependencies

- [[ch06-recursion-vs-folding-russian-dolls-and-snowballs]] — introduces folding concept and relaxed R1CS
- [[ch05-ccs-the-rosetta-stone]] — CCS framework that HyperNova generalizes to
- [[ch05-the-sumcheck-protocol-the-hidden-foundation]] — sumcheck is the technical enabler of HyperNova
- [[ch06-the-post-quantum-horizon]] — post-quantum implications of the lattice folding branch
- [[ch07-lattice-based-proving]] — Chapter 7 details the lattice assumptions underlying LatticeFold/Neo/Symphony

## Sources cited

- Kothapalli, Setty, Tzialla, "Nova: Recursive Zero-Knowledge Arguments from Folding Schemes," CRYPTO 2022.
- Kothapalli, Setty, "HyperNova: Recursive Arguments for Customizable Constraint Systems," CRYPTO 2024.
- Kothapalli, Setty, "CycleFold: Folding-scheme-based recursive arguments over a cycle of elliptic curves," ePrint 2023/1192.
- Boneh, Chen, "LatticeFold: A Lattice-based Folding Scheme and its Applications," ASIACRYPT 2025.
- Nguyen, Setty, "Neo: Lattice-based Folding over Small Fields," ePrint 2025.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P3] (E) The "four axes" framing is introduced but the Axes table is never explicitly revisited for LatticeFold, Neo, and Symphony — a one-line "axes advanced" annotation per scheme would make the framework payoff clearer

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-recursion-vs-folding-russian-dolls-and-snowballs]]
- Next: [[ch06-nightstream-what-a-folding-engine-looks-like-from-the-inside]]
