---
title: "The Trilemma -- And Its Dissolution"
slug: ch07-the-trilemma-and-its-dissolution
chapter: 7
chapter_title: "Layer 6 -- The Deep Craft"
heading_level: 2
source_lines: [3150, 3184]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 643
---

## The Trilemma -- And Its Dissolution

The original paper presented a "cryptographic primitives trilemma": a claim that any commitment scheme can achieve at most two of three desirable properties.

1. **Algebraic functionality** -- the homomorphic structure needed for folding, composition, and efficient recursive proving.
2. **Post-quantum security** -- resilience against quantum computers running Shor's and Grover's algorithms.
3. **Succinctness** -- small proofs and fast verification.

The trilemma positioned the four families like this:

- **KZG** achieves algebraic functionality and succinctness but lacks post-quantum security.
- **FRI** achieves post-quantum security but lacks algebraic functionality (no homomorphism, so no folding) and offers only moderate succinctness (large proofs).
- **IPA** achieves moderate algebraic functionality but lacks both post-quantum security and full succinctness (linear verification).
- **Lattice** achieves algebraic functionality and post-quantum security. Succinctness is the remaining gap.

This framing was useful as a historical snapshot. As a statement of permanent truth, it is increasingly wrong.

The lattice revolution -- Greyhound (2024), LatticeFold (2024), LatticeFold+ (2025), Neo (2025), Symphony (2026) -- has been systematically closing the succinctness gap. Greyhound demonstrated 50-kilobyte proofs with sublinear verification. LaBRADOR achieved 58-kilobyte proofs for large constraint systems. Symphony's high-arity folding can compress a final proof via a compact SNARK that, if instantiated with a pairing-based scheme, produces constant-size output -- and if instantiated with a lattice-based scheme, remains fully post-quantum.

The trilemma is better understood as a *spectrum* that is being actively compressed. The engineering challenge is real (lattice proofs are still 1000x larger than KZG), but the trajectory is clear: lattice schemes are approaching practical competitiveness, and the gap shrinks with each generation. What looked like a permanent constraint on the geometry of the design space is turning out to be an artifact of our current engineering, not a law of mathematical nature.

To see the trilemma clearly, state the three properties any polynomial commitment scheme would ideally achieve:

1. **Small proofs, constant size.** The proof should not grow with the size of the polynomial. Ideally, one group element or a fixed number of bytes, regardless of degree.
2. **Fast verification, constant time.** The verifier's work should not depend on the polynomial's complexity. Ideally, a single algebraic check.
3. **No trusted setup, transparent.** The scheme should require no ceremony, no toxic waste, no trust assumptions beyond the hardness of a mathematical problem.

No known scheme achieves all three. KZG achieves the first two but requires a trusted setup ceremony. FRI achieves the third (transparent) and offers reasonable verification (polylogarithmic), but its proofs are polylogarithmic rather than constant -- orders of magnitude larger. IPA achieves the third (transparent) with logarithmic proofs (impressively small), but its verification is linear -- the verifier must do work proportional to the polynomial's degree. Lattice commitments achieve the third (transparent) with logarithmic proofs, but verification is sublinear rather than constant.

The question that should keep a mathematician awake at night is: *is this trilemma fundamental?* Is there a theorem -- an impossibility result, an information-theoretic lower bound -- proving that no commitment scheme can simultaneously achieve constant-size proofs, constant-time verification, and transparency?

The answer, as of 2026, is no. No one has proven that the ideal PCS is impossible. The barriers are engineering barriers, not mathematical barriers. The bilinear pairing that gives KZG its constant-size miracle is a specific algebraic structure tied to elliptic curves, and elliptic curves require structured reference strings to exploit pairings. But nothing in information theory says that constant-size polynomial commitments *require* pairings. Nothing says that transparency *requires* large proofs. The ideal scheme -- transparent, constant-size, constant-verification, post-quantum -- remains the field's holy grail. It may not exist. But its impossibility has not been proven, and the gap between what lattice schemes achieve today and what that grail demands shrinks with every new construction. The trilemma may be less a law of nature than a confession of our current ignorance.

---


## Summary

The "cryptographic primitives trilemma" claims no commitment scheme can simultaneously achieve algebraic functionality, post-quantum security, and succinctness. As of 2026 the lattice revolution (Greyhound, LatticeFold, LatticeFold+, Neo, Symphony) is systematically closing the succinctness gap, suggesting the trilemma is an engineering artifact rather than a mathematical law — no impossibility proof exists for a scheme that is transparent, constant-size, constant-verification, and post-quantum.

## Key claims

- The trilemma: any PCS achieves at most two of {algebraic functionality, post-quantum security, succinctness}.
- KZG: functionality + succinctness, not PQ. FRI: PQ + moderate succinctness, no algebraic homomorphism. IPA: transparency + log proofs, but linear verification. Lattice: functionality + PQ, succinctness gap.
- Greyhound (2024): ~50 KB proofs with sublinear verification from Module-SIS alone.
- LaBRADOR: 58 KB for large constraint systems.
- Symphony (2026): high-arity folding can compress final proof to constant size via a compact SNARK, optionally pairing-based or fully post-quantum.
- The lattice succinctness gap is ~1,000× versus KZG but shrinks with each generation; the trilemma is a spectrum being compressed, not a fixed partition.
- No impossibility theorem has been proven for the ideal PCS; the barriers are engineering, not mathematical.

## Entities

- [[fri]]
- [[ipa]]
- [[kzg]]
- [[latticefold]]
- [[lattice]]

## Dependencies

- [[ch07-four-families-of-commitment-schemes]] — establishes the four families this trilemma maps
- [[ch07-lattice-based-proving]] — the lattice revolution dissolving the succinctness gap
- [[ch07-three-hardness-assumptions-three-worlds]] — the hardness landscape the trilemma sits within

## Sources cited

None in this section.

## Open questions

- Whether an impossibility theorem for the "ideal PCS" (transparent + constant-size + constant-verification + post-quantum) can be proven or refuted.

## Improvement notes

- [P1] (B) "The original paper presented a 'cryptographic primitives trilemma'" — no citation given for which paper introduced this trilemma framing. If this is an original synthesis rather than a cited result, the language should say so rather than implying a specific source.
- [P2] (A) FRI is described as achieving "post-quantum security but lacks algebraic functionality (no homomorphism, so no folding) and offers only moderate succinctness (large proofs)" — the trilemma as stated has three properties, but the text inconsistently uses "moderate succinctness" for FRI in the list and then later says FRI "achieves post-quantum security" and "reasonable verification (polylogarithmic)" — the mapping of FRI to exactly two of three properties is blurred.
- [P2] (B) Symphony (2026) appears in key claims with "ePrint 2025/1905" but Sources cited lists nothing for this section; the Symphony citation should be in Sources cited.
- [P3] (C) The closing rhetorical question ("*is this trilemma fundamental?*") is effective but the multi-sentence follow-up "The answer, as of 2026, is no" paragraph has an AI-essay cadence (question → answer → hedged elaboration → conclusion). Could be tightened.

## Links

- Up: [[07-the-deep-craft]]
- Prev: [[ch07-four-families-of-commitment-schemes]]
- Next: [[ch07-small-fields]]
