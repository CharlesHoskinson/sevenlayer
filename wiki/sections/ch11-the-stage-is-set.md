---
title: "The Stage Is Set"
slug: ch11-the-stage-is-set
chapter: 11
chapter_title: "zkVMs -- The Universal Stage"
heading_level: 2
source_lines: [4760, 4773]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 344
---

## The Stage Is Set

Three conclusions emerge from the landscape.

First, the ISA war is over. RISC-V won, and the remaining holdouts (Cairo, zkWASM) serve specialized niches rather than competing for the general-purpose market. For system architects, this means the language question from Chapter 3 has a default answer: write Rust, compile to RISC-V, and the zkVM handles the rest. Philosophy C absorbed Philosophies A and B -- not by defeating them, but by making their benefits available as compatibility layers on top of a universal stage.

Second, the proof core from Chapter 10 is visible in every row of the landscape table. The field choice (BabyBear, M31, Goldilocks, BN254) determines the commitment scheme (FRI, Circle STARK, KZG), which determines the arithmetization (AIR, Circle AIR, R1CS), which determines the proof system. Change one cell in the table, and every other cell in that row must adapt. The seven-layer model did not break under zkVM pressure -- it *fused*. Layers 2 and 3 (language and witness) merged when "write Rust" became the universal answer. Layers 4, 5, and 6 (arithmetization, proof system, cryptographic primitives) became the proof core triad that Chapter 10 identified. What remains separate is Layer 1 (setup: ceremony or transparent) and Layer 7 (verification: where the proof lands and who governs the verifier contract).

Third, the competitive axis is rotating. The speed race is over -- four independent teams achieved real-time Ethereum block proving in 2025. The next frontier is provable security: 128-bit security with formal verification, not just empirical benchmarks. The teams that win the next phase will not be the ones with the fastest provers but the ones whose proofs you can trust with mathematical certainty.

Midnight does not appear in this landscape table because it is not a zkVM. It is a privacy theater -- a system where every smart contract executes via zero-knowledge proofs, not as an optimization but as the fundamental execution model. Where the zkVMs in this chapter prove *computation*, Midnight proves *state transitions with privacy constraints*. Chapter 12 audits it against every layer.

---


## Summary

The ISA war ended with RISC-V; the speed race ended with four teams achieving real-time Ethereum proving in 2025. The seven-layer model fused under zkVM pressure rather than breaking: Layers 2–3 merged around Rust/RISC-V, Layers 4–6 became the proof core triad. The next competitive axis is 128-bit provable security and formal verification.

## Key claims

- RISC-V won; Cairo and zkWASM serve niches, not the general-purpose market.
- Philosophy C (general-purpose ISA) absorbed Philosophies A and B as compatibility layers.
- Field choice cascades: BabyBear/M31/Goldilocks/BN254 → commitment → arithmetization → proof system.
- Speed race ended: four teams achieved real-time Ethereum block proving in 2025.
- Next axis: 128-bit provable security with formal verification (EF target by December 2026).
- Layer 1 (setup) and Layer 7 (verification governance) remain the two genuinely separable layers.
- Midnight is excluded from this chapter; it is a privacy-first execution model, not a zkVM.

## Entities

- [[babybear]]
- [[bn254]]
- [[ceremony]]
- [[circle stark]]
- [[fri]]
- [[goldilocks]]
- [[kzg]]
- [[midnight]]

## Dependencies

- [[ch11-the-landscape-table-march-2026]] — the landscape table this section summarizes
- [[ch11-the-proof-core-triad]] — the proof core triad formalized
- [[ch11-performance-the-cost-collapse]] — speed race conclusion detailed there
- [[ch11-risc-v-convergence]] — ISA war conclusion detailed there
- [[ch12-midnight-as-test-case]] — Midnight chapter referenced as the next audit

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [P2] (D) "Philosophy C absorbed Philosophies A and B" — these labels are not defined within the section and are only meaningful with Ch3 in view; a brief inline gloss (e.g., "Philosophy C (general-purpose ISA)") would help the section stand alone or serve as a navigable reference.
- [P2] (A) "the proof core from Chapter 10" — the proof core triad concept is first introduced in Chapter 6 (ch06-the-proof-core-why-layers-4-5-and-6-are-inseparable) and revisited in Chapter 10; attributing it solely to Ch10 misrepresents its origin in the book.
- [P3] (D) "BabyBear/M31/Goldilocks/BN254 → commitment → arithmetization → proof system" — Goldilocks appears in this field-choice cascade but does not feature in the proof core triad discussion in ch11-the-proof-core-triad (only BabyBear, M31, BN254); its inclusion here without a corresponding triad analysis creates a gap.

## Links

- Up: [[11-zkvms-the-universal-stage]]
- Prev: [[ch11-risc-v-convergence]]
- Next: —
