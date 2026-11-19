# 23.2 PyPEEC Troubleshooting

What went wrong while the bridge was built, what it looked like, and what fixed it. The bridge already
does what the right-hand column says; this page is for reading a failed run of your own, or a case
changed by hand.

## 23.2.1 Terminals And Ports

| Symptom | Cause | Fix |
|---|---|---|
| A terminal's voxels split into many groups | The terminals were taken as the voxels inside the gap's outline | The terminals are the coil's voxels that share a face with the gap, grouped with their edge and corner neighbours, which gives exactly two, one on each side |
| `X borders its gap in 1 places, not 2: the gap does not open it into one conductor` (or 3, ...) | The gap region misses the coil's copper, or crosses it twice | Draw the gap (`gap_box`, a cut's box, the disc round stacked ends) so that it holds the gap and touches each of the two ends once; check its position in model coordinates (y = −y_KiCad) and the height range given to `terminals()` |
| A via port loads the TX: L TX falls by up to 2 % at a small air gap and turns with the rotor, and M is about 3 % low | A terminal as wide as the left-out via's pad ring (73 voxels at 50 µm) is held at one potential, which lets current circle through the ring and the terminal, this close to the TX | Each pad is filled over its drill hole and its terminal is the one voxel on the via's axis; L TX is then the open receivers' to 0.001 nH. Results solved with the old terminals do not merge with new ones. Cut ports, as on S0d2, never had this |
| `electric components should include at least one source` from PyPEEC, on a rotor of several sectors | PyPEEC needs a source on every separate piece of copper, and only one piece of the rotor had its 0 V voxel | Each face-connected piece of a body with no terminals gets its own 0 V voxel; a body in one piece keeps the same voxel as before |

## 23.2.2 PyPEEC's Input And Output

| Symptom | Cause | Fix |
|---|---|---|
| PyPEEC's integrity check fails on groups of unequal size | Its rule that no two conductors touch pairs the domains of the groups it is given one to one | The bridge gives it one domain per conductor: the coil's first terminal, or a rotor's grounded voxel |
| The answer is not found in PyPEEC's solution file | The file wraps its answer in a `data` block beside `meta` | The bridge reads `data` |
| `PyPEEC failed (N) on NAME: ...` | PyPEEC's mesher or solver stopped; the message carries the last three error lines | The full log is `<name>.log` in the run's folder under `case/` |
| A solve is not read on the coil board's charts (drawn as a ring) | The TX's L or R from its voltage is more than 1 % from the L from the energy or the R from the losses, or PyPEEC's own check of the solver or of the matrices' condition did not pass | Its L and R checks are in the gap's table in `SINCOS_Results.md`; none of S0d2's 81 solves failed them |

## 23.2.3 The Voxels

| Symptom | Cause | Fix |
|---|---|---|
| The grid's z step takes extreme values (45 µm at small gaps, 28 µm at 2 mm) | It looked only for the least misfit of the copper sheets | It now takes the step nearest the copper's 35 µm among those that put every sheet within a micron of a voxel layer |
| `no dz keeps the copper sheets apart; give a smaller thickness or n_cu` | No step puts every sheet on its own voxel layers | Give `n_cu` or the copper's thickness again; check the board's stack in `materials.json` |
| `two conductors claim the same voxel: their copper is closer than a voxel (use a smaller d)` | Two nets lie closer than one voxel in the plane | Use a smaller voxel size |
| `no copper sheet in the layout` | The parts hold no trace copper | Check the export (`materials.json`) and the nets the example names |
| R several percent high | A trace's edges are drawn as steps, and R follows the width directly | Expected: R's error halves with each halving of the voxels ([PyPEEC Accuracy](PyPEEC-Accuracy.md#2221-the-error-budget-on-e01)) |

## 23.2.4 Installation, KESE And Python

| Symptom | Cause | Fix |
|---|---|---|
| `these wheels are for Python 3.13` or `these wheels are for 64-bit Linux` from `install.sh` | The committed wheels fit only 64-bit Linux with Python 3.13 | `PYTHON=/path/to/python3.13 bash Solver_PyPEEC/install.sh`, or install the same versions from PyPI with `Solver_PyPEEC/requirements-lock.txt` ([PyPEEC Walkthrough](PyPEEC-Walkthrough.md#1926-installing-on-windows-and-macos)) |
| `sha256sum` reports a wheel as failed | A wheel, or one of the two parts of VTK or Qt WebEngine, is incomplete | Fetch the branch again; `install.sh` joins the `.part0` and `.part1` files itself |
| `KESE not found: copy main's Generator into 3D_Geometry (see its README) or set KESE_PATH to run_KESE.py` | A board whose export is not committed (E01, E02) needs KESE, and neither `3D_Geometry/run_KESE.py` nor `KESE_PATH` points at it | Copy KESE in ([PyPEEC Walkthrough](PyPEEC-Walkthrough.md#1925-installing-on-linux-ubuntu-2404)) or set `KESE_PATH`; the coil board runs without KESE |
| `KESE failed on BOARD: ...` or `KESE wrote no materials.json` | KESE stopped on the board, often for a missing package of its own | KESE runs in the bridge's Python: install `Generator/requirements.txt` into the same environment |
| An angle is skipped: `already in results_gap1mm.json, skipped` | The coil board's sweep keeps what it has solved, so a stopped sweep picks up where it was | Expected. For a run that must not touch the committed results, use `--trial NAME` or another `--voxel`; those results stay in `case/` |
| The machine runs out of memory | The grid is too large for the machine | See [PyPEEC Simulating Your Own Board](PyPEEC-Simulating-Your-Own-Board.md#2026-before-a-large-board) for the memory per million voxels, and check a grid's size with `--voxels-only` first |

| Previous | Next |
|:---|---:|
| [Elmer FEM Troubleshooting](Elmer-FEM-Troubleshooting.md) | [FastHenry Troubleshooting](FastHenry-Troubleshooting.md) |
