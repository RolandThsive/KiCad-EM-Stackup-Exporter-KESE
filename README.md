# KESE openEMS Integration

This branch turns a KiCad board into an [openEMS](https://github.com/thliebig/openEMS-Project) FDTD
simulation and checks the answer against a reference.  KESE stays what it is, a 3D geometry exporter:
the bridge here runs it with `--for openems`, reads its STL files and `materials.json`, places the
mesh, ports and boundaries, checks the grid and the ports before it runs, and reads back S-parameters,
line impedance and effective permittivity (TDR, crosstalk and resonances are planned).

Every example lives in its own folder under `Examples/`, with its board, its `simulation.py` and a
`README.md` that says what the board is, what it is for, what openEMS checks on it, and, in its
Results section, what was expected and what came out.  The inductive encoder coils are in
`Examples/Inductive Coils/`.

## Layout

| Folder | What it holds |
|---|---|
| `3D_Geometry/` | Empty on purpose: copy KESE's `Generator/` in from `main` by hand (see its README) |
| `Solver_OpenEMS/` | Empty on purpose: build openEMS in here by hand (see its README) |
| `bridge/` | The bridge, in Python: `fdtd.py` (KESE export, parts, mesh, preflight, model, run, results) and `kicad_writer.py` (for the examples' `make_board.py`) |
| `Examples/Inductive Coils/` | The ten inductive encoder boards from the Sinusoidal Coil Generator, one folder each (non-commercial licence, see its LICENSE.md) |
| `Examples/O01_microstrip/` | The first proof board: a 50 Ω microstrip against Hammerstad–Jensen and Kirschning–Jansen |
| `Examples/` | The 50 examples, one folder each (the rest are coming) |

## Boards tested

Each board that runs gets a `results.md` in its folder, and a line here.

| Board | Checks | Result | Machine | Date |
|---|---|---|---|---|
| [O01_microstrip](Examples/O01_microstrip/results.md) | Z0, εeff (two ways), S21 loss, S11, mesh study, engines | Z0 +1.8 %, εeff +0.7 to +1.5 % against the closed-form references; mesh converged to 0.02 %; CPU and default engines agree to four digits | 4 cores, 15 GB, 79 s, 0.15 GB | 16 Nov 2026 |

## How to run

```bash
export KESE_PATH=<your KESE>/Generator          # or copy KESE's Generator into 3D_Geometry/
cd Examples/O01_microstrip
../../Solver_OpenEMS/install/venv/bin/python simulation.py
```

The `requirements.txt` beside this README lists the Python packages the bridge needs beside openEMS's
own modules.

## Left to test on a more powerful PC

Every coil board's self-resonance check (C8) is a run of many hours (about 540,000 time steps): 7 hours for S2 and 45
for S5 on the 4-core test machine. These wait for a machine that can run them unattended. Memory, with openEMS's new CPU engine:

| Board | Memory | Fits |
|---|---|---|
| S2, D2 | about 2 GB | 8 GB |
| S1, S4, D1, D3, D4, S3 | 3.8 to 4.5 GB | 8 GB, just |
| D5_1x16x_OD74_ID40_large | about 7 GB | 16 GB |
| S5_4x_OD98_cosine_r_2subcoils_spiralTX | about 13 GB | 32 GB |

## Licence

GPL-3.0, as KESE and openEMS.  openEMS is not part of this repository; it is built from its own
source in `Solver_OpenEMS/`. The coil boards in `Examples/Inductive Coils/` keep the Sinusoidal Coil
Generator's non-commercial licences (see that folder's LICENSE.md).
