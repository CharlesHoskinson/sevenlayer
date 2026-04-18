---
title: "ZKML: Provable Machine Learning (Research)"
slug: ch13-zkml-provable-machine-learning-research
chapter: 13
chapter_title: "The Market Landscape"
heading_level: 2
source_lines: [5024, 5041]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: untouched
word_count: 647
---

## ZKML: Provable Machine Learning (Research)

Here the trust question becomes genuinely uncomfortable. Zero-knowledge proofs for machine learning inference -- proving that a specific model produced a specific output on a specific input without revealing the model's weights -- can prove that a neural network ran faithfully. They cannot prove the neural network should have run at all.

Read that distinction carefully. ZKML proves the inference was correct *given the model*. It says nothing about whether the model is fair, whether it was trained on representative data, whether its architecture is appropriate for the task, or whether deploying it is wise. You can prove the magician performed the trick exactly as rehearsed. You cannot prove the trick was worth performing. Trust in the computation is not trust in the model's correctness, and conflating the two is the central danger of this category.

The fundamental technical difficulty is that neural network operations (matrix multiplications, activation functions, normalization) map poorly onto the finite field arithmetic that ZK proof systems require.

**Lagrange's DeepProve** is the current leader, claiming 700x faster ZK proofs for ML inference compared to previous general-purpose approaches (such as running neural network operations inside a generic zkVM like EZKL on halo2, where proving a single inference of a modest model could take thousands of seconds). DeepProve achieves this through specialized arithmetization for neural network operations -- custom constraint templates for matrix multiplications and activation functions that exploit the regular structure of neural network layers rather than treating each operation as a generic polynomial constraint. At 700x, proving inference on a 100-million-parameter transformer drops from hours to seconds -- approaching practical for high-value use cases like regulatory AI audits, though still far from the millisecond latencies that production AI systems require.

**EZKL** provides an open-source toolkit for generating ZK proofs of neural network inference, targeting the halo2 proof system. EZKL converts ONNX models into ZK circuits, making it the most accessible entry point for ML engineers exploring verifiable inference. As of early 2026, ZKML remains entirely pre-commercial: no production system uses ZK-proven inference for revenue-generating decisions. The applications are clear -- verifiable content moderation, model privacy, regulatory audits of algorithmic decisions -- but the overhead tax from Chapter 5 hits ML workloads harder than any other domain, because neural network arithmetic is optimized for floating-point hardware that has no analogue in finite field circuits.

To appreciate the difficulty, consider what proving a single inference of a modest neural network (say, a 10-layer transformer with 100 million parameters) actually requires. Each matrix multiplication involves billions of field multiplications. Activation functions like ReLU require comparison operations that are expensive in finite fields. Layer normalization involves division and square roots, both of which must be decomposed into constraint-friendly operations. The overhead tax from Chapter 5 -- already 10,000-50,000x for general computation -- can be even steeper for ML workloads, because neural network arithmetic is optimized for floating-point hardware that has no analogue in finite field circuits. DeepProve's 700x improvement is impressive precisely because the starting point was so far from practical.

The ZKML market is pre-revenue and research-heavy, but the applications are clear: verifiable AI inference (prove that a content moderation decision was made by a specific model), model privacy (prove model performance without revealing weights), and auditable AI (regulatory compliance for model decisions). In a world increasingly shaped by opaque AI systems, the ability to prove properties of a model without revealing the model itself may become one of the most valuable applications of zero-knowledge proofs. But only if the field resists the temptation to let "proven inference" stand in for "trustworthy AI." The proof is one layer. The model is another. And no amount of cryptographic elegance in the first layer compensates for negligence in the second.

**Trust relocated from:** model operator's self-attestation **to:** proof of inference correctness. **Net:** promising but pre-revenue; trust in model integrity itself remains unaddressed.


## Summary

## Key claims

## Entities

## Dependencies

## Sources cited

## Open questions

## Improvement notes

## Links
