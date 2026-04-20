---
title: "ZKML: Provable Machine Learning (Research)"
slug: ch13-zkml-provable-machine-learning-research
chapter: 13
chapter_title: "The Market Landscape"
heading_level: 2
source_lines: [5045, 5060]
source_commit: 508c29f21fc4bc0080e1bf4101db484f576f36a4
status: reviewed
word_count: 647
---

## ZKML: Provable Machine Learning (Research)

Here the trust question becomes genuinely uncomfortable. Zero-knowledge proofs for machine learning inference -- proving that a specific model produced a specific output on a specific input without revealing the model's weights -- can prove that a neural network ran faithfully. They cannot prove the neural network should have run at all.

Read that distinction carefully. ZKML proves the inference was correct *given the model*. It says nothing about whether the model is fair, whether it was trained on representative data, whether its architecture is appropriate for the task, or whether deploying it is wise. You can prove the magician performed the trick exactly as rehearsed. You cannot prove the trick was worth performing. Trust in the computation is not trust in the model's correctness, and conflating the two is the central danger of this category.

The fundamental technical difficulty is that neural network operations (matrix multiplications, activation functions, normalization) map poorly onto the finite field arithmetic that ZK proof systems require. Each matrix multiplication involves billions of field multiplications. Activation functions like ReLU require comparison operations that are expensive in finite fields. Layer normalization involves division and square roots, both of which must be decomposed into constraint-friendly operations. The overhead tax from Chapter 5 -- already 10,000-50,000x for general computation -- runs even steeper for ML workloads, because neural network arithmetic is optimized for floating-point hardware that has no analogue in finite field circuits.

**Lagrange's DeepProve** is the current leader, claiming 700x faster ZK proofs for ML inference compared to previous general-purpose approaches (such as running neural network operations inside a generic zkVM like EZKL on halo2, where proving a single inference of a modest model could take thousands of seconds). DeepProve achieves this through specialized arithmetization for neural network operations -- custom constraint templates for matrix multiplications and activation functions that exploit the regular structure of neural network layers rather than treating each operation as a generic polynomial constraint. At 700x, proving inference on a 100-million-parameter transformer drops from hours to seconds -- approaching practical for high-value use cases like regulatory AI audits, though still far from the millisecond latencies that production AI systems require. The 700x improvement is impressive precisely because the starting point was so far from practical.

**EZKL** provides an open-source toolkit for generating ZK proofs of neural network inference, targeting the halo2 proof system. EZKL converts ONNX models into ZK circuits, making it the most accessible entry point for ML engineers exploring verifiable inference. As of early 2026, ZKML remains entirely pre-commercial: no production system uses ZK-proven inference for revenue-generating decisions. The applications are clear -- verifiable content moderation, model privacy, regulatory audits of algorithmic decisions -- but the overhead tax hits ML workloads harder than any other domain.

The ZKML market is pre-revenue and research-heavy, but the applications are clear: verifiable AI inference (prove that a content moderation decision was made by a specific model), model privacy (prove model performance without revealing weights), and auditable AI (regulatory compliance for model decisions). In a world increasingly shaped by opaque AI systems, the ability to prove properties of a model without revealing the model itself may become one of the most valuable applications of zero-knowledge proofs. But only if the field resists the temptation to let "proven inference" stand in for "trustworthy AI." The proof is one layer. The model is another. And no amount of cryptographic elegance in the first layer compensates for negligence in the second.

**Trust relocated from:** model operator's self-attestation **to:** proof of inference correctness. **Net:** promising but pre-revenue; trust in model integrity itself remains unaddressed.


## Summary

ZKML proves that a neural network ran correctly on a given input, but says nothing about whether the model itself is fair or appropriate. Lagrange's DeepProve claims 700x speed improvement over prior approaches; EZKL provides open-source tooling via halo2. The segment is entirely pre-commercial as of early 2026, blocked by the overhead tax of mapping floating-point neural-network arithmetic into finite fields.

## Key claims

- ZKML proves inference correctness given a model; it cannot prove the model is trustworthy or appropriate.
- Overhead tax for ML workloads exceeds the 10,000–50,000x general figure because neural-network arithmetic maps poorly to finite fields.
- Lagrange DeepProve claims 700x speedup over generic zkVM approaches (e.g., EZKL on halo2); drops 100M-parameter transformer inference from hours to seconds.
- EZKL converts ONNX models to ZK circuits for halo2; most accessible entry point for ML engineers.
- No production system uses ZK-proven inference for revenue-generating decisions as of early 2026.
- Applications: verifiable content moderation, model privacy, regulatory AI audits.

## Entities

- [[fri]]
- [[halo2]]

## Dependencies

- [[ch05-the-overhead-tax-10-000x-to-50-000x]] — overhead tax analysis directly applies to ML workloads
- [[ch05-layer-4-arithmetization]] — arithmetization difficulty for non-standard operations
- [[ch13-zk-coprocessors-off-chain-computation-on-chain-verification-growth]] — coprocessors as adjacent off-chain computation category

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

_P0/P1 items resolved in Phase 3 revision (2026-04-19); remaining P2/P3 deferred._

- [P2] (B) DeepProve's 700x speedup claim is attributed only to Lagrange ("claiming") with no external citation. Given this is a central quantitative claim, a source or caveat about independent verification is needed.
- [P3] (A) "hours to seconds" for a 100M-parameter transformer inference at 700x improvement is stated without a baseline proof time, making the improvement claim unverifiable from the text alone.

## Links

- Up: [[13-the-market-landscape]]
- Prev: [[ch13-zk-coprocessors-off-chain-computation-on-chain-verification-growth]]
- Next: [[ch13-zk-identity-growth-regulatory-mandate]]
