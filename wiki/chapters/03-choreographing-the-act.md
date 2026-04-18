---
title: "Choreographing the Act"
chapter: 3
kind: chapter-hub
status: untouched
---

# Chapter 3: Choreographing the Act

## Sections

- [[ch03-risc-v-won-why-taxonomy-still-matters]]
- [[ch03-from-circuits-to-virtual-machines-a-brief-evolution]]
- [[ch03-the-four-philosophies]]
- [[ch03-the-developer-s-actual-experience]]
- [[ch03-under-constrained-circuits-the-dominant-failure-mode]]
- [[ch03-compact-s-disclosure-analysis]]
- [[ch03-midnight-compiler-ir-circuit]]

## Audit rollup

### Severity totals

| Severity | Count |
|----------|-------|
| P0 | 0 |
| P1 | 12 |
| P2 | 17 |
| P3 | 5 |

### Top 5 findings

1. **[P1] (A) Cairo/Goldilocks misattribution** — Two sections (`ch03-from-circuits-to-virtual-machines-a-brief-evolution`, `ch03-the-four-philosophies`) incorrectly state that Cairo uses the Goldilocks field ($2^{64} - 2^{32} + 1$). Cairo uses the Stark prime (p = 2^251 + 17·2^192 + 1). This factual error propagates across sections and will mislead readers who later encounter the field again in chapters 5 and 7.

2. **[P1] (A) Philosophy D table overstates Noir/Leo privacy guarantees** — The summary table in `ch03-the-four-philosophies` marks all three DSLs as "Compiler-enforced" privacy. Noir enforces pub/private via annotations but has no disclosure-analysis pass; Leo uses a structural record model. Only Compact has compile-time disclosure rejection. The table must distinguish the three approaches.

3. **[P1] (A) ZKIR instruction count mismatch** — `ch03-midnight-compiler-ir-circuit` claims 24 typed instructions but enumerates only 17. Either the total or the enumeration is wrong; this is a verifiable technical claim that must be reconciled.

4. **[P1] (A) Plonky3/Stwo misattribution** — `ch03-under-constrained-circuits-the-dominant-failure-mode` lists Stwo as using Plonky3. Stwo uses circle STARKs over Mersenne-31, not Plonky3. SP1 uses Plonky3; Stwo does not.

5. **[P1] (C) Duplicated opening in developer-experience section** — `ch03-the-developer-s-actual-experience` repeats the same sentence twice in back-to-back lines, a clear drafting artifact that signals copy-paste origin.

### Cross-section patterns

- **Citation gap throughout**: Five of seven sections have empty "Sources cited" fields despite making specific quantitative claims (cycle counts, TVL figures, vulnerability percentages, tool scores). The Chaliasos SoK is the only cited source across the chapter, and even it appears without a full reference.
- **Tornado Cash used twice**: The one-character bug is narrated in both `ch03-from-circuits-to-virtual-machines-a-brief-evolution` and `ch03-under-constrained-circuits-the-dominant-failure-mode`. One occurrence should be cut or cross-referenced.
- **Cairo/Goldilocks error in two sections**: The same factual error about Cairo's field choice appears independently in sections 2 and 3, suggesting the claim was drafted without cross-checking.
- **Clarity/AI-smell items cluster in section 3**: The longest section (`ch03-the-four-philosophies`) has the most structural issues — a misplaced paragraph, a contradictory "1.0 pre-released" label, and an empty Sources field despite ~3700 words of specific claims.
- **Depth uneven for Philosophy D**: Compact receives two dedicated follow-on sections (disclosure analysis, compiler/IR); Noir and Leo are covered only within `ch03-the-four-philosophies`. This asymmetry is defensible given Midnight's role as the running example but should be acknowledged as a framing choice rather than appearing accidental.
