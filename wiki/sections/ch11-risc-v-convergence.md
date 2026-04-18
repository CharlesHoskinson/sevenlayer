---
title: "RISC-V Convergence"
slug: ch11-risc-v-convergence
chapter: 11
chapter_title: "zkVMs -- The Universal Stage"
heading_level: 2
source_lines: [4729, 4745]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 337
---

## RISC-V Convergence

The numbers are unambiguous: eight of ten major zkVMs target RISC-V. The original three-philosophy taxonomy -- EVM-Compatible, ZK-Native ISA, General-Purpose ISA -- is accurate as a historical classification, but the market has rendered its verdict. RISC-V won the general-purpose category decisively. Even EVM-focused projects now build RISC-V backends and layer EVM compatibility on top.

Why RISC-V? Three reasons converge.

First, RISC-V's register-transfer architecture maps cleanly onto tabular execution traces, which are the native input format for AIR and lookup-based arithmetization. A RISC-V instruction reads source registers, performs an operation, and writes a destination register -- exactly one row in a trace table.

Second, RISC-V's compiler ecosystem is decades deep. Any Rust, C, or C++ program can be compiled to RISC-V using standard LLVM toolchains. This means millions of existing programs become provable without modification. The universal stage accepts any act, because any act can be translated into its language.

Third, RISC-V is open and royalty-free. Unlike ARM (proprietary) or x86 (legacy-encumbered), RISC-V has no licensing costs and no vendor lock-in. For an open-source ecosystem, this matters.

The holdouts are instructive. Cairo (Stwo) is a ZK-native ISA designed to minimize arithmetization cost -- the ISA *is* the constraint system. This gives Cairo a structural efficiency advantage: the compiler optimization study (Gassmann et al., 2025) found that standard LLVM optimizations yield over 40% improvement on RISC-V zkVMs because they target hardware features (caches, branch predictors) absent in ZK contexts. Cairo avoids this overhead by design. Whether that advantage justifies a smaller developer ecosystem is the strategic question StarkWare has answered with "yes" for Starknet and "maybe not" for broader adoption (hence Kakarot's EVM-on-Stwo path).

zkWASM (Delphinus Lab) targets WebAssembly, offering the broadest language support of any zkVM (any language that compiles to WASM). Its PLONKish/KZG architecture is a generational outlier -- it uses pairing-based commitments rather than hash-based -- and it has not demonstrated Ethereum block proving. zkWASM appears to be a niche play for web-native applications rather than a contender for the mainstream proving market.



## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
