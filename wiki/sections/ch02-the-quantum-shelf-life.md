---
title: "The Quantum Shelf Life"
slug: ch02-the-quantum-shelf-life
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [622, 650]
source_commit: b3ed881318761d3fd0e65ead7ea58e3f6536ccf9
status: reviewed
word_count: 1003
---

## The Quantum Shelf Life

The stage is built. The universal SRS is published. The economic case for ceremonies is clear. The question now is how long the stage lasts.

Every pairing-based proof system -- Groth16, PLONK, Marlin, Sonic, KZG -- rests on the hardness of the discrete logarithm problem on elliptic curves. Shor's algorithm, running on a sufficiently powerful quantum computer, solves the discrete logarithm problem in polynomial time.

This is not "might break." This is "does break, given sufficient hardware." The question is when, not whether. Two dates are often conflated and should not be. NIST's IR 8547 sets a *deprecation schedule for pre-quantum cryptographic algorithms*, targeting 2035 for the retirement of the pre-quantum suite across federal systems [NIST, "Transition to Post-Quantum Cryptography Standards (IR 8547)," November 2024]. That is a regulatory deadline for migration, not a prediction of when a cryptographically relevant quantum computer (CRQC) arrives. Independent estimates of CRQC arrival spread across a wide band. The NSA's CNSA 2.0 FAQ plans for NSS equipment transitions completed by 2030 and a fully quantum-resistant NSS by 2035, reflecting a precautionary posture rather than a dated forecast [NSA, "Commercial National Security Algorithm Suite 2.0 FAQ," 2022, rev. 2024]. Academic timelines -- including the Mosca-Piani "quantum threat timeline" style of analysis -- place meaningful probability on CRQC arrival anywhere in the 2030-2040 window, with the tails reaching earlier and later. The summary: regulators are working to a 2035 migration deadline because the probability of a CRQC within the following decade is not negligible, not because anyone has a model that says it will arrive that year.

The implications for Layer 1 are stark. A quantum computer would not need to compromise any ceremony participant. It would not need to break into anyone's hardware or bribe anyone. It would simply take the *public SRS* -- the list of elliptic curve points that everyone can see -- and extract the original trapdoor from it. Mathematically, irreversibly, without detection.

Once the trapdoor is extracted, every proof ever generated under that SRS becomes suspect. The attacker can forge proofs of false statements indistinguishable from legitimate ones. The six-figure ceremony becomes irrelevant. The toxic waste was not in anyone's memory or on anyone's hard drive -- it was encoded in the public parameters all along, waiting for a quantum computer powerful enough to read it.

This creates a concept we will call the *quantum shelf life* of a trusted setup. A KZG ceremony conducted in 2023 produces an SRS that is secure against classical computers indefinitely but has a finite lifespan against quantum adversaries. If that SRS secures a blockchain expected to operate for 20 years, the setup's shelf life may expire before the system's intended lifetime ends.

STARKs, by contrast, rely on collision-resistant hash functions, which are believed to resist quantum computers. The caveat "believed to" deserves scrutiny. Grover's algorithm gives a quantum computer a quadratic speedup for brute-force search, which effectively halves the security level of hash functions: 256-bit classical security becomes 128-bit quantum security. This is a quantitative adjustment, not a qualitative break -- you double your hash output size and move on. More subtly, the BHT algorithm can reduce collision resistance further, but it requires quantum random-access memory (qRAM), which is widely considered physically impracticable with current technology. In sum: hash-based systems *probably* survive quantum computers with parameter adjustments, but the unqualified claim that they are "post-quantum secure" gives false confidence. What we can say is that no known quantum algorithm breaks them in the way Shor's algorithm breaks elliptic curves -- completely, efficiently, and with mathematical certainty.

A transparent STARK-based setup has no quantum shelf life problem because there is no trapdoor to extract. The "stage" is made of hash functions, and hash functions do not have secrets.

This brings us to the concept of *option value*. A transparent setup preserves the option to migrate to post-quantum cryptography without re-ceremony. A trusted setup on a pairing-friendly curve burns this option: if the post-quantum deadline arrives and your SRS lives on BLS12-381, you need a new setup from scratch. Given the NIST 2035 migration target and the CRQC uncertainty band above, systems designed today with 10+ year lifespans should seriously consider whether the performance advantages of pairing-based setups justify the loss of post-quantum migration flexibility.

Midnight's choice of BLS12-381 illustrates this tension concretely. BLS12-381 provides approximately 128-bit classical security but offers zero post-quantum security. Every component of Midnight's proof system -- the SRS, the polynomial commitments, the proof verification -- rests on assumptions that quantum computers break. Midnight originally experimented with Pluto-Eris curves (which enabled recursive proof composition), but switched back to BLS12-381 in April 2025 for pragmatic reasons: faster proof generation, an existing standardized trusted setup in place of a bespoke Pluto-Eris ceremony, wider ecosystem compatibility, and better tooling support [Midnight Network, "Midnight's Proving System is Switching from Pluto Eris to BLS," April 2025, docs.midnight.network/blog/zkp]. The switch optimized for present-day deployment at the cost of future quantum vulnerability.

The alternative approach -- exemplified by systems like Neo [Nguyen, Setty, "Neo: Lattice-based Folding Scheme for CCS over Small Fields and Pay-per-bit Commitments," IACR ePrint 2025/294] -- uses lattice-based cryptography. Instead of relying on the discrete logarithm problem (which Shor's algorithm breaks), lattice-based systems rely on the difficulty of finding short vectors in high-dimensional geometric structures -- mathematical problems that no known quantum algorithm significantly accelerates. The tradeoff: larger proofs, more expensive verification, and a transparent setup that requires no ceremony at all. The trust assumption shrinks from "1-of-N ceremony participants were honest" to "the lattice problem is hard" -- a purely mathematical assumption with no sociological component. NIST chose lattice problems as the foundation for its post-quantum encryption and signature standards (FIPS 203, 204) in August 2024, lending institutional weight to the conjecture.

Neither choice is unambiguously correct. They represent different bets on the future, and the stakes of the bet are not symmetric. If Midnight is right -- if quantum computers are 20+ years away -- it gains years of performance advantage and ecosystem maturity. If Midnight is wrong -- if a cryptographically relevant quantum computer arrives in 2032 -- every shielded transaction, every private token transfer, every confidential smart contract ever executed on Midnight becomes retroactively decryptable. The privacy guarantees the system offered its users will have been temporary, not permanent, and the users will not have known this when they made their deposits.

Lattice-based systems face the opposite asymmetry. If they are right about the quantum timeline, they will have been prepared while pairing-based systems scramble to migrate. If they are wrong -- if quantum computers are 30+ years away -- they will have paid a performance and proof-size penalty for decades, competing against faster, more mature systems that had the luxury of ignoring the threat. Nobody knows which bet is right, because nobody knows when quantum computers will arrive at cryptographic scale. But the asymmetry of consequences favors caution for any system whose privacy guarantees are meant to outlast its designers' careers.



## Summary

Every pairing-based proof system rests on the discrete logarithm problem, which Shor's algorithm breaks completely on a quantum computer; NIST's deprecation roadmap (IR 8547) targets 2035 for retirement of all pre-quantum algorithms. A quantum adversary would extract the trapdoor directly from the public SRS, rendering all historical proofs forgeable without touching any ceremony participant. Transparent STARK setups avoid this: no trapdoor exists, and hash functions degrade only quadratically under Grover's algorithm.

## Key claims

- Conservative estimates place cryptographically relevant quantum computers at 2032–2035.
- NIST finalized post-quantum standards in August 2024 and targets 2035 for deprecation of pre-quantum algorithms (IR 8547).
- A quantum computer extracts the trapdoor from the public SRS — the ceremony becomes irrelevant.
- Grover's algorithm halves hash security (256-bit → 128-bit effective); BHT further reduces it but requires impractical quantum RAM.
- Midnight chose BLS12-381 over Pluto-Eris in April 2025 for faster proofs and ecosystem compatibility, accepting the quantum exposure.
- Lattice-based systems (e.g., Neo, Nguyen and Setty, 2025) require no ceremony; trust reduces to "the lattice problem is hard."
- NIST chose lattice problems as the foundation for FIPS 203 and FIPS 204 (August 2024).

## Entities

- [[bls12-381]]
- [[ceremony]]
- [[fri]]
- [[kzg]]
- [[lattice]]
- [[midnight]]
- [[nist]]
- [[plonk]]
- [[setty]]
- [[starks]]

## Dependencies

- [[ch02-the-structured-reference-string]] — the SRS is what a quantum computer would attack
- [[ch02-two-ways-to-build-a-stage]] — transparent setups have no trapdoor to extract

## Sources cited

- NIST IR 8547 (post-quantum deprecation roadmap, 2024)
- NIST FIPS 203, 204 (August 2024, lattice-based post-quantum standards)
- Nguyen, Setty, 2025 (Neo lattice-based folding scheme)

## Open questions

- When will cryptographically relevant quantum computers arrive? Nobody knows; the asymmetry of consequences favors caution for systems with 10+ year privacy horizons.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [none] (D) No contradictions with other chapters found.
- [P3] (E) The section does not mention that Grover's quadratic speedup applies to pre-image search, not collision resistance directly; collision resistance degrades as $2^{n/3}$ under BHT (not $2^{n/2}$), which is a material distinction for parameter selection.

## Links

- Up: [[02-building-the-stage]]
- Prev: [[ch02-universal-versus-circuit-specific-setups]]
- Next: [[ch02-bn254-s-eroding-security-margin]]
