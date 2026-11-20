#!/usr/bin/env python3
##
# test_xml_syntax.py
#
# Vega Strike: Black Paralysis - Space Simulation, Combat and Trading
# Copyright (C) 2003-2005 Daniel Aleksandrow <dandandaman@users.sourceforge.net>
# Copyright (C) 2003-2026 The Vega Strike Contributors
#
# https://github.com/vegastrike/vsu-black-paralysis
#
# This file is part of Vega Strike: Black Paralysis.
#
# Vega Strike: Black Paralysis is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Vega Strike: Black Paralysis is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Vega Strike: Black Paralysis.  If not, see <https://www.gnu.org/licenses/>.
#

"""Syntax and structure validator for XML and sprite descriptor (.spr) files in Vega Strike: Black Paralysis.

Recursively scans repository assets for:
  - XML files (.xml, .system, .mission, .cpt)
  - Sprite descriptor files (.spr)

Verifies standard XML structure and sprite descriptor formatting.

Usage:
    python3 scripts/test_xml_syntax.py [--dir DIRECTORY] [FILES ...]
    python3 scripts/test_xml_syntax.py --help
"""

import argparse
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# Directories to ignore during recursive search
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".gemini",
    "build",
    "_CPack_Packages",
    "__pycache__",
}

XML_EXTENSIONS = {".xml", ".system", ".mission", ".cpt"}
SPR_EXTENSIONS = {".spr"}
ALL_VALID_EXTENSIONS = XML_EXTENSIONS | SPR_EXTENSIONS


def find_target_files(root_dir: Path) -> list[Path]:
    """Find all XML and .spr files under root_dir, skipping excluded directories."""
    target_files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude directories in-place to prevent walking into them
        dirnames[:] = [
            d for d in dirnames
            if d not in DEFAULT_EXCLUDE_DIRS and not d.startswith("build") and not d.startswith(".")
        ]
        for f in filenames:
            ext = os.path.splitext(f)[1].lower()
            if ext in ALL_VALID_EXTENSIONS:
                target_files.append(Path(dirpath) / f)
    return sorted(target_files)


def validate_xml_file(filepath: Path, verbose: bool = False) -> tuple[bool, str]:
    """Validate a single XML-based file (.xml, .system, .mission, .cpt)."""
    if not filepath.is_file():
        return False, f"File not found: {filepath}"

    if filepath.stat().st_size == 0:
        return False, f"File is empty (0 bytes): {filepath}"

    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
    except ET.ParseError as err:
        return False, f"XML parse error at line {err.position[0]}, column {err.position[1]}: {err}"
    except UnicodeDecodeError as err:
        return False, f"Encoding error: {err}"
    except Exception as err:
        return False, f"Error reading file: {err}"

    if root is None or not root.tag:
        return False, "Root XML element is missing or has empty tag"

    child_count = len(root)
    if verbose:
        return True, f"Valid XML (root: <{root.tag}> with {child_count} direct children)"
    return True, "OK"


def validate_spr_file(filepath: Path, verbose: bool = False) -> tuple[bool, str]:
    """Validate a single sprite descriptor (.spr) file.

    Format requirements:
        Line 1: 1 or 2 texture/image file references
        Line 2: 2 floating-point dimensions (width height)
        Line 3 (optional): 2 floating-point center coordinates (xcent ycent)
    """
    if not filepath.is_file():
        return False, f"File not found: {filepath}"

    if filepath.stat().st_size == 0:
        return False, f"File is empty (0 bytes): {filepath}"

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as fp:
            raw_lines = fp.readlines()
    except Exception as err:
        return False, f"Error reading file: {err}"

    lines = [line.strip() for line in raw_lines if line.strip() and not line.strip().startswith("#")]

    if len(lines) < 2:
        return False, f"Sprite descriptor has {len(lines)} content line(s); minimum 2 required (images, dimensions)"

    # Line 1: image paths
    images = lines[0].split()
    if not images:
        return False, "Line 1 has no image paths specified"

    # Line 2: dimensions (width, height)
    dim_parts = lines[1].split()
    if len(dim_parts) < 2:
        return False, f"Line 2 requires at least 2 numeric dimensions (width height), got: '{lines[1]}'"

    try:
        width = float(dim_parts[0])
        height = float(dim_parts[1])
    except ValueError as err:
        return False, f"Line 2 dimensions must be numeric floats: '{lines[1]}' ({err})"

    # Note: negative width or height is valid in Vega Strike to flip/mirror a sprite horizontally or vertically.
    if width == 0.0 or height == 0.0:
        return False, f"Line 2 dimensions cannot be zero: width={width}, height={height}"

    # Line 3 (optional): center coordinates
    if len(lines) >= 3:
        cent_parts = lines[2].split()
        if len(cent_parts) >= 2:
            try:
                float(cent_parts[0])
                float(cent_parts[1])
            except ValueError as err:
                return False, f"Line 3 center coordinates must be numeric floats: '{lines[2]}' ({err})"

    if verbose:
        return True, f"Valid sprite descriptor ({len(images)} texture reference(s), dims {width}x{height})"
    return True, "OK"


def validate_file(filepath: Path, verbose: bool = False) -> tuple[bool, str]:
    """Dispatch file validation based on file extension."""
    ext = filepath.suffix.lower()
    if ext in XML_EXTENSIONS:
        return validate_xml_file(filepath, verbose=verbose)
    elif ext in SPR_EXTENSIONS:
        return validate_spr_file(filepath, verbose=verbose)
    else:
        return False, f"Unsupported file extension: {ext}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate XML and sprite descriptor syntax for Vega Strike: Black Paralysis."
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Optional specific XML or .spr files to validate.",
    )
    parser.add_argument(
        "--dir",
        "-d",
        type=Path,
        default=None,
        help="Root directory to scan (defaults to repository root).",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed information for each validated file.",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Only output failure information.",
    )

    args = parser.parse_args()

    # Determine files to check
    if args.files:
        target_files = [f.resolve() for f in args.files]
    else:
        root = args.dir.resolve() if args.dir else Path(__file__).resolve().parent.parent
        target_files = find_target_files(root)

    if not target_files:
        print("No XML or sprite descriptor files found to validate.", file=sys.stderr)
        return 1

    total_count = len(target_files)
    pass_count = 0
    fail_count = 0

    if not args.quiet:
        print(f"Validating XML and sprite syntax for {total_count} file(s)...")

    for filepath in target_files:
        try:
            rel_path = filepath.relative_to(Path.cwd())
        except ValueError:
            rel_path = filepath

        success, message = validate_file(filepath, verbose=args.verbose)
        if success:
            pass_count += 1
            if not args.quiet:
                if args.verbose:
                    print(f"  [PASS] {rel_path} - {message}")
                else:
                    print(f"  [PASS] {rel_path}")
        else:
            fail_count += 1
            print(f"  [FAIL] {rel_path} - {message}", file=sys.stderr)

    if not args.quiet:
        print(f"\nXML/Sprite Validation Summary: {pass_count}/{total_count} passed", end="")
        if fail_count > 0:
            print(f", {fail_count} failed")
        else:
            print(" (all checks passed)")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
