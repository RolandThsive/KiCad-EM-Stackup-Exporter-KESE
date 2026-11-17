#!/bin/bash
# Sets up a fresh Ubuntu 24.04 machine for the bridge: the Python packages of requirements.txt (PyPEEC among them) in
# .venv, at the versions the examples ran with. Run it from anywhere in the branch:
#
#     bash bridge/setup_machine.sh
#
# Safe to run again. PyPEEC is pure Python: nothing is built. KESE is not needed for a board whose 3D_Geometry/ is
# committed. This script is GPL-3.0 as the bridge.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SUDO=""
[ "$(id -u)" = 0 ] || SUDO=sudo
if [ ! -x "$ROOT/.venv/bin/python" ]; then
  python3 -m venv "$ROOT/.venv" || { $SUDO apt-get update -q && $SUDO apt-get install -y -q python3-venv && \
    python3 -m venv "$ROOT/.venv"; }
fi
"$ROOT/.venv/bin/pip" install -q --upgrade pip
"$ROOT/.venv/bin/pip" install -q -r "$ROOT/requirements.txt"
"$ROOT/.venv/bin/python" -c "import pypeec; print('PyPEEC', pypeec.__version__)"
echo "ready: Python in $ROOT/.venv"
