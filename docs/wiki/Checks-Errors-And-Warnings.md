# 17. Checks, Errors And Warnings

KESE reports in three places: the terminal while it runs, `report.txt` next to every output,
and the opt-in Verifier whose lines are appended to `report.txt`. Nothing is dropped silently:
every item the model leaves out is counted under `skipped` with the reason.

```bash
python run_KESE.py board.kicad_pcb --verify     # generate, then run the Verifier
python Tests/test_boards.py                     # the regression suite over every board
```

## 17.1 Levels

| Level | Meaning | What happens |
|---|---|---|
| Error | The file cannot be modelled, or the request is impossible. | Nothing is written for that board. With one board the traceback is shown; with several, `<board>: FAILED - <reason>` is printed and the run continues. Exit code 1. |
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
| `MODE must be 'simulation' or 'visual', not ...` | A typo in `Run.MODE` or `--mode`. |
| `unknown FILE_FORMAT entries [...]` | Only `glb`, `stl`, `obj`, `step`. |
| `visual mode is a surface, not solids: FILE_FORMAT may only contain glb / obj` | STL and STEP need closed solids; use simulation mode. |
| `no Edge.Cuts outline and OUTLINE_FALLBACK is 'error'` | Draw an outline, or set `Board.OUTLINE_FALLBACK = "copper_hull"`. |
| `missing Python package(s): ...` | Printed before anything runs, with the `pip install` line to use. |
| `<Module>_Parameters has no parameter <NAME>` | A `--set` with a misspelt name. |
| `no boards given and none found in Input/` | Put a board in `Input/` or give a path. |

### 17.1.2 Warnings

| Message | Meaning |
|---|---|
| `file has no (version ...): treated as legacy KiCad 5` | Best-effort read. |
| `file format N is outside the tested range 20211014-20260206; proceeding best-effort` | Older than KiCad 6 or newer than KiCad 10. |
| `N copper layers: more than the 6 this project has been tested with` | The layers are still modelled. |
| `N copper zone(s) have no fill stored in the file and are ignored` | Fill the zones in KiCad (press **B**) and save. Until then those zones produce no copper. |
| `Edge.Cuts lines/arcs do not form a closed outline` | The outline could not be polygonized; closed shapes on `Edge.Cuts` are still used. |
| `no Edge.Cuts outline; using the copper's convex hull + 1.0 mm` | The fallback outline. |
| `DIELECTRIC_SPLIT=... unknown, using 'even'` | Only `"even"` is implemented. |
| `step: cadquery is not installed (pip install cadquery); STEP skipped` | The other formats are written. |
| `step: fuse failed for <part> (...); written as a compound` | That part is touching solids instead of one body. |
| `note: boolean union unavailable (...); pieces left touching` | A part could not be unioned; its pieces are concatenated. The Verifier will report it as not closed. |

## 17.2 What `report.txt` Counts

### 17.2.1 Read

Tracks and arc tracks per layer, zone fills per layer, graphics and footprint graphics per layer,
text per layer, pads, pad mask openings per side, non-plated holes, through vias, blind/buried
vias, footprints, outline shapes on `Edge.Cuts`, via rings removed on unconnected layers,
castellated holes, the edge plating band and its net, text in a TrueType face drawn with the
stroke font.

### 17.2.2 Skipped

| Entry | Why |
|---|---|
| `3D component models (bare board only)` | Footprint `(model ...)` files are not loaded; KESE models the bare board. |
| `zones with no fill (unfilled - press B in KiCad and save)` | No fill polygons in the file. |
| `keepout / rule areas (no copper by design)` | Rule areas never carry copper; listed for completeness. |
| `<item> on <layer> (not a physical layer)` | Fab, courtyard, paste, user and comment layers are not part of the board. |
| `gr_text_box / fp_text_box / dimension on <layer> (not modelled)` | Text boxes and dimensions are not rendered. |
| `image / target / group / generated / table items` | Not physical. |
| `pads of shape <shape>` | A pad shape KESE does not know. |
| `TrueType text on <layer> (DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT is False)` | Skipped by the setting. |
| `castellation plating (CASTELLATION is 'off')` | The holes stay bare. |

## 17.3 The Verifier

`Generator/Verifier.py`, run with `--verify` or `Run.VERIFY = True`. It proves the written model,
not the input.

| Mode | Check | Pass condition |
|---|---|---|
| simulation | every part is a closed, consistently wound solid; its volume is printed in mm³ | `closed=True winding=True` for every part |
| simulation | no two parts overlap: 3,000 random vertical rays through the model, the intervals each part occupies along every ray | worst overlap below 0.1 µm (`worst 0.000 um` on the example boards) |
| visual | the skin is one visible surface: along every ray exactly one upward-facing and one downward-facing hit | `up {1: n} down {1: n}` |
| both | the GLB passes the Khronos glTF validator, when the `gltf_validator` command-line tool is on the PATH | the validator's last line; otherwise `gltf_validator not on PATH: glTF validation skipped` |

Example tail of a `report.txt`:

```text
Verifier: PASS
  Board_dielectric 1                   closed=True winding=True volume=2530.6188 mm3
  Copper_TX                            closed=True winding=True volume=3.1673 mm3
  Top Solder Mask                      closed=True winding=True volume=16.0024 mm3
  overlap between different parts along 3000 vertical rays: worst 0.000 um
  gltf_validator not on PATH: glTF validation skipped
```

A `FAIL` names the part: an open solid means a union did not close (see the `note: boolean
union unavailable` warning), an overlap above 0.1 µm means two parts share volume. Both are
bugs worth reporting with the board file.

## 17.4 The Regression Suite

`Tests/test_boards.py` runs every board in `Tests/boards/` and `Input/` through **both** modes
with the Verifier and compares every part's volume with `Tests/baseline.json`:

```bash
python -m pytest Tests                 # or:  python Tests/test_boards.py
python Tests/test_boards.py --accept   # re-record the baseline after an intended geometry change
```

A board fails when the Verifier fails, when a part's volume moved by more than 0.1 % from the
recorded baseline, when a part disappeared or a new one appeared, or (for the small boards
`one_layer`, `six_layer`, `synthetic`, when `cadquery` is installed) when the STEP file has an
invalid solid or a free edge, checked by reading it back with OCP.

The test boards cover: a one-layer board with text, a six-layer board with a full stack-up
(prepreg / core, 17.5 µm inner foil, black mask, blind and buried vias, "remove unused layers"
vias, zone fills), and a synthetic board with a two-ply stack-up.

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
