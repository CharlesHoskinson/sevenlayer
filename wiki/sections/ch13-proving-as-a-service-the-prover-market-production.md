---
title: "Proving-as-a-Service: The Prover Market (Production)"
slug: ch13-proving-as-a-service-the-prover-market-production
chapter: 13
chapter_title: "The Market Landscape"
heading_level: 2
source_lines: [5064, 5093]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 1170
---

## Proving-as-a-Service: The Prover Market (Production)

Here the privacy tradeoff from Chapter 4 returns with full force. Generating ZK proofs is computationally expensive but highly parallelizable, so a natural market has emerged: delegate your proving to someone with better hardware. The efficiency gain is real. The trust consequence is this: the person who proves for you sees your data.

The Chapter 4 paradox returns with full force here. The architecture that protects your data the most -- client-side proving, where your secrets never leave your device -- requires hardware that most people do not own. The architecture that works on any device -- delegated proving -- requires trusting the prover with your secrets. Chapter 4 called this out as the economic structure of privacy in 2026. Here it becomes a business model.

**Succinct** operates the leading prover network. By early 2026, the Succinct Network had generated over 6 million proofs on mainnet, secured over $4 billion in value, and launched the $PROVE token. The network's SP1 Hypercube zkVM powers multiple rollup deployments.

**RISC Zero Boundless** launched its open proof marketplace in September 2025. Boundless processed 542.7 trillion cycles by December 2025, then forced migration from its centralized prover service to the decentralized marketplace. This migration -- shutting down the centralized option to force adoption of the decentralized alternative -- is a notable governance decision. Trust in a centralized prover was replaced by trust in a marketplace mechanism. Whether that is an improvement depends on what you think markets are.

**ZkCloud** (formerly Gevulot) provides production-ready proving infrastructure with its Firestarter platform.

**Aligned Layer** takes a different approach: it uses EigenLayer restaking ($11 billion+ restaked ETH) to provide proof verification as a service, allowing any application to submit proofs for verification without deploying its own verifier contract.

The proving market is transitioning from an infrastructure cost (borne by rollup operators) to a tradeable service (priced by market dynamics). The $PROVE token represents the first attempt to create a liquid market for computational integrity. You can now buy and sell the ability to generate mathematical truth. But the trust has been delegated to prover hardware, and the privacy question -- who sees the witness? -- has no market solution. It has only engineering solutions, each with its own trust assumptions. TEEs, MPC-based proving, client-side hardware acceleration: each moves the trust, none eliminates it.

The economics of proving-as-a-service deserve to be spelled out, because they determine who actually pays for mathematical truth -- and at what margin. The cost structure has three layers: hardware (GPU clusters, typically H100 or A100 machines running at $2-3 per GPU-hour on cloud providers, less for owned hardware with amortized capex), energy (a single H100 draws roughly 700W under proving load; at industrial electricity rates of $0.05-0.08/kWh, that is $0.035-0.056 per GPU-hour), and engineering (the prover software itself, maintained by teams of 10-50 engineers at salaries that dwarf the hardware costs). The first two are commodity inputs. The third is the moat.

Who pays? Today, the answer is straightforward: rollup operators pay. A ZK rollup that generates proofs for every batch of transactions absorbs proving costs as an operational expense, recouped through user transaction fees. At current rates, proving costs for a major rollup run $200,000-$500,000 per year -- significant, but a small fraction of the sequencer revenue for any rollup with meaningful throughput. The user pays indirectly, through transaction fees that embed a proving surcharge. That surcharge has been falling: the 2,000-fold cost collapse described in Chapter 6 means the proving component of a typical L2 transaction fee has dropped from dollars to fractions of a cent. The user, in most cases, does not notice.

But as ZK proofs extend beyond rollups into coprocessors, ZKML, identity, and enterprise applications, the payment model diversifies. A DeFi protocol using a ZK coprocessor to compute a verified TWAP pays per query -- perhaps $0.10-$1.00 per coprocessor call, depending on the computation's complexity. An enterprise using ZK proofs for compliance verification pays per attestation -- perhaps $5-50 per KYC proof, still far cheaper than the manual compliance process it replaces. A ZKML application proving model inference pays per inference -- and here the costs are still high enough to be prohibitive for all but the most valuable use cases, because the computational overhead of proving neural network operations remains steep.

The margin structure is revealing. Hardware and energy costs are transparent and declining. The margin on proving-as-a-service therefore comes from three sources: software differentiation (a faster prover generates more proofs per GPU-hour, extracting more revenue from the same hardware), network effects (a larger prover network attracts more proof requests, spreading fixed costs across more revenue), and trust premiums (a prover network with a longer track record and more stake at risk can charge more than a new entrant, because the customer is paying not just for computation but for reliability). The first source rewards engineering excellence. The second rewards early movers. The third -- and this is the one that connects to our thesis -- rewards *visible trustworthiness*. The margin on proving-as-a-service is, in part, a margin on trust. The customer pays more to a prover they trust more. Trust has not been eliminated. It has been priced.

Current gross margins for proving services are estimated at 40-60% for operators with owned hardware, dropping to 15-25% for operators renting cloud GPU capacity. As the market matures and competition intensifies, margins will compress toward the cloud-rental floor -- unless operators differentiate on software speed, privacy guarantees, or the economic security of their staking mechanisms. The $PROVE token's role in this dynamic is worth watching: it attempts to align prover incentives with network reliability through slashing (stake at risk if proofs are invalid or late), which is an economic mechanism for trust. You do not trust the prover's goodwill. You trust the prover's financial exposure. Whether that is trust-minimized or merely trust-financialized is a question the market has not yet answered.

The long-term equilibrium may resemble cloud computing: a few large operators (Succinct, RISC Zero, ZkCloud) competing on price and performance, with specialized boutique provers serving niche markets (enterprise privacy, ZKML, identity). The commodity layer -- raw proof generation -- will be a low-margin, high-volume business. The value layer -- proof orchestration, privacy-preserving proving, domain-specific optimization -- will be a higher-margin, lower-volume business. In both layers, the customer pays for computation and receives a proof. But in the value layer, the customer also pays for the *conditions* under which the proof was generated: was the witness kept private? Was the hardware audited? Was the proving pipeline formally verified? These conditions are trust assumptions, and they carry a price. The proving market does not sell trustlessness. It sells *degrees of trust*, at different price points, to customers with different risk tolerances. This is an honest market. It is not the market the cypherpunks imagined.

Where did the trust go? From self-hosted proving infrastructure to proving marketplace operators and hardware availability. The cost efficiency is real; so are the new dependencies on prover liveness and correctness.


## Summary

The proving-as-a-service market shifts proof generation from self-hosted infrastructure to competitive marketplaces. Succinct's network exceeded 6 million proofs and $4B secured value; RISC Zero Boundless processed 542.7 trillion cycles by December 2025 before forcing decentralization. Trust is not eliminated but priced: providers charge a premium for track record and stake at risk, and the witness-privacy problem has no market solution — only engineering trade-offs.

## Key claims

- Succinct Network: >6M proofs on mainnet, >$4B secured, $PROVE token launched by early 2026.
- RISC Zero Boundless processed 542.7 trillion cycles by December 2025 then shut centralized prover to force marketplace adoption.
- Aligned Layer uses EigenLayer restaking ($11B+ ETH) for proof verification as a service.
- Rollup proving costs: $200,000–$500,000/year for major rollups; per-L2-tx proving fee is now fractions of a cent.
- Gross margins: 40–60% for owned-hardware operators, 15–25% for cloud-GPU operators.
- Trust is priced, not eliminated: longer track record and slashing stake command higher fees.
- Witness privacy (who sees the inputs) has no market solution; TEEs and MPC-based proving move but do not eliminate that trust.

## Entities

- [[h100]]
- [[mpc]]

## Dependencies

- [[ch04-the-disclose-boundary-midnight-s-witness-architecture]] — Chapter 4 privacy paradox: client-side vs. delegated proving
- [[ch06-the-three-families]] — cost-collapse figures (2,000x) referenced from Chapter 6
- [[ch13-zk-rollups-the-proving-grounds-production]] — rollup operators are primary current paying customers
- [[ch13-market-sizing]] — $97M proving-services sub-market and Chorus One projections

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [P1] (C) Paragraphs 1 and 2 both open with the same idea ("the Chapter 4 privacy tradeoff returns with full force"), nearly verbatim. The second paragraph is redundant with the first and should be merged or cut.
- [P2] (B) No sources for: RISC Zero Boundless 542.7 trillion cycles, Aligned Layer $11B+ EigenLayer restaking figure, rollup proving costs $200K–$500K/year, GPU rental rates, H100 power draw, or gross margin estimates (40–60%/15–25%). This section has the highest density of specific quantitative claims and fewest citations of any ch13 section.
- [P2] (A) Gross margin estimates (40–60% owned hardware, 15–25% cloud) are presented as established figures but are apparently internal estimates with no sourcing; they should be flagged as estimates or attributed.
- [P3] (A) "542.7 trillion cycles by December 2025" is unusually precise for an uncited claim; if this is from a RISC Zero announcement it should be cited directly.

## Links

- Up: [[13-the-market-landscape]]
- Prev: [[ch13-zk-identity-growth-regulatory-mandate]]
- Next: [[ch13-enterprise-pilots-pilot]]
