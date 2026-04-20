---
title: "Privacy-Enhancing Technologies"
chapter: 9
kind: chapter-hub
status: reviewed
---

# Chapter 9: Privacy-Enhancing Technologies

## Sections

- [[ch09-the-four-pillars]]
- [[ch09-three-kinds-of-security]]
- [[ch09-composability-when-one-pet-is-not-enough]]
- [[ch09-real-world-deployments-five-case-studies]]
- [[ch09-privacy-architectures-for-smart-contracts-kachina-and-zexe]]
- [[ch09-the-regulatory-intersection]]
- [[ch09-the-decision-matrix]]
- [[ch09-open-problems]]
- [[ch09-the-incomplete-stack]]

## Revision status

Phase 3 revision applied 2026-04-19 per `wiki/drafts/ch09-v2.md`. 0 P0 + 6 P1 resolved (the audit rollup listed 4 P1; the final backlog pass caught 2 additional P1s which were also cleared). Draft preserved. P2 (8) and P3 (2) deferred.

**Key corrections:** Ozdemir-Boneh collaborative zk-SNARKs cited to USENIX 2022 / ePrint 2021/1530; Zexe cited as "IEEE S&P 2020, preprint 2018; ePrint 2018/962" (matches ch06); "BLS-12" replaced with specific BLS12-377 + BW6-761 context; Gentry FHE cited to STOC 2009 (matches bibliography); Battering RAM currency unified to €50 with De Meulemeester et al. 2025 attribution; TEE attacks (Foreshadow, AEPIC Leak, Downfall/CVE-2022-40982, SGAxe, Plundervolt, Battering RAM, SGX deprecation) all cited inline.

**Regression fix:** Part III divider + transitional italic block were accidentally dropped from the splice and restored inline post-splice.

## Audit rollup (pre-revision)

Audited 2026-04-18. 9 sections, 14 findings total: P0=0, P1=4, P2=8, P3=2.

| Section | Findings |
|---------|----------|
| ch09-the-four-pillars | P1 (B) Gentry thesis vs STOC 2009 mismatch; P2 (B) Yao/Dwork/Dinur absent from chapter bibliography; P2 (C) "key insight" AI smell |
| ch09-three-kinds-of-security | P1 (A) Battering Ram cost inconsistent (€50 body vs $50 key claims); P1 (B) no sources for all named TEE attacks; P2 (D) SGX deprecation detail never reconnects to security-tier taxonomy |
| ch09-composability-when-one-pet-is-not-enough | P2 (B) no sources for zkFHE gate count claim; P2 (E) privacy stack ordering uncited |
| ch09-real-world-deployments-five-case-studies | P2 (A) spurious `[[nova]]` entity; P3 (B) Privacy Pools volume figure unsourced |
| ch09-privacy-architectures-for-smart-contracts-kachina-and-zexe | P1 (B) Zexe venue "2018" should be IEEE S&P 2020; P1 (A) "BLS-12" ambiguous, should be BLS12-377; P2 (B) duplicate dependency slug (ch03 vs ch04 for same section); P3 (B) Kachina affiliation unverified |
| ch09-the-regulatory-intersection | P2 (A) eIDAS "effective 2024" potentially misleading re wallet deployment deadline; P3 (B) Galactica/zyphe/hyli cited without references |
| ch09-the-decision-matrix | P2 (A) TEE <5% overhead conflicts with Downfall mitigation data in same chapter; P2 (B) no sources for performance figures |
| ch09-open-problems | P1 (B) Ozdemir-Boneh USENIX 2022 absent from master bibliography; P2 (B) EUROCRYPT 2026 PIR paper unnamed and unverifiable |
| ch09-the-incomplete-stack | clean |
