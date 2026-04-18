---
title: "Case Study: Midnight and the Three-Token Architecture"
slug: ch08-case-study-midnight-and-the-three-token-architecture
chapter: 8
chapter_title: "Layer 7 -- The Verdict"
heading_level: 2
source_lines: [3797, 3866]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 1211
---

## Case Study: Midnight and the Three-Token Architecture

Midnight, developed by IOG (Input Output Global), provides an instructive case study for Layer 7 because it makes different architectural choices than the Ethereum rollup model. Where Ethereum rollups post proofs to a general-purpose L1 and rely on upgradeable verifier contracts, Midnight integrates verification into its consensus layer and uses a novel three-token economic model that directly shapes the verification experience.

### The Verification Pipeline

Midnight uses a split execution model. Smart contracts are written in Compact, a domain-specific ZK language, but they never execute on-chain in the traditional sense:

1. The user's SDK executes the Compact circuit locally, computing the new state.
2. A proof server generates a ZK proof that the state transition is valid.
3. The SDK packages the proof, fee inputs, and state delta into a transaction.
4. Every Midnight node verifies the proof against the circuit's verifier keys, which were deployed on-chain when the contract was created.
5. If valid, the blockchain updates the contract's ledger state.

The critical difference from the Ethereum rollup model: verification is not performed by a specialized verifier contract that can be upgraded via governance. It is performed by every node as part of consensus. The verifier keys are stored on-chain at the contract address and are immutable -- once deployed, a contract's verification logic cannot be changed. A new contract must be deployed for logic changes.

This is a strong answer to the governance-as-attack-surface problem. You cannot upgrade what is immutable. But it creates a different problem: what happens when there is a bug? The answer is migration -- deploy a corrected contract and convince users to move to it. This is slower and messier than a governance upgrade, but it cannot be exploited by an attacker with admin keys. The tradeoff is explicit: Midnight accepts the inconvenience of immutability in exchange for immunity to the Beanstalk-style attack.

### Three Tokens, Three Privacy Levels

Midnight's three-token model is not an arbitrary design choice. Each token represents a different point on the privacy-transparency spectrum, and together they create an economic system where verification costs, privacy guarantees, and governance rights are separate and independently tunable.

**Night** is the unshielded native token. It is fully transparent -- all operations are publicly visible on the ledger, stored as UTXOs with public-key authentication. Night serves two purposes: staking (and therefore governance) and backing for DUST generation. Every Night token registered for dust generation produces DUST over time at a deterministic rate.

**Shielded tokens** are ZK-private custom tokens. Any Compact contract can mint shielded tokens with unique type identifiers ("colors"). Balances and transaction details are hidden via zero-knowledge proofs. Shielded tokens use UTXOs with Pedersen commitments -- only the key holder can view or modify wallet state. All shielded token transfers go through contracts, not direct peer-to-peer.

**DUST** is the fee token. All transaction fees are denominated in DUST, but DUST is not mined or minted in the traditional sense. It is a time-dependent scalar computed from Night holdings. A user registers Night UTXOs for dust generation, and DUST accumulates over time according to a deterministic formula with parameters for rate, maximum cap, and creation time.

This creates a novel fee model with direct implications for verification economics:

- **No fee market**: Fees are computed deterministically, not bid. There is no gas auction.
- **Rate-limited spam**: Transaction throughput is naturally limited by DUST regeneration rate relative to Night holdings. An attacker who wants to spam the network must hold (or acquire) Night tokens and wait for DUST to regenerate.
- **Staking alignment**: Only Night holders can generate DUST. Transaction capability is tied to network participation.
- **Time-gated recovery**: A user who has spent all their DUST must wait for regeneration before transacting again. This is a natural circuit breaker against denial-of-service attacks.

### Disclosure Rules and Compiler-Enforced Privacy

In Compact, everything is private by default. Values only appear on-chain when the developer explicitly calls `disclose()`. The Compact compiler enforces this through static disclosure analysis at compile time -- privacy is a compiler guarantee, not developer discipline.

What must be disclosed includes contract ledger state (any `export ledger` field), counter increments and decrements, state transition deltas (so validators can verify the new state), nullifiers (to prevent double-spending), and hash commitments (stored for future verification). What stays private includes secret keys, witness values (circuit private inputs), shielded balances, vote choices (only aggregate tallies change on-chain), authorization preimages, and computation logic (ZK proof hides the execution path).

This compiler-enforced privacy boundary is a significant Layer 7 innovation. In the Ethereum model, what is public and what is private depends on the developer's care in managing calldata, events, and storage. In Midnight, the compiler draws the line, and crossing it requires an explicit annotation that is visible in code review.

### Private Governance

Midnight's DAO governance pattern demonstrates what private on-chain governance can look like:

- **Anonymous identity**: Voters prove membership via hash commitments, never revealing their real identity.
- **Weighted voting**: Contract-state token balances serve as anonymous voting weights via ZK circuit reads.
- **Per-proposal nullifier domains**: Each proposal has its own nullifier space, preventing double-voting while allowing participation across multiple proposals.
- **Vote privacy**: The voter's choice remains private -- only the aggregate tally changes on-chain.
- **Irreversible state machines**: Proposal status is encoded as counter increments (0 unused, 1 open, 2 approved, 3 executed), and counters are monotonically increasing, so state transitions are irreversible by construction.

The multi-signature treasury adds M-of-N threshold approval with propose/approve/execute circuits, where signer identity is verified via hash commitment and double-vote prevention uses per-(proposal, signer) nullifiers.

Every design choice is a direct architectural response to the attacks we just witnessed. Anonymous weighted voting means an attacker cannot flash-loan governance tokens and vote -- they would need to know the secret key that corresponds to a registered hash commitment, and flash-loaning tokens does not give them that. Irreversible state machines mean a proposal cannot be rolled back after execution. Per-proposal nullifier isolation means vote manipulation in one proposal cannot leak to another.

The Beanstalk attacker borrowed a billion dollars of voting power for the duration of a single transaction. Against Midnight's architecture, that borrowing would be useless. You cannot vote with a key you do not possess.

### The Gaps

Midnight's approach is not without its own Layer 7 vulnerabilities:

- **Protocol upgrade governance**: The documentation does not describe how consensus-level parameters (fee rates, dust generation parameters, consensus rules) are governed. This is the most significant gap. Immutable contracts solve contract-level governance attacks, but someone must still govern the protocol itself.
- **Oracle centralization**: All oracle patterns in the current documentation use single-party authorization via hash commitment. There is no multi-oracle or threshold-oracle pattern. A single compromised oracle can feed false data to every contract that depends on it.
- **Fixed participant sets**: Current governance contracts hardcode 2-3 participant slots. Production governance with dynamic participant sets would require Merkle-tree-based registration, which has been demonstrated (in the lending pool pattern) but not yet integrated into governance contracts.
- **No emergency procedures**: There is no documented kill switch, pause mechanism, or emergency parameter override for deployed contracts. Immutability is a feature for preventing governance attacks, but it is a liability when a critical bug is discovered.

---


## Summary

Midnight integrates ZK verification into consensus — every node verifies proofs — rather than delegating to an upgradeable contract, making verifier keys immutable after deployment. Its three-token model (Night for staking/governance, DUST for fees, shielded tokens for privacy) creates a spam-resistant, flash-loan-immune fee economy with compiler-enforced privacy boundaries.

## Key claims

- Verification is performed by every Midnight node as part of consensus, not by a governance-controlled proxy contract; verifier keys are immutable at the contract address.
- Bug response requires contract migration, not governance upgrade — trades operational convenience for immunity to Beanstalk-style admin-key attacks.
- Night (transparent UTXO token): staking, governance, and DUST backing.
- DUST (fee token): deterministically computed from Night holdings over time; no gas auction, rate-limited by regeneration.
- Shielded tokens: ZK-private, UTXO with Pedersen commitments, custom type identifiers per Compact contract.
- Compact compiler enforces privacy at compile time via `disclose()` annotations; private by default.
- Private governance: anonymous weighted voting via hash commitments; per-proposal nullifier domains prevent double-voting; counter-based irreversible state machines prevent rollbacks.
- Flash-loan governance attacks fail — borrowing tokens does not transfer the secret key bound to the hash commitment.
- Known gaps: protocol-level upgrade governance undocumented; single-oracle authorization; fixed 2-3 participant slots in current governance contracts; no emergency pause.

## Entities

- [[midnight]]
- [[nova]]
- [[pedersen]]
- [[sdk]]
- [[beanstalk]]

## Dependencies

- [[ch08-governance-the-achilles-heel]] — Beanstalk/Tornado Cash attacks that Midnight's architecture responds to
- [[ch08-who-verifies-the-verifier]] — immutable verifier tradeoff table includes Midnight as example
- [[ch03-compact-s-disclosure-analysis]] — Compact compiler and disclosure analysis
- [[ch04-the-disclose-boundary-midnight-s-witness-architecture]] — witness architecture underlying the privacy boundary

## Sources cited

None in this section.

## Open questions

- How are consensus-level parameters (fee rates, dust generation, consensus rules) governed? Not described in current documentation.
- No multi-oracle or threshold-oracle pattern documented.

## Improvement notes

## Links

- Up: [[08-the-verdict]]
- Prev: [[ch08-proof-aggregation-the-missing-layer]]
- Next: [[ch08-the-deepest-symmetry]]
