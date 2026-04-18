---
title: ""Trustless" versus "Trust-Minimized""
slug: ch10-trustless-versus-trust-minimized
chapter: 10
chapter_title: "The Synthesis -- Three Paths, Not Two"
heading_level: 2
source_lines: [4529, 4544]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 307
---

## "Trustless" versus "Trust-Minimized"

The analysis concludes with a question that should be printed on the wall of every ZK team's office:

> If zero-knowledge proofs provide "trustless" computation, but the setup requires trusting ceremony participants (Layer 1), the program requires trusting the developer not to make constraint errors (Layer 2), the witness requires trusting the hardware not to leak side channels (Layer 3), the proof system requires trusting that mathematical hardness assumptions hold (Layer 6), and the verifier requires trusting that governance will not override the math (Layer 7) -- then where, exactly, is the "trustless" part?

The answer: nowhere. "Trustless" is a word that flatters the technology and misleads the user. Zero-knowledge proofs do not eliminate trust. They minimize and distribute it. Instead of trusting one bank with your financial data, you trust that: (a) at least one ceremony participant was honest, (b) the circuit was correctly written and audited, (c) the hardware is not leaking, (d) discrete logarithms are hard, and (e) the governance multisig will not go rogue.

Each of these is a weaker assumption than trusting a single entity. The combination is far more resilient than any single point of trust. But they are assumptions nonetheless, and a responsible guide to zero-knowledge proofs should catalog them explicitly.

We stated this thesis in the opening pages of Chapter 1: trust decomposition, not trust elimination. Ten chapters later, the decomposition is precise. Seven assumptions instead of one. Fourteen causal edges instead of a monolith. Three architectural paths, each with different failure profiles. The word "trustless" obscures every one of these distinctions. The word "trust-minimized" preserves them.

The remaining chapters of this book will use "trust-minimized" rather than "trustless." Not because it sounds better -- it sounds worse, deliberately -- but because it is accurate. And accuracy in naming things is where understanding begins.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
