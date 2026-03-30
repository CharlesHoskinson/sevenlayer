# Release Notes — v1.10

## Proving Nothing: A Layered Guide to Zero-Knowledge Proof Systems

**Date:** March 2026
**Author:** Charles Hoskinson

---

### Title Change

The book has been renamed from *The Seven-Layer Magic Trick* to **Proving Nothing: A Layered Guide to Zero-Knowledge Proof Systems**. All internal references, build scripts, and metadata updated accordingly.

### New Formats

- **EPUB** (Kindle-ready): Reflowable format per Amazon Kindle Publishing Guidelines v2025.1. MathML for mathematical content, HTML tables, custom CSS for Kindle Enhanced Typesetting.
- **PDF** (dark-mode): Updated with XeLaTeX-rendered cover page featuring classical painting artwork.

### Cover Art

New cover art: a classical painting depicting a figure presenting a sealed certificate to a gathered audience — a visual realization of the book's prover/verifier metaphor. Cover text rendered via XeLaTeX for professional-quality typography.

### Chapter-by-Chapter Editorial Changes

**Chapter 1: The Promise of Provable and Programmable Secrets**
- Expanded "The Phenomenon" with Fiat-Shamir transform bridge (the conceptual barrier to non-interactive proofs, Fiat & Shamir's 1986 insight)
- Expanded "Three Converging Forces" with eIDAS 2.0 selective disclosure detail, rollup mechanics explanation, and individual narratives for SP1 Hypercube, RISC Zero, StarkWare Stwo (940x throughput improvement), and EF zkEVM
- Expanded Layers 4-5 preview in "The Deepest Question" with concrete overhead example
- Introduced Midnight as second running example alongside Sudoku, with author disclosure
- Added polynomial definition and $2^{128}$ notation gloss
- Voice fixes: removed lecturer tics, reduced grandiosity

**Chapter 2: Layer 1 — Building the Stage**
- Expanded SRS section with geometric elliptic curve explanation, discrete logarithm grounding, and pairing explanation
- Added pairing bridge sentence for knowledge gradient
- Expanded Option-Value Analysis with 3-scenario sensitivity table and HNDL/NSA parallel
- Added bridging transition before Quantum Shelf Life section
- Deduplicated capex/opex sentence (3 verbatim repetitions → 1 canonical + 1 callback)
- Removed draft scaffolding (BGM17/BCTV14 parenthetical author's note)
- Tightened Peter Todd narrative, fixed "three mechanisms" → "four mechanisms" count
- Rewrote chapter coda as synthesis rather than recap

**Chapter 3: Choreographing the Act (Layer 2 — Language)**
- Filled PLACEHOLDER_PROVE_REST with honest description of proof-generation developer experience
- Expanded Philosophy C (RISC-V) from 321 to 650 words explaining why RISC-V won
- Moved Polygon zkEVM cautionary tale into Philosophy A section (was standalone)
- Added Sudoku running example in Compact (`verify_sudoku` circuit)
- Added Chapter 2→3 transition callback
- Glossed "nanopass" terminology inline
- Added TVL timestamp qualifiers

**Chapter 4: The Secret Performance (Layer 3 — Witness)**
- Developed "privacy is a luxury good" argument with implications for technology roadmaps
- Added witness verification subsection (property-based testing, differential testing, formal verification)
- Added Sudoku scaling context (80 field elements → thousands → billions)
- Added equity gap in synthesis connecting four technical gaps to hardware stratification
- Fixed 95% → 96% population arithmetic
- Removed defensive "This is not science fiction" line
- Added timestamp qualifiers to all hardware prices

**Chapter 5: Encoding the Performance (Layer 4 — Arithmetization)**
- Strengthened Chapter 4→5 transition with causal bridge
- Added mid-chapter checkpoint after CCS section
- Added developer-facing overhead rule of thumb
- Connected ZKIR to Chapter 3's Sudoku example
- Voice fixes: removed condescension and lecturer tics

**Chapter 6: Layer 5 — The Sealed Certificate**
- Added Nightstream generalizability note
- Added Solana ZK ElGamal date qualifier
- Connected Proof Core observation to Chapter 10 preview
- Added Midnight devnet performance caveat

**Chapter 7: Layer 6 — The Deep Craft**
- Expanded Sections 10-12 (algebraic hash functions, structural advantage of lattices, maturity and readiness)
- Reduced "miraculous" repetition (5→3 instances)
- Softened Forrester Q-Day 2030 attribution
- Added 2-adicity explanation inline
- Added curve cycle and non-native arithmetic glosses
- Added production blockers for lattice adoption
- Differentiated decision frameworks (Cascade Effect vs. One-Way Door)

**Chapter 8: Layer 7 — The Verdict**
- Expanded Solana ZK ElGamal example with attack specifics
- Added proving-system-specificity caveat to pricing attacks table

**Chapter 9: Privacy-Enhancing Technologies**
- Expanded Midnight/Kachina connection (disclose() as Kachina's information-flow control)
- Added Part III transition bridge
- Voice fix: "key insight" → direct statement

**Chapter 10: The Synthesis — Three Paths, Not Two**
- No edits needed — publication-ready as written (DAG with 14 edges, three paths, trust decomposition delivered)

**Chapter 11: zkVMs — The Universal Stage**
- Added synthesizing conclusion "The Stage Is Set" (three conclusions: ISA war over, proof core visible, competitive axis rotating)
- Added Midnight exclusion note in landscape table
- Added forward bridge to Chapter 12

**Chapter 12: Midnight — The Privacy Theater**
- Expanded Layer 4 (ZKIR) with concrete Sudoku DAG example and abstraction cost analysis
- Expanded Layer 5 (Halo 2) with selection rationale and four-phase pipeline detail
- Expanded Layer 6 with Jubjub curve role, Poseidon dual nature, field size tradeoff
- Expanded governance analysis with verifier key upgrade mechanics
- Expanded side-channel gap with Poseidon, indexer, and network timing specifics
- Fixed "seven dedicated layer analysts" phrase
- Strengthened Lesson 5 with generalizable principle

**Chapter 13: The Market Landscape**
- Added Midnight reference in rollups section
- Added aggregate $20B TVL framing and Stage 2 maturity gap
- Added concrete coprocessor example (DeFi lending TWAP query)
- Fixed ZKML "700x faster" baseline
- Added eIDAS 2.0 scale (450M users, 4 Large Scale Pilots)
- Consolidated Privacy Pools data from Chapter 9
- Added market segment breakdown table with estimated percentages
- Added CAGR methodology for projections

**Chapter 14: Open Questions and the Road Ahead**
- Deepened Q1 (GPU witness) with team names and "solved" definition
- Deepened Q4 ("trustless") with explicit seven-assumption enumeration and actuarial concept
- Expanded Convergence section mapping three forces (Ch1) to three frontiers
- Expanded Privacy Frontier with three additional dimensions
- Expanded Coda with pharmacy and Madrid personas, difficulty acknowledgment
- Connected open questions to frontier blockers with risk scenarios

### Cross-Book Improvements

- **Midnight introduction naturalized**: Glossary entry, Chapter 1 planting + author disclosure, Chapter 2 bridge paragraph, Chapter 12 framing paragraph
- **Knowledge gradient fixes**: Pairing bridge sentence in Chapter 2, polynomial definition in Chapter 1, NTT gloss in Chapter 4, 2-adicity in Chapter 7
- **Voice consistency**: 18 AI-tell markers across 5,511 lines (0.33 per 100 — far below threshold)
- **Cross-reference integrity**: 87 chapter references verified, zero broken
- **All forward promises fulfilled**: DAG in Chapter 10, three paths, trust decomposition, magician metaphor farewell

### Build System

- New Kindle EPUB pipeline: `build_kindle.py` with `kindle.css`, `kindle-filter.lua`, `metadata.xml`
- Cover generation: `generate_cover.py` (Pillow) and `coverpage.tex` (XeLaTeX)
- Font fix: STIX Two Text installed, Consolas → DejaVu Sans Mono fallback
- Files renamed from `the-seven-layer-magic-trick.*` to `proving-nothing.*`

### File Inventory

| File | Description |
|------|-------------|
| `proving-nothing.md` | Master manuscript (5,512 lines) |
| `proving-nothing.pdf` | Dark-mode PDF (357 pages) |
| `proving-nothing.epub` | Kindle-ready EPUB |
| `assets/coverart.jpeg` | Source cover painting |
| `assets/cover_print.jpg` | Cover image (portrait) |
| `assets/cover_kindle.jpg` | Cover image (Kindle landscape) |
| `coverpage.tex` | XeLaTeX cover page |
| `build_kindle.py` | EPUB build script |
| `kindle.css` | Kindle stylesheet |
| `kindle-filter.lua` | EPUB Lua filter |
| `tex/chapter1-14.tex` | Standalone LaTeX chapters |
