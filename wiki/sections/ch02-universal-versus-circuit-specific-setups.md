---
title: "Universal versus Circuit-Specific Setups"
slug: ch02-universal-versus-circuit-specific-setups
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [617, 631]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 511
---

## Universal versus Circuit-Specific Setups

The BCTV14 bug revealed that the SRS construction must be correct independently of the ceremony. But there is a second dimension to setup design that the bug also illuminates: the Sprout-era system required a ceremony for every new circuit. Change the program, run a new ceremony. This constraint shaped an entire generation of systems -- and breaking free of it required a different kind of SRS entirely.

Groth16 [Groth, 2016] produces the most compact proofs ever constructed: exactly 192 bytes, three group elements, verified with three pairing operations (recall: a pairing is a function that takes two curve points and checks algebraic relationships between them without revealing the secrets behind them). No other system comes close. But Groth16's setup is circuit-specific. The SRS encodes the structure of a particular circuit: the specific polynomial constraints, the wiring, the gates. Change the circuit -- add a feature, fix a bug, upgrade the protocol -- and you need a new ceremony. New coordination. New participants. New toxic waste to destroy. At $2-5 million per ceremony, this is unsustainable for any system that evolves.

PLONK [Gabizon, Williamson, Ciobotaru, 2019] and Marlin [Chiesa et al., 2019] solved this by making the SRS *universal*. Instead of encoding a specific circuit's structure, the universal SRS encodes the raw mathematical material (powers of a secret on an elliptic curve) that any circuit can use. Any circuit up to a maximum size -- whether it verifies a token transfer, a compliance check, or an entire Ethereum block -- can derive its proving keys from the same SRS. The per-circuit derivation is entirely *deterministic and public*: same source code plus same compiler yields same keys. No new secrets. No new ceremony. No new toxic waste. The ceremony is the capital expenditure. Everything after it is operating expense.

The universal model transformed the economics of zero-knowledge deployments. But describing it in the abstract only goes so far. To see how the capex/opex distinction plays out in practice -- how a real system chooses its curve, runs its ceremony, derives its per-circuit keys, and lives with the consequences -- we need a concrete example. The Sudoku puzzle from Chapter 1 will carry us through the mathematical layers. For the architectural layers -- setup, deployment, quantum exposure -- we need a production system that made these choices for real.

Midnight adopted the universal model. Midnight uses a PLONK-family proof system (a variant of Halo2) with a universal SRS on BLS12-381. The Compact compiler takes each smart contract, compiles it to a circuit intermediate representation called ZKIR, and derives per-circuit proving and verification keys from the universal SRS. One ceremony serves all contracts. The per-contract compilation runs in seconds and requires no trust beyond the original ceremony. Midnight's full Layer 1 architecture is analyzed in detail below.

The capex/opex distinction introduced above applies with full force: every new contract, every bug fix, every protocol upgrade deploys under the same SRS. The marginal cost of adding a new application to the ecosystem converges to the cost of compilation -- effectively zero.



## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
