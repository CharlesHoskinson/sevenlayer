---
title: "Real-Time Ethereum Proving"
slug: ch06-real-time-ethereum-proving
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2779, 2796]
source_commit: b3ed881318761d3fd0e65ead7ea58e3f6536ccf9
status: reviewed
word_count: 385
---

## Real-Time Ethereum Proving

The performance revolution in proof systems has had a direct economic consequence worth pausing to appreciate, because it changes the fundamental calculus of what this technology is good for.

In December 2023, proving a single Ethereum block cost approximately $80.21. By December 2025, the cost had fallen to roughly $0.04 -- a 2,000x reduction in 24 months. Airbender (ZKsync's prover) achieved $0.0001 per transfer. These numbers come from CastleLabs and Ethproofs benchmarks [43, 44], and they represent a cost curve steeper than Moore's Law.

But cost is only half the story. Speed matters equally, because Ethereum produces a new block every 12 seconds. If proving takes longer than 12 seconds, the prover cannot keep up with the chain. For years, this was a distant goal. In late 2025, at least two teams crossed the threshold with named, public results:

- **SP1 Hypercube** (Succinct Labs): Proved 99.7% of Ethereum Layer 1 blocks in under 12 seconds, using 16 NVIDIA RTX 5090 GPUs (hardware cost approximately $32,000). SP1 Hypercube uses a multilinear polynomial stack built on the sumcheck protocol, with a "jagged" polynomial commitment scheme that enables pay-per-use proving. (The system also uses a STARK wrapper for intermediate recursion and Groth16 for on-chain posting; "sumcheck-based" refers to the core polynomial arithmetic layer, not to the exclusion of these outer stages.)

- **ZKsync Airbender**: Achieved 21.8 million cycles per second on a single H100 GPU, proving Ethereum blocks in approximately 35 seconds. Open-source, moving toward formal verification.

The Ethereum Foundation responded by declaring the speed race "operationally viable" in December 2025 and shifting its targets [Ethereum Foundation, "Ethereum proving roadmap update," December 2025]. The new requirements: less than 10 seconds per block, less than $100,000 in hardware, less than 10 kilowatts of power, 128-bit provable security, and proof sizes under 300 kilobytes. The pivot from speed to security signals that the raw performance problem, which dominated proof system research for five years, has been substantially solved. The next frontier is formal security guarantees -- a topic we will revisit in Chapter 7.

This cost drop matters for reasons beyond Ethereum. When proving costs $80, ZK proofs are a luxury -- viable only for high-value transactions or well-funded rollups. When proving costs four cents, ZK proofs become infrastructure -- cheap enough to apply to every transaction, every block, every state transition. The technology moves from "expensive security upgrade" to "default operating mode." That shift was enabled almost entirely by improvements at Layer 5.

---


## Summary

Ethereum block proving cost fell from $80.21 (December 2023) to $0.04 (December 2025) -- a 2,000x reduction. By late 2025, SP1 Hypercube proved 99.7% of blocks under 12 seconds (16 RTX 5090 GPUs); ZKsync Airbender proved blocks in ~35 seconds on one H100. The Ethereum Foundation declared the speed race won and pivoted to formal 128-bit security guarantees.

## Key claims

- Ethereum block proving: ~$80.21 in December 2023 → ~$0.04 in December 2025, 2,000x reduction (CastleLabs/Ethproofs).
- Airbender achieved $0.0001 per transfer.
- SP1 Hypercube: 99.7% of L1 blocks under 12 seconds on 16 NVIDIA RTX 5090 GPUs (~$32,000 hardware).
- ZKsync Airbender: 21.8 million cycles/second on a single H100; blocks in ~35 seconds.
- Ethereum Foundation December 2025 targets: <10 seconds/block, <$100K hardware, <10 kW power, 128-bit provable security, <300 KB proofs.
- The pivot from speed to security marks the end of the "speed race" as the dominant proving challenge.
- Cost threshold shift: from luxury ($80) to infrastructure ($0.04) changes ZK from optional to default.

## Entities

- [[nvidia]]
- [[h100]]
- [[airbender]]

## Dependencies

- [[ch06-circle-starks-and-stwo-a-generational-leap]] — Circle STARKs are the core technology enabling these benchmarks
- [[ch06-from-speed-race-to-security-race]] — the "speed race won" narrative continues directly in that section
- [[ch06-the-hybrid-pipeline]] — pipeline architecture enabling sub-$1 proving

## Sources cited

- CastleLabs benchmarks, December 2023 and December 2025.
- Ethproofs benchmarks, December 2025.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P3] (E) Very short section (385 words); the pivot from speed to security is stated but not developed — that development is delegated entirely to ch06-from-speed-race-to-security-race, but the handoff could name the specific formal-verification milestone (SP1's 62-opcode check) to give readers a concrete anchor before the next section

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-circle-starks-and-stwo-a-generational-leap]]
- Next: [[ch06-the-proof-core-why-layers-4-5-and-6-are-inseparable]]
