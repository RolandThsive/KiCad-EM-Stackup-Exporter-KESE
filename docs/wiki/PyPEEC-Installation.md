# 44. PyPEEC Installation

The bridge needs two things: a Python environment with PyPEEC and the bridge's packages, and, only to
export a board whose geometry is not committed, a copy of KESE. PyPEEC is pure Python, so nothing is
compiled for it, but it runs on numpy, scipy, VTK, Qt and others that are. The branch commits the very
build every simulation ran with, in `Solver_PyPEEC/`.

## 44.1 Linux (Ubuntu 24.04)

This is the route the test boards ran on, with Python 3.13 and PyPEEC 5.8.0.

**PyPEEC, from the committed wheels**, with no internet, from the branch's root:

```bash
bash Solver_PyPEEC/install.sh
.venv/bin/python -c "import pypeec; print(pypeec.__version__)"      # 5.8.0
```

`install.sh` makes `.venv` and installs every wheel of `Solver_PyPEEC/wheels/` into it at exactly the
versions of `requirements-lock.txt`. Two wheels are over GitHub's 100 MB limit (VTK and Qt WebEngine)
and are kept in two parts each, `.part0` and `.part1`; the script joins them, checks every wheel
against `SHA256SUMS`, and only then installs. `PYTHON=...` picks the Python 3.13 to use, `VENV=...`
where the environment goes.

| | |
|---|---|
| Package | `pypeec==5.8.0`, with `scisave==1.6.0` (its file formats) and everything under them: 56 packages, 514 MB of wheels |
| Wheels | from PyPI on 17 November 2026, unmodified: `manylinux` builds for x86_64, CPython 3.13 (or abi3 for 3.10 and up) |
| Needs | 64-bit Linux, Python 3.13, glibc 2.34 or newer (Ubuntu 22.04 and up) |
| Speed-ups | none: PyPEEC's defaults, SciPy's FFT and SuperLU. PyPEEC's optional FFTW, PARDISO and CuPy are not used, since MKL and CUDA are not free software |

**Or in one step:** `bash bridge/setup_machine.sh` does the same where it finds Python 3.13, and
otherwise installs the same versions from PyPI with the system's Python 3 (Ubuntu 24.04's is 3.12).
It installs `python3-venv` when the system lacks it and is safe to run again.

**KESE**, only for a board whose `3D_Geometry/` is not committed (E01 and E02 export their board on
the first run; the coil board's export is committed). Copy `main`'s `Generator/` so that
`run_KESE.py` sits directly in `3D_Geometry/`:

```bash
git -C <your KESE clone> archive main Generator | tar -x --strip-components=1 -C 3D_Geometry
.venv/bin/python 3D_Geometry/run_KESE.py --help
```

or point the bridge at any KESE with `KESE_PATH`. KESE runs in the bridge's Python, so its own
packages (`Generator/requirements.txt` on `main`) go into the same environment.

**Check the whole chain** with the first proof board at 50 µm voxels (with KESE in place, for its
export), written to its own results file so the committed `results.json` stays as it is:

```bash
cd Examples/E01_circular_loop
../../.venv/bin/python simulation.py --voxels 0.05 --results check.json
```

It should print L 56.59 nH and R 65.23 mΩ at 10 kHz, and L 55.61 nH and R 81.93 mΩ at 3.5 MHz, the
50 µm values of [PyPEEC Test Board Results](PyPEEC-Test-Board-Results.md#481-e01-circular-loop),
in about 3 and 8 seconds. To check without KESE, solve the coil board, whose export is committed:
`python simulation.py --angles 0 --no-away --trial check` in its `PyPEEC Simulation/` folder (about
4 minutes and 2.4 GB at the default 1 mm air gap; `--trial` keeps the results in `case/`, away from the
committed ones). It should give L TX 271.54 nH and M SIN −3.0957 nH.

## 44.2 Windows And macOS

The committed wheels are for 64-bit Linux only. PyPEEC itself runs on Linux, Windows and macOS, so
install the same versions from PyPI instead (Python 3.12 or 3.13: numpy 2.5 and scipy 1.18 need 3.12;
PyPEEC itself runs from 3.10):

| Route | Steps | Notes |
|---|---|---|
| **WSL 2 (recommended on Windows)** | Install Ubuntu 24.04 from the Microsoft Store, then follow [44.1](#441-linux-ubuntu-2404) inside it | The committed wheels then fit as on Linux. Keep the repository inside the WSL file system, not under `/mnt/c` |
| **Native** | `py -m venv .venv`, then `.venv\Scripts\pip install -r Solver_PyPEEC/requirements-lock.txt` (macOS: `.venv/bin/pip install ...`) | The same versions, from PyPI. Not yet run on the test boards |

`requirements.txt` at the branch's root lists only the packages the bridge asks for by name (PyPEEC,
scisave, numpy, scipy, shapely, trimesh, mapbox_earcut, and matplotlib and pillow for the charts);
`Solver_PyPEEC/requirements-lock.txt` lists every package of the environment, as `pip freeze` wrote
it.

## 44.3 What The Test Machine Had

| Item | Version |
|---|---|
| OS | Ubuntu 24.04, 4 cores, 15 GB of memory |
| Python | 3.13.18 |
| PyPEEC | 5.8.0, with scisave 1.6.0 |
| numpy, scipy, shapely, trimesh | 2.5.5, 1.18.1, 2.2.0, 5.2.1 |
| KESE | 3.4.0, which made every export |

Each example writes the versions it ran with into its results files, so every number on
[PyPEEC Test Board Results](PyPEEC-Test-Board-Results.md) names the software that made it. Where the
machine that solved a coil board had no KESE, the results name the KESE that made the committed export
(`kese 3.4.0 (made the export; not installed where this ran)`).

| Previous | Next |
|:---|---:|
| [PyPEEC Introduction](PyPEEC-Introduction.md) | [PyPEEC Workflow](PyPEEC-Workflow.md) |
