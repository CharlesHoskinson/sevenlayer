---
title: "Proof Aggregation: The Missing Layer"
slug: ch08-proof-aggregation-the-missing-layer
chapter: 8
chapter_title: "Layer 7 -- The Verdict"
heading_level: 2
source_lines: [3795, 3810]
source_commit: ae218cbb73ddecefb37373fa1c8e789e5b6f8f93
status: reviewed
word_count: 256
---

## Proof Aggregation: The Missing Layer

Between the prover (who generates proofs) and the on-chain verifier (who checks them), a significant infrastructure layer has emerged that the seven-layer model does not account for: proof aggregation services.

**SHARP (Shared Prover)**, built by StarkWare for Starknet, is the original aggregation service. Multiple applications submit their execution traces to SHARP, which generates a single STARK proof covering all of them, then wraps that proof in Groth16 for on-chain verification. The verification gas cost is amortized across all participating applications.

**Aligned Layer**, launched on mainnet with over $11 billion in restaked ETH (via EigenLayer), provides verification-as-a-service. Rollups and applications submit proofs to Aligned Layer, which batches and verifies them, posting the aggregated result to Ethereum.

**NEBRA**, live since August 2024, provides proof aggregation with a focus on universal verification -- supporting multiple proof systems (Groth16, PLONK, STARK) within a single aggregation layer.

The economic logic is straightforward. If a single Groth16 verification costs ~200,000 gas, and an aggregation service can batch 100 proofs into a single on-chain verification, the per-proof verification cost drops from ~$1 to ~$0.01. At sufficient volume, aggregation makes proof verification nearly free.

But aggregation introduces a new trust assumption. Users must trust that the aggregation service correctly includes their proof in the batch, and that the aggregated proof faithfully represents all constituent proofs. If the aggregation service is centralized (as SHARP is for Starknet), this is a single point of failure at Layer 7 that can undermine the decentralization guarantees of the underlying proof system.

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

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P2] (B) No sources cited for any of the three named aggregation services (SHARP, Aligned Layer, NEBRA); the Aligned Layer ">$11B restaked ETH" figure and NEBRA "live August 2024" date are unanchored.
- [P2] (E) Section does not explain how aggregation fits (or fails to fit) the seven-layer model beyond a single sentence; the trust-analysis of the aggregation layer is thin relative to the governance section's depth.

## Links

- Up: [[08-the-verdict]]
- Prev: [[ch08-governance-the-achilles-heel]]
- Next: [[ch08-case-study-midnight-and-the-three-token-architecture]]
