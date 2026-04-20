---
title: "The Causal Web: Why It Is a DAG, Not a Stack"
slug: ch10-the-causal-web-why-it-is-a-dag-not-a-stack
chapter: 10
chapter_title: "The Synthesis -- Three Paths, Not Two"
heading_level: 2
source_lines: [4444, 4485]
source_commit: 9eb332547f6b1cd6e7e67527183abbd5c486974c
status: reviewed
word_count: 1164
---

## The Causal Web: Why It Is a DAG, Not a Stack

The book has presented seven layers as floors in a building -- stacked, each resting on the one below. The evidence from Parts I and II tells a different story. The layers are not a stack; they are a directed acyclic graph with bidirectional pressures. The building metaphor was useful for learning. Now it must be complicated.

The most consequential causal chain runs *upward* from Layer 6. Small-field primitives (BabyBear, M31) at Layer 6 enabled Circle STARKs and efficient multilinear proving at Layer 5, which enabled lookup-based and AIR-based arithmetization at Layer 4, which shaped shard-based witness generation at Layer 3, which favored RISC-V ISAs at Layer 2, and universal zkVMs amortized setup costs at Layer 1. The foundation shaped the building. That much the metaphor gets right.

But there are equally important *downward* pressures. The audience shapes the show:

**Layer 7 forces Layer 6.** Ethereum gas economics demand Groth16 verification, which requires BN254 pairings, which constrains the outer proof system. The verifier's economics shape the prover's cryptography. The audience's ticket price dictates the magician's technique.

**Layer 7 forces Layer 5.** STARK-to-SNARK wrapping exists because Ethereum's gas costs make raw STARK verification uneconomical. The verification layer forces a compression step the proof system layer would not otherwise need.

**Layer 2 constrains Layer 4.** Cairo was designed so that its ISA minimizes arithmetization cost. The language was shaped by the constraint system, not the other way around. Layer 4 requirements propagated upward to shape Layer 2 design. The choreography was rewritten to fit the stage machinery.

**Layer 3 collapses into Layer 4.** In Jolt, witness generation *is* the arithmetization -- every instruction is decomposed into lookups on subtables. There is no meaningful boundary between "generate the trace" and "encode the computation."

The pedagogical ordering (Layer 1 first, Layer 7 last) follows the *data flow*: setup before language, language before witness, witness before proof. This is how a user encounters the system. But the *engineering causality* is inverted: the field choice at Layer 6 determines the commitment scheme, which determines the polynomial representation, which determines the arithmetization, which shapes everything above it.

These four examples are not anomalies. They are the norm. Once every causal arrow is cataloged, the picture that emerges is not a tower but a web -- and the web has a specific mathematical structure worth naming precisely.

### The Shape of the Web

Roger Penrose, in *The Road to Reality*, draws a distinction between structures that are merely complicated and structures that are *irreducibly entangled*. A stack is complicated: many parts, one ordering. A DAG is entangled: many parts, many orderings, no cycles. The seven-layer model, once you draw all the arrows, is a DAG with at least fourteen directed edges and zero cycles. It has structure, but that structure is not linear.

Consider the full edge set. Layer 6 forces Layer 5 (field choice determines commitment scheme). Layer 5 forces Layer 4 (commitment scheme shapes arithmetization). Layer 4 shapes Layer 3 (constraint format determines witness layout). Layer 3 shapes Layer 2 (witness cost influences ISA design). Layer 2 shapes Layer 1 (ISA scope determines setup complexity). That is the upward chain -- six edges, roughly linear, roughly matching the pedagogical ordering. If this were all, the stack metaphor would suffice.

But it is not all. Layer 7 forces Layer 6 (gas economics demand BN254). Layer 7 forces Layer 5 (verification cost forces wrapping). Layer 4 forces Layer 2 (constraint cost shapes ISA, as Cairo demonstrates). Layer 3 collapses into Layer 4 (Jolt's lookup singularity). Layer 6 forces Layer 7 (field size determines proof size, which determines verification cost). Layer 1 forces Layer 5 (setup type constrains which proof systems are available). Layer 5 forces Layer 7 (proof format determines verifier contract design). Layer 2 forces Layer 3 (ISA instruction count determines trace width).

That is fourteen edges among seven nodes. The graph has no cycles -- no node reaches itself by following arrows -- which is what makes it a DAG rather than a general directed graph. But the graph has *width*: multiple independent paths connect the same pair of nodes. Layer 6 reaches Layer 7 both directly (field determines proof size) and indirectly via Layer 5 (field determines proof system, which determines verifier). Layer 7 reaches Layer 5 both directly (gas cost forces wrapping) and indirectly via Layer 6 (gas cost forces BN254, which constrains proof system). These parallel paths are why changing a single parameter -- say, the base field -- propagates unpredictably through the stack. The change follows multiple routes, and those routes interfere with each other.

Penrose would recognize this as a feature, not a bug. Physical theories have the same structure: general relativity and quantum mechanics are not stacked but entangled, each constraining the other through multiple channels. The seven layers of zero-knowledge proofs exhibit the same irreducible entanglement. Layer 5 (the proof system) cannot be understood without simultaneously understanding Layer 6 (the field) and Layer 7 (the verifier). Layer 2 (the ISA) cannot be designed without understanding Layer 4 (the constraint system). The system is not modular. It is coherent -- every layer reaches every other layer through a small number of hops, and the short path-length is what makes local changes non-local.

### Why No Cycles?

The absence of cycles is not obvious and deserves explanation. Why can arrows not be followed from Layer 7 back to Layer 7?

Because the arrows represent *design-time constraints*, not *runtime data flow*. At runtime, data flows in a rough circle: the user submits a transaction (Layer 2), which generates a witness (Layer 3), which is arithmetized (Layer 4), which is proved (Layer 5), which is verified (Layer 7), which triggers a state change that enables the next transaction (back to Layer 2). That loop is a cycle, and it is real. But the *design* constraints -- which architectural choices force which other architectural choices -- are acyclic. Choosing M31 at Layer 6 forces Circle STARKs at Layer 5, but choosing Circle STARKs at Layer 5 does not force M31 at Layer 6 (any Mersenne prime could do). The arrows are asymmetric. The forcing goes one way.

This distinction -- cyclic runtime flow, acyclic design constraints -- explains why the seven-layer model is useful despite being wrong. The model captures the design-time DAG by projecting it onto a linear ordering. The projection loses information (it hides the downward and cross-cutting arrows) but preserves the acyclicity. A stack is the simplest DAG. The seven-layer stack is the simplest correct projection of the seven-layer web. It is a useful lie that points toward a more interesting truth.

A seven-layer model that acknowledges this bidirectionality is more accurate than one that implies simple top-down dependency. The layers are aspects of a single integrated system, not modules with clean interfaces. The magician, the stage, and the audience are not separable. They are one show.


## Summary

The seven-layer model is not a stack but a DAG with 14 directed design-time edges — six forming the upward chain and eight representing downward and cross-cutting pressures that the pedagogical ordering hides. The absence of cycles is explained by the distinction between design-time constraints (acyclic, asymmetric) and runtime data flow (cyclic), and this structure accounts for why parameter changes propagate unpredictably through the system via multiple independent paths.

## Key claims

- The most consequential upward chain: Layer 6 (small fields) → Layer 5 (Circle STARKs) → Layer 4 (lookup/AIR) → Layer 3 (shard-based witness) → Layer 2 (RISC-V ISAs) → Layer 1 (zkVM amortization).
- Four key downward pressures: Layer 7 → Layer 6 (Ethereum gas forces BN254); Layer 7 → Layer 5 (gas forces STARK-to-SNARK wrapping); Layer 4 → Layer 2 (Cairo ISA shaped by constraint cost); Layer 3 collapses into Layer 4 (Jolt's lookup singularity).
- Full edge count: 14 directed edges among 7 nodes, no cycles — a DAG with width.
- Layer 6 reaches Layer 7 via two independent paths (direct: field determines proof size; indirect via Layer 5: field → proof system → verifier contract).
- The absence of cycles arises because design-time constraints are asymmetric: choosing M31 forces Circle STARKs, but choosing Circle STARKs does not force M31.
- Runtime data flow is cyclic (user → witness → arithmetization → proof → verification → next transaction) but design-time constraints are acyclic.
- A seven-layer stack is the simplest correct projection of the seven-layer DAG: it loses the downward arrows but preserves acyclicity.
- Every layer is connected to every other layer through at most two hops.

## Entities

- [[babybear]]
- [[bn254]]
- [[circle stark]]
- [[jolt]]
- [[mersenne]]
- [[small-field]]
- [[starks]]

## Dependencies

- [[ch10-the-map-redrawn]] — the diagram that this section elaborates in prose
- [[ch07-the-cascade-effect]] — earlier treatment of field-to-commitment-to-proof causality
- [[ch05-layer-4-arithmetization]] — Layer 4 behavior referenced in edge catalogue
- [[ch04-memory-the-binding-constraint]] — Layer 3 behavior and Jolt fusion context

## Sources cited

- Penrose, Roger — *The Road to Reality* (distinction between complicated and irreducibly entangled structures)

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P3] B Penrose reference (*The Road to Reality*) paraphrases a distinction without a page number or chapter reference, making it unverifiable. Low priority given it is used illustratively, not as a technical claim.

## Links

- Up: [[10-the-synthesis-three-paths-not-two]]
- Prev: [[ch10-the-three-path-table]]
- Next: [[ch10-trust-decomposition-seven-weaker-assumptions]]
