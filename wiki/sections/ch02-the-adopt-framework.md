---
title: "The ADOPT Framework"
slug: ch02-the-adopt-framework
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [674, 690]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 265
---

## The ADOPT Framework

The most comprehensive survey of trusted setup ceremonies, the SoK paper by Wang, Cohney, and Bonneau [Wang, Cohney, Bonneau, 2025], catalogs over forty real-world ceremonies and evaluates them against five properties (the ADOPT framework):

- **A**vailable: Can anyone access and verify the SRS?
- **D**ecentralized: Is there a single coordinator who could manipulate the ceremony?
- **O**pen: Can anyone participate without permission?
- **P**ersistent: Will the ceremony data survive long-term for auditing?
- **T**ransparent: Is every step of the ceremony publicly observable?

Their finding: *no existing ceremony satisfies all five properties*. The Ethereum KZG ceremony scores well on openness and availability but still relied on a coordinating entity (the Ethereum Foundation). Many older ceremonies fail on persistence -- the intermediate transcript data for projects like Hermez has already become unrecoverable just a few years later.

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

- [P1] (A) The section claims Hermez transcript data "has already become unrecoverable" — this is a strong factual claim with no source. The Wang, Cohney, Bonneau 2025 paper should be cited for this specific finding, and the claim should be qualified (e.g., "as of 2024" or "per the authors' investigation").
- [P2] (B) The Wang, Cohney, Bonneau 2025 citation lacks venue; this is a SoK-style paper and should reference its conference (likely IEEE S&P or similar) once published, or the ePrint number.
- [P2] (C) The ADOPT acronym expansion is presented as a list, which is clear, but the paragraph "Their finding: no existing ceremony satisfies all five properties" uses a leading italicization pattern that borders on the numbered-proof-step style warned against in style guidelines.
- [none] (D) No contradictions found.
- [P3] (E) The section does not discuss which ADOPT properties Zcash Sprout or Sapling scored on/failed — applying the framework retroactively to those ceremonies would give the reader a richer comparative picture.

## Links

- Up: [[02-building-the-stage]]
- Prev: [[ch02-bn254-s-eroding-security-margin]]
- Next: [[ch02-midnight-s-bls12-381-stage]]
