---
title: "Witness-Constraint Divergence"
slug: ch04-witness-constraint-divergence
chapter: 4
chapter_title: "The Secret Performance"
heading_level: 2
source_lines: [1455, 1488]
source_commit: b3ed881318761d3fd0e65ead7ea58e3f6536ccf9
status: reviewed
word_count: 843
---

## Witness-Constraint Divergence

The witness is not just the most expensive artifact in the ZK pipeline. It is also the most dangerous place for bugs.

Remember the dual-track problem from Chapter 3: in many ZK systems, the witness generator and the constraint system are two separate programs that must compute identical functions on all inputs. When they disagree, the result is either a soundness bug (the proof system accepts false statements) or a completeness bug (the proof system rejects true statements). Both are bad. Soundness bugs are worse.

Two real-world examples illustrate the stakes.

RISC Zero disclosed CVE-2025-52484: a missing constraint in the RISC-V circuit that allowed confusion between the rs1 and rs2 source-register operands. According to the GitHub security advisory, the circuit failed to constrain the case where a three-register RISC-V instruction named the same register for both source operands. The advisory identifies 3-register instructions generally -- the `remu` and `divu` instructions are cited as examples -- without naming a single instruction as the whole class. The witness generator computed the correct values for both registers; the constraint system did not enforce that rs1 and rs2 carried the same value when they referenced the same register. A malicious prover could substitute one register for another, and the proof would still verify. The computation would appear valid, but the result would be wrong. The fix shipped in risc0-zkvm 2.1.0.

The zkSync Era MemoryWriteQuery bug was worse. The struct that handled memory write operations failed to call `lc.enforce_zero(cs)` on the highest 128 bits of a 256-bit value, leaving those bits unconstrained. A malicious prover could modify the highest 128 bits of any memory write -- including withdrawal amounts. The proof system would accept the modification. An attacker could change a withdrawal of 0.00002 ETH to a withdrawal of 100,000 ETH, and the proof would verify.

These bugs share a common structure: the witness was correct, but the constraints were insufficient. The magician performed the trick honestly backstage, but the constraint system's description of what "honest" meant was incomplete. The proof certified that the computation matched the constraints. The constraints did not match the intended computation.

Call it the correctness gap: the distance between what the developer meant and what the constraints actually enforce. The zkSync bug illustrates the typical failure mode: the method enforcing the constraint existed but was never called. Missing constraints are not always missing code; they are sometimes code present but never invoked.

Multiple valid witnesses can exist for the same statement, and the proof system does not care which one the prover uses. If you prove that you know a square root of 25, the proof system accepts whether you use 5 or -5. This is by design -- the proof system guarantees soundness (you cannot prove a false statement), not uniqueness (there is only one valid witness).

This property -- that multiple valid witnesses exist -- is fundamental, not a bug. The proof system guarantees that the prover knows *some* valid witness. It does not guarantee which one. For most applications, this is exactly right: if you prove you know a valid password, it does not matter whether you know the first password in the hash table or the last.

Non-deterministic hints exploit this deliberately. Instead of computing a square root step by step -- which is expensive inside a circuit -- the prover *guesses* the answer (as a witness value) and the circuit verifies that the square of the guess equals 25. The computation goes from expensive (sequential square root algorithm) to cheap (one multiplication and one comparison). This "guess and check" pattern is a standard programming technique in ZK systems, not a bug. But it requires that the checking constraints are complete. If the check only verifies $x \cdot x = 25$ without constraining that $x$ is in the correct range, a malicious prover might find a field element that satisfies the equation but is not the intended square root.

### Closing the Correctness Gap

The correctness gap -- the distance between what the developer meant and what the constraints enforce -- is identified, but what do teams actually do about it?

The most common approach is *property-based testing*: generate thousands of random inputs, run them through both the witness generator and the constraint checker, and verify that the constraint system is satisfied for every valid witness and violated for every invalid one. This is the ZK equivalent of fuzzing. Takahashi, Kim, and collaborators built zkFuzz (IEEE S&P 2026, arXiv 2504.11961) to automate it against Circom; on 354 real-world circuits their tool identified 66 bugs including 38 zero-days, of which 18 were confirmed by developers and 6 were fixed for bug bounties. The limitation is coverage: random testing exercises the common cases but may miss the adversarial corner cases that matter most.

*Differential testing* takes a different angle. You implement the same computation twice -- once as a witness generator, once as an independent reference implementation -- and check that they agree on all inputs. If the constraint system accepts a witness that the reference implementation rejects, you have found a bug. This approach catches the class of errors where the witness generator and the constraint system silently diverge (the dominant failure mode in Circom).

*Formal verification* is the gold standard but remains aspirational for large circuits. NAVe (Ozdemir, Brown, and Bonneau, 2023; targeted at Noir) and Picus (Wen, Cheng, and Wang, CCS 2023; targeted at Circom) can verify properties of small to medium circuits automatically, but circuits with millions of constraints exceed current solver capacity. The combination of compile-time prevention (Compact's disclosure analysis, refinement types) and post-hoc verification (ZKAP's static analysis for under-constrained circuit detection -- F1 score 0.82 on that specific task -- and zkFuzz) could provide comprehensive coverage, but no production system achieves both today. This gap is one of the field's most important open problems.

---


## Summary

When the witness generator and the constraint system compute different functions, the result is either a soundness bug (false proofs accepted) or a completeness bug (true proofs rejected). Two real vulnerabilities illustrate the stakes: RISC Zero CVE-2025-52484 (unconstrained register operands) and zkSync Era's MemoryWriteQuery bug (unconstrained high 128 bits of a 256-bit write, potentially enabling arbitrary withdrawal inflation). Property-based testing, differential testing, and formal verification each close part of the gap; no production system achieves all three.

## Key claims

- RISC Zero CVE-2025-52484: missing constraint allowed rs1/rs2 register confusion; witness was correct, constraint system was not.
- zkSync Era MemoryWriteQuery: `lc.enforce_zero(cs)` not called on high 128 bits of a 256-bit value — a malicious prover could modify withdrawal amounts and the proof would still verify.
- Multiple valid witnesses can exist for the same statement; this is by design (soundness, not uniqueness).
- Non-deterministic hints ("guess and check") are valid but require complete checking constraints.
- zkFuzz found 66 bugs including 38 zero-days via property-based testing.
- ZKAP achieves F1 score 0.82 and discovered 34 previously unknown vulnerabilities via static analysis (Circom only).
- Formal verification tools (NAVe for Noir, Picus for Circom) cannot yet handle circuits with millions of constraints.

## Entities

None.

## Dependencies

- [[ch03-under-constrained-circuits-the-dominant-failure-mode]] — the upstream chapter section that introduces this failure mode
- [[ch04-the-witness-as-a-multi-dimensional-problem]] — synthesizes correctness as the fourth gap

## Sources cited

- RISC Zero CVE-2025-52484 (disclosed; rs1/rs2 register operand confusion)
- zkSync Era MemoryWriteQuery bug (missing `lc.enforce_zero(cs)` on high 128 bits)
- zkFuzz — 66 bugs found, 38 zero-days
- ZKAP — F1 score 0.82, 34 previously unknown vulnerabilities, Circom only

## Open questions

- Extending static analysis tools (ZKAP) to Rust-based systems (halo2, Plonky3) is flagged as an open problem.
- No production system combines compile-time prevention and post-hoc verification for comprehensive correctness coverage.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [P3] (D) The section introduces "non-deterministic hints" as a relevant concept but this term is not indexed in the Entities list and does not link to a concept page. If it appears again in ch05, it should be a [[concept]] link here.

## Links

- Up: [[04-the-secret-performance]]
- Prev: [[ch04-side-channel-attacks-when-the-walls-leak]]
- Next: [[ch04-the-disclose-boundary-midnight-s-witness-architecture]]
