---
title: "Midnight -- The Privacy Theater"
chapter: 12
kind: chapter-hub
status: untouched
---

# Chapter 12: Midnight -- The Privacy Theater

## Sections

- [[ch12-midnight-as-test-case]]
- [[ch12-midnight-at-a-glance]]
- [[ch12-full-seven-layer-mapping]]
- [[ch12-where-midnight-validates-the-model]]
- [[ch12-where-midnight-challenges-the-model]]
- [[ch12-the-privacy-theater-analogy]]
- [[ch12-five-lessons-for-zk-system-design]]

## Audit rollup

Audited 2026-04-18. P0=1, P1=3, P2=7, P3=5.

| Section | Findings |
|---------|----------|
| ch12-midnight-as-test-case | none |
| ch12-midnight-at-a-glance | P2 B (missing citations for localhost:6300 and token claims); P3 C (boilerplate framing) |
| ch12-full-seven-layer-mapping | P1 A (BLS12-381 scalar field stated as ~2^253, should be ~2^255); P1 A (Halo 2 mislabelled "UltraPlonk"); P1 D (verifier-key mutability contradicts ch08 immutability claim); P2 A (~490T SPECK uncited/undefined unit); P2 B (Pluto-Eris history and Halo 2 rationale uncited); P3 C (extended Asimov/theater analogies in Layer 3 add length without information) |
| ch12-where-midnight-validates-the-model | P2 E (no explanation of why L3/L6 are not clean fits); P3 B (490T SPECK floats uncited) |
| ch12-where-midnight-challenges-the-model | P2 A ("Shielded" used as token name instead of "custom tokens"); P2 B (26-intermediate-language claim uncited); P3 D (abrupt table transition) |
| ch12-the-privacy-theater-analogy | P1 A ("air-gapped" is technically incorrect for localhost process); P2 B (490T SPECK uncited); P3 C (Penrose close is decorative) |
| ch12-five-lessons-for-zk-system-design | P0 A (Lesson 3 calls DUST a "shielded token" — DUST is unshielded/public); P2 B (L2Beat Stage 0-1 and bug claims uncited); P2 B (cross-contract/compiler-bug claims undated, staleness risk); P3 C (three-declarative theater close is stylistic not informational) |
