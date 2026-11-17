# Solver_PyPEEC

[PyPEEC](https://github.com/otvam/pypeec) is the solver of this branch: a 3D magneto-quasi-static solver by Thomas
Guillod (Dartmouth College) that uses the PEEC method on voxels. It is pure Python, published on PyPI, so nothing is
built here: it goes into the bridge's Python environment with the other packages of
[`../requirements.txt`](../requirements.txt), at the version every simulation in this branch ran with.

| | |
|---|---|
| Package | `pypeec==5.8.0` from PyPI, with `scisave==1.6.0` (its file formats) |
| Runs on | Linux, Windows and macOS, Python 3.12 or 3.13 with these pins (PyPEEC itself from 3.10; numpy 2.5 and scipy 1.18 need 3.12); checked here on Ubuntu 24.04, Python 3.13 |
| Speed-ups | none: PyPEEC's defaults, SciPy's FFT and SuperLU. Its optional FFTW, PARDISO and CuPy are not used (MKL and CUDA are not free software) |
| Tolerances | [`../bridge/tolerance.yaml`](../bridge/tolerance.yaml): PyPEEC's own defaults, from its examples |
| Licence | MPL-2.0 |

## Installing it

On Ubuntu (24.04 checked), from the branch's root:

```
bash bridge/setup_machine.sh
```

It makes `.venv` and installs `requirements.txt` into it. By hand, on any system with Python 3.12 or 3.13:

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt          # Windows: .venv\Scripts\pip install -r requirements.txt
.venv/bin/python -c "import pypeec; print(pypeec.__version__)"
```

Then run an example with that Python, for instance
`.venv/bin/python "Examples/Inductive Coils/S0_1x_OD21_2L_tiny/PyPEEC Simulation/simulation.py" --gap 1`.

## How much it needs

A coil board's solve, one rotor angle, on 4 cores: about 5 minutes and 2.3 GB at a 1 mm air gap with 50 µm voxels,
more at wider gaps (the grid grows taller with the gap). E01 and E02 take seconds to a few minutes. Each board's
README gives its own numbers.
