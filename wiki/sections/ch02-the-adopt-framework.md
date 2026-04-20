---
title: "The ADOPT Framework"
slug: ch02-the-adopt-framework
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [664, 682]
source_commit: 6e757843ed29aa50ce4558719452a86510ed0d20
status: finalized
word_count: 265
---

## The ADOPT Framework

The most comprehensive survey of trusted setup ceremonies, the SoK paper by Wang, Cohney, and Bonneau [Wang, Cohney, Bonneau, "SoK: Trusted Setups for Powers-of-Tau Strings," *Financial Cryptography 2025* / IACR ePrint 2025/064], catalogs over forty real-world ceremonies and evaluates them against five properties (the ADOPT framework):

- **A**vailable: Can anyone access and verify the SRS?
- **D**ecentralized: Is there a single coordinator who could manipulate the ceremony?
- **O**pen: Can anyone participate without permission?
- **P**ersistent: Will the ceremony data survive long-term for auditing?
- **T**ransparent: Is every step of the ceremony publicly observable?

No existing ceremony satisfies all five properties. Applying the framework retrospectively to the earlier Zcash ceremonies sharpens the picture. The Sprout ceremony (2016) scores poorly on openness (six invited participants), decentralization (a single coordinating team), and persistence (hardware destroyed, intermediate transcripts not archived). It scores better on availability (the final SRS was published) but fails transparency -- the ceremony pre-dates the norms of public audit trails. The Sapling ceremony (2018) improves on openness (roughly ninety participants) and transparency (the BGM17 protocol was published), but still relied on a central coordinator and saw some intermediate data lost. The Ethereum KZG ceremony (2023) scores well on openness and availability, but still relied on a coordinating entity (the Ethereum Foundation) for decentralization, and time will tell whether its transcripts remain accessible.

Many older ceremonies fail on persistence -- as of the SoK's investigation, intermediate transcript data for projects including Hermez had already become unrecoverable just a few years after the ceremony ended [Wang, Cohney, Bonneau, 2025].

This is not a failure of any specific project. It is a structural limitation of the ceremony model. Ceremonies are social events, and social events are messy. The gap between the abstract "1-of-N honest participant" security model and the operational reality of running a ceremony with hundreds of thousands of participants -- each using different hardware, different software, different randomness sources, across different jurisdictions -- is wide. The protocol can be mathematically perfect. The ceremony is always imperfect.

The transparent alternative -- STARKs, hash-based commitments, no ceremony at all -- avoids this entire problem class. There is no ceremony to evaluate, no transcript to preserve, no coordinator to trust. The cost is measured in proof size and verification time, not in coordination complexity and social trust.



## Summary

Wang, Cohney, and Bonneau's SoK survey of 40+ real-world ceremonies defines five ADOPT properties (Available, Decentralized, Open, Persistent, Transparent) and finds that no existing ceremony satisfies all five. The Ethereum KZG ceremony scores well on openness and availability but still relied on an Ethereum Foundation coordinator; many older ceremonies already fail on persistence, with transcript data becoming unrecoverable within years. Transparent setups (STARKs) avoid the entire problem class by having no ceremony to evaluate.

## Key claims

- The ADOPT framework has five properties: Available, Decentralized, Open, Persistent, Transparent.
- No existing ceremony satisfies all five properties (Wang, Cohney, Bonneau, 2025).
- Ethereum KZG: passes on openness and availability; fails decentralization (Ethereum Foundation coordinator).
- Many older ceremonies already fail persistence — e.g., Hermez transcript data is already unrecoverable.
- Transparent setups trade proof size and verification time for total elimination of ceremony coordination risk.

## Entities

- [[ceremony]]
- [[kzg]]
- [[starks]]

## Dependencies

- [[ch02-two-ways-to-build-a-stage]] — establishes both paths being evaluated
- [[ch02-the-141-416-person-question]] — the sociological dimension of why ceremony quality is hard to guarantee

## Sources cited

- Wang, Cohney, Bonneau, 2025 (SoK on trusted setup ceremonies, ADOPT framework)

## Open questions

None flagged by this section.

## Improvement notes

_All P0/P1/P2/P3 findings resolved in Phase 3 revisions (2026-04-18 through 2026-04-20)._

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [none] (D) No contradictions found.

## Links

- Up: [[02-building-the-stage]]
- Prev: [[ch02-bn254-s-eroding-security-margin]]
- Next: [[ch02-midnight-s-bls12-381-stage]]
