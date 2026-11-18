# 63. Palace Workflow

What happens between `python simulation.py` and the numbers in the results file, step by step. Every step is one
function of the bridge on the `Palace_Integration` branch; the file is named with each. The bridge is general: nothing
in it names a board, a coil or an example. Each example adds only what belongs to its own board: which nets are coils,
where each coil is opened, what to sweep, and what to compare the answer with.

## 63.1 Export The Board With KESE

`bridge/geometry.py` runs KESE as a program, never as a library:

```bash
python run_KESE.py board.kicad_pcb --for elmer --format step stl --out <folder> \
    --set Stackup.solder_mask=True --set SolderMask.USE_STACKUP_MASK_THICKNESS=False \
    --set SolderMask.MASK_OVER_COPPER_MM=0.020 --set SolderMask.MASK_OVER_LAMINATE_MM=0.020 \
    --set SolderMask.VIA_TENTING=tented
```

KESE's solver preset writes one STL per solid and a `materials.json` with each part's role, net, layer and height
([Choosing An Export](Choosing-An-Export.md)); the bridge reads the STL files with `trimesh`. `bridge/study.py` keeps
the export in one of two ways, and either way an unchanged board is not exported twice:

| Call | Where the export goes |
|---|---|
| `kese_geometry(board, folder)` | a folder meant to be committed beside the board (the examples use `3D_Geometry/`), with a `source.json` holding the board file's hash, KESE's version and the settings |
| `kese_export(board, cache)` | a scratch cache named by the board file's hash |

Because every example's `3D_Geometry/` is committed, the examples run without KESE installed.

## 63.2 Place The Parts

`geometry.load_parts` turns each solid into a part in model coordinates: x and y as KESE's (y up, so
y_model = −y_KiCad), z shifted so that the top face of the top copper is z = 0. A part's body is its net for copper,
`MASK` or `FR4` otherwise, or whatever the example's `body_of` names it. A second board can be flipped copper side
down without mirroring its pattern, lifted by an air gap and turned about an axis the caller gives: that is how a rotor
is placed over a stator, at KiCad's point (100, 100).

## 63.3 Build The 2.5D Mesh

`bridge/mesh25d.py` builds a **2.5D mesh**, the shape a printed board has:

| Step | What happens |
|---|---|
| Slabs (`Layout.build`) | Every height at which some part starts or ends splits the model into slabs; each part is sectioned in the middle of each slab it spans. With `insulators=False` (every example) FR-4 and mask are left out: to these fields an insulator with μr 1 is air |
| Triangles (`build_mesh`) | One triangle mesh, made by gmsh, covers the domain's disc, with every copper edge of every slab drawn into it as a line, and any line the caller adds (`extra_lines`: port lines, cut outlines). Every point is snapped to a 0.5 µm grid, so a given line lands exactly on mesh edges. The size is `h_edge` at copper edges, growing by `grade` per mm away from them, at most `h_in` inside copper and `h_max` far away |
| Wedges | The triangle mesh is swept through the slabs as prisms: layers at most `dz_copper` thick in a copper foil, at most `dz_max` elsewhere, and two thin air layers (`pads`) above and below. Each wedge takes the body of the part of highest priority whose section holds its triangle; a `void` part (air of priority 4) takes copper out, which is how a cut or a left-out via barrel is made |
| Tetrahedra (`tet_fill`) | gmsh fills the air above and below the wedges out to the domain's top and bottom, growing by `tet_grade` per mm up to `tet_max`, then Netgen's optimiser removes slivers, which stall the iterative solve |

No 3D Booleans: the wedges follow the layers exactly, so 35 µm copper on a 0.8 mm board stays a few hundred thousand
nodes. `write_gmsh` writes the mesh in Gmsh's format 2.2, in millimetres, each body a physical volume and each boundary
a physical surface.

## 63.4 Open Each Coil At Its Port

A lumped port in Palace must be a rectangle with its two ends on conductors, its direction along one of its sides.
`bridge/ports.py` and `mesh25d.vertical_faces` build it from a straight line drawn into the triangle mesh: the port is
the stack of vertical mesh faces along that line between two heights.

| Coil opened at | Port | Direction |
|---|---|---|
| Two stacked trace ends on two layers (the TX of the coil boards) | a sheet standing across the board between the two copper faces, 0.16 mm wide | `+Z` |
| A gap between two round trace ends on one layer (E01, E02) | a sheet across the gap through the copper's thickness, from tip to tip (`ports.facing_vertices` finds the two facing outline vertices) | along the line, `+Y` |
| A 0.2 mm cut across a top trace (SIN and COS of `S0d2_1x_OD23_2L_tiny_TX3top_Cut`) | the copper inside the cut box made air, the box's outline drawn into the mesh, and a sheet across the cut through the copper's thickness, from one cut face to the other | along the trace |
| A layer-change via left out | the barrel made air, its two pads filled over the drill hole, and a sheet standing between the pads | `+Z` |

`ports.electrodes` checks that the coil's copper meets the opening in exactly two places, so that the coil is one
open conductor.

![How S0d2_1x_OD23_2L_tiny_TX3top_Cut is set up in Palace, drawn by rig_picture.py from the geometry the mesh is built from. Left, seen from above: the TX's three turns in dark grey on F.Cu round SIN in blue and COS in orange, the rotor's two copper sectors in grey 1 mm above, the SIN and COS ports ringed at their 0.2 mm cuts across a top trace and the TX port ringed at its two stacked ends at x = 111 mm. Top right, a section through the stack with heights stretched: the rotor copper 1 mm over the stator's top copper, FR-4 and mask drawn as air. Bottom right, the SIN port as a hatched sheet across the cut, through the 35 µm copper, along the trace, and the TX port as a hatched sheet standing between its two ends, direction +z, driven through 50 Ω at 3.5 MHz](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Palace-Workflow/S0d2_1x_OD23_2L_tiny_TX3top_Cut/S0d2_1x_OD23_2L_tiny_TX3top_Cut_palace_setup.webp)

## 63.5 Write Palace's Input

`bridge/palace_case.py` (`config`) writes one `config.json` per solve:

| Section | What it holds |
|---|---|
| `Problem` | `Driven`: the frequency-domain solve |
| `Model` | the Gmsh mesh, with `L0 = 1e-3` (millimetres) |
| `Domains` | air everywhere (εr = μr = 1, FR-4 and mask included) and the copper with σ = 5.8e7 S/m |
| `Boundaries` | the outside as `PEC` (tangential E = 0), and one `LumpedPort` per coil: the driven one with 50 Ω and an excitation, the receivers with 1 MΩ, so they are open to a few parts in a million; or every port driven in turn, for the whole impedance matrix |
| `Solver` | Nédélec elements of order 1, one frequency point, and the linear solver: GMRES preconditioned by hypre's AMS |

The domain is a cylinder: 60 mm in radius and half height round E01 and E02, and three board radii (35.1 mm) round
`S0d2_1x_OD23_2L_tiny_TX3top_Cut`, reaching as far above the rotor and below the stator.

## 63.6 Solve And Read Back

`palace_case.run` runs `palace -np N config.json` on N MPI ranks, writing `palace.log` as it goes, and reads back
the CSV files Palace writes:

| Result | From |
|---|---|
| Each port's V | `port-V.csv`: the field's line integral across the sheet, along the port's direction |
| Each port's current I | (2 V_inc − V) / R at the driven port, with the source taken as 2 V_inc behind R; −V / R at an undriven one |
| Z | V I⁻¹ with every port driven, or the driven column Z[k][TX] = V_k / I_TX |
| R, L of a coil | Re Z, Im Z / ω (`coil_rows`) |
| M to a receiver, and M back | Im(Z[rx][TX]) / ω, and Im(Z[TX][rx]) / ω where the receiver was driven too |
| L from the field's energy | 2W / \|I\|², with W = ½ Re ∫ H*·B from `domain-E.csv` (`energy_check`) |
| Iterations, residual, converged, peak memory | Palace's log |

All of it, with the mesh's size, the run's time and the software versions, goes into the example's results file
(`results.json` for E01 and E02; `Results/<gap>_AirGap/results_gap<gap>mm.json` for the coil board, which also writes
a `.csv`, a chart and `SINCOS_Results.md`).

| Previous | Next |
|:---|---:|
| [Palace Installation](Palace-Installation.md) | [Palace Simulating Your Own Board](Palace-Simulating-Your-Own-Board.md) |
