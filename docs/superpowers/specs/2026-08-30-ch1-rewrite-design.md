# Chapter 1 Rewrite — Design (first chapter of the v2.0 second edition)

**Date:** 2026-08-30
**Status:** approved in discussion (rigor: inline semi-formal; length: ~13–15k words; pipeline: 5 stages with cross-vendor audit; voice: Hemingway profile active; anti-slop: enforced, not hoped)
**Program:** the book is developed chapter by chapter into a second edition. Version line: v1.10 (current, untouched) → **v2.0.0-dev** while chapters land under `v2/` → released as **v2.0** when all 14 are done. This spec covers chapter 1; the pipeline it establishes is the template for chapters 2–14.
**Inputs:** `learnobjectives.md` (ch1 goals, 5 personas), `learnobjectives-review.md` (ch1 scored 6.8/10 — crypto 4.0, engineer 5.8, economist 6.8, educator 7.5, assessor 9.8), the master graph's ch1 digest (`graphify-out/chapter-digest.md`)
**Drafting engine:** the installed inkwell plugin (`claude --plugin-dir /home/charl/inkwell`), real subagent pipeline

## 1. Why

The five-persona review found chapter 1 teaches its thesis well (trust-minimized vs trustless: 9–10 across personas) but fails four concrete demands: the 4×4 Sudoku arrives only as a late preview and is never played; the three properties are taught on the bouncer anecdote, unquantified; Fiat-Shamir's price (public-coin restriction, random-oracle assumption, weak-FS hazard) is never named; and the formal layer — probabilistic games, an actual simulator, soundness arithmetic — is absent. The rewrite closes these while keeping what scored 9+.

## 2. Voice contract (binding)

- **The Hemingway voiceprint profile is active for every drafting and revision round.** The dispatch prompt names the profile explicitly (inkwell resolution order #1: a profile named in the request). Under inkwell's authority table the active profile outranks the personas; persona findings that collide with measured Hemingway habits are dropped and logged.
- What this means concretely (from `hemingway.metrics.json`): median sentence ~7 words, ~65% of sentences under 10 words, em dash ≈0.83/1,000 words, parentheticals ≈0.10/1,000 (effectively never), semicolons rare, contractions in narration, `But`-openers a habit not an error. Short is the default; the long sentence is a release, deliberately rare.
- **Measured, not asserted:** after stages A, B/C, and D, run inkwell's `conformance.py` scoring the chapter against `hemingway.metrics.json`. Target: distribution verdict `close` on the final chapter. Inline math notation will drag the distribution; the scorer's number is reported honestly either way, and prose sentences—not formulas—carry the register.

## 3. Anti-slop contract (binding)

- The five-family tell audit (Content, Language, Style, Communication, Filler-and-hedging tells — taxonomy attributed to blader/humanizer) runs inside every Gottlieb edit round; tell findings are ordinary edit findings.
- The **humanizer skill runs as the final surface pass** after cadence (stage D), per the book's and inkwell's own guidance: writing first, humanizer last, no shared code.
- The repo's own `draft_lint.py` (math-explainer skill) runs on the final chapter: no pipeline/QA vocabulary in reader-facing prose, no anaphora runs.
- Banned by construction: rule-of-three flourishes, "delve/tapestry/pivotal/crucial" vocabulary, negative parallelism, uniform paragraph rhythm, em-dash crutches (the profile already caps them).

## 4. New chapter outline (~13.6k words; current 7,091)

| # | Section | Words | What changes |
|---|---|---|---|
| 1 | The Trick | ~800 | Kept, sharpened |
| 2 | **Play the Game** (new) | ~1,800 | The 4×4 Sudoku as a real interactive proof, three rounds played on the page, reader as verifier; commitment mechanics; per-round catch probability and rounds-to-2⁻⁴⁰ inline |
| 3 | The Proof at the Door | ~1,500 | Bouncer reframed as the social echo; completeness/soundness/ZK *derived from the played rounds*, stated semi-formally (Pr[accept]=1, soundness error ε, ZK via a constructed Sudoku simulator); risk-allocation contract: what each property insures, who bears residual loss |
| 4 | **Firing the Verifier** (new) | ~1,400 | Fiat-Shamir as a personnel change: public-coin restriction, the ROM theorem inline, what is unproven under SHA-256, weak-FS hazard forward-pointed to ch6 |
| 5 | The Phenomenon / Three Converging Forces | ~1,200 | Kept, tightened |
| 6 | The Seven Layers at a Glance | ~2,200 | Labeled stack diagram (assessor); SNARK-vs-STARK per-layer assumption audit — reduction-backed vs procedural (cryptographer) |
| 7 | **The Stack on Disk** (new) | ~1,500 | Circom+Groth16 ls-listing: `circuit.circom → .r1cs → .ptau → .wtns → proof.json → verifier`, each artifact pinned to its layer (engineer) |
| 8 | The Deepest Question | ~2,000 | Receipts kept; replacement-cost column priced for all seven layers (economist) |
| 9 | The First Decision / How to Read This Guide | ~1,200 | Kept; Sudoku threads backward naturally |

## 5. Pipeline (5 stages)

- **Stage A — Draft.** Three section-groups (§1–4, §5–7, §8–9), each drafted headless by the real inkwell pipeline (ground → zinsser draft → gottlieb edit with tell audit → apply), Hemingway profile named in every dispatch; then one stitch pass for seams and cross-references. Conformance score recorded.
- **Stage B — Panel revision.** The same five personas score the draft against their own ch1 goals (same 0–10 evidence-cited format); findings distilled into a revision brief; a gottlieb fix cycle applies it in voice.
- **Stage C — Cross-vendor audit.** Grok 4.6 and GPT-5.6 Sol cold-read as demanding line editors: AI-tell hunt, voice drift where inline formalism enters, factual spot-checks (soundness arithmetic, artifact names, citations), continuity with ch2–14. Confirmed findings applied; disagreements recorded, not silently resolved.
- **Stage D — Cadence + clarity.** leguin-reviser pass; target-reader loop (≤3 cycles, fresh-eyes agent, high/medium flags only); then the humanizer surface pass and `draft_lint.py`. Conformance re-scored.
- **Stage E — Re-score and land.** Panel re-scores the final chapter (before/after table); the chapter lands as `v2/ch01.md` — `proving-nothing.md` (v1.10) is never modified; structural verification (pandoc parse); PR with the score table, conformance number, and lint results in the description.

## 6. Success criteria

- Chapter mean **≥8.5** (from 6.8); cryptographer **≥7.0** (4.0); engineer **≥7.5** (5.8); no persona below 7.0; educator and assessor hold ≥9.
- Hemingway conformance verdict `close` on the final chapter (number reported regardless).
- Zero unresolved five-family tell findings; `draft_lint.py` clean; humanizer pass applied.
- Word count 13,000–15,000. All kept material that scored 9+ survives recognizably.

## 7. Mechanics and guardrails

- Work on branch `v2/ch01`; deliverable is `v2/ch01.md` plus `v2/README.md` (the second-edition program note). Stage outputs (`stageA.md`, `stageB.md`, …) live in `v2/.work/ch01/` — gitignored per the repo's `.work` convention — so every iteration is diffable locally without polluting the tree. `proving-nothing.md` stays v1.10, untouched.
- Headless inkwell dispatches follow the footguns discipline: `--plugin-dir /home/charl/inkwell`, scoped allowed tools, prompt via stdin, outputs verified nonempty and on-topic; transcript checked for real subagent dispatches.
- The book's factual content is not invented: new technical claims (round arithmetic, artifact names, assumption audit rows) must trace to the master graph or the chapter digest; anything unverifiable is cut, not hedged.
- Later-chapter dependencies: §4's weak-FS forward pointer must name ch6's Frozen Heart treatment as it actually exists; §7's artifact names must match ch2/ch3 usage (`.ptau`, `.r1cs`, `.wtns`).
