---
title: "Market Sizing"
slug: ch13-market-sizing
chapter: 13
chapter_title: "The Market Landscape"
heading_level: 2
source_lines: [5118, 5160]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 956
---

## Market Sizing

The zero-knowledge proof market is growing fast from a small base:

| Year | Market Size | Source |
|------|------------|--------|
| 2024 | $1.28 billion (total ZKP market) | Grand View Research [42] |
| 2025 | $1.54 billion (total ZKP market) | Grand View Research [42] |
| 2025 | $97 million (proving services only) | Chorus One |
| 2030 | $1.34 billion (proving services only) | Chorus One |
| 2033 | $7.59 billion (total ZKP market) | Grand View Research [42] |

> **Note on sources**: The total ZKP market figures ($1.28B, $1.54B, $7.59B) are from Grand View Research's "Zero-Knowledge Proof Market Size Report" (2025), which covers all ZKP segments at a 22.1% CAGR. The proving-services sub-market figures ($97M, $1.34B) are from Chorus One's "The Economics of ZK-Proving: Market Size and Future Projections" (2025), which covers the narrower ZK proving services segment at a higher CAGR. Earlier versions of this table conflated the two sources.

The Grand View Research figures cover the full ZK ecosystem: proof generation hardware and services, ZK rollup infrastructure, ZK identity systems, ZKML tooling, and enterprise licensing. The Chorus One figures cover the narrower proving-services sub-market. For context, the approximate segment breakdown of the $1.54 billion total market (2025) by revenue source:

| Segment | Estimated Share | Primary Revenue Source |
|---------|----------------|----------------------|
| ZK Rollups | ~60% | Transaction fees + sequencer revenue |
| Proving-as-a-Service | ~20% | Infrastructure fees + token mechanisms |
| ZK Identity | ~10% | Credential issuance + verification fees |
| Enterprise/Compliance | ~5% | Licensing + integration fees |
| Coprocessors | ~3% | Per-query proving fees |
| ZKML | ~2% | Research grants (pre-revenue) |

These estimates are approximate — no authoritative segment breakdown exists yet, and the boundaries between segments are porous (a rollup's proving costs may be counted as either rollup infrastructure or proving-as-a-service depending on the source). The key observation is that rollup transaction fees dominate the current market, but the fastest-growing segments by percentage are proving-as-a-service and identity, both driven by expanding use cases beyond the original blockchain scaling thesis.

The Grand View Research CAGR of 22.1% assumes continued blockchain adoption plus emerging non-blockchain applications (enterprise compliance, identity wallets, verifiable AI). The Chorus One projections for the proving sub-market assume steeper growth (approximately 55% CAGR from $97M to $1.34B over five years) driven by the transition from self-hosted proving to marketplace-based proving-as-a-service. Both projections assume no major cryptographic break (quantum or otherwise) and continued regulatory tailwinds from eIDAS 2.0 and MiCA.

The cost trajectory suggests that ZK proving is following a classic deflationary technology curve -- the same pattern that drove computing from mainframes to smartphones. As costs approach zero, the binding constraint shifts from "can we afford to prove this?" to "what else can we prove?" This shift is what drives the expansion from rollups (proving transaction execution) into coprocessors (proving data queries), ZKML (proving model inference), and identity (proving personal attributes).

But the market numbers, by themselves, tell you nothing about trust. A $7.59 billion market in which trust has merely been moved from one institution to another is not the same as a $97 million market in which trust has genuinely been minimized. The thesis of this chapter -- that the market reveals where trust is actually being minimized and where it is merely being relocated -- should make you read these projections with a specific question: in each segment, what trust assumption remains that the buyer does not examine?

The enterprise market is the largest long-term opportunity but the slowest to materialize. Financial institutions move on regulatory timelines (years, not months), require extensive compliance review, and demand vendor stability. The fact that major banks are conducting ZK pilots -- rather than dismissing the technology -- suggests the institutional adoption curve has begun, but the revenue impact will take 3-5 years to manifest at scale.

Six venues. Six audiences. In two of them -- rollups and proving-as-a-service -- the technology is production-grade and the trust reduction is measurable: cryptographic proofs replace re-execution, and the economics are favorable. In two -- identity and enterprise compliance -- the trust minimization is genuine but the adoption path depends on regulatory mandates (eIDAS 2.0, DTCC pilots) rather than pure market forces. In two -- coprocessors and ZKML -- the technology works but the trust story is incomplete: new dependencies on data availability, model integrity, and prover correctness introduce assumptions that are not yet well-tested at scale. The market is honest about what it sells. The question is whether buyers are honest about what they are buying.

The market is real, growing, and diversifying beyond its blockchain origins. The magician now performs in six different venues -- rollups, coprocessors, ML inference, identity wallets, proving marketplaces, and boardrooms -- for six different audiences with six different trust requirements. In some venues, trust is being genuinely minimized. In others, it is being moved to a new location and given a new name. The numbers tell us where the technology is being adopted. They do not tell us where it is honest. For that, we need to ask different questions -- not "how big is the market?" but "what remains unsolved?" Those questions are the subject of our final chapter.

The market is growing. The technology works. The money is real. But beneath every market segment, open questions persist -- questions about governance, quantum vulnerability, privacy guarantees, and whether the trust minimization marketed to buyers matches the trust decomposition the mathematics actually delivers. The final chapter names these questions, assesses which are solvable and which may be permanent, and draws the line between what zero-knowledge proofs have achieved and what remains to be built.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
