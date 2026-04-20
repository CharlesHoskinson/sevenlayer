---
title: "Coda"
slug: ch14-coda
chapter: 14
chapter_title: "Open Questions and the Road Ahead"
heading_level: 2
source_lines: [5417, 5532]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 1850
---

## Coda

The magician walks on stage. She faces an audience of strangers -- people who have no reason to trust her and every reason to doubt. She makes a claim that sounds impossible.

But the audience is no longer what it once was. Over thirteen chapters, the stage has been built, inspected, and rebuilt. The choreography has been written in languages that prevent the worst mistakes. The backstage recording has been compressed into a mathematical certificate that no forger can reproduce. The seal rests on problems that have resisted every attack for decades, and increasingly on problems designed to resist quantum computers too. The verdict is rendered by software that is slowly, painfully, being placed beyond the reach of any committee or key-holder.

The trick still requires trust. It always will.

But the trust has been decomposed, distributed, and minimized until what remains is not faith in a person or an institution but confidence in a conjunction of mathematical facts -- each independently testable, each independently replaceable, each weaker than trusting any single entity with everything.

Think about what that means for a real person.

Consider Alice. She is a small-business owner applying for a loan. In the world before this technology, the bank demands everything: tax returns, account balances, transaction histories, personal identification, credit reports. The bank sees all of Alice's financial life, stores it on servers that get breached with depressing regularity, and shares it with partners and regulators and data brokers in ways Alice never consented to and cannot control.

Now consider Alice in the world this technology is building. She generates a zero-knowledge proof that her income exceeds the lending threshold. She proves her identity is verified and her funds are not sanctioned. She proves her credit score falls within an acceptable range. The bank receives three proofs and a loan application. It learns that Alice qualifies. It learns nothing else -- not her exact income, not her account numbers, not her transaction history, not the names of her customers. The sealed certificates say: she qualifies. The mathematics guarantees it. The bank verifies in milliseconds.

Alice controls her data. The bank gets the answer it needs. The regulator can verify that the process was followed correctly. And no database holds Alice's financial life story, waiting to be breached.

Consider the patient at the pharmacy counter. In the world before this technology, filling a prescription meant surrendering your name, your diagnosis, your prescribing physician, and your insurance details to four different organizations. In the world this technology is building, you prove you hold a valid prescription, your insurance covers it, and you have met your deductible -- three proofs, three bits of verified truth, zero dossiers assembled, zero databases waiting to be breached.

Consider the 22-year-old in Madrid, renting a car in Berlin. In the world before eIDAS 2.0, she hands her passport across a counter and a stranger photographs every page. In the world this technology is building, her phone generates a proof: "I hold a valid EU driving license and I am over 21." The rental agent learns two facts. The proof reveals nothing else -- not her name, not her nationality, not her date of birth, not her address. The wallet proves the attributes. The mathematics does the rest.

This vision is not yet fully realized. The open questions in this chapter -- GPU witness parallelism, post-quantum proof compactness, governance binding, constant-time proving -- are the engineering work that remains. The timeline is 3-5 years for the hardest problems. Some may take longer. Some may resist solution entirely. But every year, the proving gets cheaper, the verification gets faster, the security gets more formal, and the privacy gets more principled. The seven-layer model is imperfect -- the layers couple, some collapse, others are missing. But it gives the field a shared vocabulary for discussing what trust means, where it lives, and how to reduce it. That vocabulary is worth preserving even as the architecture it describes continues to evolve.

That is what seven layers of mathematics make possible. Not trustlessness -- trust-minimization. Not perfection -- progress. Not magic -- engineering that looks like magic until you understand every layer, at which point it looks like something better: a system where telling the truth is easier than lying, and where proving a fact does not require surrendering the context that makes it private.

The magician performs. The audience verifies. And between them, seven layers of mathematics ensure that the proof reveals nothing but the truth.


---

# Complete Bibliography {.unnumbered}

### Chapter 1: The Promise
1. Clarke, Arthur C. *Profiles of the Future*. Harper & Row, 1962.
2. Goldwasser, Shafi, Silvio Micali, and Charles Rackoff. "The Knowledge Complexity of Interactive Proof Systems." *SIAM Journal on Computing* 18(1): 186--208, 1989.
3. Chaliasos, Stefanos, et al. "SoK: What Don't We Know? Understanding Security Vulnerabilities in SNARKs." *USENIX Security Symposium*, 2024.

### Chapter 2: Layer 1 -- Building the Stage
4. Kate, Aniket, Gregory M. Zaverucha, and Ian Goldberg. "Constant-Size Commitments to Polynomials and Their Applications." *ASIACRYPT 2010*.
5. Bowe, Sean, Ariel Gabizon, and Ian Miers. "Scalable Multi-party Computation for zk-SNARK Parameters in the Random Beacon Model." ePrint 2017/1050.
6. Groth, Jens. "On the Size of Pairing-Based Non-interactive Arguments." *EUROCRYPT 2016*.
7. Gabizon, Ariel, Zachary J. Williamson, and Oana Ciobotaru. "PLONK: Permutations over Lagrange-bases for Oecumenical Noninteractive arguments of Knowledge." ePrint 2019/953.
8. Ben-Sasson, Eli, et al. "Scalable, Transparent, and Post-Quantum Secure Computational Integrity." ePrint 2018/046.
9. Bunz, Benedikt, et al. "Bulletproofs: Short Proofs for Confidential Transactions and More." *IEEE S&P 2018*.
10. Wang, Faxing, Shaanan Cohney, and Joseph Bonneau. "SoK: Trusted Setups for Powers-of-Tau Strings." *FC 2025*. ePrint 2025/064.
11. Boneh, Dan and Binyi Chen. "LatticeFold+: Faster, Simpler, Shorter Lattice-Based Folding for Succinct Proof Systems." *CRYPTO 2025*. ePrint 2025/247.

### Chapters 3-5
12. Pailoor, Shankara, et al. "Automated Detection of Under-Constrained Circuits in Zero-Knowledge Proofs." *PLDI 2023*. ePrint 2023/512. (See also ref [47].)
13. Wen, Hongbo, et al. "Practical Security Analysis of Zero-Knowledge Proof Circuits." *USENIX Security 2024*. ePrint 2023/190. (See also ref [48].)
14. Setty, Srinath, Justin Thaler, and Riad Wahby. "Customizable Constraint Systems for Succinct Arguments." ePrint 2023/552.
15. Setty, Srinath, Justin Thaler, and Riad Wahby. "Unlocking the Lookup Singularity with Lasso." ePrint 2023/1216.
16. Arun, Arasu, Srinath Setty, and Justin Thaler. "Jolt: SNARKs for Virtual Machines via Lookups." ePrint 2023/1217.

### Chapter 6: Layer 5 -- The Sealed Certificate
17. Kothapalli, Abhiram, Srinath Setty, and Ioanna Tzialla. "Nova: Recursive Zero-Knowledge Arguments from Folding Schemes." *CRYPTO 2022*.
18. Kothapalli, Abhiram and Srinath Setty. "HyperNova: Recursive Arguments for Customizable Constraint Systems." *CRYPTO 2024*. ePrint 2023/573.
19. Bunz, Benedikt and Binyi Chen. "ProtoStar: Generic Efficient Accumulation/Folding for Special Sound Protocols." *ASIACRYPT 2023*. ePrint 2023/620.
20. Boneh, Dan and Binyi Chen. "LatticeFold: A Lattice-based Folding Scheme and its Applications to Succinct Proof Systems." *ASIACRYPT 2025*. ePrint 2024/257.
21. Nguyen, Wilson and Srinath Setty. "Neo: Lattice-based Folding Scheme for CCS over Small Fields and Pay-per-bit Commitments." ePrint 2025/294.
22. Trail of Bits. "Frozen Heart: Forgery of Zero Knowledge Proofs." Blog post, April 2022.
23. Haboeck, Ulrich, David Levit, and Shahar Papini. "Circle STARKs." ePrint 2024/278.
49. LFDT-Nightstream. "Nightstream: Lattice-Based Folding Implementation." GitHub repository, 2025. https://github.com/LFDT-Nightstream/Nightstream

### Chapter 7: Layer 6 -- The Deep Craft
24. Shor, Peter W. "Algorithms for Quantum Computation: Discrete Logarithms and Factoring." *FOCS 1994*.
25. NIST. FIPS 203, 204, 205. August 2024.
26. NIST. "Transition to Post-Quantum Cryptography Standards (IR 8547)." November 2024.

### Chapter 8: Layer 7 -- The Verdict
27. L2Beat. "Stages Framework for L2 Maturity." https://l2beat.com/stages. Accessed March 2026.
28. Chaliasos, Stefanos, et al. "Unaligned Incentives: Pricing Attacks Against Blockchain Rollups." arXiv 2509.17126, 2025.

### Chapter 9: Privacy-Enhancing Technologies
29. Gentry, Craig. "Fully Homomorphic Encryption Using Ideal Lattices." *STOC 2009*.
30. Kerber, Thomas, Aggelos Kiayias, and Markulf Kohlweiss. "Kachina -- Foundations of Private Smart Contracts." *IEEE CSF 2021*.
31. Buterin, Vitalik, et al. "Blockchain Privacy and Regulatory Compliance: Towards a Practical Equilibrium." *Blockchain: Research and Applications*, 2023. SSRN 4563364.

### Chapters 10-11: Synthesis and zkVMs
32. Gassmann, Thomas, et al. "Evaluating Compiler Optimization Impacts on zkVM Performance." arXiv 2508.17518, 2026.
34. Ozdemir, Alex, Fraser Brown, and Riad Wahby. "CirC: Compiler Infrastructure for Proof Systems, Software Verification, and More." *IEEE S&P 2022*. ePrint 2020/1586.
35. Liu, Junrui, et al. "Certifying Zero-Knowledge Circuits with Refinement Types (Coda)." *IEEE S&P 2024*. ePrint 2023/547.
36. Maller, Mary, Sean Bowe, Markulf Kohlweiss, and Sarah Meiklejohn. "Sonic: Zero-Knowledge SNARKs from Linear-Size Universal and Updatable Structured Reference Strings." CCS 2019. ePrint 2019/099.
37. Groth, Jens, Markulf Kohlweiss, Mary Maller, Sarah Meiklejohn, and Ian Miers. "Updatable and Universal Common Reference Strings with Applications to zk-SNARKs." *CRYPTO 2018*. ePrint 2018/280.
38. Kohlweiss, Markulf, Mary Maller, Janno Siim, and Mikhail Volkhov. "Snarky Ceremonies." *ASIACRYPT 2021*. ePrint 2021/219.
50. Kim, Taechan and Razvan Barbulescu. "Extended Tower Number Field Sieve: A New Complexity for the Medium Prime Case." *CRYPTO 2016* (LNCS 9814, pp. 543--571). ePrint 2015/1027.
51. Guillevic, Aurore. "Comparing the Pairing Efficiency over Composite-Order and Prime-Order Elliptic Curves." *ACNS 2013*. ePrint 2013/218.
52. Succinct Labs. "SP1 Hypercube: Proving Ethereum in Real-Time." Blog post, May 2025. https://blog.succinct.xyz/sp1-hypercube/
53. ZKsync. "Airbender: GPU-Accelerated RISC-V Proving." Product announcement, June 2025. https://www.zksync.io/airbender
55. Kadianakis, George. "Shipping an L1 zkEVM #2: The Security Foundations." Ethereum Foundation Blog, December 2025. https://blog.ethereum.org/2025/12/18/zkevm-security-foundations
56. Chen, Binyi. "Symphony: Scalable SNARKs in the Random Oracle Model from Lattice-Based High-Arity Folding." ePrint 2025/1905.

### Chapter 12: Midnight
39. Midnight Network. "Compact Language Reference." 2025. https://docs.midnight.network/develop/reference/
40. Midnight Network. "ZKIR Intermediate Representation Reference." 2025. https://docs.midnight.network/develop/reference/
41. Midnight Network. "Developer Guide." 2025. https://docs.midnight.network/

### Chapter 13: The Market Landscape
42. Grand View Research. "Zero-Knowledge Proof Market Size, Share & Trends Analysis Report." Report GVR-4-68040-808-5, 2025. https://www.grandviewresearch.com/industry-analysis/zero-knowledge-proof-market-report
43. CastleLabs. "ZK Proofs: Is Privacy Cheap Enough to Be Mainstream?" 2025. https://research.castlelabs.io
44. Ethproofs. "ZK Proving Cost Tracker." Ethereum Foundation, 2025. https://ethproofs.org
57. Klich, Rafal (Chorus One). "The Economics of ZK-Proving: Market Size and Future Projections." Research report, March 2025.
58. DTCC. "DTCC and Digital Asset Tokenize US Treasuries on Canton Network." Press release, December 2025. https://www.dtcc.com/digital-assets/tokenization
59. Tools for Humanity (World). "World Whitepaper." 2024. https://whitepaper.world.org/
60. European Union. "Regulation (EU) 2024/1183 -- European Digital Identity Framework (eIDAS 2.0)." *Official Journal of the European Union*, 2024.

### Chapter 14: Open Questions
45. Nair, Vineet, Justin Thaler, and Michael Zhu. "Proving CPU Executions in Small Space." ePrint 2025/611.
46. Ozdemir, Alex, Evan Laufer, and Dan Boneh. "Volatile and Persistent Memory for zkSNARKs via Algebraic Interactive Proofs." *IEEE S&P 2025*. ePrint 2024/979.
47. Pailoor, Shankara, et al. "Automated Detection of Under-Constrained Circuits in Zero-Knowledge Proofs." *PLDI 2023*. ePrint 2023/512.
48. Wen, Hongbo, et al. "Practical Security Analysis of Zero-Knowledge Proof Circuits." *USENIX Security 2024*. ePrint 2023/190.
61. Hochrainer, Christoph, Valentin Wustholz, and Maria Christakis. "Arguzz: Testing zkVMs for Soundness and Completeness Bugs." arXiv 2509.10819, 2025.
62. Wee, Hoeteck and David J. Wu. "Lattice-Based Functional Commitments: Fast Verification and Cryptanalysis." *ASIACRYPT 2023*. ePrint 2024/028.
63. Mascelli, Jillian and Megan Rodden. "'Harvest Now Decrypt Later': Examining Post-Quantum Cryptography and the Data Privacy Risks for Distributed Ledger Networks." FEDS 2025-093, Federal Reserve Board, 2025.
64. NIST. "Module-Lattice-Based Digital Signature Standard (FIPS 204)." August 2024.

## Summary

The Coda grounds the book's technical arc in three concrete human scenarios — a loan applicant, a pharmacy patient, and a car-rental user under eIDAS 2.0 — to illustrate what trust-minimization means in practice. The remaining open questions (GPU parallelism, post-quantum compactness, governance binding, constant-time proving) are the residual engineering work; the trajectory toward trust-minimization is unambiguous even if zero trust is unreachable. This section also contains the book's complete bibliography.

## Key claims

- Trust has been "decomposed, distributed, and minimized" into a conjunction of independently testable mathematical facts
- Three concrete scenarios demonstrate the practical value: loan qualification (3 proofs, no data exposure), pharmacy prescription (3 proofs, no dossier), car rental under eIDAS 2.0 (2 facts proven, no identity disclosed)
- Remaining open questions have a 3-5 year timeline for the hardest problems; some may resist solution entirely
- The goal is trust-minimization, not trustlessness; progress, not perfection
- The seven-layer model's value is the shared vocabulary it provides, independent of whether production systems have exactly seven layers

## Entities

- [[airbender]]
- [[boneh]]
- [[bulletproofs]]
- [[circle stark]]
- [[folding]]
- [[gabizon]]
- [[groth16]]
- [[hypernova]]
- [[jolt]]
- [[lasso]]
- [[latticefold]]
- [[lattice]]
- [[l2beat]]
- [[midnight]]
- [[nist]]
- [[nova]]
- [[plonk]]
- [[setty]]
- [[starks]]
- [[symphony]]

## Dependencies

- [[ch01-three-converging-forces]] — privacy crisis, scaling, cost collapse that the Coda's Alice/patient/eIDAS scenarios resolve
- [[ch14-the-seven-questions-that-remain-open]] — the open questions named as "engineering work that remains"
- [[ch14-convergence]] — the trust-minimization trajectory summarized in the Coda's closing lines

## Sources cited

The Coda itself contains no inline citations; this section contains the book's complete bibliography (refs 1-64, including refs 45-64 assigned to Chapter 14). See bibliography above.

## Open questions

None flagged by this section.

## Improvement notes

- [P1] (D) The complete bibliography skips reference number 33 — the sequence runs 32, 34, skipping 33 entirely. Either a reference was deleted without renumbering or a citation was omitted. The gap should be resolved.
- [P2] (A) The Coda states "3-5 years for the hardest problems," but Q2 in ch14-the-seven-questions sets a "5-10 years for theoretical resolution" timeline and Q6 sets "3-5 years." The Coda's single range flattens the spread and understates Q2's horizon.

## Links

- Up: [[14-open-questions-and-the-road-ahead]]
- Prev: [[ch14-convergence]]
- Next: —
