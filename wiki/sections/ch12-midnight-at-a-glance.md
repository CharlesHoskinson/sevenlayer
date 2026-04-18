---
title: "Midnight at a Glance"
slug: ch12-midnight-at-a-glance
chapter: 12
chapter_title: "Midnight -- The Privacy Theater"
heading_level: 2
source_lines: [4778, 4792]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
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

Midnight is a Cardano sidechain running privacy-preserving smart contracts in Compact, a TypeScript-inspired DSL. The `compactc` compiler produces three artifacts from one source file -- ZKIR circuits, TypeScript bindings, and key pairs -- reflecting the split between provable logic, private witnesses, and cryptographic infrastructure. Its three-token model (NIGHT, DUST, custom tokens) separates governance, fees, and application value with per-UTXO shielding choice.

## Key claims

- Midnight is a Cardano sidechain; smart contracts are written in Compact (TypeScript-inspired DSL).
- `compactc` compiles a single `.compact` file to three artifacts: ZKIR circuit JSON, TypeScript API bindings, and proving/verifier key pairs.
- The local proof server runs at `localhost:6300`.
- NIGHT is the governance/staking token; always unshielded.
- DUST is the fee token; public/unshielded; generated from staking NIGHT over time.
- Custom tokens can be shielded (ZK proofs + nullifiers) or unshielded (BIP-340 Schnorr), chosen per UTXO.

## Entities

- [[midnight]]
- [[sdk]]
- [[utxo]]

## Dependencies

- [[ch03-compact-s-disclosure-analysis]] — Compact language design and disclosure analysis
- [[ch05-midnight-s-zkir-a-concrete-layer-4]] — ZKIR instruction set detail
- [[ch08-case-study-midnight-and-the-three-token-architecture]] — Three-token model analysed at Layer 7

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [P2] (B) `localhost:6300` and per-UTXO shielding/unshielded token claims are stated as fact with no source citation; add references to Wallet SDK or Developer Guide.
- [P3] (C) The pipeline ASCII diagram labels are clean, but the prose phrase "This three-part output reflects the fundamental architecture" edges toward boilerplate framing — tighten.

## Links

- Up: [[12-midnight-the-privacy-theater]]
- Prev: [[ch12-midnight-as-test-case]]
- Next: [[ch12-full-seven-layer-mapping]]
