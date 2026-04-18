---
title: "Trust Decomposition: Seven Weaker Assumptions"
slug: ch10-trust-decomposition-seven-weaker-assumptions
chapter: 10
chapter_title: "The Synthesis -- Three Paths, Not Two"
heading_level: 2
source_lines: [4469, 4530]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 2483
---

## Trust Decomposition: Seven Weaker Assumptions

Now we arrive at the heart of the matter.

Everything in this book has been building toward this section. The seven layers, the three paths, the proof core, the causal DAG -- all of it converges on a single observation, and it is the most important thing this book has to say.

A traditional financial system requires trusting a single institution. The bank holds your money, knows your balance, controls your transactions, and you trust that it will behave honestly. You trust *one entity* with *everything*.

Zero-knowledge proofs do not eliminate trust. They do something different. They *decompose* it. They shatter a single monolithic trust assumption into seven independent, weaker assumptions. And because the assumptions are independent, no single failure breaks the system. This is not trustlessness. It is something better: trust that is distributed, auditable, and replaceable.

Here are the seven assumptions, and each one is a thread you can pull:

**Layer 1**: At least one of N ceremony participants was honest (for trusted setups), or that hash functions are collision-resistant (for transparent setups). This is the trust in the stage itself -- that the mathematical parameters were generated fairly.

**Layer 2**: The circuit was correctly written and audited. The under-constrained circuit epidemic catalogued in Chapter 3 remains the dominant vulnerability class, and a bug here lets the prover prove false statements. This is the trust in the choreography: that the script describes the trick accurately.

**Layer 3**: The hardware running the prover does not leak the witness through side channels. Timing attacks on Zcash's Groth16 prover leaked transaction amounts with $R = 0.57$ correlation. Cache timing attacks on ZK-friendly hash functions (Poseidon, Reinforced Concrete) have been demonstrated in cloud environments. This is the trust in the backstage -- that no one can see behind the curtain through cracks in the wall.

**Layer 4**: The arithmetization correctly encodes the computation. If the translation from program to polynomial constraints is wrong, the proof system faithfully proves the wrong thing. This is the trust in the encoding -- that the mathematical puzzle accurately represents the trick.

**Layer 5**: The proof system is sound -- no efficient adversary can forge proofs. This depends on the Fiat-Shamir transform being correctly implemented (the Frozen Heart bug of 2022 affected three independent implementations simultaneously) and on the underlying interactive proof being sound. This is the trust in the seal -- that the certificate cannot be forged.

**Layer 6**: The mathematical hardness assumptions hold. Discrete logarithms are hard (or lattice problems are hard, or hash preimages are hard). These are conjectures, not theorems. Tower NFS improvements already reduced BN254's estimated security from ~128 bits to ~100 bits. This is the trust in mathematics itself -- the deepest assumption, and the one we have the least power to verify.

**Layer 7**: The governance structure will not override the cryptography. Most deployed ZK rollups are Stage 0 or Stage 1 on L2Beat's framework, meaning a multisig can override the proof system. The Beanstalk flash-loan governance attack ($182M, April 2022) and the Tornado Cash CREATE2 contract replacement (May 2023) demonstrate that governance can be exploited. This is the trust in the theater management -- that the people who run the venue will not rig the show.

### When Each Thread Snaps: Seven Failure Scenarios

The seven assumptions above are not hypothetical. Every one of them has failed, is failing, or will fail in a live system. Isaac Asimov once observed that the most exciting phrase in science is not "Eureka!" but "That's funny..." -- the moment when an assumption you did not know you were making turns out to be wrong. In zero-knowledge systems, "That's funny..." is the sound of money disappearing. Here is what each failure looks like in practice, what breaks, and -- critically -- what does *not* break.

**If Layer 1 fails (compromised setup):** An attacker who knows the toxic waste from a trusted setup ceremony can forge proofs of arbitrary statements. They can mint tokens from nothing, approve transactions that never happened, fabricate state transitions whole cloth. The terrifying property of this failure is its *invisibility*. A forged Groth16 proof is indistinguishable from a legitimate one -- both are 192 bytes, both pass the verifier, both look identical on-chain. No alarm fires. No anomaly appears in the logs. The counterfeiting is perfect by construction. This is why Zcash's Powers-of-Tau ceremony involved 87 independent participants across six continents -- the assumption is that at least one of them destroyed their toxic waste. If all 87 were compromised (through coercion, incompetence, or a coordinated state-level attack), the entire shielded pool would be silently forgeable. Note what does *not* break: the circuit logic (Layer 2) is still correct, the witness privacy (Layer 3) is still intact, the math (Layer 6) still holds. The stage was rigged, but the trick's choreography was genuine.

**If Layer 2 fails (buggy circuit):** The proof system faithfully proves a false statement. This is the most common failure mode in production, and the canonical example is Tornado Cash. A single missing constraint in Tornado Cash's withdrawal circuit allowed an attacker to generate valid proofs for withdrawals from deposits that never existed. The circuit was supposed to verify that a nullifier corresponded to a real deposit commitment in the Merkle tree. A missing range check meant the prover could satisfy the constraints with fabricated values. The proof was *valid* -- it passed the verifier -- because the verifier only checks that the proof matches the circuit, and the circuit was wrong. The Zcash "InternalH" bug (CVE-2019-7167, February 2019) is the same species: a missing check in the Sapling circuit would have allowed unlimited counterfeiting of shielded ZEC. Found by a Zcash engineer during routine review, it was quietly patched before exploitation. The gap between "found by an auditor" and "found by an attacker" was a matter of months. Circom's under-constrained circuit epidemic -- where developers use the `<--` assignment operator instead of the `<==` constraining operator -- produces the same failure at industrial scale. The proof system is not broken. The program is broken. The seal is perfect; the document it seals is a forgery.

**If Layer 3 fails (witness leakage):** The zero-knowledge property evaporates. The proof is still valid, and the computation is still correct, but the secret inputs are exposed. The system proves the truth and simultaneously reveals what it was supposed to hide. Timing side-channel attacks on Zcash's Groth16 prover demonstrated this concretely: by measuring how long proof generation took, an observer could infer the transaction amount with $R = 0.57$ correlation. The proof said "this transaction is valid" without revealing the amount -- but the *time it took to generate the proof* leaked the amount through a side channel. In cloud proving environments (AWS, GCP), cache-timing attacks on ZK-friendly hash functions like Poseidon and Reinforced Concrete are even more direct: a co-located VM can observe memory access patterns and reconstruct the witness. This is a privacy catastrophe but not an integrity catastrophe. The computations are still correct. The proofs are still sound. But the magician's secrets are visible through cracks in the dressing room wall.

**If Layer 4 fails (incorrect arithmetization):** The constraint system does not faithfully represent the computation it claims to encode. This is subtler than a Layer 2 bug because the *program* may be correct -- the error is in the *translation* from program to polynomial constraints. Consider a zkVM that claims to prove RISC-V execution. If the arithmetization incorrectly encodes the behavior of, say, the `slt` (set-less-than) instruction -- treating signed comparison as unsigned, or failing to handle the overflow edge case at INT_MIN -- then the zkVM produces valid proofs of executions that never happened. The program was correct. The proof system was sound. The encoding between them was wrong. This failure is especially dangerous in hand-rolled constraint systems (pre-zkVM era), where a developer manually translates each operation into R1CS or AIR constraints. SP1's formal verification of all 62 RISC-V opcodes against the Sail specification exists precisely to prevent this class of failure. The trust is not in the magician or the seal, but in the translator standing between them -- and translators make mistakes.

**If Layer 5 fails (broken proof system):** An attacker can forge proofs without knowing the witness. The Frozen Heart vulnerability (2022) is the textbook case. Three independent implementations of the Fiat-Shamir transform -- Bellman (Zcash), Gnark (ConsenSys), and an academic reference -- all made the same mistake: they failed to bind the public inputs to the transcript hash. An attacker could take a valid proof for one statement and re-use it for a different statement. The proof said "I know a witness for X" but could be replayed to claim "I know a witness for Y." All three implementations were broken simultaneously, because all three misunderstood the same subtle requirement of the Fiat-Shamir transform. This is a soundness catastrophe. The seal can be forged. Valid-looking proofs can be manufactured for false statements. Unlike a Layer 2 failure (where the circuit is wrong but the proof system is honest), a Layer 5 failure means the proof system itself is compromised. Every proof it has ever generated becomes suspect.

**If Layer 6 fails (broken hardness assumption):** The mathematical foundation dissolves. This has not happened catastrophically yet, but it has happened incrementally, and incrementally is frightening enough. Tower NFS improvements reduced BN254's estimated security from approximately 128 bits to approximately 100 bits -- not a break, but an erosion. The 2023 lattice basis reduction advances by Ducas and van Woerden tightened the known attacks on NTRU lattices, and while they did not break any deployed scheme, they moved the boundary closer. A full break of BN254's discrete logarithm problem would compromise every Groth16 proof ever generated on that curve: past, present, and future. Every wrapped STARK-to-SNARK proof on Ethereum would be forgeable. Every ZK rollup using BN254 verification would lose its security guarantee retroactively. Shor's algorithm achieves exactly this for all pairing-based and elliptic-curve cryptography, given a sufficiently large quantum computer. The question is not *whether* this assumption will weaken but *when* and *how fast*. This is the failure that the post-quantum folding path (Path Three) exists to survive.

**If Layer 7 fails (governance override):** The cryptography is irrelevant because the humans in charge simply bypass it. This is the most prosaic failure and arguably the most dangerous, because it requires no mathematical sophistication -- only social engineering, legal coercion, or economic incentive. The Beanstalk flash-loan governance attack ($182M, April 2022) demonstrated the economic version: an attacker borrowed enough governance tokens to pass a malicious proposal in a single transaction, draining the protocol's treasury. The cryptography was never touched. The proofs were never forged. The governance mechanism -- the human layer above the math -- was the attack surface. The Tornado Cash CREATE2 replacement (May 2023) demonstrated the supply-chain version: the deployer address used CREATE2 to replace the governance contract with a malicious one, granting the attacker control over all locked funds. Again, no cryptographic break was needed. Most deployed ZK rollups operate with upgrade multisigs that can push new verifier contracts, effectively overriding any proof system guarantee. If three of five multisig holders collude (or are coerced by a state actor), they can deploy a verifier that accepts all proofs, or no proofs, or only proofs from approved provers. The mathematical fortress has a human door, and the door has a human lock.

### The Cascade Structure

Not all failures are created equal, and not all are independent. The seven assumptions form their own internal DAG of failure propagation.

A Layer 6 failure cascades into Layer 5 (if the hardness assumption breaks, the proof system built on it is unsound) and Layer 1 (if discrete logs are easy, trusted setup toxic waste can be reconstructed). But it does *not* cascade into Layer 2 (the circuit logic is still correct), Layer 3 (the witness generation is still private against non-quantum adversaries), or Layer 4 (the arithmetization is still faithful). A quantum computer that breaks BN254 makes Groth16 proofs forgeable, but it does not introduce bugs into Circom circuits. The choreography is fine. The seal is broken.

A Layer 2 failure is *contained*. A buggy circuit produces provably wrong results, but the proof system is still sound (it just proves the wrong thing), the setup is still valid, the hardware does not leak, and the math still holds. This containment is precisely what makes Layer 2 failures survivable: fix the circuit, redeploy the verifier, and the system recovers. The Zcash InternalH bug was patched in a single release. The stage machinery was fine; only the script needed rewriting.

A Layer 7 failure is the most isolated and the most devastating. It requires no interaction with any other layer. A governance override does not break the math, corrupt the circuit, or leak the witness. It simply ignores all of them. This isolation means that Layer 7 cannot be fixed by improving any other layer. Better proof systems, stronger fields, more rigorous audits -- none of these matter if a three-of-five multisig can replace the verifier contract. The only defense is the same defense that human institutions have always relied on: constitutional constraints, time-locks, social consensus, and the slow, unglamorous work of governance design.

The cascade structure reveals a counterintuitive truth about the seven-layer model. The *deepest* failures (Layer 6: math breaks) are the most catastrophic in scope but the least likely in practice. The *shallowest* failures (Layer 2: buggy circuit, Layer 7: governance override) are the most common in practice but the most recoverable. The threat landscape is inverted: the risks you encounter most often are the risks you can fix most easily. This inversion is what makes the trust decomposition genuinely useful. A monolithic trust model (trust the bank) gives you one failure mode: total. A decomposed trust model gives you seven failure modes, most of which are partial and recoverable. The system degrades gracefully, and graceful degradation is the definition of resilient engineering.

Each of these is independently falsifiable, independently auditable, and independently improvable. Breaking one does not necessarily break the others (though some failures cascade -- a quantum computer breaks Layers 1, 5, and 6 simultaneously for pairing-based systems). This decomposition is the genuine value proposition of zero-knowledge proofs: not trustlessness, but trust minimization through distribution.

Remember the bank from Chapter 1? The institution that holds your money, knows your balance, and controls your transactions? With zero-knowledge proofs, you no longer trust one bank with everything. You trust that at least one ceremony participant was honest. You trust that the circuit was correctly written. You trust that the hardware does not leak. You trust that the math is hard. You trust that the governance will not go rogue. Seven assumptions instead of one. Each weaker. Each testable. Each replaceable.

That is not a marketing slogan. It is a structural transformation.


## Summary

Zero-knowledge proofs do not eliminate trust; they decompose a single monolithic trust assumption into seven independent, weaker, and individually auditable assumptions mapped to each layer. The section catalogs every assumption, a concrete failure scenario with real exploits (Tornado Cash, Zcash CVE-2019-7167, Frozen Heart, Beanstalk, Tower NFS), and the cascade structure explaining which failures propagate across layers and which are contained. The central conclusion is that the threat landscape is inverted: the deepest failures (Layer 6 math) are most catastrophic in scope but least likely; the shallowest (Layer 2 bugs, Layer 7 governance) are most common but most recoverable.

## Key claims

- Layer 1 (setup): ≥1 of N ceremony participants was honest, or hash functions are collision-resistant.
- Layer 2 (circuit): circuit was correctly written and audited — under-constrained circuits are the dominant production vulnerability class.
- Layer 3 (witness): hardware does not leak witness through side channels; timing attacks on Zcash's Groth16 prover leaked transaction amounts with R = 0.57 correlation.
- Layer 4 (arithmetization): translation from program to polynomial constraints is faithful.
- Layer 5 (proof system): Fiat-Shamir is correctly implemented — the Frozen Heart bug (2022) broke three independent implementations (Bellman, Gnark, academic reference) simultaneously.
- Layer 6 (hardness): discrete logs / lattice problems / hash preimages are hard — Tower NFS reduced BN254 security from ~128 bits to ~100 bits.
- Layer 7 (governance): the multisig or governance mechanism will not override the cryptography — Beanstalk flash-loan attack ($182M, April 2022); Tornado Cash CREATE2 replacement (May 2023).
- A Layer 6 failure cascades into Layers 5 and 1 for pairing-based systems but does not corrupt Layers 2, 3, or 4.
- A Layer 2 failure is contained: fix the circuit, redeploy, recover — Zcash InternalH (CVE-2019-7167) patched in a single release.
- A Layer 7 failure is maximally isolated (requires no interaction with any other layer) and cannot be fixed by improving cryptography alone.
- Most deployed ZK rollups are Stage 0 or Stage 1 on L2Beat's framework — a multisig can override the verifier.

## Entities

- [[beanstalk]]
- [[bn254]]
- [[ceremony]]
- [[fiat-shamir]]
- [[folding]]
- [[fri]]
- [[groth16]]
- [[l2beat]]
- [[lattice]]
- [[poseidon]]
- [[tornado cash]]
- [[zcash]]

## Dependencies

- [[ch02-the-quantum-shelf-life]] — BN254 erosion from ~128 to ~100 bits via Tower NFS
- [[ch04-side-channel-attacks-when-the-walls-leak]] — Layer 3 witness leakage and Zcash timing attack detail
- [[ch08-governance-the-achilles-heel]] — Layer 7 governance failure context
- [[ch08-when-the-transcript-lies-fiat-shamir-vulnerabilities]] — Frozen Heart / Fiat-Shamir failure mode
- [[ch03-under-constrained-circuits-the-dominant-failure-mode]] — Layer 2 Circom under-constraint bugs

## Sources cited

- Zcash CVE-2019-7167 "InternalH" bug — February 2019
- Frozen Heart vulnerability — 2022 (Bellman, Gnark, academic reference)
- Beanstalk flash-loan governance attack — $182M, April 2022
- Tornado Cash CREATE2 contract replacement — May 2023
- Tower NFS — BN254 security reduction to ~100 bits

## Open questions

None flagged by this section.

## Improvement notes

- [P0] D Frozen Heart count contradicts ch08: this section says the bug "affected three independent implementations simultaneously" and Key claims lists "Bellman, Gnark, academic reference." But ch08-when-the-transcript-lies (the canonical treatment) says six implementations across three proof systems (Dusk Network PLONK, Iden3/SnarkJS Groth16, ConsenSys/gnark PLONK, ING Bank zkrp Bulletproofs, SECBIT Labs ckb-zkp Groth16, Adjoint Inc. Bulletproofs). The number is wrong (three vs. six) and the named implementations don't match — "Bellman" is not listed in ch08's six. Must be corrected to six implementations, and the three named instances replaced with the canonical ch08 list.
- [P1] A The Layer 2 Tornado Cash example conflates the circuit-bug narrative with the 2022 governance exploit. The actual Tornado Cash governance attack ($~$1M TORN, April 2023) was a governance takeover, not a circuit vulnerability. A missing-constraint circuit exploit in Tornado Cash would be a separate event. The text should identify the specific CVE or audit finding it is referencing, or use a cleaner example (e.g., the Zcash InternalH bug, already mentioned, is a better standalone Layer 2 illustration).
- [P2] E The cascade structure section notes that a Layer 6 failure "does not cascade into Layer 2, 3, or 4," but does not explain why a quantum break of discrete logs would leave the circuit logic (Layer 2) or arithmetization (Layer 4) intact even though the proof system (Layer 5) using those layers becomes unsound. The reasoning is correct but the isolation argument would benefit from one sentence of elaboration.

## Links

- Up: [[10-the-synthesis-three-paths-not-two]]
- Prev: [[ch10-the-causal-web-why-it-is-a-dag-not-a-stack]]
- Next: [[ch10-trustless-versus-trust-minimized]]
