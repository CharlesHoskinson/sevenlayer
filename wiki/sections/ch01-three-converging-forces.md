---
title: "Three Converging Forces"
slug: ch01-three-converging-forces
chapter: 1
chapter_title: "The Promise of Provable and Programmable Secrets"
heading_level: 2
source_lines: [241, 279]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 1343
---

## Three Converging Forces

In January 2024, a data broker called National Public Data suffered a breach that exposed the Social Security numbers, addresses, and birth dates of approximately 2.9 billion records. The data had been collected for background-check services. The people in those records had never been asked whether they consented to the collection. They had no way to revoke it. And now their most sensitive identifiers were available on the dark web for pennies.

What does that mean for the people in those records? You cannot change your Social Security number. Unlike a password or a credit card number, it is permanent and irreplaceable. Each person in that database faces a lifetime of vulnerability from a collection they never authorized. And the structural problem runs deeper than any single breach: the current verification model requires assembling a dossier in order to check a fact. Once the dossier exists, it can be stolen. The breach is not the disease. It is the symptom.

That breach is one data point in a crisis that has been building for twenty years. Zero-knowledge proofs were a theoretical marvel during most of that time. Three forces converged to pull them into production.

**The privacy crisis became quantifiable.** Proving you are over eighteen requires revealing your full date of birth. Proving your creditworthiness requires revealing your financial history. Proving your vaccination status requires revealing your medical records. In each case, a zero-knowledge proof could replace full disclosure with a single verified bit: yes or no, nothing more.

The regulatory response arrived in 2024, when the European Parliament finalized eIDAS 2.0 -- the Electronic Identification, Authentication and Trust Services regulation. The mandate is sweeping: by 2026, every EU member state must offer its citizens a digital identity wallet capable of *selective disclosure*. That phrase is the key. Selective disclosure means proving individual attributes -- your age, your nationality, your professional qualification -- without revealing the underlying document. A Spanish citizen proving her age to a German car rental company reveals one fact and nothing more. No passport number. No home address. No full name, unless the rental company has a legal basis to request it. The wallet proves the attribute. The zero-knowledge proof makes the attribute verifiable without the dossier. For 450 million EU citizens, this is not a research agenda. It is law, with a compliance deadline.

**The scaling problem acquired a price tag.** Ethereum processes roughly 15 transactions per second on its base layer. For comparison, Visa handles roughly 65,000 at peak. During a popular NFT mint or a sudden market crash, Ethereum transaction fees spike to $50 or $100 -- not because the network is broken, but because demand exceeds capacity by orders of magnitude and users bid against each other for scarce block space.

ZK rollups solve this by moving computation off the main chain. A rollup operator collects hundreds or thousands of transactions, executes them on a separate machine, and posts a single zero-knowledge proof back to Ethereum. That proof certifies: "All of these transactions were executed correctly. Here is the resulting state." Ethereum's validators check the proof -- a few milliseconds of work -- instead of re-executing every transaction. The rollup inherits the security of the main chain (because the proof is verified there) without inheriting its throughput limitation (because the computation happens elsewhere). The proof is sufficient.

By early 2026, the total value locked in ZK rollups exceeded $20 billion. These are not research projects. They are financial infrastructure securing real capital, and every dollar locked is a dollar betting that the proof system works.

**The cost curve collapsed.** In December 2023, generating a single zero-knowledge proof of a meaningful computation cost approximately $80. By December 2025, it cost $0.04. A 2,000-fold reduction in twenty-four months. Solar energy costs dropped 99% over four decades. DNA sequencing outran Moore's Law, but its steepest plunge took a decade. Zero-knowledge proving compressed a comparable cost collapse into two years.

The difference is structural. Solar panels got cheaper because manufacturers learned to deposit thinner layers of silicon on larger substrates -- a physical process requiring new materials and new factories. DNA sequencing got cheaper because chemists developed new fluorescent tags and new optical readers. Each improvement required new laboratory equipment. Zero-knowledge proving got cheaper because researchers found better algorithms and better ways to use existing GPUs. No new atoms. No new lab equipment. Just better mathematics applied to commodity hardware. Software eats its own cost curve faster than hardware ever can.

What drove it? Four independent teams raced to prove Ethereum blocks in real time -- meaning the proof could be generated before the next block arrived, roughly every twelve seconds. Succinct's SP1 Hypercube built a prover that shards an Ethereum block's execution trace across 16 GPUs, each proving a segment in parallel, then stitching the segment proofs together. By late 2025, SP1 proved a block in 6.9 seconds, handling 99.7% of Ethereum L1 blocks in under 12 seconds. RISC Zero took a different approach: a RISC-V virtual machine whose proof system was co-designed with the instruction set, achieving similar speeds through architectural elegance rather than brute parallelism. StarkWare's Stwo rewrote their prover around Circle STARKs -- a mathematical construction that enables efficient proving over small number fields -- and achieved a 940x throughput improvement over their previous system. The Ethereum Foundation's own zkEVM effort aimed to prove the Ethereum Virtual Machine directly, opcode by opcode.

The improvements compounded across the entire stack: smaller fields reduced per-operation cost, Circle STARKs enabled efficient proving over those fields, better arithmetization reduced constraint counts, and GPU parallelization accelerated everything. The seven-layer model we build in this book is a map of where those cost reductions came from.

In December 2025, the Ethereum Foundation declared the speed race won and pivoted to the next frontier: provable security at 128-bit strength by end of 2026. The performance frontier has been crossed. The security frontier is now.

At $0.04 per proof, the economics shift. At $80, only the most valuable financial settlements justify the expense. At four cents, you can prove *everything*: identity checks, game-state transitions, AI model inferences, supply-chain attestations, compliance audits. Projections for 2027 suggest sub-cent proofs for computations exceeding one billion cycles. The question stops being "can we afford to prove this?" and becomes "why would we *not* prove everything?"

These three forces -- privacy demand, scaling need, and cost collapse -- form a flywheel. Cheaper proofs make more applications viable. More applications create more demand. More demand funds more engineering. More engineering produces cheaper proofs.

The flywheel is already visible in specific systems. Ethereum's ZK rollups -- zkSync, Starknet, Scroll -- address the scaling force, compressing thousands of transactions into a single proof verified on the base layer. The eIDAS 2.0 identity wallets address the privacy force, using zero-knowledge proofs to let citizens prove attributes without revealing documents. And systems like Midnight -- a privacy-focused blockchain built on the Cardano ecosystem, where every smart contract executes via zero-knowledge proofs -- sit at the intersection of all three: privacy as the design goal, scaling through proof compression, and cost reduction through a PLONK-family proof system that serves an entire ecosystem from a single trusted setup ceremony. Throughout this book, Midnight serves as a second running example alongside the Sudoku puzzle: where Sudoku lets us trace each layer in miniature, Midnight shows what those layers look like in a production system that made real engineering choices under real constraints.

A disclosure: I am the founder of Input Output Global, the company that built Midnight. I chose it as the primary case study not because it is the best system in every dimension -- it is not -- but because I have access to its internal architecture, documentation, and engineering decisions at a depth that outside analysis rarely provides. Where that proximity creates bias, the analysis in Chapter 12 is designed to be independently verifiable: every claim references public documentation or measured behavior.

Understanding how the flywheel works requires understanding what a zero-knowledge system actually is -- layer by layer.



## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
