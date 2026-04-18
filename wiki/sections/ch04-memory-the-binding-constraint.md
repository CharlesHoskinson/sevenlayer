---
title: "Memory: The Binding Constraint"
slug: ch04-memory-the-binding-constraint
chapter: 4
chapter_title: "The Secret Performance"
heading_level: 2
source_lines: [1345, 1392]
source_commit: 8b894477fca68f8420de3f8ba0e5301ba00fbb0a
status: reviewed
word_count: 1646
---

## Memory: The Binding Constraint

The Witness Gap is also a memory problem.

GPU proving requires a minimum of 24 GB of VRAM -- which excludes every consumer GPU below the NVIDIA RTX 4090 (approximately $2,000 USD retail as of early 2026). Large computations demand far more. Jolt requires up to 128 GB of system RAM for long traces. Groth16 for circuits with $2^{25}$ constraints needs approximately 200 GB of RAM. An Ethereum block execution trace, with its millions of state accesses and storage operations, can require specialized hardware with 512 GB or more.

These are not abstract numbers. They determine who can generate proofs and who cannot.

If you are a rollup operator running a proving cluster in a data center with 16 NVIDIA H100 GPUs and dual-socket servers with 512 GB of RAM, the memory requirements are a budgeted operating expense. You buy the hardware, you run the provers, you amortize the cost across millions of transactions.

But if you are an individual user generating proofs on your own device -- the scenario that provides maximum privacy, because your private data never leaves your machine -- the memory requirements become a barrier to entry. A laptop with 16 GB of RAM cannot generate proofs for non-trivial computations. A phone cannot even attempt it.

This leads to an uncomfortable conclusion: *privacy is, in part, a luxury good*. The privacy-maximizing architecture (client-side proving, where your secrets never leave your device) requires hardware that most people do not own. The privacy-minimizing architecture (delegated proving, where you send your private data to a proving service) works on any device but requires trusting the service with your secrets.

Read that again. The architecture that protects your data the most demands hardware that costs the most. The architecture that exposes your data to third parties is the one available to everyone. This is not a theoretical concern. It is the economic structure of privacy in 2026, and it should disturb anyone who believes privacy is a right rather than a commodity.

### The Hardware Ladder

The abstract claim becomes concrete when you map it to specific hardware tiers. Prices below reflect U.S. retail figures gathered in early 2026 from NVIDIA partner listings and the PCPartPicker GPU price tracker; expect variance by region and by the memory premiums charged on HBM parts.

**Tier 1: A laptop with 16 GB of RAM (~$800-1,500).** You can prove trivial computations -- a few thousand constraints, the kind found in simple identity attestations or basic Merkle membership proofs. Anything resembling a real application (a token transfer with privacy, a complex smart contract execution, a state transition proof) exceeds your memory budget. The witness alone may require more RAM than you have. At this tier, you must delegate proving to a remote service. Your private data -- the witness, which contains every secret the proof is supposed to protect -- leaves your machine. You are trusting someone else's hardware with your secrets.

**Tier 2: An NVIDIA RTX 4090 with 24 GB VRAM (~$2,000 for the GPU alone, ~$4,000 for a workstation that can host it).** You can prove moderately complex circuits locally. This is the minimum hardware for client-side privacy-preserving proofs of meaningful complexity. ZKPoG targets this tier explicitly, arguing that it represents the frontier of "democratized" proving. Midnight's proof server targets similar hardware. At this tier, your secrets stay on your machine. You have genuine privacy. But you have also spent $4,000 on a workstation, which places you in the top 5% of computing hardware ownership globally.

**Tier 3: A data center server with an NVIDIA H100 GPU, 80 GB of HBM3 (High Bandwidth Memory) (~$30,000 for the GPU, ~$50,000-80,000 for a full server).** You can prove Ethereum blocks in real time. You can run a rollup's proving infrastructure. You can handle the most complex circuits that production systems generate today. This is the rollup operator tier -- the hardware that Succinct, RISC Zero, and other proving services deploy. The H100's HBM3 provides 3.35 TB/s of memory bandwidth, which is the binding constraint for NTT performance at large polynomial sizes. No consumer GPU comes close.

**Tier 4: A cluster of 16 NVIDIA H100 GPUs (~$500,000 for the GPUs alone, ~$1 million or more for the full cluster with networking, cooling, and redundancy).** You can prove the most complex computations that exist in the ZK ecosystem: large zkVM programs with billions of cycles, full Ethereum block proofs with all precompiles, recursive proof compositions with deep nesting. This is the proving-as-a-service tier. Companies like Succinct and Gevulot operate at this level. A single proof that would take an RTX 4090 several minutes completes in seconds when the computation is sharded across 16 H100s with high-bandwidth interconnect.

**Tier 0: A smartphone with 4-8 GB of RAM (~$200-800).** This is what most of the world actually owns. At this tier, zero-knowledge proving of any meaningful complexity is not slow -- it is impossible. The memory is insufficient. The compute is insufficient. The thermal envelope is insufficient. A phone cannot generate a ZK proof for a shielded transaction, a private vote, or a verifiable computation of any significant size. Not "cannot generate it quickly" -- cannot generate it at all.

The uncomfortable math: approximately 5.5 billion people on Earth own a smartphone. Approximately 200 million own a desktop or laptop with a discrete GPU capable of ZK proving. Of those, perhaps 10-20 million own hardware at Tier 2 or above. That means roughly 96% of the world's population -- including nearly all smartphone-only users in developing economies -- cannot perform client-side ZK proving. They must delegate. They must trust. The cryptographic guarantee of privacy is available to them only through the intermediation of someone else's hardware.

This is not a bug in the technology. It is a structural feature of the cost curve. Moore's Law may eventually bring proving hardware to lower price points. Algorithmic improvements (streaming provers, algebraic RAM reduction) may lower the hardware floor. But in 2026, the privacy hierarchy is clear: the richer your hardware, the more private your computation. The poorer your hardware, the more you must trust others with your secrets.

There is a historical parallel. In the 1990s, strong encryption was classified as a munition by the United States government. Export-grade encryption was deliberately weakened to 40-bit keys, ensuring that only domestic users (and the NSA) had access to real cryptographic security. The rest of the world got a pantomime of privacy. The "Crypto Wars" ended when the government relented and strong encryption became universally available. The current ZK hardware barrier is not a government restriction -- it is an economic one. But the effect is similar: strong privacy for the few, weak privacy (or no privacy) for the many. Whether this barrier will fall, as the export restrictions did, depends on whether the field can make proving cheap enough to run on the hardware that people actually own.

The implications cut in several directions. For technology roadmaps, the target is not "faster proofs" in the abstract but "proofs on cheaper hardware" -- a different optimization problem with different constraints. Streaming provers that trade compute for memory, algebraic RAM reductions that shrink the witness itself, and protocol-level innovations like folding (Chapter 6) that amortize proving cost across many steps all attack different facets of this problem. For system architects, the choice between client-side and delegated proving is not merely a technical tradeoff -- it is a decision about who your system's privacy guarantees actually serve. A system that provides privacy only to users with $4,000 workstations has made an implicit choice about its constituency. Acknowledging that choice honestly is the first step toward changing it.

The field is aware of this tension. ZKPoG specifically targets the NVIDIA RTX 4090 as its hardware platform, arguing that democratizing ZK proving requires targeting accessible consumer hardware rather than data center GPUs. Streaming witness generation reduces memory requirements at the cost of additional computation. And proof delegation with trusted execution environments (TEEs) offers a middle path -- your data is processed inside a secure enclave that even the hardware operator cannot inspect. But TEEs have their own vulnerability history (Foreshadow, AEPIC Leak, Downfall), and Intel deprecated SGX on consumer processors in 2021.

The memory constraint also interacts with NTT performance in a way that matters for system design. NTT is memory-bandwidth-limited at large sizes. The butterfly structure of the NTT requires global memory accesses with poor locality in later stages, meaning that the speed of proving is ultimately limited not by compute (FLOPS) but by memory bandwidth (GB/s). HBM (High Bandwidth Memory) on data center GPUs provides the bandwidth; consumer GPUs do not.

For a system architect making infrastructure decisions, the takeaway is this: when evaluating ZK proving solutions, ask about memory, not just speed. A system that generates proofs in 3 seconds but requires 256 GB of RAM is not the same as a system that generates proofs in 10 seconds but runs in 32 GB. The first requires a data center. The second runs on a workstation. A proving service that advertises "sub-second proofs" but requires an H100 cluster is making a different claim than one that advertises "ten-second proofs" on consumer hardware.

The memory question also intersects with the privacy question. If client-side proving requires 24 GB of VRAM, and only data center GPUs and the NVIDIA RTX 4090 have that much, then privacy-preserving client-side proving is available to a narrow slice of users. Everyone else must delegate proving to a service, which means sending their private witness to someone else's hardware. The Midnight architecture partially addresses this by running the proof server locally alongside the dApp -- but "locally" still means "on hardware with sufficient resources." Midnight's developer documentation and community reports describe typical proof generation times of 20-60 seconds on desktop hardware. On a mobile device, the same computation is infeasible.

---


## Summary

The Witness Gap is also a memory problem: GPU proving requires ≥24 GB VRAM, Jolt and ZKM can need 128 GB of system RAM, and a Groth16 circuit with $2^{25}$ constraints needs ~200 GB. This creates a hardware ladder where client-side (privacy-maximizing) proving is available only to the ~4% of users who own Tier-2+ hardware, making privacy a luxury good in 2026.

## Key claims

- Minimum 24 GB VRAM for GPU proving excludes every consumer GPU below the RTX 4090 (~$2,000).
- Groth16 at $2^{25}$ constraints requires ~200 GB RAM; Ethereum block traces can exceed 512 GB.
- Jolt and ZKM can require 128 GB of system RAM.
- ~96% of the world's population cannot perform client-side ZK proving and must delegate (exposing their witness to a third party).
- The H100's HBM3 provides 3.35 TB/s memory bandwidth — the binding constraint for NTT performance at large polynomial sizes.
- NTT is memory-bandwidth-limited, not compute-limited, at large sizes.
- Privacy-maximizing architecture (client-side) requires the most expensive hardware; privacy-minimizing (delegated) works on any device.
- TEE-based delegation is a middle path but carries its own vulnerability history (Foreshadow, AEPIC Leak, Downfall).

## Entities

- [[folding]]
- [[groth16]]
- [[h100]]
- [[midnight]]
- [[nova]]
- [[ntt]]
- [[nvidia]]

## Dependencies

- [[ch04-witness-generation-costs]] — establishes the cost structure that drives memory demand
- [[ch06-nightstream-what-a-folding-engine-looks-like-from-the-inside]] — folding as a technique that reduces per-step memory cost
- [[ch08-case-study-midnight-and-the-three-token-architecture]] — Midnight's proof server targets Tier-2 hardware

## Sources cited

- ZKPOG — targets NVIDIA RTX 4090 (24 GB VRAM) as the democratized proving tier
- Nair, Thaler, Zhu — streaming reduces space from $O(T)$ to $O(\sqrt{T})$

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [P2] (A) "approximately 5.5 billion people on Earth own a smartphone" — this figure should be sourced; GSMA or Statista reports from 2025 put smartphone penetration at roughly 4.7–5.1 billion. The claim of ~96% unable to do client-side proving depends on this base number being accurate.
- [P2] (B) The Crypto Wars paragraph is presented as historical analogy without a citation for the "40-bit export-grade encryption" claim. This is well-known history but a footnote or source would keep the book's citation standard consistent.
- [P2] (C) "Read that again." — imperative-to-reader register is a mild AI/pop-nonfiction smell. Could be dropped; the argument stands without the rhetorical prod.
- [P2] (C) "The uncomfortable math:" and "The uncomfortable conclusion:" — two consecutive sections using "uncomfortable" as a setup word is a detectable pattern; vary the framing.
- [P2] (E) TEE vulnerabilities are listed (Foreshadow, AEPIC Leak, Downfall) with no dates or brief descriptions. Readers unfamiliar with these attacks get no context for their severity or whether mitigations exist.
- [P3] (D) The section ends with a paragraph on NTT being memory-bandwidth-limited, which is accurate but feels appended — it doesn't connect back to the hardware ladder or the equity argument. Consider moving it earlier or integrating it into the H100 tier description.

## Links

- Up: [[04-the-secret-performance]]
- Prev: [[ch04-witness-generation-costs]]
- Next: [[ch04-side-channel-attacks-when-the-walls-leak]]
