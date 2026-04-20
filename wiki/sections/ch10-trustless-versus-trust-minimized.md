---
title: ""Trustless" versus "Trust-Minimized""
slug: ch10-trustless-versus-trust-minimized
chapter: 10
chapter_title: "The Synthesis -- Three Paths, Not Two"
heading_level: 2
source_lines: [4548, 4563]
source_commit: 402f8a6c81370d3fe1e3caa98dda3cd8f4078e71
status: reviewed
word_count: 307
---

## "Trustless" versus "Trust-Minimized"

The analysis concludes with a question that should be printed on the wall of every ZK team's office:

> If zero-knowledge proofs provide "trustless" computation, but the setup requires trusting ceremony participants (Layer 1), the program requires trusting the developer not to make constraint errors (Layer 2), the witness requires trusting the hardware not to leak side channels (Layer 3), the arithmetization requires trusting the translation from program to polynomial constraints (Layer 4), the proof system requires trusting Fiat-Shamir soundness and correct implementation (Layer 5), the primitives require trusting that mathematical hardness assumptions hold (Layer 6), and the verifier requires trusting that governance will not override the math (Layer 7) -- then where, exactly, is the "trustless" part?

The answer: nowhere. "Trustless" is a word that flatters the technology and misleads the user. Zero-knowledge proofs do not eliminate trust. They minimize and distribute it. Instead of trusting one bank with your financial data, you trust that: (a) at least one ceremony participant was honest; (b) the circuit was correctly written and audited; (c) the hardware is not leaking; (d) the arithmetization faithfully encodes the intended computation; (e) the proof system is sound and its Fiat-Shamir transform is correctly implemented; (f) discrete logarithms (or lattice problems, or hash preimages) are hard; and (g) the governance multisig will not go rogue.

Each is a weaker assumption than trusting a single entity. The combination is far more resilient than any single point of trust. But they are assumptions nonetheless, and a responsible guide to zero-knowledge proofs should catalog them explicitly.

We stated this thesis in the opening pages of Chapter 1: trust decomposition, not trust elimination. Ten chapters later, the decomposition is precise. Seven assumptions instead of one. Fourteen causal edges instead of a monolith. Three architectural paths, each with different failure profiles. The word "trustless" obscures every one of these distinctions. The word "trust-minimized" preserves them.

The remaining chapters of this book will use "trust-minimized" rather than "trustless." Not because it sounds better -- it sounds worse, deliberately -- but because it is accurate. And accuracy in naming things is where understanding begins.

---


## Summary

The word "trustless" is inaccurate: ZK proofs still require trust in ceremony participants, circuit correctness, hardware side-channel resistance, mathematical hardness, and governance behavior — they minimize and distribute trust rather than eliminate it. From Chapter 11 onward this book uses "trust-minimized" instead of "trustless," not because it sounds better but because it is accurate, and naming things accurately is where understanding begins.

## Key claims

- "Trustless" flatters the technology and misleads users; ZK proofs have at least five residual trust assumptions (ceremony, circuit, hardware, math, governance).
- Trust decomposition replaces one monolithic trust point with seven weaker, independently auditable, independently replaceable assumptions.
- The thesis stated in Chapter 1 ("trust decomposition, not trust elimination") is now confirmed with full precision: seven assumptions, 14 causal edges, three architectural paths.
- From Chapter 11 onward: "trust-minimized" replaces "trustless" in this book's vocabulary.

## Entities

- [[ceremony]]

## Dependencies

- [[ch01-the-deepest-question]] — original trust decomposition thesis stated here
- [[ch10-trust-decomposition-seven-weaker-assumptions]] — the seven assumptions whose existence this section summarizes

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

## Links

- Up: [[10-the-synthesis-three-paths-not-two]]
- Prev: [[ch10-trust-decomposition-seven-weaker-assumptions]]
- Next: —
