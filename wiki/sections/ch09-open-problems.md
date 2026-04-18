---
title: "Open Problems"
slug: ch09-open-problems
chapter: 9
chapter_title: "Privacy-Enhancing Technologies"
heading_level: 2
source_lines: [4294, 4305]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 252
---

## Open Problems

Three capabilities sit at the frontier of PET research and will likely shape the next generation of privacy architectures:

**Verifiable FHE**: Proving in zero knowledge that an FHE computation was performed correctly. This closes the loop in the healthcare scenario: the AI firm not only computes on encrypted data but also proves that it computed *correctly* on the encrypted data. The surgeon not only operates through the glovebox -- she provides a certificate that the operation was performed to specification. The zkFHE project and SherLOCKED prototype (using RISC Zero's Bonsai zkVM) are early implementations.

**Collaborative/threshold proving**: Distributing ZK proof generation across multiple servers using MPC, so that no single server sees the full witness. The work by Ozdemir and Boneh (USENIX Security 2022) and subsequent improvements in 2024 demonstrate that proof generation itself can be privacy-preserving. This creates a fifth proving model -- between client-side (private but expensive) and delegated (cheap but witness-exposing) -- that combines the privacy of the former with the performance of the latter. The magician's backstage preparation is distributed across multiple locked rooms. No single stagehand sees the whole act.

**Private Information Retrieval (PIR)**: Querying a database without revealing which record you are accessing. A client-side prover in a private rollup (like Aztec) needs to retrieve encrypted notes from the network without revealing which notes belong to them. Recent advances at EUROCRYPT 2026 achieved information-theoretic PIR with sublinear server time and quasilinear space, moving PIR from theoretical curiosity toward practical deployment for billion-entry databases.

---


## Summary

Three frontier capabilities likely to define the next privacy architecture generation: verifiable FHE (zkFHE, closing the integrity gap for encrypted computation), collaborative/threshold ZK proving via MPC (no single server holds the full witness), and Private Information Retrieval (querying a database without revealing which record was accessed). EUROCRYPT 2026 advances moved PIR toward practical deployment for billion-entry databases.

## Key claims

- zkFHE: ZK proof that FHE computation was performed correctly; SherLOCKED prototype uses RISC Zero's Bonsai zkVM.
- Collaborative proving (Ozdemir and Boneh, USENIX Security 2022; improvements 2024): proof generation distributed across MPC servers — a fifth proving model combining client privacy with delegated performance.
- PIR advances at EUROCRYPT 2026: information-theoretic PIR with sublinear server time and quasilinear space.
- PIR relevance: Aztec client-side provers need to retrieve encrypted notes without revealing ownership.

## Entities

- [[boneh]]
- [[fhe]]
- [[mpc]]

## Dependencies

- [[ch09-composability-when-one-pet-is-not-enough]] — zkFHE introduced as active research frontier there
- [[ch09-the-four-pillars]] — FHE integrity gap motivates zkFHE
- [[ch09-privacy-architectures-for-smart-contracts-kachina-and-zexe]] — Aztec note retrieval as PIR use case

## Sources cited

- Ozdemir, A., Boneh, D. Experimenting with Collaborative zk-SNARKs. USENIX Security 2022.
- EUROCRYPT 2026: information-theoretic PIR with sublinear server time and quasilinear space (specific paper not named in text).
- zkFHE / SherLOCKED prototype using RISC Zero Bonsai zkVM.

## Open questions

- zkFHE beyond toy circuits remains an open research problem.
- Collaborative proving performance improvements post-2024 not yet production-deployed.
- PIR at billion-entry scale: practical deployment conditions not yet established.

## Improvement notes

## Links

- Up: [[09-privacy-enhancing-technologies]]
- Prev: [[ch09-the-decision-matrix]]
- Next: [[ch09-the-incomplete-stack]]
