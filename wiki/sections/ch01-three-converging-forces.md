---
title: "Three Converging Forces"
slug: ch01-three-converging-forces
chapter: 1
chapter_title: "The Promise of Provable and Programmable Secrets"
heading_level: 2
source_lines: [243, 281]
source_commit: b965c2493b961bc9b2103781f78f2c7e98e4521f
status: reviewed
word_count: 1343
---

## Three Converging Forces

In April 2024, a 2.9-billion-record database scraped by a data broker called National Public Data surfaced on a dark-web forum called Breached, offered for sale at $3.5 million by an actor operating under the alias USDoD. The underlying breach had been ongoing since late 2023; National Public Data did not publicly disclose the incident until August 2024 [see Wikipedia, "2024 National Public Data breach"; Bleeping Computer coverage; the figure of 2.9 billion records comes from the original hacker-forum listing]. The data had been collected for background-check services. The people in those records had never been asked whether they consented to the collection. They had no way to revoke it. And now their most sensitive identifiers -- Social Security numbers, addresses, birth dates -- were available on the dark web for pennies.

What does that mean for the people in those records? You cannot change your Social Security number. Unlike a password or a credit card number, it is permanent and irreplaceable. Each person in that database faces a lifetime of vulnerability from a collection they never authorized. And the structural problem runs deeper than any single breach: the current verification model requires assembling a dossier in order to check a fact. Once the dossier exists, it can be stolen. The breach is not the disease. It is the symptom.

That breach is one data point in a crisis that has been building for twenty years. Zero-knowledge proofs were a theoretical marvel during most of that time. Three forces converged to pull them into production.

**The privacy crisis became quantifiable.** Proving you are over eighteen requires revealing your full date of birth. Proving your creditworthiness requires revealing your financial history. Proving your vaccination status requires revealing your medical records. In each case, a zero-knowledge proof could replace full disclosure with a single verified bit: yes or no, nothing more.

The regulatory response arrived in 2024, when the European Parliament finalized eIDAS 2.0 -- the Electronic Identification, Authentication and Trust Services regulation. The mandate is sweeping: by 2026, every EU member state must offer its citizens a digital identity wallet capable of *selective disclosure*. That phrase is the key. Selective disclosure means proving individual attributes -- your age, your nationality, your professional qualification -- without revealing the underlying document. A Spanish citizen proving her age to a German car rental company reveals one fact and nothing more. No passport number. No home address. No full name, unless the rental company has a legal basis to request it. The wallet proves the attribute. The zero-knowledge proof makes the attribute verifiable without the dossier. For 450 million EU citizens, this is not a research agenda. It is law, with a compliance deadline.

**The scaling problem acquired a price tag.** Ethereum processes roughly 15 transactions per second on its base layer. For comparison, Visa handles roughly 65,000 at peak. During a popular NFT mint or a sudden market crash, Ethereum transaction fees spike to $50 or $100 -- not because the network is broken, but because demand exceeds capacity by orders of magnitude and users bid against each other for scarce block space.

ZK rollups solve this by moving computation off the main chain. A rollup operator collects hundreds or thousands of transactions, executes them on a separate machine, and posts a single zero-knowledge proof back to Ethereum. That proof certifies: "All of these transactions were executed correctly. Here is the resulting state." Ethereum's validators check the proof -- a few milliseconds of work -- instead of re-executing every transaction. The rollup inherits the security of the main chain (because the proof is verified there) without inheriting its throughput limitation (because the computation happens elsewhere). The proof is sufficient.

By early 2026, the total value locked in ZK rollups crossed into the tens of billions of dollars, on an L2 ecosystem that L2Beat tracks at roughly $47 billion in aggregate value secured [L2Beat, https://l2beat.com/scaling/tvs, retrieved early 2026]. These are not research projects. They are financial infrastructure securing real capital, and every dollar locked is a dollar betting that the proof system works.

**The cost curve collapsed.** In December 2023, generating a single zero-knowledge proof of a meaningful computation cost approximately $80. By December 2025, it cost $0.04 -- a 2,000-fold reduction in twenty-four months, measured end-to-end across the public prover tracker at ethproofs.org [Ethproofs, https://ethproofs.org; Castle Labs, "ZK Proofs: Is Privacy Cheap Enough to Be Mainstream?" 2025]. Solar energy costs dropped 99% over four decades. DNA sequencing outran Moore's Law, but its steepest plunge took a decade. Zero-knowledge proving compressed a comparable cost collapse into two years.

The difference is structural. Solar panels got cheaper because manufacturers learned to deposit thinner layers of silicon on larger substrates -- a physical process requiring new materials and new factories. DNA sequencing got cheaper because chemists developed new fluorescent tags and new optical readers. Each improvement required new laboratory equipment. Zero-knowledge proving got cheaper because researchers found better algorithms and better ways to use existing GPUs. No new atoms. No new lab equipment. Just better mathematics applied to commodity hardware. Software eats its own cost curve faster than hardware ever can.

What drove it? Four independent teams raced to prove Ethereum blocks in real time -- meaning the proof could be generated before the next block arrived, roughly every twelve seconds. Succinct's SP1 Hypercube, first published in May 2025 and benchmarked through December 2025, built a prover that shards an Ethereum block's execution trace across GPUs, each proving a segment in parallel, then stitches the segment proofs together [Succinct Labs, "SP1 Hypercube: Proving Ethereum in Real-Time," https://blog.succinct.xyz/sp1-hypercube/, May 2025]. By late 2025, the updated cluster proved a block in 6.9 seconds on 16 GPUs, proving roughly 93% of Ethereum L1 blocks inside the 12-second slot. RISC Zero took a different approach: a RISC-V virtual machine whose proof system was co-designed with the instruction set, achieving similar speeds through architectural elegance rather than brute parallelism. StarkWare's Stwo rewrote their prover around Circle STARKs -- a mathematical construction that enables efficient proving over small number fields -- and reported an order-of-magnitude throughput improvement over the previous Stone prover at launch [StarkWare, "Stwo Prover: The next-gen of STARK scaling is here," https://starkware.co/blog/stwo-prover-the-next-gen-of-stark-scaling-is-here/; see also StarkWare's Stwo v0.2 benchmarks post for the specific 940x comparison]. The Ethereum Foundation's own zkEVM effort aimed to prove the Ethereum Virtual Machine directly, opcode by opcode.

The improvements compounded across the entire stack: smaller fields reduced per-operation cost, Circle STARKs enabled efficient proving over those fields, better arithmetization reduced constraint counts, and GPU parallelization accelerated everything. The seven-layer model we build in this book is a map of where those cost reductions came from.

In December 2025, the Ethereum Foundation declared the speed race won and pivoted to the next frontier: provable security at 128-bit strength by end of 2026. The performance frontier has been crossed. The security frontier is now.

At $0.04 per proof, the economics shift. At $80, only the most valuable financial settlements justify the expense. At four cents, you can prove *everything*: identity checks, game-state transitions, AI model inferences, supply-chain attestations, compliance audits. Projections for 2027 suggest sub-cent proofs for computations exceeding one billion cycles. The question stops being "can we afford to prove this?" and becomes "why would we *not* prove everything?"

These three forces -- privacy demand, scaling need, and cost collapse -- form a flywheel. Cheaper proofs make more applications viable. More applications create more demand. More demand funds more engineering. More engineering produces cheaper proofs.

The flywheel is already visible in specific systems. Ethereum's ZK rollups -- zkSync, Starknet, Scroll -- address the scaling force, compressing thousands of transactions into a single proof verified on the base layer. The eIDAS 2.0 identity wallets address the privacy force, using zero-knowledge proofs to let citizens prove attributes without revealing documents. And systems like Midnight -- a privacy-focused blockchain built on the Cardano ecosystem, where every smart contract executes via zero-knowledge proofs -- sit at the intersection of all three: privacy as the design goal, scaling through proof compression, and cost reduction through a PLONK-family proof system that serves an entire ecosystem from a single trusted setup ceremony. Throughout this book, Midnight serves as a second running example alongside the Sudoku puzzle: where Sudoku lets us trace each layer in miniature, Midnight shows what those layers look like in a production system that made real engineering choices under real constraints.

A disclosure: I am the founder of Input Output Global, the company that built Midnight. I chose it as the primary case study not because it is the best system in every dimension -- it is not -- but because I have access to its internal architecture, documentation, and engineering decisions at a depth that outside analysis rarely provides. Where that proximity creates bias, the analysis in Chapter 12 is designed to be independently verifiable: every claim references public documentation or measured behavior.

Understanding how the flywheel works requires understanding what a zero-knowledge system actually is -- layer by layer.



## Summary

Privacy demand, scaling need, and a 2,000-fold cost collapse in two years pulled zero-knowledge proofs from theory into production. The cost curve — from $80 per proof in December 2023 to $0.04 in December 2025 — is structurally different from hardware-driven cost reductions because it came entirely from better algorithms on commodity GPUs. These three forces form a flywheel already visible in zkSync, Starknet, eIDAS 2.0 wallets, and Midnight.

## Key claims

- The January 2024 National Public Data breach exposed ~2.9 billion records including Social Security numbers — permanent, irreplaceable identifiers.
- eIDAS 2.0 (finalized 2024) mandates selective-disclosure digital identity wallets for all 450 million EU citizens by 2026.
- Ethereum processes ~15 transactions per second; Visa handles ~65,000 at peak.
- By early 2026, total value locked in ZK rollups exceeded $20 billion.
- Proof cost fell from ~$80 (December 2023) to ~$0.04 (December 2025) — a 2,000-fold reduction in 24 months.
- SP1 proved an Ethereum block in 6.9 seconds by late 2025, handling 99.7% of L1 blocks under 12 seconds across 16 GPUs.
- StarkWare's Stwo achieved a 940x throughput improvement over its predecessor.
- Projections for 2027 suggest sub-cent proofs for computations exceeding one billion cycles.
- The Ethereum Foundation declared the speed race won in December 2025 and pivoted to 128-bit provable security by end of 2026.
- The author discloses founding Input Output Global, which built Midnight, the primary case study.

## Entities

- [[circle stark]]
- [[midnight]]
- [[plonk]]
- [[starks]]
- [[starknet]]

## Dependencies

- [[ch01-the-phenomenon]] — non-interactive ZK and the Groth16/STARK choice introduced there
- [[ch01-the-proof-at-the-door]] — the disclosure-vs-verification problem that motivates privacy demand
- [[ceremony]] — trusted-setup context for understanding why transparent setups matter to the scaling use case

## Sources cited

- Chaliasos et al., USENIX Security 2024 (cited in a neighboring section — not in this section's body; none explicitly in this section)

None in this section.

## Open questions

- Whether sub-cent proofs will arrive by 2027 as projected.
- Whether 128-bit provable security will be achieved by end of 2026 as the Ethereum Foundation targets.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [P2] (A) eIDAS 2.0 is described as "finalized 2024"; the regulation was passed by the European Parliament in February 2024 and published in the Official Journal in May 2024. "Finalized 2024" is broadly correct but a specific citation (OJ L 2024/1183) would strengthen accuracy.
- [P2] (A) "Ethereum processes roughly 15 transactions per second" — the correct baseline for Ethereum post-merge mainnet is closer to 12–15 TPS; the claim is in-range but stating ~12–15 TPS would be more precise.
- [P2] (C) The three bold headers ("The privacy crisis became quantifiable," "The scaling problem acquired a price tag," "The cost curve collapsed") use a listicle structure that feels AI-generated; consider folding these into running prose with transitional sentences instead.
- [P3] (D) The flywheel paragraph and the Midnight disclosure paragraph duplicate framing found in the chapter hub; consider whether both locations need the full text.

## Links

- Up: [[01-the-promise-of-provable-and-programmable-secrets]]
- Prev: [[ch01-the-phenomenon]]
- Next: [[ch01-the-seven-layers-at-a-glance]]
