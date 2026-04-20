---
title: "The Three Families"
slug: ch06-the-three-families
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2449, 2506]
source_commit: 199f27399ce5c5a87123a37bf3c457a226778185
status: reviewed
word_count: 1859
---

## The Three Families

Every zero-knowledge proof system in production today belongs to one of three families. They differ in what they require before you start, how large a proof they produce, and what mathematical assumptions keep them secure. Choosing among them is not a philosophical exercise. It is an engineering decision with direct consequences for cost, speed, security, and quantum resistance.

### Groth16: The Gold Standard for Size

In 2016, Jens Groth published a proof system that produces the smallest possible proofs: three elliptic curve group elements, totaling 192 bytes (two G1 points and one G2 point on BLS12-381). Verification requires three pairing computations (the Ethereum EVM implementation batches this as four pairings via EIP-1108) -- about 250,000 gas on Ethereum. Nearly a decade later, nothing comes close to this combination of proof size and verification cost. Groth16 remains the final wrapping target for almost every production ZK system that posts proofs on-chain.

The catch is severe. Groth16 requires a per-circuit trusted setup ceremony. You cannot change the circuit without re-running the ceremony. The ceremony produces a structured reference string (SRS) that contains "toxic waste" -- secret randomness that, if any single participant retains, would allow them to forge proofs for that circuit forever. The 1-of-N trust model (discussed in Chapter 2) mitigates this, but the ceremony is expensive, inflexible, and not quantum-resistant.

Put differently: Groth16 seals the smallest possible certificate -- just 192 bytes, three elliptic curve points. But you need a custom seal for every circuit you want to prove, and manufacturing that seal requires a ceremony involving thousands of people, any one of whom could secretly keep a master key to forge future certificates. If a quantum computer ever appears, every seal ever manufactured becomes useless.

Despite these limitations, Groth16's on-chain economics are so favorable that it persists as the outer shell of nearly every hybrid proving pipeline. The inner proof system might be a STARK, a folding scheme, or something else entirely. But the last step -- the proof that actually touches the blockchain -- is almost always Groth16 over the BN254 curve, because Ethereum's EVM has precompiled contracts that make BN254 pairings cheap.

### PLONK: The Universal Workhorse

In 2019, Gabizon, Williamson, and Ciobotaru published PLONK, which solved Groth16's biggest practical problem: the per-circuit setup. PLONK uses a universal structured reference string. Run one ceremony, and you can use the resulting SRS for any circuit up to a fixed size. Change your program? No new ceremony needed. Just compile a new circuit against the same SRS.

PLONK introduced "PLONKish" arithmetization -- a system of gate constraints and copy constraints glued together by a permutation argument. This turned out to be very flexible. Custom gates allow specialized operations (elliptic curve arithmetic, hash functions, range checks) to be encoded efficiently. Lookup tables (via Plookup and its successors) let the prover reference pre-computed values instead of re-deriving them from scratch. The result was a proof system that could be tuned for specific workloads while retaining universality.

Halo 2, developed by the Electric Coin Company for Zcash and later adopted by other projects, extended PLONK with custom gates, lookup tables, and a flexible backend that supports multiple commitment schemes. Note: the original Halo paper (2019) used IPA commitments with no trusted setup. Halo 2, as deployed by Zcash for Orchard and adopted by Midnight, uses KZG commitments requiring a ceremony -- a different trust model despite the shared name. When instantiated with IPA instead of KZG, Halo 2 eliminates the trusted setup entirely, and the proof size grows from constant to logarithmic, but verification becomes somewhat more expensive.

PLONK and its variants (UltraPlonk, TurboPlonk, Halo 2) are the workhorses of production ZK today. They sit at the center of a design space between Groth16's extreme compactness and STARKs' extreme transparency. Most ZK applications that need flexibility -- circuits that change frequently, applications where a per-circuit ceremony is impractical -- choose a PLONK-family system.

### STARKs: The Transparent Path

STARKs (Scalable Transparent ARguments of Knowledge), introduced by Ben-Sasson, Bentov, Horesh, and Riabzev in 2018, took a radically different approach. No trusted setup at all. No pairings. No elliptic curves. The only cryptographic assumption is the existence of collision-resistant hash functions -- a primitive that is believed to be quantum-resistant.

The core idea is clean. STARKs prove statements about Algebraic Intermediate Representations (AIR): polynomial constraints on an execution trace, where each row represents one time step and the constraints enforce that consecutive rows are consistent. The key mechanism is the FRI protocol (Fast Reed-Solomon Interactive Oracle Proof), which verifies that a committed function is close to a low-degree polynomial. If the computation was performed correctly, the trace satisfies all constraints, and the polynomial is low-degree. If the prover cheated, the polynomial's degree blows up, and FRI catches the inconsistency with overwhelming probability.

The cost of this transparency is proof size. A STARK proof is hundreds of kilobytes -- roughly 1,000 times larger than a Groth16 proof. On Ethereum, where every byte costs gas, this difference translates directly into money. But STARKs offer something the other families cannot: a path to post-quantum security, and a proving architecture that scales almost linearly with computation size.

So the three families seal certificates with different properties. Groth16 seals the smallest possible certificate -- just 192 bytes -- but requires a custom seal for every circuit. PLONK seals a slightly larger certificate but can use the same seal for any trick, eliminating the per-circuit ceremony. STARKs seal certificates without any secret ingredient at all -- no ceremony, no toxic waste, no trust assumptions beyond collision-resistant hashing -- but the certificates are much bulkier: hundreds of kilobytes instead of hundreds of bytes.

### Three Envelopes: An Intuition

The technical differences between the three families are real, but their *character* is better grasped through analogy. Each family seals a certificate. Think of each certificate as a letter placed inside an envelope. The families differ not in what the letter says but in how the envelope is made, what it costs, and what it reveals about the process of sealing.

**Groth16 is the smallest possible envelope.** Three numbers -- two points on a curve and one more -- encode an entire computation. Consider the compression ratio. A circuit proving that an Ethereum block was executed correctly might involve billions of constraints, millions of intermediate values, a witness consuming gigabytes of memory. The Groth16 proof of that computation is 192 bytes. Three elliptic curve elements. It is as though someone handed you a novel -- a thick, sprawling saga with hundreds of characters and interlocking subplots -- and you compressed it into a haiku. Seventeen syllables. And yet a reader who knows the rules of haiku composition can verify that those seventeen syllables faithfully capture the plot. Not a summary. Not an approximation. A mathematically exact encoding from which any deviation would be detectable. The haiku either satisfies the verification equation or it does not. There is no room for a "pretty good" forgery.

The cost of this extreme compression is inflexibility. The haiku form must be custom-designed for each novel. You cannot take a haiku mold built for *War and Peace* and use it to compress *Moby Dick*. In Groth16 terms, this means a new trusted setup ceremony for every circuit. The ceremony produces the specific algebraic structure -- the structured reference string -- that makes the compression possible for that particular computation. Change the computation, and you need a new ceremony. This is why Groth16 is almost never used as the primary proof system. It is used as the *final wrapper* -- the outermost envelope -- because you only need one ceremony for the wrapping circuit, and that circuit does not change.

**PLONK is the universal envelope.** One envelope fits all letters. The envelope factory runs a single setup ceremony and produces a structured reference string that works for any circuit up to a certain size. Write a new smart contract? Same envelope. Update your program logic? Same envelope. The setup cost is paid once. After that, any computation that fits within the size bound can be sealed without a new ceremony.

The analogy is a standardized shipping container. Before containerization, every type of cargo required its own packaging, its own crane, its own dockworker expertise. A container does not care whether it holds televisions, bananas, or machine parts. It is a universal interface between the thing being shipped and the infrastructure that moves it. PLONK's universal SRS is the container. The circuit -- whatever it computes -- is the cargo. The infrastructure -- the verifier, the blockchain, the precompiled contract -- handles every circuit the same way, because they all arrive in the same container.

The proofs are slightly larger than Groth16's (a few hundred bytes to a few kilobytes, depending on the variant), and verification is slightly more expensive. These are the costs of universality. You pay a modest premium for the ability to change your message without manufacturing a new envelope. For most applications, this tradeoff is overwhelmingly favorable, which is why PLONK-family systems are the workhorses of production ZK.

**STARKs are glass envelopes.** Nothing is hidden in the construction. There is no trusted setup, no toxic waste, no secret randomness that could compromise the system if leaked. The envelope-making process is entirely public. Anyone can inspect it, audit it, reproduce it. The cryptographic assumption is minimal: collision-resistant hash functions exist. That is all.

The trade: glass envelopes are bulkier than paper ones. A STARK proof is hundreds of kilobytes -- roughly a thousand times larger than a Groth16 proof. On a blockchain where every byte costs gas, this bulk translates directly into dollars. Glass is heavier than paper. You pay more to ship it. But glass has a property that paper lacks: you can see through it. The transparency is not a metaphor. It is a literal statement about the trust model. There is no ceremony to trust, no participant to worry about, no toxic waste to dispose of. The security rests on the hardest-to-break foundation in cryptography: the belief that hash functions do not have secret backdoors.

And glass has another property that matters more each year: it does not shatter under quantum impact. Hash-based cryptography is believed to resist quantum attacks. Paper envelopes -- those built on elliptic curve assumptions -- will dissolve the moment a sufficiently powerful quantum computer runs Shor's algorithm. Glass envelopes will still be standing. The bulk that seems like a disadvantage today may prove to be the price of survival.

But notice: the three envelope types are not competing products on a shelf. They are components in a supply chain. The glass envelope (STARK) is manufactured first, because it is transparent and quantum-resistant. Then the contents are transferred into a paper envelope (Groth16) for shipping, because paper is lighter and the postal system (the blockchain) charges by weight. The glass envelope never reaches the destination. It does its job backstage -- proving the computation with full transparency -- and then the result is repackaged into the smallest, cheapest container for the final mile. Understanding this supply chain is what the next section is about.

---


## Summary

Every production ZK proof system belongs to one of three families: Groth16 (192-byte proofs, per-circuit trusted setup), PLONK (universal setup, slightly larger proofs), and STARKs (no setup, hash-based security, ~100x larger proofs). In practice these are not competitors but pipeline stages -- STARKs prove computation with transparency, Groth16 wraps the result for cheap on-chain verification.

## Key claims

- Groth16 produces the smallest proofs: 192 bytes (two G1 + one G2 on BLS12-381), ~250,000 gas to verify via EIP-1108.
- Groth16 requires a per-circuit trusted setup; toxic waste in the SRS enables forgery if any participant retains it.
- PLONK (Gabizon, Williamson, Ciobotaru, 2019) introduced a universal SRS: one ceremony covers all circuits up to a fixed size.
- Halo 2, as deployed by Midnight and Zcash Orchard, uses KZG commitments (trusted setup) despite the original Halo paper using IPA (no setup).
- STARKs rely only on collision-resistant hash functions -- no elliptic curves, no trusted setup, plausibly post-quantum.
- STARK proofs are ~1,000x larger than Groth16 proofs; this bulk trades for transparency and quantum resistance.
- Production systems use STARKs inside and Groth16 outside -- each contributing what it does best.

## Entities

- [[groth16]]
- [[plonk]]
- [[starks]]
- [[fri]]
- [[kzg]]
- [[ipa]]
- [[halo2]]
- [[ceremony]]
- [[bn254]]
- [[bls12-381]]
- [[zcash]]
- [[eip]]
- [[gabizon]]

## Dependencies

- [[ch06-sealing-the-certificate]] — introduces the certificate concept this section enumerates
- [[ch02-universal-versus-circuit-specific-setups]] — 1-of-N trust model for ceremonies
- [[ch06-the-hybrid-pipeline]] — next section explains how the three families compose in production
- [[ch07-four-families-of-commitment-schemes]] — commitment schemes (KZG, FRI, IPA) underlying each family

## Sources cited

- Groth, "On the Size of Pairing-Based Non-interactive Arguments," EUROCRYPT 2016.
- Gabizon, Williamson, Ciobotaru, "PLONK: Permutations over Lagrange-bases for Oecumenical Noninteractive arguments of Knowledge," ePrint 2019/953.
- Ben-Sasson, Bentov, Horesh, Riabzev, "Scalable, transparent, and post-quantum secure computational integrity," ePrint 2018/046.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P2] (C) Excessive bolding on the "Three Envelopes" subsection headers ("Groth16 is the smallest possible envelope", "PLONK is the universal envelope", "STARKs are glass envelopes") — the bold labels are redundant with the prose that follows and create a numbered-proof-steps feel
- [P2] (C) "It is worth spelling out" — AI smell in hybrid pipeline paragraph
- [P2] (A) BN254 security described as "~100 bits after Tower NFS advances" — consensus is 100–110 bits depending on the model; the claim is defensible but should cite Kim-Barbulescu (2016) or equivalent
- [P3] (B) No citation for the EVM pairing cost of "250,000 gas via EIP-1108"; should cite EIP-1108 directly
- [P3] (E) The envelope analogy is extended over three long paragraphs; it crowds out technical comparison of prover complexity and concrete proof-size numbers for PLONK variants (a few hundred bytes to a few KB is mentioned but not broken down by variant)

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-sealing-the-certificate]]
- Next: [[ch06-the-hybrid-pipeline]]
