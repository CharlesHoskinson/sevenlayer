---
title: "The Laws That Break"
slug: ch07-the-laws-that-break
chapter: 7
chapter_title: "Layer 6 -- The Deep Craft"
heading_level: 2
source_lines: [2984, 2999]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 397
---

## The Laws That Break

Richard Feynman liked to say that the laws of physics do not change. You can test them in New York or on the moon, today or in a billion years, and you get the same answers. The constants are constant. The symmetries hold. Nature does not update its firmware.

Zero-knowledge proof systems have their own "laws of physics" -- mathematical assumptions about which problems are hard to solve. These assumptions sit beneath every layer we have examined so far. The setup ceremonies of Layer 1, the constraint systems of Layer 4, the proof engines of Layer 5 -- all of them rest on a handful of beliefs about the difficulty of certain computations. If those beliefs are correct, the entire tower stands. If they are wrong, it collapses -- not gracefully, not partially, but completely.

Here is the uncomfortable question that Feynman would have asked, leaning forward with that half-grin that meant he had spotted something everyone else was politely ignoring: *What happens when quantum computers change these "laws"?*

Physics does not change. Mathematics does not change either. But our *assumptions* about which mathematical problems are hard -- those change whenever someone invents a better attack. And a quantum computer running Shor's algorithm is not a better attack. It is not a faster way to pick the same lock. It is a different kind of physics applied to the same mathematics, and it renders certain problems trivially easy that we have spent fifty years assuming were impossibly hard.

This chapter descends to the deepest layer of the zero-knowledge stack: the cryptographic primitives that everything else is built upon. It is about hardness assumptions, commitment schemes, finite fields, and the coming quantum reckoning. It is also about a revolution in progress -- a shift from one family of mathematical foundations to another that may dissolve what looked like permanent tradeoffs.

Here the metaphor reaches its limit. We cannot avoid the mathematics. But we can make it concrete. Every abstraction in this chapter corresponds to a specific engineering choice made by real teams building real systems. When we say "the Goldilocks field," we mean a specific 64-bit prime number. When we say "Module-SIS," we mean a specific problem involving short vectors in high-dimensional lattices. The goal is not to teach the mathematics but to explain why these choices matter and what they cost.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
