# 6. Working Principle

<!-- Picture wanted: Introduction 1, one overview picture of the pipeline: the .kicad_pcb on the
     left, the seven stages, the output files on the right. -->

KESE is a linear pipeline of seven stages (`Generator/Pipeline.py`). Every stage works on one
in-memory object and hands it to the next; nothing is recomputed per output format.

```text
Reader -> BoardBreakdown -> Geometry -> Colorer -> Assembler -> Verifier -> Packager
```

1. **Reader** (`Generator/Reader.py`). Parses the s-expression file into a tree. Checks that it is
   a `(kicad_pcb ...)` file, reads the `(version ...)` and `(generator ...)`, lists the copper
   layers in order (`F.Cu`, `In1.Cu` ... `InN.Cu`, `B.Cu`), takes the board thickness from
   `(general (thickness ...))` and the title from the title block. A file format outside the
   tested range or more than six copper layers gives a warning; missing `F.Cu` or `B.Cu` is an
   error.

2. **BoardBreakdown** (`Generator/BoardBreakdown.py`). Walks the tree and turns every element into
   a flat 2D shape in KiCad's coordinate frame (mm, Y down): track segments and arcs become
   thick lines, pads become their KiCad shape at their position and angle, zones contribute their
   stored fill polygons, graphics and text become painted strokes, vias become a round pad on
   every layer they span plus a hole. The stack-up is read from Board Setup
   ([Stack-Up Model](Stack-Up-Model.md)). Then `resolve()` builds the outline from `Edge.Cuts`,
   moves everything into the board frame (Y up, origin at the outline centre or at KiCad's
   origin), snaps it to the geometry grid, unions the copper per layer and per net, clips it to
   the outline, drills the holes and computes the plated barrels, mask openings and silkscreen.
   The result is a `Breakdown`: per-layer regions with nets, plus counters of what was found and
   what was skipped.

3. **Geometry** (`Generator/Geometry/`). Five builders turn the regions into *prisms*, each a
   flat region between two heights with a part name, a role and physical properties:
   `Board` (dielectrics), `Copper` (copper per net, via barrels, etch slices), `SolderMask`,
   `Silkscreen` and `Finish`. All prisms go into one `PrismSet` (`Generator/Common/prisms.py`).
   This is the master geometry; everything downstream is made from it.

4. **Colorer** (`Generator/Colorer.py`). Gives every part a material from
   `Color_Parameters.MATERIALS`, honouring the stack-up's colour names when
   `Color.USE_STACKUP_COLORS` is on. Physical properties (εr, conductivity) stay on the prisms;
   the Colorer only decides the look. See [Colorizing](Colorizing.md).

5. **Assembler** (`Generator/Assembler.py`). Builds one in-memory `Model`. In simulation mode,
   every prism is extruded to a closed triangle mesh and all pieces of a part (a net's traces on
   every layer plus its vias) are joined by a boolean union into one closed solid. Before the
   union, regions that touch are made to share exact boundary vertices (no T-junctions) and
   regions that touch at a single point are parted by a hair so each solid is manifold. In visual
   mode the `Skin` builder keeps only the faces that are not buried inside another prism
   ([Output Modes](Output-Modes.md)). The meshes are then scaled to the output units, rotated to
   the output orientation and given smooth normals across edges flatter than
   `Run.SMOOTH_SHADE_ANGLE_DEG`.

6. **Verifier** (`Generator/Verifier.py`, opt-in). Proves the model: in simulation mode every
   part must be watertight with consistent winding and no two parts may overlap along 3,000
   random vertical rays; in visual mode every ray must cross exactly one upward and one downward
   surface. If the Khronos `gltf_validator` is on the PATH, the GLB is validated too. See
   [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md).

7. **Packager** (`Generator/Packager/`). Writes the requested files from the same `Model`: GLB,
   OBJ and STL from the meshes; STEP from the prisms themselves as exact B-rep solids (not from
   triangles), with runs of vertices that lie on one circle written back as true arcs. Then
   `materials.json`, `parameters.txt` and `report.txt`. See
   [Project Output Organization](Project-Output-Organization.md).

## 6.1 The Design Choice That Matters Most

Everything is built from **2D regions snapped to one grid** (`Geometry.SNAP_GRID_MM`, 0.1 µm by
default) and extruded between **heights computed once** from the stack-up. Because neighbouring
layers share identical vertices and exact z values, the solids of different parts touch without
gaps or overlaps, the per-part unions succeed, and the Verifier's overlap test comes back at
0.000 µm on the example boards. The price is that curves are faceted in the mesh formats; the STEP
writer recovers the true circles from the faceted rings so that CAD gets real cylinders.

## 6.2 Coordinate Frames

| Frame | Where | Axes |
|---|---|---|
| KiCad | the file | mm, X right, Y **down**, page origin |
| Board | inside KESE | mm, X right, Y **up**, origin at the outline centre (`Run.ORIGIN = "center"`) or at KiCad's page origin (`"kicad"`); z = 0 at the laminate mid-plane, `F.Cu` toward +Z |
| Output | the files | mm or m (`Run.UNITS`); board in the XY plane with `F.Cu` toward +Z (`Run.ORIENTATION = "upright"`) or in the XZ plane with `F.Cu` toward +Y (`"flat"`) |

`report.txt` states which origin was used, with the offset in KiCad coordinates, so positions can
be mapped back to the layout.

| Previous | Next |
|:---|---:|
| [Examples](Examples.md) | [Stack-Up Model](Stack-Up-Model.md) |
