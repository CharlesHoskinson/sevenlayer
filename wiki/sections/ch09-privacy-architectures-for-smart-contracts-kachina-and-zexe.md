---
title: "Privacy Architectures for Smart Contracts: Kachina and Zexe"
slug: ch09-privacy-architectures-for-smart-contracts-kachina-and-zexe
chapter: 9
chapter_title: "Privacy-Enhancing Technologies"
heading_level: 2
source_lines: [4202, 4243]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 741
---

## Privacy Architectures for Smart Contracts: Kachina and Zexe

Two academic systems -- Kachina and Zexe -- represent the theoretical foundations for how private smart contracts can be deployed on blockchains. They take complementary approaches, and understanding both illuminates the design space that every privacy-focused blockchain must work within.

### Kachina: Privacy as a Parameter

Kachina, developed by Kerber, Kiayias, and Kohlweiss at the University of Edinburgh and IOHK, provides a UC-secure (universally composable) framework for privacy-preserving smart contracts. Its key innovation is treating privacy as a *parameter*, not a binary choice. Think of it as a dimmer switch rather than an on/off toggle.

Contract state is split into *shared public* state (on-chain) and *individual private* state (per party, off-chain). Users prove in zero knowledge that their state transitions are valid given some private state and input. The critical architectural insight is the *state oracle transcript*: instead of proving full state transitions (which would require locking shared state), users capture oracle queries and responses as partial transcripts. These transcripts are partial functions over state, enabling concurrent transactions to succeed even when state changes between proof creation and proof submission.

The privacy leakage is formally captured by a *leakage function* Lambda that specifies exactly what information each transaction reveals. Lambda can be tuned from "full leakage" (equivalent to Ethereum, where everything is visible) to "near-zero leakage" (equivalent to Zerocash, where only nullifiers and commitments are visible). This parameterization means the same framework can model both transparent and private contracts, and everything in between. The magician decides, contract by contract, how much of the trick to reveal.

Proving complexity is $O(|T_\rho| + |T_\sigma|)$ -- proportional to the *transcript lengths*, not the full state size. This matters for scalability: a contract with millions of state entries can support private transactions that only touch a few entries, and the proving cost reflects only the entries accessed.

### Zexe: Function Privacy

Zexe, developed by Bowe, Chiesa, Green, Miers, Mishra, and Wu (2018), takes a UTXO-based approach with a stronger privacy guarantee: not only are the transaction data hidden, but the *function being computed* is hidden as well. An observer cannot distinguish a token transfer from a governance vote from a swap -- all transactions look identical on-chain. The audience sees identical envelopes. Every envelope looks the same. The contents are unknowable.

The architecture uses a "records nano-kernel" (RNK) -- a minimalist shared execution environment where records have birth and death predicates. Transactions consume old records and create new ones by satisfying these predicates in zero knowledge. The on-chain footprint is constant: 968 bytes for a 2-input/2-output transaction, regardless of the complexity of the off-chain computation.

Zexe uses recursive proof composition (bounded depth 2, not full recursion) with a BLS-12 curve for inner SNARKs and a Cocks-Pinch curve for outer composition. Proof generation takes roughly one minute plus computation-dependent time. Verification takes tens of milliseconds.

### Comparison

| Property | Kachina | Zexe |
|----------|---------|------|
| State model | Account-based (state machine) | UTXO-based (records) |
| Data privacy | Parameterizable (Lambda function) | Full |
| Function privacy | No (function identity visible) | Yes (all transactions indistinguishable) |
| Concurrency | State oracle transcripts | UTXO model (naturally concurrent) |
| On-chain cost | $O(\text{transcript length})$ | Constant (968 bytes) |
| Proving cost | $O(\text{transcript length})$ | ~1 minute + computation |
| Security model | UC-secure ($\mathcal{F}_\text{nizk}$, $\mathcal{G}_\text{ledger}$ hybrid) | Simulation-based |

Midnight's architecture follows the Kachina model most closely -- parameterizable disclosure via `disclose()`, account-based state, and compiler-enforced privacy boundaries. The `disclose()` mechanism from Chapter 3 is the practical instantiation of Kachina's information-flow control: the compiler traces every data-flow path from private witness to public surface and rejects programs that leak without explicit consent. This makes Midnight one of the few deployed systems where the PET composition (ZKP for transaction privacy, with architectural room for MPC extensions) is grounded in the formal model rather than bolted on after the fact.

Aztec's design follows the Zexe model more closely -- UTXO-based notes, client-side proving, and a Private Execution Environment (PXE) that handles proof generation.

For the system architect choosing between these approaches, the key question is: do you need function privacy? If yes (all transactions must be indistinguishable), the Zexe/UTXO model is the natural choice. If no (you can tolerate revealing which function was called, as long as the arguments are private), the Kachina/account model offers simpler programming and easier state management.

---


## Summary

Contrasts Kachina (UC-secure, account-based, parameterisable leakage via Lambda function) and Zexe (UTXO-based, full function privacy, constant 968-byte on-chain footprint) as the two theoretical foundations for private smart contracts. Midnight follows the Kachina model most closely; Aztec follows Zexe.

## Key claims

- Kachina splits state into shared public (on-chain) and individual private (off-chain); proving complexity is O(|transcript|), not O(full state).
- Kachina leakage function Lambda is tunable from full transparency (Ethereum-equivalent) to near-zero leakage (Zerocash-equivalent).
- Zexe on-chain footprint is constant: 968 bytes for a 2-input/2-output transaction regardless of off-chain computation complexity.
- Zexe uses recursive proof composition (bounded depth 2) with BLS-12 inner SNARKs and a Cocks-Pinch curve for outer composition.
- Zexe proof generation: ~1 minute + computation-dependent time; verification: tens of milliseconds.
- Midnight's `disclose()` mechanism is the practical instantiation of Kachina's information-flow control.
- Aztec's Private Execution Environment (PXE) handles client-side proving in the Zexe/UTXO model.
- Design decision: need function privacy (all txs indistinguishable) → Zexe/UTXO; tolerating visible function identity → Kachina/account.

## Entities

- [[midnight]]
- [[mpc]]
- [[nova]]
- [[utxo]]

## Dependencies

- [[ch03-the-disclose-boundary-midnight-s-witness-architecture]] — Midnight's `disclose()` as Kachina instantiation
- [[ch09-composability-when-one-pet-is-not-enough]] — ZKP+MPC composition context
- [[ch09-the-four-pillars]] — ZKPs as underlying PET for both systems
- [[ch04-the-disclose-boundary-midnight-s-witness-architecture]] — witness architecture detail

## Sources cited

- Kerber, T., Kiayias, A., Kohlweiss, M. Kachina: Foundations of Private Smart Contracts. University of Edinburgh / IOHK.
- Bowe, S., Chiesa, A., Green, M., Miers, I., Mishra, P., Wu, H. Zexe: Enabling Decentralized Private Computation. 2018.

## Open questions

None flagged by this section.

## Improvement notes

- [P1] (B) Zexe cited as "(2018)" in prose and Sources cited — this is the ePrint date; the published venue is IEEE S&P 2020 (confirmed by ch06 bibliography). Should read "Bowe et al. IEEE S&P 2020" or at minimum note the ePrint vs. publication distinction.
- [P1] (A) "BLS-12 curve for inner SNARKs" is ambiguous — Zexe uses BLS12-377 for inner proofs; "BLS-12" does not identify a specific curve and could be confused with BLS12-381.
- [P2] (B) Dependencies lists both `[[ch03-the-disclose-boundary-midnight-s-witness-architecture]]` and `[[ch04-the-disclose-boundary-midnight-s-witness-architecture]]` for the same conceptual section — duplicate or stale link that should be resolved to the correct slug.
- [P3] (B) Kachina affiliation "University of Edinburgh and IOHK" — the bibliography entry (IEEE CSF 2021) does not list an affiliation; worth verifying that all three authors were at those institutions.

## Links

- Up: [[09-privacy-enhancing-technologies]]
- Prev: [[ch09-real-world-deployments-five-case-studies]]
- Next: [[ch09-the-regulatory-intersection]]
