---
title: "Option-Value Analysis"
slug: ch02-option-value-analysis
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [698, 722]
source_commit: b3ed881318761d3fd0e65ead7ea58e3f6536ccf9
status: reviewed
word_count: 598
---

## Option-Value Analysis

The economic analysis of Layer 1 has one more dimension, borrowed from financial options theory: *option value*.

In finance, an option is the right -- but not the obligation -- to take an action at a future date. You pay a premium today for the flexibility to act later. The premium is the option's cost. The flexibility is its value. The concept applies directly to setup choices.

A trusted setup on BLS12-381 buys performance today but forecloses certain futures. When -- not if -- post-quantum migration becomes necessary, every system on BLS12-381 will need a new setup. New ceremony. New coordination. New toxic waste. If the system has accumulated ten years of state and ten million users, the migration cost is not just the ceremony. It is the coordination cost of upgrading every node, every contract, every verifier key, plus wallet migration for every user -- a cost that grows with every year the system has been running.

A transparent setup on hash-based primitives costs more per proof today but preserves the option to migrate without re-ceremony. The hash function can be swapped. The security parameters can be adjusted. No toxic waste needs to be re-destroyed because none was ever created. The transparent setup is the option premium. The post-quantum flexibility is the option value.

What is this option worth? The calculation is sensitive to assumptions, so consider three scenarios. The migration-cost column below is an *illustrative order-of-magnitude* figure -- the aggregate of a new ceremony, node and contract upgrades, wallet migration across a ten-year-old chain, and the forked-state transition period. It is meant to anchor the arithmetic, not to substitute for a project-specific cost model.

| Scenario | Quantum probability (15yr) | Illustrative migration cost | Expected cost of trusted path | Break-even premium |
|---|---|---|---|---|
| Optimistic | 10% | $50M | $5M | ~$500K/yr for 10 years |
| Base case | 30% | $50M | $15M | ~$1.5M/yr for 10 years |
| Cautious | 50% | $50M | $25M | ~$2.5M/yr for 10 years |

At the base case -- a 30% probability that cryptographically relevant quantum computers arrive within 15 years -- the expected cost of the trusted-setup path is $15 million. That is a real liability sitting on the balance sheet of every system built on BLS12-381 or BN254 today. Compare that to the annual cost premium of transparent proofs (perhaps $3-4 million more per year in on-chain verification, shrinking as STARKs get cheaper). Even in the base case, the option is expensive enough to take seriously. In the cautious case, it dominates.

There is also the "Harvest Now, Decrypt Later" threat. For systems with 10+ year lifespans, it may be the most pressing near-term exposure -- not because a quantum computer exists today, but because adversaries can archive public parameters now and decrypt later. Adversaries who record the public SRS today do not need a quantum computer now. They need one *eventually*. Intelligence agencies routinely archive encrypted communications for future decryption -- the NSA's upstream collection programs, disclosed through Snowden documents in 2013 (reported by Barton Gellman and Laura Poitras, *Washington Post*, June 2013), were built on exactly this logic. Are they recording SRS parameters? The Federal Reserve's FEDS working paper on post-quantum risk for distributed ledger networks takes this possibility seriously enough to recommend that systems with 10+ year lifespans use post-quantum or post-quantum-ready primitives [Mascelli, Rodden, "'Harvest Now Decrypt Later': Examining Post-Quantum Cryptography and the Data Privacy Risks for Distributed Ledger Networks," FEDS 2025-093, Federal Reserve Board, 2025; https://www.federalreserve.gov/econres/feds/harvest-now-decrypt-later-examining-post-quantum-cryptography-and-the-data-privacy-risks-for-distributed-ledger-networks.htm]. For a privacy blockchain whose users chose it specifically to protect sensitive data, HNDL means that today's shielded transactions could become tomorrow's open records -- not because the cryptography was broken in real time, but because it was archived and broken later.

The answer depends on your estimate of the quantum timeline. If you believe cryptographically relevant quantum computers are 20+ years away, the option has low present value, and the performance advantage of pairing-based setups dominates. If you believe the timeline is 10-15 years -- consistent with the NIST 2035 migration target and the NSA's CNSA 2.0 transition schedule -- the option is substantial. Transparent setups satisfy the Federal Reserve's criterion by default. Trusted setups on pairing-friendly curves do not.



## Summary

A trusted setup on BLS12-381 or BN254 buys performance today but forecloses post-quantum migration without a new ceremony; a transparent setup pays a per-proof premium but preserves that option. At a 30% probability of cryptographically relevant quantum computers within 15 years (the base case), the expected migration cost is $15M, dominating the annual per-proof premium for most systems. The "Harvest Now, Decrypt Later" threat — adversaries archiving the public SRS for future quantum decryption — may be the most urgent variant, particularly for privacy systems with long-lived secrets.

## Key claims

- Base case (30% quantum probability in 15 years): expected migration cost for trusted-setup path = $15M.
- Optimistic case (10%): $5M expected cost. Cautious case (50%): $25M expected cost.
- Annual on-chain verification premium for transparent vs. trusted: approximately $3–4M/year, shrinking as STARKs get cheaper.
- The Federal Reserve's FEDS 2025-093 working paper recommends post-quantum or PQ-ready primitives for systems with 10+ year lifespans.
- NIST's 2035 deprecation target: systems designed today with 10+ year lifespans should weigh post-quantum migration flexibility against performance.
- "Harvest Now, Decrypt Later": intelligence agencies archive encrypted data for future decryption; NSA upstream collection programs (disclosed 2013) operated on this logic.
- Transparent setups satisfy FEDS 2025-093 by default; trusted setups on pairing-friendly curves do not.

## Entities

- [[bls12-381]]
- [[bn254]]
- [[ceremony]]
- [[fri]]
- [[kzg]]
- [[nist]]
- [[starks]]

## Dependencies

- [[ch02-the-quantum-shelf-life]] — the quantum timeline analysis underlying the option-value calculation
- [[ch02-the-capex-opex-framework]] — the per-proof cost differential that the option premium is weighed against

## Sources cited

- Federal Reserve FEDS 2025-093 (quantum threats to financial infrastructure)
- NSA upstream collection programs (disclosed 2013, cited as precedent for HNDL threat)

## Open questions

- What is the correct probability of cryptographically relevant quantum computers within 15 years? The option-value calculation is highly sensitive to this estimate, and no consensus exists.

## Improvement notes

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [none] (D) No structural contradictions found.
- [P3] (E) The option-value framework does not account for the possibility of SNARK-to-STARK migration without a new ceremony — the hybrid pipeline already uses a transparent inner proof, so a plausible upgrade path exists that the analysis ignores.

## Links

- Up: [[02-building-the-stage]]
- Prev: [[ch02-midnight-s-bls12-381-stage]]
- Next: [[ch02-the-setup-tradeoff]]
