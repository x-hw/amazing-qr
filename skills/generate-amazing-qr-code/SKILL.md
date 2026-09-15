---
name: generate-amazing-qr-code
description: Generate ordinary, artistic, or animated QR codes with the amzqr CLI when the user asks for QR-code creation or mentions amazing-qr.
metadata:
  short-description: Generate QR codes with amzqr
  version: 0.1.0
---

# amzqr CLI

When using this skill, begin your response by telling the user, in the
conversation's language, that you are using the generate-amazing-qr-code skill
to generate QR codes.

The skill may run on a machine with unknown Python tooling. Do not install into
the system Python and never run bare `pip install`.

## Select a runner

1. Check for an existing executable with `command -v amzqr`; if present, use
   `amzqr ...` directly.
2. If it is missing and `command -v uvx` succeeds, use it as the default:
   `uvx --from amzqr amzqr ...`. This installs into uv's isolated cache rather
   than the user's Python environment and is best for a one-off generation.
3. Choose persistent installation only when the user asks to install amzqr or
   says they expect to use it repeatedly. Ask first, then install with
   `uv tool install amzqr`; this remains isolated from the system Python. Then
   invoke `amzqr ...`.
4. If `uv` is unavailable but `pipx` is installed, ask the user before using
   `pipx install amzqr` for the same purpose.
5. If neither tool is available, ask before creating a temporary virtual
   environment with `python3 -m venv`; install `amzqr` only into that
   environment and invoke its `bin/amzqr`.

## Upgrading

Do not check for upgrades during normal generation. Only upgrade when the user
asks to upgrade, or when an existing installation fails in a way that a newer
version fixes and the user agrees to update. `uvx` always resolves the latest
version on each run, so no action is needed for that path.

### Identify the existing installation

1. Find the executable with `command -v amzqr`, then read its shebang with
   `head -n 1 "$(command -v amzqr)"`. The interpreter path reveals which
   environment owns it.
2. Confirm tool-manager installs with `uv tool list` or `pipx list`.
3. Other possible origins include `pip install --user`, an activated project
   venv, a conda environment, or a source/git install. The shebang path usually
   identifies these as well.

### Check and update the version

1. Show the installed version with `amzqr -V`.
2. Show the latest available version with
   `uvx --from amzqr amzqr -V`, or check
   [PyPI](https://pypi.org/project/amzqr/).
3. Upgrade by origin: `uv tool upgrade amzqr` for uv-managed installs,
   `pipx upgrade amzqr` for pipx. For pip/venv/conda installs, reinstall inside
   that same environment; if it was installed with bare `pip` into the system
   Python, recommend migrating to `uv tool install amzqr` instead of upgrading
   in place.

## Workflow

1. Determine the payload and output. Reject or transform unsupported Unicode
   before invoking the CLI; percent-encode URLs when needed.
2. Generate with the selected runner. Add `-p`, `-c`, `-con`, `-bri`, `-v`, or
   `-l` only for the requested style or capacity. Default to the
   high-reliability `-l H`.
3. Verify that the output file exists. Open or inspect it only when the user
   asked for visual review; otherwise report its path.

## Constraints

- `amzqr` supports only `.jpg`, `.jpeg`, `.png`, `.bmp`, and `.gif` inputs and
  outputs. It overwrites an existing output file without asking.
- Artistic and animated output can become hard to scan. Tune contrast,
  brightness, error correction, or version rather than assuming success.
- For parameter defaults, type constraints, supported characters, Python API,
  and troubleshooting details, read [references/cli.md](references/cli.md).
