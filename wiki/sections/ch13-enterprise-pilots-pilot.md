---
title: "Enterprise Pilots (Pilot)"
slug: ch13-enterprise-pilots-pilot
chapter: 13
chapter_title: "The Market Landscape"
heading_level: 2
source_lines: [5102, 5131]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 1416
---

## Enterprise Pilots (Pilot)

The magician has left the theater. She now performs in boardrooms, data centers, and regulatory offices. The trick is the same. The audience has changed -- and this audience does not care about trustlessness. It cares about compliance.

**Deutsche Bank, UBS, and Goldman Sachs** have all conducted pilots on ZKsync, exploring tokenized assets with ZK-verified compliance. These pilots use ZK proofs to demonstrate regulatory compliance (KYC/AML verification) without revealing the underlying customer data to settlement counterparties. The bank proves its customer is compliant. The counterparty learns nothing about who the customer is. This is not trust-minimization in the way a cypherpunk would recognize it. It is trust in compliance frameworks, verified by cryptographic proofs but governed by regulatory requirements. The magician performs for regulators now, and the trick she performs is: "we followed the rules, and here is a proof."

The Deutsche Bank pilot reveals what enterprise adoption actually looks like from the inside. Deutsche Bank's Project Guardian participation -- coordinated through the Monetary Authority of Singapore -- tested whether institutional-grade foreign exchange and government bond transactions could settle on-chain with ZK-verified KYC attestations replacing the traditional correspondent banking chain. The specific mechanism: Deutsche Bank's compliance team verifies a client's KYC status through conventional channels, then issues a ZK credential -- a proof that the client passed all required AML/CFT checks, without encoding *which* checks, *what* documents, or *whose* name. The counterparty's smart contract verifies the proof on-chain and permits settlement. The transaction completes in minutes rather than the T+2 standard. The compliance data never crosses an institutional boundary.

Understand what has changed and what has not. The settlement speed improved. The data exposure shrank. The compliance *cost* dropped, because the correspondent banking chain -- each intermediary performing redundant KYC on the same client -- collapsed into a single proof verified by mathematics. But the trust did not disappear. It migrated. Before: you trusted the correspondent bank's compliance department. After: you trust Deutsche Bank's compliance department *and* the correctness of their ZK credential issuance system *and* the soundness of the proof system *and* the smart contract that verifies it. The number of trust assumptions increased. Their *visibility* increased too -- and visibility is not nothing. A trust assumption you can examine is better than one you cannot. But it is still a trust assumption.

The pilot's economics are instructive. Correspondent banking fees for cross-border institutional transactions typically run 0.1-0.3% of notional value. For a $100 million FX trade, that is $100,000-$300,000 in intermediary costs. The ZK-verified on-chain settlement reduced this to gas fees plus proving costs -- roughly $50-200 per transaction at current rates. The savings are not marginal. They are structural. And they create an incentive so large that the technology's imperfections become, from an institutional perspective, tolerable. Banks do not adopt ZK proofs because they believe in trustlessness. They adopt ZK proofs because the alternative costs a quarter of a million dollars per transaction and takes two days. Trust-moved is acceptable when the cost savings are three orders of magnitude.

**DTCC** (the Depository Trust & Clearing Corporation) partnered with the Canton Network for tokenized Treasury securities in December 2025, using ZK proofs for privacy-preserving settlement. The DTCC clears approximately $2.5 quadrillion in securities annually. If even a single-digit percentage of that volume migrates to ZK-verified on-chain settlement within a decade, the proving infrastructure required would dwarf every other ZK application combined.

The Canton Network partnership is structurally different. Canton is a privacy-first blockchain designed by Digital Asset, built on the Daml smart contract language, where every transaction is visible only to its direct participants. ZK proofs enter not as a replacement for Canton's native privacy (which is achieved through data partitioning) but as a *bridge* between partitions: proving to a regulator that aggregate settlement volumes across private partitions satisfy capital adequacy requirements, without revealing the individual transactions. The regulator sees a proof. The proof says: "the sum of all positions held by Institution X nets to Y, and Y satisfies threshold Z." The regulator learns Y and whether it exceeds Z. The regulator learns nothing about the individual positions that produced Y.

This is trust architecture of a very specific kind. The DTCC is not minimizing trust in itself -- it *is* the trusted institution, and it intends to remain so. It is minimizing the *data exposure* required to maintain that trust. The regulator still trusts the DTCC. But the regulator no longer needs to see every transaction to verify compliance. The proof substitutes for the data. The magician has not replaced the theater manager. She has given the theater manager a way to check the books without reading every page.

**Partisia Blockchain** operates in a different corner of the enterprise market, one that reveals how ZK proofs interact with multiparty computation in government applications. Partisia's collaboration with the Danish government on digital student credentials -- part of Denmark's broader digitization initiative -- uses ZK proofs to enable students to prove enrollment status, degree completion, or GPA thresholds to employers and other institutions without revealing their full academic transcript. A student proves she graduated with honors. The employer learns that fact and nothing else -- not the specific courses, not the grades in individual subjects, not the institution's internal student ID number.

The trust analysis here differs from the banking cases in a way that matters. In the Deutsche Bank pilot, the institution issuing the credential (the bank) is the same institution the counterparty already trusts. The ZK proof is an efficiency gain, not a trust transformation. In the Partisia student credential system, the institution issuing the credential (the university) and the institution verifying it (the employer) have no pre-existing trust relationship. The ZK proof is not making an existing trust relationship more efficient. It is *creating a new trust pathway* -- one that runs through mathematics rather than through phone calls to a registrar's office. This is closer to genuine trust minimization. The employer trusts the proof, not the university's willingness to answer the phone.

But even here, the trust has not vanished. It has been moved to the credential issuance step. The ZK proof guarantees that the credential was issued by the university's signing key. It does not guarantee that the university's signing key was not compromised, that the university's records were accurate, or that the student did not commit academic fraud that went undetected. The mathematics is honest about the student's credential. It says nothing about whether the credential is honest about the student. Trust in the proof is not trust in the underlying reality. This distinction -- between proving a document is authentic and proving a document is *true* -- is the gap that no amount of cryptography can close. The magician can prove the card was in the deck. She cannot prove the deck was not rigged.

The regulatory dimension of enterprise adoption inverts the usual narrative. In every other context we have examined, ZK proofs are adopted *despite* regulatory uncertainty -- builders move fast, regulators catch up later. In the enterprise space, the dynamic is reversed. EU eIDAS 2.0, the Markets in Crypto-Assets Regulation (MiCA), Basel III's treatment of tokenized assets, and the SEC's evolving stance on digital securities all create compliance obligations that ZK proofs can satisfy. The regulation arrives first. The technology follows. This means enterprise ZK adoption is not driven by technological enthusiasm. It is driven by legal necessity. When a regulation says "you must verify compliance without sharing customer data across jurisdictions," the list of technologies that satisfy that requirement is very short. ZK proofs are at the top of it.

**Privacy Pools** (0xbow) launched on Ethereum mainnet in April 2025, enabling users to prove the provenance of their funds -- that they did not originate from sanctioned addresses -- without revealing their full transaction history. This is a direct response to the regulatory challenges highlighted by Tornado Cash sanctions. Privacy Pools is the most philosophically interesting enterprise application: it uses ZK proofs to prove innocence without proving identity. The trust assumption is not in a bank or a regulator but in the mathematical definition of "sanctioned address." That definition is still set by a government. The mathematics enforces the policy. It does not choose the policy.

The trust calculus for enterprise is mixed: centralized audit and compliance processes give way to ZK-verified attestations and institutional key management. Cryptographic integrity gains are real, but offset by institutional adoption risk and key ceremony complexity. The math improves. The organizational challenge compounds.


## Summary

Enterprise ZK adoption is regulation-first: MiCA, eIDAS 2.0, Basel III, and SEC digital-asset rules create compliance obligations that ZK proofs satisfy more cheaply than legacy correspondent-banking chains. Deutsche Bank's Project Guardian pilot reduced per-transaction compliance costs from $100K–$300K to $50–200; DTCC cleared $2.5 quadrillion annually and partnered with Canton in December 2025. Trust is not eliminated — it migrates to credential-issuance infrastructure and key management — but visibility of trust assumptions increases.

## Key claims

- Deutsche Bank (Project Guardian/MAS) used ZK-verified KYC attestations to settle FX and government bond transactions; compliance cost dropped from 0.1–0.3% notional to ~$50–200 per transaction.
- DTCC partnered with Canton Network in December 2025 for ZK-verified privacy-preserving settlement of tokenized Treasuries; DTCC clears ~$2.5 quadrillion annually.
- Canton Network uses ZK proofs as a bridge between privacy partitions — proving aggregate capital adequacy without exposing individual transactions.
- Partisia Blockchain + Danish government: student credentials proving degree/GPA thresholds to employers without exposing full transcripts; creates new trust pathway rather than improving an existing one.
- Privacy Pools (0xbow) launched April 2025: proves fund provenance (not sanctioned) without revealing full transaction history; direct response to Tornado Cash sanctions.
- Enterprise adoption is regulation-driven (eIDAS 2.0, MiCA, Basel III, SEC); technology follows legal mandate, not enthusiasm.
- Trust assumptions increase in number but gain in visibility; visible trust assumptions are better than invisible ones.

## Entities

- [[ceremony]]
- [[tornado cash]]

## Dependencies

- [[ch04-the-disclose-boundary-midnight-s-witness-architecture]] — credential issuance and selective disclosure architecture
- [[ch08-the-social-layer]] — governance and regulatory context for on-chain compliance
- [[ch13-zk-identity-growth-regulatory-mandate]] — eIDAS 2.0 and Privacy Pools cross-referenced between identity and enterprise segments
- [[ch13-proving-as-a-service-the-prover-market-production]] — proving cost figures ($50–200/tx) connect to prover economics

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [P2] (B) No sources cited for any of the named pilots (Deutsche Bank Project Guardian, DTCC/Canton December 2025, Partisia/Danish government), the DTCC $2.5 quadrillion figure, or the correspondent banking fee range (0.1–0.3% notional). Each of these is a specific verifiable claim.
- [P2] (A) "DTCC clears approximately $2.5 quadrillion in securities annually" conflates clearing with transaction processing notional; DTCC's reported figures include repo and netting activity that inflates the number beyond what "clears" conventionally implies. Needs qualification or a more precise verb.
- [P3] (B) The claim that "Deutsche Bank, UBS, and Goldman Sachs have all conducted pilots on ZKsync" is asserted without citation; UBS and Goldman Sachs involvement in ZKsync-specific pilots (vs. Project Guardian more broadly) is worth verifying.

## Links

- Up: [[13-the-market-landscape]]
- Prev: [[ch13-proving-as-a-service-the-prover-market-production]]
- Next: [[ch13-market-sizing]]
