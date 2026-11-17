#!/bin/bash
# Sets up a fresh 64-bit Linux machine for the bridge: PyPEEC and every package under it in .venv, at the versions
# the examples ran with. Run it from anywhere in the branch:
#
#     bash bridge/setup_machine.sh
#
# Where Python 3.13 is found (or PYTHON=... names it), it installs the committed wheels of Solver_PyPEEC/wheels/
# with no internet (Solver_PyPEEC/install.sh); otherwise it installs the same versions
# (Solver_PyPEEC/requirements-lock.txt) from PyPI with the system's Python 3, which needs 3.12 or newer. Safe to run
# again. KESE is not needed for a board whose 3D_Geometry/ is committed. This script is GPL-3.0 as the bridge.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SUDO=""
[ "$(id -u)" = 0 ] || SUDO=sudo
PY="${PYTHON:-$(command -v python3.13 || true)}"
if [ -n "$PY" ] && [ "$(uname -m)" = x86_64 ] && [ ! -x "$ROOT/.venv/bin/python" ]; then
  "$PY" -m venv --help >/dev/null 2>&1 || { $SUDO apt-get update -q && $SUDO apt-get install -y -q python3.13-venv; }
  PYTHON="$PY" bash "$ROOT/Solver_PyPEEC/install.sh"
else
  if [ ! -x "$ROOT/.venv/bin/python" ]; then
    python3 -m venv "$ROOT/.venv" || { $SUDO apt-get update -q && $SUDO apt-get install -y -q python3-venv && \
      python3 -m venv "$ROOT/.venv"; }
  fi
  "$ROOT/.venv/bin/pip" install -q --upgrade pip
  "$ROOT/.venv/bin/pip" install -q -r "$ROOT/Solver_PyPEEC/requirements-lock.txt"
fi
"$ROOT/.venv/bin/python" -c "import pypeec; print('PyPEEC', pypeec.__version__)"
echo "ready: Python in $ROOT/.venv"
