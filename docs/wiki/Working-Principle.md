# 7. Working Principle

![The nine stages of KESE as cards, read to report, each with its folder, a picture of what it made for board 20b_format_kicad7, and the object it hands to the next stage: RawBoard, Items, Regions, PrismSet, PrismSet, Model, Files, Files, Files. Card 1 shows the board file as KiCad draws it, card 8 one net's volume found four ways, and card 9 what report.txt lists](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/wp_1_pipeline.webp)

KESE is one straight pipeline, `kese/pipeline.py`. Every stage is a folder in `kese/` with a
`run(what the stage before made, job)` that returns what it makes:

```python
STAGES = (read, collect, resolve, geometry, materials, assemble, write, verify, report)

out = pcb_path
for stage in STAGES:
    out = stage.run(out, job)
```

| # | Stage | Gets | Gives | What it does |
|---|---|---|---|---|
| 1 | `s1_read` | `.kicad_pcb` file | `RawBoard` | Parses the file and lists the copper layers, the board thickness and the file format; every rule that depends on the KiCad version is in `parse_kicad_version.py`. Warns outside the tested file formats (the 2013 builds before KiCad 4 to KiCad 10) and above eight copper layers; stops if `F.Cu` or `B.Cu` is missing |
| 2 | `s2_collect` | `RawBoard` | `Items` | Every track, pad, zone fill, graphic, text and via as a flat shape on its layer, with its net, in KiCad's frame; the stack-up from Board Setup; counts of what was read and what was skipped |
| 3 | `s3_resolve` | `Items` | `Regions` | The outline; the copper joined per layer and net, clipped and drilled; barrels, edge plating, mask openings and silkscreen; everything moved to the board frame and snapped to the grid |
| 4 | `s4_geometry` | `Regions` | `PrismSet` | The heights from the stack-up, once; every part as prisms, each a flat region between two heights |
| 5 | `s5_materials` | `PrismSet` | `PrismSet` | A material for every part ([Colorizing](Colorizing.md)) |
| 6 | `s6_assemble` | `PrismSet` | `Model` | Closed solids (simulation mode) or the visible surface (visual mode), in the output units and orientation (7.2) |
| 7 | `s7_write` | `Model` | `Files` | GLB, STEP, STL, OBJ and `materials.json` in a new run folder |
| 8 | `s8_verify` | `Files` | `Files` | Only with `--verify`: every part closed and consistently wound, its volume the same four ways, no two parts overlapping ([Checks, Errors And Warnings](Checks-Errors-And-Warnings.md)) |
| 9 | `s9_report` | `Files` | `Files` | `report.txt` and `parameters.txt` |

Nothing is rebuilt per output format: stage 7 writes every file from the one `Model`. The files are
written before the Verifier runs, because it also checks the written GLB, and the report comes last
so that it carries the Verifier's result.

Two shared folders sit below the stages: `kese/core/` holds the tools that know nothing about
stages (the s-expression parser, 2D shapes, the boundary of a stack of prisms, triangulation, the
stroke font, work in threads and processes), and `kese/model/` the classes handed from one stage
to the next. A stage uses only those, `parameters/` and the stages before it;
`tests/test_layout.py` checks this ([Project Output Organization](Project-Output-Organization.md)
shows the whole tree).

## 7.1 The Design Choice That Matters Most

Everything is built from **2D regions snapped to one grid**, between **heights worked out once**
from the stack-up:

```python
# kese/core/shapes2d.py, snap(): every polygon that is not on the grid yet is rounded to it
off = ~on_grid(parts)
parts[off] = shapely.set_precision(parts[off], grid())      # Geometry.SNAP_GRID_MM, 0.1 µm
```

- Every vertex of every region lies on the grid; heights are not rounded. So two parts that touch
  have the very same edges and heights: no gap and no overlap between them, and every part's
  surface closes. The Verifier's overlap test finds no shared material on any board of the
  regression suite.
- Cuts are taken on the grid (`shapes2d.diff` and `inter`). Where GEOS refuses one, the regions
  are made valid and the cut tried again; where it still refuses, both are put on the grid first
  (`snap`) and the cut made again. That last step is for a slice joined in floating point whose
  sliver holes, thinner than a grid step, snap rounding cannot place (the visual skin of a KiCad 4
  board stopped there).
- Where a region would pinch to a point (two pieces touching at one vertex), a disc of
  `Geometry.PINCH_POINT_OPENING_MM` is cut out of the smaller piece so that the solid can close
  (`kese/core/pinches.py`). Those vertices sit just off the grid.
- One known exception, where parts can overlap or leave a gap: the wedge beside a sloped copper
  wall (`Copper.ETCH_FACTOR > 0`, see [Copper And Traces](Copper-And-Traces.md#125-etch-factor)).
- The price: curves are polygons, in the meshes and in the STEP file alike.

## 7.2 How A Part Becomes A Closed Solid

![Stage 6 on one net of board 04_vias_blind_buried, a through via with a track on In3.Cu: its four prisms, its five slices between six heights, its six flat faces looking up or down, its walls, its 1,048 triangles, and the same volume found four ways, from the prisms, the slices, the faces and the triangles, as four equal bars](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/wp_2_solid.webp)

Stage 6 needs no CAD kernel. Every part's surface is worked out in 2D from its prisms
(`kese/core/boundary.py`) and then cut into triangles (`kese/core/boundary_mesh.py`):

```python
def boundary_of(part, prisms, log=None):
    """The prisms of one part -> its Boundary, closed by construction."""
    levels = heights_of(prisms)                    # every height where a prism starts or ends
    slices = slices_of_part(prisms, levels, log)   # the material between two neighbouring heights
    flats, again = [], range(len(levels))
    for _ in range(sh.G().VERTEX_SHARING_ROUNDS):   # Geometry.VERTEX_SHARING_ROUNDS, 20
        flats = flat_faces(slices, levels, flats, again)   # below minus above looks up, above minus below down
        slices, changed = slices_sharing_vertices(slices, flats, levels, log)
        if not changed:
            break
        again = {k for i in changed for k in (i, i + 1)}      # the heights at a changed slice's ends
    ...

mesh = mesh_of_boundary(boundary)                  # faces cut into triangles, two per wall edge
```

- The walls are the rings of every slice, stood up between the slice's two heights
  (`Boundary.walls()`). Faces and walls must meet on identical edges, so the slices that meet at a
  height are given each other's vertices, and their faces' vertices, until nothing changes
  (`kese/core/vertices.py`). Then the mesh closes by construction. Where needle tips of two
  slices lie a grid step or two apart, giving one the other's vertex and putting both back on the
  grid can move them for ever: slices still changing after `Geometry.VERTEX_SHARING_ROUNDS`
  rounds (20; most settle in one to three, a hole's finish in visual mode has taken twelve) are
  cut open at each point a further round adds, every slice by a disc of
  `Geometry.PINCH_POINT_OPENING_MM`, doubling each round, for at most `Geometry.PINCH_CUT_ROUNDS`
  rounds, and `report.txt` notes it. On one board's solder mask the slices still traded vertices
  after an hour; a 20 µm piece of it ends some 400 rounds with three T-junctions, and cut open so
  settles, closed.
- A slice is made once for all the heights the same prisms span (a hole's finish is three prisms,
  one per stretch of the wall, and the same between every two of its layers). The faces at a height
  are cut only where the slices below and above differ (`kese/core/flat_faces.py`): the pieces both
  have, ring for ring, face nothing, and the rest is cut group by group, the pieces within a grid
  step of each other, the most a cut on the grid reaches. Each cut is taken in floating point and
  only its new vertices, where two outlines cross, are rounded onto the grid
  (`shapes2d.exact_diff`): where two slices differ by less than a grid step, as where a band one
  step wide ends in two needle tips a hair apart, a cut on the grid would drop that sliver from the
  faces while the walls of both slices keep their tips, and leave the part open. After the first
  round, the faces are cut again only at the heights next to a slice that changed.
- The faces are cut by earcut, as in KiCad's 3D viewer; a polygon of more than
  `Geometry.TRIANGULATE_CELL_POINTS` points strip by strip, as KiCad cuts big polygons into cells.
  A cut that does not close exactly on the polygon's edges is done again by GEOS's constrained
  Delaunay triangulation, through `shapely` (`kese/core/triangulate.py`). Earcut makes a flat triangle (three points on one
  line, area zero) where a ring has a point on a straight run, the vertex another face shares; such
  a triangle is flipped away with its neighbour across its long edge, so no mesh holds a triangle
  of zero area, which some meshers and STL importers reject.
- `Parallel.WORKERS` parts are built at once (at most `Parallel.PROCESS_WORKERS`), the biggest
  first, each in a process of its own (much of the work is Python's, which threads would take in
  turn; a board of under `Parallel.PROCESS_MIN_COORDINATES` coordinates, 20,000, is built part
  after part, as starting the processes would take longer). The files come out the same,
  byte for byte, however many processes ran, but for the time in the STEP file's header, and the
  times in `report.txt` and `parameters.txt`. Every part keeps its faces (its `Boundary`), and the
  STEP writer writes those same faces as a closed solid.
- Visual mode does the same for all parts at once and keeps only the faces between material and
  air (`skin_faces.py`, `skin_mesh.py`, see [Output Modes](Output-Modes.md)). There each part is
  sliced in a process of its own, as above; the faces are then found, and the hidden triangles
  dropped, in `Parallel.WORKERS` threads.
- Last, every mesh is scaled to the output units, turned to the output orientation and shaded
  smooth across edges flatter than `Run.SMOOTH_SHADE_ANGLE_DEG` (`transform.py`). The meshes are
  KESE's own (`kese/core/mesh.py`), and so are the GLB, STL, OBJ and STEP writers (`kese/s7_write/`).

## 7.3 Coordinate Frames

![The outline of board 20c_format_kicad8 and its top left corner P in three frames: KiCad's, in mm with Y down from the page's corner; the board frame, in mm with Y up from the outline's centre and z from the laminate's mid-plane; and the output, in metres, upright or flat](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/wp_3_frames.webp)

| Frame | Where | Units and axes | Origin |
|---|---|---|---|
| KiCad | the `.kicad_pcb` file | mm; X right, Y **down** | the page's top left corner |
| Board | inside KESE, stages 3 to 6 | mm; X right, Y **up**; `F.Cu` toward +Z | the outline's centre (`Run.ORIGIN = "center"`) or KiCad's origin (`"kicad"`); z = 0 at the laminate's mid-plane |
| Output | the written files | mm or m (`Run.UNITS`); the board in the XY plane with `F.Cu` toward +Z (`Run.ORIENTATION = "upright"`) or in the XZ plane with `F.Cu` toward +Y (`"flat"`) | as the board frame |

```python
# kese/s3_resolve/frame.py: KiCad (x, y down) -> board (x - cx, -(y - cy)), on the grid
sh.snap(affinity.affine_transform(sh.polys_only(g), [1, 0, 0, -1, -cx, cy]))

# kese/s6_assemble/transform.py: board -> output
scale = 1.0 if R.UNITS == "mm" else 0.001
if R.ORIENTATION == "flat":      # board in XZ, F.Cu toward +Y
    rot = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, 0], [0, 0, 0, 1]], dtype=float)
```

`report.txt` names the origin used, for example
`origin: outline centre (112.0000, 108.0000) in KiCad coordinates`, so a position in the model can
be mapped back to the layout.

## 7.4 Work Done In Parallel

`Parallel.WORKERS` threads or processes work at once (`0`: one per processor thread the run may
use; `1`: everything in turn, in one process), and at most `Parallel.PROCESS_WORKERS` processes
([Parameter Reference](Parameter-Reference.md#179-parallel-parametersparallelpy)).
`kese/core/parallel.py` holds both kinds:

| Stage | What runs at once | In |
|---|---|---|
| 3 resolve | the copper layers, the biggest first | processes on a board of `Parallel.PROCESS_MIN_NETS` nets or more (1,000), else threads |
| 3 resolve | the solder mask's minimum web width, group by group of openings | threads |
| 4 geometry | the top and bottom solder mask, then the top and bottom silkscreen; the finish's bores, in groups near each other, and copper layers | threads |
| 6 assemble, simulation mode | the parts' solids, the biggest part first, and with the Verifier on their checks | processes |
| 6 assemble, visual mode | each part sliced | processes |
| 6 assemble, visual mode | the faces, the walls and the test for hidden triangles | threads |
| 7 write, STEP | each part's topology and arcs, then its entities' text | processes |
| 8 verify, simulation mode | the overlap check: the slices split into polygons, then shrunk and tested | threads |

- Threads where the 2D geometry library, GEOS, does the work: it runs outside Python's lock.
  Processes where much of the work is Python's own, which threads would take in turn. Parts that
  hold under `Parallel.PROCESS_MIN_COORDINATES` coordinates in all (20,000) are built, and written
  to STEP, in the main process, as starting the processes would take longer. The copper layers go
  to processes only on a board of `Parallel.PROCESS_MIN_NETS` nets or more (1,000), counted layer
  by layer (`kese/s3_resolve/copper.py`): much of a net's work is then Python's, and CIAA ACC's copper takes
  13 s in four processes against 24 s in four threads; with fewer nets most of the work is GEOS's,
  which threads run as fast without sending the shapes to and fro (NE_Delta, 804 nets on 2 layers:
  8.0 s in threads, 9.3 s in processes).
- A STEP file's parts are worked on in two rounds (`kese/s7_write/step_parts.py`). First each
  part's topology and arcs, which give the exact number of entities the part takes, so that the
  number its entities start from is known; then each part's entities, numbered from there, are
  written into a file of their own, in a hidden folder beside the STEP file. The files are copied
  into the STEP file in the parts' order and removed, and so is the folder, also when the write
  fails (a full disk, Ctrl-C).
- The results are put back in the layers', sides' and parts' order, so the files are the same,
  byte for byte, however many threads or processes ran (but for the times, as in 7.2).
- A thread makes shapes only from its own copies of the shapes other threads use
  (`kese/core/shape_copies.py`). GEOS 3.14 counts the shapes of each of its factories without a
  lock, and a shape on the grid shares its factory with every shape made from it: two threads
  making shapes from one shared shape could crash the run. The copies keep the grid of the shape
  and of each of its parts. Where only the coordinates count (the walls, a coverage union), a
  cheaper copy on no grid does: it is on GEOS's default factory, which is never freed, so threads
  may share it. GEOS 3.15 counts atomically, and with it nothing is copied.
- A prepared shape, whose search indexes GEOS builds on first use, serves one thread at a time:
  the threads take turns with one prepared copy of each slice's material, so memory does not grow
  with the number of threads, and the test for hidden triangles frees its indexes when it is done.
  An R-tree that threads share (of each slice's material, of the solid beside the finish's bores)
  is built before they share it (`kese/core/graph.py`, `shared_tree`): GEOS builds one on its first
  query, under a lock, but a thread that finds it built reads it with none, and on a processor that
  may reorder writes (ARM) could read it half written.
- After each step done in threads, and in each worker after each part, the memory freed is handed
  back to the system (`Parallel.GIVE_BACK_MEMORY`). On Linux, glibc keeps a pool of memory for each thread and holds on to what
  is freed in it, where the steps that follow cannot use it. With these, NE_Delta's visual model
  peaks at 2.65 GB with 4 workers and 3.57 GB with 32, where it took 3.45 GB and 4.76 GB.
- The processes start afresh, as Windows and macOS start them, on every system, and are given the
  run's settings, `--for` and `--set` included. Shapes sent to and from them keep their grid, which
  shapely's own pickling would drop.
- Where the system stops a worker, or one runs out of memory, the parts left go to half as many
  processes, and to the main process, one after another, once that would be one; where the
  processes cannot start, the main process builds the parts. `report.txt` says so each time
  ([Checks, Errors And Warnings](Checks-Errors-And-Warnings.md#1813-notes-worth-knowing)). An
  error in a part's own work stops the run at once and ends the other workers.
- Ctrl-C, or the end of the main process however it ends, ends the workers too. On Linux the
  system's out-of-memory killer takes a worker before the main process. Inside a
  `multiprocessing.Pool`'s worker, which may not start processes, every part is built in that
  process. A script that calls KESE without `if __name__ == "__main__":` is not run again in each
  worker.

| Previous | Next |
|:---|---:|
| [Time Distribution](Time-Distribution.md) | [Stack-Up Model](Stack-Up-Model.md) |
