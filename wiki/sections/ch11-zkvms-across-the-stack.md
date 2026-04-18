---
title: "zkVMs Across the Stack"
slug: ch11-zkvms-across-the-stack
chapter: 11
chapter_title: "zkVMs -- The Universal Stage"
heading_level: 2
source_lines: [4553, 4562]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 251
---

## zkVMs Across the Stack

We need to talk about the thing that changed everything.

The zkVM is not a Layer 2 phenomenon. It is a technology that reaches into every layer of the stack -- from the field choice at Layer 6, through the arithmetization at Layer 4, to the verification economics at Layer 7. If the seven-layer model is the map, the zkVM is the earthquake that reshaped the terrain.

Before zkVMs, every zero-knowledge application required building a custom stage: hand-crafting constraint systems, choosing a field, designing a witness format, writing a custom verifier. Each application was a bespoke production -- a one-night show with its own scenery, its own props, its own choreography. The zkVM changed this by providing a **universal stage** that can host any trick. A developer writes ordinary Rust, compiles it to RISC-V, and the zkVM handles everything else: witness generation, arithmetization, proving, compression, and verification. The stage is universal; the performances are infinite.

The preceding layer-by-layer analysis reveals why this matters so deeply. The most urgent findings at nearly every layer are not isolated gaps but consequences of the same underlying shift. Polygon zkEVM's shutdown at Layer 2, the Witness Gap's amplification at Layer 3, CCS and LogUp's emergence at Layer 4, folding's rise and the hybrid pipeline's dominance at Layer 5, the small-field revolution at Layer 6, STARK-to-SNARK wrapping at Layer 7 -- these are the seismic effects of a single tectonic event: the zero-knowledge virtual machine reorganized the entire stack around itself.


## Summary

zkVMs act as a universal proving stage, abstracting all seven layers behind a single Rust-to-RISC-V pipeline. The cross-layer effects -- Witness Gap at Layer 3, small-field revolution at Layer 6, STARK-to-SNARK wrapping at Layer 7 -- are not independent trends but consequences of this one reorganization.

## Key claims

- zkVMs reach all seven layers, not just Layer 2.
- The universal stage model: write Rust, compile to RISC-V, zkVM handles witness, arithmetization, proving, compression, verification.
- Polygon zkEVM's shutdown is a Layer 2 consequence of the zkVM shift.
- CCS and LogUp emergence at Layer 4 is a zkVM consequence.
- Folding's rise and hybrid pipeline dominance at Layer 5 trace to the same cause.
- The small-field revolution at Layer 6 is driven by zkVM throughput demands.
- STARK-to-SNARK wrapping at Layer 7 is the zkVM ecosystem's verification solution.

## Entities

- [[folding]]
- [[logup]]
- [[polygon]]
- [[small-field]]

## Dependencies

- [[ch11-the-landscape-table-march-2026]] — details the zkVM landscape this section frames
- [[ch11-three-zkvms-through-seven-layers]] — traces the cross-layer effects through SP1, Stwo, Jolt
- [[ch10-the-causal-web-why-it-is-a-dag-not-a-stack]] — the causal structure of layer interdependencies
- [[ch06-the-hybrid-pipeline]] — STARK-to-SNARK wrapping referenced here
- [[ch05-lookup-arguments]] — CCS and LogUp's Layer 4 emergence

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [P2] (B) "Polygon zkEVM's shutdown at Layer 2" stated without citation; this is a specific empirical claim that needs a source or date.
- [P2] (B) No sources cited anywhere in the section despite making specific cross-layer causal claims (Witness Gap amplification, LogUp/CCS emergence as zkVM consequences). At minimum, forward references to sourced sections should anchor these claims.

## Links

- Up: [[11-zkvms-the-universal-stage]]
- Prev: —
- Next: [[ch11-the-landscape-table-march-2026]]
