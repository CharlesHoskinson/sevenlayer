---
title: "The Constraint System Evolution: R1CS, AIR, PLONKish"
slug: ch05-the-constraint-system-evolution-r1cs-air-plonkish
chapter: 5
chapter_title: "Encoding the Performance"
heading_level: 2
source_lines: [1677, 1868]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 5095
---

## The Constraint System Evolution: R1CS, AIR, PLONKish

The three major constraint systems -- R1CS, AIR, and PLONKish -- emerged in a span of just seven years (2012-2019). Each was designed to solve a specific limitation of its predecessor, but each also introduced new trade-offs. Understanding this evolution is not optional for understanding modern ZK: every proof system, every zkVM, and every privacy protocol in production today is built on one of these three foundations (or, increasingly, on CCS, which unifies all three).

The history of arithmetization is a history of increasing expressiveness. Each new constraint system solved a specific limitation of its predecessor. Understanding this genealogy is essential because the constraint system you choose determines which proof systems you can use, which fields are efficient, and how much overhead the encoding imposes.

The genealogy also reveals how rapidly the field moves. R1CS was introduced in 2012. By 2023, it was already the "legacy" format -- still deployed in production (Groth16 is not going away), but superseded by more expressive systems for new development. The eleven-year span from R1CS to CCS saw more architectural innovation in constraint system design than the previous four decades of theoretical computer science produced. This acceleration is driven by practical pressure: the economic value of efficient zero-knowledge proofs creates strong incentives for better arithmetization.

### R1CS: The Assembly Language (2012)

The first practical arithmetization emerged from the work of Gennaro, Gentry, Parno, and Raykova (GGPR) in 2012, who introduced the QAP (Quadratic Arithmetic Program) framework that R1CS later formalized. The name "Rank-1 Constraint System" describes the mathematical structure precisely: each constraint has rank 1 (it is the product of two linear functions), and the system is a collection of such constraints. The "rank-1" designation means each constraint captures exactly one multiplication -- a bilinear relationship between variables. Addition is free (it does not require a constraint, because linear combinations can be folded into the matrix entries). Only multiplication generates constraints. This is why the number of R1CS constraints for a circuit equals the number of multiplication gates, not the total number of gates.

Before the mathematical notation, let us ground it in the spreadsheet from the previous section. Imagine your spreadsheet has three special columns -- call them A, B, and C. For each row, column A and column B each contain a combination of the variables, and column C contains the result. The rule for every row is: (what is in column A) multiplied by (what is in column B) must equal (what is in column C). That is all R1CS is: a spreadsheet where every row enforces one multiplication rule. The mathematical notation below says exactly this, just more precisely.

R1CS encodes a computation as a list of constraints, each of the form:

*(linear combination of variables) times (linear combination of variables) equals (linear combination of variables)*

Or, in mathematical notation: $(\mathbf{A} \cdot \mathbf{z}) \circ (\mathbf{B} \cdot \mathbf{z}) = \mathbf{C} \cdot \mathbf{z}$, where $\mathbf{A}$, $\mathbf{B}$, and $\mathbf{C}$ are sparse matrices and $\mathbf{z}$ is the vector of all variables (public inputs, private witness, and intermediate values). Each row of the matrices defines one constraint. Each constraint captures one multiplication gate.

For the tiny spreadsheet example (3 + 4 = 7, then 7 * 2 = 14), the witness vector is $\mathbf{z} = (1, 3, 4, 7, 2, 14)$ -- the constant 1 followed by the variables x, y, z, w, and the final result. The first row of A selects "x" (entry 1 in position corresponding to x), the first row of B selects "1" (indicating the addition is encoded as (x + y) * 1 = z after reformulation), and the first row of C selects "z". The second row of A selects "z" (value 7), the second row of B selects "w" (value 2), and the second row of C selects "result" (value 14). The matrices are mostly zeros -- only a handful of entries are nonzero. This sparsity is typical: a circuit with millions of constraints has matrices with millions of rows but only a few nonzero entries per row.

R1CS is the assembly language of constraint systems -- simple, well-understood, and directly amenable to proof systems like Groth16 and Spartan. Groth16, deployed across most of the Ethereum ecosystem, works natively with R1CS and produces the smallest possible proofs -- three elliptic curve group elements, constant-time verification.

But R1CS has a fundamental limitation: each constraint is bilinear -- degree $2$. You can encode a multiplication ($a \cdot b = c$) directly. But what about a computation that requires checking a hash function, where a single invocation might need thousands of multiplications? You encode each multiplication as a separate constraint, one after another. There is no way to express a higher-degree relationship in a single constraint, and there is no notion of "this constraint applies uniformly across all time steps." Every gate gets its own row.

For small circuits, R1CS works beautifully. For large, repetitive computations -- like executing millions of processor instructions in a zkVM -- the lack of structure becomes a liability.

To see this concretely, consider encoding a computation with 10 million multiplication gates in R1CS. You need 10 million rows in the matrices A, B, and C. Each matrix is sparse (most entries are zero), but the total number of nonzero entries -- and hence the prover's work -- scales linearly with the gate count. There is no compression possible: R1CS treats each gate independently, with no awareness that gate 5,000,001 might be performing exactly the same operation as gate 1. Compare this to a function that repeats the same 1,000-gate circuit 10,000 times: R1CS still requires 10,000,000 separate constraints, while a structured constraint system could potentially describe the repeating pattern once and instantiate it 10,000 times. This structural blindness is what motivated the search for richer constraint formats.

Yet R1CS persists. Groth16 proofs (which require R1CS) remain the gold standard for on-chain verification because of their unmatched proof size: 3 group elements, roughly 128 bytes, verifiable in constant time. No other proof system achieves this compactness. When Ethereum smart contracts verify ZK proofs, the gas cost of verification is proportional to proof size -- and Groth16's tiny proofs mean minimal gas costs. Many production systems (Zcash, Tornado Cash, Worldcoin) use Groth16 for precisely this reason, accepting the constraint system's limitations in exchange for the proof system's efficiency. R1CS is the assembly language: nobody wants to write it directly, but the machine code it produces is unbeatable.

### AIR: The State Machine (2018)

The Algebraic Intermediate Representation arrived alongside STARKs, introduced by Ben-Sasson, Bentov, Horesh, and Riabzev in 2018. The name is precise: "Algebraic" because the constraints are polynomial equations over fields (not boolean circuits or SAT formulas). "Intermediate" because AIR sits between the high-level computation and the low-level proof system -- it is the "compiled" form of the computation, analogous to LLVM IR in a compiler toolchain. "Representation" because it is a way of representing the computation, not the computation itself. AIR solves the structure problem by embracing the spreadsheet metaphor directly.

An AIR consists of two things: an execution trace (a 2D matrix where rows are time steps and columns are algebraic registers) and transition constraints (polynomial equations that must hold between consecutive rows). The constraints are *uniform* -- the same polynomial equations apply at every row.

This uniformity is AIR's great strength and its great limitation. It is a perfect fit for sequential computations where the same operation repeats: hash chains, state machine execution, virtual machine instruction cycles. The constraint "if the opcode is ADD, then the output register equals the sum of the two input registers" applies identically at every step. You write it once; it is enforced everywhere.

The word "uniform" deserves emphasis. In R1CS, each constraint row can encode a completely different relationship between variables. Row 1 might enforce $a + b = c$; row 2 might enforce $d \cdot e = f$; row 3 might enforce $g = h$. Each row is independent. In AIR, every row obeys the same set of transition polynomials. If the transition constraint says "$\text{column\_3}[\text{next}] = \text{column\_1}[\text{current}] + \text{column\_2}[\text{current}]$," then this relationship holds at every pair of consecutive rows. The prover cannot make exceptions. This rigidity is what enables compression: a single polynomial equation describes the entire computation, regardless of how many steps it contains.

The limitation is that AIR cannot natively handle non-uniform computation. If your program has different instruction types -- additions, multiplications, hash invocations, memory accesses -- you need tricks to encode the selection logic ("which instruction is executing at this row?") within the uniform framework. This is possible but adds complexity and overhead.

In practice, real STARK-based systems handle non-uniformity by using multiple AIR traces -- one per "sub-machine." Cairo's architecture, for example, decomposes the VM into separate traces for the CPU, memory, range checks, and each built-in operation (Pedersen hash, ECDSA, bitwise operations). Each trace is a separate AIR with its own transition constraints. Cross-trace consistency is enforced through permutation arguments and lookup arguments that connect the traces: when the CPU trace records "hash instruction at step 1000," the hash trace must contain a corresponding row with matching inputs and outputs. This multi-trace design preserves AIR's uniformity within each trace while handling the non-uniformity of a full instruction set across traces. The cost is the cross-trace connection overhead, but for computations dominated by a single operation type (as hash-heavy applications often are), the overhead is manageable.

AIR became the foundation of the STARK ecosystem: StarkWare's Stone and Stwo provers, Polygon Miden, and others. Its tight coupling with FRI (the hash-based polynomial commitment scheme) means AIR-based systems are transparent (no trusted setup) and plausibly post-quantum secure.

The AIR-FRI coupling deserves a moment of attention because it illustrates how Layers 4 and 5 (arithmetization and proof system) become inseparable. FRI works by repeatedly folding a polynomial in half -- reducing its degree by a factor of 2 at each step -- and checking consistency at random points. This folding requires the polynomial to be evaluated on a domain with a specific multiplicative structure (a "coset" of a subgroup of the field). AIR traces are naturally expressed as polynomials on such domains because the trace rows correspond to consecutive powers of a group generator. The uniformity of AIR's transition constraints means the constraint polynomial has the same degree structure as the trace polynomial, which is exactly what FRI needs. Try to use FRI with a non-uniform constraint system (like PLONKish), and you need additional machinery (permutation polynomials, selector commitments) that adds overhead. AIR and FRI were born for each other.

#### A Tiny AIR: The Counter

To make AIR concrete, consider the simplest possible state machine: a counter that starts at 0 and increments by 1 each step. The execution trace has two columns -- `counter` (the current value) and `flag` (whether to increment) -- and three rows:

| Row | counter | flag |
|-----|---------|------|
| 0   | 0       | 1    |
| 1   | 1       | 1    |
| 2   | 2       | 1    |

The transition constraint is a single polynomial equation that must hold between every pair of consecutive rows:

$\text{counter}[i+1] = \text{counter}[i] + \text{flag}[i]$

Check it. Between rows 0 and 1: does 1 = 0 + 1? Yes. Between rows 1 and 2: does 2 = 1 + 1? Yes. The trace is valid.

Now suppose a cheating prover submits a trace where row 2 claims `counter = 5`. The transition constraint between rows 1 and 2 becomes: does 5 = 1 + 1? No. The constraint is violated, and the proof fails.

There is a subtlety that the transition constraint alone does not capture: the starting value. The transition constraint says "each row follows correctly from the previous row," but it says nothing about where the counter begins. A trace starting at counter = 1000 with flag = 1 at every row would satisfy the transition constraint perfectly -- 1000, 1001, 1002 -- even though the counter was supposed to start at 0. This is where **boundary constraints** enter. A boundary constraint pins a specific cell to a specific value: "counter at row 0 must equal 0." In an AIR, you typically have transition constraints (which apply uniformly between consecutive rows) and boundary constraints (which apply at specific rows, usually the first and last). The transition constraints ensure the computation proceeds correctly; the boundary constraints ensure it starts and ends in the right place.

The full AIR for this counter is therefore:

- Transition constraint: $\text{counter}[i+1] = \text{counter}[i] + \text{flag}[i]$ (for all consecutive row pairs)
- Boundary constraint: $\text{counter}[0] = 0$ (the counter starts at zero)
- Boundary constraint: $\text{flag}[i] \cdot (1 - \text{flag}[i]) = 0$ (each flag is boolean -- either 0 or 1)

The boolean constraint on the flag deserves attention. Without it, a cheating prover could set flag = 7 at some row, making the counter jump by 7 instead of 0 or 1. The constraint $\text{flag} \cdot (1 - \text{flag}) = 0$ is satisfied only when flag is 0 or 1 (plug in either value and one factor is zero). This is a polynomial constraint of degree $2$ -- exactly the kind of equation that AIR handles naturally.

The critical observation is what the prover *wrote down* to define this constraint system. Not three separate rules -- one for each row -- but a small set of polynomial equations applied uniformly across the entire trace. One transition rule and a few boundary conditions, enforced everywhere. If the counter had a million rows instead of three, the constraint description would be identical: the same equations. Only the trace grows; the constraints stay fixed.

This is the structural difference from R1CS. In R1CS, you would write a separate constraint for each row: "row 0's output equals row 0's input plus row 0's flag," then "row 1's output equals row 1's input plus row 1's flag," and so on -- one constraint per step. For a million-step computation, you need a million constraints. In AIR, you write the rule once. The prover fills in the trace; the polynomial machinery checks the rule everywhere simultaneously.

For repetitive computations -- hash chains where the same compression function executes thousands of times, virtual machines where the same instruction cycle repeats for every step -- AIR's uniformity is not just convenient. It is a compression of the constraint description itself, from linear in the number of steps to constant in the number of distinct transition rules. That compression is what made STARKs practical for proving large computations.

One further detail illuminates how the polynomial machinery works behind the scenes. The prover does not submit the raw trace table to the verifier. Instead, the prover interpolates each column of the trace as a polynomial. For the counter column with values (0, 1, 2), the prover finds a polynomial $P(x)$ such that $P(0) = 0$, $P(1) = 1$, $P(2) = 2$ -- in this case, simply $P(x) = x$. For the flag column with values (1, 1, 1), the polynomial is $F(x) = 1$. The transition constraint "$P(x+1) = P(x) + F(x)$" becomes a polynomial identity that must hold at $x = 0$ and $x = 1$ (every pair of consecutive rows). The proof system checks this identity at a random evaluation point -- not at $x = 0$ or $x = 1$, but at some random $r$ chosen by the verifier -- and the Schwartz-Zippel lemma guarantees that a false identity will fail this random check with overwhelming probability.

The trace, the constraints, and the verification all reduce to polynomials. The trace columns are polynomials. The transition constraint is a polynomial identity. The verification is a polynomial evaluation. This is what "arithmetization" means in practice: every aspect of the computation becomes a polynomial, and every check becomes a polynomial evaluation.

The polynomial encoding also reveals the source of the overhead. The counter trace has 3 rows and 2 columns -- 6 values. But the polynomials that interpolate these columns have degree $2$ (you need a degree-$2$ polynomial to pass through 3 points in general). The transition constraint, when expressed as a polynomial, produces a "constraint polynomial" whose degree is the sum of the degrees of the trace polynomials it involves. If the trace polynomial has degree $d$ and the transition constraint has algebraic degree $k$, the constraint polynomial has degree roughly $d \cdot k$. For a trace with $n$ rows, $d$ is roughly $n$, so the constraint polynomial has degree roughly $n \cdot k$. This polynomial must be shown to vanish on all consecutive-row pairs, which means it is divisible by a "vanishing polynomial" $Z(x)$ that has roots at the evaluation domain. The quotient $T(x) = \text{constraint}(x) / Z(x)$ is the polynomial the prover commits to; if the division is exact (no remainder), the constraints are satisfied. If the prover cheated, the division leaves a remainder, and the random evaluation check catches it.

This is where the NTTs come in. Converting between coefficient and evaluation representations of these high-degree polynomials requires the Number Theoretic Transform -- the finite-field version of the FFT -- which dominates the prover's computation time.

The limitation is equally visible. Suppose you want some rows to add and other rows to multiply. With a single uniform constraint, you cannot express "do addition at row 5 and multiplication at row 6" without encoding the selection logic into the polynomial itself -- adding flag columns, conditional terms, and degree overhead. The counter example is clean because every row does the same thing. Real programs do not.

### PLONKish: The Custom Workshop (2019)

PLONK, introduced by Gabizon, Williamson, and Ciobotaru in 2019, took a different approach. Instead of uniform constraints, PLONKish arithmetization uses *selector columns* to enable non-uniform gates.

The key innovation separates the constraint system into two components:

1. **Gate constraints**: polynomial equations controlled by selector polynomials. Different rows can have different gate types. If the selector for "addition" is active at row 5, the addition constraint is enforced there. If the selector for "multiplication" is active at row 6, the multiplication constraint is enforced there. You can define custom gates for any operation you need.

2. **Copy constraints**: a permutation argument that enforces wiring -- ensuring that the output of one gate is correctly fed as input to another gate. This replaces R1CS's matrix-based variable assignment with a more flexible connection mechanism.

PLONKish sits between R1CS and AIR in expressiveness. Like AIR, it uses a structured trace with rows and columns. Unlike AIR, different rows can follow different rules. Like R1CS, it can handle arbitrary circuits. Unlike R1CS, it supports custom gates that capture complex operations in fewer constraints.

PLONKish became the dominant arithmetization in deployed systems. Halo2 (used by Zcash and Scroll), Polygon zkEVM (before its shutdown), and numerous other production systems chose PLONKish because its flexibility handles the diverse instruction sets of real-world computations. The Halo2 library, originally developed by the Electric Coin Company for the Zcash Orchard protocol, became the de facto standard for PLONKish circuit development. Its "region-based" API lets developers define gates, assign cells, and specify copy constraints in a structured way that catches many common errors at compile time. Scroll's zkEVM -- one of the most ambitious ZK projects ever attempted -- encoded the entire Ethereum Virtual Machine instruction set as Halo2 PLONKish circuits, using custom gates for EVM opcodes, lookup arguments for bytecode verification, and copy constraints to wire the data path. The resulting circuit has millions of constraints per block and requires GPU clusters to prove, but it works -- which says something about PLONKish's flexibility.

#### A Tiny PLONKish Circuit: Compute 3 + 4, Then Multiply, Then Add Again

Here is a three-row PLONKish trace that computes (3 + 4) * 2 + 1 = 15. The trace has three "witness" columns (a, b, c) and two "selector" columns (q_add, q_mul):

| Row | a  | b  | c  | q_add | q_mul |
|-----|----|----|----|-------|-------|
| 0   | 3  | 4  | 7  | 1     | 0     |
| 1   | 7  | 2  | 14 | 0     | 1     |
| 2   | 14 | 1  | 15 | 1     | 0     |

The gate constraint is a single equation evaluated at every row:

$q_{\text{add}} \cdot (a + b - c) + q_{\text{mul}} \cdot (a \cdot b - c) = 0$

At row 0: $q_{\text{add}} = 1$, $q_{\text{mul}} = 0$, so the equation becomes $1 \cdot (3 + 4 - 7) + 0 \cdot (\ldots) = 0$. Check: $0 = 0$. The addition gate is active.

At row 1: $q_{\text{add}} = 0$, $q_{\text{mul}} = 1$, so the equation becomes $0 \cdot (\ldots) + 1 \cdot (7 \cdot 2 - 14) = 0$. Check: $0 = 0$. The multiplication gate is active.

At row 2: $q_{\text{add}} = 1$, $q_{\text{mul}} = 0$, so the equation becomes $1 \cdot (14 + 1 - 15) + 0 \cdot (\ldots) = 0$. Check: $0 = 0$. The addition gate is active again.

The selectors act as switches. When $q_{\text{add}} = 1$ and $q_{\text{mul}} = 0$, only the addition constraint is "on." When the selectors flip, only the multiplication constraint is "on." One polynomial equation, evaluated identically at every row, enforces different gate types depending on which selector is active.

But the gate constraint alone does not guarantee correctness. Look at the trace: row 0 produces c = 7, and row 1 consumes a = 7. How does the proof system know these two 7s are the *same* value -- that the output of row 0 actually flows into the input of row 1?

This is the job of the **copy constraint**. A permutation argument -- a separate cryptographic mechanism outside the gate equation -- enforces that the cell (row 0, column c) contains the same value as the cell (row 1, column a). Similarly, (row 1, column c) must equal (row 2, column a). The permutation argument works by proving that a certain set of values is a rearrangement of another set, which can only be true if the "wired" cells agree. Without copy constraints, a cheating prover could fill row 1 with a = 999 and the gate equation would still pass (as long as 999 * 2 = c at row 1). The copy constraint is what stitches the circuit together.

To see the copy constraint at work, consider what happens without it. A cheating prover submits this trace:

| Row | a  | b  | c  | q_add | q_mul |
|-----|----|----|----|-------|-------|
| 0   | 3  | 4  | 7  | 1     | 0     |
| 1   | 99 | 2  | 198| 0     | 1     |
| 2   | 198| 1  | 199| 1     | 0     |

Every gate constraint passes: 3 + 4 = 7, 99 * 2 = 198, 198 + 1 = 199. But the computation is wrong -- row 1 should have used a = 7 (the output of row 0), not a = 99. Without the copy constraint binding cell (row 0, c) to cell (row 1, a), the prover is free to insert any value it likes. The copy constraint catches this: it requires that position (row 0, column c) and position (row 1, column a) hold the same value. Since 7 is not 99, the permutation check fails, and the proof is rejected.

This reveals why PLONKish is more flexible than AIR. In the AIR counter example, every row obeyed the same transition rule. Here, row 0 adds, row 1 multiplies, and row 2 adds again -- three different operations in three rows, controlled by selector values. You can define custom gates for any operation: a "range check" gate, a "Poseidon hash round" gate, an "elliptic curve addition" gate. Each gets its own selector column, and the prover activates whichever gate the computation requires at each row. The trace is a heterogeneous computation log, not a uniform state machine.

The power of custom gates becomes clearer with a slightly more complex example. Suppose you want to enforce that a value lies in the range $[0, 255]$ -- an 8-bit range check. In R1CS, you would decompose the value into 8 bits, constrain each bit to be boolean (8 constraints), and constrain the sum to equal the original value (1 constraint) -- 9 constraints total. In PLONKish, you can define a single custom "range gate" that encodes the entire check in one row, using a lookup argument or a specialized polynomial identity. One row, one gate, one constraint. The circuit designer creates the gate once; the prover activates it wherever a range check is needed.

The cost of this flexibility is the copy constraint machinery. The permutation argument adds overhead -- both in proof size and in prover computation -- that AIR avoids because AIR's uniform structure implicitly handles data flow between consecutive rows. But for computations that mix many different operations (as real programs do), the overhead is worth paying.

#### The Same Computation, Three Encodings

To crystallize the differences, consider encoding the same simple computation -- "compute $x \cdot (x + 1)$ where $x = 3$, so the result is $12$" -- in all three systems.

**In R1CS:** You need two constraints. First, an addition: an intermediate variable $t = x + 1 = 4$. Then a multiplication: $\text{result} = x \cdot t = 3 \cdot 4 = 12$. Each constraint takes one row in the R1CS matrix. The matrices A, B, C encode the variable wiring. Two rows, two constraints, done.

**In AIR:** You set up a two-row trace. Row 0 holds $x = 3$ and computes $t = x + 1 = 4$. Row 1 holds the multiplication $\text{result} = x \cdot t = 12$. The transition constraint relates consecutive rows. But here is the awkwardness: the addition and the multiplication are *different* operations, and AIR wants uniform constraints across all rows. You either need to encode both operations into a single transition polynomial (using conditional logic with flag columns, which increases the constraint degree), or you define a two-step cycle where even rows add and odd rows multiply (which works but means half the trace structure is "wasted" on selection logic). For this tiny example, AIR is overkill.

**In PLONKish:** Row 0 uses the addition gate: $a = 3$, $b = 1$, $c = 4$ ($q_{\text{add}} = 1$). Row 1 uses the multiplication gate: $a = 3$, $b = 4$, $c = 12$ ($q_{\text{mul}} = 1$). A copy constraint links (row 0, column c) to (row 1, column b), and another links the input $x = 3$ to (row 1, column a). Two rows, two different gate types, clean and direct.

The comparison reveals each system's natural habitat. R1CS handles this computation most directly -- two bilinear constraints, no overhead. PLONKish handles it almost as directly, with slight overhead from the copy constraints. AIR handles it least naturally, because the computation is not repetitive -- there is no pattern that repeats across many rows. For a computation that *is* repetitive (running the same hash compression 1000 times), the ranking reverses: AIR wins by writing the constraint once, while R1CS and PLONKish must either repeat the constraint description 1000 times or use recursion to simulate repetition.

The constraint count for the same computation across different systems is instructive:

| System | Constraints for x*(x+1) | Constraints for 1000 hash rounds | Why |
|--------|------------------------|--------------------------------|-----|
| R1CS | 2 | ~30,000,000 | 1 constraint per gate, ~30,000 per hash round |
| AIR | ~4 (with padding) | ~30,000 | One transition polynomial, reused 1000 times |
| PLONKish | 2 (+ copy constraints) | ~15,000,000 | Custom hash gates cut per-round cost in half |

The numbers are approximate, but the ratios are revealing. For the tiny computation, all three systems are roughly comparable. For the hash chain, AIR's constraint count is independent of the number of repetitions -- it depends only on the number of distinct transition types. This is why STARKs dominate in hash-heavy workloads (blockchain state verification, recursive proof composition) while PLONKish dominates in mixed workloads (smart contract execution, general-purpose circuits).

A clarification for the precise reader: AIR's "~30,000" for 1000 hash rounds refers to the *constraint description* size -- the number of distinct polynomial equations that must hold. The actual *trace* still has 1000 * (rows per hash round) rows, each of which must satisfy the constraints. The prover's work is proportional to the trace size, not the constraint description size. But the constraint description size matters for the verifier (who must check the polynomial identity, not every row) and for the proof size (which depends on the degree of the constraint polynomial, not the number of trace rows). The asymmetry between "small constraint description, large trace" is precisely what makes AIR efficient for repetitive computations: the verifier's work grows with the constraint complexity, not with the number of repetitions.

### Three Dialects, One Problem

By 2022, the ZK ecosystem had three constraint system families, each with its own proof systems, tooling, and community:

| System | Year | Constraint Structure | Best For | Key Proof Systems |
|--------|------|---------------------|----------|-------------------|
| R1CS | 2012 | Bilinear (degree 2) | Small circuits, Groth16 | Groth16, Spartan, Nova |
| AIR | 2018 | Uniform polynomial | VM traces, STARKs | STARKs (Stone, Stwo) |
| PLONKish | 2019 | Selector-gated, custom | Flexible circuits | PLONK, Halo2 |

A folding scheme designed for R1CS could not accept AIR input. A proof system built for AIR could not handle PLONKish circuits. A developer choosing an arithmetization was simultaneously choosing a proof system ecosystem -- and switching later meant rewriting everything.

The fragmentation had real costs. When the Polygon team decided to migrate from Hermez (PLONK-based) to a STARK-based architecture, the circuit rewrite took years. When Scroll built their zkEVM on Halo2 (PLONKish), they could not easily adopt the newer sumcheck-based proof systems that emerged in 2023-2024 without rewriting their entire constraint system. Research teams working on folding schemes had to choose: target R1CS (like Nova did) and exclude the STARK ecosystem, or target a custom format and exclude everyone else. The constraint system choice was a one-way door -- enter through it, and you are locked into the corresponding proof system family for the life of the project.

The field needed a unifier. Not a compromise format that sacrificed efficiency for generality, but a mathematical framework that could express R1CS, AIR, and PLONKish as special cases -- preserving the efficiency of each while providing a single target for proof systems to implement.

---


## Summary

R1CS (2012), AIR (2018), and PLONKish (2019) each solved a specific limitation of its predecessor: R1CS introduced bilinear constraints, AIR added uniformity for repetitive traces, and PLONKish added selector-gated custom gates with copy constraints. By 2022 the three formats were locked into separate proof system ecosystems, motivating CCS. Groth16 proofs remain unbeaten at 192 bytes (3 group elements) despite R1CS's expressiveness limits.

## Key claims

- R1CS has one constraint per multiplication gate; addition is free. Witness vector $\mathbf{z}$ satisfies $(\mathbf{A}\mathbf{z}) \circ (\mathbf{B}\mathbf{z}) = \mathbf{C}\mathbf{z}$.
- AIR transition constraints apply uniformly to every consecutive row pair; a single polynomial equation describes an arbitrarily long trace. Boundary constraints fix start/end values.
- PLONKish separates gate constraints (selector-weighted) from copy constraints (permutation argument); different rows can enforce different operations.
- For 1,000 hash rounds: R1CS ~30,000,000 constraints; AIR ~30,000 (description size only); PLONKish ~15,000,000 with custom hash gates.
- AIR and FRI are structurally coupled — the uniform polynomial structure of AIR matches the folding-based reduction in FRI.
- Choosing a constraint system was a one-way door that locked in a proof system family until CCS.
- R1CS was introduced by GGPR (2012), AIR by Ben-Sasson et al. (2018), PLONKish by Gabizon, Williamson, Ciobotaru (2019).

## Entities

- [[folding]]
- [[groth16]]
- [[halo2]]
- [[nova]]
- [[plonk]]
- [[polygon]]
- [[poseidon]]
- [[spartan]]
- [[starks]]
- [[tornado cash]]
- [[zcash]]

## Dependencies

- [[ch05-the-spreadsheet-metaphor-and-where-it-works]] — spreadsheet model is the prerequisite intuition
- [[ch05-ccs-the-rosetta-stone]] — CCS is the unifier that resolves the three-family fragmentation
- [[ch05-lookup-arguments]] — lookup arguments emerged as a fix to arithmetic-hostile ops in all three systems

## Sources cited

- [R-L4-2] Ben-Sasson, Bentov, Horesh, Riabzev. "Scalable, Transparent, and Post-Quantum Secure Computational Integrity." ePrint 2018/046.
- [R-L4-3] Gabizon, Williamson, Ciobotaru. "PLONK." ePrint 2019/953.
- [R-L4-1] Gennaro, Gentry, Parno, Raykova. "Quadratic Span Programs and Succinct NIZKs without PCPs." EUROCRYPT 2013.

## Open questions

None flagged by this section.

## Improvement notes

- [P1] (A) Groth16 proof size is stated as "three elliptic curve group elements, roughly 128 bytes" in the body and as "192 bytes (3 group elements)" in the Summary. These are inconsistent: three BLS12-381 G1 points are 3 × 48 = 144 bytes (compressed) or 3 × 96 = 288 bytes (uncompressed); the commonly cited figure is 192 bytes for two G1 + one G2. The "128 bytes" figure in the body and "192 bytes" in the summary cannot both be correct; the body figure needs a correction.
- [P1] (A) The AIR constraint count comparison table claims AIR costs "~30,000" constraints for 1,000 hash rounds and attributes this to "description size only" — but a footnote immediately after clarifies that the prover's work scales with trace size, not description size. The table entry is therefore misleading: calling it "~30,000 constraints" for 1,000 rounds implies a 1,000× reduction in prover work, which is not what AIR provides. The table column header or the AIR cell value should be qualified to avoid this misreading.
- [P2] (A) R1CS is credited to GGPR (2012) in one place and the Key claims list cites "GGPR (2012)" correctly. However, the body text says GGPR "introduced the QAP framework that R1CS later formalized" — implying R1CS came after QAP, but R1CS is sometimes treated as a renaming/refinement that happened in 2013 (Parno et al., "Pinocchio"). The history is slightly compressed.
- [P2] (C) Paragraph beginning "The history of arithmetization is a history of increasing expressiveness" is a near-duplicate of the opening paragraph of the same section. Two nearly identical "history of arithmetization" framing sentences appear within the first eight lines — one of them should be cut.
- [P3] (E) The PLONKish section does not discuss the Halo2 commitment scheme (IPA/KZG variants) or why Halo2 avoids a trusted setup, which is a key differentiator over vanilla PLONK. A brief note would improve depth given that Halo2 is cited as the production standard.

## Links

- Up: [[05-encoding-the-performance]]
- Prev: [[ch05-the-spreadsheet-metaphor-and-where-it-works]]
- Next: [[ch05-ccs-the-rosetta-stone]]
