---
title: "The Incomplete Stack"
slug: ch09-the-incomplete-stack
chapter: 9
chapter_title: "Privacy-Enhancing Technologies"
heading_level: 2
source_lines: [4321, 4342]
source_commit: 64ef08cec31e6c519d3e388f85563b82e6479728
status: reviewed
word_count: 377
---

## The Incomplete Stack

A thread runs through this chapter that is worth stating plainly.

Privacy is not a feature that you add to a system after it is built. It is a property of the architecture, present from the first design document or absent forever. You cannot retrofit privacy onto a transparent blockchain any more than you can retrofit soundproofing onto a glass house. Or, to stay with our metaphor: you cannot add trapdoors to a stage after the audience is already seated.

The four PETs -- ZKPs, MPC, FHE, and DP -- are not competing technologies. They are complementary tools in a single toolkit. The magician's wand, the glovebox, the fog machine, and the locked vault where multiple parties contribute secrets they never share. Each excels at a different trust problem. Each fails at problems the others solve well. The system architect who understands all four, and who understands how they compose, has a genuine advantage over one who knows only ZKPs and treats every privacy problem as a nail to be hit with the zero-knowledge hammer.

The regulatory environment is, for the first time, pulling in the same direction as the technology. GDPR, eIDAS 2.0, and the global trend toward data sovereignty create legal mandates for exactly the capabilities that PETs provide. The question is no longer "should we use privacy-enhancing technologies?" but "which ones, in what combination, and how do we prove to regulators that they work?"

That last part -- proving to regulators that the privacy technology works -- is, fittingly, itself a zero-knowledge problem. And we have the tools to solve it.

Part III steps back from the individual layers and asks: when you put all seven together, what does the system actually look like? The answer turns out to be more tangled than the seven-layer model suggests.

---

# Part III: Synthesis and the Road Ahead {.unnumbered}

*The trick has been performed seven times, each time revealing a deeper layer of the mechanism. Now we step back from the stage. What does the whole show look like from the back of the theater? Where is the art heading? And does the magic hold up outside the theater, in the harsh light of commerce, regulation, and the passage of time?*

---


## Summary

Closing argument for chapter 9: privacy is an architectural property that cannot be retrofitted, the four PETs are complementary not competing, and the regulatory environment (GDPR, eIDAS 2.0) is for the first time pulling in the same direction as the technology. The chapter closes by bridging to Part III, which examines the full seven-layer system.

## Key claims

- Privacy cannot be added to a transparent system after construction — it must be present from the first design document.
- ZKPs, MPC, FHE, and DP are not competing; they are complementary tools for distinct trust problems.
- Regulators now mandate the capabilities PETs provide, shifting the question from "should we?" to "which combination, and how do we prove it works?"
- Proving to regulators that the privacy technology works is itself a zero-knowledge problem.

## Entities

- [[fhe]]
- [[mpc]]
- [[zkps]]

## Dependencies

- [[ch09-the-four-pillars]] — the four pillars summarised here
- [[ch09-the-regulatory-intersection]] — regulatory pull argument developed there
- [[ch09-the-decision-matrix]] — composition as the engineering answer
- [[ch10-the-causal-web-why-it-is-a-dag-not-a-stack]] — Part III entry point referenced at section close

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [none] X — no issues found.

## Links

- Up: [[09-privacy-enhancing-technologies]]
- Prev: [[ch09-open-problems]]
- Next: —
