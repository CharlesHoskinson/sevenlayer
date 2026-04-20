---
title: "Proof Aggregation: The Missing Layer"
slug: ch08-proof-aggregation-the-missing-layer
chapter: 8
chapter_title: "Layer 7 -- The Verdict"
heading_level: 2
source_lines: [3779, 3794]
source_commit: 53f41415d307dcd4ed73d852dfd6aa97146e882f
status: reviewed
word_count: 256
---

## Proof Aggregation: The Missing Layer

Between the prover (who generates proofs) and the on-chain verifier (who checks them), a significant infrastructure layer has emerged that the seven-layer model does not account for: proof aggregation services. In terms of the stack, aggregation sits at Layer 7 but acts as a trust intermediary between Layers 5-6 (the proof system) and the on-chain verifier -- a sub-layer that inherits the security properties of neither automatically.

**SHARP (Shared Prover)**, built by StarkWare for Starknet (documentation: docs.starknet.io), is the original aggregation service. Multiple applications submit their execution traces to SHARP, which generates a single STARK proof covering all of them, then wraps that proof in Groth16 for on-chain verification. The verification gas cost is amortized across all participating applications.

**Aligned Layer**, launched on mainnet in late 2024 with over $11 billion in restaked ETH secured via EigenLayer at launch (Aligned Layer launch announcement, November 2024), provides verification-as-a-service. Rollups and applications submit proofs to Aligned Layer, which batches and verifies them, posting the aggregated result to Ethereum.

**NEBRA**, live since August 2024 (NEBRA mainnet launch post, August 2024), provides proof aggregation with a focus on universal verification -- supporting multiple proof systems (Groth16, PLONK, STARK) within a single aggregation layer.

The economic logic is straightforward. If a single Groth16 verification costs ~187,000 gas, and an aggregation service can batch 100 proofs into a single on-chain verification, the per-proof verification cost drops from ~$1 to ~$0.01. At sufficient volume, aggregation makes proof verification nearly free.

But aggregation introduces new trust assumptions that the seven-layer model must account for. The aggregation service sits between prover and verifier and makes two commitments: that it correctly includes submitted proofs in the batch, and that the aggregated proof faithfully represents all constituent proofs. These commitments are not automatically inherited from the underlying proof system's soundness. A soundness error or equivocation at the aggregation layer can silently drop proofs, reorder them, or substitute forged proofs -- and the on-chain verifier, seeing a valid aggregated proof, has no way to detect the manipulation. If the aggregation service is centralized (as SHARP is for Starknet), it is a single point of failure at Layer 7 that can undermine the decentralization guarantees of Layers 1 through 6. The aggregator's own governance therefore warrants the same scrutiny as the verifier contract's governance.

---


## Summary

Between prover and on-chain verifier an aggregation infrastructure layer has emerged that the seven-layer model does not account for. Batching 100 proofs into a single on-chain verification reduces per-proof cost from ~$1 to ~$0.01, but centralized aggregators are single points of failure that reintroduce trust assumptions at the same layer they appear to solve.

## Key claims

- SHARP (StarkWare/Starknet): multiple applications submit traces; single STARK proof covers all, wrapped in Groth16; gas cost amortized across participants.
- Aligned Layer: launched with >$11B restaked ETH (EigenLayer); provides verification-as-a-service across rollups and applications.
- NEBRA (live August 2024): universal aggregation supporting Groth16, PLONK, and STARK in one layer.
- At 100-proof batches, per-proof verification cost drops from ~$1 to ~$0.01.
- Centralized aggregators (e.g., SHARP) are a single Layer 7 failure point that can undermine the proof system's decentralization guarantees.

## Entities

- [[groth16]]
- [[plonk]]
- [[starknet]]
- [[starks]]

## Dependencies

- [[ch08-the-price-of-a-verdict]] — the ~200K gas cost that aggregation amortizes
- [[ch08-the-social-layer]] — aggregation infrastructure as one of four Layer 7 concerns
- [[ch08-governance-the-achilles-heel]] — centralized aggregators need governance analysis analogous to verifier contracts

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

## Links

- Up: [[08-the-verdict]]
- Prev: [[ch08-governance-the-achilles-heel]]
- Next: [[ch08-case-study-midnight-and-the-three-token-architecture]]
