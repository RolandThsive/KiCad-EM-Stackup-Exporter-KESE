# Solver_PyPEEC

[PyPEEC](https://github.com/otvam/pypeec) is the solver of this branch: a 3D magneto-quasi-static solver by Thomas
Guillod (Dartmouth College) that uses the PEEC method on voxels. It is pure Python, so nothing is compiled for it,
but it runs on numpy, scipy, VTK, Qt and others that are. `wheels/` is the build every simulation in this branch ran
with: PyPEEC 5.8.0 and all 56 packages under it, at the exact versions installed here, as the wheel files PyPI
serves for 64-bit Linux and Python 3.13. It is committed so a fresh copy of the branch can install the very same
environment without the internet, and so every machine solves with the same packages.

| | |
|---|---|
| Package | `pypeec==5.8.0`, with `scisave==1.6.0` (its file formats) and everything under them, in `wheels/` (514 MB) |
| Wheels | from PyPI on 17 November 2026, unmodified: `manylinux` builds for x86_64, CPython 3.13 (or abi3 for 3.10 and up), needing glibc 2.34 or newer (Ubuntu 22.04 and up) |
| Runs on | Linux, Windows and macOS, Python 3.12 or 3.13 with these pins (PyPEEC itself from 3.10; numpy 2.5 and scipy 1.18 need 3.12); checked here on Ubuntu 24.04, Python 3.13 |
| Speed-ups | none: PyPEEC's defaults, SciPy's FFT and SuperLU. Its optional FFTW, PARDISO and CuPy are not used (MKL and CUDA are not free software) |
| Tolerances | [`../bridge/tolerance.yaml`](../bridge/tolerance.yaml): PyPEEC's own defaults, from its examples |
| Licence | PyPEEC MPL-2.0; every other wheel keeps its own licence, inside it (`*.dist-info/`): numpy, scipy, VTK and matplotlib BSD-style, PySide6 and Qt LGPL-3.0, among others |

## Installing it

On 64-bit Linux with Python 3.13 (Ubuntu 24.04 checked), from the branch's root:

```
bash Solver_PyPEEC/install.sh
```

It makes `.venv` and installs every wheel of `wheels/` into it, with no internet: it joins the two wheels kept in
parts (VTK and Qt WebEngine are over GitHub's 100 MB limit, so each is split in two, `.part0` and `.part1`), checks
every wheel against `SHA256SUMS`, and installs exactly the versions of `requirements-lock.txt`. `PYTHON=...` picks
the Python 3.13 to use, `VENV=...` where the environment goes. `bash bridge/setup_machine.sh` does the same where it finds
Python 3.13, and otherwise installs the same versions from PyPI with the system's Python 3 (Ubuntu 24.04's is 3.12). To check it:

```
.venv/bin/python -c "import pypeec; print(pypeec.__version__)"              # 5.8.0
```

On Windows, macOS or another Python, these wheels do not fit; install the same versions from PyPI instead:

```
python3 -m venv .venv
.venv/bin/pip install -r Solver_PyPEEC/requirements-lock.txt     # Windows: .venv\Scripts\pip install -r ...
```

[`../requirements.txt`](../requirements.txt) lists only the packages the bridge asks for by name, and
`requirements-lock.txt` every package of the environment, as `pip freeze` wrote it.

Then run an example with that Python, for instance
`.venv/bin/python "Examples/Inductive Coils/S0_1x_OD21_2L_tiny/PyPEEC Simulation/simulation.py" --gap 1`.

## How much it needs

A coil board's solve, one rotor angle, on 4 cores: about 5 minutes and 2.3 GB at a 1 mm air gap with 50 µm voxels,
more at wider gaps (the grid grows taller with the gap). E01 and E02 take seconds to a few minutes. Each board's
README gives its own numbers.
