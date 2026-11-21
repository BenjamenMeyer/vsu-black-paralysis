#!/usr/bin/env python3
##
# verify_asset_references.py
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

"""Cross-reference and link integrity verifier for Vega Strike: Black Paralysis.

Recursively validates that:
  - Textures, planets, rings, and jump destinations in .system files exist.
  - Cockpit descriptors (.cpt) reference existing sprite (.spr) and texture files.
  - Sprite descriptors (.spr) reference existing image textures or animation frames.
  - Mission files reference existing systems, ship classes, factions, and AI scripts.
  - Galaxy sector manifests (universe/black_paralysis.xml) match existing .system files.
  - Weapon manifests (weapons.json) reference existing audio files in sounds/.
  - Playlist manifests (.black-paralysis/*.m3u) contain valid track references.

Usage:
    python3 scripts/verify_asset_references.py [--dir DIRECTORY] [-v] [-q] [--strict-audio]
    python3 scripts/verify_asset_references.py --help
"""

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


def _find_file_case_insensitive(directory: Path, filename: str) -> Optional[Path]:
    """Look up a file in directory case-insensitively."""
    target = directory / filename
    if target.exists():
        return target
    if not directory.is_dir():
        return None
    lower_name = filename.lower()
    for child in directory.iterdir():
        if child.name.lower() == lower_name:
            return child
    return None


def verify_system_references(repo_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Verify textures, rings, units, and jump destinations in .system files."""
    errors = []
    checks_passed = 0
    sectors_dir = repo_root / "sectors"
    textures_dir = repo_root / "textures"
    meshes_dir = repo_root / "meshes"
    units_dir = repo_root / "units"

    if not sectors_dir.is_dir():
        return 0, 1, [f"Missing sectors directory: {sectors_dir}"]

    system_files = sorted(sectors_dir.rglob("*.system"))
    for sys_file in system_files:
        rel_sys = sys_file.relative_to(repo_root)
        try:
            tree = ET.parse(sys_file)
            root = tree.getroot()
        except Exception as err:
            errors.append(f"{rel_sys}: Failed to parse XML: {err}")
            continue

        # Check background cubemap textures
        bg = root.get("background")
        if bg:
            bg_target = textures_dir / bg
            bg_parent = bg_target.parent
            bg_stem = bg_target.name
            matches = list(bg_parent.glob(f"{bg_stem}*")) if bg_parent.is_dir() else []
            if matches:
                checks_passed += 1
                if verbose:
                    print(f"  [PASS] {rel_sys} background '{bg}' ({len(matches)} face files found)")
            else:
                errors.append(f"{rel_sys}: Background cubemap '{bg}' not found in {textures_dir}")

        # Check elements inside system
        for elem in root.iter():
            # Planet or Ring textures
            if elem.tag in ("planet", "Ring"):
                f = elem.get("file")
                if f:
                    tf = textures_dir / f
                    if tf.exists():
                        checks_passed += 1
                        if verbose:
                            print(f"  [PASS] {rel_sys} {elem.tag} '{elem.get('name', '')}' texture: {f}")
                    else:
                        errors.append(f"{rel_sys}: {elem.tag} texture '{f}' not found in textures/")

                # Jump destination system
                dest = elem.get("destination")
                if dest:
                    dest_file = sectors_dir / f"{dest}.system"
                    if dest_file.is_file():
                        checks_passed += 1
                        if verbose:
                            print(f"  [PASS] {rel_sys} jump destination system '{dest}' exists")
                    else:
                        errors.append(f"{rel_sys}: Jump destination '{dest}' not found at {dest_file}")

            # Fog elements (atmosphere meshes)
            elif elem.tag == "FogElement":
                f = elem.get("file")
                if f:
                    mf = meshes_dir / f
                    if mf.exists():
                        checks_passed += 1
                        if verbose:
                            print(f"  [PASS] {rel_sys} FogElement mesh '{f}' exists")
                    else:
                        errors.append(f"{rel_sys}: FogElement mesh '{f}' not found in meshes/")

            # In-system unit installations
            elif elem.tag == "unit":
                f = elem.get("file")
                if f:
                    unit_found = False
                    for candidate in (
                        units_dir / "installations" / f,
                        units_dir / "installations" / f.lower(),
                        units_dir / "installations" / f.capitalize(),
                        units_dir / "vessels" / f,
                        units_dir / "vessels" / f.lower(),
                        units_dir / "vessels" / f.capitalize(),
                    ):
                        if candidate.exists():
                            unit_found = True
                            break
                    if unit_found:
                        checks_passed += 1
                        if verbose:
                            print(f"  [PASS] {rel_sys} unit '{f}' exists in units/")
                    else:
                        errors.append(f"{rel_sys}: Unit '{f}' not found in {units_dir}")

    return checks_passed, len(errors), errors


def verify_cockpit_references(repo_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Verify sprite and texture references in cockpit descriptor files (.cpt)."""
    errors = []
    checks_passed = 0
    cockpits_dir = repo_root / "cockpits"
    textures_dir = repo_root / "textures"

    if not cockpits_dir.is_dir():
        return 0, 1, [f"Missing cockpits directory: {cockpits_dir}"]

    cpt_files = sorted(cockpits_dir.rglob("*.cpt"))
    for cpt_file in cpt_files:
        if not cpt_file.is_file():
            continue
        rel_cpt = cpt_file.relative_to(repo_root)
        cpt_parent = cpt_file.parent
        try:
            tree = ET.parse(cpt_file)
            root = tree.getroot()
        except Exception as err:
            errors.append(f"{rel_cpt}: Failed to parse XML: {err}")
            continue

        for elem in root.iter():
            f = elem.get("file")
            if not f:
                continue
            # Search in cpt parent dir, cockpits root, textures dir
            target1 = cpt_parent / f
            target2 = cockpits_dir / f
            target3 = textures_dir / f
            if target1.exists() or target2.exists() or target3.exists():
                checks_passed += 1
                if verbose:
                    print(f"  [PASS] {rel_cpt} <{elem.tag}> file '{f}' exists")
            else:
                errors.append(f"{rel_cpt}: <{elem.tag}> referenced file '{f}' not found")

    return checks_passed, len(errors), errors


def verify_sprite_references(repo_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Verify that sprite descriptors (.spr) reference existing textures."""
    errors = []
    checks_passed = 0
    textures_dir = repo_root / "textures"
    sprites_dir = repo_root / "sprites"

    for spr_file in sorted(repo_root.rglob("*.spr")):
        rel_spr = spr_file.relative_to(repo_root)
        try:
            with open(spr_file, "r", encoding="utf-8", errors="replace") as fp:
                lines = [l.strip() for l in fp if l.strip() and not l.strip().startswith("#")]
        except Exception as err:
            errors.append(f"{rel_spr}: Error reading file: {err}")
            continue

        if not lines:
            continue

        img_tokens = lines[0].split()
        first_token = img_tokens[0] if img_tokens else ""

        if first_token.endswith(".ani"):
            # Animated sprite: frame lines start from line 3 or line 4
            for frame_line in lines[2:]:
                parts = frame_line.split()
                if not parts:
                    continue
                ext = os.path.splitext(parts[0])[1].lower()
                if ext in (".png", ".jpg", ".jpeg", ".bmp", ".image"):
                    img_path = parts[0]
                    target1 = textures_dir / img_path
                    target2 = sprites_dir / img_path
                    target3 = spr_file.parent / img_path
                    if target1.exists() or target2.exists() or target3.exists():
                        checks_passed += 1
                        if verbose:
                            print(f"  [PASS] {rel_spr} frame '{img_path}' exists")
                    else:
                        errors.append(f"{rel_spr}: Animation frame texture '{img_path}' not found")
        else:
            # Still sprite: check first image and optional alphamap token
            for tok in img_tokens[:2]:
                if tok in ("0", "true", "false", "-"):
                    continue
                target1 = textures_dir / tok
                target2 = sprites_dir / tok
                target3 = spr_file.parent / tok
                if target1.exists() or target2.exists() or target3.exists():
                    checks_passed += 1
                    if verbose:
                        print(f"  [PASS] {rel_spr} texture '{tok}' exists")
                else:
                    errors.append(f"{rel_spr}: Texture '{tok}' not found")

    return checks_passed, len(errors), errors


def verify_mission_references(repo_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Verify system, flightgroup, faction, and AI script references in mission files."""
    errors = []
    checks_passed = 0
    mission_dir = repo_root / "mission"
    sectors_dir = repo_root / "sectors"
    units_dir = repo_root / "units"
    ai_dir = repo_root / "ai"
    factions_file = repo_root / "factions.xml"

    if not mission_dir.is_dir():
        return 0, 1, [f"Missing mission directory: {mission_dir}"]

    # Load known factions from factions.xml
    known_factions: Set[str] = set()
    if factions_file.is_file():
        try:
            ftree = ET.parse(factions_file)
            for faction_elem in ftree.getroot().findall("Faction"):
                name = faction_elem.get("name")
                if name:
                    known_factions.add(name.lower())
        except Exception as err:
            errors.append(f"factions.xml: Failed to parse XML: {err}")

    # Load known unit keys from units/ships.json and units/units.json
    known_units: Set[str] = set()
    ships_json = units_dir / "ships.json"
    if ships_json.is_file():
        try:
            with open(ships_json, "r", encoding="utf-8") as fp:
                sdata = json.load(fp)
            for item in sdata.get("units", []):
                key = item.get("data", {}).get("Key")
                if key:
                    known_units.add(key.lower())
                    if "." in key:
                        known_units.add(key.split(".")[0].lower())
        except Exception:
            pass

    # Add directories in units/vessels and units/installations
    for sub in ("vessels", "installations"):
        p = units_dir / sub
        if p.is_dir():
            for child in p.iterdir():
                known_units.add(child.name.lower())

    for mfile in sorted(mission_dir.glob("*.mission")):
        rel_m = mfile.relative_to(repo_root)
        try:
            tree = ET.parse(mfile)
            root = tree.getroot()
        except Exception as err:
            errors.append(f"{rel_m}: Failed to parse XML: {err}")
            continue

        # Check system variable
        for var in root.iter("var"):
            if var.get("name") == "system":
                val = var.get("value")
                if val:
                    sys_path = sectors_dir / f"{val}.system"
                    if sys_path.is_file():
                        checks_passed += 1
                        if verbose:
                            print(f"  [PASS] {rel_m} system '{val}' exists")
                    else:
                        errors.append(f"{rel_m}: System '{val}' not found at {sys_path}")

        # Check flightgroups
        for fg in root.iter("flightgroup"):
            name = fg.get("name", "unnamed")
            # Ship type
            ship_type = fg.get("type")
            if ship_type:
                if ship_type.lower() in known_units:
                    checks_passed += 1
                    if verbose:
                        print(f"  [PASS] {rel_m} flightgroup '{name}' ship type '{ship_type}' exists")
                else:
                    errors.append(f"{rel_m}: Flightgroup '{name}' ship type '{ship_type}' not found in units")

            # Faction
            faction = fg.get("faction")
            if faction:
                if faction.lower() in known_factions:
                    checks_passed += 1
                    if verbose:
                        print(f"  [PASS] {rel_m} flightgroup '{name}' faction '{faction}' exists")
                else:
                    errors.append(f"{rel_m}: Flightgroup '{name}' faction '{faction}' not found in factions.xml")

            # AI Name
            ainame = fg.get("ainame")
            if ainame:
                ai_event = ai_dir / "events" / f"{ainame}.agg.xml"
                ai_script = ai_dir / "script" / f"{ainame}.xml"
                if ai_event.is_file() or ai_script.is_file():
                    checks_passed += 1
                    if verbose:
                        print(f"  [PASS] {rel_m} flightgroup '{name}' AI '{ainame}' exists")
                else:
                    errors.append(f"{rel_m}: Flightgroup '{name}' AI '{ainame}' not found in {ai_dir}")

    return checks_passed, len(errors), errors


def verify_universe_references(repo_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Verify that universe sector and system manifests match existing .system files."""
    errors = []
    checks_passed = 0
    galaxy_file = repo_root / "universe" / "black_paralysis.xml"
    sectors_dir = repo_root / "sectors"

    if not galaxy_file.is_file():
        return 0, 1, [f"Missing universe galaxy definition: {galaxy_file}"]

    try:
        tree = ET.parse(galaxy_file)
        root = tree.getroot()
    except Exception as err:
        return 0, 1, [f"{galaxy_file}: Failed to parse XML: {err}"]

    for sector in root.iter("sector"):
        sector_name = sector.get("name")
        if not sector_name:
            continue
        for system in sector.iter("system"):
            sys_name = system.get("name")
            if not sys_name:
                continue
            expected_sys = sectors_dir / sector_name / f"{sys_name}.system"
            if expected_sys.is_file():
                checks_passed += 1
                if verbose:
                    print(f"  [PASS] Galaxy sector '{sector_name}' system '{sys_name}' exists")
            else:
                errors.append(f"universe/black_paralysis.xml: Sector '{sector_name}' system '{sys_name}' not found at {expected_sys}")

    return checks_passed, len(errors), errors


def verify_weapon_references(repo_root: Path, verbose: bool = False) -> Tuple[int, int, List[str]]:
    """Verify that weapon manifests (weapons.json) reference existing audio files."""
    errors = []
    checks_passed = 0
    weapons_file = repo_root / "weapons.json"
    sounds_dir = repo_root / "sounds"

    if not weapons_file.is_file():
        return 0, 1, [f"Missing weapons.json: {weapons_file}"]

    try:
        with open(weapons_file, "r", encoding="utf-8") as fp:
            weapons_data = json.load(fp)
    except Exception as err:
        return 0, 1, [f"{weapons_file}: Failed to parse JSON: {err}"]

    checked_sounds: Set[str] = set()
    for weapon in weapons_data:
        sound = weapon.get("Appearance.soundwav")
        if not sound or sound in checked_sounds:
            continue
        checked_sounds.add(sound)
        found = _find_file_case_insensitive(sounds_dir, sound)
        if found:
            checks_passed += 1
            if verbose:
                print(f"  [PASS] Weapon sound '{sound}' exists ({found.name})")
        else:
            errors.append(f"weapons.json: Audio file '{sound}' not found in sounds/")

    return checks_passed, len(errors), errors


def verify_playlist_references(
    repo_root: Path, verbose: bool = False, strict_audio: bool = False
) -> Tuple[int, int, List[str]]:
    """Verify that playlist files (.m3u) contain valid syntax and track references."""
    errors = []
    checks_passed = 0
    playlist_dir = repo_root / ".black-paralysis"

    if not playlist_dir.is_dir():
        return 0, 0, []

    m3u_files = sorted(playlist_dir.glob("*.m3u"))
    for m3u_file in m3u_files:
        rel_m3u = m3u_file.relative_to(repo_root)
        try:
            with open(m3u_file, "r", encoding="utf-8", errors="replace") as fp:
                lines = [l.strip() for l in fp if l.strip()]
        except Exception as err:
            errors.append(f"{rel_m3u}: Failed to read playlist: {err}")
            continue

        for line in lines:
            if line.startswith("#"):
                continue
            # Validate track syntax
            if not line.endswith((".ogg", ".wav", ".mp3")):
                errors.append(f"{rel_m3u}: Invalid audio file extension in entry: '{line}'")
                continue

            checks_passed += 1
            # Check if file exists on disk
            audio_path = (m3u_file.parent / line).resolve()
            if audio_path.exists():
                if verbose:
                    print(f"  [PASS] {rel_m3u} track exists: {line}")
            elif strict_audio:
                errors.append(f"{rel_m3u}: Track file not found on disk: '{line}'")

    if not strict_audio and verbose:
        print(f"  [INFO] Verified {checks_passed} playlist track entries across {len(m3u_files)} playlists (music tracks external/optional)")

    return checks_passed, len(errors), errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify cross-references and asset link integrity for Vega Strike: Black Paralysis."
    )
    parser.add_argument(
        "-d",
        "--dir",
        dest="directory",
        default=".",
        help="Root directory of the asset repository (default: current working directory)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Print detailed results for every passed reference",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        help="Quiet mode: report errors and summary only",
    )
    parser.add_argument(
        "--strict-audio",
        dest="strict_audio",
        action="store_true",
        help="Fail if external music tracks in .black-paralysis/*.m3u are missing",
    )

    args = parser.parse_args()
    repo_root = Path(args.directory).resolve()
    if not (repo_root / "config.json").exists():
        script_repo = Path(__file__).resolve().parent.parent
        if (script_repo / "config.json").exists():
            repo_root = script_repo

    if not repo_root.is_dir():
        print(f"Error: Target directory does not exist: {repo_root}", file=sys.stderr)
        return 2

    verbose = args.verbose and not args.quiet
    if not args.quiet:
        print(f"Verifying cross-asset references in {repo_root.name}...")

    sections = [
        ("System Definitions (.system)", verify_system_references(repo_root, verbose)),
        ("Cockpit Descriptors (.cpt)", verify_cockpit_references(repo_root, verbose)),
        ("Sprite Descriptors (.spr)", verify_sprite_references(repo_root, verbose)),
        ("Mission Files (.mission)", verify_mission_references(repo_root, verbose)),
        ("Universe Manifest (universe/black_paralysis.xml)", verify_universe_references(repo_root, verbose)),
        ("Weapon Audio (weapons.json)", verify_weapon_references(repo_root, verbose)),
        ("Playlists (.black-paralysis/*.m3u)", verify_playlist_references(repo_root, verbose, args.strict_audio)),
    ]

    total_checks = 0
    total_errors = 0
    all_errors = []

    for name, (passed, err_count, errors) in sections:
        total_checks += passed
        total_errors += err_count
        if errors:
            all_errors.extend(errors)
            if not args.quiet:
                print(f"  [FAIL] {name}: {err_count} broken reference(s)")
                for e in errors:
                    print(f"    - {e}")
        elif not args.quiet:
            print(f"  [PASS] {name}: {passed} reference(s) verified")

    if not args.quiet:
        print()
        if total_errors == 0:
            print(f"Asset Integrity Verification Summary: {total_checks} reference(s) verified, 0 broken links (all checks passed)")
        else:
            print(f"Asset Integrity Verification Summary: {total_checks} verified, {total_errors} broken link(s) found", file=sys.stderr)

    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
