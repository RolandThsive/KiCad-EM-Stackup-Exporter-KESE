# KESE PyPEEC Integration

This branch turns a KiCad board into a [PyPEEC](https://github.com/otvam/pypeec) simulation and checks the answer
against a reference. KESE stays what it is, a 3D geometry exporter: the bridge here runs it with `--for elmer` (the
same export as the Elmer branch, so both branches solve the same copper), draws its copper onto PyPEEC's uniform
voxel grid, writes PyPEEC's input and reads back inductance, resistance and mutual inductance from its
magneto-quasi-static solve. PyPEEC (by Thomas Guillod, MPL-2.0) uses the PEEC method: only the copper carries
unknowns, the air needs no mesh at all, and the couplings between voxels are products with FFTs.

Every example lives in its own folder under `Examples/`, with its board, its `simulation.py` and a `README.md` that
says what the board is, what it is for, what PyPEEC checks on it, and, in its Results section, what was expected and
what came out. The inductive encoder coils are in `Examples/Inductive Coils/`, laid out as on the Elmer branch.

## Layout

| Folder | What it holds |
|---|---|
| `3D_Geometry/` | Empty on purpose: copy KESE's `Generator/` in from `main` by hand (see its README), only to export a board whose `3D_Geometry/` is not committed |
| `Solver_PyPEEC/` | The PyPEEC build every simulation here ran with: PyPEEC 5.8.0 and every package under it as committed wheels for 64-bit Linux and Python 3.13, with `install.sh`, which installs them into `.venv` without the internet; what it runs on and what it needs (see its README) |
| `bridge/` | The bridge, in Python, general to any board: `geometry.py` (KESE's parts), `layers.py` (the board's slabs and sections), `voxels.py` (the grid and the copper drawn onto it), `ports.py` (each coil's two terminals), `pypeec_case.py` (PyPEEC's input, running it, each coil's V, I, Z and M), `study.py` (one solve per frequency and the numbers back). Its [README](bridge/README.md) says what it does, how to call it and where it stops |
| `Examples/E01_circular_loop/`, `Examples/E02_coaxial_loops/` | The two proof boards (the Elmer branch's boards), each with its board, `make_board.py`, `simulation.py`, `README.md` and `results.md` |
| `Examples/Inductive Coils/` | Inductive encoder boards from the Sinusoidal Coil Generator, one folder each: S0 and the boards made from it (non-commercial licence, see its LICENSE.md) |
| `Examples/kicad_writer.py`, `Examples/references.py` | Shared by the proof boards, and not part of the bridge: a small KiCad 7 board writer for their `make_board.py`, and the textbook values they are checked against |
| `requirements.txt` | The Python packages the bridge asks for by name, PyPEEC among them, at the versions every simulation here ran with (every package of the environment is in `Solver_PyPEEC/requirements-lock.txt`); `bash bridge/setup_machine.sh` puts them in `.venv` |

## Boards tested

| Board | Checks | Result | Machine | Date |
|---|---|---|---|---|
| [E01_circular_loop](Examples/E01_circular_loop/results.md) | L and R of one loop at 10 kHz and 3.5 MHz, a voxel ladder (100 to 12.5 µm in the plane) | at 10 kHz, L 56.09 nH at 12.5 µm voxels, inside the band of 55.99 to 56.44 nH that Grover's ring formula gives the open loop, and settling towards its lower end (57.00, 56.59, 56.24, 56.09 nH at 100, 50, 25, 12.5 µm); R 1.8 % over the annular sector, its excess halving with each halving of the voxels, which puts the limit 0.3 % over it, as the round ends add; L and R from the coil's voltage and from the stored energy and the losses agree to the last digit | 4 cores, 15 GB | 17 Nov 2026 |
| [E02_coaxial_loops](Examples/E02_coaxial_loops/results.md) | M between two coaxial loops, the TX's L beside an open loop | at 10 kHz, M 24.09 nH at 50 µm voxels, 0.17 % under Maxwell's formula for the open loop (24.13 nH) and rising towards it as the voxels shrink; the open RX leaves the TX's L and R as E01's to 0.01 %; at 3.5 MHz its proximity loss shows in the TX's R (+0.8 %) | 4 cores, 15 GB | 17 Nov 2026 |
| [Inductive Coils](Examples/Inductive%20Coils/) | SIN and COS against the rotor's angle on six boards, at 0.1, 0.5, 1, 1.5 and 2 mm air gaps | all 286 solves readable (L and R worked out two ways agree within 0.001 %); SIN and COS within 0.4 % and 90° apart, 0.1° to 0.5° rms of angle error from 0.5 to 2 mm; against the Elmer branch the same curves and angle error, SIN 1.7 to 2.6 % higher where the coils are opened by a cut, L TX 8 to 14 % higher, where a hand calculation on S0 sides with PyPEEC; see [Comparisons](Examples/Inductive%20Coils/Comparisons/README.md) | 4 cores, 15 GB a machine | 17 Nov 2026 |

## Licence

GPL-3.0, as KESE. PyPEEC itself is MPL-2.0 and is installed from PyPI, not kept here; `bridge/tolerance.yaml` is a
copy of its default tolerances and keeps its licence (see its header). The coil boards in `Examples/Inductive Coils/`
keep the Sinusoidal Coil Generator's non-commercial licences (see that folder's LICENSE.md).
