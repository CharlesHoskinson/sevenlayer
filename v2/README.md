# Proving Nothing — Second Edition (v2.0.0-dev)

The first edition (v1.10) is frozen in `proving-nothing.md`. This directory is
the second edition, built one chapter at a time.

Each chapter is rewritten against the learning objectives a five-persona
academic panel derived from the book's knowledge graph (`learnobjectives.md`),
and scored by the same panel before it lands (`learnobjectives-review.md`
holds the v1 baseline scores). The pipeline per chapter: three section-group
drafts by the inkwell writing pipeline, a panel revision round, a
cross-vendor editorial audit (Grok 4.6 + GPT-5.6 Sol), a cadence and
clarity pass, and a final panel re-score against explicit acceptance
criteria. Specs and plans live under `docs/superpowers/`.

Two contracts bind every chapter:

- **Voice.** The Hemingway voiceprint profile (inkwell's measured author
  profile) is active in every drafting and revision round, and the finished
  chapter is scored against `hemingway.metrics.json` by inkwell's
  conformance scorer. Short is the default. The long sentence is a release.
- **No AI slop.** The five-family tell audit runs inside every edit round;
  the humanizer pass and the repo's own `draft_lint.py` gate the final text.

Version plan: chapters land here as `chNN.md` under `2.0.0-dev`; when all
fourteen are done, the second edition assembles and releases as **v2.0**.

## Chapters

| Chapter | v1 panel score | v2 panel score | Conformance | Words | Landed |
|---|---|---|---|---|---|
| 1 — The Promise of Provable and Programmable Secrets | 6.8 | — | — | — | in progress |
