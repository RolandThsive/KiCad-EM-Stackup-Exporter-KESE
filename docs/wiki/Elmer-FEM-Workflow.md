# 26. Elmer FEM Workflow

What happens between `python simulation.py` and the numbers in the results files, step by step. Every
step is one function of the bridge on the `Elmer_Integration` branch; the file is named with each.

## 26.1 Export The Board With KESE

`bridge/geometry.py` runs KESE as a program, never as a library:

```bash
python run_KESE.py board.kicad_pcb --for elmer --format step stl --out <folder> \
    --set Stackup.solder_mask=True ...
```

The `elmer` preset writes simulation-mode solids, one per net and one per dielectric, in mm on
KiCad's origin, with no surface finish ([Choosing An Export](Choosing-An-Export.md)). The bridge
asks for STL beside STEP and reads the STL files with `trimesh`, together with `materials.json`
for each part's role, net, layer and height. By default it asks for a 20 µm solder mask over copper
and laminate with tented vias, as the coil boards' brief does.

`bridge/study.py` keeps the export in one of two places. `kese_export` keeps it in a scratch cache
named by a hash of the board file (E01 and E02). `kese_geometry` keeps it in a folder meant to be
committed beside the board, with a `source.json` holding that hash (the coil board's `3D_Geometry/`).
Either way an unchanged board is not exported twice.

KESE writes the board with y up (y_model = −y_KiCad) and z = 0 in the middle of the board. The
bridge shifts z so that the top face of the F.Cu copper is z = 0.

## 26.2 Section The Parts Into Slabs

`bridge/mesh25d.py` builds a **2.5D mesh**, the shape a printed board has: everything is flat in z.
`Layout.build` takes every height at which some part starts or ends, which splits the board into
**slabs**, and cuts each part at the middle of each slab it spans, giving one 2D outline per part
and slab.

For the magneto-quasi-static solve an insulator with μr = 1 is air: the A-V solver has no
displacement current, so εr plays no part. `insulators=False` therefore leaves out FR-4 and mask
altogether, which removes their heights from the slabs; with `insulators=True` they are kept, and a
board or mask part that lies wholly outside the copper's heights is merged into the air anyway.
All three boards of this category run with `insulators=False`.

## 26.3 Triangulate The Footprint

One triangle mesh covers the whole footprint: a disc around the board (its rim sized to the far
field's element size), with every copper edge of every slab drawn into it as a line, so each
triangle lies wholly inside or outside the copper in every slab. The element size comes from a
raster: `h_edge` at copper edges, growing by `grade` per mm away from them, at most `h_in` inside
copper and `h_max` far away. Lines given in `extra_lines` (port sheets, the outline of a cut, a
rotor's copper at its angle) are drawn in too.

## 26.4 Stack The Wedges, Fill The Air

The triangle mesh is repeated at a series of heights in z and joined into wedges (prisms):

| Slab | Layer height |
|---|---|
| A copper foil (a slab with copper, at most `foil_max` = 0.15 mm thick) | at most `dz_copper` (E01 and E02 use 0.018 mm at level 1, about half copper's skin depth at 3.5 MHz) |
| Any other slab, including a dielectric that holds only via barrels, and the air gap to a rotor | at most `dz_max` |
| Above and below the boards | two thin air layers (`pads`), then tetrahedra |

Above and below the wedges, gmsh fills the air with tetrahedra out to the top and bottom of the
domain, growing from the wedges' size by `tet_grade` per mm up to `tet_max`, then optimises them
with Netgen. Each wedge gets the body of the part of highest priority whose outline holds its
triangle (copper over mask over board); a `void` part (air of higher priority than copper) takes
copper out, which is how a cut across a trace or a left-out via is made in the model while the
board file stays as it is.

## 26.5 Open Each Coil At Its Port

Elmer's 3D massive coils take their current's direction from a potential (`W`) that runs from 0 at
one electrode to 1 at the other, so a coil must be **open**. `bridge/ports.py` opens it where the
real board gets its leads:

| Port part | What it is | Boundary condition |
|---|---|---|
| Electrodes T1 and T2 | the coil's copper faces that border the gap (two separate groups) | W = 0 (T1), W = 1 (T2), and the scalar potential fixed (A re = A im = 0) |
| Sheet | faces inside the gap that join the two electrodes | n × A = 0 (`A re {e} = 0`, `A im {e} = 0`) |

The gap is wherever the coil's copper is absent:

| Coil | Opened at | Sheet |
|---|---|---|
| E01's loop, E02's TX and RX | the 0.2 mm gap between the trace's two round ends | across the gap at a level of the copper (`sheet_at_level`) |
| The coil board's TX | its two ends, stacked on F.Cu and B.Cu at one point | upright through the board between them (`sheet_vertical`, along a line drawn into the mesh) |
| The coil board's SIN and COS | a 0.2 mm cut across a top trace, 0.4 mm across, made in the model | across the cut's floor, at the copper's lower face, as on E01 |

With the sheet in place, the coil's voltage is IR + jω∮A·dl round the whole loop, gap included: the
coil's EMF, as a meter at its leads would read it.

![How the coil board sits in Elmer, drawn from the geometry the mesh is built from. Left, seen from above: the stator's TX in dark grey (three turns on F.Cu), SIN in blue and COS in orange, each on F.Cu and B.Cu, with the rotor's two quarter-ring copper sectors in grey at 0 degrees, 1 mm above and copper face down; SIN's and COS's ports are ringed where a 0.2 mm cut crosses a top trace, and the TX port at its two stacked ends at KiCad (111, 100). Top right, a section through the stack with heights stretched: the rotor copper 1 mm above the stator, FR-4 and mask treated as air, and air out to 35.1 mm from the axis and 35.1 mm above and below. Bottom right: the SIN port, the cut's two faces as electrodes and a dashed port sheet across the gap's floor, with 0 A forced through SIN so the voltage across the cut is its open-circuit EMF; and the TX port, an electrode on each stacked end and a hatched port sheet between them, where 1 A is driven at 3.5 MHz](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Workflow/S0d2_1x_OD23_2L_tiny_TX3top_Cut/elmerworkflow_1_setup.webp)

The coil board's three ports, drawn by its `rig_picture.py`.

## 26.6 Write The Elmer Case

`bridge/elmer_case.py` writes one `.sif` per frequency:

| Solver | What it does |
|---|---|
| 1 `WPotentialSolver` | W in each coil, once, before everything, with a direct solve (UMFPACK) |
| 2 `CircuitsAndDynamicsHarmonic` | one circuit per coil: a current source of 1 A for the driven coil and 0 A for a sensing coil |
| 3 `WhitneyAVHarmonicSolver` | A (edge elements) and V in the conductors, complex, with the circuits; iterative or direct, below |
| 4 `MagnetoDynamicsCalcFields` | current density, field energy and eddy power |
| 5 `CircuitsOutput` | every circuit's V and I |
| 6 `SaveScalars` | the scalars to `res_<name>/scalars_<name>.dat` |

The A-V solve has two modes (`Case.solver`):

| Mode | What Elmer is told | Used by |
|---|---|---|
| `iterative` (the default) | BiCGStab(l) of degree 4 or GCR, with Elmer's `Circuit` preconditioner, optionally with an ILU of the field's block (`ilu_order`, shifted by `ilu_factor`); the run goes on at the iteration cap (`Linear System Abort Not Converged = False`) | E01 and E02 (BiCGStab(l), no ILU) |
| `mumps` | a direct solve with serial MUMPS (`mumpslocal`), `Use Tree Gauge = False` and `Mumps Solve Singular = True`, so A stays ungauged and MUMPS handles the null pivots of the gradients | the coil board |

Every coil is a massive component (`Coil Type = Massive`). Conductors that are not coils (a rotor)
are ordinary conducting bodies, with their own scalar potential fixed to 0 by default
(`conductor_potential=False`), so there E = −jωA. The outer boundary has n × A = 0. Coordinates stay
in mm (`Coordinate Scaling = 0.001`).

> [!NOTE]
> `Activate Constraint` on the massive coils is off by default today (`constraint=False`), and the
> eddy power is then a second check on R. E01 and E02 ran on 15 and 16 November with it on, the
> bridge's setting then; the coil board ran on 17 November with it off.

## 26.7 Solve And Read Back

`bridge/study.py` runs ElmerSolver once per frequency (OpenMP threads set by `threads`, the stack
limit lifted for serial MUMPS), reads the scalars and, for an iterative solve, the last iteration
count and residual from its log, and records Elmer's peak memory. Per coil it reports:

| Result | From |
|---|---|
| V, I, Z = V / I | the circuit outputs |
| R = Re Z, L = Im Z / ω | Z |
| M, the mutual inductance to the driven coil | Im(V_sense / I_drive) / ω, for a coil with no current |
| R_dc | Elmer's `r_component`, from ∫σ\|∇W\|² |
| L from the field energy | 2W / I², a check on L that does not go through the circuit |
| R from the eddy power | 2P / I², a check on R (right only with `Activate Constraint` off) |

All of it, with the mesh's size, the run's time, memory and the software versions, is written to the
example's results files; each example's results page sets it against the reference.

## 26.8 A Rotor Over A Stator

The coil board adds a second board. `load_parts` turns the rotor copper side down without mirroring
it, lifts its copper face to the air gap above z = 0, and turns it about the axis (KiCad's point
(100, 100)) by the rotor angle. Every angle gets its own mesh, with the rotor's copper at that angle
drawn into it, and one solve; a run with the rotor's copper made air gives the TX with the rotor
away. The receivers' M at each angle is fitted with a sine, and the angle read back as
atan2(SIN, COS) gives the angle error ([Elmer FEM Test Board Results](Elmer-FEM-Test-Board-Results.md#293-s0d2_1x_od23_2l_tiny_tx3top_cut)).

| Previous | Next |
|:---|---:|
| [Elmer FEM Installation](Elmer-FEM-Installation.md) | [Elmer FEM Simulating Your Own Board](Elmer-FEM-Simulating-Your-Own-Board.md) |
