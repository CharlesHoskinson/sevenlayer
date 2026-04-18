---
title: "The Four Pillars"
slug: ch09-the-four-pillars
chapter: 9
chapter_title: "Privacy-Enhancing Technologies"
heading_level: 2
source_lines: [3999, 4080]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 3079
---

## The Four Pillars

Zero-knowledge proofs are one member of a family. The family is called privacy-enhancing technologies -- PETs -- and understanding ZKPs without understanding their siblings is like watching a magician and concluding that all performance is sleight of hand. It is not. Some performers sing. Some dance. Some vanish entirely. And the best shows combine all of them.

There are four major PET categories that matter for system architects making decisions in 2026. Each answers a different question. Each has a different relationship to the stage.

**Zero-Knowledge Proofs (ZKPs)** answer: *How do I prove a statement about my private data without revealing the data itself?*

Think of ZKPs as the magician's core trick: the audience sees the result but not the method. "My balance exceeds the minimum." "I am over 18." "This computation was performed correctly." The key insight, often missed, is that ZKPs are a tool for *selective disclosure*, not blanket privacy. The proof reveals the *truth of the statement* -- which is itself information. Proving "my balance exceeds $1 million" tells you something about the balance, even though the exact figure stays hidden. The magician chooses which cards to reveal. That choice is itself a disclosure.

If ZKPs are the magician's core trick -- proving truth without revealing method -- then the three siblings each perform a different kind of magic.

**Secure Multi-Party Computation (MPC)** answers: *How can multiple parties jointly compute a function on their combined data without any party revealing its input to the others?*

Picture three rival magicians who want to know whose trick is most popular -- but none will reveal their ticket sales to the others. MPC is the protocol that lets them compute the answer as if a trusted accountant had all the books, without any such accountant existing. The inputs stay private. Only the agreed-upon output is revealed.

MPC is not a single protocol. It is a family, and the family members have very different properties:

| Protocol Family | Trust Model | Security Type | Best For |
|----------------|-------------|---------------|----------|
| Shamir secret sharing | Honest majority (>50% honest) | Information-theoretic | Statistical computations, few parties |
| SPDZ (dishonest majority) | Any number of corruptions | Computational | Adversarial settings, financial computation |
| Garbled circuits | Two parties, semi-honest or malicious | Computational | Two-party computation |

The distinction between honest-majority and dishonest-majority protocols matters enormously. Shamir-based MPC with honest majority achieves *information-theoretic* security -- it remains secure even against an adversary with unlimited computational power, including quantum computers. SPDZ provides security against any number of corruptions, but relies on computational hardness assumptions.

To understand what MPC actually does, consider the problem that started the field. In 1982, Andrew Yao posed what is now called the Millionaires' Problem: two millionaires want to determine who is richer without either revealing their net worth. They are standing at a cocktail party. Neither will say a number. Neither trusts the other to be honest. And no accountant is available whom both would trust with the truth. How do they find out?

Here is the trick. Alice has a net worth of, say, $7 million. Bob has $5 million. Alice encodes her wealth into an encrypted lookup table -- a garbled circuit -- that represents the comparison function "is Alice's input greater than Bob's input?" She hands the garbled table to Bob. Bob, using a sub-protocol called oblivious transfer, obtains the encryption key corresponding to his own input ($5 million) without Alice learning which key he selected. Bob evaluates the garbled circuit with his key and obtains a single bit of output: "Alice is richer." He announces the result. Neither party learned the other's number. The function was computed. The inputs stayed private.

The garbled circuit deserves a moment of its own, because it is one of the most counterintuitive constructions in all of cryptography. Alice takes the computation she wants to perform and compiles it into a Boolean circuit -- AND gates, OR gates, NOT gates, the same primitives that make up a physical processor. She then encrypts every wire in the circuit with random labels: each wire gets two labels, one for "0" and one for "1," and Alice encrypts each gate's truth table so that only the correct pair of input labels decrypts to the correct output label. The result is a garbled mess -- a table of ciphertexts that encodes the computation but reveals nothing about it. Bob can evaluate the garbled circuit gate by gate, decrypting one entry per gate, following the circuit from input to output. He sees the computation unfold, but the labels are random strings. He learns the output and nothing else. Alice never sees Bob's input. Bob never sees Alice's circuit internals. The computation happens in a kind of cryptographic fog, visible only at the endpoints.

Scale this from cocktail-party curiosity to industrial infrastructure and the applications multiply. Private auctions: bidders submit encrypted bids to an MPC protocol that determines the winner and the clearing price without revealing any losing bid. The auction house learns who won and at what price. It never learns what the losers were willing to pay -- information that, in traditional auctions, the house can exploit in future rounds. Dark pool matching in finance: two investment banks want to match buy and sell orders for the same security without revealing their order books to each other or to the market. MPC lets them compute the intersection of their orders -- the trades that both sides want -- without exposing the orders that did not match. The matched trades execute. The unmatched orders remain invisible.

Private set intersection, or PSI, is the simplest and most widely deployed MPC primitive. Two parties each hold a set of items. They want to learn which items appear in both sets -- and nothing else. When COVID-19 contact tracing required matching infected individuals against location databases, PSI offered a path that did not require a central authority to hold everyone's location history. Google and Apple's Exposure Notification framework used a related technique: devices broadcast rotating pseudonymous identifiers, and the matching computation happens locally on each device. The computation is distributed. The data never congregates.

The cost of MPC is communication, not computation. Each gate in the circuit requires the parties to exchange encrypted values. For garbled circuits, this means transmitting roughly four ciphertexts per gate. A circuit with a billion gates requires transmitting billions of ciphertexts -- tens of gigabytes over the network. The computation itself is fast. The network is the bottleneck. This is why MPC shines for problems where the function is simple but the privacy requirement is absolute, and struggles for problems where the function is complex and latency matters. The magician works quickly. The postal service does not.

MPC is the ensemble performance: multiple magicians, each holding one card of a shared secret, jointly computing a result that none of them could produce alone. The audience sees the answer. No single performer ever sees the full hand.

**Fully Homomorphic Encryption (FHE)** answers: *How can I outsource computation on my data without the computing party learning anything about the data?*

Craig Gentry, who invented FHE, gave it the perfect image: performing surgery on a patient inside a sealed glovebox. The surgeon's hands are inside the gloves, manipulating the patient, but the glovebox prevents any direct contact. The surgeon can work -- she can cut, stitch, probe -- but she never touches the patient directly, and nothing from the operating field crosses the barrier. It is a vivid image from a different domain -- not our magician's stage but a laboratory -- and we borrow it here because Gentry's metaphor has become inseparable from the concept itself.

You encrypt your data. You send the ciphertext to a cloud provider. The cloud provider performs operations on the ciphertext. You decrypt the result. The cloud provider learns nothing -- not the data, not the result, not even which operations were meaningful. The gloves never come off.

But the glovebox is thick, and the gloves are stiff. Current FHE computations are 10,000x to 1,000,000x slower than their plaintext equivalents. Ciphertexts accumulate noise with each operation, requiring periodic "bootstrapping" that is computationally expensive. Not all operations are equally efficient -- additions and multiplications are the native operations, while comparisons and divisions are far more costly. The surgeon can work, but she works very, very slowly.

To understand why the gloves are so stiff, you need to see what an FHE computation actually looks like from the inside. The dominant schemes -- BFV, BGV, and CKKS -- all share a common mathematical structure. A plaintext value (say, the number 42) is encoded as a polynomial in a ring, typically $\mathbb{Z}_q[X]/(X^n + 1)$ for $n = 2^{13}$ or $2^{14}$ and $q$ a large modulus, perhaps 200 to 800 bits long. Encryption adds a carefully sampled noise term to this polynomial. The ciphertext is a pair of ring elements, each thousands of bits wide. Where a plaintext integer fits in 64 bits, its ciphertext might occupy 32 kilobytes. The glovebox is thick because the encoding is thick.

Addition through the glovebox is relatively gentle. You add two ciphertexts component-wise, and the noise terms add as well. The noise grows, but only linearly. Encrypted addition is perhaps 100x slower than plaintext addition -- expensive, but not prohibitively so.

Multiplication is where the cost explodes. When you multiply two ciphertexts, the underlying polynomial multiplication produces a result with noise that is roughly the *product* of the two input noise levels, not the sum. One multiplication might double the noise budget. Two multiplications might quadruple it. After a dozen consecutive multiplications without intervention, the noise overwhelms the signal -- the ciphertext becomes a random-looking polynomial that decrypts to garbage. The noise is not a flaw in the design. It *is* the security. Without noise, the lattice-based hardness assumptions that make FHE secure would not hold. The glovebox is thick because thinning it would make it transparent.

Gentry's breakthrough -- the idea that launched FHE from theoretical impossibility to practical research program -- was bootstrapping. The concept is recursive and almost paradoxical: to clean the noise from a ciphertext, you decrypt it *homomorphically*. That is, you take the noisy ciphertext, encrypt the decryption key under a fresh public key, and then run the decryption algorithm as a circuit *inside the encryption*. The output is a fresh ciphertext encrypting the same plaintext, but with reset noise -- as if you had just encrypted the value for the first time. The surgeon, working through the glovebox, performs a second surgery on the glovebox itself, replacing the foggy glass with a clean pane, all without ever removing her hands.

The cost of this cleaning step is enormous. A single bootstrapping operation might take 10 to 100 milliseconds on modern hardware -- which sounds fast until you realize that the plaintext operation it replaces (a single multiplication) takes about one nanosecond. The ratio is 10 million to one. And bootstrapping must be performed after every few multiplications to keep the noise below the fatal threshold. The 10,000x to 1,000,000x slowdown is not a single penalty applied once. It is the accumulated cost of performing every arithmetic operation on bloated polynomial ciphertexts and periodically cleaning the noise through a decryption-inside-encryption cycle that is itself a complex computation.

Recent optimizations have attacked every link in this chain. TFHE (Torus FHE) reduces the bootstrapping cost for Boolean circuits by working over a different algebraic structure. GPU acceleration parallelizes the polynomial ring arithmetic. Hybrid schemes use leveled FHE (no bootstrapping) for shallow circuits and switch to bootstrapping only when depth demands it. The overhead is shrinking -- from a million-fold five years ago to ten-thousand-fold today -- but the fundamental structure remains: encrypted computation is expensive because the noise that provides security must be managed, and managing it costs orders of magnitude more than the computation itself.

And here is the connection that brings us back to our magician. FHE lets you compute on encrypted data, but how do you know the computation was performed *correctly*? The cloud provider claims it evaluated your function honestly. But the output is encrypted -- you cannot inspect the intermediate steps. The provider could have computed a different function, or computed the right function incorrectly, and you would not know until you decrypted the result and found it nonsensical. Verifiable FHE -- zkFHE -- addresses this by having the computing party produce a zero-knowledge proof that the homomorphic operations were performed according to specification. The surgeon operates through the glovebox, and a camera inside the glovebox records the procedure for the review board. The patient stays sealed. The surgery is verified. This is where FHE and ZKPs converge, and it is one of the most active research frontiers in applied cryptography.

The field is improving rapidly. Zama, the leading FHE company, reportedly achieved a $1 billion valuation in June 2025 and launched the Confidential Blockchain Protocol testnet in July 2025. Their roadmap projects hundreds of transactions per second with GPU acceleration. But a 10,000x overhead, even if it shrinks to 1,000x, means FHE is practical only for computations where the privacy guarantee is worth the performance cost. The glovebox is for surgery you cannot perform any other way.

FHE is the trick performed inside a sealed box: the computation happens on encrypted data, and even the magician who executes the computation never sees the plaintext. The box opens to reveal only the result.

**Differential Privacy (DP)** answers: *How can I release statistical insights about a dataset while guaranteeing that no individual's record can be reverse-engineered from the output?*

If the other PETs are stage tricks -- precise, targeted, visible to the audience -- differential privacy is fog. It blurs the picture just enough that no individual face can be identified, while the overall scene remains recognizable. Apple uses it for iOS telemetry (since 2016, with $\varepsilon = 2$ per day for most data types). Google deployed RAPPOR (Randomized Aggregatable Privacy-Preserving Ordinal Response) for Chrome usage monitoring. The US Census Bureau used it for the 2020 Census -- the first-ever deployment at national scale, motivated by the Dinur-Nissim database reconstruction theorem, which proved that releasing too many exact statistics about a dataset inevitably leaks individual records.

DP works by adding carefully calibrated noise to query results. The noise is large enough to mask any individual's contribution but small enough to preserve the statistical utility of the aggregate. The privacy guarantee is parameterized by epsilon (lower epsilon = more privacy = more noise = less accuracy), and composability is formalized by a composition theorem: sequential queries consume a "privacy budget," and once the budget is exhausted, no more queries can be safely answered. The fog has a finite supply. Use it wisely.

The epsilon parameter deserves a longer look, because it is where the mathematics of differential privacy meets the politics of data collection. Think of epsilon as controlling the blur radius on a photograph. At $\varepsilon = 0.1$, you are looking at a Monet painting -- the water lilies are recognizable as water lilies, but individual petals dissolve into impression. The aggregate is preserved. The particular is lost. At $\varepsilon = 1$, you are looking at a photograph taken through frosted glass -- shapes and proportions are clear, but faces are unreadable. At $\varepsilon = 10$, you are looking at a photograph with a slight smudge -- almost everything is visible, and a determined adversary with auxiliary information might identify individuals. At $\varepsilon = \infty$, there is no blur at all. You are looking at the raw data.

The art of differential privacy is choosing the blur. Too much noise (low epsilon) and the data is useless -- a census that cannot distinguish New York from Nebraska serves no one. Too little noise (high epsilon) and the privacy guarantee is hollow -- a medical database that lets researchers reconstruct individual diagnoses is not private in any meaningful sense. The Dinur-Nissim theorem makes the stakes precise: for any dataset of $n$ individuals, if you answer more than $O(n)$ counting queries with accuracy better than $1/\sqrt{n}$, you can reconstruct the entire dataset. The blur is not optional. Without it, the data eventually gives up everyone's secrets.

What does this look like in practice? Apple's deployment adds noise locally, on each device, before data is transmitted -- a technique called local differential privacy. When your iPhone wants to report which emoji you use most frequently, it does not send "thumbs up." It sends "thumbs up" with probability $(e^\varepsilon)/(e^\varepsilon + 1)$ and a random emoji with probability $1/(e^\varepsilon + 1)$. Any individual report is plausibly random. But aggregate millions of reports, and the noise cancels out, revealing the population-level distribution. Apple uses $\varepsilon = 2$ per day for most data types and $\varepsilon = 8$ for some health-related queries. Google's RAPPOR uses a similar local model with a two-stage randomization that provides both plausible deniability for individual responses and high accuracy for aggregate statistics. You never see any of this. Your phone adds the noise silently, the aggregation server receives randomized data, and the statistical team extracts population trends from the collective fog.

The composition problem is the silent killer of differential privacy deployments. Each query against a dataset consumes a portion of the privacy budget. If you query a medical database once with $\varepsilon = 1$, you get a strong privacy guarantee. If you query it twice, the effective epsilon is (at most) 2 -- weaker, but still meaningful. If you query it a thousand times, each with $\varepsilon = 1$, the effective epsilon is (at most) 1000 -- and at that point, the privacy guarantee is essentially worthless. Advanced composition theorems (Dwork, Rothblum, and Vadhan, 2010) give tighter bounds: k queries with epsilon each compose to roughly $\varepsilon \cdot \sqrt{k}$ rather than $\varepsilon \cdot k$. But the fundamental truth remains: privacy budgets are finite, and every query spends them. A dataset that has been queried ten thousand times is not the same, from a privacy standpoint, as one that has been queried ten times. The fog dissipates with each question asked. The Census Bureau's TopDown Algorithm was designed with this in mind: the total privacy budget was fixed before any queries were defined, and the noise allocation was optimized across all geographic levels simultaneously, from national aggregates down to census blocks. The budget was spent once, carefully, and then the books were closed.

---


## Summary

Introduces the four major privacy-enhancing technology families — ZKPs, MPC, FHE, and DP — each answering a distinct trust question. MPC (via Shamir secret sharing or garbled circuits) enables multi-party computation without revealing inputs; FHE enables outsourced computation on encrypted data at 10,000–1,000,000× plaintext cost; DP adds calibrated noise to protect individuals in statistical releases with a finite privacy budget parameterised by epsilon.

## Key claims

- ZKPs provide selective disclosure: the proof reveals the truth of a statement, which is itself information.
- MPC honest-majority (Shamir) achieves information-theoretic security; SPDZ handles dishonest majority with computational security.
- Garbled circuits transmit ~4 ciphertexts per gate; network bandwidth is the primary MPC bottleneck.
- FHE noise grows multiplicatively with multiplications; bootstrapping resets noise at ~10M× plaintext operation cost.
- BFV/BGV/CKKS ciphertexts are ~32 KB for a 64-bit plaintext value (n = 2^13–2^14, q = 200–800 bits).
- Apple deployed DP in iOS 10 (2016) at ε = 2 per day for most data types.
- US Census Bureau 2020 TopDown Algorithm was motivated by the Dinur-Nissim reconstruction theorem.
- Zama reportedly achieved a $1 billion valuation in June 2025 and launched its Confidential Blockchain Protocol testnet in July 2025.

## Entities

- [[fhe]]
- [[lattice]]
- [[mpc]]
- [[zkps]]

## Dependencies

- [[ch09-three-kinds-of-security]] — classifies the security types that each pillar provides
- [[ch09-composability-when-one-pet-is-not-enough]] — shows how the four pillars compose in practice
- [[ch09-the-decision-matrix]] — maps pillars to use-case selection criteria
- [[ch08-on-chain-verification-in-2026]] — prior chapter context on ZKP deployment

## Sources cited

- Yao, A. C. (1982). Protocols for secure computations. FOCS 1982. (Millionaires' Problem / garbled circuits)
- Gentry, C. (2009). A fully homomorphic encryption scheme. PhD thesis, Stanford. (FHE / bootstrapping)
- Dwork, C., Rothblum, G., Vadhan, S. (2010). Boosting and differential privacy. FOCS 2010. (advanced composition)
- Dinur, I., Nissim, K. (2003). Revealing information while preserving privacy. PODS 2003. (reconstruction theorem)
- Apple iOS 10 differential privacy deployment (2016).
- US Census Bureau 2020 TopDown Algorithm.
- Zama Confidential Blockchain Protocol testnet (July 2025).

## Open questions

None flagged by this section.

## Improvement notes

## Links

- Up: [[09-privacy-enhancing-technologies]]
- Prev: —
- Next: [[ch09-three-kinds-of-security]]
