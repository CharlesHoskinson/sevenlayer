---
title: "The ADOPT Framework"
slug: ch02-the-adopt-framework
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [674, 690]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
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

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
