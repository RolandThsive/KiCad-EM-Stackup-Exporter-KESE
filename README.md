# KESE FastHenry Integration

This branch turns a KiCad board into a [FastHenry](Solver_FastHenry/README.md) simulation and checks the answer
against a reference. KESE stays what it is, a 3D geometry exporter: the bridge here runs it with its solver preset
(`--for elmer`: one STL per solid and a `materials.json`) for the board's stack-up, the heights and thicknesses of its
copper layers, and reads the copper itself from the `.kicad_pcb`: every track a FastHenry segment along its centre
line, every via a vertical bar, every copper polygon a grid of bars. It writes FastHenry's input and reads back
inductance, resistance and mutual inductance from its magneto-quasi-static solve. FastHenry (M.I.T., in
FastFieldSolvers' release 3.0.1) cuts the conductors into filaments that each carry a uniform current; every filament
couples to every other through its partial inductance, so only the copper is discretised and the air needs no mesh
and no boundary.

Every example lives in its own folder under `Examples/`, with its board, its `simulation.py` and a `README.md` that
says what the board is, what it is for, what FastHenry checks on it, and, in its Results section, what was expected
and what came out. The inductive encoder coils are in `Examples/Inductive Coils/`, one folder per board.

## Layout

| Folder | What it holds |
|---|---|
| `3D_Geometry/` | Empty on purpose: copy KESE's `Generator/` in from `main` by hand (see its README), only to export a board whose `3D_Geometry/` is not committed |
| `Solver_FastHenry/` | The FastHenry build every simulation here ran with: FastHenry 3.0.1 built for 64-bit Linux (`install/bin/fasthenry`, needing only the C library), the script that builds the very same file from its source, what it runs on, and its licence (see its README) |
| `bridge/` | The bridge, in Python, general to any board: `kicad.py` (the board's nets, tracks, arcs, vias and copper polygons), `stackup.py` (KESE's export and the copper layers' heights), `fasthenry_case.py` (the filaments, the ports, FastHenry's input, running it, reading `Zc.mat`, each coil's Z, R, L and M), and `setup_machine.sh`. Its [README](bridge/README.md) says what it does, how to call it and where it stops |
| `Examples/E01_circular_loop/`, `Examples/E02_coaxial_loops/` | The two proof boards, each with its board, `make_board.py`, `simulation.py`, `README.md` and `results.md` |
| `Examples/Inductive Coils/` | Inductive encoder boards from the Sinusoidal Coil Generator, one folder each: S0 and the boards made from it (non-commercial licence, see its LICENSE.md) |
| `Examples/kicad_writer.py`, `Examples/references.py` | Shared by the proof boards, and not part of the bridge: a small KiCad 7 board writer for their `make_board.py`, and the textbook values they are checked against (Grover's ring formula, Neumann's double integral for arcs) |
| `requirements.txt` | The Python packages the bridge and the examples ask for, at the versions every simulation here ran with; `bash bridge/setup_machine.sh` puts them in `.venv` and builds FastHenry if the committed one does not run |

## Boards tested

| Board | Checks | Result | Machine | Date |
|---|---|---|---|---|
| [E01_circular_loop](Examples/E01_circular_loop/results.md) | L and R of one loop at 10 kHz and 3.5 MHz, a filament ladder (1 × 1 to 15 × 3 across and through the trace) | at 10 kHz, L 55.58 nH, 0.02 % under Neumann's integral over the open arc (55.59 nH), settling from below (55.34, 55.47, 55.52, 55.54, 55.58 nH as the filaments get finer); R 61.208 mΩ, the model's own chords' resistance, 0.011 % over the annular sector; at 3.5 MHz R rises to 1.23 times its DC value as the current crowds to the edges | 4 cores, 15 GB | 17 Nov 2026 |
| [E02_coaxial_loops](Examples/E02_coaxial_loops/results.md) | M between two coaxial loops, the TX's L beside an open loop, reciprocity | at 10 kHz, M 23.892 nH, 0.02 % over Neumann's integral for the two open arcs averaged over the traces' widths (23.886 nH), the same from 1 × 1 to 9 × 3 filaments; M from the RX back to the TX the same to the last digit; the open RX leaves the TX's L and R as E01's | 4 cores, 15 GB | 17 Nov 2026 |
| [Inductive Coils](Examples/Inductive%20Coils/) | SIN and COS against the rotor's angle on six boards, at 0.1, 0.5, 1, 1.5 and 2 mm air gaps | SIN's amplitude from 1.02 nH (2 mm) to 9.76 nH (0.1 mm) over the six boards; SIN and COS within 0.3 % of each other; the angle error 0.1° to 0.7° rms from 0.5 to 2 mm and up to 1.5° at 0.1 mm; S0's L TX with the rotor away 135.3 nH, 2.1 % over a hand calculation; 286 solves, every one reciprocal to the last digit | 4 cores, 15 GB | 17 to 18 Nov 2026 |

## Licence

GPL-3.0, as KESE. FastHenry keeps its own licence, M.I.T.'s re-release of 2003, which lets anyone use, copy,
modify and distribute it (see [`Solver_FastHenry/LICENSE.md`](Solver_FastHenry/LICENSE.md)). The coil boards in
`Examples/Inductive Coils/` keep the Sinusoidal Coil Generator's non-commercial licences (see that folder's
LICENSE.md).
