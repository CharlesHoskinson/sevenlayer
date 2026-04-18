---
title: "The Post-Quantum Horizon"
slug: ch06-the-post-quantum-horizon
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2943, 2958]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
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

Shor's algorithm makes all elliptic-curve-based proof systems (Groth16, PLONK, Halo 2, KZG, Nova) insecure once a cryptographically relevant quantum computer exists. NIST IR 8547 targets 2035 for deprecation; Q-Day estimates range 2032--2035. STARKs are partially quantum-resistant but the hybrid pipeline's Groth16 wrapper reintroduces vulnerability. LatticeFold/Neo/Symphony offer the most direct post-quantum path; no post-quantum on-chain verifier yet exists.

## Key claims

- Shor's algorithm breaks discrete logarithm; all pairing-based systems (Groth16, PLONK, Halo 2, KZG, Nova) become insecure.
- NIST IR 8547 targets 2035 for pre-quantum deprecation; Q-Day estimates: 2032--2035.
- STARKs are partially PQ (hash-based); Grover reduces SHA-256 collision resistance from 128 to ~85 bits, but requires quantum RAM (physically impracticable).
- Hybrid pipeline reintroduces quantum vulnerability at the Groth16 wrapper step (BN254 pairings).
- Neo achieves 127-bit security under Module-SIS/Module-LWE over Goldilocks field.
- No post-quantum on-chain verifier exists in production; lattice proofs are tens of KB vs. hundreds of bytes.
- Closing the on-chain verification gap is an open problem at the frontier.

## Entities

- [[lattice]]
- [[nova]]
- [[hypernova]]
- [[groth16]]
- [[plonk]]
- [[halo2]]
- [[kzg]]
- [[fri]]
- [[goldilocks]]
- [[ntts]]
- [[symphony]]
- [[nist]]
- [[bn254]]
- [[folding]]

## Dependencies

- [[ch06-the-folding-genealogy]] — LatticeFold/Neo/Symphony genealogy is the PQ path
- [[ch07-the-quantum-threat-horizon]] — Chapter 7 covers quantum timeline in detail
- [[ch10-path-three-post-quantum-folding]] — Chapter 10 places this as Path Three in the three-path synthesis
- [[ch02-the-quantum-shelf-life]] — quantum shelf-life framing from Chapter 2

## Sources cited

- NIST IR 8547, "Transition to Post-Quantum Cryptography Standards," 2024.

## Open questions

- No post-quantum on-chain verifier exists; closing this gap (lattice-friendly L1 precompiles or novel compression) is an open problem flagged by this section.

## Improvement notes

- [P2] (A) "Shor's algorithm breaks the discrete logarithm problem in polynomial time. This means every proof system built on elliptic curve cryptography … becomes insecure. Not 'might become insecure.' Becomes insecure." — the certainty is slightly overstated; Shor's algorithm requires a cryptographically relevant quantum computer (fault-tolerant, large-scale) that does not yet exist; the phrasing conflates mathematical implication with practical threat; a hedge ("once a sufficiently powerful quantum computer exists") would be more precise
- [P3] (E) "No post-quantum on-chain verifier exists in production" — accurate, but the section could briefly mention NIST PQC standardization (CRYSTALS-Dilithium, FALCON) and why none of those directly apply to on-chain ZK verifiers, to help readers understand the gap

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-snark-recursion-vs-folding-the-full-picture]]
- Next: [[ch06-from-speed-race-to-security-race]]
