---
title: "Where the Analogies Break"
slug: ch05-where-the-analogies-break
chapter: 5
chapter_title: "Encoding the Performance"
heading_level: 2
source_lines: [2341, 2408]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 1313
---

## Where the Analogies Break

We promised at the beginning of this chapter to say where the analogies break down.

Arithmetization is the hardest layer to explain because it is the layer where computer science, algebra, and information theory collide in ways that resist simplification. The "spreadsheet with polynomial rules" captures the structure but not the mechanism. The "Sudoku puzzle" captures the constraint-satisfaction flavor but misleads about uniqueness. The "encoding" metaphor captures the transformation but hides the overhead.

What actually happens at Layer 4 is a lossy translation. A computation in the real world involves pointers, variable-length data, exceptions, floating-point approximation, and timing. The arithmetized version strips all of that away and replaces it with fixed-size field elements, fixed-structure polynomial constraints, and deterministic evaluation. The gap between the two -- the "abstraction tax" of 10,000x to 50,000x -- is the price of making computation mathematically verifiable.

Consider what is lost in the translation. A native C program uses 64-bit integers with overflow semantics (values wrap around at $2^{64}$). The arithmetized version uses field elements modulo a prime -- where overflow does not exist, because field arithmetic is always exact. To faithfully represent 64-bit overflow behavior, the constraint system must decompose the values into 64 individual bits, check that each is boolean, compute the sum, and check that only the low 64 bits are retained. The "overflow" that hardware handles in zero cycles costs dozens of constraints. Similarly, a floating-point multiplication that the CPU executes in one cycle using a dedicated FPU requires hundreds of constraints to simulate in field arithmetic -- because there is no floating-point hardware in a finite field, only integers. Every gap between native computation and field arithmetic generates constraints. The overhead is not laziness or bad engineering. It is the cost of bridging two incompatible computational models.

That price is falling. It fell when AIR replaced R1CS for VM-style computations. It fell when PLONKish introduced custom gates. It fell when CCS unified the constraint systems. It fell when LogUp eliminated sorting from lookups. It fell when Lasso made table sizes irrelevant. It fell when small fields replaced 254-bit primes. It falls every time a researcher finds a way to encode more computation in fewer constraints.

But it has not fallen to zero, and it may never fall to zero. Provable computation is inherently more expensive than unprovable computation. The magician who performs backstage with no audience can cut corners. The magician who must produce a sealed certificate -- one that any stranger can verify -- must record every step with mathematical precision. The overhead of arithmetization is the cost of making the performance verifiable.

There is a theoretical lower bound that clarifies the situation. Any computation that produces n bits of output requires at least n bits of communication to verify (you need to at least read the output). The overhead above this information-theoretic minimum comes from the cryptographic machinery: polynomial commitments, random challenge generation, and the proof that the polynomial identities hold. Whether this cryptographic overhead can be reduced to $O(1)$ multiplicative factor remains an open question. The current answer is: not yet, but the constant factor is shrinking every year.

The honest summary of Layer 4 in 2026: arithmetization is hard, expensive, and getting better fast. The constraint systems are converging toward CCS. The lookup revolution is replacing hand-crafted constraints with table lookups. The overhead is falling from 10,000x toward 1,000x and below. And the sumcheck protocol -- invented in 1992, long before anyone imagined practical zero-knowledge proofs -- has become the universal verification engine that makes it all work.

From this point forward, the magician-and-audience framing will recede. Layers 5, 6, and 7 operate at a level of abstraction where the metaphor obscures more than it reveals. The sealed certificate, the deep craft, the verdict -- these section titles keep the theatrical frame alive as a mnemonic, but the explanations will be increasingly technical. We will still speak of provers and verifiers, because those are the real actors, but the stage curtains come down here. When the metaphor returns in full force, it will be in Chapter 12, where Midnight provides a concrete theater that makes the abstraction physical again.

---

*The computation is encoded as mathematics. Every instruction, every memory access, every comparison has been transformed into polynomial equations over a finite field. The equations are organized -- as R1CS, as AIR, as PLONKish, or as CCS -- and the lookup arguments have replaced the most expensive operations with table references. The sumcheck protocol stands ready to verify that the equations hold, without checking every cell in the spreadsheet.*

*The constraint system is the scorecard. But a scorecard means nothing until someone seals it into a certificate that cannot be tampered with. The next chapter enters the proof system -- the cryptographic mechanism that seals the certificate.*

---

### Reference Data

- **R1CS** (2012): bilinear constraints (degree 2). One constraint per multiplication gate. Native format for Groth16 (128-byte proofs, constant-time verification) and Spartan.
- **AIR** (2018): uniform transition constraints over execution traces. Native format for STARKs (transparent, post-quantum). Constraint description size independent of trace length.
- **PLONKish** (2019): selector-gated custom gates with copy constraints via permutation arguments. Native format for Halo2, PLONK. Dominant in deployed systems (2020-2025).
- **CCS** (Setty, 2023): unifies R1CS, AIR, and PLONKish without overhead. Native target for HyperNova, Neo, ProtoStar, ProtoGalaxy.
- **Sumcheck protocol** (Lund et al., 1992): reduces verification of polynomial sums over $2^n$ inputs to $n$ rounds of interaction. Backbone of Spartan, HyperNova, Jolt, and SP1 Hypercube.
- **Plookup** (2020): first practical lookup argument. Sorting-based, $O(n \log n)$.
- **LogUp** (2022): sorting-free lookup via logarithmic derivatives. $O(n)$ prover cost.
- **LogUp-GKR** (2023): logarithmic verifier cost for lookups. Used in SP1 Hypercube and Stwo.
- **Lasso** (2023): lookups into tables of size $2^{128}$, prover cost independent of table size.
- **Jolt** (2023): approximately 6x faster than RISC Zero in theoretical commitment cost analysis. Full RISC-V ISA via lookups.
- **Overhead tax**: 10,000-50,000x versus native execution (2024-2025 systems). Falling to 1,000-5,000x by 2027-2028.
- **Overhead breakdown**: field encoding (10-100x), constraint expansion (50-100x), polynomial commitment (10-50x). Sources multiply.
- **Ozdemir et al.**: 50-150x reduction in memory checking constraints via algebraic approaches.
- **Binius** (2025): 100x reduction in bit-level embedding overhead via binary tower fields.
- **Mersenne-31**: field modulus $2^{31} - 1$. Fastest known modular reduction. Used by SP1 and Stwo.
- **ZKIR**: 24 typed instructions, compiling Compact to PLONKish constraints over BLS12-381 ($\sim 2^{253}$).

### Sources

- [R-L4-1] Gennaro, Gentry, Parno, Raykova. "Quadratic Span Programs and Succinct NIZKs without PCPs." EUROCRYPT 2013. ePrint 2012/215.
- [R-L4-2] Ben-Sasson, Bentov, Horesh, Riabzev. "Scalable, Transparent, and Post-Quantum Secure Computational Integrity." ePrint 2018/046.
- [R-L4-3] Gabizon, Williamson, Ciobotaru. "PLONK." ePrint 2019/953.
- [R-L4-4] Setty, Thaler, Wahby. "Customizable Constraint Systems for Succinct Arguments." ePrint 2023/552.
- [R-L4-5] Setty. "Spartan: Efficient and General-Purpose zkSNARKs without Trusted Setup." ePrint 2019/550.
- [R-L4-6] Gabizon, Williamson. "Plookup." ePrint 2020/315.
- [R-L4-7] Haboeck. "LogUp." ePrint 2022/1530.
- [R-L4-8] Papini, Shahar and Ulrich Haboeck. "LogUp-GKR." ePrint 2023/1284.
- [R-L4-9] Setty, Thaler, Wahby. "Lasso." ePrint 2023/1216.
- [R-L4-10] Arun, Setty, Thaler. "Jolt." ePrint 2023/1217.
- Midnight ZKIR Reference (v2/v3), 119 oracle traces. Compact compiler v0.29.0.
- Lund, Fortnow, Karloff, Nisan. "Algebraic Methods for Interactive Proof Systems." JCSS 1992.


---

*A note on the next three chapters.* Chapters 5, 6, and 7 cover arithmetization, proof systems, and cryptographic primitives -- what this book calls the "proof core." In practice, these three layers are inseparable: the choice of field (Layer 6) determines which arithmetization works (Layer 4), which determines which proof system is viable (Layer 5). We present them sequentially because a book must be linear, but they are best understood as a single coupled design unit. If a choice in Chapter 7 seems to contradict a claim in Chapter 5, it is because the dependency runs in both directions. Read all three, then revisit.

---

## Summary

Layer 4 is a lossy translation: native computation (64-bit integers, floats, pointers, exceptions) becomes fixed-size field elements and deterministic polynomial constraints, and the gap costs 10,000–50,000x overhead. The overhead is falling — CCS, LogUp, Lasso, small fields, and Binius each reduced one component — but a theoretical lower bound remains: provable computation is inherently more expensive than unprovable computation.

## Key claims

- Native 64-bit overflow wrapping costs ~dozens of polynomial constraints (bit decomposition, boolean checks, reconstruction) vs. zero CPU cycles.
- Each gap between native and field computation generates constraints; the overhead is structurally necessary, not a design flaw.
- Current trajectory: 10,000–50,000x (2024–2025) → 1,000–5,000x (2027–2028) for general-purpose zkVMs.
- Overhead milestones: AIR replaced R1CS for VMs; PLONKish added custom gates; CCS unified formats; LogUp eliminated sorting; Lasso made table size irrelevant; small fields gave ~100x per-op savings.
- Binius (2025): 100x reduction for bit-heavy workloads by working natively in binary tower fields.
- Mersenne-31 modular reduction: two shifts and two additions — faster than any other prime reduction.
- An information-theoretic lower bound exists: $n$ bits of output requires $\Omega(n)$ communication. Whether the cryptographic overhead can approach $O(1)$ multiplicative factor is open.

## Entities

- [[arithmetization]]
- [[bls12-381]]
- [[groth16]]
- [[halo2]]
- [[hypernova]]
- [[jolt]]
- [[lasso]]
- [[logup]]
- [[mersenne]]
- [[midnight]]
- [[nova]]
- [[plonk]]
- [[spartan]]
- [[starks]]

## Dependencies

- [[ch05-the-overhead-tax-10-000x-to-50-000x]] — quantitative overhead analysis this section synthesizes
- [[ch05-the-constraint-system-evolution-r1cs-air-plonkish]] — each system improved the overhead at some dimension
- [[ch05-ccs-the-rosetta-stone]] — CCS is one of the "it fell when" milestones
- [[ch05-lookup-arguments]] — LogUp and Lasso are the other milestones
- [[ch05-where-the-layers-collapse]] — the proof-core coupling is the architectural punchline

## Sources cited

- [R-L4-1] Gennaro, Gentry, Parno, Raykova. "Quadratic Span Programs and Succinct NIZKs without PCPs." EUROCRYPT 2013.
- [R-L4-2] Ben-Sasson, Bentov, Horesh, Riabzev. ePrint 2018/046.
- [R-L4-3] Gabizon, Williamson, Ciobotaru. "PLONK." ePrint 2019/953.
- [R-L4-4] Setty, Thaler, Wahby. "CCS." ePrint 2023/552.
- [R-L4-5] Setty. "Spartan." ePrint 2019/550.
- [R-L4-6] Gabizon, Williamson. "Plookup." ePrint 2020/315.
- [R-L4-7] Haboeck. "LogUp." ePrint 2022/1530.
- [R-L4-8] Papini, Haboeck. "LogUp-GKR." ePrint 2023/1284.
- [R-L4-9] Setty, Thaler, Wahby. "Lasso." ePrint 2023/1216.
- [R-L4-10] Arun, Setty, Thaler. "Jolt." ePrint 2023/1217.
- Lund, Fortnow, Karloff, Nisan. "Algebraic Methods for Interactive Proof Systems." JCSS 1992.
- Midnight ZKIR Reference (v2/v3). Compact compiler v0.29.0.

## Open questions

None flagged by this section.

## Improvement notes

## Links

- Up: [[05-encoding-the-performance]]
- Prev: [[ch05-where-the-layers-collapse]]
- Next: —
