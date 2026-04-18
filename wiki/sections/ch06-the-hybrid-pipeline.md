---
title: "The Hybrid Pipeline"
slug: ch06-the-hybrid-pipeline
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2508, 2547]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 1107
---

## The Hybrid Pipeline

Here is the secret that the field's own marketing has obscured: in production, the three families are not competitors. They are components of a single pipeline.

The dominant architecture in 2025 looks like this:

1. **Prove the computation with a STARK.** The inner proof system generates a large, transparent proof using fast, small-field arithmetic. No trusted setup is required. The prover runs on GPUs.

2. **Recursively compress the STARK.** Apply one or more rounds of recursive STARK verification to shrink the proof from hundreds of kilobytes to tens of kilobytes.

3. **Wrap the compressed STARK in a Groth16 SNARK.** A small circuit verifies the STARK proof and produces a Groth16 proof: 192 bytes, 250K gas to verify on-chain. The wrapping circuit adapts the STARK's field arithmetic (say, Mersenne-31) to the BN254 field that Ethereum's precompiles support.

4. **Post the SNARK on-chain.** The Ethereum verifier contract checks the Groth16 proof. It has no idea that the inner computation used a STARK. From the chain's perspective, everything looks the same.

Every major production system follows this architecture: SP1 (Succinct Labs), Stwo (StarkWare), Polygon, ZKM, and most others. The STARK generates the raw material; the SNARK seals it into a certificate the blockchain will accept. The STARK provides transparency and prover efficiency. The SNARK provides on-chain cost efficiency. Each family contributes what it does best.

The implication is worth spelling out. The "SNARK vs. STARK" debate that dominated conference panels from 2019 to 2023 was a false dichotomy. The field converged on "STARK inside, SNARK outside" because the engineering tradeoffs demanded it. Transparency for the prover. Compactness for the chain. The only remaining question is whether the outer SNARK wrapper can itself become post-quantum -- a problem that lattice-based proof systems (discussed later in this chapter) are beginning to address.

### A Concrete Pipeline: From 1,000 Transactions to a 192-Byte Proof

The hybrid architecture becomes vivid when you trace a specific workload through it, step by step. Consider a ZK rollup operator -- running on Ethereum mainnet -- who receives a batch of 1,000 transactions. Each transaction is a token transfer, a swap, or a contract call. The operator must prove that executing all 1,000 transactions against the current state produces the claimed new state root. Here is how the pipeline processes that batch in 2025.

**Step 1: Execute and generate the witness.** The operator's sequencer replays all 1,000 transactions against a local copy of the rollup's state. Every storage read, every storage write, every arithmetic operation is recorded in an execution trace -- the giant spreadsheet from Chapter 4. The witness includes all private data: account balances, nonces, intermediate computation values. This step is ordinary software execution, no cryptography involved. On a modern server, it takes 1 to 2 seconds. The output is a trace with millions of rows and dozens of columns.

**Step 2: Generate a STARK proof over a small field.** The prover takes the execution trace and produces a STARK proof using BabyBear (31-bit) or Mersenne-31 arithmetic. This is where the heavy computation happens. The trace is interpolated into polynomials, the polynomials are committed via FRI (Merkle trees of evaluations), and the FRI protocol verifies low-degree proximity. On a cluster of GPUs -- say, four NVIDIA A100s -- this step takes 3 to 5 seconds. The output is a STARK proof: transparent, hash-based, quantum-resistant, and roughly 200 to 400 kilobytes in size.

**Step 3: Recursively compress the STARK.** The raw STARK proof is too large to post on-chain economically. So the operator generates a second STARK proof that verifies the first one. This is recursion: a proof about a proof. The verifier circuit for a STARK is much smaller than the original computation circuit, so the recursive proof is faster to generate and produces a smaller output. One or two rounds of recursive compression shrink the proof from hundreds of kilobytes to tens of kilobytes. This step takes 1 to 2 seconds.

**Step 4: Wrap in Groth16 over BN254.** The compressed STARK proof is now small enough to verify inside a Groth16 circuit. A specialized wrapping circuit takes the STARK verifier computation -- check the Merkle paths, verify the FRI folding, confirm the constraint evaluations -- and expresses it as an R1CS instance over the BN254 field. The Groth16 prover then seals this into a 192-byte proof: two G1 points and one G2 point. This is the field-crossing step, where 31-bit STARK arithmetic is translated into 254-bit BN254 arithmetic. It is computationally expensive per field operation, but the circuit is small (it is only verifying a STARK, not re-executing the original computation). On a single GPU, this step takes 5 to 10 seconds.

**Step 5: Post the proof to Ethereum.** The operator submits a transaction to the rollup's on-chain verifier contract. The transaction contains the 192-byte Groth16 proof, the new state root, and a commitment to the batch of transactions. The Ethereum verifier contract calls the BN254 pairing precompile (EIP-1108), checks the three pairings, and accepts or rejects. Verification costs approximately 250,000 gas -- roughly $0.50 to $1.00 at typical gas prices. The state root is updated. The 1,000 transactions are finalized.

The audience sees only Step 5. A 192-byte proof appears on-chain. A smart contract checks it in a few milliseconds. The state updates. Nobody knows -- or needs to know -- that behind those 192 bytes lie four NVIDIA GPUs, two rounds of recursive compression, a field-crossing circuit, and the execution traces of 1,000 individual transactions. The entire pipeline, from receiving the batch to posting the proof, completes in under 15 seconds and costs under $1.00.

That is the hybrid pipeline in concrete terms. The STARK did the heavy lifting: proving the computation with transparency and quantum resistance. The Groth16 wrapper did the packaging: compressing everything into the smallest possible on-chain footprint. Each proof system contributed what it does best. The audience -- Ethereum's verifier contract -- received the finished product and asked no questions about the manufacturing process.

Two years earlier, the same pipeline took minutes and cost tens of dollars. Two years before that, it was a research prototype that could not process a full Ethereum block at all. The economics shifted not because anyone invented a fundamentally new proof system, but because each component in the pipeline got faster -- small-field arithmetic, GPU parallelism, recursive compression, optimized wrapping circuits -- and the improvements compounded multiplicatively across stages. A 3x improvement in STARK proving, combined with a 2x improvement in recursive compression, combined with a 2x improvement in Groth16 wrapping, produces a 12x improvement end-to-end. This is why the cost curve has been steeper than Moore's Law.

---


## Summary

In production, Groth16, PLONK, and STARKs are not competitors but sequential pipeline stages. The dominant architecture uses a STARK over a small field (BabyBear or Mersenne-31) for transparent inner proving, recursive compression to shrink the proof, then Groth16 over BN254 as the on-chain wrapper. A batch of 1,000 transactions can be proven and posted for under $1 in under 15 seconds.

## Key claims

- The hybrid pipeline: STARK (inner, transparent) → recursive compression → Groth16 (outer, 192 bytes, ~250K gas).
- All major production systems follow this architecture: SP1, Stwo, Polygon, ZKM.
- BabyBear (31-bit) or Mersenne-31 is used for inner STARK arithmetic; BN254 for the Groth16 wrapper.
- Four NVIDIA A100 GPUs generate the STARK proof in 3--5 seconds; Groth16 wrapping takes 5--10 seconds.
- Verification on Ethereum costs ~250,000 gas ($0.50--$1.00); end-to-end pipeline under 15 seconds, under $1.
- Cost improvements compound multiplicatively across stages, explaining why cost curves exceed Moore's Law.
- The outer Groth16 wrapper remains quantum-vulnerable; replacing it with a post-quantum equivalent is an open problem.

## Entities

- [[groth16]]
- [[starks]]
- [[fri]]
- [[bn254]]
- [[babybear]]
- [[mersenne]]
- [[small-field]]
- [[nvidia]]
- [[polygon]]
- [[eip]]

## Dependencies

- [[ch06-the-three-families]] — establishes the three families whose roles in the pipeline are explained here
- [[ch04-execution-traces]] — execution trace generation is Step 1 of the pipeline
- [[ch06-recursion-vs-folding-russian-dolls-and-snowballs]] — recursive compression (Step 3) is explained in the next section
- [[ch10-path-one-the-hybrid-stark-to-snark-pipeline]] — Chapter 10 places this pipeline in the three-path synthesis

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [P1] (B) No sources cited for any concrete timing or cost figures (3–5s STARK, 5–10s Groth16 wrap, "$0.50–$1.00 per verification", sub-$1 end-to-end); these should reference CastleLabs/Ethproofs or a dated benchmark
- [P2] (A) "All major production systems follow this architecture: SP1, Stwo, Polygon, ZKM" — Polygon runs multiple proving systems (e.g., Polygon zkEVM uses a different pipeline); the claim needs qualification or a source
- [P2] (C) "The implication is worth spelling out" — AI smell
- [P2] (A) "$0.50–$1.00 at typical gas prices" is vague and gas-price-dependent; the figure is anchored to no specific date or gas price level
- [P3] (E) The pipeline section describes four NVIDIA A100s but ch06-real-time-ethereum-proving describes RTX 5090s for SP1 Hypercube; no note explains the different hardware baselines used in the two sections

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-the-three-families]]
- Next: [[ch06-recursion-vs-folding-russian-dolls-and-snowballs]]
