---
title: "Midnight's BLS12-381 Stage"
slug: ch02-midnight-s-bls12-381-stage
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [691, 707]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
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

Midnight's Layer 1 uses a Powers-of-Tau ceremony on BLS12-381 with a PLONK-family (Halo2) proof system; the Compact compiler derives per-circuit proving and verification keys deterministically from the universal SRS with no new trust. In April 2025 Midnight switched back from Pluto-Eris (a curve cycle enabling recursive composition) to BLS12-381 for pragmatic reasons — faster proofs, better tooling — accepting that all shielded transactions become forgeable if a quantum computer extracts the trapdoor. The quantum migration path is not a software update: it requires a new ceremony, new keys for every contract, and new wallet software.

## Key claims

- Midnight runs a `midnight-trusted-setup` Powers-of-Tau ceremony producing a universal SRS on BLS12-381.
- A simple counter contract produces a 13.7 KB proving key and a 1.3 KB verification key from the universal SRS.
- The proof server runs locally at localhost:6300; witnesses never cross the network.
- Midnight originally used Pluto-Eris curves for recursive composition; switched to BLS12-381 in April 2025.
- BLS12-381 provides ~128-bit classical security but zero post-quantum security.
- Quantum migration requires: new ceremony, new SRS, new proving/verification keys for every contract, new wallet software, and a transition period.

## Entities

- [[bls12-381]]
- [[ceremony]]
- [[fri]]
- [[ipa]]
- [[kzg]]
- [[midnight]]
- [[plonk]]

## Dependencies

- [[ch02-the-adopt-framework]] — the ADOPT lens for evaluating Midnight's ceremony
- [[ch02-universal-versus-circuit-specific-setups]] — the universal setup model Midnight uses
- [[ch02-the-quantum-shelf-life]] — the quantum exposure Midnight accepted with BLS12-381

## Sources cited

None in this section.

## Open questions

- Whether Midnight's quantum migration is feasible at scale before cryptographically relevant quantum computers arrive remains open.

## Improvement notes

- [P1] (A) The section describes Midnight's proof system as "PLONK-family (a variant of Halo2)" but ch06-case-study-midnight-s-sealed-certificate identifies it specifically as "Halo 2 / UltraPlonk with custom gates." The ch02 description is vague where a more precise characterization exists; the term "Halo2 variant" is used in ch02-universal-versus-circuit-specific-setups as well, but "UltraPlonk" is the specific variant and should be named here.
- [P1] (A) The April 2025 Pluto-Eris → BLS12-381 switch claim has no source citation (same issue as in ch02-the-quantum-shelf-life); the `midnight-trusted-setup` repository reference also lacks a URL.
- [P2] (B) The proof server URL (localhost:6300) and the 13.7 KB / 1.3 KB proving/verification key sizes appear to be sourced from Midnight devnet documentation, but no source is cited.
- [none] (C) No AI-smell or style issues. Concrete, specific, and direct.
- [none] (D) No contradictions with other chapters found.
- [P3] (E) The section does not note whether the `midnight-trusted-setup` ceremony has been completed or is ongoing, or how its ADOPT scores compare to the Ethereum KZG ceremony analyzed in the preceding section.

## Links

- Up: [[02-building-the-stage]]
- Prev: [[ch02-the-adopt-framework]]
- Next: [[ch02-option-value-analysis]]
