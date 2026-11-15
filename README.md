# KESE openEMS Integration

This branch turns a KiCad board into an [openEMS](https://github.com/thliebig/openEMS-Project) FDTD
simulation and checks the answer against a reference.  KESE stays what it is, a 3D geometry exporter:
the bridge here runs it with `--for openems`, reads its STL files and `materials.json`, places the
mesh, ports and boundaries, and reads back S-parameters, impedance, TDR, crosstalk and resonances.

Every example lives in its own folder under `Examples/`, with its board, its `simulation.py` and a
`README.md` that says what the board is, what it is for, what openEMS checks on it, and, in its
Results section, what was expected and what came out.  The inductive encoder coils are in
`Examples/Inductive Coils/`.

## Layout

| Folder | What it holds |
|---|---|
| `3D_Geometry/` | Empty on purpose: copy KESE's `Generator/` in from `main` by hand (see its README) |
| `Solver_OpenEMS/` | Empty on purpose: build openEMS in here by hand (see its README) |
| `bridge/` | The bridge, in Python (coming) |
| `Examples/` | One folder per example (coming) |

## Licence

GPL-3.0, as KESE and openEMS.  openEMS is not part of this repository; it is built from its own
source in `Solver_OpenEMS/`.
