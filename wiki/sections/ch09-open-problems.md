---
title: "Open Problems"
slug: ch09-open-problems
chapter: 9
chapter_title: "Privacy-Enhancing Technologies"
heading_level: 2
source_lines: [4292, 4303]
source_commit: 53f41415d307dcd4ed73d852dfd6aa97146e882f
status: reviewed
word_count: 252
---

## Open Problems

Three capabilities sit at the frontier of PET research and will likely shape the next generation of privacy architectures:

**Verifiable FHE**: Proving in zero knowledge that an FHE computation was performed correctly. This closes the loop in the healthcare scenario: the AI firm not only computes on encrypted data but also proves that it computed *correctly* on the encrypted data. The surgeon not only operates through the glovebox -- she provides a certificate that the operation was performed to specification. The zkFHE project and SherLOCKED prototype (using RISC Zero's Bonsai zkVM) are early implementations.

**Collaborative/threshold proving**: Distributing ZK proof generation across multiple servers using MPC, so that no single server sees the full witness. The work by Ozdemir and Boneh, "Experimenting with Collaborative zk-SNARKs: Zero-Knowledge Proofs for Distributed Secrets," USENIX Security 2022 (ePrint 2021/1530), and subsequent improvements in 2024 demonstrate that proof generation itself can be privacy-preserving. This creates a fifth proving model -- between client-side (private but expensive) and delegated (cheap but witness-exposing) -- that combines the privacy of the former with the performance of the latter. The magician's backstage preparation is distributed across multiple locked rooms. No single stagehand sees the whole act.

**Private Information Retrieval (PIR)**: Querying a database without revealing which record you are accessing. A client-side prover in a private rollup (like Aztec) needs to retrieve encrypted notes from the network without revealing which notes belong to them. Recent results presented at EUROCRYPT 2026 claimed information-theoretic PIR with sublinear server time and quasilinear space -- a result that, if confirmed, would move PIR from theoretical curiosity toward practical deployment for billion-entry databases. The specific paper had not been formally published at time of writing; treat these benchmarks as provisional pending peer review.

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

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

## Links

- Up: [[09-privacy-enhancing-technologies]]
- Prev: [[ch09-the-decision-matrix]]
- Next: [[ch09-the-incomplete-stack]]
