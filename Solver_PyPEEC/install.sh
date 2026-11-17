#!/bin/bash
# Installs the Python environment every PyPEEC simulation in this branch ran with, from the wheels in wheels/ and
# without the internet: PyPEEC 5.8.0 and every package under it, at the exact versions, for 64-bit Linux and
# Python 3.13. Run it from anywhere in the branch:
#
#     bash Solver_PyPEEC/install.sh                    makes .venv at the branch's root
#     VENV=/some/where bash Solver_PyPEEC/install.sh   makes it there instead
#     PYTHON=/usr/bin/python3.13 bash ...              with that Python (default: python3.13)
#
# Two wheels are over GitHub's 100 MB limit, so they are kept in parts (.part0, .part1); this joins them in a
# temporary folder first and checks every wheel against SHA256SUMS. This script is GPL-3.0 as the bridge.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$HERE")"
VENV="${VENV:-$ROOT/.venv}"
PY="${PYTHON:-python3.13}"
command -v "$PY" >/dev/null || { echo "needs Python 3.13 ($PY not found); set PYTHON=..." >&2; exit 1; }
"$PY" -c 'import sys; assert sys.version_info[:2] == (3, 13), sys.version' \
  || { echo "these wheels are for Python 3.13" >&2; exit 1; }
[ "$(uname -s)-$(uname -m)" = "Linux-x86_64" ] || { echo "these wheels are for 64-bit Linux" >&2; exit 1; }
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
for first in "$HERE"/wheels/*.whl.part0; do
  name="$(basename "${first%.part0}")"
  cat "$HERE/wheels/$name".part* > "$TMP/$name"
done
( cd "$HERE/wheels" && ln -sf "$HERE"/wheels/*.whl "$TMP"/ && cd "$TMP" && sha256sum --quiet -c "$HERE/SHA256SUMS" )
"$PY" -m venv "$VENV"
"$VENV/bin/pip" install -q --no-index --find-links "$TMP" -r "$HERE/requirements-lock.txt"
"$VENV/bin/python" -c "import pypeec; print('PyPEEC', pypeec.__version__, 'ready in', '$VENV')"
