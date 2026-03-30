"""Pandoc + XeLaTeX PDF build workflow."""

from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .buildlog import BuildLog


TOC_PATTERN = re.compile(
    r"^# Table of Contents\r?\n.*?(?=\r?\n^# )",
    flags=re.MULTILINE | re.DOTALL,
)
HR_BEFORE_HEADING_PATTERN = re.compile(
    r"^---\s*$\r?\n(?=^#{1,4} )",
    flags=re.MULTILINE,
)
# Strip --- lines immediately before Part headings (e.g. "# Part I:")
HR_BEFORE_PART_PATTERN = re.compile(
    r"^---\s*$\r?\n(?=^# Part [IVX]+:)",
    flags=re.MULTILINE,
)
# Strip --- lines immediately after Part headings
HR_AFTER_PART_PATTERN = re.compile(
    r"(^# Part [IVX]+:.*\r?\n)\r?\n?^---\s*$",
    flags=re.MULTILINE,
)
SUPPORTED_BOX_CLASSES = {"technical", "insight", "caution", "example", "patient", "regulatory"}
MIN_PDF_SIZE_BYTES = 100_000
LATEX_AUX_EXTENSIONS = (".aux", ".log", ".out", ".toc")


@dataclass(slots=True)
class NormalizationResult:
    """Normalized markdown plus normalization metadata."""

    text: str
    manual_toc_removed: bool
    inserted_blank_lines: int
    stripped_part_hrs: int


@dataclass(slots=True)
class LatexBuildConfig:
    """Configuration for the Pandoc + XeLaTeX workflow."""

    source: Path
    output: Path
    log_path: Path
    temp_path: Path
    assets_dir: Path
    keep_temp: bool = False

    @property
    def asset_paths(self) -> dict[str, Path]:
        return {
            "preamble.tex": self.assets_dir / "preamble.tex",
            "coverpage.tex": self.assets_dir / "coverpage.tex",
            "licensepage.tex": self.assets_dir / "licensepage.tex",
            "box-filter.lua": self.assets_dir / "box-filter.lua",
        }

    @property
    def temp_tex_path(self) -> Path:
        return self.temp_path.with_suffix(".tex")

    @property
    def latex_auxiliary_paths(self) -> list[Path]:
        return [self.output.with_suffix(ext) for ext in LATEX_AUX_EXTENSIONS]


def first_line(text: str) -> str:
    """Return the first non-empty line from text."""

    return text.splitlines()[0].strip() if text.splitlines() else ""


def ensure_blank_line_before_h1(text: str) -> tuple[str, int]:
    """Insert a blank line before top-level headings when missing."""

    lines = text.splitlines()
    normalized: list[str] = []
    inserted = 0
    for line in lines:
        if line.startswith("# ") and normalized and normalized[-1].strip():
            normalized.append("")
            inserted += 1
        normalized.append(line)
    normalized_text = "\n".join(normalized)
    if text.endswith("\n"):
        normalized_text += "\n"
    return normalized_text, inserted


def strip_part_adjacent_hrs(text: str) -> tuple[str, int]:
    """Remove horizontal rules immediately before or after Part headings."""

    count = 0
    text, n = HR_BEFORE_PART_PATTERN.subn("", text)
    count += n
    text, n = HR_AFTER_PART_PATTERN.subn(r"\1", text)
    count += n
    return text, count


def normalize_markdown(text: str) -> NormalizationResult:
    """Strip the manual TOC, normalize chapter spacing, and clean Part HRs."""

    had_manual_toc = bool(TOC_PATTERN.search(text))
    normalized = TOC_PATTERN.sub("", text, count=1)
    normalized = normalized.lstrip("\ufeff\r\n")
    # Strip a leading --- that Pandoc could misinterpret as YAML frontmatter
    normalized = re.sub(r"^---\s*\n", "", normalized)
    normalized = normalized.lstrip("\r\n")
    normalized, inserted_blank_lines = ensure_blank_line_before_h1(normalized)
    normalized, stripped_part_hrs = strip_part_adjacent_hrs(normalized)
    if not normalized.endswith("\n"):
        normalized += "\n"
    return NormalizationResult(
        text=normalized,
        manual_toc_removed=had_manual_toc,
        inserted_blank_lines=inserted_blank_lines,
        stripped_part_hrs=stripped_part_hrs,
    )


def probe_command(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    """Run a short command and capture its output."""

    return subprocess.run(
        command,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )


def run_command(
    command: list[str],
    *,
    cwd: Path,
    description: str,
    log: BuildLog,
) -> None:
    """Run a command while streaming output into the build log."""

    log.info(f"Running {description}: {' '.join(command)}")
    process = subprocess.Popen(
        command,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert process.stdout is not None
    for line in process.stdout:
        stripped = line.rstrip()
        if stripped:
            log.info(f"{description} output: {stripped}")
    return_code = process.wait()
    if return_code != 0:
        raise RuntimeError(f"{description} failed with exit code {return_code}")


def audit_source(config: LatexBuildConfig, log: BuildLog) -> str:
    """Inspect the markdown source for formatting risks."""

    log.section("source-audit")
    if not config.source.exists():
        raise FileNotFoundError(f"Source file not found: {config.source}")

    text = config.source.read_text(encoding="utf-8")
    line_count = len(text.splitlines())
    headings = {
        "h1": len(re.findall(r"^# ", text, flags=re.MULTILINE)),
        "h2": len(re.findall(r"^## ", text, flags=re.MULTILINE)),
        "h3": len(re.findall(r"^### ", text, flags=re.MULTILINE)),
        "h4": len(re.findall(r"^#### ", text, flags=re.MULTILINE)),
    }
    hr_count = len(re.findall(r"^---\s*$", text, flags=re.MULTILINE))
    fenced_div_classes = re.findall(
        r"^:::\s*\{\.([A-Za-z0-9_-]+)\}",
        text,
        flags=re.MULTILINE,
    )
    unknown_divs = sorted(
        {name for name in fenced_div_classes if name not in SUPPORTED_BOX_CLASSES}
    )
    hr_before_heading = len(HR_BEFORE_HEADING_PATTERN.findall(text))
    part_headings = len(re.findall(r"^# Part [IVX]+:", text, flags=re.MULTILINE))
    table_count = len(re.findall(r"^\|.*\|.*\|", text, flags=re.MULTILINE))

    log.info(
        "Line count: "
        f"{line_count}; headings: H1={headings['h1']}, H2={headings['h2']}, "
        f"H3={headings['h3']}, H4={headings['h4']}"
    )
    log.info(
        "Structural counts: "
        f"horizontal_rules={hr_count}, "
        f"part_headings={part_headings}, "
        f"table_rows={table_count}, "
        f"fenced_divs={len(fenced_div_classes)}"
    )
    if TOC_PATTERN.search(text):
        log.info("Manual markdown TOC detected and will be stripped in normalization.")
    else:
        log.info("No manual markdown TOC detected.")
    if hr_before_heading:
        log.warn(
            f"Found {hr_before_heading} horizontal rules immediately before a heading."
        )
    if hr_count > 30:
        log.warn(
            f"Found {hr_count} horizontal rules; design guidance recommends sparse usage."
        )
    if unknown_divs:
        log.warn(
            "Unsupported fenced div classes present: " + ", ".join(unknown_divs)
        )
    return text


def preflight(config: LatexBuildConfig, log: BuildLog) -> None:
    """Verify tools and assets exist before rendering."""

    log.section("preflight")
    pandoc_path = shutil.which("pandoc")
    if not pandoc_path:
        raise FileNotFoundError("Required executable not found on PATH: pandoc")
    log.info(f"Found pandoc: {pandoc_path}")
    pandoc_version = probe_command(["pandoc", "--version"], cwd=config.assets_dir)
    if pandoc_version.stdout.strip():
        for line in pandoc_version.stdout.strip().splitlines():
            log.info(f"pandoc --version stdout: {line}")
    if pandoc_version.stderr.strip():
        for line in pandoc_version.stderr.strip().splitlines():
            log.warn(f"pandoc --version stderr: {line}")
    pandoc_version_line = first_line(pandoc_version.stdout)
    if pandoc_version_line:
        log.info(f"pandoc version: {pandoc_version_line}")

    xelatex_path = shutil.which("xelatex")
    if not xelatex_path:
        raise FileNotFoundError("Required executable not found on PATH: xelatex")
    log.info(f"Found xelatex: {xelatex_path}")
    xelatex_version = probe_command(["xelatex", "--version"], cwd=config.assets_dir)
    if xelatex_version.stdout.strip():
        for line in xelatex_version.stdout.strip().splitlines():
            log.info(f"xelatex --version stdout: {line}")
    if xelatex_version.stderr.strip():
        for line in xelatex_version.stderr.strip().splitlines():
            log.warn(f"xelatex --version stderr: {line}")
    if xelatex_version.returncode != 0:
        raise RuntimeError(
            "XeLaTeX is installed but MiKTeX setup is incomplete. Finish the "
            "MiKTeX first-time setup and check for updates before building PDFs."
        )
    version_line = first_line(xelatex_version.stdout)
    if version_line:
        log.info(f"xelatex version: {version_line}")

    for asset_name, path in config.asset_paths.items():
        if not path.exists():
            raise FileNotFoundError(f"Required asset not found: {path}")
        log.info(f"Found asset {asset_name}: {path}")


def normalize_source(text: str, config: LatexBuildConfig, log: BuildLog) -> None:
    """Write normalized markdown to the temp source path."""

    log.section("normalizer")
    result = normalize_markdown(text)
    config.temp_path.write_text(result.text, encoding="utf-8")
    log.info(
        f"Wrote normalized source to {config.temp_path} "
        f"(manual_toc_removed={'yes' if result.manual_toc_removed else 'no'})."
    )
    if result.inserted_blank_lines:
        log.warn(
            "Inserted "
            f"{result.inserted_blank_lines} blank line(s) before top-level headings "
            "to keep Pandoc chapter parsing stable."
        )
    if result.stripped_part_hrs:
        log.info(
            f"Stripped {result.stripped_part_hrs} horizontal rule(s) adjacent to "
            "Part headings."
        )


def _patch_table_headers(tex_path: Path, log: BuildLog) -> None:
    """Inject dark-mode header row styling into longtable header blocks.

    Pandoc generates longtable headers with \\toprule ... \\endhead.
    We inject \\rowcolor{MidnightHeaderBg} after \\toprule and wrap
    header cell text in \\color{MidnightBold}\\bfseries to make
    header rows visually distinct from body rows.
    """
    import re

    text = tex_path.read_text(encoding="utf-8")
    original = text

    # Pattern: find \toprule followed by a header row ending with \\ before \endhead
    # Inject \rowcolor after \toprule
    text = re.sub(
        r"(\\toprule\n)",
        r"\1\\rowcolor{MidnightHeaderBg}\n",
        text,
    )

    # Add a blue midrule before \endhead for visual separation
    text = re.sub(
        r"(\\endhead)",
        r"\\arrayrulecolor{MidnightBlue}\\midrule\\arrayrulecolor{MidnightBorder}\n\1",
        text,
    )

    if text != original:
        tex_path.write_text(text, encoding="utf-8")
        count = text.count("\\rowcolor{MidnightHeaderBg}")
        log.info(f"Patched {count} longtable header row(s) with MidnightHeaderBg.")
    else:
        log.info("No longtable headers found to patch.")


def render_pdf(config: LatexBuildConfig, log: BuildLog) -> None:
    """Render markdown to PDF through standalone LaTeX."""

    log.section("renderer")
    pandoc_command = [
        "pandoc",
        str(config.temp_path),
        "-o",
        str(config.temp_tex_path),
        "--standalone",
        f"--include-before-body={config.asset_paths['coverpage.tex']}",
        f"--include-before-body={config.asset_paths['licensepage.tex']}",
        f"--include-in-header={config.asset_paths['preamble.tex']}",
        f"--lua-filter={config.asset_paths['box-filter.lua']}",
        "--toc",
        "--toc-depth=2",
        "--number-sections",
        "-V",
        "toc-title=Table of Contents",
        "-V",
        "geometry:margin=1in",
        "-V",
        "fontsize=11pt",
        "-V",
        "mainfont=STIX Two Text",
        "-V",
        "monofont=DejaVu Sans Mono",
        "-V",
        "mathfont=STIX Two Math",
        "-V",
        "linestretch=1.4",
        "-V",
        "documentclass=report",
        "-V",
        "classoption=openany",
        "--columns=80",
        "--highlight-style=assets/midnight-syntax.theme",
    ]
    run_command(
        pandoc_command,
        cwd=config.assets_dir,
        description="pandoc latex render",
        log=log,
    )

    # Post-process: style longtable header rows for dark mode
    _patch_table_headers(config.temp_tex_path, log)

    xelatex_command = [
        "xelatex",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-jobname={config.output.stem}",
        f"-output-directory={config.output.parent}",
        str(config.temp_tex_path),
    ]
    for pass_number in range(1, 3):
        run_command(
            xelatex_command,
            cwd=config.assets_dir,
            description=f"xelatex pass {pass_number}",
            log=log,
        )


def validate_output(config: LatexBuildConfig, log: BuildLog) -> None:
    """Verify that the expected PDF exists and is non-trivial in size."""

    log.section("validator")
    if not config.output.exists():
        raise FileNotFoundError(f"Expected PDF not found: {config.output}")
    size = config.output.stat().st_size
    log.info(f"Output PDF size: {size} bytes")
    if size < MIN_PDF_SIZE_BYTES:
        log.warn(
            f"Output PDF is smaller than {MIN_PDF_SIZE_BYTES} bytes; inspect manually."
        )


def cleanup_artifacts(config: LatexBuildConfig, log: BuildLog) -> None:
    """Remove temporary build artifacts unless debugging was requested."""

    if config.keep_temp:
        log.info("Keeping temporary files because --keep-temp was set.")
        return

    for temp_path in (config.temp_path, config.temp_tex_path):
        if temp_path.exists():
            try:
                temp_path.unlink()
                log.info(f"Removed temporary file: {temp_path}")
            except OSError as exc:
                log.warn(f"Could not remove temporary file: {exc}")

    for aux_path in config.latex_auxiliary_paths:
        if aux_path.exists():
            try:
                aux_path.unlink()
                log.info(f"Removed LaTeX auxiliary file: {aux_path}")
            except OSError as exc:
                log.warn(f"Could not remove LaTeX auxiliary file: {exc}")


def run_latex_build(config: LatexBuildConfig) -> int:
    """Execute the full LaTeX build workflow and return a process-style exit code."""

    log = BuildLog(path=config.log_path)
    config.output.parent.mkdir(parents=True, exist_ok=True)
    config.temp_path.parent.mkdir(parents=True, exist_ok=True)
    config.temp_tex_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        text = audit_source(config, log)
        preflight(config, log)
        normalize_source(text, config, log)
        render_pdf(config, log)
        validate_output(config, log)
        log.info(f"Build completed successfully: {config.output}")
        return_code = 0
    except Exception as exc:
        log.error(str(exc))
        return_code = 1
    finally:
        cleanup_artifacts(config, log)

    return return_code
