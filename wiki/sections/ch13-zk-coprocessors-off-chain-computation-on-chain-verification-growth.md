---
title: "ZK Coprocessors: Off-Chain Computation, On-Chain Verification (Growth)"
slug: ch13-zk-coprocessors-off-chain-computation-on-chain-verification-growth
chapter: 13
chapter_title: "The Market Landscape"
heading_level: 2
source_lines: [5006, 5023]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 535
---

## ZK Coprocessors: Off-Chain Computation, On-Chain Verification (Growth)

ZK coprocessors represent a category that the original seven-layer framework entirely missed -- and the trust dynamics are subtle enough to deserve careful attention. A coprocessor allows a smart contract to verifiably read and compute over historical blockchain data without the gas cost of executing that computation on-chain. The contract sends a query; the coprocessor executes it off-chain, generates a ZK proof of correct execution, and returns the result with the proof for on-chain verification.

The magician, in this case, is not performing for a general audience. She is performing for a smart contract -- an audience that cannot reason, only verify. The proof guarantees that the computation was done correctly. But the computation happened somewhere: on specific hardware, operated by a specific entity, with access to the query inputs. Trust has not been eliminated. It has been moved off-chain.

**Axiom** raised $20 million in Series A funding and operates the leading ZK coprocessor platform. Axiom's coprocessor can access any historical Ethereum block header, account state, storage slot, transaction, or receipt, generate a computation over that data, and deliver a verified result to a smart contract in a single callback.

**Brevis** operates both a ZK coprocessor and the Pico Prism zkVM. Brevis's ProverNet launched mainnet beta in December 2025, enabling decentralized proof generation for coprocessor queries.

**Lagrange** provides ZK coprocessing for cross-chain state proofs and data availability verification, enabling smart contracts on one chain to verify state claims about another chain without trusting a bridge operator.

To make this concrete: consider a DeFi lending protocol that needs to know a user's 30-day average balance on Ethereum before approving a loan on Arbitrum. Without a coprocessor, the protocol either trusts an oracle (centralized, manipulable) or requires the user to submit the data manually (slow, unverifiable). With a ZK coprocessor, the protocol sends a query: "compute the time-weighted average of account 0x... across blocks 19,000,000-19,200,000." The coprocessor reads the historical state from an Ethereum archive node, performs the computation off-chain, generates a ZK proof that the computation was faithful to the actual on-chain data, and returns the result with the proof. The lending contract verifies the proof on-chain (a few hundred thousand gas) and approves the loan. The entire process replaces a trust assumption ("the oracle is honest") with a mathematical guarantee ("the computation was correct"), at a cost of roughly $0.10-$1.00 per query.

The coprocessor market matters because it extends ZK proofs beyond transaction execution into data analytics. A DeFi protocol can use a coprocessor to compute time-weighted average prices over 30 days of on-chain data, prove the computation is correct, and use the result in a lending decision -- all without trusting an oracle. The sealed certificate now covers not just "the computation was correct" but "the data was real." That is a genuine advance. But who watches the prover's hardware? The proof says the computation was faithful. It does not say the machine was honest about what it was asked to compute. The trust has shifted, not vanished.

**Trust relocated from:** on-chain computation (expensive, public) **to:** off-chain proving (cheap, private) + data availability assumptions. **Net:** cost reduction with new trust in prover correctness and DA layer.


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
