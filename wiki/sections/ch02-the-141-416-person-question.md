---
title: "The 141,416-Person Question"
slug: ch02-the-141-416-person-question
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [548, 595]
source_commit: 6e757843ed29aa50ce4558719452a86510ed0d20
status: finalized
word_count: 1146
---

## The 141,416-Person Question

If the 1-of-N trust model says you only need one honest participant, why did 141,416 people participate in the Ethereum KZG ceremony? What is the marginal value of participant number 141,417?

The mathematical answer: zero. One honest participant is sufficient. The 141,415 others add nothing to the mathematical security guarantee.

The operational answer: everything. Security is not a binary state -- it is a confidence level. With six participants, a well-resourced adversary could conceivably investigate, coerce, or compromise all six. With 141,416 anonymous participants from around the world, many contributing through ephemeral browser sessions, the attack surface becomes unmanageable. You would need to compromise not just the people but their hardware, their network connections, their randomness sources, their memories.

There is also a signaling dimension. A ceremony with 141,416 participants is a public demonstration that the community takes the trust assumption seriously. It is *social consensus made visible*. The ceremony functions as both a cryptographic protocol and a coordination event.

But a deeper question hides beneath this one.

"If the toxic waste is destroyed, how does anyone *know* it was actually destroyed?"

The epigraph that opened this chapter asked it. Here is the answer: nobody knows. "Destruction" is a physical claim about a digital artifact. You cannot prove you deleted something from your own computer. You can only promise you did. The 1-of-N model rests on: "I trust that at least one person is honest, *and* that their computer was not compromised, *and* that no backup exists anywhere, *and* that no side-channel leaked the secret during generation."

This is weaker than trusting a single entity. But it is not zero trust. The word "trustless" does not apply here. The accurate word is "trust-minimized." This distinction matters, and it will recur at every layer.


### The Structure of Ceremony Trust

The 141,416-person question admits a deeper analysis than the one just given, one that touches the foundations of how human societies construct shared belief.

Consider what it means to "trust" a cryptographic ceremony. You are not trusting that a specific person told the truth. You are not trusting that a specific institution acted in good faith. You are trusting a *statistical claim about a population*: that among 141,416 independent actors, at least one behaved honestly. This is a fundamentally different kind of trust than anything that existed before networked cryptography. It is closer to the trust you place in thermodynamic laws -- not trust in any particular molecule, but trust in the aggregate behavior of an astronomically large ensemble.

The sociologist Niklas Luhmann distinguished between *trust* (an active bet on a specific person) and *confidence* (passive reliance on a system) [Luhmann, *Risk: A Sociological Theory*, 1993]. The 1-of-N ceremony model converts the first into the second: you don't trust any participant; you have confidence in the design. If that confidence ever broke, there would be no villain to blame -- only the discovery that a system designed to be trustworthy was not.

This is why the ceremony must not only *be* secure but be *perceived* as secure by a community large enough to sustain confidence over decades. Perception is an engineering requirement. A cryptographically perfect ceremony that the community does not believe in provides no security in practice.

The Ethereum KZG ceremony achieved its social credibility through four mechanisms that future ceremony designers should study.

First, *radical openness*. The ceremony's source code was published. The coordination protocol was specified in public documents. The queue was visible in real time. Every contribution was logged in a publicly verifiable transcript. This transparency did not make the ceremony secure -- security came from the 1-of-N assumption -- but it made the ceremony *auditable*, which is a precondition for sustained confidence.

Second, *permissionless participation*. The decision to let anyone with an Ethereum address contribute was not merely a design choice. It was a statement about who the SRS belongs to. A ceremony restricted to credentialed cryptographers would have been more efficient and arguably more secure in a narrow technical sense -- each contribution would have been generated with better operational hygiene. But it would have been a ceremony *for* the community, not *by* the community. The permissionless design traded some individual contribution quality for a qualitative shift in collective ownership.

Third, *diversity of entropy sources*: participants contributed from different hardware, operating systems, locations, and jurisdictions, making simultaneous compromise operationally infeasible. Fourth, *unforgeable cost of participation*: each contributor spent real time waiting, computing, and verifying, and that aggregate investment across 141,416 people signals commitment in a way no amount of on-chain capital can replicate.

The game-theoretic analysis reinforces this intuition. In a ceremony with six participants, the cost of corrupting the ceremony is the maximum of the costs of corrupting each participant -- you need all six. With 141,416 participants, the cost is still the maximum of individual corruption costs (since you need all of them), but the *minimum* of those individual costs is now determined by the most resilient participant in a population of 141,416. Among that many people, there is almost certainly someone whose operational security is excellent, whose hardware is air-gapped, whose randomness source is physical, and whose motivation is ideological rather than financial. The ceremony's security is, in a precise sense, determined by its strongest link rather than its weakest. Nikolaenko et al. formalize this: their on-chain ceremony model proves security holds as long as one participant acts honestly, regardless of adversarial coordination among all others [Nikolaenko et al., "Powers-of-Tau to the People," IACR ePrint 2022/1592].

This is the inverse of the chain metaphor that dominates security thinking. A chain is only as strong as its weakest link. A ceremony is only as *insecure* as its *strongest* link. This inversion -- this structural optimism built into the mathematics of the 1-of-N model -- is what makes mass-participation ceremonies viable. You do not need to ensure that every participant is careful. You need to ensure that the population is large enough and diverse enough that at least one participant, somewhere, is careful enough.

The question of how large is "large enough" has no clean mathematical answer, because it depends on the adversary model. Against a lone hacker, six participants may suffice. Against a corporate adversary, ninety. Against a nation-state with global surveillance capabilities, perhaps tens of thousands. Against a coalition of nation-states -- the most paranoid threat model, but not an absurd one for infrastructure securing tens of billions of dollars -- perhaps hundreds of thousands. The Ethereum ceremony's 141,416 participants do not guarantee security against any specific adversary. They guarantee that the *sociological* bar for a successful attack is extraordinarily high, higher than any previous cryptographic ceremony has set, and plausibly higher than any adversary can clear.

Plausibly. Not provably. And that gap -- between plausible and provable -- is where any honest assessment of ceremony security must live.

But even if the ceremony is perfect -- even if all 141,416 participants were honest and every fragment of toxic waste is truly gone -- the system can still be broken. The ceremony protects the stage. It does not protect what is performed on it.



## Summary

Mathematically, one honest participant suffices; operationally, 141,416 anonymous contributors make the attack surface for compromise unmanageable against any known adversary model. The 1-of-N ceremony model converts personal trust into statistical confidence (Luhmann's distinction): security is determined by the population's strongest link rather than its weakest. But the model is trust-minimized, not trustless, and a perfect ceremony still does not protect against bugs in the construction itself.

## Key claims

- Mathematical marginal value of participant 141,417: zero; one honest participant is sufficient.
- Sociological value: with 141,416 anonymous global contributors, simultaneous compromise is operationally infeasible for any adversary including nation-states.
- A ceremony's security is determined by its strongest link (1-of-N), the inverse of the chain metaphor.
- The Ethereum KZG ceremony used four credibility mechanisms: radical openness, permissionless participation, diversity of entropy sources, and unforgeable cost of participation.
- "Trustless" does not apply; "trust-minimized" is the accurate term — the gap matters.
- Against a coalition of nation-states, a population of hundreds of thousands is a plausible but not provable bar.

## Entities

- [[ceremony]]
- [[kzg]]

## Dependencies

- [[ch02-two-ways-to-build-a-stage]] — provides the mathematical basis for the 1-of-N multiplicative structure
- [[ch02-the-structured-reference-string]] — defines the SRS these 141,416 participants were building

## Sources cited

None in this section.

## Open questions

- How large must N be for the sociological bar to exceed any plausible adversary's capacity? No clean mathematical answer exists; it depends on the threat model.

## Improvement notes

_All P0/P1/P2/P3 findings resolved in Phase 3 revisions (2026-04-18 through 2026-04-20)._

_P0/P1/P2 items resolved in Phase 3 revision (2026-04-19); remaining P3 deferred._

_P0/P1 items resolved in Phase 3 revision (2026-04-18); remaining P2/P3 deferred._

- [none] (A) No factual errors found.
- [none] (D) No contradictions with other chapters found.

## Links

- Up: [[02-building-the-stage]]
- Prev: [[ch02-the-capex-opex-framework]]
- Next: [[ch02-the-bug-that-was-not-a-ceremony-failure]]
