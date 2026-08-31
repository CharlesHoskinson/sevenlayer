## Chapter 1: The Promise of Provable and Programmable Secrets  [`proving_nothing_ch01_the_promise`]
- Define a zero-knowledge proof by stating its three properties — completeness, soundness, and the zero-knowledge property — in a closed-book paragraph that a grader can check against the GMR 1985 formulation.
- List the seven layers of the Seven-Layer Model (setup, language, witness, arithmetization, proof system, primitives, verification) in order, evidenced by reproducing the labeled stack diagram from memory with zero omissions or transpositions.
- Explain the Fiat-Shamir Transform in the student's own words as the move from interactive to non-interactive proofs, with mastery shown by a two-to-three-sentence account that correctly names the hash function's role as the substitute verifier.
- Paraphrase the book's trust-minimized-versus-trustless thesis — that ZK proofs decompose one monolithic trust assumption into seven weaker, testable ones — evidenced by a short written answer that a peer unfamiliar with the book can restate accurately.

## Chapter 2: Layer 1 -- Building the Stage  [`proving_nothing_ch02_building_the_stage`]
- Describe the purpose of a Trusted Setup Ceremony and the Structured Reference String it produces, evidenced by a written account that correctly explains why the toxic waste (trapdoor) must be destroyed.
- Summarize the 1-of-N trust model, with mastery shown by explaining in one paragraph why the Zcash Sprout (2016) and Ethereum KZG Summoning (2023) ceremonies remain sound if even a single participant was honest.
- Classify a given list of schemes (KZG-based, Groth16, STARK) along the trusted-versus-transparent and universal-versus-circuit-specific setup axes, evidenced by a correctly completed two-by-two sorting table.
- Interpret the BCTV14 bug (CVE-2019-7167) and the Quantum Shelf Life argument as cautionary evidence about setup risk, demonstrated by a short response identifying what each implies for ceremony design.

## Chapter 3: Choreographing the Act (Layer 2 -- Language)  [`proving_nothing_ch03_choreographing_the_act`]
- Classify Circom, Cairo, Noir, Leo, and Compact into the Four Layer-2 Language Philosophies (EVM-compatible, ZK-native ISA, general-purpose ISA, application-specific DSL), evidenced by sorting all five correctly with a one-line justification each.
- Explain why under-constrained circuits account for 67% of catalogued SNARK vulnerabilities, with mastery shown by articulating the difference between computing a value and constraining it.
- Apply the lesson of the Tornado Cash '=' versus '<==' bug by identifying and correcting the missing constraint in a supplied three-line Circom fragment, evidenced by the repaired code rejecting a forged witness.
- Use disclosure analysis to mark the disclose() boundary in a short Compact program, demonstrated by correctly labeling every value that crosses from private to public state.

## Chapter 4: The Secret Performance (Layer 3 -- Witness Generation)  [`proving_nothing_ch04_the_secret_performance`]
- Construct the complete witness and execution trace for the 4x4 Sudoku running example from a given solved grid, evidenced by a trace table that satisfies every range, uniqueness, and boundary constraint.
- Demonstrate why the Witness Gap consumes 50-70% of total proving time, with mastery shown by annotating a supplied proving-pipeline profile to isolate witness-generation cost from proof-generation cost.
- Apply constant-time proving principles to a short prover routine by flagging each secret-dependent branch or memory access, evidenced by a marked-up listing with a proposed fix for every flag.
- Illustrate the Zcash Groth16 timing attack (R=0.57) by computing what an observer learns from proving-time measurements in a worked scenario, demonstrated by a correct numerical inference about the hidden input.

## Chapter 5: Encoding the Performance (Layer 4 -- Arithmetization)  [`proving_nothing_ch05_encoding_the_performance`]
- Translate the 4x4 Sudoku uniqueness and range constraints into R1CS form, evidenced by a constraint matrix that a checker script verifies against both a valid and an invalid witness.
- Execute one full round of the Sumcheck Protocol on a supplied three-variable polynomial, demonstrated by producing the correct univariate restriction and verifier check at each step.
- Compare R1CS, PLONKish arithmetization, AIR, and CCS on expressiveness and prover cost, evidenced by a completed comparison matrix that correctly identifies CCS as the generalization subsuming the others.
- Analyze how the lookup-argument lineage (Plookup, LogUp, Lasso) attacks the 10,000x-50,000x Overhead Tax, with mastery shown by a written argument tracing which cost term each successive scheme removes.

## Chapter 6: Layer 5 -- The Sealed Certificate  [`proving_nothing_ch06_the_sealed_certificate`]
- Differentiate folding (Nova, relaxed R1CS) from recursive proof composition (the Russian Doll), evidenced by an annotated diagram plus a cost argument identifying where each defers versus performs verification work.
- Analyze the Groth16-versus-PLONK trade-off — 192-byte circuit-specific proofs against larger proofs with a universal setup — demonstrated by a written analysis that correctly attributes each property to its Layer 1 setup choice.
- Deconstruct the Frozen Heart vulnerability class into its root cause, evidenced by tracing a supplied broken transcript to the specific public input omitted from the Fiat-Shamir hash.
- Examine how HyperNova and the lattice-folding line (LatticeFold, Neo, Symphony) extend Nova's folding to CCS and post-quantum settings, with mastery shown by a lineage map that correctly orders the schemes and states what each generation adds.

## Chapter 7: Layer 6 -- The Deep Craft  [`proving_nothing_ch07_the_deep_craft`]
- Analyze the Cryptographic Primitives Trilemma by placing KZG, FRI, Bulletproofs/IPA, and Ajtai lattice commitments on its three axes (algebraic functionality, post-quantum security, succinctness), evidenced by a placement diagram with a defensible justification for each vertex.
- Organize the Cascade Effect into an explicit dependency chain — field choice determines commitment scheme determines proof system determines arithmetization — demonstrated by tracing two concrete stacks (BN254/KZG/PLONK and M31/FRI/Circle STARK) through all four links.
- Attribute the post-quantum status of each major polynomial commitment scheme to its underlying hardness assumption (discrete log, collision-resistant hashing, Module-SIS), evidenced by a table stating which schemes Shor's algorithm breaks and why.
- Examine the Small-Field Revolution by comparing Goldilocks, BabyBear, and Mersenne-31 against 256-bit fields, with mastery shown by a written analysis connecting field size to hardware arithmetic cost and to FRI-based proving.

## Chapter 8: Layer 7 -- The Verdict  [`proving_nothing_ch08_the_verdict`]
- Evaluate a given rollup's deployment against the L2Beat Stages framework, evidenced by a written Stage 0/1/2 assignment defending each criterion with evidence from the rollup's published architecture.
- Judge whether a system's data availability choice (Ethereum EIP-4844 blobs versus Celestia) preserves or reintroduces trust, demonstrated by a verdict memo that weighs the DA-Saturation Attack against cost.
- Critique the claim that a sound proof system implies a secure system, using the Beanstalk flash-loan ($182M) and Tornado Cash CREATE2 governance attacks as evidence, with mastery shown by locating each attack outside Layers 4-6 in the seven-layer stack.
- Assess the verifier-side attack surface by ranking the Last Challenge Attack, Prover-Killer Attack, and Solana ZK ElGamal Fiat-Shamir bugs by severity for a specified deployment, evidenced by a justified risk ranking.

## Chapter 9: Privacy-Enhancing Technologies  [`proving_nothing_ch09_privacy_enhancing_technologies`]
- Evaluate the fit of ZK proofs, FHE, MPC, TEEs, and differential privacy for three supplied deployment scenarios, evidenced by a decision matrix that selects one PET per scenario and defends each rejection.
- Judge whether a given credential design satisfies eIDAS 2.0 and GDPR data-minimization requirements, demonstrated by a compliance verdict citing the specific selective-disclosure property that carries the argument.
- Critique Privacy Pools (0xbow) as a resolution of the privacy-versus-compliance tension, with mastery shown by a written appraisal that identifies both the mechanism's strongest guarantee and its weakest residual assumption.
- Defend or refute the composability claim behind verifiable FHE (zkFHE) — that proving correct computation over encrypted data combines the guarantees of both PETs — evidenced by an argument that names the cost or trust assumption the combination adds.

## Chapter 10: The Synthesis -- Three Paths, Not Two  [`proving_nothing_ch10_the_synthesis`]
- Evaluate the book's claim that the SNARK-versus-STARK debate was a false dichotomy, evidenced by a written argument that uses the Hybrid STARK-to-SNARK Pipeline's production dominance as its central exhibit.
- Justify a choice among the three paths (hybrid pipeline, pure transparent, post-quantum folding) for a specified application profile, demonstrated by a recommendation memo that scores each path against the application's setup, quantum, and verification-cost requirements.
- Critique the Trust Decomposition thesis by testing the Seven-Layer Causal DAG (14 edges) for a missing or contestable edge, with mastery shown by either defending the DAG as complete or proposing one amended edge with supporting evidence from earlier chapters.

## Chapter 11: zkVMs -- The Universal Stage  [`proving_nothing_ch11_zkvms_the_universal_stage`]
- Evaluate Jolt, SP1 Hypercube, RISC Zero, Airbender, and ZisK against a common rubric (arithmetization strategy, field choice, recursion story, maturity), evidenced by a ranked comparison report with a stated weighting scheme.
- Judge the lookup-centric bet of Jolt — that Lasso-style lookups can replace most bespoke constraints — demonstrated by a verdict essay that marshals the Lookup Singularity argument for and the overhead evidence against.
- Recommend one zkVM for a specified RISC-V workload, with mastery shown by a defense that traces the recommendation through all seven layers rather than citing benchmarks alone.
- Formulate a benchmark protocol that would fairly compare two zkVMs with different proof systems, evidenced by a written protocol controlling for hardware, field size, and recursion depth.

## Chapter 12: Midnight -- The Privacy Theater  [`proving_nothing_ch12_midnight_the_privacy_theater`]
- Evaluate Midnight's full stack layer by layer against the seven-layer model, evidenced by a completed audit table assigning each of Midnight's choices (Compact, ZKIR, Zswap) to its layer and rating the trust assumption incurred there.
- Judge whether Zswap's nullifier mechanism prevents double-spending without creating linkability, demonstrated by a written verdict that traces one shielded transaction through commitment, spend, and nullifier revelation.
- Critique the author's disclosed conflict of interest — having founded IOG, the company behind Midnight — with mastery shown by an appraisal that lists which of the chapter's claims are independently verifiable and which require outside audit.

## Chapter 13: The Market Landscape  [`proving_nothing_ch13_the_market_landscape`]
- Evaluate the maturity of the ZK Rollup segment against the emerging segments (ZK identity, ZK coprocessors, ZKML), evidenced by a market memo that grades each on a stated adoption-versus-hype rubric.
- Judge the Proving-as-a-Service model against the book's Privacy-as-a-Luxury-Good thesis, demonstrated by a verdict on whether delegated proving rescues or forfeits the privacy promise, with the trust cost named explicitly.
- Construct a market map that places Starknet, ZKsync Era, proving services, coprocessors, and ZKML ventures at the seven-layer positions where they compete, evidenced by an original diagram a reader could use to locate a new entrant.
- Formulate an adoption thesis predicting which segment reaches product-market fit first, with mastery shown by a written argument grounded in at least two layer-level constraints from earlier chapters.

## Chapter 14: Open Questions and the Road Ahead  [`proving_nothing_ch14_open_questions`]
- Design a research proposal targeting one of the Seven Open Questions, evidenced by a one-page proposal stating the question, the layer it lives in, a method, and a measurable success criterion.
- Hypothesize how resolving one chosen open question would propagate through the Seven-Layer Causal DAG, demonstrated by an original cascade diagram predicting which layers' trust assumptions weaken and which are untouched.
- Compose a prioritized three-year roadmap across the Three Frontiers (performance, security, privacy), with mastery shown by a written plan that defends its ordering against the strongest objection from a competing frontier.
- Produce an original seven-layer trust decomposition of a system outside zero-knowledge proofs (for example, a certificate authority or a voting system), evidenced by a decomposition that names seven independent, testable assumptions in the style of the book's thesis.
