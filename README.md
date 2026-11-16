# KESE Elmer Integration

This branch turns a KiCad board into an [Elmer](https://github.com/ElmerCSC/elmerfem) finite element
simulation and checks the answer against a reference.  KESE stays what it is, a 3D geometry exporter:
the bridge here runs it with `--for elmer`, builds a 2.5D mesh from its STL files with gmsh, writes
Elmer's case and reads back inductance, resistance and mutual inductance from Elmer's magneto-quasi-static
A-V solver. The same bridge is meant to take capacitance, temperature and stress later; it does not yet.

Every example lives in its own folder under `Examples/`, with its board, its `simulation.py` and a
`README.md` that says what the board is, what it is for, what Elmer checks on it, and, in its Results
section, what was expected and what came out.  The inductive encoder coils are in
`Examples/Inductive Coils/`.

## Layout

| Folder | What it holds |
|---|---|
| `3D_Geometry/` | Empty on purpose: copy KESE's `Generator/` in from `main` by hand (see its README) |
| `Solver_Elmer/` | Empty on purpose: build Elmer in here by hand (see its README) |
| `bridge/` | The bridge, in Python: `geometry.py` (KESE's parts), `mesh25d.py` (the 2.5D mesh), `ports.py` (each coil's electrodes and port sheet), `elmer_case.py` (the case and its circuits), `study.py` (running Elmer and reading it back), `kicad_writer.py` (the example boards) |
| `Examples/E01_circular_loop/`, `Examples/E02_coaxial_loops/` | The two proof boards, each with its board, `make_board.py`, `simulation.py`, `README.md` and `results.md` |
| `Examples/Inductive Coils/` | The ten inductive encoder boards from the Sinusoidal Coil Generator, one folder each (non-commercial licence, see its LICENSE.md) |
| `Examples/` | More examples, one folder each, to come |

## Boards tested

| Board | Checks | Result | Machine | Date |
|---|---|---|---|---|
| [E01_circular_loop](Examples/E01_circular_loop/results.md) | L and R of one loop at 10 kHz and 3.5 MHz, a three-level mesh ladder, the iteration check | L 3.1 % under Grover's ring formula at the finest mesh and rising with the mesh; R +0.5 %; the circuit's L and the field energy's agree within 0.05 % | 4 cores, 15 GB; 7.1 GB at the finest mesh | 15 to 16 Nov 2026 |
| [E02_coaxial_loops](Examples/E02_coaxial_loops/results.md) | M between two coaxial loops, the TX's L beside an open loop | M_E02_SUMMARY | 4 cores, 15 GB; 6.7 GB | 15 to 16 Nov 2026 |

## Left to test on a more powerful PC

Every coil board. S2, the smallest, was meshed: 979,420 nodes at level 1. The proof boards measured
about 59 kB per node with the iterative solver, so S2 needs about 59 GB, four times the test
machine's 15 GB. The others scale S2 by each stator's length of copper, about 61 GB per metre.

| Board | Stator copper | Solves | Memory | Needs |
|---|---|---|---|---|
| S2_4x_OD40_2L_small | 0.96 m | 9 | about 59 GB (measured mesh) | 64 GB |
| S1_1x_OD54_2L_baseline | 0.92 m | 9 | about 55 GB | 64 GB |
| D2_1x8x_OD40_small | 1.56 m | 18 | about 95 GB | 128 GB |
| S3_8x_OD59_4L_series_wideband | 1.91 m | 9 | about 115 GB | 128 GB |
| S4_16x_OD54_2L_fingers | 1.30 m | 9 | about 80 GB | 128 GB |
| S5_4x_OD98_cosine_r_2subcoils_spiralTX | 3.41 m | 9 | about 210 GB | 256 GB |
| D1_1x16x_OD54_Renesas_R145_size | 3.14 m | 18 | about 190 GB | 256 GB |
| D3_1x16x_OD59_fitted_bands | 3.07 m | 18 | about 190 GB | 256 GB |
| D4_2x8x_OD59_parallel_TX | 2.74 m | 18 | about 170 GB | 256 GB |
| D5_1x16x_OD74_ID40_large | 3.96 m | 18 | about 240 GB | 256 GB |

A coarser mesh or a direct solver on a machine with more memory changes these numbers; the wiki's
*Elmer FEM Hardware* page has the details.

## Licence

GPL-3.0, as KESE.  Elmer itself is GPL-2.0 or later (its library LGPL-2.1) and is not part of this
repository; it is built from its own source in `Solver_Elmer/`. The coil boards in `Examples/Inductive Coils/`
keep the Sinusoidal Coil Generator's non-commercial licences (see that folder's LICENSE.md).
