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
| `bridge/` | The bridge, in Python, general to any board: `geometry.py` (KESE's parts), `mesh25d.py` (the 2.5D mesh), `ports.py` (each coil's electrodes and port sheet), `elmer_case.py` (the case and its circuits), `study.py` (running Elmer and reading it back). Its [README](bridge/README.md) says what it does, how to call it and where it stops |
| `Examples/E01_circular_loop/`, `Examples/E02_coaxial_loops/` | The two proof boards, each with its board, `make_board.py`, `simulation.py`, `README.md` and `results.md` |
| `Examples/Inductive Coils/` | Inductive encoder boards from the Sinusoidal Coil Generator, one folder each: S0 and the boards made from it (non-commercial licence, see its LICENSE.md) |
| `Examples/kicad_writer.py`, `Examples/references.py` | Shared by the proof boards, and not part of the bridge: a small KiCad 7 board writer for their `make_board.py`, and the textbook values they are checked against |
| `Examples/` | More examples, one folder each, to come |

## Boards tested

| Board | Checks | Result | Machine | Date |
|---|---|---|---|---|
| [E01_circular_loop](Examples/E01_circular_loop/results.md) | L and R of one loop at 10 kHz and 3.5 MHz, a three-level mesh ladder, the iteration check | L 3.1 % under Grover's ring formula at the finest mesh of the ladder, 0.46 % under it with the air graded four times as finely: the air's mesh held most of the gap; R +0.5 %; the circuit's L and the field energy's agree within 0.05 % | 4 cores, 15 GB; 7.1 GB at the finest mesh | 15 to 16 Nov 2026 |
| [E02_coaxial_loops](Examples/E02_coaxial_loops/results.md) | M between two coaxial loops, the TX's L beside an open loop | M 3.1 % under Maxwell's formula at level 1 and rising with the mesh, 1.1 % under it with the air graded twice as finely; the open RX leaves the TX's L alone; the RX's proximity loss shows in the TX's R at 3.5 MHz | 4 cores, 15 GB; 6.7 GB | 15 to 16 Nov 2026 |

## Left to test on a more powerful PC

The ten larger coil boards from the generator (S1 to S5 and D1 to D5) were taken out of the branch on
16 November and will be added back later. Before that, S2, the smallest, was meshed: 979,420 nodes at
level 1. The proof boards measured about 59 kB per node with the iterative solver, so S2 needs about
59 GB, four times the test machine's 15 GB, and the others scale with each stator's length of copper,
about 61 GB per metre.

A coarser mesh or a direct solver on a machine with more memory changes these numbers; the wiki's
*Elmer FEM Hardware* page has the details.

## Left to do

* **A ladder that refines the air as well.** A level divides only the copper's sizes. E01's
  diagnostic runs found that the air's grading round the copper holds most of the gap to the
  reference (3.7 % with the examples' grading, 0.46 % with it four times as fine), so a level should
  also divide `grade` and `tet_grade`; the coil boards' memory then needs measuring again.

## Licence

GPL-3.0, as KESE.  Elmer itself is GPL-2.0 or later (its library LGPL-2.1) and is not part of this
repository; it is built from its own source in `Solver_Elmer/`. The coil boards in `Examples/Inductive Coils/`
keep the Sinusoidal Coil Generator's non-commercial licences (see that folder's LICENSE.md).
