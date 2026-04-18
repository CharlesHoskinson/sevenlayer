---
title: "The Hidden Bottleneck"
slug: ch04-the-hidden-bottleneck
chapter: 4
chapter_title: "The Secret Performance"
heading_level: 2
source_lines: [1192, 1207]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 271
---

## The Hidden Bottleneck

The choreography is written and compiled. Now the magician goes backstage, and the costs begin.

Here is a number that should have been a scandal: 50-70%.

That is the fraction of total proving time consumed by witness generation in modern GPU-accelerated systems. Not 10-25%, as the field commonly claimed until recently. The outright majority. If witness generation accounts for more than half the cost of producing a zero-knowledge proof, why has the field treated it as a minor backstage interlude? Why have billions of dollars in optimization effort focused on the cryptographic proving step while the dominant bottleneck hid in plain sight?

The answer reveals something important about how technology communities deceive themselves. When GPU acceleration made the cryptographic proving step 10 times faster, witness generation did not get faster. It stayed the same speed. But its *share* of total time climbed from a modest 20% to a dominant 67%. The better the proof system got, the worse the witness gap became. The field celebrated its proving breakthroughs while the actual bottleneck quietly grew.

This chapter is about what happens backstage. The curtain has closed. The audience (the verifier) cannot see what the magician does next. She takes her private data -- your bank balance, your identity, your vote -- and runs the computation, recording every step. This recording is the witness: the complete execution trace. Later layers will prove properties about it without revealing its contents.

But three problems lurk behind that curtain. The recording is expensive to make. The recording room has thin walls. And if the recording is wrong, the entire system breaks.

---


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
