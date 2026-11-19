#!/usr/bin/env python3
##
# test_json_syntax.py
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

"""Syntax and structure validator for JSON files in Vega Strike: Black Paralysis.

Recursively scans repository assets for all .json files and verifies that
each file is valid JSON and contains a non-empty container (dict or list).

Usage:
    python3 scripts/test_json_syntax.py [--dir DIRECTORY] [FILES ...]
    python3 scripts/test_json_syntax.py --help
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Directories to ignore during recursive search
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".gemini",
    "build",
    "_CPack_Packages",
    "__pycache__",
}


def find_json_files(root_dir: Path) -> list[Path]:
    """Find all .json files under root_dir, skipping excluded directories."""
    json_files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude directories in-place to prevent walking into them
        dirnames[:] = [
            d for d in dirnames
            if d not in DEFAULT_EXCLUDE_DIRS and not d.startswith("build") and not d.startswith(".")
        ]
        for f in filenames:
            if f.endswith(".json"):
                json_files.append(Path(dirpath) / f)
    return sorted(json_files)


def validate_json_file(filepath: Path, verbose: bool = False) -> tuple[bool, str]:
    """Validate a single JSON file.

    Returns:
        (success, message)
    """
    if not filepath.is_file():
        return False, f"File not found: {filepath}"

    if filepath.stat().st_size == 0:
        return False, f"File is empty (0 bytes): {filepath}"

    try:
        with open(filepath, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except json.JSONDecodeError as err:
        return False, f"JSON decode error at line {err.lineno}, column {err.colno}: {err.msg}"
    except UnicodeDecodeError as err:
        return False, f"Encoding error: {err}"
    except Exception as err:
        return False, f"Error reading file: {err}"

    if not isinstance(data, (dict, list)):
        return False, f"Root element is {type(data).__name__}, expected dict or list"

    element_count = len(data)
    if verbose:
        return True, f"Valid JSON ({type(data).__name__} with {element_count} elements)"
    return True, "OK"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate JSON syntax and structures for Vega Strike: Black Paralysis."
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Optional specific JSON files to validate.",
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
        target_files = find_json_files(root)

    if not target_files:
        print("No JSON files found to validate.", file=sys.stderr)
        return 1

    total_count = len(target_files)
    pass_count = 0
    fail_count = 0

    if not args.quiet:
        print(f"Validating JSON syntax for {total_count} file(s)...")

    for filepath in target_files:
        try:
            rel_path = filepath.relative_to(Path.cwd())
        except ValueError:
            rel_path = filepath

        success, message = validate_json_file(filepath, verbose=args.verbose)
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
        print(f"\nJSON Validation Summary: {pass_count}/{total_count} passed", end="")
        if fail_count > 0:
            print(f", {fail_count} failed")
        else:
            print(" (all checks passed)")

    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
