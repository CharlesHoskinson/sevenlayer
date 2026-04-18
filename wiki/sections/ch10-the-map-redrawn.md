---
title: "The Map Redrawn"
slug: ch10-the-map-redrawn
chapter: 10
chapter_title: "The Synthesis -- Three Paths, Not Two"
heading_level: 2
source_lines: [4352, 4390]
source_commit: e06eabb8221ef210de8c05819f8f7dad94c70483
status: drafted
word_count: 356
---

## The Map Redrawn

Chapter 1 presented seven layers as a stack -- neat, linear, one resting on the next. Nine chapters of evidence say otherwise. The seven layers are a directed acyclic graph with fourteen causal edges, and we owe you the honest picture before proceeding.

```
                    ┌──────────────────────────────────┐
                    │  THE SEVEN-LAYER CAUSAL WEB       │
                    │  (14 directed design-time edges)  │
                    └──────────────────────────────────┘

        ┌─────────┐         ┌─────────┐         ┌─────────┐
        │ Layer 1 │◄────────│ Layer 2 │◄────────│ Layer 3 │
        │  Setup  │         │Language │         │ Witness │
        └────┬────┘         └────┬────┘         └────┬────┘
             │                   │ ▲                  │
             │                   │ │                  │
             ▼                   ▼ │                  ▼
        ┌─────────┐         ┌─────────┐         ┌─────────┐
        │         │         │ Layer 4 │◄────────│         │
        │         │         │  Arith  │─ ─ ─ ─ ►│         │
        │         │         └────┬────┘         │         │
        │ Layer 5 │◄─────────────┘              │ Layer 7 │
        │  Proof  │◄─────────────┐              │ Verdict │
        │ System  │         ┌────┴────┐         │         │
        │         │◄────────│ Layer 6 │◄────────│         │
        │         │────────►│Primitive│────────►│         │
        └─────────┘         └─────────┘         └─────────┘

  ── ► Upward chain (6 edges): 6→5→4→3→2→1 (design flows up)
  ◄ ── Downward pressure (8 edges): 7→6, 7→5, 4→2, 3≡4,
       6→7, 1→5, 5→7, 2→3
```

**Reading the diagram.** The upward chain (six edges) is what the book has followed: field choice (Layer 6) determines commitment scheme (Layer 5), which shapes arithmetization (Layer 4), which constrains witness layout (Layer 3), which influences ISA design (Layer 2), which determines setup scope (Layer 1). If this were the whole story, the stack metaphor would suffice.

It is not the whole story. Eight downward and cross-cutting edges complicate the picture. Ethereum gas economics (Layer 7) force BN254 pairings (Layer 6) and STARK-to-SNARK wrapping (Layer 5). Cairo's constraint system (Layer 4) dictated its ISA design (Layer 2). Jolt fused witness generation (Layer 3) into arithmetization (Layer 4). The graph has no cycles -- design-time constraints are asymmetric -- but it has width: multiple independent paths connect the same pair of nodes, and a single parameter change propagates through the web along all of them simultaneously.

The three paths below are routes through this DAG, not floors in a building. Each path makes different choices at each node, and the edges explain why those choices are coupled.


## Summary

The seven-layer stack is more accurately a directed acyclic graph (DAG) with 14 design-time causal edges, not a simple top-down ordering. The section provides the corrected diagram and explains that each of the three paths below is a route through this DAG, with coupled choices at each node.

## Key claims

- The seven-layer model has 14 directed design-time edges, not 6.
- Six edges form the upward chain: Layer 6 → 5 → 4 → 3 → 2 → 1.
- Eight additional downward and cross-cutting edges include: Layer 7 forces Layer 6 (gas → BN254), Layer 7 forces Layer 5 (gas → wrapping), Layer 4 forces Layer 2 (Cairo ISA), Layer 3 collapses into Layer 4 (Jolt).
- The graph has no cycles — design-time constraints are asymmetric — but has width: multiple independent paths connect the same pair of nodes.
- A single parameter change (e.g., base field) propagates along multiple routes simultaneously and unpredictably.

## Entities

- [[bn254]]
- [[jolt]]

## Dependencies

- [[ch01-the-seven-layers-at-a-glance]] — original linear stack model now being revised
- [[ch07-the-cascade-effect]] — earlier treatment of field-to-proof-system causality
- [[ch05-layer-4-arithmetization]] — Layer 4 behavior relevant to DAG edges

## Sources cited

None in this section.

## Open questions

None flagged by this section.

## Improvement notes

- [P2] C The ASCII diagram is hard to parse: the visual arrow count does not obviously match the "14 directed edges" claim in the header, and the legend lists only 14 edges split as "6 upward" + "8 downward" without labelling all 8 downward arrows in the figure. A reader cannot verify the edge count from the diagram alone.

## Links

- Up: [[10-the-synthesis-three-paths-not-two]]
- Prev: [[ch10-the-binary-that-broke]]
- Next: [[ch10-path-one-the-hybrid-stark-to-snark-pipeline]]
