---
title: "Option-Value Analysis"
slug: ch02-option-value-analysis
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [708, 732]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 598
---

## Option-Value Analysis

The economic analysis of Layer 1 has one more dimension, borrowed from financial options theory: *option value*.

In finance, an option is the right -- but not the obligation -- to take an action at a future date. You pay a premium today for the flexibility to act later. The premium is the option's cost. The flexibility is its value. The concept applies directly to setup choices.

A trusted setup on BLS12-381 buys performance today but forecloses certain futures. When -- not if -- post-quantum migration becomes necessary, every system on BLS12-381 will need a new setup. New ceremony. New coordination. New toxic waste. If the system has accumulated ten years of state and ten million users, the migration cost is not just the $2-5 million of the ceremony. It is the coordination cost of upgrading every node, every contract, every verifier key -- a cost that grows with every year the system has been running.

A transparent setup on hash-based primitives costs more per proof today but preserves the option to migrate without re-ceremony. The hash function can be swapped. The security parameters can be adjusted. No toxic waste needs to be re-destroyed because none was ever created. The transparent setup is the option premium. The post-quantum flexibility is the option value.

What is this option worth? The calculation is sensitive to assumptions, so consider three scenarios:

| Scenario | Quantum probability (15yr) | Migration cost | Expected cost of trusted path | Break-even premium |
|---|---|---|---|---|
| Optimistic | 10% | $50M | $5M | ~$500K/yr for 10 years |
| Base case | 30% | $50M | $15M | ~$1.5M/yr for 10 years |
| Cautious | 50% | $50M | $25M | ~$2.5M/yr for 10 years |

At the base case -- a 30% probability that cryptographically relevant quantum computers arrive within 15 years -- the expected cost of the trusted-setup path is $15 million. That is a real liability sitting on the balance sheet of every system built on BLS12-381 or BN254 today. Compare that to the annual cost premium of transparent proofs (perhaps $3-4 million more per year in on-chain verification, shrinking as STARKs get cheaper). Even in the base case, the option is expensive enough to take seriously. In the cautious case, it dominates.

There is also the "Harvest Now, Decrypt Later" threat, and it may be the most urgent variant of the quantum risk. Adversaries who record the public SRS today do not need a quantum computer now. They need one *eventually*. Intelligence agencies routinely archive encrypted communications for future decryption -- the NSA's upstream collection programs, disclosed in 2013, were built on exactly this logic. Are they recording SRS parameters? The Federal Reserve's FEDS 2025-093 working paper on quantum threats to financial infrastructure takes this possibility seriously enough to recommend that systems with 10+ year lifespans use post-quantum or post-quantum-ready primitives. For a privacy blockchain whose users chose it specifically to protect sensitive data, the HNDL threat means that today's shielded transactions could become tomorrow's open records -- not because the cryptography was broken in real time, but because it was archived and broken later.

The answer depends on your estimate of the quantum timeline. If you believe cryptographically relevant quantum computers are 20+ years away, the option has low present value, and the performance advantage of pairing-based setups dominates. If you believe the timeline is 10-15 years -- consistent with NIST's 2035 deprecation target -- the option is substantial. Transparent setups satisfy the Federal Reserve's criterion by default. Trusted setups on pairing-friendly curves do not.



## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
