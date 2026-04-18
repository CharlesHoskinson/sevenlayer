---
title: "Composability: When One PET Is Not Enough"
slug: ch09-composability-when-one-pet-is-not-enough
chapter: 9
chapter_title: "Privacy-Enhancing Technologies"
heading_level: 2
source_lines: [4118, 4151]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 1219
---

## Composability: When One PET Is Not Enough

The real power of PETs emerges when they are composed. No single instrument plays the whole symphony. Consider a realistic healthcare scenario -- and notice how each PET enters at the moment its particular strength is needed:

1. **Step 1 (MPC)**: Five hospitals jointly compute aggregate statistics on a rare disease using their combined patient records. Each hospital contributes its data to an MPC protocol. No hospital sees any other hospital's records. The output is aggregate statistics: prevalence rates, treatment outcomes, demographic distributions.

2. **Step 2 (Differential Privacy)**: Before the aggregate statistics leave the MPC computation, differential privacy noise is added. This ensures that even the aggregate output cannot be used to infer individual patient records. The privacy budget (epsilon) is tracked across queries.

3. **Step 3 (FHE)**: The differentially private aggregate statistics are encrypted under FHE. An AI firm trains a predictive model on the encrypted data. The AI firm never sees the plaintext statistics. The hospitals never see the AI firm's model architecture (which may be proprietary). The glovebox, again.

4. **Step 4 (ZKP)**: The AI firm produces a zero-knowledge proof that the trained model meets accuracy and fairness criteria specified in a regulatory standard, without revealing the model's weights or the training data. A regulator verifies the proof and certifies the model for clinical use. The magician performs. The audience -- in this case, the regulator -- verifies.

Each step uses the PET best suited to its specific trust problem: MPC for multi-party data aggregation, DP for statistical disclosure control, FHE for outsourced computation on sensitive data, and ZKP for verifiable compliance without disclosure.

But the transitions between steps are not trivial. The MPC-to-FHE handoff requires either the hospitals to encrypt the MPC output under the AI firm's FHE public key (which means they see the plaintext), or a protocol that converts MPC secret shares directly to FHE ciphertexts (an active research frontier). The FHE-to-ZKP handoff requires verifiable FHE -- proving in zero knowledge that an FHE computation was performed correctly -- which is emerging but not yet production-ready.

The composability lesson: PETs compose in theory. In practice, each composition point requires protocol engineering that is often harder than the individual PET deployments. The system architect must understand not just what each PET does, but how they hand off to each other. The orchestra sounds beautiful when everyone enters on cue. Getting the cues right is the hard part.

Three composition patterns deserve particular attention, because they recur across domains and will likely define the privacy architecture of the next decade.

**ZKP + MPC: Verified Inputs to Joint Computation.** The healthcare scenario above assumes each hospital contributes honest data to the MPC protocol. But what if a hospital submits fabricated records -- inflating its patient count to increase its share of research funding, or omitting records to conceal a malpractice pattern? MPC computes correctly on whatever inputs it receives. It does not verify that the inputs are truthful. This is where ZKPs enter: each participant produces a zero-knowledge proof that its MPC input satisfies agreed-upon constraints -- the records come from a certified database, the patient count matches a signed attestation from the hospital's electronic health record system, the data format conforms to the protocol specification. The MPC protocol verifies these proofs before accepting the inputs. The joint computation proceeds on data that is both private *and* certified. No party reveals its data. Every party proves its data is legitimate. The magician does not merely perform behind a curtain -- she presents her credentials before stepping onto the stage.

This pattern -- ZKP-verified inputs to MPC -- appears in private auctions (prove your bid is backed by sufficient funds without revealing the bid amount), in private voting (prove you are an eligible voter without revealing your identity), and in collaborative machine learning (prove your training data meets quality thresholds without revealing the data itself). In each case, MPC provides the privacy during computation, and ZKPs provide the integrity of the inputs. The two PETs are not redundant. They address orthogonal trust problems. Privacy without integrity is a system that computes correctly on lies. Integrity without privacy is a system that reveals everything it verifies.

**ZKP + FHE: Verifiable Encrypted Computation.** This is the zkFHE frontier mentioned earlier, and it deserves a structural explanation. The problem: a cloud provider performs FHE computation on your encrypted data and returns an encrypted result. You decrypt and get an answer. But did the provider actually compute the function you requested? Or did it compute a cheaper approximation, or a different function entirely, or simply return a random ciphertext? FHE guarantees confidentiality -- the provider cannot see your data. It does not guarantee integrity -- the provider can lie about what it computed. ZKPs close this gap. The provider produces a zero-knowledge proof that the sequence of homomorphic operations it performed on the ciphertext corresponds exactly to the function specification. The proof is verified against the input ciphertext, the output ciphertext, and the function description. If it checks out, you know the computation was honest. If it does not, you know to reject the result and find another provider.

The difficulty is that proving FHE computations in zero knowledge is very expensive. Each homomorphic operation involves polynomial arithmetic over large rings, and the ZKP circuit must encode all of this arithmetic faithfully. Current zkFHE prototypes achieve verification for small circuits -- a few hundred multiplication gates -- and the proving overhead adds another order of magnitude atop FHE's already steep costs. But the research trajectory is clear, and the incentive is enormous: anyone who wants to outsource computation on sensitive data to an untrusted cloud needs both confidentiality (FHE) and integrity (ZKP). Neither alone is sufficient.

**The Privacy Stack.** PET composition is fundamentally an architectural problem: do not think of PETs as individual tools to be selected. Think of them as layers in a protocol stack, analogous to the network stack that separates TCP from IP from Ethernet. At the bottom, differential privacy provides statistical-level guarantees for aggregate data releases -- the coarsest and cheapest form of privacy, suitable for telemetry and census-scale statistics. Above it, MPC provides computation-level privacy for multi-party protocols -- stronger than DP (it protects individual inputs, not just statistical aggregates), but more expensive and limited to specific interaction patterns. Above that, FHE provides data-level privacy for outsourced computation -- stronger still (the computing party learns nothing at all), but with the highest performance cost. And at the top, ZKPs provide verification-level privacy -- the ability to prove properties of private data or private computation without revealing the underlying secrets.

Each layer addresses a different threat. Each has a different cost. And like network layers, they compose vertically: a system might use DP for its public-facing analytics dashboard, MPC for its inter-institutional data sharing, FHE for its cloud-based model training, and ZKPs for its compliance proofs -- all within the same architecture, each operating at its appropriate level of the stack. The system architect who treats PET selection as a single choice ("we will use ZKPs") is making the same mistake as the network engineer who treats protocol selection as a single choice ("we will use TCP"). The answer is almost always a stack, not a single layer.

---


## Summary

Walks through a four-step healthcare scenario (MPC → DP → FHE → ZKP) to show that PETs compose in theory but each handoff requires protocol engineering that is often harder than either component alone. Introduces three composition patterns — ZKP+MPC for verified inputs, ZKP+FHE (zkFHE) for verifiable encrypted computation, and a layered "privacy stack" analogous to the network stack — and argues that architects should think in stacks rather than single-tool selections.

## Key claims

- MPC-to-FHE handoff requires either plaintext exposure or active-research share-to-ciphertext conversion.
- ZKP+MPC: ZKPs certify input integrity (honest inputs to MPC); MPC provides computation privacy. The two address orthogonal problems.
- zkFHE current prototypes handle only a few hundred multiplication gates; proving overhead adds another order of magnitude atop FHE's cost.
- Privacy stack layers: DP (statistical/aggregate) < MPC (computation on multi-party inputs) < FHE (outsourced computation) < ZKPs (verifiable claims).
- ZKP-verified inputs to MPC appear in private auctions, private voting, and collaborative ML.
- "Privacy without integrity is a system that computes correctly on lies. Integrity without privacy is a system that reveals everything it verifies."

## Entities

- [[fhe]]
- [[mpc]]
- [[zkps]]

## Dependencies

- [[ch09-the-four-pillars]] — defines the four PETs being composed
- [[ch09-open-problems]] — zkFHE and collaborative proving are flagged as open frontiers
- [[ch09-the-decision-matrix]] — composition logic feeds into selection criteria
- [[ch09-privacy-architectures-for-smart-contracts-kachina-and-zexe]] — Midnight/Aztec as deployed composition examples

## Sources cited

None in this section.

## Open questions

- MPC-to-FHE direct share-to-ciphertext conversion protocol (active research frontier, no production implementation cited).
- zkFHE beyond small circuits (a few hundred multiplication gates) is not yet production-ready.

## Improvement notes

- [P2] (B) No sources cited despite specific quantitative claims: "few hundred multiplication gates" for zkFHE prototypes and the MPC-to-FHE share-to-ciphertext conversion as an "active research frontier" — these should cite the relevant papers or prototypes.
- [P2] (E) The "privacy stack" layer ordering (DP < MPC < FHE < ZKP by cost/strength) is asserted as architectural fact with no supporting reference; a citation to a survey or prior taxonomy would strengthen it.

## Links

- Up: [[09-privacy-enhancing-technologies]]
- Prev: [[ch09-three-kinds-of-security]]
- Next: [[ch09-real-world-deployments-five-case-studies]]
