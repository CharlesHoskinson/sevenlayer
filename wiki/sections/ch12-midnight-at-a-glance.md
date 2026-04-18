---
title: "Midnight at a Glance"
slug: ch12-midnight-at-a-glance
chapter: 12
chapter_title: "Midnight -- The Privacy Theater"
heading_level: 2
source_lines: [4776, 4790]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 178
---

## Midnight at a Glance

Midnight is a Cardano sidechain that executes privacy-preserving smart contracts written in **Compact**, a TypeScript-inspired domain-specific language. The architecture follows a pipeline:

```
Compact source --> compactc compiler --> ZKIR circuits + TypeScript bindings + proving keys
                                              |                    |                |
                                         Proof server         DApp frontend    On-chain verifier
                                        (localhost:6300)      (browser/node)   (blockchain node)
```

The compiler produces three artifacts from a single `.compact` file: ZKIR circuit descriptions in JSON, TypeScript API bindings for the DApp frontend, and cryptographic proving/verifier key pairs. This three-part output reflects the fundamental architecture of privacy-preserving computation: what can be proven (ZKIR), what runs privately (TypeScript witnesses), and what makes proofs possible (keys).

Midnight's token model has three layers. **NIGHT** is the governance and staking token, always unshielded (transparent). **DUST** is the fee token, a public (unshielded) token per the wallet SDK, generated from staking NIGHT over time, with a balance computed from generation parameters. **Custom tokens** can be either shielded (encrypted, spent via ZK proofs and nullifiers) or unshielded (transparent, spent via BIP-340 Schnorr signatures), at the developer's choice per UTXO.


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
