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
| `Examples/Inductive Coils/` | The ten inductive encoder boards from the Sinusoidal Coil Generator, one folder each (non-commercial licence, see its LICENSE.md) |
| `Examples/` | The 50 examples, one folder each (coming) |

## Boards tested

None yet. Each board that runs gets a `results.md` in its folder, and a line here.

| Board | Checks | Result | Machine | Date |
|---|---|---|---|---|

## Left to test on a more powerful PC

A first guess from each board's length of copper, corrected once S2's mesh study has measured the real memory per
metre. The test machine has 4 cores and 16 GB, about 12 GB of it free for a solver.

| Board | Memory, first guess | Needs |
|---|---|---|
| D2_1x8x_OD40_small | about 17 GB | 32 GB |
| S3_8x_OD59_4L_series_wideband | about 20 GB | 32 GB |
| D4_2x8x_OD59_parallel_TX | about 28 GB | 32 GB |
| S5_4x_OD98_cosine_r_2subcoils_spiralTX | about 35 GB | 64 GB |
| D1_1x16x_OD54_Renesas_R145_size | about 32 GB | 64 GB |
| D3_1x16x_OD59_fitted_bands | about 32 GB | 64 GB |
| D5_1x16x_OD74_ID40_large | about 41 GB | 64 GB |

## Licence

GPL-3.0, as KESE.  Elmer itself is GPL-2.0 or later (its library LGPL-2.1) and is not part of this
repository; it is built from its own source in `Solver_Elmer/`. The coil boards in `Examples/Inductive Coils/`
keep the Sinusoidal Coil Generator's non-commercial licences (see that folder's LICENSE.md).
