---
title: "The Setup Tradeoff"
slug: ch02-the-setup-tradeoff
chapter: 2
chapter_title: "Layer 1 -- Building the Stage"
heading_level: 2
source_lines: [733, 754]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 388
---

## The Setup Tradeoff

If you had to build a privacy blockchain today, the analysis in this chapter recommends a specific architecture: a universal trusted setup on BLS12-381 for production deployment (smallest proofs, cheapest verification, broadest tooling), with a transparent STARK inner proof for the actual computation (no additional ceremony, post-quantum security for the data), and a concrete migration plan for the day quantum computers arrive. That is, in fact, roughly what every major production system has chosen. The consensus is not accidental. It reflects the tradeoffs in this chapter: ceremony cost amortizes, proof size costs recur, and quantum risk compounds.

But the 1-of-N trust model, for all its elegance, is trust-minimized, not trustless. The BCTV14 bug proves that ceremony integrity alone is insufficient -- the construction must be independently correct. The quantum shelf life means that no pairing-based setup is permanent. And the ADOPT framework reveals that no ceremony conducted to date achieves the ideal of full availability, decentralization, openness, persistence, and transparency.

The stage is ready. The mathematical parameters are in place. The SRS is published. The toxic waste is (we hope) destroyed. The verifier keys are derived and deployed.

The magician needs a script. She needs to express her computation -- the thing she wants to prove -- in a language the proof system can understand. That language choice turns out to be the single most consequential decision for the security of the entire system. Not because of the cryptography. Because of the bugs.

Sixty-seven percent of real-world SNARK vulnerabilities are under-constrained circuits: programs whose mathematical rules fail to pin down the correct answer, leaving room for a cheater to slip through. Missing range checks. Forgotten equality constraints. A single `=` where `<==` was needed. The proof system does not know the program is wrong -- it faithfully proves whatever the program says, true or false. The stage can be perfect. The script is where the mistakes live.

Who writes the script?

---

# Part II: The Craft {.unnumbered}

*The audience has seen the stage. They know the rules. Now the curtain rises, and the real work begins -- backstage, in the mathematics, where every step must be recorded, encoded, sealed, and verified. The next six chapters trace the magician's craft from the first line of code to the final proof on the blockchain.*

---


## Summary

The chapter's recommended architecture — universal BLS12-381 trusted setup with a transparent STARK inner proof and a concrete quantum migration plan — is what every major production system has independently converged on. But the 1-of-N model is trust-minimized, not trustless; the BCTV14 bug shows ceremony integrity alone is insufficient; and the ADOPT framework confirms no ceremony achieves the ideal. The next question — how the prover encodes the computation the stage must verify — is where 67% of real-world vulnerabilities live.

## Key claims

- Consensus architecture: universal BLS12-381 trusted setup + transparent STARK inner proof + quantum migration plan.
- The 1-of-N trust model is trust-minimized, not trustless.
- No pairing-based setup is permanent: quantum shelf life compounds over time.
- No existing ceremony satisfies all five ADOPT properties.
- 67% of real-world SNARK vulnerabilities are under-constrained circuits, not ceremony or cryptography failures.

## Entities

- [[bls12-381]]
- [[ceremony]]
- [[groth16]]
- [[kzg]]

## Dependencies

- [[ch02-the-adopt-framework]] — the evaluation framework that reveals no ceremony is ideal
- [[ch02-the-bug-that-was-not-a-ceremony-failure]] — ceremony integrity is necessary but not sufficient
- [[ch02-the-quantum-shelf-life]] — no pairing-based setup is permanent

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

## Links

- Up: [[02-building-the-stage]]
- Prev: [[ch02-option-value-analysis]]
- Next: —
