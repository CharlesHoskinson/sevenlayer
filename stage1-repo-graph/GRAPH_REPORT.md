# Graph Report - sevenlayer  (2026-08-30)

## Corpus Check
- Large corpus: 9122 files · ~4,291,409 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder.

## Summary
- 1189 nodes · 2048 edges · 79 communities (71 shown, 8 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 82 edges (avg confidence: 0.86)
- Token cost: 1,105,931 input · 0 output

## Community Hubs (Navigation)
- Graphify Pipeline & Audit Trail
- PDF Build Pipeline
- Book-Graph Builder
- Master-Graph Builder
- Dependency Resolution & Evals
- Reference Fetcher
- Wiki Scraper
- Manim Merkle Scenes
- PDF Graph Deepening
- Folding Schemes & Nova Lineage
- Master-Graph Tests
- zkVMs & Small Fields
- Trusted Setup Ceremonies
- Math-Explainer Pipeline
- MOOC Lecture Ingestion
- Draft Linter
- Sage Figure Runner
- Manim Renderer
- Interactive Proofs & GMR
- Paper Vector Extraction
- Commitments & Hard Problems
- Recursion & Curve Cycles
- Environment Probe
- Privacy Technologies
- Teaching Method (Sanderson/Tao)
- Wiki Mapping Program
- ZK Languages & Circuits
- Witness Generation
- Midnight Case Study
- Proving Nothing
- Recursion Outline
- 2026 06 12 Book Graph Comparison Design
- Proving Nothing
- Test Paper Vector
- 2026 06 14 Mooc Lecture Ingestion
- 2026 06 13 Master Graph
- Test Manifest
- 2026 06 12 Eprint Cloudflare Stealth Tie
- 2026 06 14 Book Outline Design
- Test Recursion Manifest
- Pipeline
- Build Kindle
- Multilinear Extension
- Proving Nothing
- Proving Nothing
- Test Deepen Pdfs
- Mini Foundations
- 2026 06 12 Book Graph Comparison
- 2026 06 13 Recursion Graph
- Proving Nothing
- Proving Nothing
- Recursion Outline
- Elliptic Curves
- Schwartz Zippel
- 2026 06 12 Deepen Pdf Graph
- 2026 06 12 Knowledge Graph References
- Proving Nothing
- Readme
- Audit Checks
- Lint
- Bilinear Pairings
- Discrete Log
- Recursion Outline
- Finite Fields
- Freivalds
- Fri
- Lagrange Interpolation
- R1Cs
- Reed Solomon
- Sigma Protocols
- Pyproject

## God Nodes (most connected - your core abstractions)
1. `Chapter 6: Layer 5 -- The Sealed Certificate` - 25 edges
2. `Chapter 7: Layer 6 -- The Deep Craft` - 25 edges
3. `LLM Wiki` - 23 edges
4. `Chapter 5: Encoding the Performance (Layer 4 -- Arithmetization)` - 22 edges
5. `evaluate()` - 21 edges
6. `Chapter 2: Layer 1 -- Building the Stage` - 21 edges
7. `BuildLog` - 18 edges
8. `Chapter 3: Choreographing the Act (Layer 2 -- Language)` - 18 edges
9. `lint_draft()` - 16 edges
10. `cmd_snowball_merge()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Schwartz-Zippel Lemma` --conceptually_related_to--> `R1CS`  [AMBIGUOUS]
  .claude/skills/math-explainer/tests/fixtures/mini_foundations.md → recursion/recursion-outline.md
- `Pedersen Commitment (vector form)` --semantically_similar_to--> `Pedersen Commitments in Folding`  [INFERRED] [semantically similar]
  .claude/skills/math-explainer/tests/fixtures/mini_foundations.md → recursion/recursion-outline.md
- `Seven-Layer ZK Stack` --semantically_similar_to--> `Hybrid Proving Pipelines`  [INFERRED] [semantically similar]
  README.md → recursion/recursion-outline.md
- `test_merge_extraction_unions_and_dedups()` --calls--> `merge_extraction()`  [INFERRED]
  tests/test_book_graph.py → scripts/build_book_graph.py
- `test_collect_fragments_unions_outline_and_refs()` --calls--> `collect_fragments()`  [INFERRED]
  tests/test_recursion_graph.py → scripts/build_recursion_graph.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **LLM Wiki Operation Suite** — _claude_skills_llm_wiki_skill_llm_wiki, _claude_skills_llm_wiki_references_operations_init_init, _claude_skills_llm_wiki_references_operations_ingest_ingest, _claude_skills_llm_wiki_references_operations_query_query, _claude_skills_llm_wiki_references_operations_lint_lint, _claude_skills_llm_wiki_references_operations_scrape_scrape [EXTRACTED 1.00]
- **Provenance Integrity Chain** — _claude_skills_llm_wiki_references_conventions_provenance_marker, _claude_skills_llm_wiki_references_conventions_contradiction_handling, _claude_skills_llm_wiki_references_operations_scrape_is_verbatim, _claude_skills_llm_wiki_references_operations_query_abstention, _claude_skills_llm_wiki_references_operations_ingest_atomic_commit [INFERRED 0.85]
- **Wiki Page Type System** — _claude_skills_llm_wiki_references_conventions_page_types, _claude_skills_llm_wiki_assets_page_templates_source_source_template, _claude_skills_llm_wiki_assets_page_templates_concept_concept_template, _claude_skills_llm_wiki_assets_page_templates_entity_entity_template, _claude_skills_llm_wiki_assets_page_templates_synthesis_synthesis_template, _claude_skills_llm_wiki_assets_page_templates_map_map_template [INFERRED 0.95]
- **Pipeline Artifacts Validated by schemas.py** — scripts_schemas, _claude_skills_math_explainer_references_dependency_protocol_concept_brief, _claude_skills_math_explainer_references_pipeline_stuck_points, _claude_skills_math_explainer_references_accuracy_protocol_accuracy_report, _claude_skills_math_explainer_references_pipeline_comprehension_set, _claude_skills_math_explainer_references_pipeline_bundle [EXTRACTED 1.00]
- **Recursion Construction Strategy Taxonomy (§1.3)** — recursion_recursion_outline_full_recursion, recursion_recursion_outline_atomic_accumulation, recursion_recursion_outline_folding_schemes, recursion_recursion_outline_stark_recursion, recursion_recursion_outline_hybrid_pipelines [EXTRACTED 1.00]
- **Nova Folding Family Tree (§2.4)** — recursion_recursion_outline_nova, recursion_recursion_outline_supernova, recursion_recursion_outline_hypernova, recursion_recursion_outline_protostar, recursion_recursion_outline_cyclefold [EXTRACTED 1.00]
- **Four-Graph Knowledge Pipeline** — docs_superpowers_specs_2026_06_12_knowledge_graph_references_design_graphify_out, docs_superpowers_specs_2026_06_12_book_graph_comparison_design_book_graph, docs_superpowers_specs_2026_06_13_recursion_graph_design_recursion_graph, docs_superpowers_specs_2026_06_13_master_graph_design_master_graph [EXTRACTED 1.00]
- **Reference Fetch Infrastructure** — docs_superpowers_plans_2026_06_12_knowledge_graph_references_fetch_references, docs_superpowers_plans_2026_06_12_knowledge_graph_references_two_tier_fetch, docs_superpowers_specs_2026_06_12_eprint_cloudflare_stealth_tier_design_stealth_tier, docs_superpowers_plans_2026_06_12_knowledge_graph_references_reference_manifest [EXTRACTED 1.00]
- **Second Edition Authoring Program** — docs_superpowers_specs_2026_06_14_book_outline_design_spec, docs_superpowers_specs_2026_06_13_master_graph_design_master_graph, docs_superpowers_specs_2026_06_13_master_graph_design_concepts_for_book, docs_superpowers_specs_2026_06_14_math_explainer_skill_design_six_stage_pipeline [INFERRED 0.75]
- **Proof Core Triad (Field + Commitment + Arithmetization)** — proving_nothing_arithmetization, proving_nothing_polynomial_commitment_scheme, proving_nothing_small_field_revolution, proving_nothing_proof_core [EXTRACTED 1.00]
- **Production Systems Following the Hybrid STARK-to-SNARK Pipeline** — proving_nothing_sp1_hypercube, proving_nothing_risc_zero, proving_nothing_airbender, proving_nothing_stwo, proving_nothing_hybrid_pipeline [EXTRACTED 1.00]
- **Folding Scheme Genealogy (Nova to Symphony)** — proving_nothing_nova, proving_nothing_supernova, proving_nothing_hypernova, proving_nothing_protostar, proving_nothing_protogalaxy, proving_nothing_cyclefold, proving_nothing_latticefold, proving_nothing_latticefold_plus, proving_nothing_neo, proving_nothing_symphony [EXTRACTED 1.00]

## Communities (79 total, 8 thin omitted)

### Community 0 - "Graphify Pipeline & Audit Trail"
Cohesion: 0.06
Nodes (67): Andrej Karpathy, Structural AST Extraction, Edge Confidence Audit Trail (EXTRACTED/INFERRED/AMBIGUOUS), Post-Commit Rebuild Hook, Community Detection, Semantic Extraction Cache, God Nodes, Graph Query (BFS/DFS Traversal) (+59 more)

### Community 1 - "PDF Build Pipeline"
Cohesion: 0.05
Nodes (52): ArgumentParser, CompletedProcess, PDF Build Pipeline, zkbook_pdf Package, BuildLog, Shared logging helpers for PDF build workflows., Collect log lines and mirror them to stdout and an optional file., build_parser() (+44 more)

### Community 2 - "Book-Graph Builder"
Cohesion: 0.05
Nodes (48): cmd_augment(), cmd_build(), _dump_communities(), _export(), _export_with_communities(), _load(), main(), merge_extraction() (+40 more)

### Community 3 - "Master-Graph Builder"
Cohesion: 0.07
Nodes (61): _all_papers(), _append_manifest_entries(), build_alias_map(), chapter_of(), citation_key(), cmd_concepts(), cmd_consolidate(), cmd_merge() (+53 more)

### Community 4 - "Dependency Resolution & Evals"
Cohesion: 0.10
Nodes (45): main(), main(), parse_strata(), resolve(), _is_nonempty_str(), _str_list(), validate_accuracy_report(), validate_bundle() (+37 more)

### Community 5 - "Reference Fetcher"
Cohesion: 0.07
Nodes (35): atomic_write(), _clear_cloudflare(), _curl_get(), fetch_paper(), _fetch_paper_stealth(), fetch_web_text(), is_pdf(), load_manifest() (+27 more)

### Community 6 - "Wiki Scraper"
Cohesion: 0.07
Nodes (41): already_ingested(), build_frontmatter(), _check_deps(), content_hash(), _content_type_from_page(), crawl_site(), CrawlBudget, dedup_key() (+33 more)

### Community 7 - "Manim Merkle Scenes"
Cohesion: 0.08
Nodes (24): H(), MerkleTreesScene, node(), Scene, _angle(), _commit(), PedersenCommitment, _pos() (+16 more)

### Community 8 - "PDF Graph Deepening"
Cohesion: 0.12
Nodes (27): anchors_for_source(), batch_for_ids(), cmd_finalize(), cmd_jobs(), cmd_merge(), cmd_relabel(), graph_stats(), load_fragment() (+19 more)

### Community 9 - "Folding Schemes & Nova Lineage"
Cohesion: 0.16
Nodes (26): Abhiram Kothapalli, Binyi Chen, CCS (Customizable Constraint Systems), Chapter 6: Layer 5 -- The Sealed Certificate, CycleFold, Dan Boneh, Folding (Snowball), GGPR 2013: Quadratic Span Programs and Succinct NIZKs (+18 more)

### Community 10 - "Master-Graph Tests"
Cohesion: 0.12
Nodes (16): _g(), Minimal node-link graph dict for tests., test_build_alias_map_collapses_variants_to_highest_degree(), test_build_alias_map_skips_unlabeled_nodes(), test_coverage_diff_tags_absent_under_and_well_covered(), test_coverage_diff_well_covered_and_wiki_chapter(), test_degree_map_counts_incidence(), test_degree_map_counts_self_loop_twice() (+8 more)

### Community 11 - "zkVMs & Small Fields"
Cohesion: 0.17
Nodes (24): BabyBear Field (31-bit), Barry Whitehat, Chapter 5: Encoding the Performance (Layer 4 -- Arithmetization), Chapter 11: zkVMs -- The Universal Stage, Jolt zkVM, Justin Thaler, Lasso (2023), LFKN 1992: Algebraic Methods for Interactive Proof Systems (+16 more)

### Community 12 - "Trusted Setup Ceremonies"
Cohesion: 0.14
Nodes (23): ADOPT Framework (Available/Decentralized/Open/Persistent/Transparent), Andrew Miller, Ariel Gabizon, BCTV14 Bug (CVE-2019-7167), BGM17 MMORPG Ceremony Protocol, Capex/Opex Setup Economics Framework, Chapter 2: Layer 1 -- Building the Stage, Ethereum KZG Summoning Ceremony (141,416 participants, 2023) (+15 more)

### Community 13 - "Math-Explainer Pipeline"
Cohesion: 0.13
Nodes (22): bundle.json Artifact Schema, check_env.py, manim_render.py, math-explainer Skill Implementation Plan, resolve_deps.py, run_sage.py, scorecard.py, Five Eval Concepts (+14 more)

### Community 14 - "MOOC Lecture Ingestion"
Cohesion: 0.14
Nodes (21): chunk_text(), cmd_fetch(), cmd_merge(), _dump_json(), fetch_slides(), fetch_transcript(), lecture_paths(), _load() (+13 more)

### Community 16 - "Draft Linter"
Cohesion: 0.19
Nodes (17): _anaphora(), lint_draft(), main(), Flag paragraphs where >=3 sentences open with the same first three words., Flag body references to the draft's own home chapter (rule 11). The home…, Return prose-hygiene findings as strings (empty == clean)., _self_chapter_ref(), test_ai_vocab_heading_flagged() (+9 more)

### Community 17 - "Sage Figure Runner"
Cohesion: 0.22
Nodes (16): main(), parse_manifest(), Path, Return the last stdout line that parses as a JSON object., Validate a manifest's figure path and return it as a Path. Correct-by-…, run_recipe(), validate_figure(), skipif (+8 more)

### Community 18 - "Manim Renderer"
Cohesion: 0.22
Nodes (15): main(), Path, Return mismatch messages for keys present in both dicts. Keys absent from the…, Render a manim scene and return the output media path. Drives a local manim…, render_scene(), validate_scene_values(), skipif, test_bool_int_drift_flagged() (+7 more)

### Community 19 - "Interactive Proofs & GMR"
Cohesion: 0.18
Nodes (17): Chapter 1: The Promise of Provable and Programmable Secrets, Chapter 13: The Market Landscape, Charles Rackoff, Completeness, eIDAS 2.0 (EU Digital Identity Regulation), GMR 1985: The Knowledge Complexity of Interactive Proof Systems, Interactive Proof, Privacy as a Luxury Good (+9 more)

### Community 20 - "Paper Vector Extraction"
Cohesion: 0.28
Nodes (15): build_frontmatter(), extract_manifest(), extract_pdf_to_markdown(), is_safe_manifest_file(), load_manifest(), main(), manifest_pdf_path(), paper_slug() (+7 more)

### Community 21 - "Commitments & Hard Problems"
Cohesion: 0.23
Nodes (16): Ajtai / Lattice Commitments, BN254 Curve (~100-bit security after Tower NFS), Bulletproofs / Inner Product Argument (IPA), Chapter 7: Layer 6 -- The Deep Craft, Discrete Logarithm Problem, Greyhound (Lattice SNARK, 2024), Module-SIS, NIST PQC Standards (FIPS 203/204/205) (+8 more)

### Community 22 - "Recursion & Curve Cycles"
Cohesion: 0.13
Nodes (15): BCTV, Scalable ZK via Cycles of Elliptic Curves (CRYPTO 2014), Verification-Key Binding Failures, Customizable Constraint Systems (CCS), Elliptic Curve Cycles, CycleFold, Full Recursion, HyperNova, Nguyen-Boneh-Setty, Revisiting Nova on a Cycle of Curves (ePrint 2023/969) (+7 more)

### Community 23 - "Environment Probe"
Cohesion: 0.27
Nodes (9): main(), missing(), mode(), probe(), Report the pipeline's multimodal capability from the probe. - ``full-…, Return the subset of `required` tool names that are not available., test_missing_empty_required_is_satisfied(), test_mode_consistent_with_probe() (+1 more)

### Community 24 - "Privacy Technologies"
Cohesion: 0.22
Nodes (14): Andrew Yao, Chapter 9: Privacy-Enhancing Technologies, Craig Gentry, Differential Privacy, Fully Homomorphic Encryption (FHE), GDPR, Kachina (Privacy as a Parameter), Secure Multi-Party Computation (MPC) (+6 more)

### Community 25 - "Teaching Method (Sanderson/Tao)"
Cohesion: 0.27
Nodes (13): Stage 4 Accuracy Protocol, Stage 1 Dependency Protocol, Draft-Quality Rules, Sanderson Moves, Tao: There's More to Mathematics than Rigour and Proofs, Tao Staging, math-explainer Skill, Six-Stage Explanation Pipeline (+5 more)

### Community 26 - "Wiki Mapping Program"
Cohesion: 0.19
Nodes (13): build_manifest.py, Entity Map (entity-map.json), Improvement Backlog (IMPROVEMENT_BACKLOG.md), 14 Parallel Chapter Extraction Agents, Sevenlayer Wiki Mapping Plan, reconcile.py, Section Manifest (section-manifest.json), Five Audit Dimensions (Accuracy, Citations, Clarity, Coherence, Depth) (+5 more)

### Community 27 - "ZK Languages & Circuits"
Cohesion: 0.31
Nodes (13): ACIR (Abstract Circuit Intermediate Representation), Chapter 3: Choreographing the Act (Layer 2 -- Language), Chaliasos et al. SoK: What Don't We Know? (USENIX Security 2024), Circom, Compact (Midnight DSL), Disclosure Analysis / disclose() Boundary, Four Layer-2 Language Philosophies, Leo (Aleo) (+5 more)

### Community 28 - "Witness Generation"
Cohesion: 0.27
Nodes (13): Alex Ozdemir, Algebraic RAM Consistency Checking, BatchZK (Pipelined Proving), Chapter 4: The Secret Performance (Layer 3 -- Witness Generation), Constant-Time Proving, Execution Trace, Reinforced Concrete Hash (Cache-Timing Vulnerable), Remote Side-Channel Attacks on Anonymous Transactions (USENIX 2020) (+5 more)

### Community 29 - "Midnight Case Study"
Cohesion: 0.22
Nodes (13): Arithmetization, BLS12-381 Curve, Chapter 12: Midnight -- The Privacy Theater, Jubjub Curve, Midnight, Nullifier, PLONKish Arithmetization, Pluto-Eris Curve Cycle (+5 more)

### Community 30 - "Proving Nothing"
Cohesion: 0.19
Nodes (13): Proving Nothing: A Layered Guide to Zero-Knowledge Proof Systems, The Cascade Effect / One-Way Door, Seven-Layer Causal DAG (14 Edges), Chapter 10: The Synthesis -- Three Paths, Not Two, Chapter 14: Open Questions and the Road Ahead, Charles Hoskinson, Path Three: Post-Quantum Folding, Seven-Layer Model (+5 more)

### Community 31 - "Recursion Outline"
Cohesion: 0.18
Nodes (13): Aggregation Trees, Chiesa-Tromer, Proof-Carrying Data (ICS 2010), Folding Schemes, Incrementally Verifiable Computation (IVC), Proof-Carrying Data (PCD), ProtoStar / ProtoGalaxy, Recursion Gap, Recursive Proof Composition Outline (+5 more)

### Community 32 - "2026 06 12 Book Graph Comparison Design"
Cohesion: 0.21
Nodes (12): Book Graph (book-graph/), Per-Chapter Split Extraction, Reference Subgraph Augmentation, Book Graph Comparison Design Spec, Vocabulary Drift Risk, Additive Anchored Extraction, Additive Invariant (node count never decreases), Shared concept_<kebab> Node IDs (+4 more)

### Community 33 - "Proving Nothing"
Cohesion: 0.29
Nodes (12): Aligned Layer, Beanstalk Flash-Loan Governance Attack ($182M, 2022), Celestia, Chapter 8: Layer 7 -- The Verdict, DA-Saturation Attack, Data Availability, EIP-4844 Blobs, Flash Loan (+4 more)

### Community 34 - "Test Paper Vector"
Cohesion: 0.29
Nodes (7): _paper(), test_extract_manifest_idempotent_with_stubbed_extractor(), test_load_manifest_accepts_object_and_array(), test_paper_slug_is_stable_and_ranked(), test_validate_manifest_enforces_expected_count(), test_validate_manifest_rejects_duplicate_slugs(), test_validate_manifest_rejects_unsafe_file_paths()

### Community 35 - "2026 06 14 Mooc Lecture Ingestion"
Cohesion: 0.24
Nodes (11): merge_fragment Additive Merge, fetch_references.py, build_master_graph.py, Dual-Interpreter Discipline, ingest_lecture.py, MOOC Lecture Ingestion Plan, Canonical slides.pdf source_file, Berkeley ZKP MOOC Lecture 1 (Goldwasser) (+3 more)

### Community 36 - "2026 06 13 Master Graph"
Cohesion: 0.20
Nodes (11): build_alias_map Deterministic Dedup, coverage_diff Verdicts, Hub LLM Synonym Pass, merge_graphs with Origin Tracking, Master Knowledge Graph Plan, score_concepts Ranking, should_stop Bounded Stop-Check, Bounded Citation Snowball (+3 more)

### Community 37 - "Test Manifest"
Cohesion: 0.33
Nodes (10): curated(), load(), Hand-curated bibliography entries (snowball discoveries excluded)., Auto-discovered entries appended by the citation snowball., snowball(), test_entry_shape(), test_every_bibliography_ref_present_exactly_once(), test_slugs_are_kebab_case_and_unique() (+2 more)

### Community 38 - "2026 06 12 Eprint Cloudflare Stealth Tie"
Cohesion: 0.27
Nodes (10): _CF_SESSIONS Per-Origin Cache, _fetch_paper_stealth, _looks_like_cloudflare Detector, ePrint Cloudflare Stealth Tier Plan, In-Flight Premise Corrections, cf_clearance Cookie + UA Reuse, Clear the Challenged PDF URL, ePrint Cloudflare Stealth Tier Design Spec (+2 more)

### Community 39 - "2026 06 14 Book Outline Design"
Cohesion: 0.20
Nodes (10): Debt Ledger Device, Feynman Spiral (met intuitively, locked rigorously), IOP + PCS = SNARK Unification, Midnight Production Case Study, Part III Dependency-Pure Rigorous Engine, Single Forward Pass Structure, Six-Lens Architect Synthesis, Book Outline Design (2nd Edition) (+2 more)

### Community 41 - "Test Recursion Manifest"
Cohesion: 0.33
Nodes (9): curated(), load(), Hand-curated recursion bibliography (snowball discoveries excluded)., Auto-discovered entries appended by the citation snowball., snowball(), test_entry_shape(), test_ids_unique_and_sorted(), test_slugs_kebab_and_unique() (+1 more)

### Community 42 - "Pipeline"
Cohesion: 0.28
Nodes (9): accuracy_report, Correct-by-Construction Figures, concept_brief, Graphify Best-Effort Enrichment, bundle.json Bundle, comprehension_set, stuck_points, schemas.py (+1 more)

### Community 43 - "Build Kindle"
Cohesion: 0.31
Nodes (8): build_epub(), check_tools(), main(), normalize_source(), Verify pandoc is available., Strip the manual TOC and normalize the source for EPUB conversion. Mirrors the…, Run pandoc to generate EPUB3., Kindle EPUB Pipeline

### Community 44 - "Multilinear Extension"
Cohesion: 0.28
Nodes (7): bil(), _heat_color(), MultilinearExtension, Scene, manim scene for the multilinear extension (MLE). Extends 4 discrete corner…, Bilinear (multilinear, n=2) extension: linear in each coordinate., Map a value in [1,6] to a cool->warm color for the surface fill.

### Community 45 - "Proving Nothing"
Cohesion: 0.25
Nodes (9): Airbender (ZKsync), Circle STARKs, Ethereum Foundation Security Pivot (Dec 2025), Mersenne-31 Field (M31), Real-Time Ethereum Proving, Shahar Papini, Stwo (StarkWare Circle STARK Prover), Three Frontiers (Performance/Security/Privacy) (+1 more)

### Community 46 - "Proving Nothing"
Cohesion: 0.28
Nodes (9): Groth16 (192-byte proofs), Halo (Recursion Without Pairings), Halo 2, Hybrid STARK-to-SNARK Pipeline, Jens Groth, KZG Commitment (Kate-Zaverucha-Goldberg), PLONK, Recursive Proof Composition (Russian Doll) (+1 more)

### Community 47 - "Test Deepen Pdfs"
Cohesion: 0.28
Nodes (8): consolidate_nodes(), merge_fragment(), Merge duplicate nodes: drop alias ids, redirect their edges to the canonical…, Additively merge a fragment into a node-link graph. Union nodes by id (existing…, test_consolidate_nodes_drops_edges_to_missing_canonical(), test_consolidate_nodes_redirects_and_drops_dups(), test_merge_fragment_enforces_additive_invariant(), test_merge_fragment_is_additive_and_dedups()

### Community 48 - "Mini Foundations"
Cohesion: 0.32
Nodes (8): Dual-Interpreter Rule, Finite Fields F_p, Pedersen Commitment (vector form), Schwartz-Zippel Lemma, MATH_FOUNDATIONS.md, LatticeFold, Pedersen Commitments in Folding, resolve_deps.py

### Community 49 - "2026 06 12 Book Graph Comparison"
Cohesion: 0.25
Nodes (8): build_book_graph.py, compare_graphs.py, Concept-Label Jaccard Comparison, merge_extraction Helper, Book Graph Comparison Plan, reference_subgraph Helper, split_manuscript.py, build_recursion_graph.py

### Community 50 - "2026 06 13 Recursion Graph"
Cohesion: 0.25
Nodes (8): fetch_references --manifest Flag, Recursion Graph Plan, Reuse Entries for 9 Overlap Papers, split_recursion_outline.py, Recursion Reference Corpus (references/recursion/), Recursion Graph (recursion-graph/), Recursion Outline (3 Chapters), Recursion Graph Design Spec

### Community 51 - "Proving Nothing"
Cohesion: 0.36
Nodes (8): AIR (Algebraic Intermediate Representation), Collision-Resistant Hash Functions, Eli Ben-Sasson, FRI (Fast Reed-Solomon IOP of Proximity), Grover's Algorithm, Path Two: Pure Transparent, STARK, Transparent Setup

### Community 52 - "Proving Nothing"
Cohesion: 0.25
Nodes (8): Cairo, Jordi Baylina, Linea, Polygon zkEVM (Sunset 2025/26), Scroll, Starknet, ZisK, ZK Rollup

### Community 53 - "Recursion Outline"
Cohesion: 0.25
Nodes (8): Seven-Layer ZK Stack, Continuations / Sharding, Fractal, Hybrid Proving Pipelines, Plonky2, Real-Time L1 Proving, Rollups and Proof Compression, STARK Recursion

### Community 54 - "Elliptic Curves"
Cohesion: 0.38
Nodes (5): add_points(), EllipticCurvesScene, inv_mod(), mul_point(), Scene

### Community 55 - "Schwartz Zippel"
Cohesion: 0.38
Nodes (5): _p(), Scene, _q(), manim scene for the Schwartz-Zippel lemma (pilot). Animates the random-point…, SchwartzZippel

### Community 57 - "2026 06 12 Deepen Pdf Graph"
Cohesion: 0.29
Nodes (7): anchors_for_source, Batch-1 Checkpoint Gate, batch_for_ids, deepen_pdfs.py, Do Not Run graphify update on the Content Graph, Deep PDF Mining Plan, Pilot-Then-Parallel Orchestration

### Community 58 - "2026 06 12 Knowledge Graph References"
Cohesion: 0.29
Nodes (7): Knowledge Graph + Reference Corpus Plan, Reference Manifest (references/manifest.json), Stub Entries for Print-Only Sources, Two-Tier Scrapling Fetch, Graph Corpus: Manuscript + References + Wiki, Manifest-Driven Pipeline, Knowledge Graph + Reference Corpus Design Spec

### Community 59 - "Proving Nothing"
Cohesion: 0.29
Nodes (7): Adi Shamir, Amos Fiat, Fiat-Shamir 1986 (Crypto '86), Fiat-Shamir Transform, Frozen Heart Vulnerability Class (2022), Last Challenge Attack (gnark, 2023/24), Solana ZK ElGamal Fiat-Shamir Bugs (2025)

### Community 60 - "Readme"
Cohesion: 0.38
Nodes (7): Midnight Case Study, Proving Nothing, 4x4 Sudoku Running Example, Extractor Blowup, Khovratovich et al., How to Prove False Statements (ePrint 2025/118), Fiat-Shamir in IVC, Release v1.10

### Community 61 - "Audit Checks"
Cohesion: 0.67
Nodes (5): _dependency_check(), main(), _paper_vector_temp_idempotency(), _run(), run_checks()

### Community 62 - "Lint"
Cohesion: 0.60
Nodes (5): _ftype(), _has_frontmatter(), lint(), main(), _target()

### Community 63 - "Bilinear Pairings"
Cohesion: 0.40
Nodes (3): BilinearPairings, Scene, manim scene for bilinear pairings (Chapter 11). Depicts the pairing e : G1 x G2…

### Community 64 - "Discrete Log"
Cohesion: 0.50
Nodes (3): DiscreteLogScene, pos(), Scene

### Community 65 - "Recursion Outline"
Cohesion: 0.40
Nodes (5): Atomic Accumulation, BCMS, PCD from Accumulation Schemes (TCC 2020), Halo, Mina / Coda, Pickles

## Ambiguous Edges - Review These
- `resolve_deps.py` → `Schwartz-Zippel Lemma`  [AMBIGUOUS]
  .claude/skills/math-explainer/tests/fixtures/mini_foundations.md · relation: shares_data_with
- `Schwartz-Zippel Lemma` → `R1CS`  [AMBIGUOUS]
  .claude/skills/math-explainer/tests/fixtures/mini_foundations.md · relation: conceptually_related_to
- `Mersenne-31 Field (M31)` → `Airbender (ZKsync)`  [AMBIGUOUS]
  proving-nothing.md · relation: references

## Knowledge Gaps
- **102 isolated node(s):** `zkbook-pdf-builder`, `Community Detection`, `Semantic Extraction Cache`, `God Nodes`, `Obsidian Vault Export` (+97 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `resolve_deps.py` and `Schwartz-Zippel Lemma`?**
  _Edge tagged AMBIGUOUS (relation: shares_data_with) - confidence is low._
- **What is the exact relationship between `Schwartz-Zippel Lemma` and `R1CS`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Mersenne-31 Field (M31)` and `Airbender (ZKsync)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `merge_fragment()` connect `Test Deepen Pdfs` to `PDF Graph Deepening`, `Book-Graph Builder`, `Master-Graph Builder`, `MOOC Lecture Ingestion`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `Proving Nothing` connect `Readme` to `Teaching Method (Sanderson/Tao)`, `Recursion Outline`, `PDF Build Pipeline`, `Recursion Outline`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Why does `Proving Nothing: A Layered Guide to Zero-Knowledge Proof Systems` connect `Proving Nothing` to `Proving Nothing`, `Folding Schemes & Nova Lineage`, `zkVMs & Small Fields`, `Trusted Setup Ceremonies`, `Interactive Proofs & GMR`, `Commitments & Hard Problems`, `Privacy Technologies`, `ZK Languages & Circuits`, `Witness Generation`, `Midnight Case Study`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **What connects `zkbook-pdf-builder`, `Community Detection`, `Semantic Extraction Cache` to the rest of the system?**
  _102 weakly-connected nodes found - possible documentation gaps or missing edges._