# 45. PyPEEC Workflow

What happens between `python simulation.py` and the numbers in the results files, step by step. Every
step is one module of the bridge on the `PyPEEC_Integration` branch; the file is named with each. The
bridge is general: nothing in it names a board, a coil or an example. Each example adds only what
belongs to its own board: which nets are coils, where each coil is opened, what to sweep, and what to
compare the answer with.

## 45.1 Export The Board With KESE

`bridge/geometry.py` runs KESE as a program, never as a library, with its solver preset (named
`elmer` in KESE): simulation-mode solids, one STL per solid, a `materials.json` with each part's role,
net, layer and height, plus a STEP and KESE's report. `bridge/study.py` keeps the export in one of two
places:

| Function | Where the export goes | Used by |
|---|---|---|
| `kese_geometry` | a folder of its own, meant to be committed beside the board, with a `source.json` holding the board file's hash | the coil board (`3D_Geometry/Stator/`, `3D_Geometry/Rotor/`) |
| `kese_export` | a scratch cache under `case/`, named by that hash | E01 and E02 |

Either way an unchanged board is not exported twice, and a board with a committed export runs with no
KESE at all.

## 45.2 Place The Parts

`geometry.load_parts` turns each solid into a part in model coordinates: x and y as KiCad's with y up
(KiCad's (x, y) becomes (x, −y)), and z = 0 at the top face of the top copper. A board can be flipped
copper side down, moved up by an air gap and turned about an axis: that is how the rotor is placed over
the stator. On the coil board the axis is KiCad's (100, 100), and the air gap is measured from the
stator's F.Cu top face to the rotor's copper face, copper to copper.

## 45.3 Section The Parts Into Slabs

`layers.Layout` cuts the model into slabs at every height any part starts or ends, and sections each
part in the middle of each slab. FR-4 and solder mask are left out (`insulators=False`): to a
magneto-quasi-static solve an insulator with μr 1 is air, so they would add heights and nothing else.

## 45.4 Draw The Copper As Voxels

`voxels.build` draws every conductor onto one uniform grid:

| Direction | Voxel size | How it is chosen |
|---|---|---|
| In the board's plane | d (50 µm on the coil board; 100 to 12.5 µm on E01's ladder) | given by the example. A voxel is copper when its centre lies in the part's section, so a trace's edges are drawn as steps |
| Through the board | dz, close to the copper's 35 µm | each copper sheet is one voxel layer thick (or `n_cu`), centred on its own height, and dz is chosen so that the distance between any two sheets is a whole number of voxels to within a micron or so |

Each sheet's resistivity is scaled by its voxels' thickness over the copper's, so it keeps its sheet
resistance: on E02, 45 steps of 34.8 µm put the two sheets within 1 µm of where they are, and the
resistivity is scaled by 0.994. A via's barrel is drawn as a solid column of its outer diameter. The
voxel layers between the sheets that hold no copper add no unknowns, only grid to the FFTs; there is
no air box and no outer boundary.

![How S0d2_1x_OD23_2L_tiny_TX3top_Cut sits in PyPEEC, drawn from the voxels it is solved with. Left, seen from above: the stator's TX (three grey turns), SIN (blue) and COS (orange) on F.Cu and B.Cu, with the rotor's two quarter-ring copper sectors in grey at 0°, 1 mm above and copper face down, on a grid of 405 × 364 × 52, 7.7 million voxels of 50 µm; the SIN and COS ports are circled where a 0.2 mm cut crosses each top trace, the TX port where its two ends stack at the right. Top right, a section through the axis: one voxel layer of 34.5 µm through each copper sheet, the stator's FR-4 and mask drawn as air with no voxels, the rotor copper 1 mm above. Bottom right: SIN's cut voxel by voxel, terminal 1 (green, where the current goes in) and terminal 2 (purple, held at 0 V) on the two faces of the grey gap; and the TX port between its two stacked ends, terminal 1 on B.Cu and terminal 2 on F.Cu](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Workflow/S0d2_1x_OD23_2L_tiny_TX3top_Cut/S0d2_1x_OD23_2L_tiny_TX3top_Cut_pypeec_setup.webp)

The coil board as PyPEEC solves it, drawn by its `rig_picture.py` from the very voxels
`simulation.py` builds.

## 45.5 Open Each Coil At Its Port

A coil needs two terminals, so it must be **open**. `bridge/ports.py` opens it where the real board
gets its leads, and the caller says where: the bridge never guesses.

| Coil opened at | How (`ports.cut`, `ports.terminals`) | Used on |
|---|---|---|
| A gap between two trace ends on one layer | the gap is in the board already | E01's loop, E02's two loops (a 0.2 mm gap) |
| A cut across a trace | the coil's voxels inside a box (0.2 mm along the trace, 0.4 mm across) are taken out of the top copper | SIN and COS of the coil board |
| Two trace ends stacked on two layers | the gap is the board between them, inside a small disc round the ends (0.1 mm radius) | the coil board's TX |
| A via left out | the barrel is taken out; each pad is filled over its drill hole and its terminal is the one voxel on the via's axis | not used on the boards of this category |

The two terminals are the coil's voxels that share a face with the gap, one group on each side,
grouped with their edge and corner neighbours so that there are exactly two.

## 45.6 Write PyPEEC's Case

`bridge/pypeec_case.py` writes PyPEEC's two inputs, the geometry (its voxel mesher, given the voxels'
indices directly) and the problem:

| Part | What it is |
|---|---|
| Each coil's copper | a domain of copper's resistivity (σ = 5.8 × 10⁷ S/m), scaled per sheet as above |
| A coil's first terminal | a current source: 1 A in the driven coil, 0 A in a receiver, whose voltage is then its open-circuit EMF |
| A coil's second terminal | a 0 V source |
| A conductor with no terminals (the rotor) | eddy currents only. PyPEEC needs a source on every piece of copper, so one voxel of each separate piece is held at 0 V; that is the piece's only connection, so no current flows in or out |
| PyPEEC's integrity checks | every coil in one piece, and no two conductors touching |
| Tolerances | `bridge/tolerance.yaml`, PyPEEC's own defaults, unchanged: GMRES with its own preconditioner, SciPy's FFT and SuperLU |

## 45.7 Solve And Read Back

`study.solve` runs PyPEEC's mesher and solver once per frequency, in a process of its own, so that
its peak memory is measured. Per coil it reads back:

| Result | From |
|---|---|
| V, I, Z = V / I | the sources' values: V across the two terminals, I into the first |
| R = Re Z, L = Im Z / ω | Z |
| M and the mutual resistance, for a coil with no current | Im(V_RX / I_TX) / ω and Re(V_RX / I_TX) |
| L from the stored energy, R from the losses | 4W / \|I\|² and 2P / \|I\|², with one coil driven: a check that does not go through the terminals |
| The solve itself | iterations, residual, PyPEEC's own checks (solver, condition, solution), peak memory, time |

All of it, with the grid, the settings and the software versions, goes into the example's results
file: `results.json` for E01 and E02, `Results/<gap>_AirGap/results_gap<gap>mm.json` (with a `.csv`
and a chart) for the coil board. A coil-board solve is read only when the TX's L and R from its voltage
agree with the L from the energy and the R from the losses within 1 %.

| Previous | Next |
|:---|---:|
| [PyPEEC Installation](PyPEEC-Installation.md) | [PyPEEC Simulating Your Own Board](PyPEEC-Simulating-Your-Own-Board.md) |
