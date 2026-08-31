# Learning Objectives — *Proving Nothing*

Pedagogical goals for each of the 14 chapters, authored by a swarm of five
academic personas who each walked the book sequentially, chapter by chapter,
grounded in the master knowledge graph (`graphify-out/graph.json`: 3,991 nodes /
7,237 edges over the book, its recursion outline, and 293 reference papers;
per-chapter grounding in `graphify-out/chapter-digest.md`). Concept centrality
(node degree) guided which ideas each persona treated as load-bearing.

## The panel

- **Prof. Elena Vasquez — Theoretical Cryptographer.** Definitions, security games, theorems, and the assumptions they rest on.
- **Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition).** Intuition first, one worked object per idea, explicit prerequisites, named stuck-points.
- **Priya Raghavan — Staff ZK Systems Engineer.** What you can build, benchmark, configure, or break; failure modes over formalism.
- **Dr. Marisol Chen — Curriculum & Assessment Designer.** Measurable revised-Bloom objectives with in-sentence evidence of mastery, rising in level across the book.
- **Prof. David Lindqvist — Political Economist of Trust.** Every mechanism re-read as a trust reallocation: who bears risk, whose incentives, at what cost.

---

# Chapter 1: The Promise of Provable and Programmable Secrets

### Prof. Elena Vasquez — Theoretical Cryptographer
- Define an Interactive Proof system exactly as GMR 1985 (cited here) does: state Completeness and Soundness as probabilistic games between a prover and a PPT verifier, with explicit acceptance probabilities and soundness error — no "the verifier is convinced" hand-waving.
- Define the Zero-Knowledge Property via the simulation paradigm: exhibit the simulator existentially, state the indistinguishability notion (perfect/statistical/computational), and explain why Zero-Knowledge Proof (deg 15, the most load-bearing concept in the graph) is a property of the *verifier's view*, not of the message contents.
- State the Fiat-Shamir Transform (deg 8) precisely as it descends from Fiat-Shamir 1986 (cited): which class of protocols it applies to (public-coin), what it produces (a non-interactive argument), the theorem it satisfies in the random-oracle model, and what is *not* proven once the oracle is instantiated by a concrete hash.
- Read the Seven-Layer Model and the Trust-Minimized (vs Trustless) rationale critically: the claim that ZK decomposes one monolithic assumption into "seven independent, weaker, testable" ones is a taxonomy, not a theorem — identify, for a SNARK and a STARK, which layers carry cryptographic assumptions with reductions and which carry only procedural trust.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Own the interactive-proof intuition before any formalism (GMR 1985): a prover survives a barrage of random challenges only if the claim is true. Anchor it with the 4x4 Sudoku from day one — "I can convince you my grid is solved without ever showing you the grid" — and let students physically play verifier for three rounds before the words "completeness" or "soundness" appear. No prerequisite; this is the ground floor, and everything else stands on it.
- Hold completeness, soundness, and the zero-knowledge property as three separate promises made to three different parties, each visible in the same Sudoku game: the honest solver always convinces (completeness), the bluffer gets caught with quantifiable probability (soundness), and the verifier walks away knowing nothing but "a solution exists" (zero-knowledge). Builds only on the interactive-proof picture above — do not let students blur the three into one vague "it's secure."
- Internalize the Seven-Layer Model as the book's map, not a theorem: setup, language, witness, arithmetization, proof system, primitives, verification. Students should be able to point at the Sudoku example and say which layer each future question will live in. Builds on the interactive-proof intuition — the layers are where that one clean game gets industrialized.
- Stuck-point: students must be able to articulate why "trust-minimized" is NOT "trustless." The deg-3 rationale node carries the book's central thesis — ZK proofs do not delete trust, they decompose one monolithic assumption into seven weaker, independently testable ones. A student who says "trustless" on the exit ticket has not yet started the book. Builds on the three-properties goal: each property is itself a conditional promise, resting on assumptions we will spend thirteen chapters naming.

### Priya Raghavan — Staff ZK Systems Engineer
- Implement the 4x4 Sudoku running example as an interactive proof in ~200 lines of Python, then apply the Fiat-Shamir transform yourself — hash the transcript, kill the interaction — and demonstrate completeness, soundness, and zero-knowledge by actually cheating: submit a bad witness and measure how many challenge rounds it takes for soundness error to drop below 2^-40.
- Take one production stack you can run today (say Circom+Groth16, or SP1) and map it onto the Seven-Layer Model — setup, language, witness, arithmetization, proof system, primitives, verification — writing down for each layer the concrete artifact on disk (the .r1cs file, the SRS, the witness .wtns) so the decomposition stops being a diagram and becomes an ls listing.
- Argue the Trust-Minimized (vs Trustless) thesis with receipts: for each of the seven layers, name one real incident or assumption (a ceremony, a compiler bug, a hash function) that shows the trust didn't vanish, it just got smaller and testable — because "trustless" on the marketing site is what gets you paged when layer 2 was the actual assumption.
- Read GMR 1985 and Fiat-Shamir 1986 (the two highest-degree citation nodes here) and be able to state, in one sentence each, what an interactive proof is and exactly what property the Fiat-Shamir transform trades away — since a wrong answer to that question is the root cause of an entire vulnerability class you'll meet in Chapter 6.

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Define a zero-knowledge proof by stating its three properties — completeness, soundness, and the zero-knowledge property — in a closed-book paragraph that a grader can check against the GMR 1985 formulation.
- List the seven layers of the Seven-Layer Model (setup, language, witness, arithmetization, proof system, primitives, verification) in order, evidenced by reproducing the labeled stack diagram from memory with zero omissions or transpositions.
- Explain the Fiat-Shamir Transform in the student's own words as the move from interactive to non-interactive proofs, with mastery shown by a two-to-three-sentence account that correctly names the hash function's role as the substitute verifier.
- Paraphrase the book's trust-minimized-versus-trustless thesis — that ZK proofs decompose one monolithic trust assumption into seven weaker, testable ones — evidenced by a short written answer that a peer unfamiliar with the book can restate accurately.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to prosecute the word "trustless" as marketing and defend "trust-minimized" as the honest term: for any ZK deployment, name the monolithic trust relationship that existed before (verifier trusts prover, citizen trusts institution) and enumerate the seven weaker, independently replaceable assumptions it is decomposed into — decomposition, not elimination, is the product being sold.
- Students must be able to read completeness, soundness, and zero-knowledge as a risk-allocation contract between two counterparties: soundness insures the verifier against a lying prover, zero-knowledge insures the prover against an extractive verifier — and for each property, say who bears the residual loss when it fails.
- Students must be able to analyze the Fiat-Shamir transform as a personnel change on the trust roster: the trusted interactive verifier (who must sample randomness honestly) is fired and replaced by a hash function modeled as a random oracle — and articulate what new, cheaper-to-audit but subtler failure mode is hired in exchange.
- Using the Seven-Layer Model as an institutional org chart, students must be able to state, for each layer, which party or mathematical assumption occupies the trusted seat and what it would cost — in capex, coordination, or migration pain — to replace that occupant without rebuilding the whole institution.

---

# Chapter 2: Layer 1 -- Building the Stage

### Prof. Elena Vasquez — Theoretical Cryptographer
- Define a Structured Reference String and Toxic Waste (Trapdoor) formally; state the theorem a KZG Commitment (deg 7) satisfies (evaluation binding under a q-type pairing assumption) and prove that knowledge of the trapdoor lets an adversary equivocate — then explain what property actually failed in the BCTV14 Bug (CVE-2019-7167).
- Formalize the 1-of-N Trust Model as a security game: the adversary corrupts N−1 participants of a BGM17 MMORPG Ceremony; state the theorem (one honest, randomness-destroying participant suffices) and its unstated preconditions — verifiable contribution transcripts, no subverted software — using the Wang-Cohney-Bonneau SoK (FC 2025, cited) as the critical checklist for what the Zcash Sprout and Ethereum KZG Summoning ceremonies actually guarantee versus claim.
- Distinguish Universal vs Circuit-Specific Setup with Sonic as the pivot: state precisely what updatability buys and why a Transparent Setup (deg 6) is a different *assumption class*, not merely a better ceremony.
- Analyze the Quantum Shelf Life of Trusted Setups against Harvest Now, Decrypt Later: derive exactly what a future discrete-log-breaking adversary can do with a published SRS (forge new proofs) versus cannot do (retroactively break the hiding of past commitments is a separate analysis) — and weigh the author's Capex/Opex Setup Economics rationale for what it admits to being: an economic argument, not a cryptographic one.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Own the picture of the Structured Reference String as a stage built from a secret blueprint: KZG needs powers of a secret tau, and whoever knows tau — the toxic waste — can forge. The worked object is the ceremony itself: trace one participant's contribution and deletion. Builds on Chapter 1's Seven-Layer map — this is Layer 1, the trust assumption that exists before any proof is made.
- Own the 1-of-N intuition through the concrete arc from Zcash Sprout (six participants, 2016) to the Ethereum KZG Summoning Ceremony (141,416 participants, 2023): the assumption weakens from "trust this group" to "trust that at least ONE of 141,416 strangers was honest." Builds directly on Chapter 1's trust-minimized-not-trustless thesis — this is the first worked example of decomposing trust rather than eliminating it.
- Stuck-point: students must be able to articulate why a compromised trusted setup is NOT a privacy leak — it is a soundness break. Toxic waste lets an attacker forge proofs of false statements (BCTV14, CVE-2019-7167: unlimited undetectable counterfeiting), while everyone's secrets stay perfectly hidden. Builds on Chapter 1's separation of soundness from the zero-knowledge property; students who fused those two properties get exactly this wrong.
- Understand the capex/opex economics of why ceremonies persist despite transparent alternatives: the ceremony is one-time capital expenditure amortized over every proof, and the hybrid STARK-to-SNARK pipeline previewed here shows the field refusing to pick a side. Builds on Chapter 1's framing that layer choices are engineering trade-offs, not moral positions.

### Priya Raghavan — Staff ZK Systems Engineer
- Run a local powers-of-tau ceremony end-to-end with snarkjs: contribute randomness, apply a random beacon, produce the Structured Reference String, and verify someone else's contribution — then explain what file on your disk is the toxic waste and why `rm` is a security-critical operation here.
- Demonstrate why the trapdoor matters by forging: given a KZG commitment setup where you kept tau, construct a fake opening proof and watch the verifier accept it — this is the BCTV14 bug (CVE-2019-7167) failure mode made tangible, counterfeit money with no alarm.
- Benchmark the Universal vs Circuit-Specific tradeoff: change one constraint in a Groth16 circuit and time the full phase-2 re-ceremony, then do the same under a universal-setup system and measure what actually needs redoing — this is the Capex/Opex economics framework as a wall-clock number.
- Trace the Hybrid STARK-to-SNARK Pipeline (the dominant 2026 production pattern per the graph, deg 6) and identify precisely which stage reintroduces the ceremony dependence and what its Quantum Shelf Life is — i.e., which byte of your system a Harvest-Now-Decrypt-Later adversary is storing today.

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Describe the purpose of a Trusted Setup Ceremony and the Structured Reference String it produces, evidenced by a written account that correctly explains why the toxic waste (trapdoor) must be destroyed.
- Summarize the 1-of-N trust model, with mastery shown by explaining in one paragraph why the Zcash Sprout (2016) and Ethereum KZG Summoning (2023) ceremonies remain sound if even a single participant was honest.
- Classify a given list of schemes (KZG-based, Groth16, STARK) along the trusted-versus-transparent and universal-versus-circuit-specific setup axes, evidenced by a correctly completed two-by-two sorting table.
- Interpret the BCTV14 bug (CVE-2019-7167) and the Quantum Shelf Life argument as cautionary evidence about setup risk, demonstrated by a short response identifying what each implies for ceremony design.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to model a trusted setup ceremony as an institution that converts "trust one party absolutely" into a 1-of-N honesty assumption, then analyze the incentive economics of participation: contrast Zcash Sprout's six participants (2016) with the Ethereum KZG Summoning's 141,416 (2023) and argue where the marginal participant stops buying security and starts buying legitimacy theater.
- Students must be able to explain why the BCTV14 bug (CVE-2019-7167) is the most instructive setup incident precisely because the ceremony was not compromised: the ritual verified the wrong artifact, undetectable counterfeiting risk fell silently on every Zcash holder, and remediation was done in secret — then argue what this implies about who audits the auditors of a ceremony.
- Students must be able to deploy the Capex/Opex Setup Economics Framework: the ceremony is one-time capital expenditure amortized across every proof, while transparent setups shift cost into per-proof operating expense — and argue, for a given deployment (universal SRS à la Sonic vs circuit-specific, on-chain vs off-chain verification), which side of the ledger a rational operator should load.
- Students must be able to grade a real ceremony against the ADOPT framework (Available/Decentralized/Open/Persistent/Transparent) and against BGM17's MMORPG rolling-participation design — identifying the coordinator's residual powers — and to price the Quantum Shelf Life problem: under Harvest-Now-Decrypt-Later, trust purchased in a ceremony today is a depreciating asset with an uncertain write-off date.

---

# Chapter 3: Choreographing the Act (Layer 2 -- Language)

### Prof. Elena Vasquez — Theoretical Cryptographer
- Define an Under-Constrained Circuit (deg 7) precisely: the relation the circuit enforces is a strict superset of the intended relation, hence a *soundness* failure with zero-knowledge fully intact. Reconstruct the Tornado Cash '=' vs '<==' Bug: identify the assignment that generated no constraint and construct the forged witness the gap admits.
- Read the Chaliasos et al. SoK (USENIX Security 2024, cited) with methodological suspicion: what counted as a SNARK vulnerability in the 67% figure, at which layer the bugs lived, and why "bugs, not cryptography" is the empirical claim the Four Layer-2 Language Philosophies taxonomy rests on.
- Map Circom, Compact (Midnight DSL), Cairo, and RISC-V onto the four philosophies and state, for each, where the soundness burden falls: hand-written constraints, compiler correctness, or ISA semantics — what the developer sees determines what the developer under-constrains.
- State formally what Picus (QED^2) and ZKAP verify — witness uniqueness/determinism as a proxy for being fully constrained — and identify the gap between "the analyzer found nothing" and "the circuit implements the intended relation," including where the disclose() Boundary analysis fits.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Own the intuition that a circuit language writes claims, not computations: nothing "runs," everything is asserted. The worked object is the 4x4 Sudoku rulebook itself — "every cell is in {1,2,3,4}, every row has no repeats" — written as constraints rather than as a checking loop. Builds on Chapter 1's Seven-Layer map: Layer 2 is where the informal claim "I solved it" becomes a formal language membership statement.
- Stuck-point: students must be able to articulate why assigning a value is NOT constraining it. The Tornado Cash '=' vs '<==' bug is one character wide, and under-constrained circuits are 67% of real SNARK vulnerabilities — the proof happily accepts any witness the constraints fail to pin down. Builds on Chapter 1's soundness: an unconstrained Sudoku cell is a hole through which a false statement gets proved true.
- Hold the four language philosophies (EVM-compatible, ZK-native ISA, general-purpose ISA, application-specific DSL) as a taxonomy of what the developer sees — because what the developer sees determines what bugs they make, and bugs, not cryptography, dominate the failure record. Builds on Chapter 1's trust decomposition: the compiler and the language design are themselves Layer 2 trust assumptions.
- Own the disclose() boundary as deliberate, audited revelation: in the Sudoku, the pre-filled clue cells are disclosed, the solution cells are not, and the line between them is drawn in source code where a reviewer can see it. Builds on Chapter 1's zero-knowledge property — this is the first place the abstract property becomes an engineering artifact.

### Priya Raghavan — Staff ZK Systems Engineer
- Reproduce the Tornado Cash '=' vs '<==' bug in Circom: write a MiMC-style circuit with assignment instead of constraint, generate a malicious witness that satisfies the underconstrained system, and get a valid proof for a false statement — then fix it and show the exploit witness now fails. Under-constrained circuits are 67% of SNARK vulnerabilities per the graph; this is the bug class to internalize in your fingers.
- Run an actual circuit static analyzer — Picus (QED^2) or ZKAP — against both your buggy and fixed circuit, and triage the output: which findings are the real underconstraint, which are noise, and what would you gate CI on.
- Implement the same range-check-plus-uniqueness logic (the Sudoku constraints) in three of the Four Layer-2 Language Philosophies — Circom (constraint DSL), Noir (compiling to ACIR), and a RISC-V zkVM guest program — and compare what the developer sees vs what actually gets constrained, because what the developer sees determines what bugs they make.
- Write a small Compact (Midnight DSL) contract and audit its `disclose()` boundary: enumerate exactly which values cross from private to public, and construct one case where a naive contract leaks more than the author intended.

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Classify Circom, Cairo, Noir, Leo, and Compact into the Four Layer-2 Language Philosophies (EVM-compatible, ZK-native ISA, general-purpose ISA, application-specific DSL), evidenced by sorting all five correctly with a one-line justification each.
- Explain why under-constrained circuits account for 67% of catalogued SNARK vulnerabilities, with mastery shown by articulating the difference between computing a value and constraining it.
- Apply the lesson of the Tornado Cash '=' versus '<==' bug by identifying and correcting the missing constraint in a supplied three-line Circom fragment, evidenced by the repaired code rejecting a forged witness.
- Use disclosure analysis to mark the disclose() boundary in a short Compact program, demonstrated by correctly labeling every value that crosses from private to public state.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to identify the trust migration this layer performs: the verifier no longer trusts the cryptographer's math but newly trusts the language designer and compiler author — and support it with the Chaliasos SoK finding that under-constrained circuits account for 67% of SNARK vulnerabilities: the developer, not the proof system, is the weakest counterparty.
- Students must be able to read the Tornado Cash '=' vs '<==' bug as a one-character trust failure with institutional lessons: an assignment that looks like a constraint shifts risk invisibly onto every user of the pool, and no ceremony or audit of the cryptography would have caught it — then argue what liability regime (audits, formal tools, language design) prices this risk correctly.
- Students must be able to analyze the Four Layer-2 Language Philosophies (EVM-compatible, ZK-native ISA, general-purpose ISA, application-specific DSL) as governance choices about who absorbs semantic-gap risk — what the developer sees determines what bugs they make — and cite the Polygon zkEVM sunset (2025/26) as the market pricing a losing bet on that spectrum.
- Students must be able to argue the regulatory and institutional value of Compact's disclose() boundary — making every act of revelation an explicit, auditable decision — and to evaluate verification tooling (Picus/QED^2, ZKAP) as a trust reallocation from individual developer diligence to tool vendors, with its own vendor-concentration cost.

---

# Chapter 4: The Secret Performance (Layer 3 -- Witness Generation)

### Prof. Elena Vasquez — Theoretical Cryptographer
- Define the Witness relative to an NP relation and separate witness generation from proving; then state the model boundary exactly: the zero-knowledge simulator argues about the verifier's *view in the protocol*, so The Witness Gap (deg 7, 50-70% of proving time) is computation the security proof never sees.
- Work through the Zcash Groth16 Timing Attack (R=0.57) via the cited Remote Side-Channel Attacks on Anonymous Transactions (USENIX 2020): show that the deployed system leaked witness-dependent timing while the ZK property, as defined, held — a clean specimen of a true theorem failing to protect a real user.
- Define Constant-Time Proving as a property (execution trace and timing independent of the witness for fixed public parameters) and explain why the Reinforced Concrete Hash's table lookups violate it — then say what Streaming Witness Generation changes about the memory-access side channel, and what it does not.
- Turn the Privacy as a Luxury Good rationale into a formal question: delegated proving hands the witness to a service, so state the trust assumption delegation reintroduces and judge whether it silently re-monolithizes the seven-layer decomposition Chapter 1 promised.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Own the witness as an object distinct from the proof: the witness IS the filled-in 4x4 grid — the secret performance itself — and the execution trace is its step-by-step recording. Builds on Chapter 3's constraints: the circuit defines which grids count as witnesses; this chapter is about actually producing one.
- Internalize the Witness Gap: 50-70% of proving time is spent generating the witness, before a single cryptographic operation happens. Streaming and GPU witness generation (ZKPoG, BatchZK) exist because the boring part is the expensive part. Builds on Chapter 3's languages — the compiler's output determines this cost, and students should trace one Sudoku constraint from source to witness slot.
- Stuck-point: students must be able to articulate why the zero-knowledge property is NOT zero leakage. ZK is a mathematical guarantee about the proof transcript; the machine generating the witness still radiates timing, and the Zcash Groth16 timing attack (R=0.57 correlation) recovered secret-dependent information from a system whose math was flawless. Builds on Chapter 1's precise statement of what the ZK property quantifies over — the transcript, not the prover's physical execution.
- Understand "privacy as a luxury good": client-side proving is maximal privacy but demands hardware most of the world lacks, so over 90% of users delegate proving and hand a service their secrets. Builds on Chapter 1's trust decomposition — delegation quietly reintroduces exactly the monolithic trust assumption the whole architecture set out to split.

### Priya Raghavan — Staff ZK Systems Engineer
- Profile a real prover run end-to-end (Circom witness gen + Groth16, or a zkVM trace) with `perf` or built-in timers and verify The Witness Gap claim yourself: is witness generation really 50-70% of total proving time on your workload? Report the split and identify the single hottest function.
- Reproduce the shape of the Zcash Groth16 timing attack: instrument proving time across witnesses with different secret values, compute the correlation (the paper found R=0.57), and explain why a remote adversary with only timestamps can deanonymize — then state what Constant-Time Proving would have to guarantee to kill it.
- Configure streaming witness generation (or simulate it by chunking) and measure peak RSS vs the naive materialize-everything approach — this is the difference between proving on a 16GB laptop and OOM-killing at 3am.
- Do the Privacy as a Luxury Good math for a concrete circuit: measure client-side proving time on a phone-class CPU vs a GPU box, and write the one-paragraph memo on who in your user base can prove locally and who must delegate their secrets to a proving service.

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Construct the complete witness and execution trace for the 4x4 Sudoku running example from a given solved grid, evidenced by a trace table that satisfies every range, uniqueness, and boundary constraint.
- Demonstrate why the Witness Gap consumes 50-70% of total proving time, with mastery shown by annotating a supplied proving-pipeline profile to isolate witness-generation cost from proof-generation cost.
- Apply constant-time proving principles to a short prover routine by flagging each secret-dependent branch or memory access, evidenced by a marked-up listing with a proposed fix for every flag.
- Illustrate the Zcash Groth16 timing attack (R=0.57) by computing what an observer learns from proving-time measurements in a worked scenario, demonstrated by a correct numerical inference about the hidden input.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to identify witness generation as the moment the entire trust-minimization story is at its weakest: the secret exists in plaintext on some machine, and whoever controls that machine must be trusted absolutely — no downstream cryptography can claw that trust back.
- Students must be able to analyze the Zcash Groth16 timing attack (R=0.57 correlation between proving time and witness content) as a side channel that leaks through a formally zero-knowledge system, and argue the economic trade it forces: constant-time proving imposes a performance tax on every honest prover to insure against an attacker most provers will never meet — who should pay it, and when is it rational to skip?
- Students must be able to work the "Privacy as a Luxury Good" argument end to end: client-side proving demands hardware most of the world does not own, so over 90% of users must delegate proving and hand their secrets to a service — then analyze the proving service's incentives (data monetization, subpoena exposure, uptime economics) and identify which non-cryptographic institutions (contracts, TEEs, regulation) are being substituted for the cryptography that was promised.
- Students must be able to argue how streaming witness generation, BatchZK pipelining, and GPU proving (ZKPoG) function as trust-redistribution policy, not mere optimization: every reduction in the hardware floor moves marginal users off the delegation ladder and shrinks the population forced to trust a third party.

---

# Chapter 5: Encoding the Performance (Layer 4 -- Arithmetization)

### Prof. Elena Vasquez — Theoretical Cryptographer
- Define R1CS (deg 12), AIR, and PLONKish Arithmetization as satisfiability relations, then prove the containments that make CCS (Customizable Constraint Systems, deg 10) a strict generalization of R1CS and PLONKish — this is a theorem, so prove it, don't gesture at it.
- State and prove soundness of the Sumcheck Protocol (deg 12) as LFKN 1992 (cited) gives it: the per-round soundness error d/|F| via the Schwartz-Zippel Lemma, and the union bound over rounds. This is the one proof in the book a student must be able to reproduce cold.
- Define the lookup relation and trace the edge chain Plookup → LogUp → LogUp-GKR → Lasso: state LogUp's fractional-sum identity and what Lasso (2023) adds for structured tables; then read The Lookup Singularity as what it is — a conjecture about where arithmetization is heading, not a proven endpoint.
- Decompose The Overhead Tax (10,000x-50,000x): attribute it to commitment costs (MSM), transform costs (NTT), and constraint blowup, and show how the choice among R1CS/AIR/CCS — and Jolt zkVM's lookup-centric bet — moves each term.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Own the move from rules to polynomials with one fully worked object: the Sudoku row-uniqueness check rewritten as an R1CS constraint (one multiplication per row of the matrix) and again as an AIR row transition, so students see R1CS, AIR, and PLONKish as three encodings of the same claim. Builds on Chapter 3's constraints and Chapter 4's witness — the witness values are what get slotted into these polynomial identities.
- Own Schwartz-Zippel as the engine of everything: two distinct low-degree polynomials agree almost nowhere, so checking one random point suffices. Work it numerically over a small field so the soundness error is a fraction students can compute. Builds on Chapter 1's soundness — this lemma is where "cheaters get caught with quantifiable probability" gets its actual number.
- Own lookup arguments through the smallest possible table: the Sudoku range check "cell in {1,2,3,4}" as a 4-entry lookup instead of bit decomposition, then extrapolate to Plookup, LogUp, Lasso, and the Lookup Singularity. Builds on Chapter 3's range constraints — the same rule, now proved by membership rather than re-derivation.
- Stuck-point: students must be able to articulate why arithmetization is NOT the proof system. R1CS and AIR are claim formats — Layer 4 output, Layer 5 input — and the Overhead Tax (10,000x-50,000x versus native execution) is paid here, in the encoding, not in the cryptography. Builds on Chapter 1's Seven-Layer separation; students who conflate Layers 4 and 5 cannot later understand why Jolt and Nova are innovations at different layers.

### Priya Raghavan — Staff ZK Systems Engineer
- Hand-compile the 4x4 Sudoku into R1CS, PLONKish, and AIR, and produce the comparison table: constraint count, column count, trace length — then explain which encoding wins for this workload and why CCS (Customizable Constraint Systems) claims to subsume all three.
- Implement the Sumcheck Protocol from scratch (it's deg 12 in this graph — arguably the most load-bearing algorithm in modern proving) and benchmark verifier work vs naively evaluating the sum: measure the O(n) → O(log n) collapse, and use Schwartz-Zippel to compute your actual soundness error for your field size.
- Replace a bit-decomposition range check with a lookup argument (the Plookup → LogUp → Lasso lineage) in a real circuit and measure the constraint savings — then articulate The Lookup Singularity thesis: what fraction of your circuit could become "just lookups"?
- Measure The Overhead Tax empirically: run a program natively, then prove it on Jolt or another RISC-V zkVM, and compute cycles-proved per cycle-executed. Verify whether your number lands in the graph's 10,000x-50,000x band, and attribute the tax across MSM/NTT/witness costs.

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Translate the 4x4 Sudoku uniqueness and range constraints into R1CS form, evidenced by a constraint matrix that a checker script verifies against both a valid and an invalid witness.
- Execute one full round of the Sumcheck Protocol on a supplied three-variable polynomial, demonstrated by producing the correct univariate restriction and verifier check at each step.
- Compare R1CS, PLONKish arithmetization, AIR, and CCS on expressiveness and prover cost, evidenced by a completed comparison matrix that correctly identifies CCS as the generalization subsuming the others.
- Analyze how the lookup-argument lineage (Plookup, LogUp, Lasso) attacks the 10,000x-50,000x Overhead Tax, with mastery shown by a written argument tracing which cost term each successive scheme removes.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to analyze the Overhead Tax (10,000x-50,000x native execution cost) as a tariff on verifiability: the prover pays it, the verifier and every downstream relying party collect the benefit — and argue which classes of computation clear that tariff economically and which never will.
- Students must be able to identify the new trusted party this layer creates: the arithmetizer that translates a program into R1CS, PLONKish, AIR, or CCS constraints — a mistranslation is invisible to both prover and verifier — and argue why the choice among these formats is a quasi-constitutional commitment that binds the layers above it with heavy switching costs.
- Students must be able to explain the Lookup Singularity (Plookup, LogUp, Lasso, LogUp-GKR) as an economic substitution — replacing per-operation constraint arithmetic with precomputed tables that slash Jolt-style zkVM prover costs — and identify the trust consequence: the table itself becomes a new auditable artifact whose correctness everyone silently assumes.
- Students must be able to read the Schwartz-Zippel lemma and the sumcheck protocol as actuarial instruments: soundness here is not certainty but a priced probability over random field elements — trust is reallocated from any human party to the size of a field and the integrity of a randomness source, which is precisely what makes it cheap.

---

# Chapter 6: Layer 5 -- The Sealed Certificate

### Prof. Elena Vasquez — Theoretical Cryptographer
- Define IVC (Incrementally Verifiable Computation) and a folding scheme precisely; state Nova's theorem (deg 10): two R1CS instances fold into one Relaxed R1CS instance with knowledge soundness — and prove why the relaxation (slack vector and scalar) is forced by the cross-terms, not a stylistic choice.
- Compare Groth16 (192-byte proofs) and PLONK (both deg 9) as construction-theorem-assumption triples: pairing-based knowledge assumptions versus AGM analyses, circuit-specific versus universal SRS, and what each buys in proof size and verifier cost. Distrust any comparison that omits the assumption column.
- Dissect the Frozen Heart Vulnerability Class (2022): identify exactly which transcript elements a weak Fiat-Shamir instantiation omitted from the hash, and construct the forgery — this is Chapter 1's transform failing at the implementation layer, and it recurs in Chapter 8.
- Follow the lattice folding lineage LatticeFold (ASIACRYPT 2025) → LatticeFold+ → Neo (Lattice Folding over Goldilocks) → Symphony, with Nightstream (15 Rust crates) as Neo's implementation: state the Module-SIS-flavored assumption underneath and the norm-growth problem every lattice folding step must control — the graph's densest cluster of new results, so read the theorem statements, not the announcements.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Own the proof system as the machine that consumes an arithmetized claim plus a witness and emits a sealed certificate, with Groth16's 192-byte proof as the extreme point of the design space and PLONK/Halo 2 as the flexible middle. Builds on Chapter 5's Proof Core triad — Layer 4's output format is precisely Layer 5's input format, and students should name the handoff explicitly.
- Own folding as the snowball: Nova does not prove each step, it folds two claims into one running claim and proves once at the end. Anchor with the Sudoku — fold the four row-check claims into a single relaxed-R1CS claim before ever touching a proof. Builds on Chapter 5's R1CS: relaxed R1CS is that same object with slack added so addition of claims stays meaningful.
- Distinguish recursion (Russian doll: a proof verifying a proof) from folding (snowball: claims merged pre-proof), and see why the hybrid STARK-to-SNARK pipeline and real-time Ethereum proving both depend on this distinction. Builds on Chapter 2's preview of the hybrid pipeline — this chapter supplies the mechanism that chapter only gestured at.
- Stuck-point: students must be able to articulate why Fiat-Shamir is NOT a mechanical detail. The Frozen Heart vulnerability class (2022) broke multiple independent implementations the same way: hash too little of the transcript and soundness dies while everything still "works." Builds on Chapter 1's introduction of the Fiat-Shamir Transform — the interactive game students played by hand is exactly what the hash must faithfully replace, challenge by challenge.

### Priya Raghavan — Staff ZK Systems Engineer
- Prove the same circuit under three regimes — Groth16 (192-byte proofs), a PLONK-family system via Halo 2, and a FRI-based STARK — and produce the three-way benchmark: prover time, proof size, verifier time, and setup requirements. This table is the entire SNARK-vs-STARK debate in one artifact.
- Build a toy folding step: implement Relaxed R1CS and fold two instances into one à la Nova, then run real Nova (or read Nightstream's Neo implementation, 15 Rust crates) and measure IVC step cost vs re-proving monolithically — the Folding (Snowball) claim only means something once you've timed both sides.
- Dissect the Frozen Heart vulnerability class: take a Fiat-Shamir transcript from a PLONK implementation, identify exactly which public inputs must be absorbed before each challenge, remove one, and demonstrate (or at least whiteboard) the forgery — this is the bug that hit multiple production codebases in 2022 and it lives at this layer.
- Run Stwo (StarkWare's Circle STARK prover) over M31 and compare prover throughput against a Plonky3 baseline, then explain why Circle STARKs exist at all — what Mersenne-31 lacks that the circle-group construction restores — and how that connects to the Real-Time Ethereum Proving race.

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Differentiate folding (Nova, relaxed R1CS) from recursive proof composition (the Russian Doll), evidenced by an annotated diagram plus a cost argument identifying where each defers versus performs verification work.
- Analyze the Groth16-versus-PLONK trade-off — 192-byte circuit-specific proofs against larger proofs with a universal setup — demonstrated by a written analysis that correctly attributes each property to its Layer 1 setup choice.
- Deconstruct the Frozen Heart vulnerability class into its root cause, evidenced by tracing a supplied broken transcript to the specific public input omitted from the Fiat-Shamir hash.
- Examine how HyperNova and the lattice-folding line (LatticeFold, Neo, Symphony) extend Nova's folding to CCS and post-quantum settings, with mastery shown by a lineage map that correctly orders the schemes and states what each generation adds.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to explain why Groth16's 192-byte proofs keep winning in production despite requiring a circuit-specific ceremony: on-chain verification is perpetual opex and Groth16 minimizes it, so operators rationally accept a one-time trust capex — the Hybrid STARK-to-SNARK pipeline exists precisely to buy that cheap opex while quarantining the ceremony to a single small wrapper circuit.
- Students must be able to analyze the Frozen Heart vulnerability class (2022) as a trust-boundary lesson: the papers were sound, the implementations of Fiat-Shamir were not, across multiple independent libraries — so the relying party's real counterparty is the implementer, and governance must fund audits of code, not admiration of proofs.
- Students must be able to argue the market-structure consequence of folding and recursion (Nova, HyperNova, ProtoStar, CycleFold, and the lattice line through LatticeFold, Neo, and Symphony): aggregation and Real-Time Ethereum Proving reward scale, concentrating proving into a small oligopoly of operators — re-centralizing an industry whose sales pitch was decentralization.
- Students must be able to read the Ethereum Foundation Security Pivot (Dec 2025) as an institutional correction: a protocol governance body reallocating resources from privately-capturable performance gains toward soundness, a public good the market was under-supplying — and evaluate whether that correction mechanism generalizes.

---

# Chapter 7: Layer 6 -- The Deep Craft

### Prof. Elena Vasquez — Theoretical Cryptographer
- Define a Polynomial Commitment Scheme (deg 9) via its games (binding, hiding, evaluation binding / knowledge extraction) and instantiate it three ways with full theorem-assumption pairing: KZG under pairing assumptions on BLS12-381, Bulletproofs/IPA under Discrete Logarithm via Pedersen Commitments, FRI under Collision-Resistant Hash Functions alone — and annotate each with its status against Shor's and Grover's algorithms.
- Module-SIS is the highest-degree node in this chapter's neighborhood (deg 13): define the problem, state the reduction that makes Ajtai / Lattice Commitments binding, and place Greyhound (Lattice SNARK, 2024) and the NIST PQC Standards on that foundation.
- Read the Cryptographic Primitives Trilemma adversarially — the digest flags it as the author's own framing, "explicitly not from the literature": treat "at most two of algebraic functionality, post-quantum security, succinctness" as a falsifiable snapshot and test it against Greyhound and the lattice folding line from Chapter 6.
- Quantify concrete security and its consequences: BN254 at ~100 bits after the Tower Number Field Sieve, the Small-Field Revolution (Goldilocks, BabyBear, Mersenne-31), and The Cascade Effect / One-Way Door — evaluate whether "crypto-agility is largely fiction" follows with the claimed algebraic necessity, layer by layer.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Own the polynomial commitment scheme as the load-bearing primitive of the whole edifice: commit to the Sudoku-trace polynomial first, then open it at the verifier's randomly chosen point. KZG, FRI, IPA, and Ajtai lattice commitments are four ways to make that one promise binding. Builds on Chapter 5's Schwartz-Zippel (why one random evaluation suffices) and Chapter 2's KZG (whose SRS students already watched get built).
- Own the Cryptographic Primitives Trilemma — algebraic functionality, post-quantum security, succinctness: pick two — by placing KZG, FRI, and lattice commitments on the triangle and checking each corner against a system from Chapter 6. Builds on Chapter 2's trusted setup: KZG's corner of the triangle is purchased with exactly the ceremony students already priced.
- Own the Cascade Effect: the Layer 6 field choice propagates upward with algebraic necessity — Goldilocks, BabyBear, and Mersenne-31 each force different commitments, proof systems, and arithmetizations, which is why crypto-agility is largely fiction here. Builds on Chapter 5's arithmetization-over-a-field and Chapter 6's Circle STARKs, which exist precisely because M31 lacks a convenient multiplicative subgroup.
- Stuck-point: students must be able to articulate why "post-quantum soundness" is NOT "quantum-safe." Shor's algorithm breaks discrete-log-based hiding retroactively — harvest-now-decrypt-later reaches back in time to today's transcripts — while a future soundness break only enables future forgeries. Builds on Chapter 2's Quantum Shelf Life and HNDL: the threat model students met at Layer 1 returns here with its full mechanism exposed.

### Priya Raghavan — Staff ZK Systems Engineer
- Implement one FRI folding round and the query phase, then compute the concrete tradeoff: for your target security level, how many queries at what blowup factor, and what that does to proof size — FRI is deg 10 here for a reason; it's the engine under every transparent system you'll deploy.
- Microbenchmark field multiplication throughput for Goldilocks (64-bit), BabyBear (31-bit), and Mersenne-31 on your actual hardware (CPU with and without vectorization; GPU if you have one) — the Small-Field Revolution is a throughput claim, so hold it to a measured number.
- Verify the "BN254 ~100-bit security after Tower NFS" claim against primary sources: read the Tower Number Field Sieve literature and at least one concrete-security estimate, and write down what the real number is and whether your Groth16-on-BN254 deployment should care — the graph asserts this figure; your job is to confirm or refute it.
- Trace The Cascade Effect / One-Way Door for two systems: show how choosing BLS12-381 vs BabyBear at layer 6 algebraically forces the commitment scheme (KZG/Pedersen vs FRI/hash), the proof system, and the arithmetization above — then test the Cryptographic Primitives Trilemma against Ajtai/lattice commitments and Greyhound: which two of algebraic-functionality/post-quantum/succinctness do they achieve, and is the trilemma cracking?

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Analyze the Cryptographic Primitives Trilemma by placing KZG, FRI, Bulletproofs/IPA, and Ajtai lattice commitments on its three axes (algebraic functionality, post-quantum security, succinctness), evidenced by a placement diagram with a defensible justification for each vertex.
- Organize the Cascade Effect into an explicit dependency chain — field choice determines commitment scheme determines proof system determines arithmetization — demonstrated by tracing two concrete stacks (BN254/KZG/PLONK and M31/FRI/Circle STARK) through all four links.
- Attribute the post-quantum status of each major polynomial commitment scheme to its underlying hardness assumption (discrete log, collision-resistant hashing, Module-SIS), evidenced by a table stating which schemes Shor's algorithm breaks and why.
- Examine the Small-Field Revolution by comparing Goldilocks, BabyBear, and Mersenne-31 against 256-bit fields, with mastery shown by a written analysis connecting field size to hardware arithmetic cost and to FRI-based proving.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to articulate what trust at the bottom layer actually is: confidence in mathematical conjectures (discrete log, Module-SIS, hash collision resistance) enforced by no counterparty at all, only by the community of cryptanalysts attacking them — and use BN254's depreciation from 128 to ~100 bits under the Tower Number Field Sieve to argue that assumptions are wasting assets requiring a monitoring-and-migration budget nobody is contractually obliged to fund.
- Students must be able to apply the author's Cryptographic Primitives Trilemma — algebraic functionality, post-quantum security, succinctness: pick two — as a procurement decision, mapping which stakeholder (on-chain verifier, privacy user, long-horizon archivist) is sacrificed at each corner, from KZG/Pedersen through FRI to Ajtai commitments and Greyhound.
- Students must be able to argue the Cascade Effect / One-Way Door as a governance fact: the field choice (Goldilocks, BabyBear, Mersenne-31, BLS12-381's scalar field) determines the commitment scheme, which determines the proof system, which determines the arithmetization — so "crypto-agility" is largely fiction here, and primitive selection is a constitutional commitment made once, contrasted with NIST PQC standardization (FIPS 203/204/205) as the institutional hedge.
- Students must be able to price the quantum question as an insurance decision: Shor's algorithm gives pairing-based trust a shelf life and HNDL makes the exposure retroactive, so choosing FRI or lattice primitives is paying a present premium (bigger proofs, higher opex) against a loss of uncertain date — and argue which deployments (payments vs decades-long identity records) rationally buy the policy.

---

# Chapter 8: Layer 7 -- The Verdict

### Prof. Elena Vasquez — Theoretical Cryptographer
- Define Data Availability (deg 5) as an assumption *orthogonal* to proof soundness: a verified state-transition proof over unpublished data still strands users. State the DA-Saturation Attack as a game and place EIP-4844 Blobs and Celestia as mitigations with their own assumptions.
- Analyze the Last Challenge Attack (gnark, 2023/24) and the Solana ZK ElGamal Fiat-Shamir Bugs (2025) as verifier-side members of the Frozen Heart class from Chapter 6: specify the complete set of values a verifier must include in the Fiat-Shamir hash, and prove what an omission concedes.
- Translate the L2Beat Stages Framework (Stage 0/1/2) into formal trust statements: who can replace or override the verifier. The Tornado Cash CREATE2 Governance Attack and the Beanstalk Flash-Loan Governance Attack ($182M) show a perfectly sound proof system governed by an unsound key — soundness composed with upgradability is only as strong as the upgrade key.
- Separate liveness from soundness in the proving market: state what Proof Aggregation (SHARP, Aligned Layer) preserves — per-statement soundness — and what the Prover-Killer Attack targets instead, which no soundness theorem addresses.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Own the intuition that a valid proof is a sentence, not a verdict: Layer 7 is where the certificate meets a verifier contract, a governance process, and a data-availability layer, and any of the three can nullify what the mathematics established. Builds on Chapter 1's Seven-Layer map — this closes the loop, and students should re-draw the map with the trust assumption of each layer now filled in.
- Own data availability through the Sudoku: a checker attesting "a valid solved grid exists and was applied" is worthless to you if nobody will hand you the grid — you cannot compute your own balance, you cannot exit. EIP-4844 blobs, Celestia, and the DA-Saturation Attack are the industrial version. Builds on Chapter 6's sealed certificate: succinctness is precisely what makes it possible for the proof to arrive without the data.
- Stuck-point: students must be able to articulate why "verified on-chain" is NOT "secure." Beanstalk lost $182M and Tornado Cash lost its governance to attacks that never touched a proof — a flash-loaned majority or a CREATE2 metamorphic contract simply changes what the verifier accepts. Builds on Chapter 1's trust decomposition: the verifier's owner is the seventh assumption, and it is the one attackers actually exercise.
- Connect the Last Challenge Attack (gnark) and the Solana ZK ElGamal Fiat-Shamir bugs back to Chapter 6's Frozen Heart class: the same transcript-hashing failure, now surfacing at the verification layer, in production, twice. Builds on Chapter 6 — students should diagnose the gnark bug themselves using only the Frozen Heart pattern before reading the disclosure.

### Priya Raghavan — Staff ZK Systems Engineer
- Cost out on-chain verification for real: measure gas for a Groth16 verify, a STARK verify, and an aggregated route (SHARP-style shared proving or Aligned Layer), and compute the batch size at which Proof Aggregation amortization beats direct verification — this is the number that decides your architecture.
- Take one live rollup and classify it yourself against the L2Beat Stages Framework (Stage 0/1/2): find the upgrade keys, the security council, the exit window, and write down exactly who can steal funds despite valid proofs — the proof being sound and the system being safe are different layers.
- Walk the Last Challenge Attack on gnark's PLONK verifier (2023/24) and the Solana ZK ElGamal Fiat-Shamir bugs (2025): in each case, identify the transcript element that wasn't bound, and write the checklist you'd apply when auditing any verifier's challenge derivation.
- Model the availability attacks that page you: simulate a Prover-Killer transaction (pathological input that blows up proving cost) and reason through a DA-Saturation Attack against EIP-4844 blob capacity or Celestia — Data Availability is deg 5 here because a chain with valid proofs and unavailable data is still a dead chain.

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Evaluate a given rollup's deployment against the L2Beat Stages framework, evidenced by a written Stage 0/1/2 assignment defending each criterion with evidence from the rollup's published architecture.
- Judge whether a system's data availability choice (Ethereum EIP-4844 blobs versus Celestia) preserves or reintroduces trust, demonstrated by a verdict memo that weighs the DA-Saturation Attack against cost.
- Critique the claim that a sound proof system implies a secure system, using the Beanstalk flash-loan ($182M) and Tornado Cash CREATE2 governance attacks as evidence, with mastery shown by locating each attack outside Layers 4-6 in the seven-layer stack.
- Assess the verifier-side attack surface by ranking the Last Challenge Attack, Prover-Killer Attack, and Solana ZK ElGamal Fiat-Shamir bugs by severity for a specified deployment, evidenced by a justified risk ranking.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to expose the last trusted party in the stack: the verifier is a smart contract with an admin key, and the L2Beat Stages Framework (Stage 0/1/2) is precisely an audit of how much governance trust survives the mathematics — a Stage 0 rollup is a trusted operator wearing a proof as ornament.
- Students must be able to analyze the Beanstalk flash-loan governance attack ($182M, 2022) and the Tornado Cash CREATE2 governance attack (2023) as failures of the institution surrounding the proof, not the proof: flash loans make voting power a rentable commodity, so any system whose upgrade keys answer to token votes has put its trust anchor up for auction.
- Students must be able to argue why proofs guarantee validity but never availability: work the DA-Saturation and Prover-Killer attacks as liveness extortion priced in gas and hardware, identify who bears exit risk when data is withheld, and evaluate Celestia and EIP-4844 blobs as markets that price data availability as a separate trust product.
- Students must be able to treat verifier implementations as the trusted computing base — using the gnark Last Challenge Attack and the Solana ZK ElGamal Fiat-Shamir bugs (2025) — and analyze shared verification infrastructure (SHARP, Aligned Layer, proof aggregation) as the classic scale bargain: amortized cost for everyone in exchange for a single, fatter point of failure.

---

# Chapter 9: Privacy-Enhancing Technologies

### Prof. Elena Vasquez — Theoretical Cryptographer
- Place ZK among the Privacy-Enhancing Technologies (deg 7) by writing each one's security game: ZK (verifier learns nothing beyond validity), Secure Multi-Party Computation (no tolerated coalition learns beyond the output), Fully Homomorphic Encryption (evaluator learns nothing about plaintexts), Differential Privacy (bounded single-record influence), TEEs (hardware attestation trust) — different adversaries, different guarantees, never interchangeable.
- State what Verifiable FHE (zkFHE) composes: FHE gives confidentiality, ZK adds integrity of the homomorphic evaluation — and derive the composed system's assumption stack, which is the union, not the intersection, of the two.
- Define Zexe's function privacy formally as hiding *which* relation was proven, not merely the witness, and state why this is a strictly stronger notion than Chapter 1's zero-knowledge — Kachina's "privacy as a parameter" is the framework for saying it precisely.
- Read Privacy Pools (0xbow) against GDPR and eIDAS 2.0 critically: write the selectively disclosed predicate as a formal statement and identify where regulatory language ("erasure," "minimization") fails to map onto any cryptographic definition in this book.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Own the PET matrix as a division of labor, not a ranking: ZK proves statements about hidden data, FHE computes on data it cannot read, MPC computes jointly across mutually distrusting parties, differential privacy releases aggregates, TEEs relocate the trust into silicon. One row each, one canonical use case each. Builds on Chapter 1's precise statement of what ZK delivers — students can only place ZK in the matrix if they know exactly what it does and does not promise.
- Stuck-point: students must be able to articulate why zero-knowledge is NOT anonymity. The ZK property hides the witness inside one proof; it says nothing about who submitted it, when, from where, or which program was run — Zexe exists precisely to add function privacy that ZK alone never provided. Builds on Chapter 4's side-channel and metadata lesson and Chapter 3's disclose() boundary: leakage lives outside the transcript, again.
- Understand composition as the frontier: verifiable FHE (zkFHE) staples ZK's integrity onto FHE's confidentiality, and Kachina makes privacy a per-contract parameter rather than a system property. Builds on Chapter 8's verdict layer — these hybrids are answers to the question "what should the contract be allowed to see?"
- Read eIDAS 2.0 and GDPR as demand-side forces: regulators are mandating selective disclosure, which is disclose() from Chapter 3 elevated to law. Builds on Chapter 3's disclosure analysis — the same boundary, drawn now by legislators instead of developers.

### Priya Raghavan — Staff ZK Systems Engineer
- Build the PET decision matrix with measured numbers, not vibes: for one concrete task (say, private set membership), benchmark or gather primary-source benchmarks for ZK proof, FHE (ciphertext ops/sec), MPC (rounds and bandwidth), and a TEE — latency, throughput, and the trust assumption each one smuggles in.
- Prototype the Privacy Pools (0xbow) mechanism: prove Merkle membership in an approved association set without revealing which leaf you are — this is the design that threads regulatory compliance (GDPR, sanctions) through a shielded pool, and it's ~100 lines of Circom on top of what you built in Chapter 3.
- Analyze where Verifiable FHE (zkFHE) composition actually breaks: identify which party can cheat in plain FHE (the compute server), what the ZK proof must attest to, and estimate the proving overhead of proving FHE ciphertext operations — then judge whether Kachina's "privacy as a parameter" framing or Zexe's function privacy is the nearer-term deployable.
- Map one eIDAS 2.0 selective-disclosure requirement onto a concrete ZK identity flow: which credential fields become witness, what gets disclosed, and what the 3am failure looks like when the issuer's key rotates.

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Evaluate the fit of ZK proofs, FHE, MPC, TEEs, and differential privacy for three supplied deployment scenarios, evidenced by a decision matrix that selects one PET per scenario and defends each rejection.
- Judge whether a given credential design satisfies eIDAS 2.0 and GDPR data-minimization requirements, demonstrated by a compliance verdict citing the specific selective-disclosure property that carries the argument.
- Critique Privacy Pools (0xbow) as a resolution of the privacy-versus-compliance tension, with mastery shown by a written appraisal that identifies both the mechanism's strongest guarantee and its weakest residual assumption.
- Defend or refute the composability claim behind verifiable FHE (zkFHE) — that proving correct computation over encrypted data combines the guarantees of both PETs — evidenced by an argument that names the cost or trust assumption the combination adds.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to map the PET family by counterparty structure rather than by mechanism: ZK trusts no one with the data but proves facts about it, MPC trusts a threshold of parties, FHE trusts a server with ciphertext but not keys, TEEs trust a hardware vendor's supply chain, differential privacy trusts a curator's noise budget — and price each structure in capex, opex, and residual exposure.
- Students must be able to analyze Privacy Pools (0xbow) as a negotiated settlement between privacy and compliance: proving membership in an innocent association set without full disclosure — and identify the new institution it quietly creates, the governor of the allowed set, whose listing decisions are the real locus of power.
- Students must be able to argue how eIDAS 2.0 and GDPR act as demand-side forces that relocate trust from platforms to states: when selective disclosure is regulated into wallets, the government-anchored issuer becomes the root of the trust graph — evaluate what citizens gain against platforms and what they newly owe to issuers.
- Students must be able to run the composition economics of hybrid designs (Kachina's privacy-as-a-parameter, Zexe's function privacy, verifiable FHE): stacking PETs multiplies cost, so argue concretely when a cheap TEE with vendor trust rationally beats an expensive zkFHE stack — the trust-minimization premium is not always worth paying.

---

# Chapter 10: The Synthesis -- Three Paths, Not Two

### Prof. Elena Vasquez — Theoretical Cryptographer
- State each path as an assumption profile, and prove the composition rule that governs it: for the Hybrid STARK-to-SNARK Pipeline (deg 6), composite soundness and quantum resistance are those of the *weakest* stage — so the transparent, post-quantum inner STARK inherits the Groth16 wrapper's pairing assumptions and trusted setup at the boundary. The "dominant 2026 production pattern" is a tradeoff, not a free lunch.
- Contrast Path Two: Pure Transparent (hash assumptions only, larger proofs) and Path Three: Post-Quantum Folding (Module-SIS, from Chapters 6-7) by which of the seven layers each eliminates and which it merely relocates.
- Evaluate the rationale's claim that the SNARK-vs-STARK debate "was a false dichotomy" as a critical-reading exercise: does the layered decomposition genuinely dissolve the dichotomy, or does the hybrid pipeline simply choose SNARK assumptions at the final layer?
- Reconstruct the Seven-Layer Causal DAG (14 Edges) and audit it against Chapter 7's Cascade Effect: verify each claimed edge is a real dependency (algebraic necessity) and not a design convention, and mark which edges Trust Decomposition (Seven Weaker Assumptions) treats as cryptographic versus procedural.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Own the Seven-Layer Causal DAG (14 edges) well enough to re-derive it: given any layer choice — say Goldilocks at Layer 6 — students should trace which commitments, proof systems, and arithmetizations it forces, edge by edge. Builds on Chapter 7's Cascade Effect; the DAG is that cascade drawn once, completely.
- Own why "SNARK vs STARK" was a false dichotomy: the hybrid STARK-to-SNARK pipeline (transparent inner proof, Groth16 wrapper for cheap on-chain verification) is the dominant production pattern, and Paths Two (pure transparent) and Three (post-quantum folding) are its live competitors. Builds on Chapter 2's first sighting of the hybrid pipeline and Chapter 6's recursion, which is the mechanism that makes wrapping possible.
- Stuck-point: students must be able to articulate why trust decomposition is NOT trust elimination. Seven weaker assumptions are a conjunction — every one must hold, and the system is exactly as strong as the weakest — so the synthesis chapter is a weakest-link audit, not a victory lap. Builds on Chapter 1's trust-minimized thesis, which students can now defend with a named assumption and a named historical failure at every layer.
- Place Path Three (post-quantum folding) as a coherent research program rather than a grab bag: LatticeFold, Neo, and Symphony are folding from Chapter 6 rebuilt on the lattice commitments of Chapter 7. Builds on both — students should say which layer each paper innovates at, using the DAG.

### Priya Raghavan — Staff ZK Systems Engineer
- Reconstruct the Seven-Layer Causal DAG (14 Edges) for a system you've actually run in earlier chapters: draw the edges, and for at least three of them demonstrate the causality with an experiment (change the layer-6 field, show what breaks upstream).
- Run the path-selection exercise as an architecture review: given three requirement sets (cheapest on-chain verification today; no ceremony ever; must survive a quantum adversary), choose between the Hybrid STARK-to-SNARK Pipeline, Path Two: Pure Transparent, and Path Three: Post-Quantum Folding — and defend each choice with the benchmark numbers you collected in Chapters 6-8.
- Build the smallest possible hybrid pipeline yourself: take a STARK proof (SP1 or RISC Zero output), run its Groth16 wrap stage, and measure wrap latency and final proof size — then state which of the Seven Weaker Assumptions from the Trust Decomposition thesis each half of the pipeline carries.

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Evaluate the book's claim that the SNARK-versus-STARK debate was a false dichotomy, evidenced by a written argument that uses the Hybrid STARK-to-SNARK Pipeline's production dominance as its central exhibit.
- Justify a choice among the three paths (hybrid pipeline, pure transparent, post-quantum folding) for a specified application profile, demonstrated by a recommendation memo that scores each path against the application's setup, quantum, and verification-cost requirements.
- Critique the Trust Decomposition thesis by testing the Seven-Layer Causal DAG (14 edges) for a missing or contestable edge, with mastery shown by either defending the DAG as complete or proposing one amended edge with supporting evidence from earlier chapters.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to defend the Hybrid STARK-to-SNARK Pipeline as an institutional compromise, not a technical inevitability: the transparent STARK core spends no ceremony trust and buys post-quantum cover, while the Groth16 wrapper spends a small, quarantined ceremony to buy cheap on-chain opex — and identify exactly which residual trust survives in the wrapper.
- Students must be able to present the three paths as portfolio strategies over trust assumptions — hybrid (accept a contained ceremony), Pure Transparent (pay perpetual verification opex), Post-Quantum Folding (pay novelty risk on young lattice assumptions) — and match each to a deployer profile by time horizon, threat model, and balance sheet.
- Students must be able to interrogate Trust Decomposition (Seven Weaker Assumptions) using the Seven-Layer Causal DAG (14 edges): decomposition only delivers its promised risk reduction if the assumptions are independent, so trace where the DAG's edges create correlated failure — a shared hash function or field choice that couples layers turns seven assumptions back into three.
- Students must be able to state the economic core of the book's thesis: the value of decomposition is replaceability — a failed layer can be swapped without institutional collapse, like replacing an official rather than a constitution — and the price is a larger audit surface and coordination cost, which must be argued, not assumed, to be worth it.

---

# Chapter 11: zkVMs -- The Universal Stage

### Prof. Elena Vasquez — Theoretical Cryptographer
- Define a zkVM precisely: the proven relation is "this Execution Trace is a valid run of RISC-V program P on input x," which moves the soundness burden from per-circuit constraints (Chapter 3) to a one-time-audited ISA constraint system — state what is gained and what single point of failure is created.
- State Jolt zkVM's central thesis (deg 10, spanning Chapters 5 and 11): every instruction's semantics as a Lasso lookup into a structured table, verified via Sumcheck — connect the theorem chain sumcheck-soundness → Lasso → instruction correctness, and contrast it with the AIR/STARK route taken by RISC Zero and SP1 Hypercube.
- Impose benchmark hygiene on the prover comparisons (SP1 Hypercube, Airbender, ZisK, Plonky2/Plonky3, Pico Prism): a speed claim is meaningless unless field, targeted security bits, ISA, and recursion depth are held fixed — reject any table that doesn't state all four.
- Trace the cross-layer consequences: a zkVM's arithmetization commitment (small fields, lookup-centric or AIR) fixes its Layer 6 primitive choices by Chapter 7's Cascade Effect — show this concretely for one lookup-centric and one STARK-based system.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Own the zkVM inversion: prove the CPU once, not each program — one circuit for the RISC-V instruction set, and your Sudoku checker becomes ordinary Rust compiled like any other binary. Builds on Chapter 3's ZK-native-ISA philosophy and Chapter 4's execution trace, which is exactly the object a zkVM arithmetizes step by step.
- Own how Jolt realizes the Lookup Singularity: instruction semantics become giant precomputed tables, and proving an ADD means proving one table membership via Lasso. Builds on Chapter 5's lookup arguments — the 4-entry Sudoku range table, scaled to 2^128 entries by structure.
- Stuck-point: students must be able to articulate why a zkVM's generality is NOT free. The Overhead Tax is paid on every emulated instruction, so a hand-built circuit or application DSL still wins by orders of magnitude when the workload is fixed — the four language philosophies of Chapter 3 remain a live engineering choice, not a settled question. Builds on Chapter 5's Overhead Tax and Chapter 3's taxonomy.
- Read the performance race — SP1 Hypercube, Airbender, ZisK, Pico Prism, Plonky3 — as competing routes to Chapter 6's real-time Ethereum proving target, and evaluate each announcement by asking which layer of the DAG it actually changed. Builds on Chapter 6's real-time proving and Chapter 10's DAG discipline.

### Priya Raghavan — Staff ZK Systems Engineer
- Run the same Rust guest program (a SHA-256 loop is the classic) on SP1, RISC Zero, and Jolt, and publish the four-column benchmark: reported cycles, prover wall-clock, peak memory, proof size — then re-run with the hash precompile/accelerator enabled and measure the delta, because precompiles are where zkVM benchmarks go to lie.
- The graph's edge for Airbender (ZKsync) is ambiguous about its base field — resolve it against primary sources: read the zksync-airbender repo and the ZKsync team's write-ups, pin down the actual field (and whether it matches the BabyBear/Mersenne-31 pattern of its peers), and note which claim in the digest was wrong. Same drill for ZisK while you're at it; never trust a knowledge graph over a repo.
- Explain, at the constraint level, how Jolt's Lasso-lookup-centric design differs from the AIR-plus-FRI architecture of SP1/RISC Zero/Airbender: pick one RISC-V instruction (say ADD with overflow) and trace how each camp constrains it — lookup table versus trace columns.
- Evaluate the newest entrants with production skepticism: for SP1 Hypercube's real-time-Ethereum claims and Pico Prism (Brevis), find the primary benchmark, identify the hardware it required (how many GPUs?), and compute the dollar cost per block proved — the graph gives you names; the invoice gives you truth.

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Evaluate Jolt, SP1 Hypercube, RISC Zero, Airbender, and ZisK against a common rubric (arithmetization strategy, field choice, recursion story, maturity), evidenced by a ranked comparison report with a stated weighting scheme.
- Judge the lookup-centric bet of Jolt — that Lasso-style lookups can replace most bespoke constraints — demonstrated by a verdict essay that marshals the Lookup Singularity argument for and the overhead evidence against.
- Recommend one zkVM for a specified RISC-V workload, with mastery shown by a defense that traces the recommendation through all seven layers rather than citing benchmarks alone.
- Formulate a benchmark protocol that would fairly compare two zkVMs with different proof systems, evidenced by a written protocol controlling for hardware, field size, and recursion depth.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to analyze the zkVM as a trust wholesaler: developers stop trusting a bespoke hand-built circuit and instead trust one VM constraint system covering an entire instruction set — a single enormous audit capex amortized across every program ever proven, against the retail model of per-application circuit trust.
- Students must be able to argue the governance meaning of the RISC-V convergence (Jolt, SP1 Hypercube, RISC Zero, Airbender, ZisK, Pico Prism): adopting an open external ISA standard imports a neutral standards body into the trust graph and reduces dependence on any single vendor's proprietary stage — then weigh that against the performance case for ZK-native designs.
- Students must be able to critique the zkVM benchmark race as marketing in a market that does not price security: speed is measurable and advertised, soundness of a sprawling constraint system is neither — so a rational buyer must weight audit history and bug-bounty economics above cycle counts, and students should say why the market currently does the opposite.
- Students must be able to connect the universal stage back to Layer 3 economics: whoever operates the zkVM prover sees the full execution, so the proving-as-a-service concentration problem arrives here at industrial scale — analyze the operators' incentives and what contestability would discipline them.

---

# Chapter 12: Midnight -- The Privacy Theater

### Prof. Elena Vasquez — Theoretical Cryptographer
- Read this chapter under an explicit conflict-of-interest discount — the digest itself records that the author founded IOG, the company behind Midnight (deg 13), and designed the chapter around that flagged bias: for each architectural claim, classify it as independently checkable (code, papers, on-chain behavior) or insider assertion, and weight accordingly.
- Define the Nullifier mechanism formally: a deterministic, key-derived tag whose revelation prevents double-spending without linking to the note — state the two games (double-spend soundness, unlinkability) and prove which one fails if nullifier derivation is malleable or non-deterministic.
- Specify what Zswap adds over a Zerocash-style shielded transfer — atomic multi-asset private swaps — and state the additional binding property the swap must satisfy that a single-asset pool never needed.
- Use Midnight as the seven-layer integration exam: instantiate every layer from earlier chapters (Compact and the disclose() Boundary at Layer 2, ZKIR's 24 opcodes at Layer 4) and identify which layer carries the system's weakest assumption.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Walk one shielded transaction through all seven layers of a shipping system — Compact source, disclose() boundary, witness on the client, ZKIR arithmetization, proof, primitives, on-chain verdict — as the payoff exercise for the entire book. Builds on Chapter 10's synthesis: students annotate each step with which of the three paths Midnight chose and which DAG edges forced the choice.
- Stuck-point: students must be able to articulate why a nullifier is NOT a pointer to the note it spends. It must be deterministic (so the same note can never be spent twice) yet unlinkable (so observers cannot connect spend to creation) — and the tension between those two demands is the entire design. Builds on Chapter 7's collision-resistant hashes and Chapter 1's soundness: double-spend prevention is soundness wearing a privacy costume.
- Own Zswap's atomic private swap as Kachina's "privacy as a parameter" made concrete: two parties exchange assets with neither the amounts nor the counterparties public, yet the contract still enforces atomicity. Builds on Chapter 9's Kachina — Midnight's contract model is its direct descendant.
- Practice reading a biased source: the author founded IOG, flags the conflict, and structures the chapter's claims to be independently checkable — students should verify one claim against the graph's external references before accepting it. Builds on Chapter 1's trust-minimization ethos, applied to authors: decompose "trust the book" into named, testable claims too.

### Priya Raghavan — Staff ZK Systems Engineer
- Trace one shielded Zswap transaction end-to-end through the stack you now know layer by layer: Compact source, the disclose() boundary, witness, commitment in, Nullifier out, Merkle root update — and state precisely which component prevents double-spends and which prevents linkability.
- Break the nullifier on paper: design two flawed nullifier derivations (one that lets you double-spend, one that links a user's transactions) and explain which layer of the seven each bug lives in — nullifier bugs are the shielded-pool equivalent of the underconstrained circuits from Chapter 3.
- Apply the author's own bias disclosure as an exercise: the digest notes the author founded IOG, the company behind Midnight, and flagged it — so pick two architectural claims from this chapter and verify them against non-IOG primary sources (the Zswap paper, the deployed testnet, independent audits). Treat founder-written case studies the way you treat vendor benchmarks.
- Map Midnight's full stack onto the seven layers — Compact at layer 2, ZKIR's 24 opcodes at layer 4, and verify against primary sources which proof system and curve sit at layers 5-6 — producing the same ls-listing-style decomposition you built for SP1 in Chapter 1, now for a privacy-first chain.

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Evaluate Midnight's full stack layer by layer against the seven-layer model, evidenced by a completed audit table assigning each of Midnight's choices (Compact, ZKIR, Zswap) to its layer and rating the trust assumption incurred there.
- Judge whether Zswap's nullifier mechanism prevents double-spending without creating linkability, demonstrated by a written verdict that traces one shielded transaction through commitment, spend, and nullifier revelation.
- Critique the author's disclosed conflict of interest — having founded IOG, the company behind Midnight — with mastery shown by an appraisal that lists which of the chapter's claims are independently verifiable and which require outside audit.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to treat the author's disclosed conflict — he founded IOG, the company that built Midnight — as a live exercise in the book's own epistemology: partition the chapter's claims into those independently verifiable from public artifacts and those resting on the author's word, and state what verification each class deserves.
- Students must be able to analyze the nullifier as an institution of permanent memory: double-spends are prevented without revealing the spend graph only because the ledger is trusted to remember every nullifier forever — an ever-growing state liability whose storage cost and integrity someone must underwrite indefinitely.
- Students must be able to read Zswap as a market-design choice: atomic private swaps determine who can see, front-run, or censor an exchange — identify which intermediary's informational advantage is being abolished and what the honest liquidity provider pays for that abolition.
- Students must be able to conduct a full seven-layer trust audit of Midnight as deployed — Compact's disclose() boundary at the language layer, ZKIR's 24-opcode surface at arithmetization, the three-token model's incentive plumbing at the verdict layer — and produce the ledger the book demands: for each layer, who is trusted, why they comply, and what replacing them would cost.

---

# Chapter 13: The Market Landscape

### Prof. Elena Vasquez — Theoretical Cryptographer
- Define a ZK Rollup (deg 10) exactly: validity proofs attest state-transition correctness, and nothing more — enumerate what remains outside the theorem (Data Availability, upgrade governance, sequencer liveness) using Chapter 8's machinery, for Starknet and ZKsync Era concretely.
- Formalize the trust that Proving-as-a-Service reintroduces: the delegated prover holds the witness, so zero-knowledge against that prover is definitionally void — connect this to Chapter 4's Privacy as a Luxury Good and state what (TEEs, MPC-assisted proving) would restore, under which added assumptions.
- State what ZKML (Provable Machine Learning) actually proves — correct inference under a *committed* model — and enumerate what it does not: training integrity, model quality, or that the committed model is the one advertised. Market prose routinely elides all three; a student must not.
- Write ZK Identity / Selective Disclosure as a predicate proof over a signed credential and check the construction against Chapter 9's eIDAS 2.0 requirements: which disclosures are provably minimal, and which merely policy-minimal.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Own the mapping from products to layers: a ZK rollup is Layers 5-7 industrialized, a ZK coprocessor rents you Layer 5 for one query, ZK identity is Chapter 3's disclose() sold as a product, ZKML is the Overhead Tax dared at scale. Builds on Chapter 10's causal DAG — every market category should be locatable on the map before its logo is memorized.
- Stuck-point: students must be able to articulate why the "ZK" in ZK rollup is NOT about privacy. Rollups like Starknet and ZKsync Era buy succinctness and validity — a fully public ledger whose correctness is proved — and the zero-knowledge property is largely unused; conflating the two is the field's most common outsider error. Builds on Chapter 1's three separate promises: this is the market punishing students who blurred them.
- Own Proving-as-a-Service as the market's answer to Chapter 4's hardware ladder — SHARP and its successors amortize prover cost across users — and name the price: the delegated prover sees your witness, re-centralizing the very trust the stack decomposed. Builds on Chapter 4's "privacy as a luxury good."
- Evaluate ZK Identity and selective disclosure against Chapter 9's regulatory pull: eIDAS 2.0 is creating the first mass-market demand for the zero-knowledge property itself, rather than for succinctness. Builds on Chapter 9's eIDAS and GDPR framing.

### Priya Raghavan — Staff ZK Systems Engineer
- Build the Proving-as-a-Service cost model: from your Chapter 11 benchmarks, compute GPU-hours per proof, price it at cloud rates, and determine the volume threshold where running your own prover cluster beats outsourcing — including the availability question: what happens to your rollup when the proving service has an outage at 3am.
- Compare Starknet and ZKsync Era layer-by-layer using the seven-layer frame: Cairo-native ISA vs EVM-compatibility, their provers, their fields, their on-chain verification costs — and explain why the graph puts them in different communities (ZKsync Era clusters with zkVMs & small fields; Starknet doesn't).
- Prototype or paper-design one ZK Coprocessor query (prove a historical storage slot to a contract) and one ZK Identity selective disclosure flow, and for each, identify the layer where the trust actually concentrates — the indexer, the issuer — because the market pitch always hides one.
- Stress-test the ZKML pitch with numbers: find the current cost of proving one inference of a small model, extrapolate to a production-sized model, and write the two-paragraph verdict on which ZKML use cases clear economic viability in 2026 and which are a decade of overhead-tax reduction away.

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Evaluate the maturity of the ZK Rollup segment against the emerging segments (ZK identity, ZK coprocessors, ZKML), evidenced by a market memo that grades each on a stated adoption-versus-hype rubric.
- Judge the Proving-as-a-Service model against the book's Privacy-as-a-Luxury-Good thesis, demonstrated by a verdict on whether delegated proving rescues or forfeits the privacy promise, with the trust cost named explicitly.
- Construct a market map that places Starknet, ZKsync Era, proving services, coprocessors, and ZKML ventures at the seven-layer positions where they compete, evidenced by an original diagram a reader could use to locate a new entrant.
- Formulate an adoption thesis predicting which segment reaches product-market fit first, with mastery shown by a written argument grounded in at least two layer-level constraints from earlier chapters.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to work the ZK Rollup income statement: proofs convert expensive L1 re-execution into concentrated L2 prover cost, sequencer and prover operators capture the margin — and identify the residual trust the marketing omits (upgrade keys, sequencer censorship, forced-exit friction) using Starknet and ZKsync Era against the L2Beat staging lens.
- Students must be able to analyze Proving-as-a-Service as a re-centralization dynamic: hardware economies of scale push proving toward a few industrial operators, reconstituting the very concentrated trust ZK was sold to dissolve — then argue which forces (open zkVMs, portable proofs, exit costs) keep that market contestable.
- Students must be able to evaluate ZK Identity and selective disclosure as a regulation-driven demand market (the eIDAS 2.0 backdrop): the trusted parties become credential issuers and wallet vendors, and students should argue what the citizen gains against advertising platforms versus what new leverage accrues to the issuing state.
- Students must be able to state precisely what a ZKML proof warrants and what it does not: verifiable inference moves trust off the model operator's honesty, but the weights, training data, and their provenance remain unproven inputs — so argue what a buyer of "provable machine learning" is actually purchasing, and what a ZK Coprocessor's proof of historical state does and does not attest.

---

# Chapter 14: Open Questions and the Road Ahead

### Prof. Elena Vasquez — Theoretical Cryptographer
- Classify each of the Seven Open Questions (deg 8) by what resolving it requires: a new theorem under existing assumptions, a new assumption altogether, or engineering under settled theory — the three are not equally hard and must not be presented as if they were.
- Map the Three Frontiers (Performance/Security/Privacy) onto the seven layers: state, for each frontier, which layer's assumption it stresses, and prove the book's implicit inequality — performance gains that shrink soundness margins are not gains, they are relocated risk.
- Produce one original open problem in the discipline this book should have taught: a precise adversary, a winning condition stated as a game, the assumption a solution would rest on, and the layer of the decomposition it would strengthen. If it cannot be stated as a game, it is not yet a question.

### Dr. Sam Okafor — Mathematics Educator (Sanderson/Tao tradition)
- Own the Three Frontiers (performance, security, privacy) as a tension triangle, not a to-do list: pushing one corner strains the others, and students should place one concrete artifact from earlier chapters at each corner — the Overhead Tax (Chapter 5), under-constrained circuits (Chapter 3), and prover side channels (Chapter 4). Builds on all three of those chapters at once; the triangle is the book's failures reorganized.
- Map the Seven Open Questions onto the seven layers: each open question is a layer's weakest assumption stated as a research problem, so the trust decomposition doubles as a research agenda. Builds on Chapter 10's Trust Decomposition — the weakest-link audit, now pointed at the future.
- Stuck-point: students must be able to articulate why an open question is NOT a missing feature. "Detect all under-constrained circuits" fights undecidability, "post-quantum succinctness with algebraic structure" fights Chapter 7's trilemma, while "cheaper client-side proving" is engineering and economics — students must sort "not yet built" from "not yet known to be possible." Builds on Chapter 7's Cryptographic Primitives Trilemma and Chapter 3's under-constrained circuit problem.
- Leave with the transferable skill: given any new proving system announced after this book, locate it on the Seven-Layer Causal DAG, name the assumptions it strengthens and weakens, and identify which of the Three Frontiers it moved. Builds on Chapter 10's DAG — the map was the point all along.

### Priya Raghavan — Staff ZK Systems Engineer
- Map the Seven Open Questions onto the seven layers and the Three Frontiers (Performance/Security/Privacy), then pick the one nearest your own work and design a falsifiable experiment for it — with the metric, the hardware, and the number that would count as an answer.
- Write the on-call runbook for a production proving stack as a capstone: for each of the seven layers, one failure mode from this book (ceremony compromise, underconstrained circuit, witness OOM, Frozen Heart transcript bug, DA saturation...), its detection signal, and its mitigation — the seven-layer model as an alerting taxonomy, because that is what it's actually for.
- Take one frontier claim from the current literature — a real-time proving benchmark, a post-quantum folding scheme's prover cost, a new lattice commitment's proof size — and reproduce or independently verify it against primary sources and your own hardware, then write up where the claim held, where it bent, and what you'd bet production on.

### Dr. Marisol Chen — Curriculum & Assessment Designer
- Design a research proposal targeting one of the Seven Open Questions, evidenced by a one-page proposal stating the question, the layer it lives in, a method, and a measurable success criterion.
- Hypothesize how resolving one chosen open question would propagate through the Seven-Layer Causal DAG, demonstrated by an original cascade diagram predicting which layers' trust assumptions weaken and which are untouched.
- Compose a prioritized three-year roadmap across the Three Frontiers (performance, security, privacy), with mastery shown by a written plan that defends its ordering against the strongest objection from a competing frontier.
- Produce an original seven-layer trust decomposition of a system outside zero-knowledge proofs (for example, a certificate authority or a voting system), evidenced by a decomposition that names seven independent, testable assumptions in the style of the book's thesis.

### Prof. David Lindqvist — Political Economist of Trust
- Students must be able to reframe the Seven Open Questions as unassigned trust liabilities: for each, name who currently bears the unresolved risk by default (usually end users) and which institution — market, standards body, protocol foundation, academy — has both the incentive and the authority to close it.
- Students must be able to analyze the Three Frontiers (Performance/Security/Privacy) as a misaligned investment portfolio: performance gains are privately captured by prover firms while security and privacy are public goods, so predict systematic underinvestment in the latter two and evaluate correction mechanisms of the Ethereum Foundation pivot variety.
- Students must be able to design a migration governance regime for assumption depreciation — the Tower NFS erosion and the quantum deadline being the standing examples: who monitors the health of a deployed assumption, who holds the authority to force a costly migration before failure rather than after, and how the one-way-door cascade constrains the plan.
- As a capstone, students must be able to argue both sides of the book's thesis with incidents as evidence: that decomposing one monolithic trust into seven weaker, replaceable assumptions is a genuine reduction in risk (BGM17, transparent setups, the hybrid pipeline) — and that it can equally be a redistribution that diffuses accountability until no one is answerable when a layer fails (BCTV14, Frozen Heart, Stage 0 rollups).

---
