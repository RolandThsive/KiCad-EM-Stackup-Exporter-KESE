# 6. Working Principle

<!-- Picture wanted: Introduction 1, one overview picture of the pipeline: the .kicad_pcb on the
     left, the nine stages, the output files on the right. -->

KESE is a linear pipeline of nine stages (`kese/pipeline.py`), one folder each in `kese/`,
numbered in the order they run. Every stage takes the one object the stage before it made and
hands its own to the next; nothing is recomputed per output format. The files are written before
the Verifier runs, because the Verifier also checks the written GLB; the two text records come
last so that the report carries the Verifier's result.

<h4 align="center">read → collect → resolve → geometry → materials → assemble → write → verify → report</h4>

1. **Read** (`kese/s1_read/`). Parses the s-expression file into a tree. Checks that it is
   a `(kicad_pcb ...)` file, reads the `(version ...)` and `(generator ...)`, lists the copper
   layers in order (`F.Cu`, `In1.Cu` ... `InN.Cu`, `B.Cu`), takes the board thickness from
   `(general (thickness ...))` and the title from the title block. A file format outside the
   tested range or more than six copper layers gives a warning; missing `F.Cu` or `B.Cu` is an
   error. The result is a `RawBoard`.

2. **Collect** (`kese/s2_collect/`, one file per kind of item). Walks the tree and turns every
   element into a flat 2D shape in KiCad's coordinate frame (mm, Y down): track segments and arcs
   become thick lines, pads become their KiCad shape at their position and angle, zones contribute
   their stored fill polygons, graphics and text become painted strokes, vias become a round pad
   on every layer they span (except rings dropped by KiCad's "remove unused layers") plus a hole.
   The stack-up is read from Board Setup ([Stack-Up Model](Stack-Up-Model.md)). The result is the
   `Items`: the shapes per layer with their nets, the holes, and counters of what was found and
   what was skipped.

3. **Resolve** (`kese/s3_resolve/`). Builds the outline from `Edge.Cuts`; per layer and per net
   it unions the copper, clips it to the outline and drills the holes, still in KiCad's frame,
   then moves the result into the board frame (Y up, origin at the outline centre or at KiCad's
   origin) and snaps it to the geometry grid; it also computes the plated barrels, the edge
   plating, the mask openings and the silkscreen. The result is the `Regions`: per-layer regions
   with nets.

4. **Geometry** (`kese/s4_geometry/`). Six builders turn the regions into *prisms*, each a
   flat region between two heights with a part name, a role and physical properties:
   `laminate` (dielectrics), `copper` (copper per net, etch slices), `plating` (via and hole
   barrels), `solder_mask`, `silkscreen` and `finish`. Before them, `heights` works out the copper
   bands and mask thicknesses from the stack-up, once. All prisms go into one `PrismSet`
   (`kese/model/prisms.py`). This is the master geometry; everything downstream is made from it.

5. **Materials** (`kese/s5_materials/`). Gives every part a material from `Color.MATERIALS`,
   honouring the stack-up's colour names when `Color.USE_STACKUP_COLORS` is on. Physical
   properties (εr, conductivity) stay on the prisms; this stage only decides the look. See
   [Colorizing](Colorizing.md).

6. **Assemble** (`kese/s6_assemble/`). Builds one in-memory `Model`. In simulation mode
   (`solids.py`), every prism is extruded to a closed triangle mesh and all pieces of a part (a
   net's traces on every layer plus its vias) are joined by a boolean union into closed solids:
   one where the pieces touch, separate bodies within the part where they do not. Before the
   union, regions that touch are made to share exact boundary vertices (no T-junctions) and
   regions that touch at a single point are parted by a hair so each solid is manifold. In visual
   mode the skin builder (`skin.py`) joins every prism in one exact union, tile by tile on a big
   board (`tiles.py`), and keeps the surface between material and air
   ([Output Modes](Output-Modes.md)). The meshes are then scaled to the output units, rotated to
   the output orientation and given smooth normals across edges flatter than
   `Run.SMOOTH_SHADE_ANGLE_DEG` (`transform.py`).

7. **Write** (`kese/s7_write/`, one file per format). Writes the requested files from the same
   `Model` into a new run folder: GLB, OBJ and STL from the meshes; STEP from the prisms
   themselves as exact B-rep solids (not from triangles), with runs of vertices that lie on one
   circle written back as true arcs; then `materials.json`. See
   [Project Output Organization](Project-Output-Organization.md).

8. **Verify** (`kese/s8_verify/`, opt-in). The Verifier proves the model: in simulation mode
   every part must be watertight with consistent winding and no two parts may overlap along 3,000
   random vertical rays; in visual mode the faces along every ray that hits the board must take
   turns, into the material and out of it. If the Khronos `gltf_validator` is on the PATH, the
   written GLB is run through it and its last line reported. See
   [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md).

9. **Report** (`kese/s9_report/`). Writes `parameters.txt` and `report.txt` next to the model
   files.

Below the stages sit two shared folders: `kese/core/` holds the tools that know nothing about
stages (the s-expression parser, 2D maths and shapes, extrusion, the stroke font, safe file
names), and `kese/model/` holds the data classes handed from one stage to the next (`RawBoard`,
`Items`, `Regions`, `PrismSet`, `Model`, `Files`). A stage uses only those, `parameters/` and the
stages before it; `tests/test_layout.py` checks this on every test run
([Project Output Organization](Project-Output-Organization.md) shows the whole tree).

## 6.1 The Design Choice That Matters Most

Everything is built from **2D regions snapped to one grid** and extruded between **heights
computed once** from the stack-up. Every vertex of every 2D region is rounded to the grid
(the one exception is where polygons touch: just before extrusion, inside one region a polygon
that touches another at a point or along a line is shrunk all round by half of
`Geometry.PINCH_POINT_OPENING_MM`, and between the regions of one part a single touching point is
notched out; as a last resort, a polygon whose own rings pinch and that cannot be extruded
watertight is shrunk all round by the full `Geometry.PINCH_POINT_OPENING_MM`. Those vertices sit
just off the grid):

```math
x' = g \cdot \mathrm{round}\left( \frac{x}{g} \right), \qquad y' = g \cdot \mathrm{round}\left( \frac{y}{g} \right) \qquad (6.1)
```

where $`g`$ is the grid pitch, `Geometry.SNAP_GRID_MM` (0.1 µm by default). Heights are not
rounded. Because neighbouring layers share identical vertices and exact z values, the solids of
different parts touch without gaps or overlaps (three known exceptions: silkscreen kept in mask
openings with `Silkscreen.SILKSCREEN_OVER_COPPER = True`, see [Silkscreens](Silkscreens.md); with
`Copper.ETCH_FACTOR > 0` an empty wedge beside each sloped copper wall, see
[Copper And Traces](Copper-And-Traces.md#115-etch-factor); and edge plating with
`Run.COPPER_GROUPING = "layer"`, where inner copper overlaps the band, see
[Copper And Traces](Copper-And-Traces.md#117-edge-plating)), the per-part unions succeed, and the Verifier's overlap test comes back at
0.000 µm on the example boards. The price is that curves are faceted in the mesh formats; the STEP
writer recovers the true circles from the faceted rings so that CAD gets real cylinders.

## 6.2 Coordinate Frames

| Frame | Where | Axes |
|---|---|---|
| KiCad | the file | mm, X right, Y **down**, page origin |
| Board | inside KESE | mm, X right, Y **up**, origin at the outline centre (`Run.ORIGIN = "center"`) or at KiCad's page origin (`"kicad"`); z = 0 at the laminate mid-plane, `F.Cu` toward +Z |
| Output | the files | mm or m (`Run.UNITS`); board in the XY plane with `F.Cu` toward +Z (`Run.ORIENTATION = "upright"`) or in the XZ plane with `F.Cu` toward +Y (`"flat"`) |

From KiCad to the board frame (in stage 3, `kese/s3_resolve/frame.py`), every 2D point is shifted to the
origin and the Y axis is flipped:

```math
x_b = x_k - c_x, \qquad y_b = -\left(y_k - c_y\right) \qquad (6.2)
```

```math
(c_x, c_y) = \begin{cases} \left( \frac{x_{\min} + x_{\max}}{2},\ \frac{y_{\min} + y_{\max}}{2} \right) & \text{origin at the centre} \\ (0,\ 0) & \text{KiCad origin} \end{cases} \qquad (6.3)
```

From the board frame to the written files (in `kese/s6_assemble/transform.py`), every 3D point is
scaled to the output units and, for the flat orientation, turned so that `F.Cu` faces +Y:

```math
\begin{pmatrix} x_o \\ y_o \\ z_o \end{pmatrix} = u R \begin{pmatrix} x_b \\ y_b \\ z_b \end{pmatrix}, \qquad u = \begin{cases} 1 & \text{mm} \\ 10^{-3} & \text{m} \end{cases}, \qquad R = \begin{cases} I & \text{upright} \\ \begin{pmatrix} 1 & 0 & 0 \\ 0 & 0 & 1 \\ 0 & -1 & 0 \end{pmatrix} & \text{flat} \end{cases} \qquad (6.4)
```

| Symbol | Meaning | Parameter |
|---|---|---|
| $`x_k, y_k`$ | a point in KiCad's frame (mm, Y down) | |
| $`x_b, y_b, z_b`$ | the same point in the board frame (mm, Y up, $`z_b = 0`$ at the laminate mid-plane) | |
| $`c_x, c_y`$ | the origin in KiCad coordinates | `Run.ORIGIN` |
| $`x_{\min} \dots y_{\max}`$ | bounding box of the board outline in KiCad coordinates | |
| $`x_o, y_o, z_o`$ | the point as written to the files | |
| $`u`$ | unit scale | `Run.UNITS` |
| $`R`$ | orientation | `Run.ORIENTATION` |

`report.txt` states which origin was used, with the offset $`(c_x, c_y)`$ in KiCad coordinates, so
positions can be mapped back to the layout.

| Previous | Next |
|:---|---:|
| [Examples](Examples.md) | [Stack-Up Model](Stack-Up-Model.md) |
