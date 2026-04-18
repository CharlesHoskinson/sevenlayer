---
title: "ZK Rollups: The Proving Grounds (Production)"
slug: ch13-zk-rollups-the-proving-grounds-production
chapter: 13
chapter_title: "The Market Landscape"
heading_level: 2
source_lines: [4986, 5011]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 745
---

## ZK Rollups: The Proving Grounds (Production)

Zero-knowledge rollups are where the thesis of this chapter becomes immediately testable. The mechanism is straightforward: execute transactions off-chain, generate a ZK proof of correct execution, and post the proof plus compressed state data to Ethereum for verification. Ethereum-grade security with 10-100x lower transaction costs. At Layer 7, the audience can verify every proof. The math is sound. The trick works.

But look at the governance. Every major rollup in production today operates at Stage 0 or Stage 1 -- meaning a security council, a multisig, or a governance committee can override the proof system. The audience can check the math, but a committee can still replace the audience. Trust has been minimized at the cryptographic layer and preserved, nearly intact, at the institutional layer. This is not a criticism. It is a fact about where we are, and it should be stated plainly.

The market has consolidated rapidly, and one of its most expensive lessons has already been paid. Polygon zkEVM, once the flagship example of EVM-compatible ZK rollups (Philosophy A in the original taxonomy), was shut down in 2025/2026 after approximately $250 million in investment. The core team, led by co-founder Jordi Baylina, spun off to found ZisK. A quarter-billion dollars bought a lesson: in a field moving this fast, the first-mover advantage is often a first-mover trap.

The current production leaders tell a more encouraging story -- but the trust question follows them onto every stage:

**Scroll** ($748M TVL as of early 2026) -- the largest zkEVM by total value locked. Scroll uses a halo2-based proof system with KZG commitments, generating PLONKish proofs that are verified directly on Ethereum L1. Seven hundred forty-eight million dollars locked means users trust the math with real money. Whether they have examined the governance is a different question.

**Linea** ($2B TVL) -- ConsenSys's zkEVM, targeting full EVM equivalence. Linea uses a custom prover with Fiat-Shamir-based PLONK and posts compressed proofs to Ethereum. Two billion dollars locked. That is not a pilot program. It is also not a trustless one.

**Starknet** -- powered by Stwo, the Circle STARK prover that went live on mainnet in November 2025. Starknet stands apart: it uses the Cairo ISA rather than EVM compatibility, and its STARK proofs are verified natively on L1 without Groth16 wrapping (accepting larger proof sizes in exchange for transparency). The only major rollup that performs the entire trick on a glass stage -- no trusted setup, no opaque wrapping. The trust tradeoff is different here: you trust the transparency of the mathematics, and you pay for it in proof size.

**ZKsync Era** -- Matter Labs' zkEVM, powered by the Airbender prover. ZKsync achieved 21.8 million cycles per second on a single H100 GPU and deployed via the Atlas upgrade. The 2026 roadmap targets formal verification and adoption as a "universal standard" for ZK proving.

Midnight, analyzed in Chapter 12, occupies a distinct position in this landscape -- not a rollup optimizing Ethereum throughput, but a privacy-first sidechain where ZK proofs are the execution model. Its Stage 0-1 maturity and ~18-second proof times place it alongside early-stage rollups in production readiness, but its privacy-by-architecture design addresses a different market: applications where transaction confidentiality is the primary requirement, not throughput.

The aggregate picture: ZK rollups collectively secured over $20 billion in total value locked by early 2026 (Chapter 1). That figure represents real capital betting on the soundness of proof systems and the governance of rollup operators. Whether that bet is well-placed depends on how quickly rollups mature from Stage 0-1 (governance can override proofs) to Stage 2 (governance cannot override proofs except for proven soundness errors). As of this writing, no major ZK rollup has reached Stage 2.

The economics have improved sharply. The 2,000-fold cost collapse described in Chapter 6 means that at current rates, continuously proving every Ethereum block costs roughly $102,000 per year -- less than the GPU cluster required to do it. Post-Pectra (May 2025) and Fusaka (December 2025), data availability costs have also dropped, with blob capacity increasing 8x via PeerDAS. The trick has become cheaper than the theater's electricity bill. But cost is not the same as trust. A cheap proof verified by a governance council you cannot remove is still a proof verified by a governance council you cannot remove.

**Trust relocated from:** L1 execution validators **to:** proof system soundness + governance multisig. **Net:** genuine minimization for computation integrity; governance remains the binding constraint.


## Summary

ZK rollups are the most mature market segment: over $20 billion in TVL by early 2026, with proving costs down ~2,000-fold since 2022. Every production rollup operates at Stage 0 or Stage 1, meaning governance multisigs can still override the proof system; no major rollup has reached Stage 2. Trust is genuinely minimized at the cryptographic layer but largely preserved at the institutional layer.

## Key claims

- ZK rollups collectively held >$20B TVL by early 2026.
- No major ZK rollup had reached Stage 2 as of this writing; all remain at Stage 0 or Stage 1.
- Scroll held $748M TVL (halo2/KZG); Linea held $2B TVL (PLONK/Fiat-Shamir).
- Starknet (Stwo/Circle STARKs) is the only major rollup without a trusted setup, at the cost of larger proof sizes.
- ZKsync Era's Airbender prover achieved 21.8 million cycles/second on a single H100.
- Polygon zkEVM was shut down after ~$250M investment; the core team founded ZisK.
- Continuously proving every Ethereum block costs roughly $102,000/year at current rates.

## Entities

- [[airbender]]
- [[circle stark]]
- [[fiat-shamir]]
- [[groth16]]
- [[h100]]
- [[halo2]]
- [[kzg]]
- [[midnight]]
- [[plonk]]
- [[polygon]]
- [[starknet]]
- [[zisk]]

## Dependencies

- [[ch01-the-phenomenon]] — TVL figures and production context introduced in Chapter 1
- [[ch06-circle-starks-and-stwo-a-generational-leap]] — Stwo/Circle STARKs technical basis
- [[ch06-the-three-families]] — proof family taxonomy referenced (Groth16, PLONK, STARKs)
- [[ch12-midnight-at-a-glance]] — Midnight's rollup-adjacent position analysed in Chapter 12
- [[ch11-the-landscape-table-march-2026]] — Stage 0/1/2 maturity classification

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [P2] (B) No sources cited for specific figures: Scroll $748M TVL, Linea $2B TVL, ZKsync Airbender 21.8M cycles/sec, $102K/year proving cost, blob capacity increase figures. These are verifiable claims that should carry citations.
- [P2] (A) "Fiat-Shamir-based PLONK" for Linea is imprecise; Linea uses a gnark-based custom SNARK. The description conflates the non-interactivity transform with the underlying proof system family.
- [P3] (D) "Philosophy A in the original taxonomy" references a ch03 classification not defined here and not wikilinked; a dependency link to the relevant ch03 section is missing.
- [P3] (A) "Atlas upgrade" for ZKsync Era's Airbender deployment is a specific named event with no citation or wikilink; if the name is wrong or contested it will be unverifiable.

## Links

- Up: [[13-the-market-landscape]]
- Prev: —
- Next: [[ch13-zk-coprocessors-off-chain-computation-on-chain-verification-growth]]
