---
title: "Layer 5 -- The Sealed Certificate"
chapter: 6
kind: chapter-hub
status: reviewed
---

# Chapter 6: Layer 5 -- The Sealed Certificate

## Sections

- [[ch06-sealing-the-certificate]]
- [[ch06-the-three-families]]
- [[ch06-the-hybrid-pipeline]]
- [[ch06-recursion-vs-folding-russian-dolls-and-snowballs]]
- [[ch06-the-folding-genealogy]]
- [[ch06-nightstream-what-a-folding-engine-looks-like-from-the-inside]]
- [[ch06-circle-starks-and-stwo-a-generational-leap]]
- [[ch06-real-time-ethereum-proving]]
- [[ch06-the-proof-core-why-layers-4-5-and-6-are-inseparable]]
- [[ch06-fiat-shamir-vulnerabilities]]
- [[ch06-case-study-midnight-s-sealed-certificate]]
- [[ch06-snark-recursion-vs-folding-the-full-picture]]
- [[ch06-the-post-quantum-horizon]]
- [[ch06-from-speed-race-to-security-race]]
- [[ch06-the-sealed-certificate]]

## Revision status

Phase 3 revision applied 2026-04-19 per `wiki/drafts/ch06-v2.md`. 0 P0 + 6 P1 resolved. Draft preserved. P2 (27) and P3 (16) deferred.

**Key corrections:** Trail of Bits Frozen Heart / gnark GHSA-7p92-x423-vwj6 / Solana ZK ElGamal postmortems all cited with URLs in body. Nightstream Lean boundary duplicate paragraphs merged. Zexe cited as "IEEE S&P 2020, preprint 2018; ePrint 2018/962". LatticeFold venue reconciled to ASIACRYPT 2025 (verified against Springer proceedings); LatticeFold+ disambiguated as CRYPTO 2025. ProtoGalaxy authors confirmed as Eagen and Gabizon only (verified via DBLP; reviewer's claim of third author "Dorota Filipczak" was incorrect). Hybrid pipeline timing and cost figures cited to SP1 Hypercube blog and Ethproofs.

## Audit rollup (pre-revision)

**Totals:** P0=0, P1=6, P2=27, P3=16

**Top 5 sections by issue count:**
1. ch06-the-folding-genealogy — 5 issues (venue error on LatticeFold, incomplete ProtoGalaxy author list, missing Symphony citation, sumcheck date ambiguity, axes framework not closed)
2. ch06-the-three-families — 5 issues (heavy bolding/AI smell, two C-class smells, BN254 security claim needs citation, EIP-1108 cost unsourced, analogy crowds technical depth)
3. ch06-circle-starks-and-stwo — 5 issues ("key insight" smell, two unsourced benchmark claims, circle-group isomorphism imprecision, BabyBear FFT-domain comparison thin)
4. ch06-the-hybrid-pipeline — 5 issues (no sources for any timing/cost figures, Polygon claim needs qualification, AI smell, gas-price anchor missing, hardware baseline inconsistency)
5. ch06-nightstream — 4 issues (Lean boundary duplicated nearly verbatim, "Twist and Shout" name clarity, no repository link, light rhetorical framing)

**Patterns:**
- B (citations): dominant issue class — 12 of 49 items; unsourced benchmarks, vulnerability disclosures, and performance claims appear throughout
- C (AI smells): "key insight", "it is worth spelling out/understanding why", excessive bolding in three-families; scattered but not systemic
- A (accuracy): citation venue errors (Zexe S&P year, LatticeFold venue) and incomplete author lists are the sharpest accuracy problems
- D (coherence): two sections (nightstream, snark-recursion) have near-verbatim internal duplication that should be resolved
- E (depth): several short sections (from-speed-race, real-time-proving, sealed-certificate closing) delegate substance to adjacent sections without adding enough of their own
