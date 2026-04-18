---
title: "The Decision Matrix"
slug: ch09-the-decision-matrix
chapter: 9
chapter_title: "Privacy-Enhancing Technologies"
heading_level: 2
source_lines: [4263, 4293]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 280
---

## The Decision Matrix

For the system architect who needs to choose a PET (or a combination of PETs), the decision depends on four questions:

**1. What is the trust model?**
- If you need privacy against computationally unbounded adversaries (including future quantum computers): MPC with honest majority provides information-theoretic security.
- If you trust computational hardness assumptions: ZKPs and FHE provide computational security.
- If you trust hardware manufacturers: TEEs provide heuristic security with high performance.

**2. Who has the data?**
- If the data holder needs to prove a property: ZKP (selective disclosure).
- If multiple parties need to compute on their combined data: MPC (collaborative computation).
- If the data needs to be processed by an untrusted third party: FHE (encrypted outsourcing).
- If aggregate statistics need to be released from a dataset: DP (statistical disclosure control).

**3. What performance is acceptable?**
- ZKP proof generation: seconds to minutes. Verification: milliseconds.
- MPC: communication rounds proportional to circuit depth. Latency is the bottleneck.
- FHE: 10,000-1,000,000x overhead over plaintext. Improving rapidly, but still orders of magnitude slower.
- DP: negligible overhead (adding noise to query results is cheap).
- TEE: near-native performance (<5% overhead for many workloads).

**4. What regulatory regime applies?**
- GDPR/eIDAS 2.0: Selective disclosure (ZKP), off-chain storage with on-chain hashing, right-to-erasure compatibility.
- Financial regulation (AML/KYC): zKYC (ZKP for compliance proofs), Privacy Pools (ZKP for provenance), MPC for inter-institutional analysis.
- Healthcare (HIPAA, EU Clinical Trials Regulation): MPC for multi-site computation, DP for statistical releases, FHE for outsourced AI model training.

No single PET answers all four questions. The art is in composition -- and the engineering is in the handoffs between them.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
