#!/bin/bash
# Sets up a fresh Ubuntu 24.04 machine for the bridge: Elmer 26.2.1 built into Solver_Elmer/install, and the Python
# packages of requirements.txt in .venv, at the versions the examples ran with. Run it from anywhere in the branch:
#
#     bash bridge/setup_machine.sh            (JOBS=2 bash bridge/setup_machine.sh to build with fewer jobs)
#
# Safe to run again: Elmer is set up only if Solver_Elmer/install/bin/ElmerSolver is missing. If ELMER_TARBALL names a
# packed Solver_Elmer/install of the same release built on Ubuntu 24.04 (tar -czf ... install), it is unpacked
# instead of building (the install finds its libraries relative to itself). KESE is not needed for a board whose
# 3D_Geometry/ is committed. This script is GPL-3.0 as the bridge.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
E="$ROOT/Solver_Elmer"
JOBS="${JOBS:-$(nproc)}"
SUDO=""
[ "$(id -u)" = 0 ] || SUDO=sudo
if [ ! -x "$E/install/bin/ElmerSolver" ]; then
  $SUDO apt-get update -q
  $SUDO apt-get install -y -q build-essential cmake git gfortran libopenmpi-dev libblas-dev liblapack-dev \
    libopenblas-dev libmumps-dev libparmetis-dev libscalapack-openmpi-dev python3-venv
  if [ -n "${ELMER_TARBALL:-}" ] && [ -f "$ELMER_TARBALL" ]; then
    tar -xzf "$ELMER_TARBALL" -C "$E"
  fi
fi
if [ ! -x "$E/install/bin/ElmerSolver" ]; then
  [ -d "$E/elmerfem" ] || git clone -q --depth 1 --branch release-26.2.1 https://github.com/ElmerCSC/elmerfem.git \
    "$E/elmerfem"
  mkdir -p "$E/build"
  cd "$E/build"
  cmake ../elmerfem -DCMAKE_BUILD_TYPE=Release -DWITH_ELMERGUI:BOOL=FALSE -DWITH_MPI:BOOL=TRUE \
    -DWITH_OpenMP:BOOL=TRUE -DWITH_Mumps:BOOL=TRUE -DCMAKE_INSTALL_PREFIX="$E/install" > "$E/build/cmake.log"
  make -j"$JOBS" install > "$E/build/make.log"
fi
if [ ! -x "$ROOT/.venv/bin/python" ]; then
  python3 -m venv "$ROOT/.venv" || { $SUDO apt-get install -y -q python3-venv && python3 -m venv "$ROOT/.venv"; }
fi
"$ROOT/.venv/bin/pip" install -q -r "$ROOT/requirements.txt"
"$E/install/bin/ElmerSolver" -v 2>/dev/null | grep -m1 'Version' || true
echo "ready: Elmer in $E/install, Python in $ROOT/.venv"
