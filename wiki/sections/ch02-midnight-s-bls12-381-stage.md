---
title: "Midnight's BLS12-381 Stage"
slug: ch02-midnight-s-bls12-381-stage
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [691, 707]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 522
---

## Midnight's BLS12-381 Stage

The ADOPT framework gives us a lens for evaluating any ceremony. Midnight -- a privacy-focused blockchain built on the Cardano ecosystem -- provides a concrete case study that illustrates how Layer 1 choices cascade through every subsequent layer. It uses BLS12-381 with a PLONK-family proof system. Here is how its Layer 1 choices cascade through the stack:

**The ceremony.** Midnight operates a `midnight-trusted-setup` repository for conducting its Powers-of-Tau ceremony. The ceremony produces a universal SRS on BLS12-381 -- a set of elliptic curve points encoding powers of a secret trapdoor. The SRS bounds the maximum circuit size: you cannot prove statements about circuits larger than the SRS supports.

**Per-circuit keys.** The Compact compiler (`compactc compile`) takes each contract's circuit description (ZKIR) and the universal SRS to produce per-circuit proving and verification keys. This is deterministic: same source plus same compiler yields same keys. No new trust assumption enters. A simple counter contract produces a 13.7 KB proving key and a 1.3 KB verification key.

**Deployment flow.** The proving key goes to the proof server (running locally at localhost:6300 -- witnesses never cross the network). The verification key reaches the blockchain via `submitInsertVerifierKeyTx`. Every node that validates transactions uses this key to check proofs.

**The Pluto-Eris detour.** Midnight originally adopted Pluto-Eris, a cycle of curves that enabled recursive proof composition (KZG on Pluto, IPA on Eris). A curve cycle lets you verify a proof *inside* another proof -- the mathematical equivalent of a Russian nesting doll, where each layer confirms the one inside it. This is powerful for building chains of trust, but it comes with a cost: arithmetic on the second curve is slower, parameter selection is constrained, and the ecosystem tooling is immature. In April 2025, the Midnight team announced a switch back to BLS12-381 -- a single, well-supported curve with faster proof generation, broader ecosystem compatibility, and better tooling. Theoretical optimality yielded to engineering pragmatism. The choices that win in production are not always the choices that win in papers.

**The quantum exposure.** BLS12-381 provides approximately 128-bit classical security but zero post-quantum security. Every ZK proof in Midnight -- state transitions, shielded transfers, Zswap privacy operations -- becomes forgeable if a quantum computer extracts the trapdoor from the SRS. The migration path is not a software update. It is a new ceremony, a new SRS, new proving and verification keys for every contract, new wallet software for every user, and a transition period during which the old and new systems must coexist. For a privacy-focused blockchain whose users chose it specifically to protect sensitive data, the quantum exposure is not merely a technical risk. It is an existential one.

The Midnight case study illustrates a broader truth about Layer 1: the setup choice is a bet on the future. Midnight bet on BLS12-381 because it is the most mature, best-tooled, most widely deployed pairing-friendly curve in the ecosystem. That bet optimizes for today's performance and ecosystem compatibility. Whether it survives the quantum transition is an open question -- one that the Midnight team will face, along with every other pairing-based system, before the decade is out.



## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
