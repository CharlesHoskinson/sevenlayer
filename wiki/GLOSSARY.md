# Glossary of Key Terms {.unnumbered}

**AIR (Algebraic Intermediate Representation)** -- A way of encoding computation as a table of numbers governed by polynomial rules that must hold between consecutive rows. Used by STARK proof systems.

**Arithmetization** -- The conversion of a computation into a system of polynomial equations that can be verified mathematically.

**BabyBear** -- A 31-bit prime field ($2^{31} - 2^{27} + 1$) used by SP1 and Plonky3. Enables SIMD-friendly arithmetic on modern CPUs.

**BLS12-381** -- A specific elliptic curve providing approximately 128-bit security. Used by Zcash, Ethereum's blob commitments, and Midnight. Vulnerable to quantum computers.

**BN254 (alt_bn128)** -- An older elliptic curve hardcoded into Ethereum's built-in operations. Its estimated security has eroded from 128 bits to approximately 100 bits.

**CCS (Customizable Constraint Systems)** -- A unified mathematical framework that includes R1CS, AIR, and PLONKish as special cases.

**Circle STARKs** -- A STARK variant operating over the circle group of a Mersenne prime field, enabling efficient FFTs without requiring smooth-order multiplicative subgroups.

**Circuit** -- A representation of a computation as a network of mathematical operations over a finite field. Not an electrical circuit -- a mathematical one.

**Commitment scheme** -- A cryptographic method that lets you "seal" a value in an envelope, later proving properties about it without opening it. The four main families are KZG, FRI, IPA, and lattice-based (Ajtai).

**CycleFold** -- An engineering optimization that delegates the non-native scalar multiplication in folding schemes to a co-processor circuit on a secondary curve, reducing overhead.

**Data availability (DA)** -- The guarantee that transaction data is published and accessible so that anyone can reconstruct state and verify proofs independently.

**Discrete logarithm problem (DLP)** -- Given points $P$ and $Q$ on an elliptic curve where $Q = nP$, finding the integer $n$. Believed hard classically; broken by Shor's algorithm on a quantum computer.

**Elliptic curve** -- A mathematical curve whose point-addition operation is easy to perform but hard to reverse. The foundation of most modern public-key cryptography.

**Execution trace** -- The complete record of every step in a computation: register values, memory accesses, intermediate results. The raw material from which a witness is derived.

**Extension field** -- A larger field constructed from a base field by adjoining roots of an irreducible polynomial, used to achieve sufficient security when working with small base fields.

**FHE (Fully Homomorphic Encryption)** -- Encryption that allows computation on encrypted data without decrypting it first. Currently 10,000x to 1,000,000x slower than plaintext computation.

**Fiat-Shamir transform** -- A technique for converting an interactive proof into a non-interactive one using a hash function. Every blockchain-based zero-knowledge proof uses this.

**Finite field** -- A set of numbers where arithmetic "wraps around" like a clock. All arithmetic in zero-knowledge proofs happens in finite fields.

**Flash loan** -- A DeFi mechanism allowing uncollateralized borrowing within a single transaction. Used in governance attacks when combined with token-weighted voting.

**Folding** -- A technique for combining two mathematical claims into one using random challenges. Dramatically reduces the cost of proving long computations.

**FRI (Fast Reed-Solomon Interactive Oracle Proof of Proximity)** -- A method for verifying polynomial proximity using only hash functions. The commitment scheme inside every STARK. Transparent and plausibly post-quantum.

**Gas** -- The unit of computational cost on Ethereum. A simple transfer costs roughly 21,000 gas; verifying a Groth16 proof costs roughly 250,000 gas.

**Goldilocks field** -- A specific 64-bit prime ($2^{64} - 2^{32} + 1$). Called "Goldilocks" because it fits in a single machine word for fast arithmetic.

**Groth16** -- The most compact zero-knowledge proof system: proofs are exactly 192 bytes. Requires a per-circuit trusted setup ceremony.

**Halo 2** -- A PLONK-family proof system developed by the Electric Coin Company. The original Halo used IPA commitments (no ceremony); Halo 2 as deployed typically uses KZG commitments.

**HyperNova** -- A folding scheme by Kothapalli and Setty that generalizes Nova from R1CS to CCS using the sumcheck protocol, enabling folding of any constraint system.

**ISA (Instruction Set Architecture)** -- The fundamental language a processor understands. RISC-V is the dominant ISA for zero-knowledge virtual machines.

**IVC (Incrementally Verifiable Computation)** -- A framework for proving that a sequence of computation steps was performed correctly, where each step's proof implicitly covers all previous steps.

**KZG (Kate-Zaverucha-Goldberg)** -- A polynomial commitment scheme producing constant-size proofs (~48 bytes) using elliptic curve pairings. Requires a trusted setup. Not quantum-resistant.

**Lattice** -- A regular grid of points in high-dimensional space. Finding a short vector in such a lattice is believed to be hard even for quantum computers.

**M31 / Mersenne-31** -- A 31-bit prime field ($2^{31} - 1$) used by Circle STARKs and Stwo. Its circle group has order $2^{31}$, enabling efficient radix-2 FFTs.

**Merkle tree** -- A pyramid-shaped data structure where a single hash at the top summarizes an entire collection, and membership can be proven with a short path of hashes.

**Midnight** -- A privacy-focused blockchain built as a sidechain of Cardano, developed by Input Output Global (IOG). Every smart contract on Midnight executes via zero-knowledge proofs, making it a full-stack case study used throughout this book (Chapters 2, 3, 4, 6, 7, 8, and 12).

**Module-LWE (Module Learning With Errors)** -- A lattice problem believed hard even for quantum computers. The foundation for NIST's post-quantum encryption standard (FIPS 203) alongside Module-SIS.

**Module-SIS (Module Short Integer Solution)** -- A mathematical problem believed hard even for quantum computers. The foundation for lattice-based ZK proof systems and NIST's post-quantum standards.

**MPC (Secure Multi-Party Computation)** -- Protocols that let multiple parties jointly compute a function without any party revealing its input to the others.

**MSM (Multi-Scalar Multiplication)** -- A computation where many elliptic curve points are multiplied by different scalars and summed. Highly parallelizable on GPUs.

**Neo** -- A lattice-based folding scheme by Nguyen and Setty that adapts HyperNova's CCS folding to small fields (Goldilocks) with Ajtai commitments, introducing pay-per-bit commitment costs.

**Nova** -- The first practical folding scheme, by Kothapalli, Setty, and Tzialla (2022). Introduced relaxed R1CS and reduced the per-step overhead of IVC by orders of magnitude.

**NTT (Number Theoretic Transform)** -- The finite-field version of the Fast Fourier Transform. A critical bottleneck in modern proof systems.

**Nullifier** -- A cryptographic value derived from a secret key and a commitment, used to prevent double-spending in privacy-preserving systems without revealing the spender's identity.

**Pedersen commitment** -- A cryptographic commitment using elliptic curve arithmetic. Not quantum-resistant.

**PLONK** -- A universal zero-knowledge proof system (2019) that works with any circuit up to a fixed size using a single trusted setup ceremony.

**PLONKish** -- The arithmetization format used by PLONK and variants. Uses selector columns for different gate types plus copy constraints for wiring.

**Post-quantum (PQ)** -- Resistant to attacks by quantum computers. Hash-based and lattice-based cryptography are believed to be PQ. Elliptic curve cryptography is not.

**Proof aggregation** -- Combining multiple proofs into a single proof that is cheaper to verify than checking each proof individually. A key technique for amortizing on-chain verification costs.

**Prover** -- The entity that generates a zero-knowledge proof. In the magician metaphor, the prover is the magician who performs the trick.

**R1CS (Rank-1 Constraint System)** -- The simplest constraint system format. The "assembly language" of arithmetization. Used natively by Groth16.

**Relaxed R1CS** -- A generalization of R1CS ($\mathbf{A}\mathbf{z} \circ \mathbf{B}\mathbf{z} = u \cdot \mathbf{C}\mathbf{z} + \mathbf{E}$) that introduces a scalar $u$ and error vector $\mathbf{E}$, enabling two instances to be combined via random linear combination. The key enabler of folding.

**RISC-V** -- An open, royalty-free instruction set architecture. Eight of ten major zkVMs use RISC-V as their target.

**Rollup** -- A blockchain scaling technique that executes transactions off the main chain, posting a compact proof back for verification.

**Shor's algorithm** -- A quantum algorithm (1994) that breaks all elliptic curve cryptography in polynomial time.

**SNARK (Succinct Non-interactive ARgument of Knowledge)** -- A proof system producing compact proofs that can be verified quickly without interaction. Groth16, PLONK, and Marlin are SNARKs.

**Soundness** -- The guarantee that a cheating prover cannot create a valid proof for a false statement, except with negligible probability.

**SRS (Structured Reference String)** -- The public mathematical parameters from a trusted setup ceremony. The stage on which the magician performs.

**STARK (Scalable Transparent ARgument of Knowledge)** -- A proof system using hash-based commitments (FRI) with no trusted setup. Transparent, plausibly post-quantum, but with larger proofs than SNARKs.

**Stwo** -- StarkWare's production implementation of Circle STARKs, deployed on Starknet mainnet. Achieved 940x throughput improvement over the previous Stone prover.

**Sumcheck protocol** -- An interactive proof protocol (1992) that reduces verifying a sum over an exponentially large domain to checking a single evaluation. The backbone of modern ZK proof systems.

**TEE (Trusted Execution Environment)** -- A hardware-isolated secure enclave (e.g., Intel SGX, ARM TrustZone) that processes data in a protected region even the hardware operator cannot inspect.

**UTXO (Unspent Transaction Output)** -- A model where each digital coin is a discrete object created by one transaction and consumed by another, like physical bills in a wallet.

**Verifier** -- The entity that checks a zero-knowledge proof. In the magician metaphor, the verifier is the audience that renders the verdict.

**Witness** -- The private data and execution trace that the prover uses to generate a proof. The verifier never sees the witness.

**Zero-knowledge** -- The property that a proof reveals nothing beyond the truth of the statement being proved.

**ZKIR** -- Midnight's Zero-Knowledge Intermediate Representation. A 24-instruction typed bytecode that the Compact compiler produces, which a backend lowers to PLONKish constraints.

**zkVM (Zero-Knowledge Virtual Machine)** -- A virtual processor that executes programs and automatically generates a zero-knowledge proof of correct execution.

---
