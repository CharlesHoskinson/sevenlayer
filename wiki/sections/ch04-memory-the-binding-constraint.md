---
title: "Memory: The Binding Constraint"
slug: ch04-memory-the-binding-constraint
chapter: 4
chapter_title: "The Secret Performance"
heading_level: 2
source_lines: [1330, 1377]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 1646
---

## Memory: The Binding Constraint

The Witness Gap is also a memory problem.

GPU proving requires a minimum of 24 GB of VRAM -- which excludes every consumer GPU below the NVIDIA RTX 4090 (approximately $2,000). Large computations demand far more. Jolt and ZKM can require 128 GB of system RAM. Groth16 for circuits with $2^{25}$ constraints needs approximately 200 GB of RAM. An Ethereum block execution trace, with its millions of state accesses and storage operations, can require specialized hardware with 512 GB or more.

These are not abstract numbers. They determine who can generate proofs and who cannot.

If you are a rollup operator running a proving cluster in a data center with 16 NVIDIA H100 GPUs and dual-socket servers with 512 GB of RAM, the memory requirements are a budgeted operating expense. You buy the hardware, you run the provers, you amortize the cost across millions of transactions.

But if you are an individual user generating proofs on your own device -- the scenario that provides maximum privacy, because your private data never leaves your machine -- the memory requirements become a barrier to entry. A laptop with 16 GB of RAM cannot generate proofs for non-trivial computations. A phone cannot even attempt it.

This leads to an uncomfortable conclusion: *privacy is, in part, a luxury good*. The privacy-maximizing architecture (client-side proving, where your secrets never leave your device) requires hardware that most people do not own. The privacy-minimizing architecture (delegated proving, where you send your private data to a proving service) works on any device but requires trusting the service with your secrets.

Read that again. The architecture that protects your data the most demands hardware that costs the most. The architecture that exposes your data to third parties is the one available to everyone. This is not a theoretical concern. It is the economic structure of privacy in 2026, and it should disturb anyone who believes privacy is a right rather than a commodity.

### The Hardware Ladder

The abstract claim becomes concrete when you map it to specific hardware tiers. Here is what zero-knowledge proving looks like at each rung of the hardware ladder, from the bottom up.

**Tier 1: A laptop with 16 GB of RAM (~$800-1,500 as of early 2026).** You can prove trivial computations -- a few thousand constraints, the kind found in simple identity attestations or basic Merkle membership proofs. Anything resembling a real application (a token transfer with privacy, a complex smart contract execution, a state transition proof) exceeds your memory budget. The witness alone may require more RAM than you have. At this tier, you must delegate proving to a remote service. Your private data -- the witness, which contains every secret the proof is supposed to protect -- leaves your machine. You are trusting someone else's hardware with your secrets.

**Tier 2: An NVIDIA RTX 4090 with 24 GB VRAM (~$2,000 for the GPU alone as of early 2026, ~$4,000 for a workstation that can host it).** You can prove moderately complex circuits locally. This is the minimum hardware for client-side privacy-preserving proofs of meaningful complexity. ZKPOG targets this tier explicitly, arguing that it represents the frontier of "democratized" proving. Midnight's proof server targets similar hardware. At this tier, your secrets stay on your machine. You have genuine privacy. But you have also spent $4,000 on a workstation, which places you in the top 5% of computing hardware ownership globally.

**Tier 3: A data center server with an NVIDIA H100 GPU, 80 GB of HBM3 (High Bandwidth Memory) (~$30,000 for the GPU as of early 2026, ~$50,000-80,000 for a server).** You can prove Ethereum blocks in real time. You can run a rollup's proving infrastructure. You can handle the most complex circuits that production systems generate today. This is the rollup operator tier -- the hardware that Succinct, RISC Zero, and other proving services deploy. The H100's HBM3 provides 3.35 TB/s of memory bandwidth, which is the binding constraint for NTT performance at large polynomial sizes. No consumer GPU comes close.

**Tier 4: A cluster of 16 NVIDIA H100 GPUs (~$500,000 for the GPUs alone, ~$1 million or more for the full cluster with networking, cooling, and redundancy).** You can prove the most complex computations that exist in the ZK ecosystem: large zkVM programs with billions of cycles, full Ethereum block proofs with all precompiles, recursive proof compositions with deep nesting. This is the proving-as-a-service tier. Companies like Succinct and Gevulot operate at this level. A single proof that would take an RTX 4090 several minutes completes in seconds when the computation is sharded across 16 H100s with high-bandwidth interconnect.

**Tier 0: A smartphone with 4-8 GB of RAM (~$200-800).** This is what most of the world actually owns. At this tier, zero-knowledge proving of any meaningful complexity is not slow -- it is impossible. The memory is insufficient. The compute is insufficient. The thermal envelope is insufficient. A phone cannot generate a ZK proof for a shielded transaction, a private vote, or a verifiable computation of any significant size. Not "cannot generate it quickly" -- cannot generate it at all.

The uncomfortable math: approximately 5.5 billion people on Earth own a smartphone. Approximately 200 million own a desktop or laptop with a discrete GPU capable of ZK proving. Of those, perhaps 10-20 million own hardware at Tier 2 or above. That means roughly 96% of the world's population -- including nearly all smartphone-only users in developing economies -- cannot perform client-side ZK proving. They must delegate. They must trust. The cryptographic guarantee of privacy is available to them only through the intermediation of someone else's hardware.

This is not a bug in the technology. It is a structural feature of the cost curve. Moore's Law may eventually bring proving hardware to lower price points. Algorithmic improvements (streaming provers, algebraic RAM reduction) may lower the hardware floor. But in 2026, the privacy hierarchy is clear: the richer your hardware, the more private your computation. The poorer your hardware, the more you must trust others with your secrets.

There is a historical parallel. In the 1990s, strong encryption was classified as a munition by the United States government. Export-grade encryption was deliberately weakened to 40-bit keys, ensuring that only domestic users (and the NSA) had access to real cryptographic security. The rest of the world got a pantomime of privacy. The "Crypto Wars" ended when the government relented and strong encryption became universally available. The current ZK hardware barrier is not a government restriction -- it is an economic one. But the effect is similar: strong privacy for the few, weak privacy (or no privacy) for the many. Whether this barrier will fall, as the export restrictions did, depends on whether the field can make proving cheap enough to run on the hardware that people actually own.

The implications cut in several directions. For technology roadmaps, the target is not "faster proofs" in the abstract but "proofs on cheaper hardware" -- a different optimization problem with different constraints. Streaming provers that trade compute for memory, algebraic RAM reductions that shrink the witness itself, and protocol-level innovations like folding (Chapter 6) that amortize proving cost across many steps all attack different facets of this problem. For system architects, the choice between client-side and delegated proving is not merely a technical tradeoff -- it is a decision about who your system's privacy guarantees actually serve. A system that provides privacy only to users with $4,000 workstations has made an implicit choice about its constituency. Acknowledging that choice honestly is the first step toward changing it.

The field is aware of this tension. ZKPOG specifically targets the NVIDIA RTX 4090 (24 GB VRAM, approximately $2,000) as its hardware platform, arguing that democratizing ZK proving requires targeting accessible consumer hardware rather than data center GPUs. Streaming witness generation reduces memory requirements at the cost of additional computation. And proof delegation with trusted execution environments (TEEs) offers a middle path -- your data is processed inside a secure enclave that even the hardware operator cannot inspect. But TEEs have their own vulnerability history (Foreshadow, AEPIC Leak, Downfall), and Intel deprecated SGX on consumer processors in 2021.

The memory constraint also interacts with NTT performance in a way that matters for system design. NTT -- the number-theoretic transform used in polynomial commitment schemes -- is memory-bandwidth-limited at large sizes. The butterfly structure of the NTT requires global memory accesses with poor locality in later stages, meaning that the speed of proving is ultimately limited not by compute (FLOPS) but by memory bandwidth (GB/s). HBM (High Bandwidth Memory) on data center GPUs provides the bandwidth; consumer GPUs do not.

For a system architect making infrastructure decisions, the takeaway is this: when evaluating ZK proving solutions, ask about memory, not just speed. A system that generates proofs in 3 seconds but requires 256 GB of RAM is not the same as a system that generates proofs in 10 seconds but runs in 32 GB. The first requires a data center. The second runs on a workstation. A proving service that advertises "sub-second proofs" but requires an H100 cluster is making a different claim than one that advertises "ten-second proofs" on consumer hardware.

The memory question also intersects with the privacy question. If client-side proving requires 24 GB of VRAM, and only data center GPUs and the NVIDIA RTX 4090 have that much, then privacy-preserving client-side proving is available to a narrow slice of users. Everyone else must delegate proving to a service, which means sending their private witness to someone else's hardware. The Midnight architecture partially addresses this by running the proof server locally alongside the dApp -- but "locally" still means "on hardware with sufficient resources." The 18-24 second proof generation time observed on Midnight's development environment reflects desktop-class hardware. On a mobile device, the same computation might be infeasible.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
