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
| `<file>: the file ends with N parentheses still open: it is cut short (an incomplete download or copy?)` | The file stops in the middle; KiCad refuses it too. Save or download it again. |
| `<file>: copper layers ['F.Cu', 'B.Cu'] are not declared` | Both outer copper layers must exist. |
| `MODE must be 'simulation' or 'visual', not ...` | A typo in `Run.MODE` (or `--set Run.MODE=...`). A typo in `--mode` is caught earlier by the command line: `argument --mode: invalid choice`, exit code 2. |
| `unknown FILE_FORMAT entries [...]` | Only `glb`, `stl`, `obj`, `step`. One format may be given as a list or as a single word (`--set Run.FILE_FORMAT=step`). |
| `<Module>.<NAME> must be '...' or '...', not ...` | A setting that takes one of a few words (those whose range [Parameter Reference](Parameter-Reference.md) gives as words with `/` between them, such as `Run.UNITS` or `Copper.COPPER_GROUPING`) has another value. The run stops before reading the board. |
| `Run.WORKERS must be a whole number, 0 or more (0: one per processor thread), not ...` | `0` uses every processor thread the run may use; a negative or fractional value means nothing. |
| `Geometry.PINCH_CUT_ROUNDS must be a whole number, 1 or more, not ...` | At least one try at opening a pinch point is needed: with none, every region checked would be noted as still pinched. |
| `visual mode is a surface, not solids: FILE_FORMAT may only contain glb / obj` | STL and STEP need closed solids; use simulation mode. |
| `no Edge.Cuts outline and OUTLINE_FALLBACK is 'error'` | Draw a closed outline, or set `Board.OUTLINE_FALLBACK = "copper_hull"`. |
| `missing Python package(s): ...` | Printed before anything runs, with the `pip install` line to use. |
| `Python package(s) too old: shapely 2.0.7 (2.1 or newer)` | shapely 2.0 lacks the constrained Delaunay triangulation the faces are cut with; printed before anything runs, with the `pip install --upgrade` line to use. |
| `--set <item>: parameters/<module>.py has no parameter <NAME> (did you mean <NAME>?)` | A `--set` with a misspelt name, or one in small letters; the closest name is given where there is one. Like every `--set` mistake below, it is printed by the command line before anything runs, exit code 2. |
| `--set <item>: there is no parameter module <Module> (did you mean <Module>?); the modules are Run, Board, ...` | A misspelt module, or one in small letters (`copper` for `Copper`). |
| `--set <item>: <item> is not Module.NAME (did you mean Run.WORKERS?)` | A name without its module, or without a name after the `.`. Where the name is in one module only, that module is given. |
| `--set <item>: give it a value, as in <item>=value` | A `--set` without `=`. |
| `no boards given and none found in Input/` | Put a board in `Input/` or give a path. |

### 17.1.2 Warnings

| Message | Meaning |
|---|---|
| `file has no (version ...): read as format 20201115, as KiCad does` | Best-effort read, by KiCad's own rule for such files. |
| `file format N is outside the tested range 3-20260206; proceeding best-effort` | Older than the 2013 builds before KiCad 4 or newer than KiCad 10 (`Run.KICAD_VERSION_MIN`, `Run.KICAD_VERSION_MAX`). |
| `N copper layers: more than the 8 this project has been tested with` | The layers are still modelled. |
| `layers named by the user or in an old language, read as KiCad reads them: TOP = F.Cu, ...` | Copper layers with names other than `F.Cu`, `B.Cu` and `In<n>.Cu` (KiCad 3 to 5 let the user rename them; KiCad 3 also wrote Italian, Polish and French names such as `Contorno.scheda`). Each is read as KiCad reads it: copper layers by their place in the list (first = `F.Cu`, last = `B.Cu`, the ones between `In1.Cu`, `In2.Cu`, ...), the old names by KiCad's own table. |
| `N copper zone(s) have no fill stored in the file and are ignored (fill the zones in KiCad, press B, and save; see parameters/copper.py)` | Fill the zones in KiCad (press **B**) and save. Until then those zones produce no copper. |
| `N via(s) name a copper layer the board does not have and are left out` | A damaged file: a via ends on a copper layer that the board's `(layers ...)` list does not have. The via is missing from the model and counted under `skipped` in `report.txt`; check it in KiCad. |
| `Edge.Cuts lines/arcs do not form a closed outline` | The outline could not be polygonized; closed shapes on `Edge.Cuts` are still used. |
| `no Edge.Cuts outline; using the copper's convex hull + 1.0 mm` | The fallback outline. |
| `DIELECTRIC_SPLIT=... unknown, using 'even'` | Only `"even"` is implemented. |
| `not modelled, see 'skipped' in report.txt: backdrills of vias, filled vias, ...` | The board has holes that KiCad 10 backdrills, post-machines, covers, plugs, caps or fills. KESE models the hole plated through its whole span and open; `skipped` gives the counts. |
| `left out, of a kind KESE does not know: fp_foo (2), ...` | Items of a kind KESE does not read, such as a drawing kind newer than this version of KESE. They are missing from the model. |
| `the stack-up colour '<value>' of <layer> is neither a colour name of parameters/color.py nor #RRGGBBAA; its parts keep their MATERIALS colour` | A mask or silkscreen colour KESE cannot read keeps KESE's colour. Add the name to the tables in `parameters/color.py` ([Colorizing](Colorizing.md#122-colours-from-the-stack-up)). |

### 17.1.3 Notes Worth Knowing

| Message in `notes` | Meaning |
|---|---|
| `note: Edge.Cuts line ends up to D mm apart joined (Board.OUTLINE_LINE_SNAP_MM = S mm)` | The outline's lines had small gaps between their ends; they were closed as KiCad closes them (KiCad joins ends up to 0.01 mm apart, the default of `Board.OUTLINE_LINE_SNAP_MM`), so the board shape is the one KiCad shows. |
| `<part>: faces and walls still changing after 20 rounds` | Stage 6 could not give the part's faces and walls the same vertices ([Working Principle](Working-Principle.md#62-how-a-part-becomes-a-closed-solid)). The part may be open; the Verifier then says so. |
| `<part>: pinch points left after 10 rounds of cutting` (or `pinch edges between two heights left ...`) | Two pieces of the part still touch at a point or along an edge after the cut-out disc grew to 512 times `Geometry.PINCH_POINT_OPENING_MM`. The part may be open there. |
| `<part>: slices still sharing new vertices after 20 rounds` | Stage 6 gave the slices that meet at a height each other's vertices 20 times and they still changed. The part may be open; the Verifier then says so. |
| `plated holes cross the board edge but the stackup has no (castellated_pads yes); set Copper.CASTELLATION = 'auto' to plate them` | With `Copper.CASTELLATION = "file"`, plated holes cut by the edge are left bare because the stack-up does not say they are castellated. |
| `edge plating: copper of net '<net>' inside the edge band moved to net '<edge net>' on N layer(s)` | Copper of another net reached into the plated edge band; it now belongs to the edge's net (see 17.5). |
| `worker processes failed (...); the N parts left are built in this process, one after another` (in visual mode `sliced`; after a lost worker, ending `(most often a lack of memory: Run.WORKERS = 1 uses less)`) | Stage 6 could not start its worker processes (`Run.WORKERS`), or lost one: the system stopped it, most often for lack of memory, or it ran out of memory (`MemoryError`). The parts the workers did not build (in visual mode, slice) are built in the main process instead, so the files are the same, only slower. An error in a part itself is not caught here: it stops the run at once, with its traceback. With little memory, `--set Run.WORKERS=1` builds everything in one process from the start. |
| `step: <part>: N edges are not shared by two faces (the solid is open there)` | The STEP writer found the part open. It is still written, and a CAD tool will report free edges on it. |
| `step: <part>: written without arcs (...)` | With `Run.STEP_EXACT_ARCS`, finding the part's arcs failed (a bug: please report it with the board). The part is written with flat faces only, as with the parameter off; the rest of the file keeps its arcs. |
| `step: no part has a solid; STEP skipped` | None of the parts has a solid, so no `<board>.step` is written. |
| `FINISH ERROR: Finish.FINISH_TYPE = "file" but no finish was found in the KiCad file ...` | `FINISH_TYPE = "file"` and the board has no stack-up or its Copper finish is empty; also `FINISH ERROR: the KiCad file's finish '...' is not one KESE knows` and `FINISH ERROR: Finish.FINISH_TYPE = '...' is not a finish KESE knows`. Change `Finish.FINISH_TYPE`, or set the finish in KiCad (Board Setup > Physical Stackup > Copper finish). |
| `nothing to build: Board.BOARD_ENABLED, Copper.COPPER_ENABLED, ... are all False` | Every part switch is off, so there is nothing to write; the run stops before reading the board. |

## 17.2 What `report.txt` Counts

### 17.2.1 Read

Tracks and arc tracks per layer, zone fills per layer, graphics and footprint graphics per layer,
text per layer, pads, pad mask openings per side, the mask openings of tracks, arc tracks and
drawings the mask leaves bare (KiCad 9 and later) per side, non-plated holes, through vias, blind/buried
vias, footprints, outline shapes on `Edge.Cuts`, via rings removed on unconnected layers,
castellated holes, the edge plating band and its net, text in a TrueType face from its render cache or drawn with the
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
| `pads with a padstack (a shape per layer)` / `vias with a padstack (a shape per layer)` (under found) | KiCad 9 and later: another shape on the inner layers or on the back; each copper layer gets its own shape, and the back mask opening follows the back shape. |
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
| simulation | no two parts share material: every slice of every part (a flat region between two heights, what the faces are cut from) against every slice of every other part | `none`: no two slices of different parts overlap in height while their regions share an area wider than two grid steps, 0.2 µm (`none` on every board of the regression suite) |
| simulation | every part's volume found four ways (`volumes.py`): from its flat faces, from its slices, from its mesh and from the prisms it was built from | `closed=True whole=True` for every part: the faces and the mesh within 1 part in 10⁷ of the slices, the prisms within that plus 0.001 mm³ (what opening pinch points may take) |
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
`pinch points left` notes); `whole=False`
means the solid holds more or less material than the prisms it was built from. An overlap line
other than `none` means two parts share material; it names the two parts and the heights of the
biggest overlap (of overlaps as big, the first by part name, so the line is the same however many
worker processes ran), and how many places there are. All of these are bugs worth reporting with the
board file.

## 17.4 The Regression Suite

`tests/test_boards.py` runs every board in `tests/boards/`, `featureTest/` and `Input/` (a board of
`Input/` that `featureTest/` holds too, byte for byte, only once) through every output, with the Verifier: simulation mode written as GLB and STEP, visual mode as GLB. It
compares every part's volume with `tests/baseline.json`:

```bash
python -m pytest tests                 # or:  python tests/test_boards.py
python tests/test_boards.py --accept   # re-record the baseline after an intended geometry change
python tests/test_boards.py --add      # record only the boards the baseline does not have yet
python tests/test_boards.py 21_rf_module six_layer   # only these boards (file names, no .kicad_pcb)
python tests/test_boards.py --faceted  # the STEP files with flat faces only (Run.STEP_EXACT_ARCS = False)
python tests/test_boards.py --healed   # read the STEP files back with OpenCascade's healing (slower)
```

Any other option stops the suite with `unknown option: ...`, so a misspelt `--heald` does not run
the plain suite instead, and a board name it does not have stops it with `no such board: ...`. Named
boards combine with the options: `--accept 18_finishes` re-records that board alone. `pytest` itself
is installed with `python -m pip install pytest`.

A board fails when the Verifier fails (an open or wrongly wound part or an overlap in simulation
mode, faces that do not take turns in visual mode), when a part's volume moved from the recorded
baseline by more than

```math
\left| V - V_0 \right| > 10^{-3} \cdot \max\left( |V_0|,\ 10^{-9} \right) \qquad (17.3)
```

where $`V`$ is the part's volume now and $`V_0`$ the baseline, both in mm³, when a part disappeared
or a new one appeared, or (when OCP, `cadquery-ocp`, is installed) when the STEP file has an invalid solid or
a free edge, checked by reading it back with OCP. In visual mode the "volume" is the signed volume
of an open surface: it means nothing on its own, but it moves when the skin does.

Reading a STEP file back takes longer than writing it. The suite reads it as written, without
OpenCascade's shape healing, which takes most of the reading time and would mend a fault rather than
report it. Before the check it works out only what any reader must work out for itself: the curve of
each edge in the parameters of each of its faces (KESE writes none, as KiCad does not), and on a
cylinder an edge's curve moved by a whole turn where it came out a turn off; the points and curves
in the file stay as written (`tests/step_audit.py`). That is about 2.5 times quicker than reading
with the healing (`python tests/test_boards.py --healed`, the check before): for the 54 MB file of
`16b_edge_plating_border`, 39 s against 97 s, its parts read one after another. On every test board
the two give the same verdict; on files broken on purpose (a face left out, a vertex moved, a face
turned over, a circle's radius changed), only the read without the healing finds every fault.

OpenCascade reads a file in one thread and holds about ten times its size in memory, and its check
of a face compares the face's edges and vertices with one another, so its time grows with the
square of the face's edges: one face of `22_hdi_module` with 8,270 edges takes 18 s on its own. So
the suite reads a file back one part at a time (`tests/step_audit.py`). In a file KESE wrote, each
part's entities stand on their own; only the assembly's, `#1` to `#24` at the end, are shared. Each
part is copied into a small STEP file of its own, with the assembly cut down to that part, and read
back in a process of its own, the biggest parts first. A part's file that does not read is an
error, and a solid that does not come back as a solid counts as invalid (OCP 7.9 makes a shell with
a face left out a shell, where 7.8 makes it an invalid solid), so a part cut in the wrong place
cannot pass as clean. A file laid out otherwise, written by another program or with its line ends
changed, is read whole. A solid is checked on its own either way, so the counts are those of
reading the whole file: on every test board the invalid solids, free edges,
number of solids and their volume come out the same both ways, and so does a file with a fault in
it. On a 4-core machine:

| STEP file (simulation, as the suite writes it) | Size | Read whole | Part by part, 4 processes |
|---|---|---|---|
| `16b_edge_plating_border` | 54 MB | 55 s | 14 s |
| `22_hdi_module` | 71 MB | 107 s | 56 s |
| `23_pcie_card` | 131 MB | 244 s | 141 s |
| `21_rf_module` | 174 MB | 263 s | 90 s |

A part is read in one piece, so the slowest part sets the shortest time however many processes
run: on `22_hdi_module` and `23_pcie_card`, the top solder mask, one solid with a face of 8,270 and
of 13,736 edges (54 s and 140 s of checking). Memory follows the parts being read rather than the
whole file: a 12-layer board's 1.25 GB file read with four processes takes 18 minutes and peaks at
7.7 GB, where read whole it held 13.4 GB and had not finished after 77 minutes. The Verifier, for
comparison, takes 1 to 4 s on the four boards above: the read-back is a test, not a step of the
run.

`python tests/test_boards.py` hands the parts to background processes, one per processor thread (at
most 61 on Windows) and at least two (`AUDITORS` in `tests/test_boards.py`), while it exports the
next boards, and prints a board's line once every part of its file is checked, in the order the
boards ran, with the number of parts and the time they took added up
(`STEP read back: 19 parts, 2.3 s`; they ran side by side, so it passed sooner). A part that does
not read fails the board (`STEP read-back failed: ...`). Without OCP, or with one that lacks what
the check uses (8.0), the line says so (`STEP not read back: ...`) and the board is not failed for
it. Under `pytest` every board is checked in turn, the parts of a file of 20 MB or more in processes
of their own, one per processor thread (at most 61 on Windows), and those of a smaller file one
after another; without a usable OCP it warns, and the STEP tests show as skipped, not as passed.

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
boards: which folders of `kese/` may import which, one `run()` per stage, no file over 200 lines
(`parse_kicad_version.py` 500), lowercase names, no KiCad version test outside
`kese/s1_read/parse_kicad_version.py`, and no code outside `Generator/`.
[`CONTRIBUTING.md`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/main/CONTRIBUTING.md)
explains these rules. It only reads the source, so it takes about a second
(`python tests/test_layout.py`). The same command runs `tests/test_colors.py`, which reads named,
user-defined and unknown stack-up colours as [Colorizing](Colorizing.md#122-colours-from-the-stack-up)
describes, in a moment (`python tests/test_colors.py`); `tests/test_text_layout.py`, which lays out
sixteen texts (each justification, two lines, two lines with a line spacing KiCad does not plot, tabs,
an angle, italic, bold, a wide font, an escaped quote, mirrored text on the back and the reference of
a turned footprint) and finds each where KiCad 7.0.11 plots it, to 5 µm, in about three seconds
(`python tests/test_text_layout.py`); `tests/test_kicad_version.py`, which checks the rules of each
KiCad version (release of each format number, copper layers by their place, the zero mask margin,
KiCad 4's text size, the text pen, segment-filled zones, the old overbar, markup) against what
KiCad's own parser does, without a board, in under a second; `tests/test_enabled.py`, which turns
each part switch off in turn (`BOARD_ENABLED`, `COPPER_ENABLED`, `FINISH_ENABLED`,
`SOLDER_MASK_ENABLED`, `SILKSCREEN_ENABLED`) and finds only that switch's parts gone and every other
part as it is with all of them on, and a run with all of them off refused, in about five seconds
(`python tests/test_enabled.py`);
`tests/test_bad_input.py`, which gives settings outside their values, misspelt `--set` items and a
damaged board file and finds an error before any work or a warning, not a Python error, in about
two seconds (`python tests/test_bad_input.py`); `tests/test_parallel.py`, which finds a thread's
own copies of shapes to be the same shapes, each part on its grid, made only where GEOS needs them,
and threads working on their own copies of one shape not crashing; finds threads taking turns with
one prepared copy of a slice's material, the test for hidden triangles letting go of its prepared
slices, a set of holes joined once when threads ask for it at once, and the memory threads freed
handed back; sends shapes through stage 6's worker processes and finds them back on
their grid (each part's too), of their type and with their SRID; and finds the run's settings in the
workers, the parts of a lost worker and of one out of memory built in the main process with the
note, an error in a part raised at once with the other workers stopped, a caller that stops early
not kept waiting, the workers first in line for Linux's out-of-memory killer, KESE run inside a
`multiprocessing.Pool`, a script without `if __name__ == "__main__":` not run again in each
worker, Ctrl-C ending the workers with one traceback, and the workers gone when the main process is
killed, in about ten seconds (`python tests/test_parallel.py`); and two STEP tests, also on their
own (`python tests/test_step_native.py`, `python tests/test_step_arcs.py`):

| Test | Path | What it checks |
|---|---|---|
| `test_step_native.py` | the STEP writer (`kese/s7_write/step.py`) and the suite's read-back (`tests/step_audit.py`) | a box with a through hole beside a second box, written from their faces and read back by OpenCascade as two valid solids with no free edge, the right faces and the right volume; names with a quote and letters outside ASCII come back as they went in. A file of three such parts, read back part by part, gives what the whole file gives, also with a face left out of the first part and of the last; a part cut in the wrong place does not pass as clean, and a file another program wrote, or one with other line ends, is read whole. Needs OCP (`python -m pip install "cadquery-ocp==7.8.1.1.post1"`), and is skipped without it; takes a few seconds |
| `test_step_arcs.py` | the true arcs of STEP files (`Run.STEP_EXACT_ARCS`; `kese/s7_write/step_arcs.py`, `step_curved.py`) | a run of vertices on one circle is written as an arc edge, and the walls on it as a cylinder, only where the arc cannot cross anything: circles and round ends become arcs, and the two arcs of an S-bend share only the vertex between them; an arc that would cross its own ring, or overlap another polygon's arc, stays straight, an outline may touch an arc where it joins it but not cross it, and an edge near the arc at another height leaves it be; a failure in the arcs writes the part with flat faces. With OCP every file is also read back: valid solids, no free edge, the volume of the true shape. Takes a few seconds |

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
