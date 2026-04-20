---
title: "Case Study: Midnight's Sealed Certificate"
slug: ch06-case-study-midnight-s-sealed-certificate
chapter: 6
chapter_title: "Layer 5 -- The Sealed Certificate"
heading_level: 2
source_lines: [2873, 2934]
source_commit: 6e757843ed29aa50ce4558719452a86510ed0d20
status: finalized
word_count: 940
---

## Case Study: Midnight's Sealed Certificate

To see how these abstract proof system choices play out in a real system, consider Midnight -- the privacy-focused blockchain developed by Input Output Global (IOG) for the Cardano ecosystem. Midnight's sealed certificate tells us what Layer 5 looks like when theory meets production.

### The Proof System: Halo 2 / UltraPlonk over BLS12-381

Midnight chose a PLONK-family proof system: specifically Halo 2, an extension of UltraPlonk with custom gates and lookup tables. The curve is BLS12-381, a pairing-friendly curve with better security properties than BN254 (roughly 128-bit security vs. BN254's ~100 bits after Tower NFS advances [Kim and Barbulescu, CRYPTO 2016]). BN254 was adopted by Ethereum for EVM compatibility -- low precompile cost was the priority -- rather than as the strongest available security choice; Midnight's selection of BLS12-381 reflects a different set of constraints where on-chain Ethereum verification cost is not the primary driver. Although the original Halo paper (2019) used inner product arguments (IPA) that required no trusted setup, Midnight's deployment uses KZG polynomial commitments over BLS12-381, which require a Powers-of-Tau ceremony -- a universal trusted setup with a 1-of-N trust assumption.

This places Midnight firmly in the "classical SNARK" camp: pairing-based, recursion-capable, not post-quantum. It is a mature, well-understood choice. The PLONK arithmetization is flexible enough to support Midnight's privacy-preserving smart contract model, where transactions carry zero-knowledge proofs of valid state transitions.

### The Four-Phase Transaction Pipeline

Midnight's proof generation follows a four-phase pipeline that illustrates how the sealed certificate gets manufactured in practice:

**Phase 1: Circuit Execution (callTx).** The DApp calls a contract function. The Compact compiler has already compiled this function into a ZKIR (Zero-Knowledge Intermediate Representation) circuit. The circuit executes locally -- on the user's machine -- producing an "unproven transaction" that contains the execution trace but no proof.

**Phase 2: Proof Generation (proveTx).** The unproven transaction is sent to a local proof server running on localhost:6300. This is a separate process, launched via Docker, that generates the ZK proof. The witness (private inputs) never leaves the client machine. The proof server runs Halo 2's prover and returns a proven transaction. This step dominates latency. This is where the certificate gets sealed.

**Phase 3: Fee Balancing (balanceTx).** The proven transaction is bound, balanced (fee inputs are added from the user's DUST wallet), and signed. This step is sub-second.

**Phase 4: Submission (submitTx).** The finalized transaction -- containing the ZK proof and the public transcript of state reads and writes -- is submitted to the blockchain. The node verifies the proof against the on-chain verifier key, checks that the transcript is consistent with the current ledger state, and applies the state transition. The sealed certificate has reached the audience.

### The Performance Reality

Measured performance on Midnight's devnet (development hardware; production performance may differ; no public benchmark link is available as of this writing) reveals the cost of sealing in concrete terms:

| Operation | Time | Bottleneck |
|-----------|------|------------|
| Deploy (constructor circuit) | 17-27 seconds | Proof generation |
| Circuit call (simple increment) | 17-18 seconds | Proof generation |
| Circuit call (sealed bid) | 22-24 seconds | Proof generation |
| Circuit call (execute escrow) | 23.8 seconds | Proof generation |
| Balance + submit | < 1 second | Network |
| Failed assertion (local) | 0.1-0.5 seconds | No proof needed |

The pattern is clear: proof generation accounts for 95% or more of every transaction's latency. A simple counter increment (the "hello world" of smart contracts) takes 17 seconds because the Halo 2 prover must generate a full zero-knowledge proof. A more complex circuit (escrow execution) takes 24 seconds. Everything else -- fee balancing, signing, network submission, on-chain verification -- is negligible by comparison.

From the user's perspective, Layer 5 is a 17-to-28-second pause during which the proof server is pressing the seal into wax. The cryptography is working. The privacy is being maintained. But the user is waiting.

### Midnight vs. the Frontier

Midnight's architecture makes different choices than the proof systems at the performance frontier. It does not use STARKs. It does not use folding. It does not use GPU acceleration (the proof server appears to be CPU-only). It does not use small-field arithmetic. These are deliberate engineering choices that prioritize maturity and correctness over raw speed.

A comparison with the frontier systems is instructive:

| Property | Midnight (Halo 2) | Neo/Symphony (Lattice folding) | SP1 Hypercube |
|----------|-------------------|-------------------------------|---------------|
| Proof system family | PLONK | Folding (CCS) | STARK + sumcheck |
| Hardness assumption | Discrete log | Module-SIS/LWE | Collision-resistant hashing |
| Post-quantum | No | Yes (plausible) | Yes (inner proof) |
| Field | BLS12-381 (255-bit) | Goldilocks (64-bit) | M31/BabyBear (31-bit) |
| Composition strategy | Recursion | Folding | STARK recursion + SNARK wrap |
| Proof time (simple circuit) | 17-18 seconds | Sub-second (GPU, NTT-based; Symphony target) | Sub-second |
| Proof size | ~hundreds of bytes | Larger (lattice-based) | ~192 bytes (after Groth16 wrap) |
| Trust model | Trusted (universal SRS) | Transparent | Transparent inner, trusted outer |

Midnight's 17-second proof time for a simple increment reflects BLS12-381's expensive 255-bit arithmetic, the absence of GPU acceleration, and the overhead of a full Halo 2 proof per transaction. SP1 Hypercube's sub-second proving reflects M31's cheap 31-bit arithmetic, GPU parallelism, and an architecture optimized for throughput. These are not different implementations of the same idea. They are different points in a design space where field size, hardware utilization, and proof architecture interact multiplicatively.

None of this is meant to criticize Midnight. Its choices are appropriate for a privacy-focused system where correctness and auditability matter more than raw speed, and where the developer toolchain (Compact language, ZKIR, local proof server) provides a coherent end-to-end experience. But it illustrates how the choices made when sealing the certificate -- amplified by the field and commitment choices at Layer 6 -- determine the user experience at the application layer.

---


## Summary

Midnight uses Halo 2 (UltraPlonk with custom gates) over BLS12-381 with KZG commitments -- a mature classical SNARK with a Powers-of-Tau ceremony. Proof generation dominates latency at 17--28 seconds per transaction on devnet (CPU-only, no GPU acceleration). The four-phase pipeline (callTx, proveTx, balanceTx, submitTx) makes Layer 5 concrete: the 17-second pause is the proof server pressing the seal into wax.

## Key claims

- Midnight: Halo 2 / UltraPlonk over BLS12-381, KZG commitments, Powers-of-Tau universal setup.
- BLS12-381 provides ~128-bit security vs. BN254's ~100-bit after Tower NFS; deployment is not post-quantum.
- Four-phase pipeline: callTx (local circuit execution) → proveTx (proof server, localhost:6300) → balanceTx (<1s) → submitTx.
- Proof generation: 17--18s (simple increment), 22--24s (sealed bid), 23.8s (escrow execution); accounts for >95% of latency.
- Witness never leaves the client machine; proof server is CPU-only with no GPU acceleration.
- Comparison table: Midnight (PLONK, discrete log, 255-bit) vs. Neo/Symphony (folding, lattice, 64-bit) vs. SP1 (STARK, hashing, 31-bit).
- Midnight's choices prioritize maturity and correctness; they are a deliberate point in the design space, not a performance failure.

## Entities

- [[midnight]]
- [[plonk]]
- [[halo2]]
- [[kzg]]
- [[bls12-381]]
- [[bn254]]
- [[ceremony]]
- [[goldilocks]]
- [[babybear]]
- [[mersenne]]
- [[lattice]]
- [[folding]]
- [[ntt]]
- [[groth16]]

## Dependencies

- [[ch03-midnight-compiler-ir-circuit]] — Compact compiler and ZKIR are Layer 3; their output feeds Phase 1 here
- [[ch06-the-three-families]] — Midnight is in the PLONK family
- [[ch06-snark-recursion-vs-folding-the-full-picture]] — Midnight's recursion strategy vs. folding alternatives
- [[ch07-case-study-midnight]] — Chapter 7 Layer 6 treatment of Midnight's cryptographic choices

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_All P0/P1/P2/P3 findings resolved in Phase 3 revisions (2026-04-18 through 2026-04-20)._

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

## Links

- Up: [[06-the-sealed-certificate]]
- Prev: [[ch06-fiat-shamir-vulnerabilities]]
- Next: [[ch06-snark-recursion-vs-folding-the-full-picture]]
