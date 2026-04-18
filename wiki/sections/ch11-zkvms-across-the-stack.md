---
title: "zkVMs Across the Stack"
slug: ch11-zkvms-across-the-stack
chapter: 11
chapter_title: "zkVMs -- The Universal Stage"
heading_level: 2
source_lines: [4547, 4556]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 251
---

## zkVMs Across the Stack

We need to talk about the thing that changed everything.

The zkVM is not a Layer 2 phenomenon. It is a technology that reaches into every layer of the stack -- from the field choice at Layer 6, through the arithmetization at Layer 4, to the verification economics at Layer 7. If the seven-layer model is the map, the zkVM is the earthquake that reshaped the terrain.

Before zkVMs, every zero-knowledge application required building a custom stage: hand-crafting constraint systems, choosing a field, designing a witness format, writing a custom verifier. Each application was a bespoke production -- a one-night show with its own scenery, its own props, its own choreography. The zkVM changed this by providing a **universal stage** that can host any trick. A developer writes ordinary Rust, compiles it to RISC-V, and the zkVM handles everything else: witness generation, arithmetization, proving, compression, and verification. The stage is universal; the performances are infinite.

The preceding layer-by-layer analysis reveals why this matters so deeply. The most urgent findings at nearly every layer are not isolated gaps but consequences of the same underlying shift. Polygon zkEVM's shutdown at Layer 2, the Witness Gap's amplification at Layer 3, CCS and LogUp's emergence at Layer 4, folding's rise and the hybrid pipeline's dominance at Layer 5, the small-field revolution at Layer 6, STARK-to-SNARK wrapping at Layer 7 -- these are the seismic effects of a single tectonic event: the zero-knowledge virtual machine reorganized the entire stack around itself.


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
