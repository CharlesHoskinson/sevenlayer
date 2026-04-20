---
title: "RISC-V Convergence"
slug: ch11-risc-v-convergence
chapter: 11
chapter_title: "zkVMs -- The Universal Stage"
heading_level: 2
source_lines: [4734, 4750]
source_commit: 53f41415d307dcd4ed73d852dfd6aa97146e882f
status: reviewed
word_count: 337
---

## RISC-V Convergence

The numbers are unambiguous: eight of ten major zkVMs target RISC-V. The original three-philosophy taxonomy -- EVM-Compatible, ZK-Native ISA, General-Purpose ISA -- is accurate as a historical classification, but the market has rendered its verdict. RISC-V won the general-purpose category decisively. Even EVM-focused projects now build RISC-V backends and layer EVM compatibility on top.

Why RISC-V? Three reasons converge.

First, RISC-V's register-transfer architecture maps cleanly onto tabular execution traces, which are the native input format for AIR and lookup-based arithmetization. A RISC-V instruction reads source registers, performs an operation, and writes a destination register -- exactly one row in a trace table.

Second, RISC-V's compiler ecosystem is decades deep. Any Rust, C, or C++ program can be compiled to RISC-V using standard LLVM toolchains. Millions of existing programs become provable without modification. The universal stage accepts any act, because any act can be translated into its language.

Third, RISC-V is open and royalty-free. Unlike ARM (proprietary) or x86 (legacy-encumbered), RISC-V has no licensing costs and no vendor lock-in. For an open-source ecosystem, this matters.

The holdouts are instructive. Cairo (Stwo) is a ZK-native ISA designed to minimize arithmetization cost -- the ISA *is* the constraint system. This gives Cairo a structural efficiency advantage: the compiler optimization study (Gassmann et al., "Optimizing RISC-V zkVM Compilation," 2025, preprint) [59] found that standard LLVM optimizations yield over 40% improvement on RISC-V zkVMs because they target hardware features (caches, branch predictors) absent in ZK contexts. Cairo avoids this overhead by design. Whether that advantage justifies a smaller developer ecosystem is the strategic question StarkWare has answered with "yes" for Starknet and "maybe not" for broader adoption (hence Kakarot's EVM-on-Stwo path).

zkWASM (Delphinus Lab) targets WebAssembly, offering the broadest language support of any zkVM (any language that compiles to WASM). It is the only production zkVM still using pairing-based KZG commitments rather than hash-based FRI, and it has not demonstrated Ethereum block proving. zkWASM appears to be a niche play for web-native applications rather than a contender for the mainstream proving market.



## Summary

Eight of ten major zkVMs converged on RISC-V by March 2026, driven by its clean register-transfer fit with AIR traces, deep LLVM toolchain, and royalty-free openness. Cairo (Stwo) and zkWASM are purpose-fit holdouts: Cairo eliminates the arithmetization tax by design; zkWASM trades proving performance for maximum language coverage.

## Key claims

- 8 of 10 major zkVMs target RISC-V as of March 2026.
- RISC-V's register-transfer architecture maps one instruction to one trace row, fitting AIR and lookup arithmetization directly.
- Standard LLVM optimizations yield >40% improvement on RISC-V zkVMs (Gassmann et al., 2025) because LLVM targets hardware features absent in ZK.
- Cairo avoids the LLVM arithmetization tax by collapsing ISA and constraint system.
- zkWASM uses PLONKish/KZG (pairing-based) -- the sole remaining non-hash-based outlier.
- zkWASM has not demonstrated Ethereum block proving.

## Entities

- [[arithmetization]]
- [[kzg]]
- [[plonk]]
- [[starknet]]

## Dependencies

- [[ch11-the-landscape-table-march-2026]] — ISA column of the landscape table
- [[ch11-three-zkvms-through-seven-layers]] — SP1 and Stwo Layer 2 analysis
- [[ch03-risc-v-won-why-taxonomy-still-matters]] — Chapter 3's treatment of ISA taxonomy
- [[ch03-the-four-philosophies]] — the three-philosophy taxonomy referenced here

## Sources cited

- Gassmann et al. (2025) — compiler optimization study: >40% LLVM improvement on RISC-V zkVMs

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P3] (C) "Unlike ARM (proprietary) or x86 (legacy-encumbered)" — ARM cores are licensed widely; calling ARM simply "proprietary" oversimplifies a nuanced licensing model and risks being misleading to technically sophisticated readers.

## Links

- Up: [[11-zkvms-the-universal-stage]]
- Prev: [[ch11-performance-the-cost-collapse]]
- Next: [[ch11-the-stage-is-set]]
