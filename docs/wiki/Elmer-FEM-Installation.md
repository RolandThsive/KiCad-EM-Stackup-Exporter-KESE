# 25. Elmer FEM Installation

The bridge needs three things: Elmer built with OpenMP and a direct solver for the circuit block,
a Python environment with the bridge's packages, and a copy of KESE. The branch never carries Elmer
or KESE itself: `Solver_Elmer/` and `3D_Geometry/` are empty on purpose and are filled by hand.

## 25.1 Linux (Ubuntu 24.04)

This is the route the test boards ran on, with Elmer release 26.2.1.

**Elmer**, built into `Solver_Elmer/install`:

```bash
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

The bridge looks for `Solver_Elmer/install/bin/ElmerSolver`; check it with
`Solver_Elmer/install/bin/ElmerSolver -v`, whose banner says whether MUMPS is linked in.

> [!IMPORTANT]
> Keep MUMPS (or UMFPACK) in the build. The bridge solves the field with an iterative method, but
> Elmer's `Circuit` preconditioner factorises the small circuit block with a direct solver and stops
> with *Preconditioner "circuit" needs either Umfpack or MUMPS* when neither is there.

**Python**, in a virtual environment at the branch's root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt       # numpy, scipy, shapely, trimesh, gmsh, mapbox_earcut
```

**KESE**, copied from `main` so that `run_KESE.py` sits directly in `3D_Geometry/`:

```bash
git -C <your KESE clone> archive main Generator | tar -x --strip-components=1 -C 3D_Geometry
.venv/bin/python 3D_Geometry/run_KESE.py --help
```

or leave `3D_Geometry/` empty and point the bridge at any KESE with `export KESE_PATH=<path to
Generator>`. KESE runs inside the bridge's Python, so its own packages (`requirements.txt` in
`Generator/`) must be in the same environment; a missing one stops the export with *missing Python
package(s)* and the `pip install` line to fix it.

**Check the whole chain** with the first proof board, on its coarsest mesh at 3.5 MHz, where the
solve converges (several minutes on 4 cores; a 10 kHz solve runs to its iteration cap and takes about
25 minutes):

```bash
cd Examples/E01_circular_loop
../../.venv/bin/python simulation.py --levels 0.75 --freqs 3.5e6
```

## 25.2 Windows

Elmer publishes Windows builds with its releases
([ElmerFEM releases](https://github.com/ElmerCSC/elmerfem/releases)). Before using one, run
`ElmerSolver -v` and check that its banner names MUMPS (or that the build lists UMFPACK), for the
reason in the note above. Two routes:

| Route | Steps | Notes |
|---|---|---|
| **WSL 2 (recommended)** | Install Ubuntu 24.04 from the Microsoft Store, then follow [25.1](#251-linux-ubuntu-2404) inside it | The bridge, KESE and Elmer all run as on Linux. Keep the repository inside the WSL file system (not under `/mnt/c`), which is many times faster for the mesh files |
| **Native** | Install Elmer from the release's Windows installer; install Python 3.11 or later from python.org; create the virtual environment with `py -m venv .venv` and `.venv\Scripts\pip install -r requirements.txt`; copy or link Elmer's `bin` folder to `Solver_Elmer\install\bin` | The bridge calls `ElmerSolver` from `Solver_Elmer/install/bin`, so that folder must hold `ElmerSolver.exe`. Not yet run on the test boards |

## 25.3 What The Test Machine Had

| Item | Version |
|---|---|
| OS | Ubuntu 24.04, 4 cores, 15 GB of memory |
| Elmer | 26.2 (release 26.2.1, OpenMP, MPI, MUMPS, UMFPACK) |
| Python | 3.13 |
| gmsh | 4.15.2 (from PyPI) |
| numpy, scipy, shapely, trimesh | 2.5.3, 1.18.1, 2.2.0, 5.2.1 |

Each example writes the versions it ran with into its `results.json`, so every number on
[Elmer FEM Test Board Results](Elmer-FEM-Test-Board-Results.md) names the software that made it.

| Previous | Next |
|:---|---:|
| [Elmer FEM Introduction](Elmer-FEM-Introduction.md) | [Elmer FEM Workflow](Elmer-FEM-Workflow.md) |
