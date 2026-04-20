---
title: "The Three Frontiers"
slug: ch14-the-three-frontiers
chapter: 14
chapter_title: "Open Questions and the Road Ahead"
heading_level: 2
source_lines: [5347, 5390]
source_commit: 8e419c9815e6fe5f507dd769315a84b46afd74d5
status: reviewed
word_count: 729
---

## The Three Frontiers

The ZK field is transitioning through three sequential frontiers, each building on the previous:

### Frontier 1: Performance (2023-2025) -- Largely Crossed

The performance frontier asked: can we prove computation fast enough and cheaply enough for production use? The answer, as of late 2025, is yes. Real-time Ethereum proving is achieved. The cost curve traced in Chapters 1 and 6 has flattened at pennies per block. The EF declared the speed race won. The remaining performance work is optimization (energy efficiency, memory reduction, witness acceleration), not breakthrough. The magician can now perform in real time. That question is settled.

**Evidence this frontier is active:**
- SP1 Hypercube: 6.9s Ethereum block proving on 16 GPUs (Dec 2025)
- Airbender: 21.8M RISC-V cycles/sec on single H100 (2025)
- Proving cost: $80 → $0.04 in 24 months (2,000x reduction)
- EF declared speed race 'effectively won,' pivoted to security (Dec 2025)

### Frontier 2: Security (2026-2028) -- Currently Active

The security frontier asks: can we prove that our proofs are actually sound, with quantifiable security guarantees? The EF's 2026 targets (100-bit by May, 128-bit by December) define this frontier precisely. It includes formal verification of zkVM implementations, provable soundness without conjectured assumptions (proximity gaps), post-quantum readiness, and protection against Fiat-Shamir vulnerabilities.

This frontier is harder than performance because security is a property you prove, not a metric you optimize. You cannot benchmark soundness the way you benchmark throughput. The tools (Picus, ZKAP, ARGUZZ, soundcalc) are emerging but immature. The field's first formal verification efforts (SP1's RISC-V Sail specification verification, Jolt's ACL2 lookup semantics verification) are promising but cover only fragments of the full stack. Proving that the trick works is easy. Proving that it *cannot* be faked is the real challenge.

**Evidence this frontier is active:**
- EF 2026 targets: 100-bit provable security by May, 128-bit by December
- SP1: formal verification of 62 RISC-V opcodes against Sail specification
- Arguzz (Hochrainer, Wustholz, Christakis, 2025): found 11 bugs across 6 major zkVMs
- soundcalc: automated soundness margin calculator for proof system parameters
- Picus, ZKAP: emerging static analysis tools for constraint under-specification

### Frontier 3: Privacy (2027+) -- Approaching

The privacy frontier asks: can we build systems where users genuinely control their data, where the "zero-knowledge" property holds not just mathematically but in practice? This frontier includes constant-time implementations, metadata privacy (timing, transaction structure, network-level information), and application-layer privacy design (compiler-enforced disclosure boundaries, selective disclosure for regulatory compliance).

Midnight represents an early attempt at this frontier. Its disclosure analysis is the most sophisticated compiler-level privacy enforcement in any ZK system. But the documentation's silence on side channels, the indexer's metadata leakage, and the SDK-level timing correlations demonstrate how far the field has to go.

The privacy frontier is the most difficult of the three because it requires solving problems across all seven layers simultaneously. Performance is primarily a Layers 3-5 problem. Security spans Layers 2-6. Privacy, as Midnight demonstrates, is a property of the entire stack. The theater must be lightproof at every joint. Question 6 (constant-time proving) is the critical blocker for this frontier -- without it, the mathematical zero-knowledge guarantee is undermined at the physical layer by timing channels, cache patterns, and electromagnetic emanations that the proof cannot control.

Beyond constant-time proving, the privacy frontier includes three additional dimensions that no current system fully addresses. Metadata protection: when you submit a transaction, the timing of your submission, the size of your proof, and the pattern of your indexer queries all leak information that the proof itself conceals. Network-level privacy: without a mixing layer (like Tor) between the user and the blockchain node, an ISP or node operator can correlate IP addresses with transaction submissions. And cross-application privacy: when shielded tokens move between contracts, the pattern of inter-contract calls can reveal information about the transaction flow even if individual calls are private.

**Evidence this frontier is active:**
- Compact disclosure analysis: 11 compile-time privacy errors caught in single voting contract — the first production example of compiler-enforced privacy at Layer 2
- Monero Bulletproofs: constant-time implementation ($R = 0.04$ timing correlation) — proof that constant-time proving is achievable, at a performance cost
- eIDAS 2.0: EU mandate for selective disclosure in digital identity wallets (2026)
- Midnight testnet: end-to-end private smart contract execution with local proving
- Zcash timing vulnerability patched; field now aware of side-channel class


## Summary

The ZK field moves through three sequential frontiers: Performance (2023-2025, largely crossed — real-time Ethereum proving at sub-cent costs), Security (2026-2028, active — EF targets 128-bit provable security by December 2026), and Privacy (2027+, approaching — constant-time proving and compiler-enforced disclosure boundaries). Each frontier is harder than the last; Privacy requires solving problems across all seven layers simultaneously.

## Key claims

- Performance frontier largely crossed: SP1 Hypercube proves an Ethereum block in 6.9s on 16 GPUs; proving cost fell from $80 to $0.04 in 24 months (2,000x)
- Airbender achieves 21.8M RISC-V cycles/sec on a single H100 (2025)
- EF declared the speed race "effectively won" in December 2025 and pivoted to security targets
- Security frontier is active: EF 2026 targets are 100-bit provable security by May and 128-bit by December
- ARGUZZ (Hochrainer, Wustholz, Christakis, 2025) found 11 bugs across 6 major zkVMs
- Privacy frontier requires all-layer solutions; Midnight's disclosure analysis is the first production compiler-level privacy enforcement
- Monero's constant-time Bulletproofs prover achieves $R = 0.04$ timing correlation, proving constant-time proving is achievable at a performance cost

## Entities

- [[airbender]]
- [[bulletproofs]]
- [[fiat-shamir]]
- [[h100]]
- [[jolt]]
- [[midnight]]
- [[sdk]]
- [[starks]]
- [[zcash]]

## Dependencies

- [[ch06-real-time-ethereum-proving]] — SP1 Hypercube and Airbender benchmarks establishing Performance frontier closure
- [[ch04-side-channel-attacks-when-the-walls-leak]] — Zcash timing correlations and Monero constant-time baseline cited as Privacy frontier evidence
- [[ch03-compact-s-disclosure-analysis]] — Midnight's 11 compile-time privacy errors, first production compiler-enforced disclosure boundary
- [[ch14-the-seven-questions-that-remain-open]] — Q6 (constant-time proving) is the critical Privacy frontier blocker flagged here

## Sources cited

- Succinct Labs. "SP1 Hypercube: Proving Ethereum in Real-Time." Blog post, May 2025. https://blog.succinct.xyz/sp1-hypercube/
- ZKsync. "Airbender: GPU-Accelerated RISC-V Proving." Product announcement, June 2025. https://www.zksync.io/airbender
- Hochrainer, Christoph, Valentin Wustholz, and Maria Christakis. "Arguzz: Testing zkVMs for Soundness and Completeness Bugs." arXiv 2509.10819, 2025.
- Kadianakis, George. "Shipping an L1 zkEVM #2: The Security Foundations." Ethereum Foundation Blog, December 2025. https://blog.ethereum.org/2025/12/18/zkevm-security-foundations
- European Union. "Regulation (EU) 2024/1183 -- European Digital Identity Framework (eIDAS 2.0)." *Official Journal of the European Union*, 2024.

## Open questions

- When will the Security frontier be fully crossed — i.e., when will 128-bit provable soundness (without conjectured proximity gaps) be achieved across leading zkVMs?
- What is the first production system to meaningfully address the Privacy frontier beyond compiler-level disclosure analysis?

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P2] (B) "SP1: formal verification of 62 RISC-V opcodes against Sail specification" appears in the Security frontier evidence block with no source listed; the sources section cites only the Kadianakis EF blog post and the Arguzz paper. The "62 opcodes" figure needs a dedicated citation.
- [P2] (A) SP1 Hypercube performance claim (6.9s, 16 GPUs) is tagged "Dec 2025" in the body but the SP1 Hypercube source is a May 2025 blog post; the EF security pivot post is Dec 2025. The date attribution conflates two separate announcements.
- [P3] (B) "soundcalc: automated soundness margin calculator" is presented as evidence with no citation anywhere in the section or sources block.
- [P3] (C) The paper is cited as "Arguzz" in Sources cited and bibliography but as "ARGUZZ" in ch14-the-seven-questions. Standardise capitalisation across both files.

## Links

- Up: [[14-open-questions-and-the-road-ahead]]
- Prev: [[ch14-the-seven-questions-that-remain-open]]
- Next: [[ch14-convergence]]
