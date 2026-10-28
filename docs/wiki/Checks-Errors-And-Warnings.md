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
| `image / target / group / generated / table / point items` | Not physical (a point is KiCad 10's snap point). For a group or a generated item (such as a length-tuning pattern) only the record is skipped; the items in it are read as usual. |
| `barcode items` | KiCad 10 barcodes (QR codes and others), on the board or in a footprint. The file holds only the barcode's text and size, which KiCad turns into a pattern when it plots, so KESE leaves them out, even on copper or silkscreen. |
| `pads of shape <shape>` | A pad shape KESE does not know. |
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
| simulation | no two parts overlap: 3,000 random vertical rays through the model, the intervals each part occupies along every ray | worst overlap below 0.1 µm (`worst 0.000 um` on the example boards) |
| simulation | every part's volume found four ways (`volumes.py`): from its flat faces, from its slices, from its mesh and from the prisms it was built from. Not with `Run.BUILD_WITH_KERNELS = True` | `closed=True whole=True` for every part: the faces and the mesh within 1 part in 10⁷ of the slices, the prisms within that plus 0.001 mm³ (what opening pinch points may take) |
| visual | the skin is one outer surface: along every ray that hits the model the faces take turns, one going into the material and the next out of it (two faces on most rays; four where a ray crosses a hollow open to the air, such as the bore of a buried via under stacked micro vias) | the line `visible surfaces per vertical ray: faces met {2: ...}; rays where in and out do not alternate: 0` ends in 0 |
| both, when a GLB was written | the GLB through the Khronos glTF validator, when the `gltf_validator` command-line tool is on the PATH | not a pass condition: the validator's last line is only reported; otherwise `gltf_validator not on PATH: glTF validation skipped`; with no GLB in the run the line is absent |

> [!NOTE]
> The ray checks cast along the output's −Z axis, so they assume `Run.ORIENTATION = "upright"`.
> With `"flat"` the rays run along the board plane, and the visual check reports FAIL on a
> correct skin.

Example tail of a `report.txt` (`Input/Stator.kicad_pcb` in simulation mode):

```text
Verifier: PASS
  Board_dielectric 1                   closed=True winding=True volume=2530.6188 mm3
  Copper_1                             closed=True winding=True volume=2.1699 mm3
  Copper_2                             closed=True winding=True volume=2.1699 mm3
  Copper_TX                            closed=True winding=True volume=3.1674 mm3
  Top Solder Mask                      closed=True winding=True volume=16.0024 mm3
  Bottom Solder Mask                   closed=True winding=True volume=16.2848 mm3
  overlap between different parts along 3000 vertical rays: worst 0.000 um
  gltf_validator not on PATH: glTF validation skipped
  Board_dielectric 1                   volume from faces 2530.618759 mesh 2530.618759 slices 2530.618759 prisms 2530.618759 mm3 closed=True whole=True
  Copper_1                             volume from faces 2.169868 mesh 2.169868 slices 2.169868 prisms 2.169868 mm3 closed=True whole=True
  Copper_2                             volume from faces 2.169863 mesh 2.169863 slices 2.169863 prisms 2.169863 mm3 closed=True whole=True
  Copper_TX                            volume from faces 3.167362 mesh 3.167362 slices 3.167362 prisms 3.167362 mm3 closed=True whole=True
  Top Solder Mask                      volume from faces 16.002391 mesh 16.002391 slices 16.002391 prisms 16.002391 mm3 closed=True whole=True
  Bottom Solder Mask                   volume from faces 16.284824 mesh 16.284824 slices 16.284824 prisms 16.284824 mm3 closed=True whole=True
```

The volume from the faces needs nothing but the faces: walls are vertical and add nothing, so a
closed surface holds the sum of height times signed area over its flat faces
(`Boundary.volume()`):

```python
v = 0
for z, region, up in boundary.flats:
    v += (1 if up else -1) * z * region.area
```

The overlap test works on the vertical rays. For each ray and each part, the pairs of hits give
the z intervals the part occupies along that ray; for every two different parts the overlap of
their intervals is measured, and the worst is reported:

```math
\Omega = \max\left( 0, \ \max_{\text{rays}} \ \max_{A \neq B} \ \left( \min\left( z^{A}_{\mathrm{top}}, z^{B}_{\mathrm{top}} \right) - \max\left( z^{A}_{\mathrm{bot}}, z^{B}_{\mathrm{bot}} \right) \right) \right) \qquad (17.1)
```

```math
\text{PASS} \iff \text{every part closed, consistently wound and whole, and } \ \Omega < 10^{-4} \text{ mm} \qquad (17.2)
```

| Symbol | Meaning |
|---|---|
| $`\Omega`$ | worst overlap, reported in µm |
| $`z^{A}_{\mathrm{top}}, z^{A}_{\mathrm{bot}}`$ | one z interval of part $`A`$ along a ray |
| rays | 3,000 vertical rays at random (x, y) inside the model's bounding box, the same every run (fixed seed) |

Parts that do not meet, or only touch, give 0.

A `closed=False`, `winding=False` or `whole=False` line names the part. An open solid means its
faces and walls do not meet on the same edges (see the `faces and walls still changing` and
`pinch points left` notes, or with kernels the `boolean union unavailable` note); `whole=False`
means the solid holds more or less material than the prisms it was built from. An overlap above
0.1 µm means two parts share volume; that line gives only the worst value, not the parts. All of
these are bugs worth reporting with the board file.

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
lowercase names, and no code outside `Generator/`. It only reads the source, so it takes about a second
(`python tests/test_layout.py`). The same command runs three STEP tests, each also on its own
(`python tests/<name>.py`):

| Test | Path | What it checks |
|---|---|---|
| `test_step_native.py` | the default writer (`kese/s7_write/step.py`) | a box with a through hole beside a second box, written from their faces and read back by OpenCascade as two valid solids with no free edge, the right faces and the right volume; names with a quote and letters outside ASCII come back as they went in. Needs OCP, which `cadquery` installs; takes a second |
| `test_step_file.py` | `Run.BUILD_WITH_KERNELS = True` (`step_file.py`) | four small parts, with a `#`, a `;`, a quote and letters outside ASCII in their names, written part by part and read back against the file OpenCascade writes for the same parts at once: the same names, placements, colours, solids and volumes. Needs `cadquery`; takes a second |
| `test_step_arcs.py` | `Run.BUILD_WITH_KERNELS = True` (`step_arcs.py`, the true circles written back into STEP) | outlines where the arc of a faceted circle would cross an edge of its own ring, a hole, another polygon or another arc keep those vertices straight, while the same arcs a little further away are kept, and so are an arc that the outline doubles back along or leaves along its tangent and the arc of a half round; with `cadquery`, OpenCascade finds the faces and solids made from them valid, and those with the crossing arcs invalid. Takes a few seconds |
[`CONTRIBUTING.md`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/main/CONTRIBUTING.md)
explains the rules.

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
