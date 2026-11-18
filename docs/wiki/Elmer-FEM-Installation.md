# 25. Elmer FEM Installation

The bridge needs three things: Elmer with OpenMP and the MUMPS direct solver, a Python environment
with the bridge's packages, and a copy of KESE. The branch carries the Elmer every example ran on,
built for Ubuntu 24.04, in `Solver_Elmer/install/`; it never carries KESE, so `3D_Geometry/` is empty
on purpose and is filled by hand.

## 25.1 Linux (Ubuntu 24.04)

### The Committed Elmer

`Solver_Elmer/install/` is Elmer 26.2.1 with MUMPS, built for 64-bit Linux on Ubuntu 24.04. It only
needs the libraries it runs with, installed once:

```bash
sudo apt-get install -y libgfortran5 libgomp1 libopenblas0 libopenmpi3t64 libmumps-5.6t64
cd Solver_Elmer
ldd install/lib/elmersolver/libelmersolver.so | grep 'not found'     # prints nothing when every library is there
install/bin/ElmerSolver -v | grep -m1 Version
```

The bridge looks for `Solver_Elmer/install/bin/ElmerSolver` and tells Elmer that `install/` is its
home, so the folder works wherever the branch is checked out. To run Elmer by hand rather than through
the bridge, set `ELMER_HOME` to that `install` folder first; without it Elmer stops with
*elements.def not found*.

| What the build is | |
|---|---|
| Source | [ElmerCSC/elmerfem](https://github.com/ElmerCSC/elmerfem), tag `release-26.2.1`, commit `a19504a`, unmodified |
| Built | 15 November 2026, Ubuntu 24.04, GNU Fortran 13.3.0, Release |
| With | MPI (Open MPI), OpenMP, MUMPS 5.6 from Ubuntu; no ElmerGUI, no Hypre, no ParMETIS |
| Licence | GPL-2.0 or later, its library LGPL-2.1; the texts are in `install/share/elmersolver/license_texts/` |

### One Command For A Fresh Machine

```bash
bash bridge/setup_machine.sh
```

installs the libraries above, the system libraries gmsh's wheel needs, and the Python packages of
`requirements.txt` into `.venv` at the branch's root. It is safe to run again, and builds Elmer from
source only if `Solver_Elmer/install/bin/ElmerSolver` is missing.

### Building Elmer Yourself

The commands that made `install/`:

```bash
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

> [!NOTE]
> ParMETIS is left out on purpose: nothing in `install/` links it (checked with `ldd` on every binary
> and library), and its licence is not an open-source one. `elmerfem/` and `build/` stay out of git.

> [!IMPORTANT]
> Keep MUMPS in the build. The coil board solves its field with MUMPS, the bridge solves each coil's
> current direction with UMFPACK, and Elmer's `Circuit` preconditioner for the iterative solve
> factorises the circuit block with a direct solver; without one it stops with *Preconditioner
> "circuit" needs either Umfpack or MUMPS*.

### Python

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt       # numpy, scipy, shapely, trimesh, gmsh, mapbox_earcut
```

### KESE

Copied from `main` so that `run_KESE.py` sits directly in `3D_Geometry/`:

```bash
git -C <your KESE clone> archive main Generator | tar -x --strip-components=1 -C 3D_Geometry
.venv/bin/python 3D_Geometry/run_KESE.py --help
```

or leave `3D_Geometry/` empty and point the bridge at any KESE with `export KESE_PATH=<path to
Generator>`. KESE runs inside the bridge's Python, so its own packages (`requirements.txt` in
`Generator/`) must be in the same environment. The coil board does not need KESE to run: its export
is committed in its own `3D_Geometry/` folder and is reused while the board is unchanged.

### Check The Whole Chain

With the first proof board, on its coarsest mesh at 3.5 MHz:

```bash
cd Examples/E01_circular_loop
../../.venv/bin/python simulation.py --levels 0.75 --freqs 3.5e6 --out case_check --results check.json
```

The committed results give L 52.93 nH and R 80.19 mOhm for this solve (3 minutes on the 4-core test
machine), the level 0.75 values of
[Elmer FEM Test Board Results](Elmer-FEM-Test-Board-Results.md#291-e01-circular-loop); its own
`--results` file keeps the committed `results.json` as it is. Those results were made with the
bridge of 15 and 16 November (see 29.1), so today's bridge may differ in the last digits.

### A Swap File For The Coil Board

The coil board's direct solves need more memory than a 16 GB machine has
([Elmer FEM Hardware](Elmer-FEM-Hardware.md#313-the-coil-board)). On Linux a swap file makes up the
rest:

```bash
sudo fallocate -l 26G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile
```

## 25.2 Windows

The committed build runs inside WSL with Ubuntu 24.04, the same way as on Linux. It does not run on
Windows itself, on macOS, or on another Linux release without its libraries at these versions.

| Route | Steps | Notes |
|---|---|---|
| **WSL 2 (recommended)** | Install Ubuntu 24.04 from the Microsoft Store, then follow [25.1](#251-linux-ubuntu-2404) inside it | The bridge, KESE and Elmer all run as on Linux. Keep the repository inside the WSL file system (not under `/mnt/c`), which is many times faster for the mesh files |
| **Native** | Build Elmer with the instructions in Elmer's repository (MSYS2) and install it into `Solver_Elmer\install`; install Python 3.11 or later from python.org; `py -m venv .venv` and `.venv\Scripts\pip install -r requirements.txt` | The bridge calls `ElmerSolver` from `Solver_Elmer/install/bin`, so that folder must hold `ElmerSolver.exe`. Not yet run on the test boards |

macOS has the same route as native Windows: build Elmer with the instructions in its repository and
install it into `Solver_Elmer/install`.

## 25.3 What The Test Machines Had

| Item | Version |
|---|---|
| OS | Ubuntu 24.04; E01 and E02 on 4 cores and 15 GB, the coil board on 16 GB machines with a swap file |
| Elmer | 26.2 (release 26.2.1, `a19504a`, OpenMP, MPI, MUMPS, UMFPACK) |
| Python | 3.13 |
| gmsh | 4.15.2 (from PyPI) |
| numpy, scipy, shapely, trimesh | 2.5.3, 1.18.1, 2.2.0, 5.2.1 |

Each example writes the versions it ran with into its results files, so every number on
[Elmer FEM Test Board Results](Elmer-FEM-Test-Board-Results.md) names the software that made it.

| Previous | Next |
|:---|---:|
| [Elmer FEM Introduction](Elmer-FEM-Introduction.md) | [Elmer FEM Workflow](Elmer-FEM-Workflow.md) |
