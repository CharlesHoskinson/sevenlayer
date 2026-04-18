---
title: "Open Problems"
slug: ch09-open-problems
chapter: 9
chapter_title: "Privacy-Enhancing Technologies"
heading_level: 2
source_lines: [4294, 4305]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 252
---

## Open Problems

Three capabilities sit at the frontier of PET research and will likely shape the next generation of privacy architectures:

**Verifiable FHE**: Proving in zero knowledge that an FHE computation was performed correctly. This closes the loop in the healthcare scenario: the AI firm not only computes on encrypted data but also proves that it computed *correctly* on the encrypted data. The surgeon not only operates through the glovebox -- she provides a certificate that the operation was performed to specification. The zkFHE project and SherLOCKED prototype (using RISC Zero's Bonsai zkVM) are early implementations.

**Collaborative/threshold proving**: Distributing ZK proof generation across multiple servers using MPC, so that no single server sees the full witness. The work by Ozdemir and Boneh (USENIX Security 2022) and subsequent improvements in 2024 demonstrate that proof generation itself can be privacy-preserving. This creates a fifth proving model -- between client-side (private but expensive) and delegated (cheap but witness-exposing) -- that combines the privacy of the former with the performance of the latter. The magician's backstage preparation is distributed across multiple locked rooms. No single stagehand sees the whole act.

**Private Information Retrieval (PIR)**: Querying a database without revealing which record you are accessing. A client-side prover in a private rollup (like Aztec) needs to retrieve encrypted notes from the network without revealing which notes belong to them. Recent advances at EUROCRYPT 2026 achieved information-theoretic PIR with sublinear server time and quasilinear space, moving PIR from theoretical curiosity toward practical deployment for billion-entry databases.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
