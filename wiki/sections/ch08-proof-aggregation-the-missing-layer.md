---
title: "Proof Aggregation: The Missing Layer"
slug: ch08-proof-aggregation-the-missing-layer
chapter: 8
chapter_title: "Layer 7 -- The Verdict"
heading_level: 2
source_lines: [3781, 3796]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
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

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
