---
title: "Real-World Deployments: Five Case Studies"
slug: ch09-real-world-deployments-five-case-studies
chapter: 9
chapter_title: "Privacy-Enhancing Technologies"
heading_level: 2
source_lines: [4141, 4180]
source_commit: b3ed881318761d3fd0e65ead7ea58e3f6536ccf9
status: reviewed
word_count: 806
---

## Real-World Deployments: Five Case Studies

### 1. Decentriq and the Swiss National Bank

In a federal pilot project beginning in 2021-2022, data clean room technology enabled encrypted collaboration between the Swiss National Bank, SIX (Switzerland's financial market infrastructure provider), and Zurich Cantonal Bank. The goal was cybersecurity threat detection: analyzing patterns of suspicious financial activity across institutions without any institution revealing its transaction data to the others.

The architecture used MPC-style computation within Decentriq's confidential computing platform, combining software-level privacy guarantees with hardware TEEs. The result demonstrated that financial regulators can gain systemic risk visibility without requiring banks to share raw transaction data -- a significant precedent for privacy-preserving financial regulation. The regulator sees the pattern. The banks keep the data. Everyone sleeps better.

### 2. DTCC and the Canton Network

The Depository Trust and Clearing Corporation (DTCC), which processes virtually all US securities transactions, partnered with Digital Asset's Canton Network in December 2025 to tokenize US Treasuries on a permissioned blockchain with privacy-preserving settlement. The architecture uses the Canton protocol's built-in privacy model, where participants see only the portions of the ledger relevant to them.

This deployment matters because of who is adopting. DTCC is not a startup experimenting with privacy. It is the backbone of US securities infrastructure, processing trillions of dollars annually. When DTCC chooses a privacy-preserving architecture, it signals that privacy is not a nice-to-have feature but a regulatory and competitive necessity. The largest financial plumbing system in the world has decided it needs these tools. Pay attention.

### 3. Partisia and Toppan Edge: Digital Student IDs

Toppan Edge and Partisia announced joint development of privacy-preserving digital student IDs in 2025, with a proof-of-concept conducted at the Okinawa Institute of Science and Technology from June to September 2025. The system combines facial recognition for identity verification, decentralized identifiers (DIDs) for credential management, smartphone NFC for physical access, and MPC via Partisia's blockchain for privacy-preserving identity verification.

The architectural move: the student's biometric data is never stored in a single location or revealed to a single party. MPC ensures that identity verification can be performed without any single server holding the student's facial template. The platform is targeted for students enrolling from April 2026. Your face opens the door, but no one holds a copy of your face.

### 4. Privacy Pools: Pragmatic On-Chain Privacy

Privacy Pools, co-authored by Vitalik Buterin and implemented by 0xbow, launched on Ethereum mainnet on April 1, 2025. Buterin was one of the first users, depositing 1 ETH.

The design addresses the fundamental tension between on-chain privacy and regulatory compliance -- a tension that destroyed Tornado Cash and haunts every privacy protocol. Users deposit funds into a pool and can later withdraw them, breaking the link between deposit and withdrawal addresses (similar to Tornado Cash). But Privacy Pools add a compliance layer: an Association Set Provider (ASP) screens deposits for connections to sanctioned or illicit addresses, and the zero-knowledge proof used for withdrawal includes a proof that the user's funds are drawn from a compliant "association set."

The result is "pragmatic privacy" -- transaction privacy for legitimate users, with a built-in compliance mechanism that prevents sanctioned funds from mixing with clean funds. As of early 2026, Privacy Pools has processed over $6 million in volume across more than 1,500 users. The broader ecosystem includes more than 35 teams pursuing approximately 13 distinct approaches to private transfers on Ethereum. The magician proves she is not cheating -- and the regulator is satisfied.

### 5. Apple, Google, and the US Census Bureau: Differential Privacy at Scale

The largest PET deployments in the world are not blockchain systems. They are not even close. They are differential privacy systems serving billions of users:

- **Apple** introduced DP in iOS 10 (2016) for emoji usage statistics, Safari search queries, HealthKit data, and keyboard autocorrect improvements. Each device adds local noise before transmitting data, with $\varepsilon = 2$ per day for most data types.
- **Google** deployed RAPPOR for Chrome settings monitoring, adding randomized responses to usage data before aggregation.
- **US Census Bureau** used the TopDown Algorithm for the 2020 Census, adding calibrated noise to census statistics at every geographic level. The decision was motivated by a concrete threat: the Dinur-Nissim reconstruction theorem proved that releasing too many exact statistics from a dataset eventually allows full reconstruction of individual records.

These deployments demonstrate that differential privacy is the only PET to have achieved planetary-scale adoption. ZKPs, MPC, and FHE remain orders of magnitude smaller in deployment footprint. For the system architect, this suggests that DP should be the first tool considered for statistical data release, with the other PETs reserved for use cases that require computation on raw data or verifiable individual claims. The fog machine is the most popular tool in the privacy toolkit. The magic wand is catching up.

---


## Summary

Five case studies spanning finance, identity, on-chain privacy, and telemetry illustrate the deployment breadth of PETs. DP is the only PET at planetary scale (Apple, Google, US Census); ZKP-based Privacy Pools launched on Ethereum mainnet April 1, 2025, processing over $6 million and 1,500+ users by early 2026 as a compliance-aware answer to Tornado Cash.

## Key claims

- Decentriq/Swiss National Bank pilot (2021–2022): MPC + hardware TEE for cross-institution cybersecurity threat detection without raw data sharing.
- DTCC partnered with Digital Asset's Canton Network in December 2025 to tokenize US Treasuries on a privacy-preserving permissioned blockchain.
- Toppan Edge + Partisia digital student IDs: MPC ensures biometric data is never held by a single party; PoC at OIST June–September 2025, deployment targeted April 2026.
- Privacy Pools (Vitalik Buterin co-author, 0xbow implementation): launched Ethereum mainnet April 1, 2025; uses Association Set Provider (ASP) ZK compliance proofs; >$6M volume, >1,500 users by early 2026.
- Apple DP: iOS 10 (2016), ε = 2/day most data types; Google RAPPOR: randomized response for Chrome usage.
- US Census Bureau 2020 TopDown Algorithm: first national-scale DP deployment, motivated by Dinur-Nissim reconstruction theorem.
- DP has orders-of-magnitude greater deployment footprint than ZKPs, MPC, or FHE.

## Entities

- [[mpc]]
- [[nova]]
- [[tornado cash]]
- [[zkps]]

## Dependencies

- [[ch09-the-four-pillars]] — introduces the PETs instantiated in these case studies
- [[ch09-the-regulatory-intersection]] — Privacy Pools directly addresses the regulatory tension explored there
- [[ch08-governance-the-achilles-heel]] — Tornado Cash governance/regulatory context
- [[ch09-the-decision-matrix]] — case studies are evidence for DP-first recommendation for statistical releases

## Sources cited

- Decentriq / Swiss National Bank pilot project (2021–2022).
- DTCC + Digital Asset Canton Network partnership announcement (December 2025).
- Toppan Edge + Partisia digital student ID announcement (2025); OIST proof-of-concept (June–September 2025).
- Buterin, V. et al. Privacy Pools. Launched Ethereum mainnet April 1, 2025.
- Apple iOS 10 differential privacy (2016).
- Google RAPPOR deployment.
- US Census Bureau 2020 Census TopDown Algorithm.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P3] (B) Privacy Pools volume figures (">$6 million, >1,500 users by early 2026") are specific claims with no URL or source; a reference to 0xbow's published stats or an Etherscan link should be added.

## Links

- Up: [[09-privacy-enhancing-technologies]]
- Prev: [[ch09-composability-when-one-pet-is-not-enough]]
- Next: [[ch09-privacy-architectures-for-smart-contracts-kachina-and-zexe]]
