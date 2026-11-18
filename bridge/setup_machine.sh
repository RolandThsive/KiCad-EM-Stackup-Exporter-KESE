#!/bin/bash
# Sets up a fresh Ubuntu 24.04 machine for the bridge: the system libraries the committed Palace 0.19.0 in
# Solver_Palace/install runs with (Open MPI, OpenBLAS, gfortran's runtime, zlib, all free), and the Python packages of
# requirements.txt in .venv, at the versions the examples ran with. Run it from anywhere in the branch:
#
#     bash bridge/setup_machine.sh
#
# Where the committed Palace does not run (another system), the script builds it from source with
# Solver_Palace/build_palace.sh (an hour on four cores; JOBS=... sets the parallel jobs). Needs Python 3.12 or newer
# (numpy 2.5). Safe to run again. KESE is not needed for a board whose 3D_Geometry/ is committed.
# This script is GPL-3.0 as the bridge.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SUDO=""
[ "$(id -u)" = 0 ] || SUDO=sudo
PALACE="$ROOT/Solver_Palace/install/bin/palace"
export OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
if ! ldconfig -p | grep -q 'libmpi.so.40' || ! ldconfig -p | grep -q 'libopenblas.so.0'; then
  $SUDO apt-get update -q
  $SUDO apt-get install -y -q openmpi-bin libopenmpi3t64 libopenblas0 libgfortran5 zlib1g
fi
if ! "$PALACE" --version >/dev/null 2>&1; then
  $SUDO apt-get update -q
  $SUDO apt-get install -y -q git cmake build-essential gfortran openmpi-bin libopenmpi-dev libopenblas-dev \
    zlib1g-dev pkg-config patchelf python3
  bash "$ROOT/Solver_Palace/build_palace.sh"
fi
# gmsh's wheel needs these system libraries even without a display
if ! ldconfig -p | grep -q libGLU.so.1; then
  $SUDO apt-get install -y -q libglu1-mesa libgl1 libxcursor1 libxft2 libxinerama1 libxrender1 libxfixes3
fi
PY="${PYTHON:-python3}"
if [ ! -x "$ROOT/.venv/bin/python" ]; then
  "$PY" -m venv "$ROOT/.venv" || { $SUDO apt-get install -y -q python3-venv && "$PY" -m venv "$ROOT/.venv"; }
fi
"$ROOT/.venv/bin/pip" install -q --upgrade pip
"$ROOT/.venv/bin/pip" install -q -r "$ROOT/requirements.txt"
"$PALACE" --version
"$ROOT/.venv/bin/python" -c "import numpy, shapely, gmsh; print('numpy', numpy.__version__, 'shapely', shapely.__version__, 'gmsh', gmsh.__version__)"
echo "ready: Palace in $ROOT/Solver_Palace/install, Python in $ROOT/.venv"
