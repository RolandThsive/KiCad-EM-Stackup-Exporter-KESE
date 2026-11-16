# 24. Elmer FEM Introduction

[Elmer](https://github.com/ElmerCSC/elmerfem) is an open-source finite element solver from CSC in
Finland. The **Elmer bridge** turns a KiCad board into an Elmer simulation: KESE exports the board's
3D geometry, the bridge meshes it, writes Elmer's case, runs ElmerSolver and reads the answer back.
The bridge lives on the `Elmer_Integration` branch of the repository; KESE itself stays what it is,
a geometry exporter, and is never changed by the bridge.

> [!NOTE]
> This category describes work in progress. Two proof boards have run (see
> [Elmer FEM Test Board Results](Elmer-FEM-Test-Board-Results.md)); the ten inductive encoder
> boards are built, and the smallest meshed, but they need more memory than the test machine has, and are marked
> **YET TO BE RUN** on [Elmer FEM Test Boards](Elmer-FEM-Test-Boards.md).

## 24.1 What Elmer Is Used For Here

At the frequencies of inductive position sensors and planar coils (kHz to a few MHz) a board is a
tiny fraction of a wavelength across: a 40 mm coil at 3.5 MHz is about 1/2000 of a wavelength. The
physics is then **magneto-quasi-static**: currents and magnetic fields, eddy currents in nearby
copper, and no wave propagation. Elmer's time-harmonic A-V solver with edge elements
(`WhitneyAVHarmonicSolver`) solves exactly this, so it is the main solver for:

| Quantity | How the bridge gets it |
|---|---|
| Inductance L of a coil | the imaginary part of the coil's impedance V / I, over ω |
| AC resistance R of a coil, with skin and proximity effect | the real part of V / I |
| DC resistance | from the potential that sets each coil's current direction |
| Mutual inductance M between two coils | the open-circuit voltage of the undriven coil over the driving current |
| The field energy, as a check on L | Elmer's field energy W gives L = 2W / I² |
| The effect of a conducting target (a rotor, a plate) | the same quantities with the conductor present and away |

What Elmer does **not** give here: the coils' capacitance and self-resonance. An eddy-current
solve has no displacement current, so those come from openEMS (see
[OpenEMS Implementation Introduction](OpenEMS-Implementation-Introduction.md)).

## 24.2 How It Fits Together

```mermaid
flowchart LR
    A[KiCad board<br>.kicad_pcb] -->|run_KESE.py --for elmer| B[STL per net<br>+ materials.json]
    B -->|bridge/mesh25d.py| C[2.5D mesh<br>wedges + tetrahedra]
    C -->|bridge/ports.py| D[coil electrodes<br>and port sheets]
    D -->|bridge/elmer_case.py| E[Elmer case<br>.sif + circuits]
    E -->|ElmerSolver| F[V and I of every coil]
    F -->|bridge/study.py| G[L, R, M<br>results.json]
```

Each step is described on [Elmer FEM Workflow](Elmer-FEM-Workflow.md).

## 24.3 The Pages Of This Category

| Page | What it covers |
|---|---|
| [Elmer FEM Installation](Elmer-FEM-Installation.md) | Building Elmer and setting up the bridge on Linux and Windows |
| [Elmer FEM Workflow](Elmer-FEM-Workflow.md) | Every step from the board file to the numbers |
| [Elmer FEM Simulating Your Own Board](Elmer-FEM-Simulating-Your-Own-Board.md) | Every setting of an example's `simulation.py`, and how to start a new one |
| [Elmer FEM Test Boards](Elmer-FEM-Test-Boards.md) | The boards, rendered by KESE, and which have run |
| [Elmer FEM Test Board Results](Elmer-FEM-Test-Board-Results.md) | What came out, against the references, with charts |
| [Elmer FEM Accuracy](Elmer-FEM-Accuracy.md) | Where the errors come from and how big they are |
| [Elmer FEM Hardware](Elmer-FEM-Hardware.md) | Memory and time, measured, and what a board needs |
| [Elmer FEM Troubleshooting](Elmer-FEM-Troubleshooting.md) | What went wrong while building the bridge, and the fixes |

The two solvers are compared on [Elmer vs openEMS](Elmer-vs-OpenEMS.md).

## 24.4 Where The Code Is

| Folder on `Elmer_Integration` | What it holds |
|---|---|
| `bridge/` | The bridge, in Python: `geometry.py`, `mesh25d.py`, `ports.py`, `elmer_case.py`, `study.py`, `kicad_writer.py` |
| `Examples/E01_circular_loop/`, `Examples/E02_coaxial_loops/` | The proof boards, each with its board, `make_board.py`, `simulation.py`, `README.md` and `results.md` |
| `Examples/Inductive Coils/` | The ten inductive encoder boards (non-commercial licence, see that folder's `LICENSE.md`) |
| `Solver_Elmer/` | Empty on purpose: Elmer is built here (see [Elmer FEM Installation](Elmer-FEM-Installation.md)) |
| `3D_Geometry/` | Empty on purpose: KESE's `Generator/` is copied here from `main`, or `KESE_PATH` points at it |

| Previous | Next |
|:---|---:|
| [openEMS Workflow](OpenEMS-Workflow.md) | [Elmer FEM Installation](Elmer-FEM-Installation.md) |
