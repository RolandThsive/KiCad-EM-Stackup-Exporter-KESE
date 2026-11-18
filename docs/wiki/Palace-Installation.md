# 62. Palace Installation

The bridge needs three things: Palace, a Python environment with the bridge's packages, and, only to export a board
whose export is not committed, a copy of KESE. Unlike the other solvers' branches, `Palace_Integration` carries Palace
itself: `Solver_Palace/install/` holds the build every simulation on the branch ran with, so a fresh copy of the branch
runs without building anything, and every machine solves with the same program.

## 62.1 The Committed Build

| Item | Value |
|---|---|
| Program | Palace 0.19.0, AWS Labs' release (tag `v0.19.0`, commit `ca9a6a2`); it prints `v0.19.0-dirty` because a patch is applied to the release's source (see [62.4](#624-why-it-is-built-without-parmetis)) |
| Build | Palace's own CMake superbuild, which builds MFEM 4.10, hypre 3.2.0, libCEED 1.0.1, METIS 5.1.0, ARPACK-NG, GSLIB and the rest at the versions Palace 0.19.0 pins; GCC 13.3 and Open MPI 4.1.6 on Ubuntu 24.04, release build, double precision, no OpenMP and no GPU |
| Solvers in it | hypre's AMS (the auxiliary-space Maxwell preconditioner) under GMRES. No sparse direct solver |
| Files | `install/bin/palace` (the launcher script, which starts the program under `mpirun`), `install/bin/palace-x86_64.bin` (the program, 36.5 MB, statically linked but for the system libraries below) and `install/lib/libceed.so` |
| Runs on | 64-bit Linux with glibc 2.38 or newer (Ubuntu 24.04 and up), with Open MPI 4.1, OpenBLAS, gfortran's runtime and zlib from the system |
| Licence | Apache 2.0 for Palace; every library built into it is open source (BSD, MIT, Apache 2.0, MPL 2.0), with its licence text in `Solver_Palace/licenses/` |

The SHA-256 of each of the three files is listed in `Solver_Palace/README.md`. Check the program with:

```bash
Solver_Palace/install/bin/palace --version
```

The bridge finds Palace by itself: `$PALACE` if it is set, else `Solver_Palace/install/bin/palace`, else `palace` on
the `PATH` (`palace_exe` in `bridge/palace_case.py`).

## 62.2 Linux (Ubuntu 24.04)

One script sets up a fresh machine, from the branch's root:

```bash
bash bridge/setup_machine.sh
```

It installs the system libraries the committed Palace runs with (`openmpi-bin`, `libopenmpi3t64`, `libopenblas0`,
`libgfortran5`, `zlib1g`), the libraries gmsh's wheel needs even without a display, makes `.venv` at the branch's root
with the packages of `requirements.txt`, and prints Palace's version and the Python packages'. Where the committed
Palace does not run, it builds Palace from source instead (below). It needs Python 3.12 or newer and is safe to run
again.

| Package (`requirements.txt`) | Version | Used by |
|---|---|---|
| numpy, scipy | 2.5.3, 1.18.1 | the bridge and the references |
| shapely, trimesh, mapbox_earcut | 2.2.0, 5.2.1, 2.1.0 | sectioning KESE's solids and the 2D outlines |
| gmsh | 4.15.2 | the triangle mesh and the tetrahedra |
| matplotlib, pillow | 3.11.2, 13.0.0 | the coil examples' charts and pictures |

**KESE** is needed only for a board whose `3D_Geometry/` export is not committed (every example's is). Copy main's
`Generator/` into `3D_Geometry/`, or set `KESE_PATH` to `run_KESE.py` or its folder. KESE's own packages
(`Generator/requirements.txt` on `main`) go into the same `.venv`.

## 62.3 Building Palace From Source

About an hour on four cores and 3 GB of disk while it builds:

```bash
sudo apt install git cmake build-essential gfortran openmpi-bin libopenmpi-dev libopenblas-dev zlib1g-dev \
                 pkg-config patchelf
bash Solver_Palace/build_palace.sh
```

The script clones Palace at `v0.19.0`, checks the commit, applies `no_parmetis.patch`, runs Palace's superbuild and
puts the program in `Solver_Palace/install/`, with its run path set so that it finds `libceed.so` beside it wherever the
folder is.

| Variable | What it does |
|---|---|
| `JOBS=8` | Parallel build jobs (default: every core) |
| `WORK=/data/palace` | Keeps the source and the build there (default: a temporary folder, removed afterwards) |
| `LOCAL_PATCHES=1` | Makes the patches the superbuild would download from github.com's commit and compare links with git from MFEM's and hypre's own repositories instead; the committed program was built this way, and the diffs are the same files, byte for byte |
| `WITH_MUMPS=1` | Adds MUMPS, ordered by METIS; not tried, since MUMPS's source comes from mumps-solver.org, which the test machine's network refused |

The script refuses to install a program in which any ParMETIS symbol is found.

## 62.4 Why It Is Built Without ParMETIS

Palace's release build links ParMETIS for the orderings of its direct solvers. ParMETIS is not open source: its
licence limits use to non-profit research and education and forbids redistribution without the University of
Minnesota's approval. A program with ParMETIS in it could not be committed or used freely, so `no_parmetis.patch`
makes it optional:

* ParMETIS is built and linked only with SuperLU_DIST or STRUMPACK, which are both left out;
* MUMPS, where it is built, is ordered by METIS alone (METIS is Apache 2.0 since 5.0.2);
* Palace's version report leaves ParMETIS out when it is not linked;
* MFEM is given hypre's BLAS and LAPACK (OpenBLAS) to link with, which a build with no direct solver otherwise lacks.

MFEM still partitions the mesh between the MPI ranks with METIS. The price is that the build has no direct solver,
so every solve is checked instead ([Palace Accuracy](Palace-Accuracy.md)).

## 62.5 Windows

The committed program and the build script are for 64-bit Linux, and every solve on the branch ran on Linux.
Windows has not been tried.

## 62.6 What The Test Machine Had

| Item | Version |
|---|---|
| OS | Ubuntu 24.04, 4 cores, 15 GB of memory |
| Palace | 0.19.0 (`0.19.0-dirty`), the committed build |
| KESE | 3.4.0 (made the exports) |
| Python | 3.13 |
| gmsh | 4.15.2 |
| numpy, scipy, shapely, trimesh, mapbox_earcut | 2.5.3, 1.18.1, 2.2.0, 5.2.1, 2.1.0 |

Every results file on the branch records the versions it ran with, so each number on
[Palace Test Board Results](Palace-Test-Board-Results.md) names the software that made it.

| Previous | Next |
|:---|---:|
| [Palace Introduction](Palace-Introduction.md) | [Palace Workflow](Palace-Workflow.md) |
