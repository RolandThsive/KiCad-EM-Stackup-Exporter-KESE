# KESE Elmer Integration

This branch turns a KiCad board into an [Elmer](https://github.com/ElmerCSC/elmerfem) finite element
simulation and checks the answer against a reference.  KESE stays what it is, a 3D geometry exporter:
the bridge here runs it with `--for elmer`, meshes its STEP file with gmsh, writes Elmer's case and
reads back inductance, resistance, mutual inductance, capacitance, temperature and stress.

Every example lives in its own folder under `Examples/`, with its board, its `simulation.py` and a
`README.md` that says what the board is, what it is for, what Elmer checks on it, and, in its Results
section, what was expected and what came out.  The inductive encoder coils are in
`Examples/Inductive Coils/`.

## Layout

| Folder | What it holds |
|---|---|
| `3D_Geometry/` | Empty on purpose: copy KESE's `Generator/` in from `main` by hand (see its README) |
| `Solver_Elmer/` | Empty on purpose: build Elmer in here by hand (see its README) |
| `bridge/` | The bridge, in Python (coming) |
| `Examples/` | One folder per example (coming) |

## Licence

GPL-3.0, as KESE.  Elmer itself is GPL-2.0 or later (its library LGPL-2.1) and is not part of this
repository; it is built from its own source in `Solver_Elmer/`.
