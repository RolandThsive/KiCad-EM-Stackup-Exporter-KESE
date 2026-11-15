# Solver_Elmer

This folder is empty on purpose: Elmer is built here from its own source, on the machine that runs
the simulations.  Checked on Ubuntu 24.04 on 15 November 2026 with Elmer release 26.2.1.

## Ubuntu 24.04

```
sudo apt-get update
sudo apt-get install -y build-essential cmake git gfortran libopenmpi-dev libblas-dev liblapack-dev \
    libopenblas-dev libmumps-dev libparmetis-dev libscalapack-openmpi-dev
cd Solver_Elmer
git clone --depth 1 --branch release-26.2.1 https://github.com/ElmerCSC/elmerfem.git elmerfem
mkdir build && cd build
cmake ../elmerfem -DCMAKE_BUILD_TYPE=Release -DWITH_ELMERGUI:BOOL=FALSE -DWITH_MPI:BOOL=TRUE \
    -DWITH_OpenMP:BOOL=TRUE -DWITH_Mumps:BOOL=TRUE -DCMAKE_INSTALL_PREFIX=$PWD/../install
make -j"$(nproc)" install
```

The bridge looks for `Solver_Elmer/install/bin/ElmerSolver` and `ElmerGrid`.  gmsh, the mesher, comes
from PyPI into the bridge's Python environment: `pip install gmsh==4.15.2`.

## Windows and macOS

Elmer's repository has build instructions for Windows (MSYS2) and macOS; follow those, and install
into `Solver_Elmer/install` so the bridge finds it.
