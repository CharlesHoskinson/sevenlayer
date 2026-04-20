---
title: "The Decision Matrix"
slug: ch09-the-decision-matrix
chapter: 9
chapter_title: "Privacy-Enhancing Technologies"
heading_level: 2
source_lines: [4282, 4312]
source_commit: 4b160057932dbd587dab82f3fc1ddfa36f581a79
status: reviewed
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

A four-question framework for selecting PETs: trust model (information-theoretic vs. computational vs. heuristic), data ownership (single holder vs. multi-party vs. outsourced vs. aggregate), acceptable performance, and applicable regulatory regime. No single PET answers all four; the answer is almost always a composed stack.

## Key claims

- Trust model: MPC honest-majority → information-theoretic; ZKP/FHE → computational; TEE → heuristic.
- Data ownership: prove a property → ZKP; joint multi-party compute → MPC; untrusted third-party compute → FHE; aggregate statistics → DP.
- Performance: ZKP proving seconds–minutes, verification milliseconds; MPC bottleneck is communication rounds; FHE 10,000–1,000,000× overhead; DP negligible; TEE <5% overhead.
- GDPR/eIDAS 2.0 regime: ZKP selective disclosure, off-chain storage + on-chain hash, right-to-erasure compatible.
- Financial regulation (AML/KYC): zKYC, Privacy Pools, MPC for inter-institutional analysis.
- Healthcare (HIPAA, EU Clinical Trials Regulation): MPC for multi-site, DP for statistical releases, FHE for outsourced AI training.

## Entities

- [[fhe]]
- [[mpc]]
- [[zkps]]

## Dependencies

- [[ch09-the-four-pillars]] — performance and trust model data for each PET
- [[ch09-three-kinds-of-security]] — trust model taxonomy
- [[ch09-the-regulatory-intersection]] — regulatory regime detail (GDPR, eIDAS 2.0)
- [[ch09-composability-when-one-pet-is-not-enough]] — composition as the expected answer

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P2] (A) "TEE: near-native performance (<5% overhead for many workloads)" conflicts with the section's own ch09-three-kinds-of-security, which reports Downfall mitigations causing up to 50% degradation for affected workloads. The figure is accurate only for unaffected workloads; the caveat should be stated.
- [P2] (B) No sources cited throughout; the entire matrix synthesises claims from prior sections but offers no anchoring references for the performance figures or regulatory mappings.

## Links

- Up: [[09-privacy-enhancing-technologies]]
- Prev: [[ch09-the-regulatory-intersection]]
- Next: [[ch09-open-problems]]
