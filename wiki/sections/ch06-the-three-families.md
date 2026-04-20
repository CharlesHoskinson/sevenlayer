---
title: "The Three Families"
slug: ch06-the-three-families
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2458, 2517]
source_commit: 6e757843ed29aa50ce4558719452a86510ed0d20
status: finalized
word_count: 1859
---

## The Three Families

Every zero-knowledge proof system in production today belongs to one of three families. They differ in what they require before you start, how large a proof they produce, and what mathematical assumptions keep them secure. Choosing among them is not a philosophical exercise. It is an engineering decision with direct consequences for cost, speed, security, and quantum resistance.

### Groth16: The Gold Standard for Size

In 2016, Jens Groth published a proof system that produces the smallest possible proofs: three elliptic curve group elements, totaling 192 bytes (two G1 points and one G2 point on BLS12-381). Verification requires three pairing computations (the Ethereum EVM implementation batches this as four pairings via EIP-1108 [Ethereum Improvement Proposal 1108, "Reduce alt_bn128 precompile gas costs," https://eips.ethereum.org/EIPS/eip-1108]) -- about 250,000 gas on Ethereum. Nearly a decade later, nothing comes close to this combination of proof size and verification cost. Groth16 remains the final wrapping target for almost every production ZK system that posts proofs on-chain.

The catch is severe. Groth16 requires a per-circuit trusted setup ceremony. You cannot change the circuit without re-running the ceremony. The ceremony produces a structured reference string (SRS) that contains "toxic waste" -- secret randomness that, if any single participant retains, would allow them to forge proofs for that circuit forever. The 1-of-N trust model (discussed in Chapter 2) mitigates this, but the ceremony is expensive, inflexible, and not quantum-resistant.

Put differently: Groth16 seals the smallest possible certificate -- just 192 bytes, three elliptic curve points. But you need a custom seal for every circuit you want to prove, and manufacturing that seal requires a ceremony involving thousands of people, any one of whom could secretly keep a master key to forge future certificates. If a quantum computer ever appears, every seal ever manufactured becomes useless.

Despite these limitations, Groth16's on-chain economics are so favorable that it persists as the outer shell of nearly every hybrid proving pipeline. The inner proof system might be a STARK, a folding scheme, or something else entirely. But the last step -- the proof that actually touches the blockchain -- is almost always Groth16 over the BN254 curve, because Ethereum's EVM has precompiled contracts that make BN254 pairings cheap. BN254 was chosen for Ethereum for EVM compatibility and its low precompile cost, not as the strongest available security choice; its ~100-bit post-Tower-NFS security is below the 128-bit standard for new deployments.

BN254's security is commonly cited as approximately 100 bits after Tower Number Field Sieve advances [Kim and Barbulescu, "Extended Tower Number Field Sieve," CRYPTO 2016]; some models place it slightly higher (100--110 bits depending on parameters). This is below the 128-bit standard for new deployments, which is why BN254 persists for on-chain verification cost reasons rather than security reasons.

### PLONK: The Universal Workhorse

In 2019, Gabizon, Williamson, and Ciobotaru published PLONK, which solved Groth16's biggest practical problem: the per-circuit setup. PLONK uses a universal structured reference string. Run one ceremony, and you can use the resulting SRS for any circuit up to a fixed size. Change your program? No new ceremony needed. Just compile a new circuit against the same SRS.

PLONK introduced "PLONKish" arithmetization -- a system of gate constraints and copy constraints glued together by a permutation argument. This turned out to be very flexible. Custom gates allow specialized operations (elliptic curve arithmetic, hash functions, range checks) to be encoded efficiently. Lookup tables (via Plookup and its successors) let the prover reference pre-computed values instead of re-deriving them from scratch. The result was a proof system that could be tuned for specific workloads while retaining universality.

Halo 2, developed by the Electric Coin Company for Zcash and later adopted by other projects, extended PLONK with custom gates, lookup tables, and a flexible backend that supports multiple commitment schemes. Note: the original Halo paper (2019) used IPA commitments with no trusted setup. Halo 2, as deployed by Zcash for Orchard and adopted by Midnight, uses KZG commitments requiring a ceremony -- a different trust model despite the shared name. When instantiated with IPA instead of KZG, Halo 2 eliminates the trusted setup entirely, and the proof size grows from constant to logarithmic, but verification becomes somewhat more expensive.

PLONK and its variants (UltraPlonk, TurboPlonk, Halo 2) are the workhorses of production ZK today. They sit at the center of a design space between Groth16's extreme compactness and STARKs' extreme transparency. Most ZK applications that need flexibility -- circuits that change frequently, applications where a per-circuit ceremony is impractical -- choose a PLONK-family system.

Proof sizes across PLONK variants span a practical range: a base PLONK proof with KZG is a few hundred bytes (roughly 400--800 bytes, dominated by the ~48-byte KZG opening proofs multiplied by the number of query points); UltraPlonk with custom gates and Plookup adds modest overhead, reaching 1--3 KB; Halo 2 with IPA commitments produces logarithmic-size proofs that grow with circuit depth, typically 5--20 KB for circuits in the million-gate range. These are all substantially larger than Groth16's 192 bytes but far smaller than STARK proofs at hundreds of kilobytes.

### STARKs: The Transparent Path

STARKs (Scalable Transparent ARguments of Knowledge), introduced by Ben-Sasson, Bentov, Horesh, and Riabzev in 2018, took a radically different approach. No trusted setup at all. No pairings. No elliptic curves. The only cryptographic assumption is the existence of collision-resistant hash functions -- a primitive that is believed to be quantum-resistant.

The core idea is clean. STARKs prove statements about Algebraic Intermediate Representations (AIR): polynomial constraints on an execution trace, where each row represents one time step and the constraints enforce that consecutive rows are consistent. The key mechanism is the FRI protocol (Fast Reed-Solomon Interactive Oracle Proof), which verifies that a committed function is close to a low-degree polynomial. If the computation was performed correctly, the trace satisfies all constraints, and the polynomial is low-degree. If the prover cheated, the polynomial's degree blows up, and FRI catches the inconsistency with overwhelming probability.

The cost of this transparency is proof size. A STARK proof is hundreds of kilobytes -- roughly 1,000 times larger than a Groth16 proof. On Ethereum, where every byte costs gas, this difference translates directly into money. But STARKs offer something the other families cannot: a path to post-quantum security, and a proving architecture that scales almost linearly with computation size.

So the three families seal certificates with different properties. Groth16 seals the smallest possible certificate -- just 192 bytes -- but requires a custom seal for every circuit. PLONK seals a slightly larger certificate but can use the same seal for any trick, eliminating the per-circuit ceremony. STARKs seal certificates without any secret ingredient at all -- no ceremony, no toxic waste, no trust assumptions beyond collision-resistant hashing -- but the certificates are much bulkier: hundreds of kilobytes instead of hundreds of bytes.

### Three Envelopes: An Intuition

The technical differences between the three families are real, but their *character* is better grasped through analogy. Each family seals a certificate. Think of each certificate as a letter placed inside an envelope. The families differ not in what the letter says but in how the envelope is made, what it costs, and what it reveals about the process of sealing.

Groth16 is the smallest possible envelope. Three numbers -- two points on a curve and one more -- encode an entire computation. A circuit proving that an Ethereum block was executed correctly might involve billions of constraints and a witness consuming gigabytes of memory; the Groth16 proof is 192 bytes. The proof either satisfies the verification equation or it does not. There is no room for a "pretty good" forgery.

The cost of this extreme compression is inflexibility. The envelope form must be custom-designed for each circuit. You cannot take a mold built for one circuit and use it for another. In Groth16 terms, this means a new trusted setup ceremony for every circuit. Change the computation, and you need a new ceremony. This is why Groth16 is almost never used as the primary proof system. It is used as the *final wrapper* -- the outermost envelope -- because you only need one ceremony for the wrapping circuit, and that circuit does not change.

PLONK is the universal envelope. One envelope fits all letters. The envelope factory runs a single setup ceremony and produces a structured reference string that works for any circuit up to a certain size. Write a new smart contract? Same envelope. Update your program logic? Same envelope. The setup cost is paid once. After that, any computation that fits within the size bound can be sealed without a new ceremony.

The analogy is a standardized shipping container. Before containerization, every type of cargo required its own packaging. A container does not care whether it holds televisions, bananas, or machine parts. It is a universal interface between the thing being shipped and the infrastructure that moves it. PLONK's universal SRS is the container. The circuit is the cargo. The verifier handles every circuit the same way, because they all arrive in the same container.

The proofs are larger than Groth16's (a few hundred bytes to a few kilobytes depending on variant: ~400--800 bytes for base KZG-PLONK, 1--3 KB for UltraPlonk, 5--20 KB for IPA-Halo 2 at million-gate depth) and verification is slightly more expensive. These are the costs of universality.

STARKs are glass envelopes. Nothing is hidden in the construction. There is no trusted setup, no toxic waste, no secret randomness that could compromise the system if leaked. The envelope-making process is entirely public. The cryptographic assumption is minimal: collision-resistant hash functions exist.

The trade: glass envelopes are bulkier than paper ones. A STARK proof is hundreds of kilobytes -- roughly a thousand times larger than a Groth16 proof. On a blockchain where every byte costs gas, this bulk translates directly into dollars. But glass has a property that paper lacks: it does not shatter under quantum impact. Hash-based cryptography is believed to resist quantum attacks. Paper envelopes -- those built on elliptic curve assumptions -- will dissolve the moment a sufficiently powerful quantum computer runs Shor's algorithm. Glass envelopes will still be standing.

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

_All P0/P1/P2/P3 findings resolved in Phase 3 revisions (2026-04-18 through 2026-04-20)._

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-sealing-the-certificate]]
- Next: [[ch06-the-hybrid-pipeline]]
