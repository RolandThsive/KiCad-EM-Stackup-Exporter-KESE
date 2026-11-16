# 26. Elmer FEM Workflow

What happens between `python simulation.py` and the numbers in `results.json`, step by step. Every
step is one function of the bridge on the `Elmer_Integration` branch; the file is named with each.

## 26.1 Export The Board With KESE

`bridge/geometry.py` runs KESE as a program, never as a library:

```bash
python run_KESE.py board.kicad_pcb --for elmer --format step stl --out <case>/kese/<board>_<hash> \
    --set Stackup.solder_mask=True ...
```

The `elmer` preset writes simulation-mode solids, one per net and one per dielectric, in mm on
KiCad's origin, with no surface finish ([Choosing An Export](Choosing-An-Export.md)). The bridge
asks for STL beside STEP and reads the STL files with `trimesh`, together with `materials.json`
for each part's role, net, layer and height. `bridge/study.py` keeps each export under a hash of the
board file and reuses it while the board is unchanged.

KESE writes the board with y up (y_model = −y_KiCad) and z = 0 in the middle of the board. The
bridge shifts z so that the top face of the F.Cu copper is z = 0, the convention of the coil
boards' brief; a second board (a rotor) can be turned copper side down without mirroring it,
lifted by an air gap and turned about an axis (`load_parts`).

## 26.2 Section The Parts Into Slabs

`bridge/mesh25d.py` builds a **2.5D mesh**, the shape a printed board has: everything is flat in z.
`Layout.build` takes every height at which some part starts or ends, which splits the board into
**slabs**, and cuts each part at the middle of each slab it spans, giving one 2D outline per part
and slab.

For the magneto-quasi-static solve an insulator with μr = 1 is air: the A-V solver has no
displacement current, so εr plays no part. `insulators=False` therefore leaves out FR-4 and mask
altogether, which removes their heights from the slabs; with `insulators=True` they are kept, and a
board or mask part that lies wholly outside the copper's heights is merged into the air anyway.

## 26.3 Triangulate The Footprint

One triangle mesh covers the whole footprint: a disc around the board (its rim sized to the far
field's element size), with every copper edge of every slab drawn into it as a line, so each
triangle lies wholly inside or outside the copper in every slab. The element size comes from a
raster: `h_edge` at copper edges, growing by `grade` per mm away from them, at most `h_in` inside
copper and `h_max` far away. Lines given in `extra_lines` (port sheets, a rotor's outline at other
angles) are drawn in too.

## 26.4 Stack The Wedges, Fill The Air

The triangle mesh is repeated at a series of heights in z and joined into wedges (prisms):

| Slab | Layer height |
|---|---|
| A copper foil (a slab with copper, at most `foil_max` = 0.15 mm thick) | at most `dz_copper` (the examples use 0.018 mm, about half copper's skin depth at 3.5 MHz) |
| Any other slab, including a dielectric that holds only via barrels | at most `dz_max` |
| Above and below the boards | two thin air layers (`pads`), then tetrahedra |

Above and below the wedges, gmsh fills the air with tetrahedra out to the top and bottom of the
domain, growing from the wedges' size by `tet_grade` per mm up to `tet_max`, then optimises them
with Netgen. Each wedge gets the body of the part of highest priority whose outline holds its
triangle (copper over mask over board); a `void` part (air of higher priority than copper) leaves
a via out.

## 26.5 Open Each Coil At Its Port

Elmer's 3D massive coils take their current's direction from a potential (`W`) that runs from 0 at
one electrode to 1 at the other, so a coil must be **open**. `bridge/ports.py` opens it where the
real board gets its leads:

| Port part | What it is | Boundary condition |
|---|---|---|
| Electrodes T1 and T2 | the coil's copper faces that border the gap (two separate groups) | W = 0 (T1), W = 1 (T2), and the scalar potential fixed (A re = A im = 0) |
| Sheet | faces inside the gap that join the two electrodes | n × A = 0 (`A re {e} = 0`, `A im {e} = 0`) |

The gap is wherever the coil's copper is absent: the space between two trace ends, the board
between two stacked ends, or the barrel of a via that is left out. With the sheet in place, the
coil's voltage is IR + jω∮A·dl round the whole loop, gap included: the coil's EMF, as a meter at
its leads would read it.

## 26.6 Write The Elmer Case

`bridge/elmer_case.py` writes one `.sif` per frequency:

| Solver | What it does |
|---|---|
| 1 `WPotentialSolver` | W in each coil, once, before everything (CG with ILU0) |
| 2 `CircuitsAndDynamicsHarmonic` | one circuit per coil: a current source of 1 A for the driven coil and 0 A for a sensing coil |
| 3 `WhitneyAVHarmonicSolver` | A (edge elements) and V in the conductors, complex, with the circuits; BiCGStabL of degree 4 with Elmer's `Circuit` preconditioner (ILU0 inside), no tree gauge |
| 4 `MagnetoDynamicsCalcFields` | current density and field energy |
| 5 `CircuitsOutput` | every circuit's V and I |
| 6 `SaveScalars` | the scalars to `res_<name>/scalars_<name>.dat` |

Every coil is a massive component (`Coil Type = Massive`) with `Activate Constraint = True`.
Conductors that are not coils (a rotor) are ordinary conducting bodies. The outer boundary has
n × A = 0. Coordinates stay in mm (`Coordinate Scaling = 0.001`).

## 26.7 Solve And Read Back

`bridge/study.py` runs ElmerSolver once per frequency (OpenMP threads set by `threads`), reads the
scalars and the solver's last iteration count and residual from its log, and records Elmer's peak
memory. Per coil it reports:

| Result | From |
|---|---|
| V, I, Z = V / I | the circuit outputs |
| R = Re Z, L = Im Z / ω | Z |
| M, the mutual inductance to the driven coil | Im(V_sense / I_drive) / ω, for a coil with no current |
| R_dc | Elmer's `r_component`, from ∫σ\|∇W\|² |
| L from the field energy | 2W / I², a check on L that does not go through the circuit |

All of it, with the mesh's size, the run's time, memory, iterations and the software versions, is
written to the example's `results.json`; each example's `results.md` sets it against the reference.

| Previous | Next |
|:---|---:|
| [Elmer FEM Installation](Elmer-FEM-Installation.md) | [Elmer FEM Simulating Your Own Board](Elmer-FEM-Simulating-Your-Own-Board.md) |
