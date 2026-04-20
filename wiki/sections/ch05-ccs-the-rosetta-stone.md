---
title: "CCS: The Rosetta Stone"
slug: ch05-ccs-the-rosetta-stone
chapter: 5
chapter_title: "Encoding the Performance"
heading_level: 2
source_lines: [1877, 1949]
source_commit: 6e757843ed29aa50ce4558719452a86510ed0d20
status: finalized
word_count: 2077
---

## CCS: The Rosetta Stone

In 2023, Srinath Setty, Justin Thaler, and Riad Wahby published a paper that changed constraint system design. Customizable Constraint Systems (CCS) unified R1CS, AIR, and PLONKish into a single mathematical framework, without overhead [R-L4-4].

The word "without overhead" is the point. Previous attempts at unification existed -- for example, you can always convert AIR to R1CS by expanding every transition into individual constraints, or convert R1CS to AIR by padding with identity transitions. But these conversions incur blowup: the converted instance is larger, sometimes much larger, than the original. CCS achieves something different: it captures each constraint format in its native form, preserving the sparsity and structure that makes each format efficient. An R1CS instance becomes a CCS instance of exactly the same size. An AIR instance becomes a CCS instance of exactly the same size. Nothing is wasted in translation.

### The Idea

A CCS instance is defined by a set of sparse matrices $M_1, \ldots, M_t$ over a finite field, a collection of multisets $S_1, \ldots, S_q$ (each specifying which matrices to multiply together element-wise), and constants $c_1, \ldots, c_q$. The satisfying condition is:

$\sum_{i=1}^{q} c_i \cdot \underset{j \in S_i}{\circ} (M_j \cdot \mathbf{z}) = \mathbf{0}$

(The operator $\circ$ denotes the Hadamard product -- element-wise multiplication: $[a, b, c] \circ [d, e, f] = [ad, be, cf]$. The product indexed over $S_i$ means: compute each matrix-vector product $M_j \cdot \mathbf{z}$ separately, then multiply the resulting vectors element by element.)

This looks abstract. Here is what it means concretely.

**R1CS is CCS with two terms.** Set $q = 2$, $S_1 = \{1, 2\}$, $S_2 = \{3\}$, $c_1 = 1$, $c_2 = -1$. The satisfying condition becomes $(M_1 \cdot \mathbf{z}) \circ (M_2 \cdot \mathbf{z}) - (M_3 \cdot \mathbf{z}) = 0$, which is exactly the R1CS equation $\mathbf{A}\mathbf{z} \circ \mathbf{B}\mathbf{z} = \mathbf{C}\mathbf{z}$ when you identify $M_1 = A$, $M_2 = B$, $M_3 = C$.

**AIR is CCS with matrices encoding shift relations.** The transition constraints between consecutive rows become matrix-vector products with appropriate shift structure.

**PLONKish is CCS with matrices encoding selector-weighted gate equations.** The selector polynomials become entries in the matrices; the copy constraints map to specific matrix structures.

The central move is not that CCS enables new computations -- any NP statement can already be expressed in R1CS. CCS provides a *uniform interface*. A proof system that targets CCS automatically handles R1CS, AIR, and PLONKish inputs without conversion overhead. Write one folding scheme for CCS, and it works with every constraint format the industry has produced.

### Why CCS Matters Now

CCS is the native constraint system for every major modern folding scheme:

- **HyperNova** (Kothapalli and Setty, 2023): multi-folding for CCS, using the sumcheck protocol to fold multiple CCS instances simultaneously.
- **ProtoStar** (Bünz and Chen, 2023) and **ProtoGalaxy** (Eagen, Fiore, and Gabizon, 2023): folding schemes that generalize Nova to higher-degree constraint systems by using a single random evaluation to fold across the full constraint degree. ProtoStar handles arbitrary-degree constraints via a "special-sound" folding step; ProtoGalaxy achieves the same goal with improved efficiency by folding multiple instances at once using a polynomial accumulation technique. CCS naturally supports both because its degree parameter $d$ is unrestricted.
- **Neo** (Nguyen and Setty, 2025): a lattice-based folding scheme targeting CCS natively, achieving post-quantum security with small-field efficiency. (LatticeFold, by Boneh and Chen, is an earlier lattice-based folding scheme; Neo is specifically designed for CCS with different structural properties.)
- **LatticeFold+** (Boneh and Chen, 2025): extends LatticeFold with faster, simpler lattice-based folding and shorter proofs.

Without CCS, none of these systems could claim generality. Each would be locked to R1CS (like Nova) or would need separate implementations for each constraint format. CCS is the abstraction layer that made the folding revolution possible.

The gap between research and deployment is real, however. Production systems in early 2026 still largely use PLONKish (Halo2, Scroll) or AIR (StarkWare, Stwo). The CCS-native stack is approximately two to three years behind the research frontier. But the trajectory is clear: as folding-based proof systems move from research prototypes to production deployments, CCS will become the standard target.

The parallel to programming language history is instructive. In the 1960s, each computer had its own instruction set, its own assembler, and its own operating conventions. Writing a program for an IBM 7090 required completely different code than writing for a UNIVAC 1108. Then came C and UNIX, which provided a common language and a common operating system interface. Programs written in C could run on any machine with a C compiler. CCS plays the same role for constraint systems: it provides a common mathematical interface that any proof system can target. Write your constraints in CCS, and any CCS-compatible proof system -- HyperNova, ProtoStar, Neo -- can prove them. The "operating system" for zero-knowledge proof systems is being standardized, even if the "applications" (production deployments) have not yet caught up.

### The Degree Parameter

One subtle but important feature of CCS is the degree parameter $d$, which captures the maximum degree of the constraint polynomials. R1CS has $d = 2$ (bilinear constraints). PLONKish can have $d = 2$ or higher, depending on the custom gate design. CCS handles arbitrary degree without modification.

This matters because higher-degree constraints can capture more complex operations in fewer constraints. A single degree-$4$ constraint can express relationships that would require multiple degree-$2$ R1CS constraints. The tradeoff is that higher-degree constraints require more sophisticated proof techniques -- but the sumcheck protocol, which we turn to next, handles arbitrary degrees naturally.

To see the degree parameter in action, return to the "x * (x + 1)" computation. In R1CS ($d = 2$), this requires two constraints: $t = x + 1 = 4$ (degree $1$, but padded to the bilinear form as $(x + 1) \cdot 1 = t$) and $\text{result} = x \cdot t$ (degree $2$). In a CCS instance with $d = 3$, you could express the entire computation in a single constraint: $x \cdot (x + 1) - \text{result} = 0$, which is a degree-$2$ polynomial in $x$. With $d = 4$, you could encode $x \cdot (x + 1) \cdot (x + 2) - \text{result} = 0$ in a single constraint -- a relationship that would require three R1CS constraints (one for each pairwise multiplication). Higher degree means more computation packed into fewer constraints, at the cost of more complex proof machinery.

### Three Dialects, One Grammar

Return to the three micro-examples we built in the previous sections and look at them through the CCS lens. What CCS reveals is that R1CS, AIR, and PLONKish are not three different formalisms. They are three dialects of the same language.

**R1CS is CCS with $q = 2$.** You need exactly two multisets: $S_1 = \{1, 2\}$ (which multiplies the results of matrices $M_1$ and $M_2$ element-wise) and $S_2 = \{3\}$ (which provides $M_3$'s result). The CCS equation becomes $c_1 \cdot (M_1 \cdot \mathbf{z} \circ M_2 \cdot \mathbf{z}) + c_2 \cdot (M_3 \cdot \mathbf{z}) = 0$, with $c_1 = 1$ and $c_2 = -1$. This is exactly $(\mathbf{A} \cdot \mathbf{z}) \circ (\mathbf{B} \cdot \mathbf{z}) - \mathbf{C} \cdot \mathbf{z} = 0$ -- the R1CS equation, expressed in CCS notation. Two matrix-vector products, one Hadamard product, one subtraction. That is the entire constraint system. Every R1CS instance that has ever been deployed -- every Groth16 proof, every Spartan verification -- is a CCS instance with $q = 2$.

For the "3 * 4 = 12" multiplication from the spreadsheet example, the CCS encoding has $t = 3$ matrices ($M_1 = A$, $M_2 = B$, $M_3 = C$), $q = 2$ multisets ($S_1 = \{1, 2\}$ and $S_2 = \{3\}$), and the witness vector $\mathbf{z} = (1, 3, 4, 12)$ where the first entry is the constant 1. The matrix A selects the left operand (3), B selects the right operand (4), and C selects the output (12). The Hadamard product $(\mathbf{A} \cdot \mathbf{z}) \circ (\mathbf{B} \cdot \mathbf{z})$ computes $3 \cdot 4 = 12$ element-wise, and subtracting $\mathbf{C} \cdot \mathbf{z} = 12$ yields zero. One constraint, three matrices, one Hadamard product.

**AIR is CCS with shift matrices.** The counter example from earlier had the transition constraint $\text{counter}[i+1] = \text{counter}[i] + \text{flag}[i]$. In CCS, this becomes a set of matrices where one matrix $M_{\text{shift}}$ extracts the "next row" values and another $M_{\text{current}}$ extracts the "current row" values. For a 3-row trace, $M_{\text{current}}$ might have ones on the diagonal (selecting counter[0], counter[1], counter[2]) while $M_{\text{shift}}$ has ones on the superdiagonal (selecting counter[1], counter[2], counter[0] with wraparound). The shift operation -- looking at row i + 1 instead of row i -- is encoded in the matrix structure itself. The polynomial constraint between consecutive rows becomes a matrix-vector product where the matrix has ones on a shifted diagonal. What looked like a fundamentally different formalism (rules between consecutive rows, rather than rules within a single row) turns out to be a specific matrix pattern within CCS.

**PLONKish is CCS with selector-weighted matrices.** The PLONKish trace with its $q_{\text{add}}$ and $q_{\text{mul}}$ columns maps to CCS matrices where the selector values are baked into the matrix entries. The gate equation $q_{\text{add}} \cdot (a + b - c) + q_{\text{mul}} \cdot (a \cdot b - c) = 0$ becomes a CCS instance where one multiset captures the addition term (weighted by $q_{\text{add}}$) and another captures the multiplication term (weighted by $q_{\text{mul}}$). The copy constraints -- the permutation argument that wires outputs to inputs -- map to additional matrix structure that enforces equality between specific positions in the witness vector.

The visual is this: imagine three spreadsheets, each with different column headers and different rules. The R1CS spreadsheet has columns A, B, C with the rule "A times B equals C." The AIR spreadsheet has columns for registers with the rule "next row relates to current row by this transition polynomial." The PLONKish spreadsheet has witness columns and selector columns with the rule "the active gate constraint must be satisfied." Three different layouts. Three different conventions. But CCS says: they are all just matrices times a witness vector, combined with Hadamard products and summed to zero. One grammar, three dialects.

This is not a metaphor. It is a theorem. Any R1CS instance, any AIR instance, any PLONKish instance can be mechanically translated into a CCS instance with no increase in constraint count or witness size. The translation preserves everything -- the structure, the sparsity, the degree. When a proof system like HyperNova targets CCS, it is not accepting a lowest-common-denominator format. It is accepting the universal format that contains every existing constraint dialect as a special case.

The practical consequence is immediate. Before CCS, a developer choosing R1CS was simultaneously choosing Groth16 or Spartan. A developer choosing AIR was choosing STARKs. A developer choosing PLONKish was choosing Halo2 or PLONK. Switching constraint systems meant rewriting the circuit and the proof system integration. CCS breaks this coupling. Write your constraints in whichever dialect is natural for your computation -- R1CS for simple circuits, AIR for VM traces, PLONKish for mixed-gate workloads -- and any CCS-compatible proof system will accept them without translation overhead. The grammar is universal; the dialects are a matter of convenience.

The existence of a universal constraint grammar is not obvious. One might have expected that the structural differences between R1CS (bilinear, flat), AIR (uniform, sequential), and PLONKish (selector-gated, permutation-wired) would require genuinely different proof techniques -- that no single algebraic framework could capture all three without paying some conversion tax. CCS demonstrates that the differences are shallow. At the level of sparse matrix-vector products and Hadamard products, all three constraint systems are doing the same thing. The "three families" narrative that dominated ZK from 2018 to 2022 was a historical artifact, not a mathematical necessity.

CCS provides the universal grammar. Sumcheck provides the universal verification engine. The two are partners: CCS tells us *what* the constraints look like -- a sum of Hadamard products of matrix-vector pairs -- and sumcheck tells us *how to check* that sum without evaluating every term. The verifier does not inspect every cell of the constraint spreadsheet. Instead, sumcheck reduces the problem: "does this multilinear polynomial sum to zero over the boolean hypercube?" becomes, after n rounds of interaction, "does this polynomial evaluate correctly at one random point?" The reduction is exponential -- from $2^n$ checks to $n$ rounds -- and it is the reason modern proof systems can verify in time logarithmic in the computation size.

---

At this point you understand three constraint system dialects (R1CS, AIR, PLONKish) and their unification under CCS. The encoding problem is solved -- we know how to turn computation into polynomial equations. The next question is: how does the verifier check that all these equations hold without re-doing the computation? The answer is a protocol from 1992, rediscovered by the ZK community three decades later.


## Summary

Customizable Constraint Systems (Setty, Thaler, Wahby 2023) unify R1CS, AIR, and PLONKish as special cases of a single sparse matrix-vector framework, with no size overhead in the translation. CCS is the native target for HyperNova, ProtoStar, ProtoGalaxy, Neo, and LatticeFold+. Production systems still predominantly use PLONKish or AIR, but CCS adoption is the clear direction as folding-based provers mature.

## Key claims

- A CCS instance: sparse matrices $M_1,\ldots,M_t$, multisets $S_1,\ldots,S_q$, constants $c_1,\ldots,c_q$; satisfying condition $\sum_i c_i \cdot \bigcirc_{j\in S_i}(M_j\cdot\mathbf{z}) = \mathbf{0}$.
- R1CS is CCS with $q=2$, $S_1=\{1,2\}$, $S_2=\{3\}$: recovers $(M_1\mathbf{z})\circ(M_2\mathbf{z}) = M_3\mathbf{z}$.
- AIR is CCS with shift matrices encoding consecutive-row relationships; PLONKish is CCS with selector-weighted matrix entries.
- CCS accepts degree parameter $d$; R1CS has $d=2$; higher $d$ encodes more computation per constraint.
- HyperNova (Kothapalli and Setty, 2023): multi-folding for CCS via sumcheck. Neo (Nguyen and Setty, 2025): first lattice-based CCS folding. LatticeFold+ (Boneh and Chen, 2025): shorter lattice proofs.
- Translation from any of the three formats to CCS is lossless — no increase in constraint count or witness size.
- Production lag: CCS-native stack is ~2–3 years behind the research frontier as of early 2026.

## Entities

- [[boneh]]
- [[folding]]
- [[groth16]]
- [[halo2]]
- [[hypernova]]
- [[latticefold]]
- [[nova]]
- [[plonk]]
- [[setty]]
- [[small-field]]
- [[spartan]]
- [[starks]]

## Dependencies

- [[ch05-the-constraint-system-evolution-r1cs-air-plonkish]] — the three dialects CCS unifies
- [[ch05-the-sumcheck-protocol-the-hidden-foundation]] — sumcheck is CCS's verification engine
- [[ch05-lookup-arguments]] — HyperNova/Lasso use CCS as their constraint format
- [[ch05-where-the-layers-collapse]] — CCS is part of the proof-core triad discussion

## Sources cited

- [R-L4-4] Setty, Thaler, Wahby. "Customizable Constraint Systems for Succinct Arguments." ePrint 2023/552.

## Open questions

None flagged by this section.

## Improvement notes

_All P0/P1/P2/P3 findings resolved in Phase 3 revisions (2026-04-18 through 2026-04-20)._

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

## Links

- Up: [[05-encoding-the-performance]]
- Prev: [[ch05-the-constraint-system-evolution-r1cs-air-plonkish]]
- Next: [[ch05-the-sumcheck-protocol-the-hidden-foundation]]
