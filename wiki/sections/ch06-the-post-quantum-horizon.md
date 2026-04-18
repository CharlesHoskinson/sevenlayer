---
title: "The Post-Quantum Horizon"
slug: ch06-the-post-quantum-horizon
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2937, 2952]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 329
---

## The Post-Quantum Horizon

Everything we have discussed in this chapter faces an existential question: what happens when quantum computers arrive?

Shor's algorithm breaks the discrete logarithm problem in polynomial time. This means every proof system built on elliptic curve cryptography -- Groth16, PLONK, Halo 2, KZG commitments, all of Nova's original elliptic-curve-based instantiations -- becomes insecure. Not "might become insecure." Becomes insecure. The mathematical fact is established; only the engineering timeline is uncertain.

The NIST IR 8547 deprecation schedule targets 2035 for phasing out pre-quantum cryptography. Conservative estimates for "Q-Day" -- the date when a cryptographically relevant quantum computer exists -- range from 2032 to 2035. For blockchain systems with 10+ year lifespans, this means systems deployed today must either plan for migration or be built on quantum-resistant foundations from the start.

The STARK family is already partially quantum-resistant: its security rests on collision-resistant hash functions, which resist quantum attacks (though Grover's algorithm reduces their effective security, SHA-256's collision resistance drops from 128 bits to roughly 85 bits under the BHT algorithm, though this attack requires quantum random-access memory, which is widely considered physically impracticable with current technology). But the STARK-to-SNARK wrapping pipeline reintroduces quantum vulnerability at the final step, because the Groth16 wrapper uses BN254 pairings.

The lattice folding branch of the genealogy -- LatticeFold, Neo, Symphony -- represents the most direct path to post-quantum proof systems. Neo achieves 127-bit security under plausible lattice hardness assumptions (Module-SIS, Module-LWE), operates over the GPU-friendly Goldilocks field, and supports the full CCS constraint framework via sumcheck-based folding. Symphony extends this to production-grade performance with GPU-optimized NTTs.

The remaining gap is on-chain verification. No post-quantum on-chain verifier exists in production. Lattice-based proofs are larger than elliptic-curve-based proofs (tens of kilobytes vs. hundreds of bytes), and no blockchain has precompiled contracts for lattice operations. Closing this gap -- either through lattice-friendly L1 verification or through novel compression techniques -- is one of the open problems at the frontier of the field.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
