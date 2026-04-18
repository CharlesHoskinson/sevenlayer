---
title: "Real-Time Ethereum Proving"
slug: ch06-real-time-ethereum-proving
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2786, 2805]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 385
---

## Real-Time Ethereum Proving

The performance revolution in proof systems has had a direct economic consequence worth pausing to appreciate, because it changes the fundamental calculus of what this technology is good for.

In December 2023, proving a single Ethereum block cost approximately $80.21. By December 2025, the cost had fallen to roughly $0.04 -- a 2,000x reduction in 24 months. Airbender (ZKsync's prover) achieved $0.0001 per transfer. These numbers come from CastleLabs and Ethproofs benchmarks, and they represent a cost curve steeper than Moore's Law.

But cost is only half the story. Speed matters equally, because Ethereum produces a new block every 12 seconds. If proving takes longer than 12 seconds, the prover cannot keep up with the chain. For years, this was a distant goal. In late 2025, four teams crossed the threshold:

- **SP1 Hypercube** (Succinct Labs): Proved 99.7% of Ethereum Layer 1 blocks in under 12 seconds, using 16 NVIDIA RTX 5090 GPUs (hardware cost approximately $32,000). SP1 Hypercube uses a multilinear polynomial stack built entirely on the sumcheck protocol, with a "jagged" polynomial commitment scheme that enables pay-per-use proving.

- **ZKsync Airbender**: Achieved 21.8 million cycles per second on a single H100 GPU, proving Ethereum blocks in approximately 35 seconds. Open-source, moving toward formal verification.

- **Two additional teams** from the Ethereum Foundation's proving ecosystem demonstrated sub-12-second proving under various hardware configurations.

The Ethereum Foundation responded by declaring the speed race "operationally viable" in December 2025 and shifting its targets. The new requirements: less than 10 seconds per block, less than $100,000 in hardware, less than 10 kilowatts of power, 128-bit provable security, and proof sizes under 300 kilobytes. The pivot from speed to security signals that the raw performance problem, which dominated proof system research for five years, has been substantially solved. The next frontier is formal security guarantees -- a topic we will revisit in Chapter 7.

This cost drop matters for reasons beyond Ethereum. When proving costs $80, ZK proofs are a luxury -- viable only for high-value transactions or well-funded rollups. When proving costs four cents, ZK proofs become infrastructure -- cheap enough to apply to every transaction, every block, every state transition. The technology moves from "expensive security upgrade" to "default operating mode." That shift was enabled almost entirely by improvements at Layer 5.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
