---
title: "The "Proof Core" Triad"
slug: ch11-the-proof-core-triad
chapter: 11
chapter_title: "zkVMs -- The Universal Stage"
heading_level: 2
source_lines: [4676, 4701]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 978
---

## The "Proof Core" Triad

The comparative analysis reveals a pattern that the seven-layer model obscures: Layers 4, 5, and 6 form a tightly coupled triad -- the **proof core** -- in every production zkVM. These three layers are not three choices. They are one choice with three manifestations.

In Stwo: M31 (Layer 6) forces Circle groups (Layer 5) forces Circle AIR (Layer 4).

In SP1: BabyBear (Layer 6) enables multilinear PCS (Layer 6) enables LogUp-GKR (Layer 4/5) enables Jagged multi-table AIR (Layer 4).

In Jolt: BN254 (Layer 6) enables Hyrax commitment (Layer 6) makes sumcheck natural (Layer 5) makes Lasso lookups natural (Layer 4).

In each case, the field choice *determines* the commitment scheme, which *determines* the polynomial representation, which *determines* the arithmetization. The proof core is the inseparable nucleus of {field, commitment scheme, polynomial representation} that straddles Layers 4, 5, and 6. Acknowledging this concept does not require restructuring the seven-layer model, but it does require acknowledging that the model's clean layer boundaries are pedagogical simplifications, not architectural truths.

To see why this coupling is not merely incidental but structurally inevitable, consider what happens when you try to swap one element of the triad while holding the others fixed. Suppose you wanted to keep M31 arithmetic (for speed) but use Hyrax commitments (for transparent elliptic-curve proofs without a trusted setup). Hyrax requires multi-scalar multiplication over an elliptic curve whose scalar field matches the proving field. No standard curve has a 31-bit scalar field -- the smallest curves used in practice have 254-bit or 256-bit scalar fields. You would need to embed M31 elements into a vastly larger field for every commitment operation, destroying the throughput advantage that motivated the M31 choice. The triad resists substitution because its elements are not independent components connected by interfaces; they are facets of a single algebraic structure viewed from different angles.

The same rigidity appears in the other direction. Suppose you wanted to keep BN254 (for Hyrax compatibility) but switch to AIR-based arithmetization (for the modular chip architecture that makes SP1 extensible). AIR evaluation requires FFTs over the proving field, and BN254's scalar field has a multiplicative subgroup of order $2^{28}$ -- adequate but not generous. More critically, BN254 field operations are 100x slower than BabyBear operations, so the FFT-intensive AIR evaluation that runs in milliseconds over BabyBear would take seconds over BN254. The AIR paradigm's viability depends on cheap field arithmetic; cheap field arithmetic depends on small fields; small fields depend on hash-based commitments. Pull one thread and the entire fabric moves.

This structural coupling explains an otherwise puzzling empirical observation: despite the enormous design space of possible {field, commitment, arithmetization} combinations, production systems cluster around a small number of triads. The March 2026 landscape shows essentially three: {small field, hash-based FRI, AIR} (SP1, Stwo, Airbender, RISC Zero, Pico Prism), {small field, hash-based FRI, AIR + lookup} (ZisK, OpenVM), and {large field, MSM-based, sumcheck + lookup} (Jolt). The clustering is not a failure of imagination. It is the proof core exerting its gravitational pull: only certain combinations are self-consistent, and the self-consistent combinations are few.

**The decisive fork is at Layer 6 (field choice).** SP1 and Stwo both chose small fields (31-bit) optimized for hardware throughput, accepting extension fields and hash-based commitments. Jolt chose a 256-bit field, accepting higher per-operation cost for native elliptic curve compatibility. This single parameter cascades through every other layer. The choice is not primarily about arithmetic speed -- it is about which mathematical universe the entire proof system will inhabit. A 31-bit field lives in the universe of hash trees, Merkle commitments, and transparent proofs. A 256-bit elliptic-curve field lives in the universe of pairings, discrete logarithms, and structured reference strings. These universes have different physics, and a system that enters one cannot easily visit the other.

**The second fork is at Layer 4 (arithmetization).** SP1 and Stwo both use AIR-based constraint systems. Jolt abandons AIR entirely in favor of lookup-based arithmetization. AIR systems *describe* computation as polynomial constraints; Jolt *tabulates* computation as lookup entries. The distinction is deeper than syntax. In an AIR system, the prover must *solve* the constraint system -- find a witness that satisfies all polynomial equations simultaneously. The constraint system is a specification that the witness must match. In a lookup system, the prover must *demonstrate membership* -- show that each instruction's input-output behavior appears in a pre-computed table. The table is not a specification to be satisfied but a reference to be consulted. One paradigm asks "does this answer satisfy the question?" The other asks "is this answer in the book?"

The practical consequence is that AIR systems scale with constraint complexity (more constraints per instruction means more work per step), while lookup systems scale with table size and decomposition depth (more subtables means more sumcheck rounds). For simple arithmetic -- adds, multiplies, shifts -- the lookup approach can be dramatically cheaper, because the subtables are small and the decomposition is clean. For complex operations -- hash functions, elliptic-curve arithmetic -- the lookup approach faces a combinatorial explosion in table size, which is why even Jolt uses a thin R1CS layer for control flow rather than attempting to tabulate branching logic.

**Where the model breaks.** Cairo shows Layer 4 shaping Layer 2 (bidirectional dependency). Jolt shows Layers 3 and 4 collapsing into one. The STARK-to-SNARK wrapping pipeline is not a Layer 5 choice; it pierces Layers 5, 6, and 7 as a single vertical shaft. The seven layers are better understood as seven *aspects* of a single integrated system, not seven *modules* with clean interfaces. The proof core triad is the strongest evidence for this view: three layers that the model presents as independent choices are in fact a single crystalline structure, as rigid and as beautiful as any lattice in mathematics. Change one axis and the crystal shatters. The map is useful. The territory is more interesting.


## Summary

Layers 4, 5, and 6 form an inseparable "proof core" in every production zkVM: field choice determines commitment scheme, which determines polynomial representation, which determines arithmetization. Production systems cluster into three self-consistent triads; swapping a single element forces changes throughout the rest.

## Key claims

- Three production triads as of March 2026: {small field, FRI, AIR}; {small field, FRI, AIR+lookup}; {large field, MSM, sumcheck+lookup}.
- M31 → Circle groups → Circle AIR (Stwo triad).
- BabyBear → multilinear PCS → LogUp-GKR → Jagged AIR (SP1 triad).
- BN254 → Hyrax → sumcheck → Lasso (Jolt triad).
- Swapping M31 for Hyrax-compatible commitments destroys the throughput advantage that motivated M31.
- BN254 field ops are ~100x slower than BabyBear; AIR over BN254 is not viable at scale.
- The decisive Layer 6 fork: small (31-bit, hash-universe) vs. large (256-bit, pairing-universe).
- Cairo shows bidirectional Layer 4 → Layer 2 dependency (model's clean top-down flow inverts).
- STARK-to-SNARK wrapping pierces Layers 5, 6, and 7 as one vertical shaft.

## Entities

- [[airbender]]
- [[babybear]]
- [[bn254]]
- [[circle stark]]
- [[fri]]
- [[jolt]]
- [[lasso]]
- [[logup]]
- [[mersenne]]
- [[pico]]
- [[prism]]
- [[zisk]]

## Dependencies

- [[ch11-three-zkvms-through-seven-layers]] — the empirical basis for the triad observation
- [[ch11-the-landscape-table-march-2026]] — the clustering claim is verifiable from that table
- [[ch06-the-proof-core-why-layers-4-5-and-6-are-inseparable]] — prior chapter treatment of the same concept
- [[ch10-the-causal-web-why-it-is-a-dag-not-a-stack]] — causal structure between layers

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [P2] (A) "In SP1: BabyBear (Layer 6) enables multilinear PCS (Layer 6)" — multilinear PCS straddles Layers 5 and 6 (commitment scheme is Layer 7 in some framings, or Layer 5 in others); labelling it Layer 6 twice in the same triad description is internally inconsistent with the book's own layer taxonomy.
- [P3] (B) No sources cited for the triad clustering claim or for the "BN254 subgroup order 2^28" figure, both of which are verifiable mathematical facts that benefit from a reference.

## Links

- Up: [[11-zkvms-the-universal-stage]]
- Prev: [[ch11-three-zkvms-through-seven-layers]]
- Next: [[ch11-performance-the-cost-collapse]]
