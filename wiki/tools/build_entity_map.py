"""Build entity-map.json: which sections mention which entities.

Seeds are case-insensitive substring matches against section body text.
Auto-discovery finds proper-noun-ish tokens (capitalized or ALL-CAPS acronyms)
that appear in >= 4 distinct sections.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


DEFAULT_SEEDS = [
    "midnight", "sudoku", "groth16", "plonk", "starks", "kzg", "fri",
    "lattice", "ajtai", "folding", "nova", "hypernova", "fiat-shamir",
    "small-field", "mersenne", "babybear", "goldilocks",
    "ceremony", "tornado cash", "beanstalk", "zcash", "poseidon",
    "circle stark", "jolt", "lasso", "logup", "spartan", "halo2",
    "bls12-381", "bn254", "jubjub",
]

# Body is everything between closing --- of frontmatter and ## Summary
BODY_RE = re.compile(r"^---\s*\n.*?\n---\s*\n(.*?)(?=^## Summary\s*$)", re.DOTALL | re.MULTILINE)
# Proper nouns: mixed-case word of 4+ chars, or all-caps acronyms of 2-6 chars
TOKEN_RE = re.compile(r"\b([A-Z][A-Za-z0-9]{3,}|[A-Z]{2,6}[0-9]*)\b")

# Common English words and generic ZK/crypto terms to exclude from auto-discovery
_STOPWORDS = {
    # English common words
    "the", "this", "that", "these", "those", "with", "from", "have", "been",
    "they", "them", "their", "there", "then", "than", "when", "what", "which",
    "where", "some", "each", "every", "over", "into", "only", "also", "even",
    "more", "most", "much", "many", "such", "both", "here", "just", "very",
    "will", "would", "could", "should", "must", "does", "were", "your",
    "about", "after", "before", "under", "while", "still", "other", "first",
    "second", "third", "three", "four", "five", "consider", "instead",
    "chapter", "chapters", "section", "layer", "layers", "proof", "proofs",
    "system", "systems", "block", "blocks", "data", "time", "true", "false",
    "note", "number", "point", "value", "field", "model", "level", "order",
    "step", "type", "case", "form", "part", "work", "make", "take", "need",
    "show", "know", "give", "come", "look", "used", "using", "given", "based",
    "called", "known", "means", "since", "whether", "through", "because",
    "between", "without", "however", "therefore", "although", "example",
    "examples", "version", "approach", "problem", "result", "results",
    "table", "figure", "read", "guide", "path", "stone",
    # Generic crypto/ZK domain words (not named entities)
    "performance", "security", "privacy", "question", "governance",
    "commitment", "summoning", "generation", "circuit", "circuits",
    "prover", "verifier", "protocol", "scheme", "hash", "curve",
    "group", "ring", "code", "program", "function", "input", "output",
    "paper", "papers", "cost", "size", "proving", "trust", "verification",
    "zero", "stark", "snark", "algebraic", "succinct", "post", "stage",
    "compact", "risc", "shamir", "fiat", "circle", "hypercube", "merkle",
    "plonkish", "zkir", "quantum", "shor", "december", "stage",
    # Abbreviations that are too generic
    "zk", "gpu", "gpus", "cpu", "cpus", "air", "srs", "evm",
    "r1cs", "bls12", "sp1", "stwo", "cairo", "rust",
    # Proper but too broad
    "ccs", "chaliasos", "ethereum", "bitcoin", "starkware",
    "circom", "tornado", "succinct",
    # More noise words caught by auto-discovery
    "think", "nothing", "neither", "seven", "fast", "change", "real",
    "small", "heart", "frozen", "everything", "nobody", "understanding",
    "production", "intermediate", "representation", "transparent",
    "computation", "network", "knowledge", "foundation", "constraint",
    "setup", "trusted", "witness", "module", "nothing", "april",
    "cash", "labs", "ir", "kb", "vm", "isa", "sis", "sha", "eth",
}


def extract_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = BODY_RE.search(text)
    return m.group(1) if m else text


def build(sections_dir: Path, seeds: list[str]) -> dict[str, list[str]]:
    bodies: dict[str, str] = {}
    for f in sorted(sections_dir.glob("*.md")):
        bodies[f.stem] = extract_body(f).lower()

    out: dict[str, list[str]] = {}
    for seed in seeds:
        s = seed.lower()
        hits = sorted(slug for slug, body in bodies.items() if s in body)
        out[seed] = hits

    # Auto-discovery: proper-noun-ish tokens in >= 8 distinct sections
    token_sections: dict[str, set[str]] = defaultdict(set)
    for f in sorted(sections_dir.glob("*.md")):
        body = extract_body(f)
        for m in TOKEN_RE.finditer(body):
            tok = m.group(1)
            token_sections[tok].add(f.stem)
    for tok, slugs in token_sections.items():
        key = tok.lower()
        if len(slugs) >= 8 and key not in out and key not in _STOPWORDS:
            out[key] = sorted(slugs)

    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sections", type=Path, required=True)
    p.add_argument("--seeds", nargs="*", default=DEFAULT_SEEDS)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    data = build(args.sections, args.seeds)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"{len(data)} entities mapped to {sum(len(v) for v in data.values())} total hits")


if __name__ == "__main__":
    main()
