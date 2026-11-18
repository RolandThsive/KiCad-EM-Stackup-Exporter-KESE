# Solver_Elmer

`install/` is the Elmer every simulation in this branch ran on: Elmer 26.2.1 with MUMPS, the direct solver the
coil boards use, built for 64-bit Linux on Ubuntu 24.04. It is committed so a fresh copy of the branch can run the
examples without building Elmer, and so every machine solves with the same Elmer. The bridge looks for
`install/bin/ElmerSolver` here, and tells Elmer that `install/` is its home, so the folder works wherever the
branch is checked out.

## Running it

On Ubuntu 24.04, install the libraries it uses, once:

```
sudo apt-get install -y libgfortran5 libgomp1 libopenblas0 libopenmpi3t64 libmumps-5.6t64
```

or run `bash bridge/setup_machine.sh`, which installs these and the Python packages. To check it works, from this
folder:

```
ldd install/lib/elmersolver/libelmersolver.so | grep 'not found'     # prints nothing when every library is there
install/bin/ElmerSolver -v | grep -m1 Version
```

To run Elmer by hand rather than through the bridge, set `ELMER_HOME` to this `install` folder first; without it
Elmer stops with "elements.def not found".

On Windows, it runs inside WSL with Ubuntu 24.04, the same way. It does not run on Windows itself, on macOS, or on
another Linux release without its libraries at these versions; build Elmer there as below.

## What it is

| | |
|---|---|
| Source | [ElmerCSC/elmerfem](https://github.com/ElmerCSC/elmerfem), tag `release-26.2.1`, commit `a19504ac53ec222e3355e182b08f2ff280c2203a`, unmodified |
| Built | 15 November 2026, Ubuntu 24.04, GNU Fortran 13.3.0, Release |
| With | MPI (Open MPI), OpenMP, MUMPS 5.6 from Ubuntu; no ElmerGUI, no Hypre |
| Licence | GPL-2.0 or later, its library LGPL-2.1: the texts are in `install/share/elmersolver/license_texts/` |

## Building it yourself

The same build, from source (the commands that made `install/`):

```
sudo apt-get update
sudo apt-get install -y build-essential cmake git gfortran libopenmpi-dev libblas-dev liblapack-dev \
    libopenblas-dev libmumps-dev libscalapack-openmpi-dev
cd Solver_Elmer
git clone --depth 1 --branch release-26.2.1 https://github.com/ElmerCSC/elmerfem.git elmerfem
mkdir build && cd build
cmake ../elmerfem -DCMAKE_BUILD_TYPE=Release -DWITH_ELMERGUI:BOOL=FALSE -DWITH_MPI:BOOL=TRUE \
    -DWITH_OpenMP:BOOL=TRUE -DWITH_Mumps:BOOL=TRUE -DCMAKE_INSTALL_PREFIX=$PWD/../install
make -j"$(nproc)" install
```

ParMETIS is not needed: nothing in `install/` links it (checked with `ldd` on every binary and library), and its
licence is not an open-source one, so it is left out. `elmerfem/` and `build/` stay out of git. gmsh, the mesher, comes from PyPI into the bridge's Python environment:
`pip install gmsh==4.15.2`.

Elmer's repository has build instructions for Windows (MSYS2) and macOS; follow those, and install into
`Solver_Elmer/install` so the bridge finds it.
