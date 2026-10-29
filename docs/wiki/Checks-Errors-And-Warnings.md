# 17. Checks, Errors And Warnings

KESE reports in three places: the terminal while it runs, `report.txt` next to every output,
and the opt-in Verifier whose lines are appended to `report.txt`. Most items the model leaves
out are counted under `skipped` with the reason. A few are left out without a count: text,
text boxes and dimensions on non-physical layers (such as the Value fields on `F.Fab`, or a
dimension on `Dwgs.User`), hidden text, pad paste layers, and images or groups inside footprints.

```bash
cd Generator                                    # the program folder
python run_KESE.py board.kicad_pcb --verify     # generate, then run the Verifier
python tests/test_boards.py                     # the regression suite over every board
```

## 17.1 Levels

| Level | Meaning | What happens |
|---|---|---|
| Error | The file cannot be modelled, or the request is impossible. | Nothing is written for that board. With one board the traceback is shown; with several, `<file>: FAILED - <reason>` is printed (the file name with `.kicad_pcb`) and the run continues. Exit code 1. |
| Warning | The board is modelled, but something is likely to be wrong or missing. | Printed as `warning: ...` and written to `report.txt`. |
| Skipped | An item KESE does not model, or that is not physical. | Counted in `report.txt` under `skipped`, with a reason in the name. |
| Note | A fact about the run. | In `report.txt` under `notes`. |
| Verifier | The model's own proof. | `Verifier: PASS` or `FAIL` plus one line per check, at the end of `report.txt`. The run does not fail on a Verifier FAIL. |

### 17.1.1 Errors

| Message | Cause and way out |
|---|---|
| `<file> is not a KiCad board file (expected (kicad_pcb ...))` | Not a `.kicad_pcb`. Export the board from pcbnew. |
| `<file>: no (layers ...) block` | A damaged or very old file. |
| `<file>: copper layers ['F.Cu', 'B.Cu'] are not declared` | Both outer copper layers must exist. |
| `MODE must be 'simulation' or 'visual', not ...` | A typo in `Run.MODE` (or `--set Run.MODE=...`). A typo in `--mode` is caught earlier by the command line: `argument --mode: invalid choice`, exit code 2. |
| `unknown FILE_FORMAT entries [...]` | Only `glb`, `stl`, `obj`, `step`. |
| `visual mode is a surface, not solids: FILE_FORMAT may only contain glb / obj` | STL and STEP need closed solids; use simulation mode. |
| `no Edge.Cuts outline and OUTLINE_FALLBACK is 'error'` | Draw a closed outline, or set `Board.OUTLINE_FALLBACK = "copper_hull"`. |
| `missing Python package(s): ...` | Printed before anything runs, with the `pip install` line to use. |
| `parameters/<module>.py has no parameter <NAME>` | A `--set` with a misspelt name. A misspelt module gives a Python `AttributeError`, and a `--set` without a `.` a `ValueError`. |
| `no boards given and none found in Input/` | Put a board in `Input/` or give a path. |

### 17.1.2 Warnings

| Message | Meaning |
|---|---|
| `file has no (version ...): treated as legacy KiCad 5` | Best-effort read. |
| `file format N is outside the tested range 20211014-20260206; proceeding best-effort` | Older than KiCad 6 or newer than KiCad 10. |
| `N copper layers: more than the 8 this project has been tested with` | The layers are still modelled. |
| `N copper zone(s) have no fill stored in the file and are ignored` | Fill the zones in KiCad (press **B**) and save. Until then those zones produce no copper. |
| `Edge.Cuts lines/arcs do not form a closed outline` | The outline could not be polygonized; closed shapes on `Edge.Cuts` are still used. |
| `no Edge.Cuts outline; using the copper's convex hull + 1.0 mm` | The fallback outline. |
| `DIELECTRIC_SPLIT=... unknown, using 'even'` | Only `"even"` is implemented. |
| `not modelled, see 'skipped' in report.txt: backdrills of vias, filled vias, ...` | The board has padstacks, or holes that KiCad 10 backdrills, post-machines, covers, plugs, caps or fills. KESE models the front shape on every layer and the hole plated through its whole span and open; `skipped` gives the counts. |
| `left out, of a kind KESE does not know: gr_ellipse (2), ...` | Items of a kind KESE does not read, such as the ellipses of KiCad's development version. They are missing from the model. |
| `the stack-up colour '<value>' of <layer> is neither a colour name of parameters/color.py nor #RRGGBBAA; its parts keep their MATERIALS colour` | A mask or silkscreen colour KESE cannot read keeps KESE's colour. Add the name to the tables in `parameters/color.py` ([Colorizing](Colorizing.md#122-colours-from-the-stack-up)). |

### 17.1.3 Notes Worth Knowing

| Message in `notes` | Meaning |
|---|---|
| `note: Edge.Cuts line ends up to D mm apart joined (Board.OUTLINE_LINE_SNAP_MM = S mm)` | The outline's lines had small gaps between their ends; they were closed as KiCad closes them (KiCad joins ends up to 0.01 mm apart, the default of `Board.OUTLINE_LINE_SNAP_MM`), so the board shape is the one KiCad shows. |
| `<part>: faces and walls still changing after 20 rounds` | Stage 6 could not give the part's faces and walls the same vertices ([Working Principle](Working-Principle.md#62-how-a-part-becomes-a-closed-solid)). The part may be open; the Verifier then says so. |
| `<part>: pinch points left after 10 rounds of cutting` (or `pinch edges between two heights left ...`) | Two pieces of the part still touch at a point or along an edge after the cut-out disc grew to 512 times `Geometry.PINCH_POINT_OPENING_MM`. The part may be open there. |
| `step: <part>: N edges are not shared by two faces (the solid is open there)` | The STEP writer found the part open. It is still written, and a CAD tool will report free edges on it. |
| `step: no part to write; STEP skipped` | No part has its role in `Run.STEP_WRITE_ROLES`, or none of those parts has a solid, so no `<board>.step` is written. |

Only with `Run.BUILD_WITH_KERNELS = True`, the older path that builds the solids with Manifold and
the STEP file with OpenCascade:

| Message in `notes` | Meaning |
|---|---|
| `<part>: note: boolean union unavailable (...); pieces left touching` | A part could not be unioned; its pieces are concatenated. The Verifier may then report it as not closed. |
| `step: fuse failed for <part> (...); written as a compound` | In the STEP file that part is touching solids instead of one body. |
| `step: cadquery is not installed (pip install cadquery); STEP skipped` | Only when `kese.pipeline.generate` is called directly (as the regression suite does). From `run_KESE.py`, asking for STEP without `cadquery` stops before anything runs with `missing Python package(s): cadquery`. |

## 17.2 What `report.txt` Counts

### 17.2.1 Read

Tracks and arc tracks per layer, zone fills per layer, graphics and footprint graphics per layer,
text per layer, pads, pad mask openings per side, the mask openings of tracks, arc tracks and
drawings the mask leaves bare (KiCad 9 and later) per side, non-plated holes, through vias, blind/buried
vias, footprints, outline shapes on `Edge.Cuts`, via rings removed on unconnected layers,
castellated holes, the edge plating band and its net, text in a TrueType face drawn with the
stroke font.

### 17.2.2 Skipped

| Entry | Why |
|---|---|
| `3D component models (bare board only)` | Footprint `(model ...)` files are not loaded; KESE models the bare board. |
| `zones with no fill (unfilled - press B in KiCad and save)` | No fill polygons in the file. |
| `keepout / rule areas (no copper by design)` | Rule areas never carry copper; listed for completeness. |
| `<item> on <layer> (not a physical layer)` | Graphics on fab, courtyard, paste, user and comment layers, which are not part of the board (text there is left out without a count). |
| `gr_text_box / fp_text_box / dimension on <layer> (not modelled)` | Text boxes and dimensions on copper, mask or silkscreen layers are counted here and not rendered; on other layers, where dimensions usually sit, they are left out without a count. |
| `image / target / group / generated / table / point / grid_item / drill_chart / drill_map items` | Not physical (a point is KiCad 10's snap point; grid items, drill charts and drill maps come from KiCad's development version). For a group or a generated item (such as a length-tuning pattern) only the record is skipped; the items in it are read as usual. |
| `barcode items` | KiCad 10 barcodes (QR codes and others), on the board or in a footprint. The file holds only the barcode's text and size, which KiCad turns into a pattern when it plots, so KESE leaves them out, even on copper or silkscreen. |
| `pads of shape <shape>` | A pad shape KESE does not know. |
| `<kind> items (unknown to KESE)` | An item at the top level of the file, or a footprint drawing (`fp_...`), of a kind KESE does not read; also a warning. |
| `pads with a padstack` / `vias with a padstack (the front shape is used on every layer)` | KiCad 9 and later: another shape on the inner layers or on the back, not modelled; also a warning. |
| `backdrills` / `tertiary drills of pads` / `of vias (the hole is plated through its whole span)` | KiCad 10: the drill that removes the plating from part of the hole, not modelled; also a warning. |
| `counterbores` / `countersinks of pads` / `of vias (not cut)` | KiCad 10's post-machining of a hole's end, not modelled; also a warning. |
| `covered` / `plugged` / `capped` / `filled vias (the ... is not modelled)` | KiCad 10's via protection, set on the via or, when it does not say, in the board setup; the hole stays open. Also a warning. |
| `TrueType text on <layer> (DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT is False)` | Skipped by the setting. |
| `castellation plating (CASTELLATION is 'off')` | The holes stay bare. The same line appears with `CASTELLATION = "file"` when the stack-up lacks `(castellated_pads yes)`. |

## 17.3 The Verifier

`kese/s8_verify/`, run with `--verify` or `Run.VERIFY = True`. It checks the meshes that
GLB, STL and OBJ are written from and, in simulation mode, the faces that the STEP file is
written from, not the input. The STEP file itself is not read back at run time (the regression
suite reads it back with OCP).

| Mode | Check | Pass condition |
|---|---|---|
| simulation | every part is a closed, consistently wound solid; its volume is printed in mm³ | `closed=True winding=True` for every part |
| simulation | no two parts share material: every slice of every part (a flat region between two heights, what the faces are cut from; with `Run.BUILD_WITH_KERNELS = True` every prism) against every slice of every other part | `none`: no two slices of different parts overlap in height while their regions share an area wider than two grid steps, 0.2 µm (`none` on every board of the regression suite) |
| simulation | every part's volume found four ways (`volumes.py`): from its flat faces, from its slices, from its mesh and from the prisms it was built from. Not with `Run.BUILD_WITH_KERNELS = True` | `closed=True whole=True` for every part: the faces and the mesh within 1 part in 10⁷ of the slices, the prisms within that plus 0.001 mm³ (what opening pinch points may take) |
| visual | the skin is one outer surface: along every ray that hits the model the faces take turns, one going into the material and the next out of it (two faces on most rays; four where a ray crosses a hollow open to the air, such as the bore of a buried via under stacked micro vias) | the line `visible surfaces per vertical ray: faces met {2: ...}; rays where in and out do not alternate: 0` ends in 0 |
| both, when a GLB was written | the GLB through the Khronos glTF validator, when the `gltf_validator` command-line tool is on the PATH | not a pass condition: the validator's last line is only reported; otherwise `gltf_validator not on PATH: glTF validation skipped`; with no GLB in the run the line is absent |

> [!NOTE]
> The visual check casts its rays along the output's −Z axis, so it assumes `Run.ORIENTATION = "upright"`.
> With `"flat"` the rays run along the board plane, and the visual check reports FAIL on a
> correct skin.

Example tail of a `report.txt` (`Input/rf_module.kicad_pcb` in simulation mode, `...` where
lines are left out):

```text
Verifier: PASS
  Board_dielectric 1                   closed=True winding=True volume=537.9918 mm3
  Board_dielectric 2                   closed=True winding=True volume=2939.6554 mm3
  Board_dielectric 3                   closed=True winding=True volume=545.0504 mm3
  Copper_+3V3                          closed=True winding=True volume=30.0643 mm3
  ...
  Copper_GND                           closed=True winding=True volume=233.5935 mm3
  ...
  Top Solder Mask                      closed=True winding=True volume=22.5245 mm3
  Bottom Solder Mask                   closed=True winding=True volume=23.5600 mm3
  Top Silkscreen                       closed=True winding=True volume=1.2008 mm3
  Bottom Silkscreen                    closed=True winding=True volume=0.5142 mm3
  overlap between different parts, every slice against the others: none
  gltf_validator not on PATH: glTF validation skipped
  Board_dielectric 1                   volume from faces 537.991825 mesh 537.991825 slices 537.991825 prisms 537.991825 mm3 closed=True whole=True
  ...
  Copper_GND                           volume from faces 233.593533 mesh 233.593533 slices 233.593533 prisms 233.593666 mm3 closed=True whole=True
  ...
  Bottom Silkscreen                    volume from faces 0.514160 mesh 0.514160 slices 0.514160 prisms 0.514160 mm3 closed=True whole=True
```

The prisms of `Copper_GND` hold 0.00013 mm³ more than its faces, within the 0.001 mm³ the
check allows them.

The volume from the faces needs nothing but the faces: walls are vertical and add nothing, so a
closed surface holds the sum of height times signed area over its flat faces
(`Boundary.volume()`):

```python
v = 0
for z, region, up in boundary.flats:
    v += (1 if up else -1) * z * region.area
```

The overlap test (`overlap.py`) works on what the solids are made of. Between two neighbouring
heights a part is one flat region, a slice ([Working Principle](Working-Principle.md#62-how-a-part-becomes-a-closed-solid)),
so two parts share material exactly where a slice of one and a slice of the other overlap in
height and their regions share an area. Every polygon of every slice is shrunk by one grid step
first: parts that only touch, along an edge or across the grid step that sharing vertices may
bend an edge by, then no longer meet. An R-tree finds the polygons whose boxes meet; of those
from different parts that overlap in height, the shrunk polygons are tested, and every pair that
still meets is reported with the volume the two parts share:

```math
V_{AB} = \operatorname{area}\left( R_A \cap R_B \right) \cdot h_{AB}, \qquad h_{AB} = \min\left( z^{A}_{1}, z^{B}_{1} \right) - \max\left( z^{A}_{0}, z^{B}_{0} \right) \qquad (17.1)
```

```math
\text{PASS} \iff \text{every part closed, consistently wound and whole, and no pair with } \ h_{AB} > 10^{-9} \text{ mm and } \left( R_A \ominus g \right) \cap \left( R_B \ominus g \right) \neq \varnothing \qquad (17.2)
```

| Symbol | Meaning |
|---|---|
| $`R_A, z^{A}_{0}, z^{A}_{1}`$ | one polygon of a slice of part $`A`$, and the slice's two heights, in mm |
| $`h_{AB}`$ | how far the two slices overlap in height; heights are told apart to $`10^{-9}`$ mm, a picometre |
| $`g`$ | one grid step, `Geometry.SNAP_GRID_MM` (0.1 µm) |
| $`R \ominus g`$ | the polygon shrunk by $`g`$ all round |
| $`V_{AB}`$ | the material the two parts share there, in mm³; the line gives the biggest |

So an overlap 0.3 µm deep is found, while two parts that only touch, or meet across less than two
grid steps, pass. A sliver 20 µm wide and 2 mm long hidden in the laminate is found wherever it
lies; 3,000 random vertical rays, the test this one replaced, found 6 of 20 such slivers.

A `closed=False`, `winding=False` or `whole=False` line names the part. An open solid means its
faces and walls do not meet on the same edges (see the `faces and walls still changing` and
`pinch points left` notes, or with kernels the `boolean union unavailable` note); `whole=False`
means the solid holds more or less material than the prisms it was built from. An overlap line
other than `none` means two parts share material; it names the two parts and the heights of the
biggest overlap, and how many places there are. All of these are bugs worth reporting with the
board file.

## 17.4 The Regression Suite

`tests/test_boards.py` runs every board in `tests/boards/`, `featureTest/` and `Input/` through
every output, with the Verifier: simulation mode written as GLB and STEP, visual mode as GLB. It
compares every part's volume with `tests/baseline.json`:

```bash
python -m pytest tests                 # or:  python tests/test_boards.py
python tests/test_boards.py --accept   # re-record the baseline after an intended geometry change
python tests/test_boards.py --add      # record only the boards the baseline does not have yet
```

A board fails when the Verifier fails (an open or wrongly wound part or an overlap in simulation
mode, faces that do not take turns in visual mode), when a part's volume moved from the recorded
baseline by more than

```math
\left| V - V_0 \right| > 10^{-3} \cdot \max\left( |V_0|,\ 10^{-9} \right) \qquad (17.3)
```

where $`V`$ is the part's volume now and $`V_0`$ the baseline, both in mm³, when a part disappeared
or a new one appeared, or (when `cadquery` is installed) when the STEP file has an invalid solid or
a free edge, checked by reading it back with OCP. In visual mode the "volume" is the signed volume
of an open surface: it means nothing on its own, but it moves when the skin does.

Reading a STEP file back takes longer than writing it: about 3.5 minutes for the 65 MB file of
`16b_edge_plating_border`, over a minute to turn the file into shapes and two more to check the
solids. So
`python tests/test_boards.py` reads the STEP files back in two background processes
(`AUDITORS` in `tests/test_boards.py`, `tests/step_audit.py`) while it exports the next boards,
and prints a board's line once its file is checked, in the order the boards ran, with the time the
read-back took (`STEP read back in 3.4 s`). Under `pytest` every board is checked in turn.

The test boards in `tests/boards/` cover:

- `one_layer`: a single-sided board with silkscreen text (it declares `F.Cu` and `B.Cu`, with
  tracks on `F.Cu` only);
- `six_layer`: a full stack-up (prepreg / core, a prepreg of two sub-layers, 17.5 µm inner foil,
  black mask, blind, buried and micro vias, a "remove unused layers" via, zone fills);
- `synthetic`: a two-layer board with one core and 70 µm copper, exercising an outline of lines and
  an arc with a circular cut-out, a blue top mask with a drawn opening and pad mask margins, an arc
  track, a via tented by the plot setting (`viasonmask false`), a zone fill, an oval drill, an NPTH,
  and items skipped on purpose (a 3D model, an `F.Fab` line).

`python -m pytest tests` also runs `tests/test_layout.py`, which checks the code rather than the
boards: which folders of `kese/` may import which, one `run()` per stage, no file over 200 lines,
lowercase names, and no code outside `Generator/`.
[`CONTRIBUTING.md`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/main/CONTRIBUTING.md)
explains these rules. It only reads the source, so it takes about a second
(`python tests/test_layout.py`). The same command runs `tests/test_colors.py`, which reads named,
user-defined and unknown stack-up colours as [Colorizing](Colorizing.md#122-colours-from-the-stack-up)
describes, in a moment (`python tests/test_colors.py`); `tests/test_text_layout.py`, which lays out
sixteen texts (each justification, two lines, two lines with a line spacing KiCad does not plot, tabs,
an angle, italic, bold, a wide font, an escaped quote, mirrored text on the back and the reference of
a turned footprint) and finds each where KiCad 7.0.11 plots it, to 5 µm, in about three seconds
(`python tests/test_text_layout.py`); and four STEP tests, each also on its own
(`python tests/<name>.py`):

| Test | Path | What it checks |
|---|---|---|
| `test_step_native.py` | the default writer (`kese/s7_write/step.py`) | a box with a through hole beside a second box, written from their faces and read back by OpenCascade as two valid solids with no free edge, the right faces and the right volume; names with a quote and letters outside ASCII come back as they went in. Needs OCP, which `cadquery` installs; takes a second |
| `test_step_file.py` | `Run.BUILD_WITH_KERNELS = True` (`step_file.py`) | four small parts, with a `#`, a `;`, a quote and letters outside ASCII in their names, written part by part and read back against the file OpenCascade writes for the same parts at once: the same names, placements, colours, solids and volumes. Needs `cadquery`; takes a second |
| `test_step_kernel.py` | `Run.BUILD_WITH_KERNELS = True` (`step_cadquery.py`) | `tests/boards/one_layer` written in metres and in millimetres: each file declares the units it is written in, so OpenCascade reads both at the same size, and a STEP file read afterwards in the same process still comes in millimetres. Needs `cadquery`; takes ten seconds |
| `test_step_arcs.py` | `Run.BUILD_WITH_KERNELS = True` (`step_arcs.py`, the true circles written back into STEP) | outlines where the arc of a faceted circle would cross an edge of its own ring, a hole, another polygon or another arc keep those vertices straight, while the same arcs a little further away are kept, and so are an arc that the outline doubles back along or leaves along its tangent and the arc of a half round; with `cadquery`, OpenCascade finds the faces and solids made from them valid, and those with the crossing arcs invalid. Takes a few seconds |

## 17.5 Inputs KESE Refuses Or Changes

| Situation | What happens |
|---|---|
| Copper of two nets overlapping in the file | The first net resolved keeps the shared area so the solids stay disjoint. |
| Copper of another net inside the edge plating band | Moved to the edge net; `report.txt` lists it. |
| Visual mode with `stl` or `step` | Error. |
| A `--set` name that does not exist | Error before the run. |
| Zones without stored fills | Ignored with a warning. |

| Previous | Next |
|:---|---:|
| [Parameter Reference](Parameter-Reference.md) | [Material Properties](Material-Properties.md) |
