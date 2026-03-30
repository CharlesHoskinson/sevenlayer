"""CLI entrypoints for the ZK book PDF builder."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .latex import LatexBuildConfig, run_latex_build


def project_root() -> Path:
    """Return the project root directory from the package location."""

    return Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser for the LaTeX backend."""

    root = project_root()
    parser = argparse.ArgumentParser(
        description="Build the ZK book PDF via the packaged zkbook_pdf CLI.",
    )
    subparsers = parser.add_subparsers(dest="backend", required=True)

    latex_parser = subparsers.add_parser(
        "latex",
        help="Build the branded Pandoc + XeLaTeX PDF.",
    )
    latex_parser.add_argument(
        "--source",
        default=str(root / "proving-nothing.md"),
    )
    latex_parser.add_argument(
        "--output",
        default=str(root / "proving-nothing.pdf"),
    )
    latex_parser.add_argument(
        "--log",
        default=str(root / "zkbook_pdf_build.log"),
    )
    latex_parser.add_argument(
        "--temp",
        default=str(root / ".tmp_zkbook_notoc.md"),
    )
    latex_parser.add_argument("--assets-dir", default=str(root))
    latex_parser.add_argument("--keep-temp", action="store_true")

    return parser


def normalize_cli_argv(argv: Sequence[str] | None) -> list[str]:
    """Default to the LaTeX backend when the user omits a subcommand."""

    args = list(argv) if argv is not None else []
    if not args or args[0].startswith("-"):
        return ["latex", *args]
    return args


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entrypoint for packaged and wrapper-based invocation."""

    args = normalize_cli_argv(argv)
    parser = build_parser()
    namespace = parser.parse_args(args)

    config = LatexBuildConfig(
        source=Path(namespace.source).resolve(),
        output=Path(namespace.output).resolve(),
        log_path=Path(namespace.log).resolve(),
        temp_path=Path(namespace.temp).resolve(),
        assets_dir=Path(namespace.assets_dir).resolve(),
        keep_temp=bool(namespace.keep_temp),
    )
    return run_latex_build(config)
