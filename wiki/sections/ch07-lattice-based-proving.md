---
title: "Lattice-Based Proving"
slug: ch07-lattice-based-proving
chapter: 7
chapter_title: "Layer 6 -- The Deep Craft"
heading_level: 2
source_lines: [3279, 3332]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 927
---

## Lattice-Based Proving

Against this backdrop -- the ticking clock, the harvest-now threat, the cliff edge -- a research program has been steadily building an alternative: lattice-based zero-knowledge proof systems that provide post-quantum security without sacrificing the algebraic structure needed for efficient proving.

The progression has been fast, compressing a decade of typical cryptographic development into two years.

### Stage 1: Greyhound (2024)

The first demonstration that lattice-based SNARKs could be practical, not just theoretical. Greyhound achieved approximately 50-kilobyte proofs with sublinear (square root of N) verification, built entirely on Module-SIS. It was a standalone SNARK, not a folding scheme -- a proof of concept that lattice proofs could fit in the same order of magnitude as STARK proofs.

### Stage 2: LatticeFold (2024)

The conceptual breakthrough. Dan Boneh and Binyi Chen adapted Nova-style folding to work over cyclotomic rings with Ajtai commitments. The key insight: Ajtai's module homomorphism is the lattice analogue of Pedersen's additive homomorphism, and it is sufficient to enable the random-linear-combination technique that makes folding work.

LatticeFold introduced three composable reductions -- $\Pi_{\text{CCS}}$ (constraint satisfaction to evaluation claims), $\Pi_{\text{RLC}}$ (random linear combination), and $\Pi_{\text{DEC}}$ (decomposition to control norm growth) -- that together form a complete folding scheme for CCS (Customizable Constraint Systems).

But LatticeFold had a critical limitation. It was restricted to power-of-two cyclotomic polynomials of the form $X^d + 1$. Over the Goldilocks field, this polynomial splits completely into degree-1 factors, meaning each NTT slot has only 64-bit security -- insufficient for the 128-bit target.

### Stage 3: LatticeFold+ (2025)

A comprehensive improvement: 5 to 10 times faster prover, simpler verification circuit, shorter folding proofs, and a new purely algebraic range proof replacing LaBRADOR's more complex approach. LatticeFold+ identified three concrete parameterizations, including one over Goldilocks with the 81st cyclotomic polynomial $\Phi_{81} = X^{54} + X^{27} + 1$. This polynomial does not split into linear factors over Goldilocks; instead, it factors into degree-2 irreducibles, giving the extension field $K = \mathbb{F}_{q^2}$ with 128-bit NTT slots.

LatticeFold+ also introduced a general composition theorem: if one reduction is "phi-restricted" with restricted knowledge soundness, and another is "phi-relaxed" knowledge sound, their composition is knowledge sound. This provided the formal foundation for chaining reductions.

### Stage 4: Neo (2025)

Neo overcame LatticeFold's power-of-two limitation directly. Its central innovation is the *rotation matrix encoding* -- the "bar transform" -- which represents ring elements as rotation matrices in a commutative subring of the matrix ring. The map sends a ring element $a$ in $R_q$ to a $d \times d$ matrix $\text{rot}(a)$, and this map is a ring isomorphism. The payoff: the matrix commitment scheme becomes S-homomorphic: $\text{rot}(\rho) \cdot \text{Com}(Z) = \text{Com}(\text{rot}(\rho) \cdot Z)$.

Neo works natively over Goldilocks with $\Phi_{81}$, giving $d = 54$, $\kappa = 16$, $m = 2^{24}$, and 127-bit post-quantum security (verified via the standard lattice estimator). The guard condition $(k+1) \cdot T \cdot (b-1) = 2{,}808 < 4{,}096 = B$ ensures that norm growth remains bounded across arbitrarily many folding steps.

### Stage 5: Symphony (2026)

The most ambitious design. Symphony pushes folding to high arity -- folding 1,024 or more instances in a single step, rather than the standard two. This eliminates the need for recursive IVC (which requires embedding hash verification inside the SNARK circuit, a major overhead). Symphony folds $\text{poly}(\lambda)$ NP statements into two committed linear statements in one shot, then proves these with a compact SNARK.

Symphony also introduces approximate range proofs (replacing the exact norm proofs of LatticeFold+), reducing verification complexity further. Its concrete instantiation can handle $2^{32}$ R1CS constraints -- over four billion -- in a single batch.

If Symphony's compact SNARK is instantiated with a pairing-based scheme (Groth16), the final proof is constant-size. If instantiated with a lattice-based scheme, the entire pipeline is post-quantum. This modularity is the architectural insight: separate the bulk proving (which must be post-quantum) from the final compression (which can optionally use classical tools for maximum succinctness).

### The Key Algebraic Insight

The entire lattice folding line rests on a single algebraic fact that deserves to be stated plainly, because it is the kind of fact that sounds narrow but turns out to govern everything.

An Ajtai commitment over the ring $R_q$ is *module-homomorphic*. This means that for any challenge element $\rho$ drawn from a strong sampling set with small coefficients, the equation $\rho \cdot \text{Com}(Z) = \text{Com}(\rho \cdot Z)$ holds. This is the lattice analogue of the scalar homomorphism that makes Nova-style folding work over elliptic curves.

But the lattice version is richer. The challenge $\rho$ is not a scalar but a *ring element* -- equivalently, a $d \times d$ rotation matrix. This richer structure enables three things simultaneously:

1. **Folding with norm control.** Challenges from the strong sampling set $\mathcal{C}$ have small coefficients (in $\{-2, -1, 0, 1, 2\}$ for Neo), so the folded witness grows slowly in norm.
2. **Sum-check compatibility.** Ring evaluation claims can be verified via the sum-check protocol over the base field, connecting the commitment layer to the constraint satisfaction layer.
3. **Decomposition.** The accumulated norm can be reduced back to the base bound $b$ via bit-decomposition, enabling unbounded recursion without norm blowup.

This algebraic trifecta -- homomorphism, sum-check compatibility, and decomposition -- is what makes lattice-based folding possible. It is the "deep craft" of Layer 6: not a single clever trick, but an interlocking set of algebraic properties that together provide something no other family offers. The geometry of the lattice (its distances, its short vectors, its algebraic symmetries) does the work that pairings do in the elliptic curve world, but without the quantum vulnerability.

---


## Summary

The lattice proving research program compressed a decade of development into two years (2024–2026) through five stages: Greyhound (first practical lattice SNARK, ~50 KB), LatticeFold (Nova-style folding on cyclotomic rings, 2024), LatticeFold+ (5–10× faster prover, Goldilocks with Φ₈₁, 2025), Neo (rotation matrix encoding enabling native Goldilocks + 127-bit PQ security, 2025), and Symphony (high-arity folding of 1,024+ instances, handles 2³² R1CS constraints, 2026). The entire line rests on Ajtai module homomorphism: ρ · Com(Z) = Com(ρ · Z).

## Key claims

- Greyhound (2024): ~50 KB proofs, sublinear (√N) verification, built entirely on Module-SIS — first practical lattice SNARK.
- LatticeFold (2024, Boneh and Chen): three composable reductions (Π_CCS, Π_RLC, Π_DEC) adapt Nova folding to cyclotomic rings with Ajtai commitments; limited to power-of-two cyclotomics.
- LatticeFold+ (2025): 5–10× prover speedup; uses Φ₈₁ = X⁵⁴ + X²⁷ + 1 over Goldilocks giving degree-2 irreducible factors and $\mathbb{F}_{q^2}$ extension with 128-bit NTT slots.
- Neo (2025): rotation matrix "bar transform" — ring element a maps to d×d rotation matrix rot(a), making commitment S-homomorphic; Φ₈₁, d=54, κ=16, m=2²⁴, 127-bit PQ security; guard condition (k+1)·T·(b−1) = 2,808 < 4,096 = B ensures bounded norm growth.
- Symphony (2026): high-arity folding (1,024+ instances per step), approximate range proofs, handles 2³² R1CS constraints; final proof is constant-size if wrapped with Groth16, or fully PQ if wrapped with lattice SNARK.
- Algebraic trifecta enabling lattice folding: homomorphism (norm control), sum-check compatibility, and decomposition (unbounded recursion without norm blowup).

## Entities

- [[ajtai]]
- [[boneh]]
- [[folding]]
- [[goldilocks]]
- [[latticefold]]
- [[lattice]]
- [[nova]]
- [[ntt]]
- [[pedersen]]
- [[symphony]]

## Dependencies

- [[ch07-three-hardness-assumptions-three-worlds]] — Module-SIS foundation for Ajtai commitments
- [[ch07-the-quantum-threat-horizon]] — motivation for the post-quantum program
- [[ch06-the-folding-genealogy]] — Nova and HyperNova lineage that LatticeFold adapts
- [[ch06-nightstream-what-a-folding-engine-looks-like-from-the-inside]] — Neo/Nightstream implementation context

## Sources cited

- Boneh and Chen, LatticeFold — ASIACRYPT 2025
- LatticeFold+ — CRYPTO 2025
- Symphony — ePrint 2025/1905

## Open questions

None flagged by this section.

## Improvement notes

## Links

- Up: [[07-the-deep-craft]]
- Prev: [[ch07-the-quantum-threat-horizon]]
- Next: [[ch07-case-study-midnight]]
