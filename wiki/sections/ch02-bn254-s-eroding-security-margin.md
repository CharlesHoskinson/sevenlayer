---
title: "BN254's Eroding Security Margin"
slug: ch02-bn254-s-eroding-security-margin
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [651, 663]
source_commit: 53f41415d307dcd4ed73d852dfd6aa97146e882f
status: reviewed
word_count: 289
---

## BN254's Eroding Security Margin

There is a more immediate security concern than quantum computers, and it affects the most widely deployed curve in the ZK ecosystem.

BN254 (also called alt_bn128 or BN128) is the curve hardcoded into Ethereum's elliptic curve precompile opcodes. Every Groth16 proof verified on Ethereum's base layer uses BN254. But the estimated security of BN254 has been eroding. The Tower Number Field Sieve (Tower NFS) -- a family of discrete log algorithms that exploits the tower structure of extension fields -- cut BN254's estimated security from 128 bits toward roughly 100 bits in the 2016 round of analysis [Kim, Barbulescu, "Extended Tower Number Field Sieve: A New Complexity for the Medium Prime Case," *CRYPTO 2016* / IACR ePrint 2015/1027; Menezes, Sarkar, Singh, "Challenges with Assessing the Impact of NFS Advances on the Security of Pairing-Based Cryptography," *MathCrypt 2016*]. Barbulescu and Duquesne refined the Tower NFS analysis for pairing-friendly curves in 2017-2019 and proposed updated key-size recommendations; on their numbers, BN254 sits at approximately 100-110 bits of security [Barbulescu, Duquesne, "Updating Key Size Estimations for Pairings," *Journal of Cryptology* 32:1298-1336, 2019; HAL preprint hal-01534101, 2017].

One hundred-odd bits of security is not broken. But it sits below the 128-bit threshold that NIST mandates for new cryptographic deployments. The ZK ecosystem has been slowly migrating from BN254 to BLS12-381, which provides a comfortable 128-bit security margin even under Tower NFS analysis. Migration is slow, though: existing smart contracts reference the BN254 precompile directly, and changing the curve means changing the verification logic, which means upgrading every contract that verifies proofs.

The setup layer casts a long shadow. Choices made at Layer 1 -- which curve, which parameters, which ceremony -- propagate forward through years or decades of deployment. The curve choice that was state-of-the-art in 2018 shows its age by 2026. The ceremony that was sufficient in 2023 may be insufficient by 2035. Building the stage is not a one-time act. It is a commitment with a time horizon.

BN254's erosion shows that setup choices degrade over time. But even at the moment of creation, how do you judge whether a ceremony was conducted well enough to trust? The question is not just mathematical -- it is organizational, procedural, and archival.



## Summary

BN254, hardcoded into Ethereum's elliptic curve precompile and used by every Groth16 proof verified on-chain, has had its estimated security reduced from 128 bits to approximately 100 bits by the Tower Number Field Sieve attack. This sits below NIST's 128-bit mandate for new deployments, driving a slow ecosystem migration to BLS12-381. Setup choices propagate forward for years: the curve that was state-of-the-art in 2018 shows its age by 2026.

## Key claims

- BN254 (alt_bn128/BN128) is hardcoded into Ethereum's elliptic curve precompile; every Groth16 on-chain verification uses it.
- Tower NFS reduced BN254's estimated security from 128 bits to ~100 bits (Kim, Barbulescu, 2016; Menezes, Sarkar, Singh, 2016).
- 100-bit security is not broken but falls below NIST's 128-bit threshold for new deployments.
- BLS12-381 provides a comfortable 128-bit security margin even under Tower NFS analysis.
- Migration is slow: existing contracts reference the BN254 precompile directly; changing the curve requires upgrading every verifying contract.

## Entities

- [[bls12-381]]
- [[bn254]]
- [[ceremony]]
- [[groth16]]
- [[nist]]

## Dependencies

- [[ch02-the-quantum-shelf-life]] — broader context of how setup choices degrade over time
- [[ch02-the-structured-reference-string]] — the SRS is what is built on top of the curve

## Sources cited

- Kim, Barbulescu, 2016 (Tower NFS analysis of BN254)
- Menezes, Sarkar, Singh, 2016 (Tower NFS analysis of BN254)

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [none] (C) No AI-smell or style issues. The section is notably concise and well-written.
- [none] (D) No contradictions with other chapters found.
- [P3] (E) The section could note that Ethereum's EIP-2537 proposal adds BLS12-381 precompiles to Ethereum's base layer, which would directly address the migration barrier described; this is directly relevant to the "changing the curve requires upgrading every verifying contract" point.

## Links

- Up: [[02-building-the-stage]]
- Prev: [[ch02-the-quantum-shelf-life]]
- Next: [[ch02-the-adopt-framework]]
