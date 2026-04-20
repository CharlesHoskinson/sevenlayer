---
title: "Midnight's BLS12-381 Stage"
slug: ch02-midnight-s-bls12-381-stage
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [681, 697]
source_commit: 53f41415d307dcd4ed73d852dfd6aa97146e882f
status: reviewed
word_count: 522
---

## Midnight's BLS12-381 Stage

The ADOPT framework gives us a lens for evaluating any ceremony. Midnight -- a privacy-focused blockchain built on the Cardano ecosystem -- provides a concrete case study that illustrates how Layer 1 choices cascade through every subsequent layer. It uses BLS12-381 with a PLONK-family proof system (Halo 2 / UltraPlonk, per the Universal versus Circuit-Specific section above). Here is how its Layer 1 choices cascade through the stack:

**The ceremony.** Midnight operates a `midnight-trusted-setup` repository for conducting its Powers-of-Tau ceremony. The ceremony produces a universal SRS on BLS12-381 -- a set of elliptic curve points encoding powers of a secret trapdoor. The SRS bounds the maximum circuit size: you cannot prove statements about circuits larger than the SRS supports.

**Per-circuit keys.** The Compact compiler (`compactc compile`) takes each contract's circuit description (ZKIR) and the universal SRS to produce per-circuit proving and verification keys. This is deterministic: same source plus same compiler yields same keys. No new trust assumption enters. A simple counter contract produces a 13.7 KB proving key and a 1.3 KB verification key [Midnight Network devnet documentation, docs.midnight.network, as of Q1 2025].

**Deployment flow.** The proving key goes to the proof server (running locally at localhost:6300 -- witnesses never cross the network [Midnight Network devnet documentation, docs.midnight.network, as of Q1 2025]). The verification key reaches the blockchain via `submitInsertVerifierKeyTx`. Every node that validates transactions uses this key to check proofs.

**The Pluto-Eris detour.** Midnight originally adopted Pluto-Eris, a cycle of curves that enabled recursive proof composition (KZG on Pluto, IPA on Eris). A curve cycle lets you verify a proof *inside* another proof -- the mathematical equivalent of a Russian nesting doll, where each layer confirms the one inside it. This is powerful for building chains of trust, but it comes with a cost: arithmetic on the second curve is slower, parameter selection is constrained, and the ecosystem tooling is immature. In April 2025, the Midnight team announced a switch back to BLS12-381 [Midnight Network, "Midnight's Proving System is Switching from Pluto Eris to BLS," docs.midnight.network/blog/zkp]. The reasons, stated in the announcement, were concrete: a well-understood standardized curve in place of a bespoke Pluto-Eris trusted setup, proof verification times halved from 12 ms to 6 ms, smaller proofs, and broader ecosystem compatibility. Theoretical optimality yielded to engineering pragmatism. The choices that win in production are not always the choices that win in papers.

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

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [none] (C) No AI-smell or style issues. Concrete, specific, and direct.
- [none] (D) No contradictions with other chapters found.
- [P3] (E) The section does not note whether the `midnight-trusted-setup` ceremony has been completed or is ongoing, or how its ADOPT scores compare to the Ethereum KZG ceremony analyzed in the preceding section.

## Links

- Up: [[02-building-the-stage]]
- Prev: [[ch02-the-adopt-framework]]
- Next: [[ch02-option-value-analysis]]
