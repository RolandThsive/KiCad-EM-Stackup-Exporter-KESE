#!/bin/bash
# Sets up a fresh 64-bit Linux machine for the bridge: the Python packages of requirements.txt in .venv, at the
# versions the examples ran with, and FastHenry. Run it from anywhere in the branch:
#
#     bash bridge/setup_machine.sh
#
# FastHenry is committed, built, in Solver_FastHenry/install/bin; where it does not run (another system), the script
# builds it from source with Solver_FastHenry/build_fasthenry.sh, which needs git, make and gcc. Needs Python 3.12 or
# newer (numpy 2.5). Safe to run again. KESE is not needed for a board whose 3D_Geometry/ is committed.
# This script is GPL-3.0 as the bridge.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SUDO=""
[ "$(id -u)" = 0 ] || SUDO=sudo
PY="${PYTHON:-python3}"
if [ ! -x "$ROOT/.venv/bin/python" ]; then
  "$PY" -m venv "$ROOT/.venv" || { $SUDO apt-get update -q && $SUDO apt-get install -y -q python3-venv && \
    "$PY" -m venv "$ROOT/.venv"; }
fi
"$ROOT/.venv/bin/pip" install -q --upgrade pip
"$ROOT/.venv/bin/pip" install -q -r "$ROOT/requirements.txt"
FH="$ROOT/Solver_FastHenry/install/bin/fasthenry"
if ! "$FH" -h 2>&1 | grep -q 'FastHenry Version'; then
  command -v gcc >/dev/null && command -v make >/dev/null && command -v git >/dev/null || \
    { $SUDO apt-get update -q && $SUDO apt-get install -y -q gcc make git; }
  bash "$ROOT/Solver_FastHenry/build_fasthenry.sh"
fi
"$FH" -h 2>&1 | grep -i 'FastHenry Version'
"$ROOT/.venv/bin/python" -c "import numpy, shapely, matplotlib; print('numpy', numpy.__version__, 'shapely', shapely.__version__)"
echo "ready: Python in $ROOT/.venv, FastHenry in $FH"
