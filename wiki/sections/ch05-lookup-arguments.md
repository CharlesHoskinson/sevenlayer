---
title: "Lookup Arguments"
slug: ch05-lookup-arguments
chapter: 5
chapter_title: "Encoding the Performance"
heading_level: 2
source_lines: [1989, 2114]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 3722
---

## Lookup Arguments

In the classical approach to arithmetization, every operation in a computation is encoded as polynomial constraints. Addition and multiplication are natural: they are already arithmetic operations over the field. But what about operations that are *not* naturally arithmetic?

Consider the problem from the perspective of a circuit designer building a zkVM. The RISC-V instruction set contains 47 base instructions. Of these, roughly half are "arithmetic-friendly" -- ADD, SUB, MUL, and their variants map naturally to field operations. But the other half are "arithmetic-hostile": AND, OR, XOR, SLL (shift left logical), SRL (shift right logical), SLT (set less than), BEQ (branch if equal), and the memory load/store operations. Each of these requires bitwise decomposition or comparison logic that does not map neatly to field arithmetic.

Bitwise AND, comparison, range checks, hash functions -- these require decomposing the values into individual bits, constraining each bit to be 0 or 1, and then reconstructing the result. A single SHA-256 hash invocation can require tens of thousands of constraints.

The cost is staggering when you trace through a concrete example. Consider XOR -- the bitwise exclusive-or of two 8-bit numbers. On a CPU, this is one instruction, one clock cycle, done. In a polynomial constraint system, you must first decompose each 8-bit input into 8 individual bits (8 range-check constraints per input, 16 total), then constrain each output bit to be the XOR of the corresponding input bits (each bit-level XOR requires the polynomial $a + b - 2ab$, which is a degree-$2$ constraint, so 8 more constraints), and finally reconstruct the output from its bits (8 more constraints). That is roughly 32 constraints for an operation that takes a single machine cycle. SHA-256 calls XOR, AND, NOT, and rotation thousands of times. Multiply 32 constraints per operation by thousands of operations and you arrive at the tens of thousands of constraints that a single hash invocation demands.

This is not a fixable inefficiency in the constraint system design. It is a fundamental mismatch between the polynomial language (which speaks addition and multiplication over large fields) and the bitwise language (which speaks AND, OR, XOR over individual bits). No amount of cleverness in the constraint layout will make polynomials natively express bit manipulation. The operations live in different algebraic worlds.

The mismatch created a two-tier cost structure in early ZK systems. "Arithmetic-friendly" operations (Poseidon hash, MiMC, elliptic curve arithmetic) -- operations designed from the ground up to minimize constraint count -- were cheap. "Arithmetic-hostile" operations (SHA-256, Keccak, AES, bitwise logic) -- operations from the traditional computing world -- were expensive by comparison. This is why the ZK community designed entirely new hash functions (Poseidon, Rescue, Neptune) that use only field additions and multiplications, avoiding bitwise operations entirely. A Poseidon hash costs roughly 300 constraints in R1CS. A SHA-256 hash costs roughly 25,000 constraints. Same security level. Hundred-fold difference in proving cost. The constraint system penalizes any computation that crosses the boundary between field arithmetic and bit arithmetic.

Lookup arguments offer a fundamentally different approach: instead of encoding the operation as constraints, you look up the answer in a pre-computed table. Instead of proving *how* you computed XOR, you prove *that* your answer appears in a table of all correct XOR results. The philosophical shift is from verification-by-recomputation to verification-by-membership.

### Plookup: The First Practical Lookup (2020)

Gabizon and Williamson introduced Plookup in 2020. The idea: if you have a table of pre-approved input-output pairs (for example, all possible 8-bit XOR results), you can prove that a set of values appears in the table without recomputing the operation.

Consider that table of 8-bit XOR results. It has 256 * 256 = 65,536 entries, each of the form (a, b, a XOR b). If the prover claims that 0x3F XOR 0xA7 = 0x98, the verifier does not check the XOR. Instead, the verifier checks that the triple (0x3F, 0xA7, 0x98) appears somewhere in the table. If it does, the answer is correct -- because the table was constructed correctly, and membership in a correct table implies correctness of the result.

Plookup works by sorting the lookup values and the table entries into a single sorted sequence, then verifying the sorting through a grand product argument. If every lookup value appears in the table, the sorted sequence has a specific structure that the grand product captures. The prover merges the table and the lookup values into one sorted list, then proves that the merged list is a valid interleaving of the original table with the queried entries. A polynomial identity -- checked via a grand product over the entire sorted sequence -- catches any entry that does not belong.

The catch: sorting costs $O(n \log n)$, and the grand product requires committing to the sorted sequence. For a circuit with $n$ lookups into a table of size $T$, the prover must commit to a sorted list of length $n + T$. This makes Plookup a meaningful optimization for expensive operations (hashes, range checks) but not a universal solution. The sorting overhead is the bottleneck, and it resists parallelization -- you cannot sort half a list on one machine and half on another without a merge step.

Despite its limitations, Plookup was immediately adopted. Lookup arguments for range checks (proving a value is between $0$ and $2^N$) replaced the naive approach of decomposing into N bits and constraining each one. For a 16-bit range check, the naive approach requires 16 boolean constraints plus a reconstruction constraint (17 total). A Plookup-based range check requires one lookup into a table of 65,536 entries. The lookup is more expensive in absolute prover time (sorting overhead), but far cheaper in constraint count -- and for systems where constraint count is the bottleneck, this tradeoff is worthwhile. By 2021, every major PLONKish system used lookup arguments for range checks.

### LogUp: The Sorting-Free Revolution (2022)

Ulrich Haboeck's LogUp paper in 2022 replaced Plookup's sorting with an observation that is, in retrospect, elegant to the point of inevitability. The name "LogUp" comes from "logarithmic derivative" -- the key mathematical technique. If you have a polynomial P(X) = Product of (X - r_i) whose roots are exactly the lookup values, then the logarithmic derivative of P is P'(X)/P(X) = Sum of 1/(X - r_i). This transforms a product (which is hard to check incrementally) into a sum (which is easy to accumulate and verify). The idea comes from complex analysis, where logarithmic derivatives convert multiplicative structures into additive ones. Haboeck's insight was to apply this classical technique to the lookup problem.

Instead of sorting, LogUp observes that if every lookup value $f_i$ appears in the table $t$, then a specific identity over rational functions must hold:

$\sum_i \frac{1}{X - f_i} = \sum_j \frac{m_j}{X - t_j}$

where $m_j$ counts how many times table entry $t_j$ is looked up. The left side sums one term per lookup. The right side sums one term per table entry, weighted by the number of times it was accessed. If every lookup value is in the table, these two sums are equal as formal rational functions -- and therefore they are equal at a random evaluation point with overwhelming probability.

A tiny example makes this concrete. Suppose the table contains {1, 2, 3} and the prover claims to look up the values {2, 3, 2}. The left side (one term per lookup) is: $1/(X-2) + 1/(X-3) + 1/(X-2) = 2/(X-2) + 1/(X-3)$. The right side (one term per table entry, weighted by frequency) is: $0/(X-1) + 2/(X-2) + 1/(X-3)$ -- because entry 1 is looked up 0 times, entry 2 is looked up twice, and entry 3 is looked up once. Both sides equal $2/(X-2) + 1/(X-3)$. The identity holds. Now suppose the prover cheats and claims to look up {2, 3, 5}, where 5 is not in the table. The left side becomes $1/(X-2) + 1/(X-3) + 1/(X-5)$. No assignment of multiplicities to the table entries {1, 2, 3} can produce a term $1/(X-5)$ on the right side. The identity fails at a random evaluation point with overwhelming probability.

This transforms the lookup argument from a product check to a *sum check* -- and sums, unlike products, compose beautifully. Why does this matter? Because a product of n terms can be thrown off by a single corrupted factor (the product becomes wrong, but localizing the error requires inspecting every factor). A sum of n terms, by contrast, is naturally decomposable: you can split the sum into batches, compute partial sums independently, and aggregate them. The algebraic structure of addition is friendlier than the algebraic structure of multiplication.

The advantages are substantial:

- **No sorting required.** Eliminates the $O(n \log n)$ overhead entirely. The prover's cost drops to $O(n + T)$, linear in the number of lookups plus the table size.
- **Natural batching.** Multiple lookup tables can be handled simultaneously via random linear combinations. If your circuit uses a XOR table, an AND table, and a range-check table, LogUp handles all three in one pass.
- **Parallelizable.** The summation structure means partial lookups can be computed independently on separate machines and aggregated with a single addition. This is exactly the property that GPU-based provers exploit.
- **Sumcheck-compatible.** The rational function identity can be verified using the sumcheck protocol, connecting lookups directly to the same verification backbone that handles constraint checking.

LogUp became the production standard. It replaced Plookup in deployed systems and enabled the next generation of lookup-based architectures. The transition was rapid: by 2024, virtually every new proof system design used LogUp or a LogUp variant for its lookup needs.

### LogUp-GKR: The Verifier Gets Faster (2023)

LogUp made the prover efficient. But the verifier still had to check the rational function identity, which naively requires work proportional to the number of lookups. Papini and Haboeck combined LogUp with the GKR interactive proof protocol to solve this.

The GKR protocol provides an efficient way to verify layered arithmetic circuits -- circuits where the computation flows through layers, each layer depending only on the one before it. The fractional sum computation in LogUp (adding up all the 1/(X - f_i) terms) has exactly this layered structure: it is a sum reduction tree. LogUp-GKR applies the GKR protocol to this tree, reducing the verifier's work from linear to logarithmic in the number of lookups.

The result: logarithmic proof size and verification time for lookup arguments. The verifier does $O(\log n)$ work regardless of how many lookups the prover performed.

LogUp-GKR is now used in Polygon's Plonky3 framework and in SP1 Hypercube. It makes lookups nearly free for the verifier, which is critical for recursive proof composition -- where the verifier's circuit size directly affects the cost of the next recursion step. If verifying a lookup takes $O(n)$ work, then a recursive verifier circuit must be $O(n)$ in size, which is expensive to prove in the next recursion layer. With LogUp-GKR, the recursive verifier circuit is $O(\log n)$, making deep recursion practical.

The combination of LogUp (efficient prover) and GKR (efficient verifier) made lookups a first-class operation in the proof system -- no longer an optimization to be applied selectively, but a general-purpose tool to be used wherever a pre-computed table exists. This set the stage for the two results that completed the lookup revolution: Lasso, which made table size irrelevant, and Jolt, which made lookups the only computation paradigm needed.

### Lasso: The Table Size Disappears (2023)

The fundamental limitation of both Plookup and LogUp is that the prover must somehow touch the entire table. For a table of $2^{16}$ entries (65,536 rows), this is manageable. For a table of all possible 64-bit operations -- $2^{128}$ entries -- it is physically impossible to even store the table, let alone commit to it. The table of all 64-bit additions alone has $2^{128}$ rows. At one byte per row, that is $10^{38}$ bytes -- more than the number of atoms in the observable universe. No amount of hardware solves this.

Lasso, by Setty, Thaler, and Wahby (2023), solves this through *decomposition*. The insight is that most useful tables have internal structure that can be exploited. Specifically, if the table's multilinear extension (MLE) can be evaluated efficiently -- meaning you can compute the table's value at any point without materializing the entire table -- then each lookup can be decomposed into lookups into much smaller subtables.

The intuition is best seen through an analogy. Suppose you have a multiplication table for two-digit numbers. Instead of storing all 90 * 90 = 8,100 entries (for digits 10-99), you could decompose each two-digit number into its tens and units digits, store separate multiplication tables for single digits (only 10 * 10 = 100 entries each), and reconstruct the full product from partial products. The full table has 8,100 entries; the subtables have a combined 200 entries. You traded one large lookup for several small lookups plus some arithmetic glue. Lasso does exactly this, but for arbitrary structured tables over finite fields, using the multilinear extension as the decomposition mechanism.

For a table of size $2^{2W}$, Lasso decomposes each lookup index into $c$ chunks. Instead of one lookup into a table of size $2^{2W}$, the prover performs $c$ lookups into subtables of size $2^{2W/c}$. For 64-bit RISC-V operations with $c = 6$, each subtable has roughly $2^{22}$ entries -- about 4 million rows. That fits comfortably in memory.

The prover's cost becomes $O(n \cdot c \cdot \log(N)/c)$, which is proportional to the number of lookups (n) and the number of chunks (c), but *independent of the table size* (N). You can look up values in a table of $2^{128}$ entries without ever materializing the table. The table exists as a mathematical function -- its MLE -- not as a stored data structure. The prover only pays for the subtable entries it actually accesses.

This is the kind of result that reshapes what is considered possible. Before Lasso, "table size" was a hard constraint on lookup arguments. After Lasso, table size is irrelevant -- only table structure matters. A structured table of $2^{128}$ entries is no harder to use than a structured table of $2^{16}$ entries. The prover's work scales with the number of lookups it performs, not with the number of entries it could theoretically look up.

### Jolt: The Lookup Singularity Realized (2023)

Arun, Setty, and Thaler's Jolt paper took Lasso's theoretical framework and applied it to its logical conclusion: what if *every* instruction in a processor were a lookup?

The concept, originally proposed by Barry Whitehat as the "lookup singularity," posits that circuits should be expressed entirely as lookups into pre-computed tables. Jolt demonstrates this is achievable for a complete RISC-V instruction set:

1. Every RISC-V instruction has an evaluation table mapping inputs to outputs.
2. All instruction tables are MLE-structured (their multilinear extensions can be evaluated efficiently).
3. Lasso's decomposition makes these lookups efficient regardless of the theoretical table size.
4. Memory consistency is verified through offline memory checking (fingerprint-based techniques), not Merkle trees.

For each instruction, the prover decomposes the operands into chunks, performs lookups into small subtables (typically around 4 million entries each), and commits to roughly 18 field elements per instruction (3 per chunk, with $c = 6$ chunks).

The memory-checking component (point 4) is worth highlighting separately. In a real processor, memory is read-write: the program loads and stores values freely. Proving that every load returns the value of the most recent store to the same address is the memory consistency problem discussed in the overhead section. Jolt handles this through "offline memory checking" -- a technique where the prover computes a cryptographic fingerprint of the sequence of all reads and writes, and the verifier checks that the fingerprint is consistent with a valid read-write memory. This avoids the per-access cost of Merkle tree proofs and makes memory checking nearly as cheap as instruction checking. The technique is not specific to Jolt; it was developed by Blum et al. in the 1990s and adapted for ZK by Setty (Spartan) and others. But Jolt's integration of offline memory checking with Lasso-based instruction lookups produces a complete zkVM architecture where every component -- instruction verification, memory consistency, program counter management -- is handled by either a lookup or a fingerprint check.

The result is a zkVM where the constraint system is almost entirely lookups, with minimal arithmetic "glue." This is not an optimization applied to an existing constraint system -- it is a different paradigm for encoding computation.

The achievement is striking. A complete RISC-V instruction set -- ADD, SUB, AND, OR, XOR, SLL, SRL, SRA, SLT, SLTU, BEQ, BNE, BLT, BGE, LW, SW, and dozens more -- expressed without writing a single arithmetic constraint by hand. Every instruction is a table lookup. The "constraint system" is a collection of tables plus the Lasso machinery to prove that every instruction's result appears in the correct table. No custom gates. No selector polynomials. No hand-optimized constraint layouts. Just tables.

To see how this works for a specific instruction, trace through a 32-bit ADD. The prover needs to prove that register_a + register_b = register_c. The "addition table" for 32-bit inputs has $2^{64}$ entries -- impossibly large to store. But Lasso decomposes each 32-bit operand into $c = 4$ chunks of 8 bits each. Each chunk lookup goes into a subtable of size $2^{16} = 65{,}536$ entries (all possible 8-bit additions, accounting for carry). The prover performs 4 small lookups instead of one impossible lookup, commits to the chunk values and the carry bits, and uses the Lasso sumcheck machinery to prove that the chunks reconstruct the full addition correctly.

Compare this to how a traditional zkVM would prove the same 32-bit ADD. In RISC Zero's earlier architecture, the prover would encode the addition as a polynomial constraint over the full 32-bit values, with range checks to ensure the operands fit in 32 bits (costing roughly 32 constraints for bit decomposition per operand), a constraint for the addition itself, and further constraints for carry propagation and overflow detection. Roughly 70 to 100 constraints per ADD instruction. In Jolt, the same instruction costs approximately 18 field element commitments (3 per chunk, 6 chunks for 64-bit RISC-V) and a handful of sumcheck rounds. The constraint count per instruction drops by roughly 4x.

This is genuinely surprising. For years, the ZK community assumed that building a practical zkVM required painstaking constraint engineering -- hand-crafting gate designs for each instruction type, optimizing selector layouts, minimizing constraint counts through algebraic tricks. Jolt demonstrates that all of that complexity can be replaced by a single, uniform mechanism: look up the answer. The engineering effort shifts from "design clever constraints" to "design decomposable tables," and the latter turns out to be systematically easier.

### The Genealogy in Full

The progression from auxiliary technique to primary computation paradigm took just three years:

| System | Year | Technique | Sorting? | Table Size Limit | Key Innovation |
|--------|------|-----------|----------|-------------------|----------------|
| Plookup | 2020 | Grand product | Yes ($O(n \log n)$) | Fixed, materializable | First practical lookup |
| LogUp | 2022 | Logarithmic derivatives | No | Fixed, materializable | Sum-based, parallelizable |
| LogUp-GKR | 2023 | LogUp + GKR | No | Fixed, materializable | Logarithmic verifier |
| Lasso | 2023 | Decomposition | No | Unlimited (structured) | Table-size independent |
| Jolt | 2023 | Lasso for full ISA | No | Unlimited (structured) | Lookup singularity realized |

The three-year progression is worth pausing on. In 2020, lookups were an auxiliary optimization -- useful for range checks and hash functions, but secondary to the main constraint system. By 2023, lookups had become a complete computation paradigm -- capable of replacing the constraint system entirely for general-purpose ISA execution. Nothing else in ZK moved this fast.

The industry has not yet fully absorbed this shift. Jolt is in alpha (open-sourced by a16z), with key missing features including full recursion support and GPU-accelerated proving. Production systems in 2026 still largely use LogUp or LogUp-GKR for specific operations (range checks, hash functions) while relying on polynomial constraints for the core computation. But the trajectory is clear: lookups are moving from a useful optimization to the primary computation paradigm.

One qualification is important. The lookup singularity works well for ISA-level computation -- adding two registers, comparing values, shifting bits. For application-specific circuits with rich algebraic structure (elliptic curve operations, pairing computations), direct polynomial constraints remain more efficient. The lookup approach excels for *general-purpose* computation; specialized circuits may still prefer custom constraints.

The lesson of the lookup revolution is about the relationship between computation and verification. The classical approach to ZK asks: "How do I re-express this computation as polynomial constraints?" The lookup approach asks a different question: "How do I prove that the answer is correct, without re-expressing the computation at all?" The table is a certificate of correctness. If the answer is in the table, the answer is correct. The proof reduces to a membership test. This conceptual shift -- from "prove the computation" to "prove membership in a table of correct answers" -- may be the most consequential shift in arithmetization since CCS unified the constraint systems. It is also, notably, the idea that connects most directly to the sumcheck protocol: LogUp's rational function identity is verified by sumcheck, Lasso's decomposition is verified by sumcheck, and Jolt's per-instruction correctness reduces to sumcheck instances. Lookups and sumcheck are two sides of the same coin.

Three advances -- CCS, sumcheck, and lookups -- form a complete verification stack. CCS provides the universal constraint format: any polynomial relation, any degree, any structure, expressed as sums of Hadamard products. Sumcheck provides the universal verification engine: any polynomial sum over an exponential domain, reduced to a single-point check in logarithmic rounds. Lookups replace the most expensive constraint-by-constraint encoding with table references: instead of proving that a value satisfies a complex relation through dozens of polynomial constraints, the prover demonstrates that the value appears in a precomputed table. Together, they answer a question that was open as recently as 2022: can we build a proof system that handles any constraint format, verifies in near-linear time, and avoids the worst overhead of hand-crafted constraint engineering? By 2024, the answer was yes -- and the combination of CCS + sumcheck + lookups is the engine inside every frontier proof system built since.

---


## Summary

Lookup arguments replace constraint-by-constraint polynomial encoding of arithmetic-hostile operations (XOR, range checks, hashes) with membership proofs in precomputed tables. The genealogy runs Plookup (2020, sorting-based) → LogUp (2022, logarithmic-derivative sums) → LogUp-GKR (2023, log-time verifier) → Lasso (2023, table-size-independent) → Jolt (2023, full RISC-V ISA as lookups). By 2024 lookups had shifted from optimization to primary computation paradigm.

## Key claims

- XOR of two 8-bit numbers costs ~32 polynomial constraints but 1 machine cycle; SHA-256 costs ~25,000 constraints vs. ~300 for Poseidon.
- Plookup (Gabizon and Williamson, 2020): grand-product sorting; $O(n \log n)$ prover cost.
- LogUp (Haboeck, 2022): replaces sorting with logarithmic-derivative rational function identity $\sum_i \frac{1}{X-f_i} = \sum_j \frac{m_j}{X-t_j}$; $O(n+T)$ prover, parallelizable.
- LogUp-GKR (Papini and Haboeck, 2023): applies GKR protocol to reduce verifier work to $O(\log n)$; used in Polygon Plonky3 and SP1 Hypercube.
- Lasso (Setty, Thaler, Wahby, 2023): decomposes lookups into $c$ subtable lookups; prover cost independent of table size $N$. Enables $2^{128}$-entry tables.
- Jolt (Arun, Setty, Thaler, 2023): entire RISC-V ISA as Lasso-based lookups; ~18 field element commitments per instruction vs. ~50–80 constraints in traditional zkVMs.
- Offline memory checking (Blum et al., adapted by Setty) handles read-write memory in Jolt without per-access Merkle proofs.

## Entities

- [[fri]]
- [[gabizon]]
- [[jolt]]
- [[lasso]]
- [[logup]]
- [[nova]]
- [[plonk]]
- [[plonky3]]
- [[polygon]]
- [[poseidon]]
- [[setty]]
- [[spartan]]

## Dependencies

- [[ch05-the-sumcheck-protocol-the-hidden-foundation]] — LogUp-GKR, Lasso, and Jolt all verify via sumcheck
- [[ch05-ccs-the-rosetta-stone]] — Lasso and Jolt use CCS as underlying constraint format
- [[ch05-the-overhead-tax-10-000x-to-50-000x]] — lookup-based architectures are one of the overhead reduction strategies
- [[ch05-where-the-layers-collapse]] — Jolt fuses witness generation and arithmetization

## Sources cited

- [R-L4-6] Gabizon, Williamson. "Plookup." ePrint 2020/315.
- [R-L4-7] Haboeck. "LogUp." ePrint 2022/1530.
- [R-L4-8] Papini, Shahar and Ulrich Haboeck. "LogUp-GKR." ePrint 2023/1284.
- [R-L4-9] Setty, Thaler, Wahby. "Lasso." ePrint 2023/1216.
- [R-L4-10] Arun, Setty, Thaler. "Jolt." ePrint 2023/1217.

## Open questions

None flagged by this section.

## Improvement notes

- [P1] (A) Jolt field-element cost stated as "~18 field element commitments per instruction (3 per chunk, with $c = 6$ chunks)" in the body text, but the Key claims state "~18 field element commitments per instruction vs. ~50–80 constraints in traditional zkVMs." The body's ADD example elsewhere says "approximately 18 field elements per instruction (3 per chunk, $c = 6$ chunks for 64-bit RISC-V)" — 3 × 6 = 18 is correct for 64-bit, but the preceding paragraph uses $c = 4$ chunks of 8 bits for a 32-bit ADD (4 chunks × 3 = 12, not 18). The section mixes 32-bit and 64-bit examples without clearly distinguishing them, making the 18-element figure appear inconsistent.
- [P1] (A) Plookup attributed to "Gabizon and Williamson" — the full paper title is "plookup: A simplified polynomial protocol for lookup tables" and includes Zacharias, not just Gabizon and Williamson. Check authorship; the ePrint 2020/315 lists Gabizon and Williamson as sole authors, which is correct for the original Plookup, but LogUp-GKR is attributed to "Papini and Haboeck" while the actual ePrint 2023/1284 authors are Shahar Papini and Ulrich Haboeck — the Key claims entry spells it "Papini, Shahar and Ulrich Haboeck" (correctly) while the Sources section uses "Papini, Shahar and Ulrich Haboeck" — consistent, but the body text just says "Papini and Haboeck" without first names. Minor inconsistency but worth normalizing.
- [P2] (A) "Offline memory checking (Blum et al., adapted by Setty)" — "Blum et al." is attributed to the 1990s but no specific paper is cited. The canonical reference is Blum, Evans, Gemmell, Kannan, Naor, "Checking the Correctness of Memories" (1991). A citation entry should be added.
- [P2] (C) The LogUp section explains logarithmic derivatives via "P'(X)/P(X) = Sum of 1/(X - r_i)" — this is mathematically correct but uses the prime-notation derivative inline before defining it, then switches to a formal display equation. The transition from the inline explanation to the displayed formula is slightly abrupt; a brief "differentiating both sides gives" would smooth it.
- [P3] (E) Jolt's status as "alpha (open-sourced by a16z)" is noted but no mention of the main missing capability for production: lack of proof recursion. This is mentioned in passing but the implications for deployment (e.g., no on-chain verification without recursion) are not elaborated.

## Links

- Up: [[05-encoding-the-performance]]
- Prev: [[ch05-the-sumcheck-protocol-the-hidden-foundation]]
- Next: [[ch05-the-overhead-tax-10-000x-to-50-000x]]
