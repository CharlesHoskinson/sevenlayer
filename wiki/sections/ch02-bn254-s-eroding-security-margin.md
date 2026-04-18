---
title: "BN254's Eroding Security Margin"
slug: ch02-bn254-s-eroding-security-margin
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [661, 673]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 289
---

## BN254's Eroding Security Margin

There is a more immediate security concern than quantum computers, and it affects the most widely deployed curve in the ZK ecosystem.

BN254 (also called alt_bn128 or BN128) is the curve hardcoded into Ethereum's elliptic curve precompile opcodes. Every Groth16 proof verified on Ethereum's base layer uses BN254. But the estimated security of BN254 has been eroding. The Tower Number Field Sieve (Tower NFS) -- a family of discrete log algorithms that exploits the tower structure of extension fields -- has reduced BN254's estimated security from 128 bits to approximately 100 bits [Kim, Barbulescu, 2016; Menezes, Sarkar, Singh, 2016].

One hundred bits of security is not broken. But it sits below the 128-bit threshold that NIST mandates for new cryptographic deployments. The ZK ecosystem has been slowly migrating from BN254 to BLS12-381, which provides a comfortable 128-bit security margin even under Tower NFS analysis. Migration is slow, though: existing smart contracts reference the BN254 precompile directly, and changing the curve means changing the verification logic, which means upgrading every contract that verifies proofs.

The setup layer casts a long shadow. Choices made at Layer 1 -- which curve, which parameters, which ceremony -- propagate forward through years or decades of deployment. The curve choice that was state-of-the-art in 2018 shows its age by 2026. The ceremony that was sufficient in 2023 may be insufficient by 2035. Building the stage is not a one-time act. It is a commitment with a time horizon.

BN254's erosion shows that setup choices degrade over time. But even at the moment of creation, how do you judge whether a ceremony was conducted well enough to trust? The question is not just mathematical -- it is organizational, procedural, and archival.



## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
