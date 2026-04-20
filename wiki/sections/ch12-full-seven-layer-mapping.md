---
title: "Full Seven-Layer Mapping"
slug: ch12-full-seven-layer-mapping
chapter: 12
chapter_title: "Midnight -- The Privacy Theater"
heading_level: 2
source_lines: [4810, 4901]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 2897
---

## Full Seven-Layer Mapping

### Layer 1: BLS12-381 and the Trusted Ceremony

The book's Layer 1 asks: trusted or transparent? Midnight answers: **trusted, with a universal SRS**.

Midnight uses the BLS12-381 elliptic curve with a PLONK-family proof system (Halo 2). The Developer Guide's architecture diagram (p.8) shows a dedicated `midnight-trusted-setup` repository for running a Powers-of-Tau ceremony. The SRS is universal -- one ceremony serves all circuits -- but the compiler generates per-circuit proving and verifier keys derived from that SRS. For a simple counter contract, the compiler produces an `increment.prover` key (13.7 KB) and an `increment.verifier` key (1.3 KB).

Midnight's cryptographic history reveals pragmatic trade-offs that echo the theme from Chapter 2. The system originally used Pluto-Eris curves for recursive proof composition but switched back to BLS12-381 for mainnet, citing faster proof generation, wider ecosystem compatibility, and support for higher transaction volumes. Theoretical optimality yielded to engineering reality -- a pattern we have seen repeatedly throughout this book.

**Post-quantum implication**: BLS12-381 provides approximately 128-bit classical security but zero post-quantum security. Shor's algorithm breaks the discrete logarithm and pairing assumptions simultaneously. The stage is strong today. Its quantum shelf life is finite.

### Layer 2: Compact as Fourth-Philosophy DSL

The three-philosophy taxonomy from earlier chapters -- EVM-Compatible, ZK-Native ISA, General-Purpose ISA -- does not accommodate Compact. Compact represents a **fourth philosophy**: the application-specific DSL.

Compact does not prove a processor. It compiles a domain-specific smart contract language directly to chain-specific ZKIR, with the compiler enforcing application-level invariants that no ISA-level approach can express. Its closest relatives are Leo (Aleo) and Mina's o1js.

The critical differentiator is **disclosure analysis**. The Compact compiler includes a `track-witness-data` analysis pass that traces witness values through all program paths and rejects any program where private data might reach public surfaces without explicit `disclose()` calls. This is a hard compile-time error, not a warning. The Developer Guide documents that a first attempt at private voting was rejected with 11 disclosure errors, each tracing the path from witness to ledger operation.

No other ZK language prevents accidental privacy leaks at compile time. In Circom, Noir, and Cairo, a disclosure mistake produces a privacy leak, not a compiler error. Compact eliminates an entire vulnerability class -- accidental disclosure -- at the language level. The stage manager locks the doors to prevent accidental reveals. The magician must explicitly ask for the key.

### Layer 3: The disclose() Boundary

Witnesses in Midnight are arbitrary JavaScript functions that run off-chain. The `disclose()` operator is the sole gateway from the witness world to the circuit world -- the single controlled opening in the curtain between backstage and audience.

Every ZKIR circuit has two transcript channels: the `publicTranscript` (ledger operations visible to the verifier) and `privateTranscriptOutputs` (witness values visible only to the prover). Without `disclose()`, witness values remain entirely invisible to the circuit and the chain. The ZKIR checker enforces transcript integrity with specific diagnostic error messages -- tampering with either transcript causes immediate rejection.

What does this boundary feel like to the developer who must work inside it every day? Consider a programmer writing a private voting contract. She writes her witness function in TypeScript -- ordinary, familiar, unexotic code that fetches voter eligibility from a local database and computes a ballot. Every variable in that function is invisible to the chain by default. She could write a hundred lines of witness logic, and none of it would leave her machine. Then she reaches the moment of commitment: she needs the circuit to know which candidate received the vote, without revealing who cast it. She writes `disclose(candidateId)`. That single call is the seam in the curtain, the controlled opening where one piece of information -- and only that piece -- crosses from the private rehearsal room into the public theater. The compiler has already analyzed every path through her code; if she accidentally wrote `disclose(voterId)` three functions earlier, the build would have failed with a traced error showing exactly how the private value reached the public surface. The developer experience is not one of navigating cryptographic abstractions. It is one of writing normal code inside a system that has opinions -- strong, enforced, non-negotiable opinions -- about what leaves the room. Asimov imagined robots governed by laws they could not violate. The Compact developer works inside a compiler governed by disclosure laws it will not bend. The fiction writer's dream of the incorruptible guardian is, in this narrow domain, an engineering reality.

The theater analogy sharpens here. In a well-designed theater, the lighting grid is the real enforcer of what the audience sees. A spotlight operator who accidentally swings a beam toward the wings will reveal the stagehands, the props not yet in play, the illusion's scaffolding. Midnight's disclosure analysis is the lighting grid: it does not merely suggest where the light should fall -- it physically prevents the spots from swinging toward the wings. The developer sets the cues. The compiler locks the grid. And when the show runs, only what was meant to be seen is seen.

**Side-channel gap**: None of the five reference documents address timing attacks, cache attacks, or metadata leakage through the indexer's GraphQL API. Proof generation dominates transaction time (~18-20 seconds), providing natural but unintentional timing padding. The curtain is thick, but no one has tested whether light leaks through the seams.

The specifics matter. Within the 18-20 second proof generation window, the Poseidon hashing operations are the most likely timing leak -- as Chapter 4 documented, Poseidon's S-box lookups create secret-dependent cache access patterns. If the proof server runs on shared hardware (a cloud VM, a shared workstation), an attacker on the same machine could observe which cache lines the Poseidon computation evicts and reconstruct information about the hashed witness values.

The indexer presents a different channel. Before generating a proof, the SDK queries the indexer's GraphQL API for current ledger state -- contract balances, UTXO sets, Merkle roots. An observer monitoring the indexer's traffic sees *which contracts* a user is querying and *when*. If the observer also monitors the blockchain's mempool, the correlation between "query at time T" and "transaction submitted at time T+20 seconds" reveals which contract the user is interacting with, even though the proof itself reveals nothing.

Network-level metadata is a third channel. The timing of transaction submission -- precisely 18-20 seconds after the proof server started -- is itself a signal. An observer who sees a burst of network activity followed by a 20-second pause followed by a transaction submission can reasonably infer that a ZK proof was generated. The pattern is distinctive enough to fingerprint.

A complete privacy audit would need to cover: constant-time proof generation (are all code paths independent of witness values?), indexer query privacy (is the indexer connection encrypted and anonymized?), network timing analysis (does the submission pattern leak proof generation activity?), and memory access patterns (are Poseidon and Jubjub implementations resistant to cache-timing attacks?). None of these are addressed in Midnight's current documentation. The theater controls its spotlights. The sound of the machinery remains audible.

### Layer 4: ZKIR as High-Level Constraint IR

Midnight's ZKIR is a typed instruction-level intermediate representation with 24 base instructions organized into 8 categories: arithmetic (`add`, `mul`, `neg`), constraints (`assert`, `constrain_eq`, `constrain_bits`, `constrain_to_boolean`), comparison (`test_eq`, `less_than`), control flow (`cond_select`, `copy`), type encoding, cryptographic operations (targeting the Jubjub curve embedded in BLS12-381), I/O, and division.

ZKIR sits above the mathematical constraint formalism but below the source language. In the taxonomy of R1CS, AIR, PLONKish, and CCS from Chapter 5, ZKIR is most analogous to PLONKish but operates at a higher abstraction level -- the developer sees typed operations with semantic meaning, not bare multiplication gates.

To make this concrete: the `verify_sudoku` circuit from Chapter 3's Compact example would compile to a ZKIR graph of approximately 200-300 instruction nodes. Each range check ("is this cell between 1 and 4?") becomes a `constrain_bits` instruction. Each equality check ("does the solution match the given clue?") becomes a `constrain_eq`. Each hash computation for nullifier generation becomes a `persistent_hash` -- a single instruction that the backend expands into dozens of PLONKish gates. The developer never sees those gates. She sees `persistent_hash([pad(32, "nullf:"), secret_key])` and knows what it means. The translation from human intent to polynomial constraints happens entirely inside the ZKIR backend.

This abstraction has a cost. Every `persistent_hash` instruction expands to a full Poseidon circuit -- roughly 300 multiplication gates. Every `ec_mul` (elliptic curve scalar multiplication on Jubjub) expands to hundreds of gates for the double-and-add algorithm. The ZKIR abstraction hides this expansion from the developer, which improves correctness (she cannot write under-constrained gates because she never writes gates) but obscures performance (she may not realize that a single `persistent_hash` costs more than all her arithmetic operations combined). This is arithmetic with a human face -- and like all abstractions, it trades visibility for safety.

### Layer 5: Halo 2 and the Four-Phase Pipeline

Midnight uses Halo 2 (UltraPlonk) over BLS12-381. The choice was pragmatic: when Midnight's proof system was designed, Halo 2 was the most mature PLONK variant with universal SRS support, a production-tested implementation (originally developed by the Electric Coin Company for Zcash), and extensive documentation. Alternatives like Plonky2 (which uses Goldilocks, a 64-bit field) would have been faster but incompatible with BLS12-381's pairing structure. The decision traded speed for ecosystem maturity -- a tradeoff that Chapter 7's cascade effect predicts.

The proof server runs locally at `localhost:6300`. The transaction lifecycle follows a four-phase pipeline:

1. **`callTx()`** — Execute the circuit locally with private witnesses. The SDK queries the indexer for current ledger state, runs the Compact circuit with the developer's witness functions, and produces an unproven transaction. This step is fast (milliseconds) because it is ordinary computation, not proof generation.

2. **`proveTx()`** — Generate the ZK proof. This is the dominant latency: 17-24 seconds for a typical circuit call, 17-28 seconds for contract deployment. The developer's machine is running the full Halo 2 prover -- computing polynomial commitments, evaluating KZG opening proofs, and binding the public transcript to the proof. During this time, the developer sees... very little. The SDK provides a promise that resolves when the proof is ready. There is no progress bar, no intermediate feedback. Just a wait, then a result. This is the experience described in Chapter 3's "Step 4: Prove" -- anticlimactic when it works, opaque when it fails.

3. **`balanceTx()`** — Bind the transaction, run token balancing (shielded, unshielded, and DUST), and sign UTXO inputs with BIP-340 Schnorr signatures. Sub-second.

4. **`submitTx()`** — Submit to the blockchain, where the node verifies the ZK proof against the on-chain verifier key. Sub-second for submission; verification is near-instantaneous.

The asymmetry is striking: the prover works for twenty seconds; the verifier confirms in milliseconds. The magician rehearses for twenty seconds. The audience's verdict takes a heartbeat. This asymmetry is not a flaw -- it is the fundamental architecture of zero-knowledge computation. The prover's cost buys the verifier's convenience.

### Layer 6: BLS12-381, Jubjub, and Poseidon

All ZKIR values are elements of the BLS12-381 scalar field ($\sim 2^{253}$). Three cryptographic primitives build on this foundation:

**Jubjub** is a twisted Edwards curve embedded natively in BLS12-381. "Embedded" means that Jubjub's arithmetic can be performed using BLS12-381 field operations -- no expensive cross-field emulation needed. This is what makes in-circuit elliptic curve operations practical. Midnight uses Jubjub for three critical functions: key derivation (computing public keys from secret keys inside the circuit), nullifier computation (producing the unique identifier that prevents double-spending of shielded UTXOs), and BIP-340 Schnorr signatures (signing unshielded UTXO spends in `balanceTx`). Without an embedded curve, each of these operations would require non-native arithmetic -- the "long division by hand" penalty from Chapter 7 -- multiplying the constraint count by 10x or more.

**Poseidon** provides ZK-friendly hashing. The ZKIR exposes two variants: `persistent_hash` (producing two field elements for collision resistance, used for Merkle roots and content-addressed storage) and `transient_hash` (producing a single field element, used for challenge derivation). As Chapter 7 discussed, Poseidon costs roughly 300 constraints per hash -- compared to 25,000 for SHA-256. But Poseidon's algebraic structure also creates the cache-timing vulnerability surface described in Chapter 4: the S-box lookups that make Poseidon algebraically efficient are the same lookups that leak information through cache access patterns in shared environments.

**The field size tradeoff**: At 253 bits per field element, BLS12-381 is 8x wider than BabyBear (31 bits) and 4x wider than Goldilocks (64 bits). Every field multiplication, every NTT butterfly, every polynomial evaluation operates on 253-bit numbers instead of 31-bit ones. On modern CPUs, a 31-bit multiply is a single machine instruction; a 253-bit multiply requires 16 limb multiplications with carry propagation -- roughly 20-30 machine instructions. The aggregate penalty is 10-100x slower per operation. This is the cost of the pairing structure that enables KZG commitments and constant-size proofs. Systems like SP1 (BabyBear) and Stwo (Mersenne-31) that use small fields achieve their speed precisely by abandoning pairings -- a tradeoff Midnight cannot make without losing its commitment scheme. Midnight pays for privacy with patience.

### Layer 7: Three Tokens and the Verifier Key Lifecycle

Midnight's three-token model (NIGHT/DUST/custom) and per-UTXO privacy choice create a deployment architecture distinct from Ethereum-style gas economics. DUST fees are paid in a public token generated by time-locked staking.

The economics deserve closer scrutiny, because they encode a philosophy. On Ethereum, gas is purchased with ETH on the open market -- every fee payment is a visible transaction, a data point for chain analysts, a signal. On Midnight, DUST accrues silently from staked NIGHT over time, like interest accumulating in an account the holder never visits. A developer deploying a contract pays ~490 trillion SPECK per circuit call, but that DUST was not purchased in a transaction anyone can observe. It was generated by the passage of time and the act of staking. The economic consequence is that fee payment itself becomes a poor signal: an observer who watches DUST expenditures sees activity, but cannot easily link that activity back to a market purchase, a wallet funding event, or an exchange withdrawal. The three-token architecture is not merely a governance convenience. It is a privacy mechanism at the economic layer -- a recognition that in a system where computation is private, the payment for computation must be private too, or else the ticket stub betrays the show. Penrose once observed that the geometry of a space constrains what can happen within it. Midnight's token geometry -- the separation of governance (NIGHT), fees (DUST), and application value (custom tokens) -- constrains the information that economic activity can leak. The shape of the money shapes the privacy of the system. This is Layer 7 not as an afterthought but as architecture.

The SDK API includes functions for dynamically managing verifier keys on-chain (`submitInsertVerifierKeyTx`, `submitRemoveVerifierKeyTx`), raising governance questions that parallel the book's discussion of upgradeable proxy contracts. The theater management retains the ability to change the locks -- to swap out the verifier that guards a contract's stage door, to retire a circuit and replace it with another. In a traditional theater, this is the producer's prerogative: the show can be recast, the set redesigned, the script rewritten between seasons. But in a privacy theater, changing the verifier key changes the terms under which secrets were originally committed. A user who shielded tokens under one verifier's rules may find those rules altered by a governance action she never approved. The trapdoor that was locked for the performer's protection can be unlocked by the theater's owner. This tension -- between upgradeable infrastructure and the immutability that privacy demands -- is not resolved in Midnight's current design. It is, at most, acknowledged.

To understand the weight of this tension, consider what a verifier key upgrade actually involves. The on-chain verifier key is derived from the universal SRS and the specific ZKIR circuit. Changing the circuit -- fixing a bug, adding a feature, optimizing a constraint -- requires a new verifier key. The old key must be removed (`submitRemoveVerifierKeyTx`) and the new one inserted (`submitInsertVerifierKeyTx`). During the transition, proofs generated under the old key cannot be verified by the new key, and proofs generated under the new key cannot be verified by the old one. Users who generated proofs before the upgrade but have not yet submitted them hold orphaned proofs -- mathematically valid certificates that no on-chain verifier will accept.

For shielded tokens, the stakes are higher. A user who deposited tokens under one verifier key holds a commitment that encodes the circuit's constraint structure. If the circuit changes, the commitment may no longer be provably spendable under the new constraints. The user's funds are not lost -- the blockchain state still records the commitment -- but the proof required to spend them may be impossible to generate under the new circuit. This is the privacy system's version of the key rotation problem that plagues every long-lived cryptographic system.

Ethereum rollups handle this through proxy contracts and multisig governance -- the approach Chapter 8's Beanstalk and Tornado Cash case studies showed can be catastrophically exploited. Midnight's immutable-verifier design avoids the Beanstalk attack surface by making key replacement a visible, auditable on-chain event rather than a silent proxy upgrade. But it replaces one governance problem (who holds the multisig?) with another (who decides when a circuit needs upgrading, and how are affected users migrated?). The documentation is silent on this question. It is the theater's most conspicuous gap.


## Summary

This section maps all seven layers of the ZK stack onto Midnight's concrete architecture. Layers 1--7 are instantiated with BLS12-381/Halo 2 (trusted universal SRS), Compact's disclosure-analysis DSL, the `disclose()` boundary separating witness from circuit, ZKIR's 24-opcode typed IR, the four-phase proof pipeline (17--28 s), the Jubjub/Poseidon/BLS12-381 commitment stack, and the NIGHT/DUST/custom three-token fee model with on-chain verifier key lifecycle.

## Key claims

- Layer 1: BLS12-381 + Halo 2 with a universal SRS; originally Pluto-Eris curves, switched to BLS12-381 for mainnet.
- Layer 1: ~128-bit classical security; zero post-quantum security; Shor's algorithm breaks both DL and pairing simultaneously.
- Layer 2: Compact is a fourth philosophy (application-specific DSL), distinct from EVM-compatible, ZK-native ISA, and general-purpose ISA approaches.
- Layer 2: Disclosure analysis (`track-witness-data`) rejects programs at compile time where private data can reach public surfaces without `disclose()`; a private voting prototype triggered 11 errors.
- Layer 3: `publicTranscript` and `privateTranscriptOutputs` are the two ZKIR channels; `disclose()` is the only gateway between them.
- Layer 3: Side-channel gaps (Poseidon cache timing, indexer GraphQL metadata, 20-second submission fingerprint) are unaddressed in documentation.
- Layer 4: ZKIR has 24 base instructions in 8 categories; `persistent_hash` expands to ~300 PLONKish gates; `ec_mul` (Jubjub) to hundreds of gates.
- Layer 5: Four-phase pipeline -- `callTx` (ms), `proveTx` (17--28 s), `balanceTx` (sub-second), `submitTx` (sub-second).
- Layer 6: BLS12-381 scalar field (~2^253); 10--100x arithmetic penalty vs. BabyBear/Goldilocks; Poseidon costs ~300 constraints vs. ~25,000 for SHA-256.
- Layer 7: DUST accrues from staking rather than open-market purchase, making fee payment a weak signal for chain analysts; ~490 trillion SPECK per circuit call.
- Layer 7: `submitInsertVerifierKeyTx`/`submitRemoveVerifierKeyTx` enable on-chain key management; orphaned proofs and frozen shielded tokens are unaddressed risks during key transitions.

## Entities

- [[beanstalk]]
- [[bls12-381]]
- [[ceremony]]
- [[folding]]
- [[goldilocks]]
- [[halo]]
- [[halo2]]
- [[jubjub]]
- [[kzg]]
- [[mersenne]]
- [[midnight]]
- [[ntt]]
- [[plonk]]
- [[poseidon]]
- [[sdk]]
- [[sudoku]]
- [[tornado cash]]
- [[utxo]]
- [[zcash]]

## Dependencies

- [[ch02-midnight-s-bls12-381-stage]] — BLS12-381 curve choice and SRS ceremony context
- [[ch03-compact-s-disclosure-analysis]] — disclosure analysis pass detail
- [[ch04-the-disclose-boundary-midnight-s-witness-architecture]] — `disclose()` operator and transcript channels
- [[ch05-midnight-s-zkir-a-concrete-layer-4]] — ZKIR instruction set taxonomy
- [[ch07-case-study-midnight]] — Jubjub/Poseidon/field-size tradeoff analysis
- [[ch08-case-study-midnight-and-the-three-token-architecture]] — three-token economic model at Layer 7

## Sources cited

- Midnight Developer Guide, p.8 (architecture diagram, `midnight-trusted-setup` repository)
- Midnight Developer Guide (per-circuit key sizes: `increment.prover` 13.7 KB, `increment.verifier` 1.3 KB)
- ZKIR Specification (24 base instructions, 8 categories)
- MidnightJS SDK Reference (`submitInsertVerifierKeyTx`, `submitRemoveVerifierKeyTx`)

## Open questions

- Side-channel completeness: no documentation addresses constant-time proof generation, indexer query privacy, network timing fingerprinting, or Poseidon/Jubjub cache-timing resistance.
- Verifier key upgrade migration: documentation is silent on how affected users with orphaned proofs or frozen shielded-token commitments are handled during a circuit upgrade.

## Improvement notes

- [P1] (A) Layer 6 states the BLS12-381 scalar field is "~2^253"; the scalar field prime for BLS12-381 is ~2^255 (255-bit prime). The same approximation appears in ch07-case-study-midnight, so this is a systemic error — both sections need correction.
- [P1] (A) Layer 5 labels Halo 2 as "UltraPlonk" (parenthetical): Halo 2 uses a UltraPLONK arithmetization but is not itself branded "UltraPlonk"; calling the proof system "UltraPlonk" conflates the arithmetization with the overall proof system name.
- [P1] (D) Layer 7 describes `submitInsertVerifierKeyTx`/`submitRemoveVerifierKeyTx` enabling on-chain key changes, but ch08 characterises Midnight verifier keys as "immutable — once deployed, a contract's verification logic cannot be changed." The two sections are in tension; one of them must qualify the other.
- [P2] (A) Layer 7 states "~490 trillion SPECK per circuit call": SPECK is a non-standard sub-unit denomination not defined in the wiki; no source is cited. Either source this or note it as an approximation from documentation.
- [P2] (B) The Pluto-Eris curve history (Layer 1) is a specific factual claim with no citation; the Halo 2 backend rationale (Layer 5) likewise cites no source. These are strong claims that need anchoring.
- [P3] (C) Layer 3 contains an extended Asimov analogy and a theater-lighting metaphor that add length without information gain; the core point (disclosure analysis = compile-time hard error) is made adequately in the first paragraph of that sub-section.

## Links

- Up: [[12-midnight-the-privacy-theater]]
- Prev: [[ch12-midnight-at-a-glance]]
- Next: [[ch12-where-midnight-validates-the-model]]
