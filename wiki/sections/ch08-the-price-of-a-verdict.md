---
title: "The Price of a Verdict"
slug: ch08-the-price-of-a-verdict
chapter: 8
chapter_title: "Layer 7 -- The Verdict"
heading_level: 2
source_lines: [3546, 3631]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 1775
---

## The Price of a Verdict

Let us start with money, because money clarifies.

A Groth16 proof verification on Ethereum uses the BN254 elliptic curve pairing precompiles introduced in the Byzantium hard fork (2017) and made cheaper by the Istanbul upgrade's EIP-1108 (2019). The gas cost breaks down as follows:

| Component | Gas Cost |
|-----------|----------|
| Pairing check (4 pairings via EIP-1108) | 181,000 |
| Calldata (256-byte proof) | 4,096 |
| EVM scaffolding | ~1,600 |
| Per public input | ~7,160 each |
| **Total (fixed, no public inputs)** | **~207,700** |

The formula is roughly $(181 + 6L) \times 1{,}000$ gas for $L$ public inputs. At typical Ethereum gas prices and ETH valuations, this works out to somewhere between fifty cents and two dollars per verification. Call it a dollar.

One dollar. To check a proof that summarizes thousands, or millions, of computations. That is the economic engine of the entire zero-knowledge rollup industry. It is also worth noting: the cost of *rendering a verdict* on an arbitrarily complex computation is effectively fixed. The computation can be ten steps or ten billion. The verdict costs the same.

But notice what that dollar buys. It buys a *Groth16* verification. Groth16 requires a trusted setup (Layer 1), uses elliptic curve pairings on BN254 (Layer 6), and produces the smallest proofs in the field -- three group elements that fit in a tweet. The cheapness of the verdict is not free. It is subsidized by decisions made five layers below.

What about STARKs? The paper being revised presents STARK verification as expensive -- two to five million gas -- and contrasts this with SNARK cheapness. This framing was arguably accurate in 2022. It is misleading in 2026. The reason is simple: nobody posts raw STARKs to Ethereum.

The actual production pipeline looks like this:

1. Generate a STARK proof (transparent, no trusted setup, large -- hundreds of kilobytes).
2. Recursively compress the STARK through multiple rounds.
3. Wrap the final compressed STARK inside a Groth16 proof.
4. Post the Groth16 proof to Ethereum.

Starknet's SHARP (Shared Prover) does this. Succinct's SP1 does this. Polygon's CDK does this. The verifier contract on Ethereum sees Groth16 in every case. The "STARK path" and the "SNARK path" converge at the courthouse door.

The actual cost differential between the two approaches, then, is not the 10-25x that a naive comparison of raw STARK versus Groth16 verification would suggest. It is closer to 2x -- the overhead of the wrapping step, amortized across many proofs. The inner proof system matters enormously for prover economics (speed, hardware requirements, parallelizability), but the on-chain verification cost is nearly identical.

There is a throughput ceiling too. An Ethereum block has a 30-million-gas limit (raised from the historical 15 million, with a 45-million effective target under various proposals). At 207,700 gas per Groth16 verification, you can fit roughly 150 to 225 verifications per block. That sounds like a lot, until you realize that each verification corresponds to a batch of rollup transactions. If Ethereum hosts 50 rollups and each wants to verify once per block, they consume less than a quarter of the block's capacity. But if we want real-time proving (verification every L1 slot), with hundreds of rollups and bridges, the verification gas budget starts to matter.

FFLONK, an alternative to Groth16, costs roughly 236,000 gas per verification -- slightly more, but with the advantage of a universal trusted setup (one ceremony works for all circuits, unlike Groth16's per-circuit setup). The gas difference is marginal. The governance and operational difference -- not needing a new ceremony for each circuit -- is substantial.

### The Verification-Data Seesaw

Before March 2024, the dominant cost of running a ZK rollup on Ethereum was not verification. It was data availability. Posting transaction data (or state diffs) as calldata cost roughly 16 gas per byte. A typical rollup batch might include hundreds of kilobytes of data, costing millions of gas -- dwarfing the ~200,000 gas for the proof check.

EIP-4844, deployed in the Dencun upgrade on March 13, 2024, changed this calculus fundamentally. It introduced "blob transactions" -- a new data type designed specifically for rollup data. Each blob contains 4,096 field elements of 32 bytes (~128 KB), with a target of 3 blobs per block and a maximum of 6. Critically, blobs have their own fee market, separate from Ethereum's execution gas market, operating under a blob-specific EIP-1559 mechanism.

The result: rollup data costs dropped by 10-100x overnight. Blob fees settled near zero because demand was well below the 3-blob target -- as of mid-2024, only about 34% of Ethereum blocks contained any blobs at all, and the average was 1.33 blob transactions per block.

But Ethereum did not stop at EIP-4844. Two subsequent upgrades expanded DA capacity further:

- **Pectra** (May 2025): Doubled blob targets from 3 to 6, and maximum from 6 to approximately 9.
- **Fusaka** (December 2025): Introduced PeerDAS (Peer Data Availability Sampling), implementing a distributed sampling scheme that raised the blob target to 14 and maximum to 21 -- an 8x increase in DA capacity over the original EIP-4844 specification.

The seesaw has tipped. With blob fees near zero and DA capacity expanding rapidly, the ~200,000 gas verification cost has become the *dominant* L1 settlement expense for many ZK rollups. This inversion matters because it changes what is worth optimizing. Before EIP-4844, the rational investment was in compression (minimizing data). After EIP-4844, the rational investment is in proof aggregation (amortizing verification across more transactions per batch) and in cheaper verification schemes.

### Beyond Ethereum: The DA Marketplace

Ethereum is not the only source of data availability. A marketplace has emerged:

**Celestia** charges roughly $0.07 per megabyte for data availability, compared to Ethereum's blob cost of roughly $3.83 per megabyte (when blobs are priced above the floor). Celestia achieves this by being a purpose-built DA layer -- it provides data ordering and availability guarantees without executing any transactions. The intellectual lineage traces directly to Mustafa Al-Bassam's LazyLedger (2019), which proposed a blockchain that does nothing but guarantee data is available and ordered, leaving execution to sovereign rollups that interpret their own transaction rules.

**EigenDA V2** targets 100 megabytes per second of throughput -- roughly two orders of magnitude more than Ethereum's native DA capacity. It achieves this by leveraging Ethereum's security through restaking (EigenLayer), where validators stake ETH to back DA guarantees.

**Avail** offers a third alternative, with its own DAS-based light client verification model.

The choice between these DA layers is not purely technical. A rollup that uses Celestia for DA instead of Ethereum blobs trades Ethereum's full consensus security for lower costs. This is a Layer 7 governance decision with Layer 6 security implications: the data availability guarantee is only as strong as the weakest link in the DA provider's consensus mechanism.

### Data Availability

The term "data availability" is one of those phrases that sounds self-explanatory and is not. It does not mean "the data exists somewhere." It does not mean "the data is stored on a server." It means something specific and testable: if you send a transaction to a rollup, can any participant in the world reconstruct the rollup's complete state using only publicly available data?

If yes, the rollup has data availability. Anyone can verify that the rollup operator is honest by replaying all transactions from genesis and checking that the claimed state matches the computed state. If no -- if some of the data is withheld, stored only on the operator's private servers, or available only to a privileged set of participants -- then the operator could cheat and nobody would know. The operator could include a transaction that steals every user's funds, prove that the resulting state transition is "valid" (because the ZK proof only proves that *some* valid transition occurred), and nobody could challenge it because nobody can see the inputs.

This is the critical subtlety that connects data availability to zero-knowledge proofs. A ZK proof proves that a state transition was computed correctly. It proves that if you start from state S and apply transactions T, you arrive at state S'. What it does *not* prove -- what it *cannot* prove, by design -- is what state S actually was. The proof attests to the correctness of the computation, not the availability of the inputs. If the operator claims the starting state was S but actually started from a fabricated state S_fake, the ZK proof will happily prove that the transition from S_fake was computed correctly. Without DA, nobody can verify the starting point.

Data availability is the anchor. The ZK proof is the chain. Without the anchor, the chain secures nothing.

The three DA strategies represent different points on the cost-security tradeoff:

**Ethereum calldata** is the oldest and most expensive approach. Transaction data is posted directly as calldata in Ethereum L1 transactions, stored permanently by every full node, and protected by Ethereum's full consensus security. The cost is high -- 16 gas per byte of calldata -- but the guarantee is absolute: if Ethereum's consensus is secure, the data is available. This was the only option before March 2024, and it made rollup operations expensive enough that most of the early rollup economics were dominated by DA costs rather than verification costs.

**Ethereum blobs** (EIP-4844 and successors) are the middle ground. Blob data is posted to Ethereum and protected by Ethereum's consensus during a pruning window (currently approximately 18 days), after which nodes may discard it. The data is available long enough for any challenge period to complete, and it is significantly cheaper than calldata because blobs have their own fee market and do not compete with execution gas. This is the default choice for most production rollups in 2026.

**External DA layers** (Celestia, EigenDA, Avail) are the cheapest option with a different trust model. The data is posted to a separate blockchain or protocol that specializes in data ordering and availability guarantees. The cost can be 10-100x lower than Ethereum blobs. The tradeoff is that the DA guarantee depends on the external protocol's consensus and validator set, not Ethereum's. A rollup using Celestia for DA inherits Celestia's security assumptions. If Celestia's validator set colludes or fails, the rollup's data may become unavailable even though Ethereum itself is functioning correctly.

The choice of DA strategy is, in practice, one of the most consequential governance decisions a rollup team makes. It determines the rollup's operating cost, its security model, its relationship to Ethereum's consensus, and its vulnerability to the DA-saturation attacks discussed later in this chapter. It is a Layer 7 decision with implications that cascade through every layer below.

---


## Summary

Groth16 verification on Ethereum costs roughly 207,700 gas (~$1) regardless of computation size, but this cheapness reflects decisions made five layers below (BN254 curve, pairing precompiles). The dominant rollup cost shifted from data availability to verification after EIP-4844 reduced blob fees 10–100×, making proof aggregation the key optimization target for 2026.

## Key claims

- Groth16 gas breakdown: 181,000 (4 pairings via EIP-1108) + 4,096 (calldata) + ~1,600 (EVM) + ~7,160 per public input ≈ 207,700 total fixed cost.
- Nobody posts raw STARKs on-chain; production pipelines (SHARP, SP1, Polygon CDK) wrap STARKs in Groth16, converging STARK and SNARK on-chain costs to within ~2×.
- Ethereum block gas limit of 30M allows roughly 150–225 Groth16 verifications per block.
- FFLONK costs ~236,000 gas but uses a universal trusted setup, avoiding per-circuit ceremonies.
- EIP-4844 (March 2024) reduced rollup DA costs 10–100× via blob transactions with a separate fee market.
- Pectra (May 2025) doubled blob targets (3→6); Fusaka (December 2025) raised target to 14 via PeerDAS — 8× total increase over original EIP-4844.
- Post-EIP-4844, verification cost (~200K gas) is now the dominant L1 settlement expense for many ZK rollups.
- Celestia charges ~$0.07/MB vs Ethereum's ~$3.83/MB; EigenDA V2 targets 100 MB/s throughput.
- Data availability means any participant can reconstruct full rollup state from public data; without it a ZK proof attests to computation correctness but not starting-state integrity.

## Entities

- [[bn254]]
- [[groth16]]
- [[starknet]]
- [[starks]]

## Dependencies

- [[ch08-the-social-layer]] — establishes Layer 7 framing and the four concerns
- [[ch08-proof-aggregation-the-missing-layer]] — aggregation amortizes the ~200K gas cost
- [[ch08-pricing-attacks]] — DA cost structure creates exploitable seams
- [[ch06-the-three-families]] — STARK vs SNARK tradeoffs that converge at Layer 7

## Sources cited

- EIP-1108 (Istanbul, 2019) — pairing precompile gas reduction
- EIP-4844 (Dencun, March 2024) — blob transactions
- Pectra upgrade (May 2025) — blob target doubled
- Fusaka upgrade (December 2025) — PeerDAS, blob target 14
- Mustafa Al-Bassam, LazyLedger (2019)

## Open questions

None flagged by this section.

## Improvement notes

- [P1] (A) The "8× increase in DA capacity over the original EIP-4844 specification" claim for Fusaka/PeerDAS is incorrect: the blob target rises from 3 to 14, which is roughly 4.7×, not 8×.
- [P2] (A) The inline gas formula "$(181 + 6L) \times 1{,}000$ gas" does not reproduce the table total (~207,700) at L=0 (gives 181,000); the formula is inconsistent with the itemized breakdown presented immediately above it.
- [P2] (B) The DA marketplace figures (Celestia ~$0.07/MB, Ethereum ~$3.83/MB, EigenDA V2 100 MB/s, 34% of blocks with blobs) carry no citations; they should be anchored to a date-stamped source.

## Links

- Up: [[08-the-verdict]]
- Prev: [[ch08-the-social-layer]]
- Next: [[ch08-when-the-transcript-lies-fiat-shamir-vulnerabilities]]
