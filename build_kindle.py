#!/usr/bin/env python3
"""
build_kindle.py — Generate Kindle-compatible EPUB from the master Markdown source.

Usage:
    python build_kindle.py [--source FILE] [--output FILE]

Follows Amazon Kindle Publishing Guidelines v2025.1:
- Reflowable format (Section 10)
- MathML for math content (Section 10.6)
- Simple HTML tables (Section 10.5)
- No forced body text styling (Section 10.3.2)
- EPUB3 with logical TOC
"""

import argparse
import subprocess
import sys
import os
import re
import shutil
import tempfile

DEFAULTS = {
    "source": "proving-nothing.md",
    "output": "proving-nothing.epub",
    "css": "kindle.css",
    "filter": "kindle-filter.lua",
    "metadata": "metadata.xml",
    "cover": None,  # Optional: path to cover image
    "temp": ".tmp_kindle_source.md",
}


def check_tools():
    """Verify pandoc is available."""
    result = subprocess.run(["pandoc", "--version"], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: pandoc not found. Install pandoc first.")
        sys.exit(1)
    version = result.stdout.split("\n")[0]
    print(f"  pandoc: {version}")


def normalize_source(source_path: str, temp_path: str):
    """
    Strip the manual TOC and normalize the source for EPUB conversion.
    Mirrors the normalization in build_pdf.py but adapted for EPUB.
    """
    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    result = []
    skip_toc = False
    prev_was_heading = False

    for i, line in enumerate(lines):
        # Skip frontmatter YAML
        if i == 0 and line.strip() == "---":
            # Find end of YAML frontmatter
            skip_toc = True
            result.append(line)
            continue
        if skip_toc and line.strip() == "---":
            skip_toc = False
            result.append(line)
            continue
        if skip_toc:
            result.append(line)
            continue

        # Normalize heading spacing: ensure blank line before headings
        if line.startswith("#"):
            if result and result[-1].strip() != "":
                result.append("")
            result.append(line)
            prev_was_heading = True
            continue

        # Suppress redundant --- adjacent to headings (filter handles the rest)
        if line.strip() == "---" and prev_was_heading:
            prev_was_heading = False
            continue

        prev_was_heading = False
        result.append(line)

    with open(temp_path, "w", encoding="utf-8") as f:
        f.write("\n".join(result))

    print(f"  Normalized source: {len(lines)} → {len(result)} lines")
    return temp_path


def build_epub(source: str, output: str, css: str, lua_filter: str,
               metadata: str, cover: str = None):
    """Run pandoc to generate EPUB3."""

    cmd = [
        "pandoc", source,
        "-o", output,
        "--standalone",
        "--css", css,
        "--lua-filter", lua_filter,
        "--toc", "--toc-depth=2",
        "--number-sections",
        "--mathml",
        "--epub-chapter-level=1",
        "--metadata", "title=Proving Nothing",
        "--metadata", "subtitle=A Complete Guide to Zero-Knowledge Proof Systems",
        "--metadata", "author=Charles Hoskinson",
        "--metadata", "lang=en",
        "--metadata", "date=2026-03-01",
        "--metadata", "rights=CC BY 4.0",
        "--columns=80",
    ]

    # Add metadata file if it exists
    if os.path.isfile(metadata):
        cmd.extend(["--epub-metadata", metadata])

    # Add cover image if provided and exists
    if cover and os.path.isfile(cover):
        cmd.extend(["--epub-cover-image", cover])
        print(f"  Cover image: {cover}")
    else:
        print("  No cover image (optional — add with --cover)")

    print(f"  Running pandoc...")
    print(f"  Command: {' '.join(cmd[:8])}...")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR: pandoc failed (exit {result.returncode})")
        if result.stderr:
            # Print last 20 lines of stderr
            lines = result.stderr.strip().split("\n")
            for line in lines[-20:]:
                print(f"  {line}")
        sys.exit(1)

    # Verify output
    if not os.path.isfile(output):
        print("ERROR: EPUB file was not created")
        sys.exit(1)

    size = os.path.getsize(output)
    print(f"  Generated: {output} ({size:,} bytes, {size/1024/1024:.1f} MB)")

    if size > 650 * 1024 * 1024:
        print("  WARNING: EPUB exceeds 650 MB Amazon limit")

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Build Kindle-compatible EPUB from Markdown source")
    parser.add_argument("--source", default=DEFAULTS["source"],
                        help="Markdown source file")
    parser.add_argument("--output", default=DEFAULTS["output"],
                        help="Output EPUB file")
    parser.add_argument("--css", default=DEFAULTS["css"],
                        help="Kindle CSS stylesheet")
    parser.add_argument("--filter", default=DEFAULTS["filter"],
                        help="Pandoc Lua filter for EPUB")
    parser.add_argument("--metadata", default=DEFAULTS["metadata"],
                        help="EPUB metadata XML file")
    parser.add_argument("--cover", default=DEFAULTS["cover"],
                        help="Cover image (JPEG, 2560x1600 recommended)")
    parser.add_argument("--keep-temp", action="store_true",
                        help="Keep temporary files")
    args = parser.parse_args()

    print("=" * 60)
    print("  Proving Nothing — Kindle EPUB Build")
    print("=" * 60)

    # Check tools
    print("\n[1/4] Checking tools...")
    check_tools()

    # Normalize source
    print("\n[2/4] Normalizing source...")
    temp_source = normalize_source(args.source, DEFAULTS["temp"])

    # Build EPUB
    print("\n[3/4] Building EPUB...")
    epub_path = build_epub(
        source=temp_source,
        output=args.output,
        css=args.css,
        lua_filter=args.filter,
        metadata=args.metadata,
        cover=args.cover,
    )

    # Cleanup
    print("\n[4/4] Cleanup...")
    if not args.keep_temp:
        if os.path.isfile(DEFAULTS["temp"]):
            os.remove(DEFAULTS["temp"])
            print(f"  Removed {DEFAULTS['temp']}")
    else:
        print(f"  Kept {DEFAULTS['temp']}")

    print("\n" + "=" * 60)
    print(f"  EPUB ready: {epub_path}")
    print(f"  Upload to: https://kdp.amazon.com")
    print("=" * 60)


if __name__ == "__main__":
    main()
