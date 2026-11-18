# KESE Palace Integration

This branch turns a KiCad board into a [Palace](Solver_Palace/README.md) simulation and checks the answer against a
reference. KESE stays what it is, a 3D geometry exporter: the bridge here runs it with its solver preset (`--for
elmer`: one STL per solid and a `materials.json`), builds a 2.5D mesh from its solids with gmsh, writes Palace's
input and reads back inductance, resistance and mutual inductance from Palace's frequency-domain solve. Palace (AWS
Labs, Apache 2.0) solves Maxwell's equations for the electric field with Nédélec edge elements: the copper is a
conducting region, the air round it is meshed out to a boundary, and each coil is opened by a lumped port, a sheet
across the place where it is opened, with a resistance across it.

Every example lives in its own folder under `Examples/`, with its board, its `simulation.py` and a `README.md` that
says what the board is, what it is for, what Palace checks on it, and, in its Results section, what was expected and
what came out. The inductive encoder coils are in `Examples/Inductive Coils/`, one folder per board.

## Layout

| Folder | What it holds |
|---|---|
| `3D_Geometry/` | Empty on purpose: copy KESE's `Generator/` in from `main` by hand (see its README), only to export a board whose `3D_Geometry/` is not committed |
| `Solver_Palace/` | The Palace build every simulation here ran with: Palace 0.19.0 for 64-bit Linux (`install/`), built without ParMETIS so that everything in it is open source, the script and patch that build the same program from source, and the licences of Palace and of everything built into it (see its README) |
| `bridge/` | The bridge, in Python, general to any board: `geometry.py` (KESE's parts), `mesh25d.py` (the 2.5D mesh, written for Palace in Gmsh's format), `ports.py` (where a coil is opened), `palace_case.py` (Palace's input, running it, reading back each coil's Z, R, L and M), `study.py` (KESE's export and the versions), and `setup_machine.sh`. Its [README](bridge/README.md) says what it does, how to call it and where it stops |
| `Examples/E01_circular_loop/`, `Examples/E02_coaxial_loops/` | The two proof boards, each with its board, `make_board.py`, `simulation.py`, `README.md` and `results.md` |
| `Examples/Inductive Coils/` | Inductive encoder boards from the Sinusoidal Coil Generator, one folder each: S0 and the boards made from it (non-commercial licence, see its LICENSE.md) |
| `Examples/kicad_writer.py`, `Examples/references.py` | Shared by the proof boards, and not part of the bridge: a small KiCad 7 board writer for their `make_board.py`, and the textbook values they are checked against (Grover's ring formula, Neumann's double integral for arcs) |
| `requirements.txt` | The Python packages the bridge and the examples ask for, at the versions every simulation here ran with; `bash bridge/setup_machine.sh` puts them in `.venv`, installs the system libraries Palace runs with, and builds Palace if the committed one does not run |

## Boards tested

| Board | Checks | Result | Machine | Date |
|---|---|---|---|---|
| [E01_circular_loop](Examples/E01_circular_loop/) | L and R of one loop at 10 kHz and 3.5 MHz, a mesh ladder | to be solved after the coil boards | 4 cores, 15 GB | |
| [E02_coaxial_loops](Examples/E02_coaxial_loops/) | M between two coaxial loops, the TX's L beside an open loop, reciprocity | to be solved after the coil boards | 4 cores, 15 GB | |
| [Inductive Coils](Examples/Inductive%20Coils/) | SIN and COS against the rotor's angle on six boards, at 0.1, 0.5, 1, 1.5 and 2 mm air gaps | S0, S0 with the TX on top, the 22 mm board, the 22 mm board opened by cuts, the 23 mm board and S0d2 solved at every gap, 286 solves: SIN's amplitude from 1.00 nH (2 mm) to 9.71 nH (0.1 mm), the angle error 0.1° to 0.7° rms from 0.5 to 2 mm and up to 1.5° at 0.1 mm, every solve converged, the TX's L from its port and from the field's energy within 0.0055 %, reciprocity within 0.00026 % | 4 cores, 15 GB | 17 to 18 Nov 2026 |

## Licence

GPL-3.0, as KESE. Palace keeps its own licence, Apache 2.0, and every library built into the committed program keeps
its own open-source licence (see [`Solver_Palace/README.md`](Solver_Palace/README.md)). The coil boards in
`Examples/Inductive Coils/` keep the Sinusoidal Coil Generator's non-commercial licences (see that folder's
LICENSE.md).
