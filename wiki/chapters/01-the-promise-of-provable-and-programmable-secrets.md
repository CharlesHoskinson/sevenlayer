---
title: "The Promise of Provable and Programmable Secrets"
chapter: 1
kind: chapter-hub
status: reviewed
---

# Chapter 1: The Promise of Provable and Programmable Secrets

## Sections

- [[ch01-the-trick]]
- [[ch01-the-proof-at-the-door]]
- [[ch01-the-phenomenon]]
- [[ch01-three-converging-forces]]
- [[ch01-the-seven-layers-at-a-glance]]
- [[ch01-the-deepest-question]]
- [[ch01-the-first-decision]]
- [[ch01-how-to-read-this-guide]]

## Revision status

Phase 3 revision applied 2026-04-18. All 2 P0 and 16 P1 findings resolved per `wiki/drafts/ch01-v2.md` ledger. Draft preserved for audit. Remaining P2 (23) and P3 (6) items deferred to future polish pass.

**Two new items introduced during revision:**
- SP1 Hypercube block-coverage claim corrected to 93% (from 99.7%) per reviewer check against source.
- Stwo 940x figure softened to "order-of-magnitude" pending primary-source verification — citation remains unresolved.

## Audit rollup (pre-revision)

**Total findings by severity:** P0: 2, P1: 16, P2: 23, P3: 6

**Top 5 most severe findings:**

1. `ch01-the-deepest-question` — `[P0] (D) The Key claims block places the 67% under-constrained circuit statistic under "Layer 1" but the body correctly assigns it to Layer 2. Direct label error that will propagate to automated summaries.`
2. `ch01-three-converging-forces` — `[P0] (A) The National Public Data breach is dated "January 2024" but public disclosure was August 2024 (USDoJ complaint); the date is unverified and likely wrong.`
3. `ch01-how-to-read-this-guide` — `[P1] (A) Describes costs as "sub-cent" under the Performance frontier, contradicting ch01-three-converging-forces which states $0.04 as of December 2025; sub-cent is a 2027 projection.`
4. `ch01-the-deepest-question` — `[P1] (A) Overhead stated as "1,000x–5,000x" but ch05-the-overhead-tax gives 10,000x–50,000x as the current range; the ch01 figures understate the upper bound.`
5. `ch01-the-phenomenon` — `[P1] (A) Groth16 attribution conflates GGPR13 (Gennaro, Gentry, Parno, Rabin, Eurocrypt 2013) with Groth16 (Groth, 2016); the 192-byte proof belongs to the 2016 paper, not the 2010–2013 constructions.`

**Cross-section patterns:**

- Missing citations (dimension B) recur across 6 of 8 sections: every quantitative claim in ch01-three-converging-forces is uncited; the GMR 1985, Fiat-Shamir 1986, and GGPR 2013 papers are named but never given ePrint/DOI/proceedings references.
- Style (dimension C) is the highest-frequency dimension (11 findings): AI-smell phrases "worth noting" appear in 2 sections; listicle bold-header structure used in ch01-three-converging-forces; aphoristic three-beat repetition in ch01-the-trick.
- The Zcash side-channel attack is described as "revealing" transaction amounts in ch01-the-seven-layers-at-a-glance but ch04-side-channel correctly reports a correlation of R = 0.57 — an overstatement appearing in 2 sections.
- Overhead figures are inconsistent between ch01-the-deepest-question (1,000x–5,000x) and ch05-the-overhead-tax (10,000x–50,000x); the discrepancy will confuse readers who read sequentially.
