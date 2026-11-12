# AGENTS.md

Working notes for AI coding agents (Claude Code, Cursor, Codex, Copilot, pi, and friends) operating
in this repository: what it is, how it builds, how the assets and scripts are laid out, and which
conventions changes are reviewed against.

**`README` and repository docs are authoritative.** Where this file disagrees with project standards,
this file should be corrected.

## What this repository is

The **game assets and Python runtime** for **Vega Strike: Black Paralysis** (`vsu-black-paralysis`).
It contains star systems, missions, ships, base interfaces, audio, shaders, and manifests designed
to run against the Vega Strike core engine (Assets API Version 3 / Engine 0.11.0+).

Engine source code lives in the separate
[`vegastrike/Vega-Strike-Engine-Source`](https://github.com/vegastrike/Vega-Strike-Engine-Source)
repository. A change that spans both needs two pull requests, one per repository.

Branches:

- `master` — development head for Black Paralysis targeting modern engine releases.
- Follow milestone/phase branches for active pull requests (e.g. `feat_*`, `fix_*`).

## Build, package, and test

Asset packaging uses CMake 3.22+:

```bash
cmake -B build
cmake --build build
```

Packaging artifacts (tarball, deb, rpm):

```bash
cpack --config build/CPackConfig.cmake -G TXZ
cpack --config build/CPackConfig.cmake -G DEB   # on Debian/Ubuntu systems
```

### Running with the engine

Running Black Paralysis requires the `vegastrike-engine` binary. Specify the repository directory
via `-D`:

```bash
# Normal startup into main menu:
vegastrike-engine -D /path/to/black-paralysis

# Direct mission launch:
vegastrike-engine -D /path/to/black-paralysis mission/bp_campaign.mission
vegastrike-engine -D /path/to/black-paralysis mission/explorer.mission

# Using the launcher script:
VS_ENGINE_BIN=/path/to/vegastrike-engine ./scripts/vsuBlackParalysis
```

**A manual playtest is mandatory.** Before opening a PR that alters missions, base scripts, controls,
or asset definitions, launch the game with `vegastrike-engine` and verify that the game boots cleanly,
transitions into flight, and behaves as expected without console exceptions or crashes.

## Asset layout

| Path | Contents |
|---|---|
| `bases/` | Python base rooms: main menu (`main_menu.py`), concourses, bars, shipyards |
| `cockpits/` | 2D cockpit overlays, gauge sprites, and VDU configurations |
| `mission/` | Mission XML definitions: `main_menu.mission`, `bp_campaign.mission`, `explorer.mission` |
| `modules/` | Python game logic: `GUI.py`, AI routines, quest managers, trading |
| `python/base_computer/` | Terminal computer interface: ship upgrades, cargo view, player info |
| `sectors/` | Star system XML files (`.system`): celestial bodies, lights, starfields |
| `sounds/` | WAV sound effects and interface audio |
| `sprites/` | 2D sprite descriptors (`.spr`) and PNG interface graphics |
| `techniques/`, `programs/` | Rendering technique trees and GLSL shaders |
| `textures/` | Skyboxes, cubemaps (`sigma`), planet surfaces, and materials |
| `units/` | Ship unit definitions (`units.json`, `ships.json`), faction setups, meshes (`.bfxm`) |
| `universe/` | Galaxy sector graph (`universe/black_paralysis.xml`) |
| Root JSON configs | Core engine configuration: `engine.json`, `bindings.json`, `theme.json`, `controls.json`, `config.json` |
| Root manifests | Economy and weapon manifests: `master_part_list.json`, `master_component_list.json`, `master_ship_list.json`, `weapons.json` |

## Facts worth knowing before you dig

- **Asset API Version 3 requires JSON configuration.** Legacy XML `vegastrike.config` is completely
  deprecated; runtime configuration is loaded from root `config.json` and engine defaults from `engine.json`.
- **Sprite descriptors (`.spr`) reference real image files.** A `.spr` file specifies the image
  path on line 1, dimensions on line 2, and optional center coordinates on line 3. Always reference
  existing images (e.g. `mouse.png` rather than missing `.image` formats).
- **Cubemap background loaders check `.image` extensions.** The engine's environment and skybox
  loaders look for `[name]_[direction].image` (e.g. `sigma_front.image`, `sigma_up.image`). Ensure
  skybox directories supply valid images for all 6 cube faces.
- **Python 3 compatibility is mandatory.** All scripts in `bases/`, `modules/`, and `python/` run
  under Python 3 embedded in the engine. Escape sequences in regular expressions must use raw strings
  (`r'...'`) to avoid deprecation warnings or runtime syntax errors.
- **Sound files must have valid WAV headers.** Ensure RIFF chunk headers and data sizes are well-formed;
  corrupted chunk lengths cause crashes in OpenAL/libvorbis loaders.
- **Flight controls depend on `bindings.json` and `config.json`.** Default steering device is
  configured under `input.device` in `config.json` with matching axis sources in `bindings.json`.

## Conventions and style

1. **Do not introduce unnecessary diff churn.** When editing JSON manifests or XML systems, touch
   only the relevant keys or tags. Do not reformat entire unaffected files.
2. **Follow `.editorconfig`.** UTF-8, LF line endings, 2 spaces for JSON/YAML/shell, 4 spaces for
   Python and XML, no trailing whitespace.
3. **Keep comments informative and authentic.** Maintain the authentic Black Paralysis lore,
   flight group names (`Shlimazel`, `Cook`), and sector names (`Test_Sector/Isaac`).
4. **No local or private paths in committed files.** Never hard-code `/home/...` or user-specific
   directories in missions, configs, or scripts.
5. **One logical change per commit.** Provide a clear conventional commit title (`feat: ...`,
   `fix: ...`) explaining what was changed and why.
6. **Licensing is GPLv3-or-later.** Keep existing file copyright headers intact. AI agents are
   credited via the git commit trailer `Co-authored-by: Antigravity <antigravity@google.com>` and
   are never added to file copyright statements.

## When in doubt

Consult existing reference implementations in [`vegastrike/Assets-Production`](https://github.com/vegastrike/Assets-Production)
or ask on the pull request.
