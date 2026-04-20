---
title: "Universal versus Circuit-Specific Setups"
slug: ch02-universal-versus-circuit-specific-setups
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [609, 621]
source_commit: 6e757843ed29aa50ce4558719452a86510ed0d20
status: finalized
word_count: 511
---

## Universal versus Circuit-Specific Setups

The BCTV14 bug revealed that the SRS construction must be correct independently of the ceremony. But there is a second dimension to setup design that the bug also illuminates: the Sprout-era system required a ceremony for every new circuit. Change the program, run a new ceremony. This constraint shaped an entire generation of systems -- and breaking free of it required a different kind of SRS entirely.

Groth16 [Groth, "On the Size of Pairing-Based Non-interactive Arguments," *EUROCRYPT 2016*] produces the most compact proofs ever constructed: exactly 192 bytes, three group elements. Verification requires two pairing checks, each involving two pairing evaluations -- three distinct pairing computations in all, with one argument shared across checks (a pairing is a function that takes two curve points and checks algebraic relationships between them without revealing the secrets behind them). No other system comes close for proof size. But Groth16's setup is circuit-specific. The SRS encodes the structure of a particular circuit: the specific polynomial constraints, the wiring, the gates. Change the circuit -- add a feature, fix a bug, upgrade the protocol -- and you need a new ceremony. New coordination. New participants. New toxic waste to destroy. Each new ceremony carries its own coordination cost, unsustainable for any system that evolves.

The first universal SNARK was Sonic [Maller, Bowe, Kohlweiss, Meiklejohn, "Sonic: Zero-Knowledge SNARKs from Linear-Size Universal and Updatable Structured Reference Strings," *ACM CCS 2019* / IACR ePrint 2019/099], published in early 2019. Sonic introduced the key idea: a single SRS that encodes raw mathematical material any circuit can use, with per-circuit derivation that is public and deterministic. PLONK [Gabizon, Williamson, Ciobotaru, IACR ePrint 2019/953] and Marlin [Chiesa et al., "Marlin: Preprocessing zkSNARKs with Universal and Updatable SRS," *EUROCRYPT 2020* / IACR ePrint 2019/1047], published months later, refined the construction and drove most of the subsequent adoption, but Sonic is the ancestor.

Any circuit up to a maximum size -- whether it verifies a token transfer, a compliance check, or an entire Ethereum block -- can derive its proving keys from the same SRS. The per-circuit derivation is entirely *deterministic and public*: same source code plus same compiler yields same keys. No new secrets. No new ceremony. No new toxic waste. The ceremony is the capital expenditure. Everything after it is operating expense.

The universal model transformed the economics of zero-knowledge deployments. Midnight is the production system this chapter uses as its running case study: it adopted the universal model with a PLONK-family proof system (Halo 2 / UltraPlonk) on BLS12-381. The Compact compiler takes each smart contract, compiles it to a circuit intermediate representation called ZKIR, and derives per-circuit proving and verification keys from the shared SRS. One ceremony serves every contract; the per-contract compilation runs in seconds. Midnight's full Layer 1 architecture is analyzed below.



## Summary

Groth16 produces the most compact proofs ever (192 bytes, three pairings) but requires a new ceremony per circuit — unsustainable for evolving systems. PLONK and Marlin broke this constraint with a universal SRS: one ceremony serves any circuit up to a maximum size, with per-circuit key derivation that is fully deterministic and public. Midnight uses this universal model with a PLONK-family system (Halo2 variant) on BLS12-381, where adding any new contract requires compilation only, no new trust.

## Key claims

- Groth16 setup is circuit-specific: changing any circuit requires a new ceremony at $2–5M per run.
- PLONK (Gabizon, Williamson, Ciobotaru, 2019) and Marlin (Chiesa et al., 2019) introduced universal SRS: one ceremony for any circuit up to a fixed size.
- Per-circuit key derivation from a universal SRS is deterministic and public — no new trust enters.
- Midnight uses a PLONK-family system (Halo2 variant) with a universal SRS on BLS12-381.
- Groth16 proofs are exactly 192 bytes; verification uses three pairing operations.
- Marginal cost of adding a new application to a universal-SRS ecosystem converges to compilation cost — effectively zero.

## Entities

- [[ceremony]]
- [[gabizon]]
- [[groth16]]
- [[halo2]]
- [[midnight]]
- [[plonk]]
- [[sudoku]]

## Dependencies

- [[ch02-the-bug-that-was-not-a-ceremony-failure]] — motivates why circuit-specific ceremonies are a liability when circuits change
- [[ch02-the-capex-opex-framework]] — the capex/opex model that universal setups optimize

## Sources cited

- Groth, 2016 (Groth16)
- Gabizon, Williamson, Ciobotaru, 2019 (PLONK)
- Chiesa et al., 2019 (Marlin)

## Open questions

None flagged by this section.

## Improvement notes

_All P0/P1/P2/P3 findings resolved in Phase 3 revisions (2026-04-18 through 2026-04-20)._

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [none] (D) No contradictions with other chapters found.

## Links

- Up: [[02-building-the-stage]]
- Prev: [[ch02-the-bug-that-was-not-a-ceremony-failure]]
- Next: [[ch02-the-quantum-shelf-life]]
