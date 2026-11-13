# 19. Parameter Reference

![A four-layer board cut through from the top silkscreen to the bottom silkscreen, every part numbered 1 to 19, beside a table that gives for each part its line in Stackup.py and the parameter file that sets its thickness and shape, its material and its colour: SilkScreen.py for the two silkscreens, SolderMask.py for the two masks and the mask over a via, Finish.py for the finish on both faces and inside the plated holes, Copper.py for the top, inner and bottom copper, the plated walls and the via resin, Board.py for the prepreg plies, the cores, the resin between the inner traces, the outline and the holes; below it the three folders of parameters/: PCB_elements with Stackup.py and the five element files, Run_KESE with Run.py, Geometry.py, Parallel.py, Verifier.py and Presets.py, and Fileformats with Step.py and Mesh.py](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Parameter-Reference/params_1_files_by_part.webp)

Every setting lives in one of thirteen files, in the three folders of `parameters/`. These are the
only files you edit.

| Folder | Files | What they set |
|---|---|---|
| `PCB_elements/` | `Stackup.py`, `Board.py`, `Copper.py`, `Finish.py`, `SolderMask.py`, `SilkScreen.py` | What the board is made of. `Stackup.py` says which layers are built and holds nothing else; each element's own file holds its thickness, shape, material and colour |
| `Run_KESE/` | `Run.py`, `Geometry.py`, `Parallel.py`, `Verifier.py`, `Presets.py` | How KESE runs. No part of the board is set here |
| `Fileformats/` | `Step.py`, `Mesh.py` | The files KESE writes |

The five element files have the same numbered sections, and the tables below follow them:
**1 Parts**, **2 Thickness**, **3 Shape**, **4 Material** (written to `materials.json` for the
solver; it changes no geometry) and **5 Color** (for the viewer). `Copper.py` has seven: all copper,
the top, the inner and the bottom copper, the plated holes, then its material and its colour.

Units are mm unless a name says otherwise. The **Range** column is what the program uses
sensibly; "None" means the program works the value out itself. Any value can be overridden for
one run with `--set Module.NAME=value`, where `Module` is the file's name without `.py`, the short
name in the heading of each section (`Copper`, `SolderMask`, `Step`). A line of `Stackup.py` is set
with `--set Stackup.<line>=True` or `False`. The `parameters.txt` written next to each output records
every value as it stood for the run, file by file: `--for`, `--set`, `--mode`, `--format` and
`--verify` are all applied as overrides first, and listed on its first line.

> [!NOTE]
> Defaults are those of the parameter files on `main`. Before the board is read, the run checks
> `MODE` and `FILE_FORMAT`; the two stack-ups of `Stackup.py` (each with exactly its own lines, each
> `True` or `False`, and at least one line of the stack-up being built `True`); every setting whose
> range below is a few words with `/` between them (such as `"mm"` / `"m"`); the settings of
> `Parallel.py`; the rounds, counts, digits and margins of `Geometry.py`; the Verifier's tolerances,
> rays and merge digits; the finish's mitre limit; the STEP arcs' settings that count or divide; the
> etch factors, foils, added plating and roughness values of the copper; the εr and tan δ of the
> laminate's defaults, the resin, the via resin, the mask and the ink; the spec and corner
> frequencies and `DIELECTRIC_TABLE`; the names in the preset of `--for`; and the kind of every
> value: `True` or `False` where the file has one of them, a number where it has a number, text, a
> list or a dict likewise (a setting that is `None` in its file takes `None` or a value of its kind).
> It also stops when a parameter file still holds a setting under an old name, or a parameter file
> of before 25.2 still lies in `parameters/` itself ([19.14](#1914-names-of-before-252)). It stops
> with an error that names the setting.
> `FINISH_TYPE` and `DIELECTRIC_SPLIT` are checked where they are used (an error or a warning),
> `PLIES_BY_HAND` when the board's stack-up is read, and `FONT_FILE` gives a note in `report.txt`.
> For the rest, a value outside the range below produces a wrong model or a plain Python error, not
> a named check.

## 19.1 Stackup (`parameters/PCB_elements/Stackup.py`)

What KESE builds: the stack-up, laid out as a real board is, from the top silkscreen down to the
bottom silkscreen. This file is the list of what goes into the files KESE writes, in every mode and
format. It holds no thickness, material or colour: those are in each element's own file. Details in
[Stack-Up Model](Stack-Up-Model.md#84-what-is-built-the-lines-of-stackuppy).

### 19.1.1 The Two Stack-Ups

| Name | Default | Range | Meaning |
|---|---|---|---|
| `FUSION_BUILD` | `"PLIES_FUSED"` | `"PLIES_FUSED"` / `"PLIES_SEPARATE"` | Which of the two stack-ups below is built |
| `PLIES_FUSED` | 14 lines | `{line: True / False}` | The laminate as one solid for each gap between two copper layers. The prepreg plies of a gap are fused into that solid, and so is the resin between the traces of the inner copper beside it |
| `PLIES_SEPARATE` | 15 lines | `{line: True / False}` | The laminate as a fabricator builds it: every prepreg ply, every core and the resin between the traces of each inner copper layer is its own solid, with its own thickness and material ([Board](Board.md#121-dielectric-solids)) |

### 19.1.2 The Lines

Each line of a stack-up is one layer of the board, or one kind of layer where a board has several.
`True` builds it and writes it to every output file; `False` leaves it out. The lines run as the
layers lie in a real board: the top side from the outside in, the inside of the board, the bottom
side from the inside out, and last what goes through the board. The order is for reading and
changes nothing: how many copper layers a board has, and the plies between them, come from the board
file, and the lines of the inside stand for every inner layer the board has.

| Line | In | Default | What it builds | Set in |
|---|---|---|---|---|
| `top_silkscreen` | both | `False` | `Top Silkscreen`: the legend ink on the top solder mask | [SilkScreen](#196-silkscreen-parameterspcb_elementssilkscreenpy) |
| `top_solder_mask` | both | `False` | `Top Solder Mask`, and in visual mode `Top Mask over Copper` | [SolderMask](#195-solder-mask-parameterspcb_elementssoldermaskpy) |
| `top_finish` | both | `True` | `Top Finish <metal>`: ENIG, HASL and the others on the top copper the mask leaves bare, its tops and its side walls | [Finish](#194-finish-parameterspcb_elementsfinishpy) |
| `top_copper` | both | `True` | `F.Cu`: the foil and the copper plated on it | [Copper](#193-copper-parameterspcb_elementscopperpy), section 2 |
| `board` | fused | `True` | The laminate: one solid for each gap, its plies fused (`Board_dielectric 1`) | [Board](#192-board-parameterspcb_elementsboardpy) |
| `prepreg_plies` | separate | `True` | Each prepreg ply its own solid (`Board_dielectric 1 ply 1`) | Board |
| `resin_between_traces` | both | `True` | The resin between the traces of the inner copper. Fused: the board solids also fill that space, so the line needs `board`. Separate: a solid of its own for each inner copper layer (`Board_resin In1.Cu`). `False` leaves the space empty, and `report.txt` notes it | Board |
| `inner_copper` | both | `True` | `In1.Cu`, `In2.Cu` and every other inner copper layer | Copper, section 3 |
| `cores` | separate | `True` | Each core its own solid (`Board_dielectric 2`) | Board |
| `bottom_copper` | both | `True` | `B.Cu`: the foil and the copper plated on it | Copper, section 4 |
| `bottom_finish` | both | `True` | `Bottom Finish <metal>` on the bottom copper the mask leaves bare | Finish |
| `bottom_solder_mask` | both | `False` | `Bottom Solder Mask`, and in visual mode `Bottom Mask over Copper` | SolderMask |
| `bottom_silkscreen` | both | `False` | `Bottom Silkscreen`: the legend ink on the bottom solder mask | SilkScreen |
| `plated_holes` | both | `True` | The plated walls of the vias and the through-hole pads, the copper in filled vias, castellations and the plated edge | Copper, section 5 |
| `hole_finish` | both | `True` | `Hole Finish <metal>` inside the plated holes and `Edge Finish <metal>` on the board's edge | Finish |
| `via_resin` | both | `True` | `Via Resin`: the resin in plugged and resin-filled vias | Copper, section 5 |

KESE works every line out first and then leaves out the ones set to `False`, so what stays is
exactly as it is with every line `True`: with the top solder mask left out, the top finish still
ends where the mask would begin, and a net's copper with `top_copper` left out is the same solid
less its `F.Cu` layer. A part with every layer of it left out is not written at all. The solder mask
and the silkscreen are `False` by default: they are many more solids, which make STEP files much
bigger and slower to open, and most EM work leaves them out.

A stack-up that cannot be built stops the run before the board is read: every line of the stack-up
being built `False`, a line missing, a line that is not one of its lines (with the closest name
offered), or a value that is not `True` or `False`. Not built in either stack-up: the seed copper
under the plated copper (it lies inside the copper solid) and the glass cloth inside a ply (a ply
is one uniform solid).

### 19.1.3 Short Names

`--set Stackup.<line>=...` sets that line in both stack-ups, so the same command works whichever is
built. Four short names set several lines at once, on the command line and in a preset:

| Short name | Lines it sets |
|---|---|
| `Stackup.silkscreen` | `top_silkscreen`, `bottom_silkscreen` |
| `Stackup.solder_mask` | `top_solder_mask`, `bottom_solder_mask` |
| `Stackup.finish` | `top_finish`, `bottom_finish`, `hole_finish` |
| `Stackup.copper` | `top_copper`, `inner_copper`, `bottom_copper`, `plated_holes` |

```
python run_KESE.py board.kicad_pcb --set Stackup.FUSION_BUILD=PLIES_SEPARATE
python run_KESE.py board.kicad_pcb --set Stackup.solder_mask=True --set Stackup.silkscreen=True
python run_KESE.py board.kicad_pcb --set Stackup.bottom_copper=False
```

## 19.2 Board (`parameters/PCB_elements/Board.py`)

The laminate (the dielectric between the copper layers), the outline, and the holes and machining
that cut through every layer. The board file is read first; the values here fill in what the file
leaves out, or replace it where a `USE_STACKUP_*` switch is `False` or `PLIES_BY_HAND` lists a gap.
Whether the laminate is built, and whether its plies are fused or separate, is in
[Stackup](#191-stackup-parameterspcb_elementsstackuppy). Details in [Board](Board.md).

### 19.2.1 Parts

| Name | Default | Range | Meaning |
|---|---|---|---|
| `JOIN_EQUAL_PLIES` | `False` | bool | Plies separate: neighbouring plies of one gap with the same type, material, εr, tan δ, spec frequency and model become one solid. It is named after the plies it holds (`Board_dielectric 3` for every ply of that dielectric, `Board_dielectric 1 ply 2-3` for some of them), and `materials.json` lists them under `joined_plies` |
| `DIELECTRIC_GROUPING` | `"layer"` | `"layer"` / `"merged"` | The solids of the stack-up being built, or the whole laminate as one solid (`Board`), whichever stack-up is built |

### 19.2.2 Thickness

| Name | Default | Range | Meaning |
|---|---|---|---|
| `BOARD_THICKNESS_MM` | `None` | None or mm > 0 | Laminate thickness; `None` takes it from the file (a usable stack-up, else `(general (thickness))` less the outer copper and the masks, else 1.6 mm less the same). A number keeps the plies' proportions, scaled to it |
| `DEFAULT_BOARD_THICKNESS_MM` | `1.6` | mm > 0 | Finished board thickness when the file gives none (KiCad's default) |
| `DIELECTRIC_SPLIT` | `"even"` | `"even"` | How the laminate is divided between copper layers when the file has no usable stack-up |
| `PLY_MIN_THICKNESS_MM` | `0.001` | mm ≥ 0 | Plies separate: a ply thinner than this is joined to its thicker neighbour, with a warning (a bond film of half a micrometre is no solid a mesher wants); 0 keeps every ply |
| `PLIES_BY_HAND` | `{}` | `{board name: {(copper above, copper below): [plies]}}` | Plies written by hand for one board, named by its file name without `.kicad_pcb`. A gap listed here takes these plies, top to bottom, in place of the file's; gaps not listed still come from the file, and other boards are not touched. Each ply is a dict with `"type"` (`"core"` / `"prepreg"`), `"thickness_mm"`, `"material"`, `"epsilon_r"` and `"loss_tangent"`, and may give `"frequency_hz"` and `"model"`. The list is checked when the stack-up is read: the two copper layers must be neighbours on that board, the upper one first, and every ply whole ([Board](Board.md#1214-plies-written-by-hand)) |

### 19.2.3 Shape

| Name | Default | Range | Meaning |
|---|---|---|---|
| `OUTLINE_LINE_SNAP_MM` | `0.01` | mm > 0 | Open `Edge.Cuts` line and arc ends closer than this are joined, as KiCad joins them (its chaining distance is 0.01 mm) |
| `OUTLINE_FALLBACK` | `"copper_hull"` | `"copper_hull"` / `"error"` | When `Edge.Cuts` gives no closed ring at all: convex hull of the copper plus a margin, or stop |
| `OUTLINE_FALLBACK_MARGIN_MM` | `1.0` | mm ≥ 0 | Margin of the fallback hull |
| `OUTLINE_DUPLICATE_AREA_MM2` | `1e-6` | mm² > 0 | Two closed `Edge.Cuts` outlines that differ by less than this area are one (a ring drawn twice) |
| `OUTLINE_MIN_AREA_MM2` | `1e-9` | mm² ≥ 0 | A closed `Edge.Cuts` outline of this area or less is left out (a line drawn there and back, a circle of no size) |
| `INCLUDE_NON_PLATED_HOLES` | `True` | bool | NPTH pads become holes through the board |
| `BACKDRILLS` | `True` | bool | KiCad 10's backdrills and tertiary drills: the hole is drilled out, plating and copper too, from its start layer through its must-cut layer ([Copper And Traces](Copper-And-Traces.md#1333-backdrills)) |
| `POST_MACHINING` | `True` | bool | KiCad 10's counterbores and countersinks are cut from the board's face ([Board](Board.md#1241-counterbores-and-countersinks)) |
| `COUNTERSINK_STEP_TOLERANCE_MM` | `0.025` | mm > 0 | A countersink's cone is built as steps that stray from it by at most this |

### 19.2.4 Material

Written to `materials.json` for the solver ([Material Properties](Material-Properties.md)); none of
these changes a solid.

| Name | Default | Range | Meaning |
|---|---|---|---|
| `DEFAULT_DIELECTRIC_MATERIAL`, `DEFAULT_DIELECTRIC_TYPE` | `"FR4"`, `"core"` | text; `"core"` / `"prepreg"` | Used when the stack-up gives none |
| `DEFAULT_EPSILON_R`, `DEFAULT_LOSS_TANGENT` | `4.5`, `0.02` | ≥ 1, ≥ 0 | Generic FR4 at 1 GHz (KiCad's defaults for a new dielectric), used when the stack-up gives none |
| `DEFAULT_SPEC_FREQUENCY_HZ` | `1e9` | Hz > 0 | The frequency εr and tan δ are given at, when the file gives none (KiCad's default) |
| `USE_STACKUP_EPSILON_R`, `USE_STACKUP_LOSS_TANGENT` | `True`, `True` | bool | Stack-up values win over the defaults when present |
| `USE_STACKUP_SPEC_FREQUENCY` | `True` | bool | A ply's `(spec_frequency ...)` in the file wins over the default (KiCad's development version writes it, file format 20260511 on) |
| `DIELECTRIC_MODEL` | `"constant"` | `"constant"` / `"djordjevic_sarkar"` / `"table"` | How εr and tan δ change with frequency, written to `materials.json` as `dielectric_model`: the same at every frequency; the wideband Djordjevic-Sarkar model, fitted to εr and tan δ at the spec frequency, with its fitted parameters; or `DIELECTRIC_TABLE`, written as given ([Material Properties](Material-Properties.md#214-how-εr-and-tan-δ-change-with-frequency)) |
| `USE_STACKUP_DIELECTRIC_MODEL` | `True` | bool | A ply's `(dielectric_model constant)` or `(dielectric_model djordjevic_sarkar)` in the file wins over `DIELECTRIC_MODEL` |
| `DS_LOW_FREQUENCY_HZ`, `DS_HIGH_FREQUENCY_HZ` | `1e3`, `1e12` | Hz > 0 | The Djordjevic-Sarkar model's lower and upper corner frequencies. A ply whose spec frequency is not between them cannot be fitted: it is written with constant values, with a warning, as KiCad falls back |
| `DIELECTRIC_TABLE` | `()` | `((frequency Hz, εr, tan δ), ...)` by rising frequency | The rows of the `"table"` model, for example `((1e8, 4.6, 0.016), (1e9, 4.5, 0.02), (1e10, 4.4, 0.022))`; empty with `DIELECTRIC_MODEL = "table"` stops the run |
| `FUSED_PROPERTIES` | `"first"` | `"first"` / `"series"` | Plies fused, a gap whose plies differ: the first ply's material, εr and tan δ (top to bottom), or the plies in series, as a field straight across the gap sees them (equation (21.3) in [Material Properties](Material-Properties.md#215-a-gap-whose-plies-differ)). Either way `materials.json` lists every ply of the gap under `plies` |
| `RESIN_MATERIAL` | `"resin"` | text | Plies separate: the material name of the resin solids (`Board_resin In1.Cu`) |
| `RESIN_EPSILON_R`, `RESIN_LOSS_TANGENT` | `3.5`, `0.02` | None, or ≥ 1 and ≥ 0 | Plies separate: εr and tan δ of the resin between the traces of the inner copper, the prepreg's resin without its glass; `None` takes that value from the prepreg ply the resin flowed from. A best guess for FR-4 epoxy (published figures give εr 3.0 to 3.57 and tan δ 0.021), not a resin maker's figure. With the plies fused the resin is part of the board solid beside it and has that solid's values; these three are not used |

### 19.2.5 Color

Each is `{color hex, alpha 0-1, metallic 0-1, roughness 0-1}`: the look of the part in GLB and OBJ,
its colour in STEP and the `look` field of `materials.json`; alpha < 1 writes a glTF BLEND material.
Details in [Colorizing](Colorizing.md).

| Name | Default | Meaning |
|---|---|---|
| `CORE_COLOR` | `#968A58` | A core, and a fused gap whose first ply is a core |
| `PREPREG_COLOR` | `#A89C66` | A prepreg ply, and a fused gap whose first ply is prepreg |
| `RESIN_COLOR` | `#B8AC78` | Plies separate: the resin between the traces of the inner copper |
| `BOARD_COLOR` | `#968A58` | The whole laminate as one solid (`DIELECTRIC_GROUPING = "merged"`), and a ply of no type |

## 19.3 Copper (`parameters/PCB_elements/Copper.py`)

The top, inner and bottom copper layers, the plated holes, the vias and the plated board edge.
Whether the copper is built is in [Stackup](#191-stackup-parameterspcb_elementsstackuppy): the lines
`top_copper`, `inner_copper` and `bottom_copper`, `plated_holes` and `via_resin`. Details in
[Copper And Traces](Copper-And-Traces.md).

### 19.3.1 All Copper

| Name | Default | Range | Meaning |
|---|---|---|---|
| `COPPER_GROUPING` | `"net"` | `"net"` / `"layer"` / `"merged"` | One copper solid per net, per layer (plating separate), or one in all |
| `NO_NET_NAME` | `"no_net"` | text | Name of copper that belongs to no net |
| `USE_STACKUP_COPPER_THICKNESS` | `True` | bool | Stack-up `(layer "F.Cu" (thickness ...))` wins when present; `False` always uses the `DEFAULT_*_FOIL_MM` of the layer's section |
| `ETCH_STEPS` | `4` | int ≥ 1 | Slices the trapezoid of an etched layer is built from |
| `ETCH_UNETCHED_REACH` | `1.5` | ≥ 0 | Copper within this × the etch inset of a hole wall or the board edge keeps its outline |
| `HAIRLINE_HOLE_MM` | `1e-3` | mm ≥ 0 | A hole in one net's copper narrower than this on average (2 × area / perimeter) is filled: the hair-wide gap KiCad leaves between a zone fill and a pad of its own net |
| `HONOUR_REMOVE_UNUSED_LAYERS` | `True` | bool | Drop via and through-hole pad annular rings on layers nothing connects to, as KiCad's option does |

### 19.3.2 Top Copper (`F.Cu`)

| Name | Default | Range | Meaning |
|---|---|---|---|
| `DEFAULT_TOP_FOIL_MM` | `0.035` | mm > 0 | Foil when the stack-up gives none (1 oz = 0.035, 0.5 oz = 0.0175) |
| `TOP_PLATING_ADDED_MM` | `0.0` | mm ≥ 0 | Electroplated copper added to the top copper during hole plating: finished copper = foil + this. Typical 0.020; 0 = foil only, as KiCad models |
| `TOP_ETCH_FACTOR` | `0.0` | ≥ 0 | Each side wall leans in by this × copper thickness over the copper height, the foot on the laminate; 0 = rectangular, as KiCad ([Copper And Traces](Copper-And-Traces.md#135-etch-factor)) |

### 19.3.3 Inner Copper (`In1.Cu`, `In2.Cu`, ...)

| Name | Default | Range | Meaning |
|---|---|---|---|
| `DEFAULT_INNER_FOIL_MM` | `0.035` | mm > 0 | Foil when the stack-up gives none. Inner copper gets no plating |
| `INNER_ETCH_FACTOR` | `0.0` | ≥ 0 | Etch factor of the inner copper. It is etched on its core: its foot is on the side toward the board's centre |

### 19.3.4 Bottom Copper (`B.Cu`)

| Name | Default | Range | Meaning |
|---|---|---|---|
| `DEFAULT_BOTTOM_FOIL_MM` | `0.035` | mm > 0 | Foil when the stack-up gives none |
| `BOTTOM_PLATING_ADDED_MM` | `0.0` | mm ≥ 0 | Finished bottom copper = foil + this, as for the top copper |
| `BOTTOM_ETCH_FACTOR` | `0.0` | ≥ 0 | Etch factor of the bottom copper, the foot on the laminate |

### 19.3.5 Plated Holes, Vias And The Board Edge

| Name | Default | Range | Meaning |
|---|---|---|---|
| `VIA_WALL_MM` | `0.025` | mm > 0 | Plated wall of vias (typical 0.020 to 0.025) |
| `PTH_WALL_MM` | `0.025` | mm > 0 | Plated wall of through-hole pads |
| `CASTELLATION` | `"auto"` | `"auto"` / `"file"` / `"off"` | Plated holes crossing `Edge.Cuts`: always plated as castellations, only when the stack-up says `(castellated_pads yes)`, or not plated |
| `CASTELLATION_WALL_MM` | `0.025` | mm > 0 | Plated wall of a castellation |
| `EDGE_PLATING` | `"file"` | `"file"` / `"yes"` / `"no"` | Copper on the routed edge: follow `(edge_plating yes)`, always, never |
| `EDGE_PLATING_WALL_MM` | `0.025` | mm > 0 | Width of the edge band inside the outline |
| `EDGE_PLATING_NET` | `"auto"` | `"auto"` or a net name | Net of the edge copper; `"auto"` = the named net with the most copper touching the band |
| `VIA_PROTECTION` | `"file"` | `"file"` / `"off"` | KiCad 10's covered, plugged, capped and filled vias (IPC-4761): as the board says, or every via left open ([Copper And Traces](Copper-And-Traces.md#1334-via-protection)) |
| `VIA_FILL` | `"copper"` | `"copper"` / `"resin"` | What a filled via is filled with: copper of the via's net, or the via resin |
| `VIA_PLUG_DEPTH_FRACTION` | `0.5` | > 0, ≤ 1 | How far a plug reaches into the hole from its face, as a share of the hole's length |

Whether the mask covers a via is `SolderMask.VIA_TENTING` ([19.5.3](#1953-shape)).

### 19.3.6 Material

Written to `materials.json` for the solver; none of these changes a solid.

| Name | Default | Range | Meaning |
|---|---|---|---|
| `COPPER_MATERIAL` | `"copper"` | text | The material name of every copper part: foils, plating, barrels, castellations and edge plating |
| `COPPER_CONDUCTIVITY_S_PER_M` | `5.8e7` | S/m | Written for every copper part (annealed copper at 20 °C) |
| `COPPER_ROUGHNESS_MODEL` | `"none"` | `"none"` / `"hammerstad"` / `"huray"` | The surface roughness model for the solver's conductor loss, written as `roughness`: smooth; one RMS height per face; or the "snowball" model, a nodule radius and a surface ratio per face. Each copper layer has two faces: the treated face, pressed into the dielectric the foil was laminated on, and the other; a copper part says which is which, layer by layer, in `treated_face` ([Material Properties](Material-Properties.md#216-copper-by-layer)) |
| `COPPER_ROUGHNESS_RMS_TREATED_UM`, `COPPER_ROUGHNESS_RMS_OTHER_UM` | `0.0`, `0.0` | µm ≥ 0 | `"hammerstad"`: the RMS height of the treated face and of the other. Foil makers quote Rz (peak to valley), which is larger: standard foil 3 to 6 µm, RTF 1 to 1.5, VLP and HVLP 0.3 to 1 |
| `COPPER_HURAY_RADIUS_TREATED_UM`, `COPPER_HURAY_RADIUS_OTHER_UM` | `0.5`, `0.5` | µm ≥ 0 | `"huray"`: the nodule radius on each face |
| `COPPER_HURAY_SURFACE_RATIO_TREATED`, `COPPER_HURAY_SURFACE_RATIO_OTHER` | `1.0`, `1.0` | ≥ 0 | `"huray"`: the nodules' surface over the flat surface, on each face |
| `VIA_RESIN_MATERIAL` | `"via resin"` | text | The material name of the `Via Resin` part |
| `VIA_RESIN_EPSILON_R`, `VIA_RESIN_LOSS_TANGENT` | `4.4`, `0.02` | ≥ 1, ≥ 0 | The plug and fill resin (San-Ei Kagaku PHP-900 IR-6P at 1 GHz) |

### 19.3.7 Color

| Name | Default | Meaning |
|---|---|---|
| `COPPER_COLOR` | `#CD803E`, metallic 0.9 | Every copper part in simulation mode. A net's copper is one solid across its layers, so the top, inner and bottom copper share one colour |
| `PLATING_COLOR` | `#CD803E`, metallic 0.9 | The plated walls of the holes, where they are a part of their own (`COPPER_GROUPING = "layer"`) |
| `EXPOSED_COPPER_COLOR` | `#DEBA60`, metallic 1.0 | Visual mode: all the copper that shows |
| `VIA_RESIN_COLOR` | `#D8CFA0` | The `Via Resin` part |

## 19.4 Finish (`parameters/PCB_elements/Finish.py`)

The surface finish on copper left bare by the solder mask. Whether it is built is in
[Stackup](#191-stackup-parameterspcb_elementsstackuppy): the lines `top_finish`, `bottom_finish`
and `hole_finish`. Details in [Finish](Finish.md).

### 19.4.1 Parts

| Name | Default | Range | Meaning |
|---|---|---|---|
| `FINISH_TYPE` | `"ENIG"` | `"file"` or a key of `FINISH_TYPES` | The finish type, or `"file"` to take it from the stack-up's `(copper_finish ...)` (KiCad's `None` builds no finish; no finish in the file, or a name that matches no key and no alias, stops the run with an error) |
| `FINISH_NAME_ALIASES` | 6 KiCad names (`HAL SnPb` → `HASL`, `HAL lead-free` → `HASL_LF`, `Hard gold`, `Immersion tin`, `Immersion silver`, `HT_OSP` → `OSP`) | `{KiCad name: key of FINISH_TYPES}` | KiCad finish names that differ from a key; matching ignores case, spaces, `-` and `_` |
| `FINISH_GROUPING` | `"metal"` | `"metal"` / `"net"` | One part per side and metal, or per side, metal and net |

### 19.4.2 Thickness

| Name | Default | Range | Meaning |
|---|---|---|---|
| `FINISH_TYPES` | ENIG, ENEPIG, HASL, HASL_LF, OSP, ImmersionSilver, ImmersionTin, HardGold | `{key: [(metal, mm), ...]}` bottom to top | Layers of each finish; each becomes its own solid on the bare copper |

### 19.4.3 Shape

| Name | Default | Range | Meaning |
|---|---|---|---|
| `FINISH_BEFORE_SOLDER_MASK` | `False` | bool | The finish goes on before the mask: on all the outer copper, with the mask and silkscreen on top of it; `False` puts it only in the mask openings |
| `FINISH_MITRE_LIMIT` | `2.0` | ≥ 1 | How the finish follows the copper's sharp corners: the outer side of each finish layer (and of the copper the mask wraps, with `FINISH_BEFORE_SOLDER_MASK`) keeps a corner's point out to this many times the finish's thickness from the copper's corner, and is cut straight across there. At `2.0` a corner of 60° or more keeps its point (a square pad's corners stay square) and a sharper tip is cut; `1.0` cuts every corner at the finish's thickness; below 1 the finish would be thinner at a corner than its thickness, so the run stops |

### 19.4.4 Material

| Name | Default | Range | Meaning |
|---|---|---|---|
| `FINISH_CONDUCTIVITY_S_PER_M` | Nickel `1.4e7`, Gold `4.1e7`, Palladium `9.5e6`, Tin `9.1e6`, Silver `6.3e7`, OSP `0.0` | `{metal: S/m}` | Written to `materials.json` |

### 19.4.5 Color

| Name | Default | Range | Meaning |
|---|---|---|---|
| `FINISH_COLORS` | Nickel `#B8B8B0`, Gold `#E6C15A`, Tin `#C9C9C9`, Silver `#E4E4E0`, Palladium `#DFDAD4`, OSP `#D9955A` | `{metal: {color hex, alpha 0-1, metallic 0-1, roughness 0-1}}` | The look of each finish metal |

## 19.5 Solder Mask (`parameters/PCB_elements/SolderMask.py`)

Short name `SolderMask`. Whether the mask is built is in
[Stackup](#191-stackup-parameterspcb_elementsstackuppy): the lines `top_solder_mask` and
`bottom_solder_mask`, both `False` by default. Details in [Solder Masks](Solder-Masks.md).

### 19.5.1 Parts

`Top Solder Mask` and `Bottom Solder Mask`, and in visual mode `Top Mask over Copper` and
`Bottom Mask over Copper`. There is no setting here: `Stackup.py` says whether they are built.

### 19.5.2 Thickness

| Name | Default | Range | Meaning |
|---|---|---|---|
| `MASK_OVER_LAMINATE_MM` | `0.010` | mm > 0 | Mask thickness over bare laminate (typical 0.020 to 0.030) |
| `MASK_OVER_COPPER_MM` | `0.010` | mm > 0 | Mask thickness on top of copper (typical 0.010 to 0.015) |
| `USE_STACKUP_MASK_THICKNESS` | `True` | bool | The first mask thickness found in the stack-up (normally `F.Mask`'s) is used for both values on both faces |

### 19.5.3 Shape

| Name | Default | Range | Meaning |
|---|---|---|---|
| `VIA_TENTING` | `"file"` | `"file"` / `"tented"` / `"open"` | Mask over vias: follow the board, cover all, open all |
| `MASK_EDGE_PULLBACK_MM` | `0.005` | mm ≥ 0 | Mask and silk stop this far short of the board edge |
| `PAD_TO_MASK_CLEARANCE_MM` | `None` | None or mm | Clearance around pads and untented vias; `None` takes the board setup's value from the file. A number replaces only the board setup's value: a pad's or footprint's own `solder_mask_margin` in the file still wins |
| `MASK_MIN_WIDTH_MM` | `None` | None or mm ≥ 0 | Narrowest web of mask kept between two openings; `None` follows Board Setup (`solder_mask_min_width`), 0 keeps every web |
| `MASK_WEB_HAIRLINE_MM` | `1e-3` | mm ≥ 0 | A web the minimum width adds that is narrower than twice this is dropped |
| `MASK_OVER_COPPER_HAIRLINE_MM` | `1e-3` | mm ≥ 0 | A piece of mask on top of copper narrower than twice this is left out, and the finish covers it instead: the slivers left where an opening's outline follows the copper's with other points ([Solder Masks](Solder-Masks.md#172-conformal-mask)); 0 keeps them |
| `MASK_OPENING_HAIRLINE_MM` | `1e-3` | mm ≥ 0 | A mask opening narrower than twice this everywhere is left out, the mask kept over it: the opening of a pad a micrometre across, which no fab makes ([Solder Masks](Solder-Masks.md#172-conformal-mask)); 0 keeps every one |
| `MASK_WALL_QUAD_SEGS` | `4` | int ≥ 1 | Segments per quarter circle on the walls where the mask climbs a trace |

### 19.5.4 Material

| Name | Default | Range | Meaning |
|---|---|---|---|
| `MASK_MATERIAL` | `"LPI"` | text | The material name of the mask when the file gives none (liquid photoimageable mask) |
| `MASK_EPSILON_R`, `MASK_LOSS_TANGENT` | `3.8`, `0.03` | ≥ 1, ≥ 0 | Generic LPI mask (JLCPCB gives εr 3.8, OSH Park 3.9; Taiyo PSR-4000BN tan δ 0.029 at 1 MHz, OSH Park 0.033), used when the file gives none |
| `USE_STACKUP_MASK_MATERIAL` | `True` | bool | Each mask layer's own `(material ...)`, `(epsilon_r ...)` and `(loss_tangent ...)` in the stack-up win, side by side: the top and the bottom mask can differ |

### 19.5.5 Color

| Name | Default | Range | Meaning |
|---|---|---|---|
| `TOP_MASK_COLOR`, `BOTTOM_MASK_COLOR` | `#EBEBE6`, alpha 0.80 | `{color hex, alpha 0-1, metallic 0-1, roughness 0-1}` | The mask on each side |
| `TOP_MASK_OVER_COPPER_COLOR`, `BOTTOM_MASK_OVER_COPPER_COLOR` | `#F2EFD8` | the same | Visual mode: the mask where it lies on top of copper |
| `VISUAL_MASK_OPAQUE` | `True` | bool | In visual mode the mask is opaque whatever its alpha |
| `USE_STACKUP_MASK_COLOR` | `True` | bool | Honour the mask colour in the board's stack-up, named or user-defined (`#RRGGBBAA`, its opacity not used) |
| `STACKUP_MASK_COLORS` | 11 names | `{name: hex}` | Mask colour names |
| `STACKUP_MASK_OVER_COPPER_COLORS` | 11 names | `{name: hex}` | Visual-mode colour of the mask over copper per stack-up colour; a name left out keeps `TOP_` / `BOTTOM_MASK_OVER_COPPER_COLOR` |
| `USER_MASK_OVER_COPPER_LIGHTEN` | `0.15` | 0-1 | With a user-defined (`#RRGGBBAA`) mask colour in the stack-up, how far the visual-mode mask over copper is mixed toward white |

## 19.6 Silkscreen (`parameters/PCB_elements/SilkScreen.py`)

Short name `SilkScreen`. Whether the silkscreen is built is in
[Stackup](#191-stackup-parameterspcb_elementsstackuppy): the lines `top_silkscreen` and
`bottom_silkscreen`, both `False` by default. Details in [Silkscreens](Silkscreens.md).

### 19.6.1 Parts

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SILK_LAYERS` | `["F.SilkS", "B.SilkS"]` | list of `F.*` / `B.*` layer names | Layers whose graphics are drawn as silkscreen, on the side their first letter names (any other name stops the run with a `KeyError` when the board has graphics on that layer); graphics on other non-physical layers are counted as skipped. Text is drawn only on `F.SilkS` / `B.SilkS`; text on other non-physical layers is ignored without a count |
| `DRAW_HIDDEN_TEXT` | `False` | bool | Draw text marked `(hide yes)` |

### 19.6.2 Thickness

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SILK_THICKNESS_MM` | `0.010` | mm > 0 | Ink thickness (typical 0.010 to 0.020) |

### 19.6.3 Shape

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SILKSCREEN_OVER_COPPER` | `False` | bool | Keep ink where the mask is open; `False` clips it off the pads as fabricators do. With `True` the ink lies on the copper and the finish is left out under it |
| `FONT_FILE` | `None` | None or a file in `kese/assets/fonts/` | Custom stroke font: this project's JSON, as one document or JSON Lines, or Hershey `.jhf`; `None` = KiCad newstroke |
| `DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT` | `True` | bool | Text in a TrueType face with no usable `render_cache` is drawn with the stroke font, with a warning; `False` leaves it out |
| `INTERLINE_PITCH` | `1.68` | > 0 | Line pitch as a multiple of the text height (KiCad's value) |
| `INTERLINE_LEGACY_FACTOR` | `0.9583` | > 0 | KiCad's correction for stroke fonts |
| `ITALIC_TILT` | `0.125` | ≥ 0 | x shift per unit of y for italic text |
| `BOLD_THICKNESS_RATIO`, `NORMAL_THICKNESS_RATIO` | `0.2`, `0.125` | > 0 | Stroke thickness as a fraction of the text width when the file gives none (KiCad's `GetPenSizeForBold` and `GetPenSizeForNormal`) |
| `MAX_PEN_RATIO` | `0.25` | > 0 | A stroke is at most this × the smaller of the text's width and height, whatever the file says (KiCad's `ClampTextPenSize`) |
| `TEXT_STROKE_QUAD_SEGS` | `4` | int ≥ 1 | Roundness of stroke ends |

### 19.6.4 Material

The board file gives no material for silkscreen (KiCad's own default εr is 1.0, as if it were air).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SILK_MATERIAL` | `"epoxy ink"` | text | The material name of the silkscreen parts |
| `SILK_EPSILON_R`, `SILK_LOSS_TANGENT` | `5.0`, `0.03` | ≥ 1, ≥ 0 | Best guesses for white legend ink: its pigment lifts εr above the mask's 3.8, and tan δ is the mask's. Neither is a maker's figure |

### 19.6.5 Color

| Name | Default | Range | Meaning |
|---|---|---|---|
| `TOP_SILK_COLOR`, `BOTTOM_SILK_COLOR` | `#141414` | `{color hex, alpha 0-1, metallic 0-1, roughness 0-1}` | The ink on each side, when the stack-up names no colour |
| `USE_STACKUP_SILK_COLOR` | `True` | bool | Honour the silkscreen colour in the board's stack-up, named or user-defined (`#RRGGBBAA`) |
| `STACKUP_SILK_COLORS` | white, black, yellow, green, red, blue, purple | `{name: hex}` | Silkscreen colour names |

## 19.7 Run (`parameters/Run_KESE/Run.py`)

What to make, where, and in which formats.

### 19.7.1 Mode, Folders And Formats

| Name | Default | Range | Meaning |
|---|---|---|---|
| `MODE` | `"simulation"` | `"simulation"` / `"visual"` | Closed solids for solvers, or the visible surface for viewers ([Output Modes](Output-Modes.md)) |
| `INPUT_DIR`, `OUTPUT_DIR` | `"Input"`, `"Output"` | paths relative to the current working directory (run from the `Generator/` folder) | Where boards are looked for and outputs written |
| `FILE_FORMAT` | `["glb"]` | any of `"glb"`, `"stl"`, `"obj"`, `"step"` | Files to write; visual mode allows only glb and obj |
| `UNITS` | `"m"` | `"mm"` / `"m"` | Units of the written files. Use `"mm"` for STEP, as CAD tools and solvers expect; the STEP file declares the units it is written in |
| `ORIGIN` | `"center"` | `"center"` / `"kicad"` | Outline centre at (0, 0), or KiCad's page origin kept |
| `ORIENTATION` | `"upright"` | `"upright"` / `"flat"` | Board in XY with `F.Cu` toward +Z, or in XZ with `F.Cu` toward +Y |

### 19.7.2 Run Behaviour

How many threads and processes work at once is set in [19.9 Parallel](#199-parallel-parametersrun_keseparallelpy),
the Verifier's settings in [19.10 Verifier](#1910-verifier-parametersrun_keseverifierpy), the presets in
[19.11 Presets](#1911-presets-parametersrun_kesepresetspy), the STEP files' own settings in
[19.12 Step](#1912-step-parametersfileformatssteppy) and those of the GLB, STL and OBJ files in
[19.13 Mesh](#1913-mesh-parametersfileformatsmeshpy).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SHOW_PROGRESS` | `True` | bool | Live `running <stage> ... 1m 23s` line on a terminal |
| `WRITE_MATERIALS_JSON` | `True` | bool | Write `materials.json` next to the outputs |

### 19.7.3 KiCad Versions

| Name | Default | Range | Meaning |
|---|---|---|---|
| `KICAD_VERSION_MIN`, `KICAD_VERSION_MAX` | `3`, `20260206` | KiCad file format numbers | Tested range, from the 2013 builds before KiCad 4 (format 3) to KiCad 10 (KiCad 4 files say `(version 4)`, KiCad 5 files `20171130`); a file outside it is read with a warning ([Compatibility](Compatibility.md#221-kicad-files)) |
| `TESTED_COPPER_LAYERS` | `8` | int > 0 | Stage 1 warns above this many copper layers (the most among the test boards); they are still modelled |

## 19.8 Geometry (`parameters/Run_KESE/Geometry.py`)

Numerical quality: how finely curves are faceted and how neighbouring layers share exact edges.
These do not change dimensions.

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SNAP_GRID_MM` | `0.0001` | mm > 0 | All 2D shapes are snapped to this grid (0.1 µm) so touching layers share identical vertices: no hairline gaps, no T-junctions |
| `SIMPLIFY_TOLERANCE_MM` | `0.0005` | mm ≥ 0 | Simplification of copper outlines after union; 0 = none |
| `ARC_STEP_DEG` | `3.0` | degrees > 0 | Maximum angle per segment when flattening arcs |
| `CIRCLE_CHORD_TOLERANCE_MM` | `0.005` | mm > 0 | Maximum deviation of a flattened circle from the true one: 5 µm, KiCad's own default (`ARC_HIGH_DEF_MM`, the board's maximum error) |
| `CIRCLE_MIN_QUAD_SEGS`, `CIRCLE_MAX_QUAD_SEGS` | `8`, `128` | int | Bounds on segments per quarter circle |
| `TRACK_END_MIN_QUAD_SEGS` | `4` | int ≥ 1 | Roundness of track ends |
| `BEZIER_SEGMENTS` | `32` | int ≥ 1 | Straight pieces per Bézier curve |
| `ELLIPSE_MIN_SEGMENTS` | `8` | int ≥ 3 | An ellipse or elliptical arc has at least this many straight pieces (else one per `ARC_STEP_DEG`) |
| `PINCH_POINT_OPENING_MM` | `1e-4` | mm > 0 | Polygons whose rings touch at a single point are opened by this much so they can be meshed |
| `PINCH_CUT_ROUNDS` | `10` | int ≥ 1 | Tries at opening one, the cut's radius doubling each time |
| `PINCH_DISC_TURN_DEG` | `17.0` | degrees | Turn of the octagon cut at a pinch, off the axes a board's edges follow |
| `PINCH_DISC_SIDES` | `8` | int ≥ 3 | Sides of that disc (an octagon) |
| `HEIGHT_DIGITS` | `9` | int ≥ 0 | Heights are told apart to 10^-9 mm (a picometre): two closer are one height, in stage 6's slices and the Verifier's checks |
| `VERTEX_SHARING_ROUNDS` | `20` | int ≥ 1 | Stage 6: rounds of cutting a part's faces and giving its slices each other's vertices, until nothing changes (mostly one to three; a hole's finish in visual mode has taken twelve). Slices still changing then are cut open where a round still moves them, as at a pinch point, for at most `PINCH_CUT_ROUNDS` more rounds; a part still changing after that is noted in `report.txt` and may be open ([Working Principle](Working-Principle.md#72-how-a-part-becomes-a-closed-solid)) |
| `NODING_ROUNDS` | `8` | int ≥ 1 | Rounds of noding a region on the snapping grid again (GEOS's hot pixels) until it changes nothing (one or two in practice) |
| `SLIVER_AREA_MM2` | `1e-10` | mm² > 0 | A polygon of less area is a sliver left by the set operations, and is dropped |
| `TRIANGULATE_CELL_POINTS` | `5000` | > 0 | A polygon with more points than this has its top and bottom cut into triangles strip by strip, much faster when it has many holes (earcut's time grows with the points times the holes). The points the strips add are taken out again, so the solid keeps exactly the polygon's own vertices |
| `TRIANGULATE_CELL_MM` | `10.0` | mm > 0 | Width of those strips, as KiCad cuts big polygons into 1 cm cells before it triangulates them |
| `SKIN_BURIED_TEST_OFFSET_MM` | `0.0005` | mm > 0 | Visual mode: a face is dropped if a point this far outside it lies inside another solid ([Output Modes](Output-Modes.md), equation (9.1)) |
| `MESH_MERGE_DIGITS` | `8` | int | 10^-8: a triangle's corner angle under 10^-8 rad counts as none (it gives no weight to smooth shading), and normals whose values spread less than that are not kept. No vertices are merged |
| `FLAT_FACET_THRESHOLD` | `5000` | > 0 | Smooth shading: two faces are one flat facet where (edge radius / edge span)² exceeds this |
| `SMOOTH_FACET_AREA_DIVISOR` | `10` | > 0 | Smooth shading: a flat facet of more than the part's area divided by this keeps flat normals (trimesh's `facet_minarea`) |
| `REACH_MARGIN_STEPS` | `8` | int ≥ 0 | Grid steps added to how far the conformal coating or the silkscreen ink can reach, where the copper near it is picked out first; a bigger margin picks out more and changes nothing else |
| `AIR_NEAR_MARGIN_STEPS` | `4` | int ≥ 0 | The holes' finish: grid steps past a band's part within which the solid beside it is taken, and further apart than their shells' reach by which bores are not grouped |
| `AIR_TILE_VERTICES`, `AIR_TILE_DEPTH` | `2000`, `16` | int ≥ 1, int ≥ 0 | The holes' finish: a bigger part of the solid beside the bores is cut first into tiles of about this many vertices, by at most this many halvings of its box (64k tiles a side), so that each bore clips only the tiles near it |
| `FINISH_BORES_AT_A_TIME` | `200` | int ≥ 1 | The holes' finish: a span's bores are worked on in groups of about this many, each group in a thread |
| `SKIN_FEW_PIECES`, `SKIN_BIG_PIECE_COORDINATES` | `200`, `10000` | int ≥ 0 | Visual skin: a face the slice beside it does not cover wholly is cut by the pieces of material that reach it, up to this many joined first, more as the whole slice's material, and a piece of this many coordinates (a dielectric, with every via hole in it) on its own |

The last four rows say how the work is cut up: other values make the same model, but where an edge
crossing rounds onto the grid another way, a sliver thinner than a grid step.

### 19.8.1 How The Curve Settings Are Used

A circle of radius $`r`$ (a via, a round pad) is flattened to $`4q`$ straight
segments, with $`q`$ segments per quarter circle chosen so that no chord strays more than
$`\varepsilon_c`$ from the true circle:

```math
n_c = \frac{\pi}{\arccos\left( 1 - \min\left( \frac{\varepsilon_c}{r},\ 1 \right) \right)} \qquad (19.1)
```

```math
q = \min\left( q_{\max},\ \max\left( q_{\min},\ \left\lceil \frac{n_c}{4} \right\rceil \right) \right) \qquad (19.2)
```

An arc (an arc track, an arc on a drawing layer) of sweep $`\varphi`$ is cut into

```math
n_a = \max\left( 2,\ \left\lceil \frac{|\varphi|}{\Delta\varphi} \right\rceil \right) \qquad (19.3)
```

segments, and the round ends of a track of width $`w`$ use

```math
q_{\mathrm{end}} = \max\left( q_{\mathrm{track}},\ \left\lfloor \frac{q(w/2)}{2} \right\rfloor \right) \qquad (19.4)
```

segments per quarter circle.

| Symbol | Meaning | Parameter |
|---|---|---|
| $`\varepsilon_c`$ | chord tolerance (5 µm) | `CIRCLE_CHORD_TOLERANCE_MM` |
| $`n_c`$ | segments a full circle needs for that tolerance | |
| $`q`$, $`q_{\min}`$, $`q_{\max}`$ | segments per quarter circle and its bounds (8, 128) | `CIRCLE_MIN_QUAD_SEGS`, `CIRCLE_MAX_QUAD_SEGS` |
| $`\varphi`$, $`\Delta\varphi`$ | arc sweep and maximum step (3°) | `ARC_STEP_DEG` |
| $`q_{\mathrm{track}}`$ | minimum roundness of track ends (4) | `TRACK_END_MIN_QUAD_SEGS` |
| $`q(w/2)`$ | equation (19.2) for radius $`w/2`$ | |

Example: a 0.3 mm via ($`r = 0.15`$ mm) gives $`n_c = 12.1`$, so $`q = \max(8, \lceil 3.03 \rceil) = 8`$, 32
segments around the via; the floor $`q_{\min}`$ decides for every circle below about 1 mm radius. A 3.2 mm
mounting hole ($`r = 1.6`$ mm) gives $`n_c = 39.7`$ and $`q = 10`$, 40 segments around it.

## 19.9 Parallel (`parameters/Run_KESE/Parallel.py`)

How many processor cores work at once, and how much the work holds in memory at once
([Working Principle](Working-Principle.md#74-work-done-in-parallel)). None of these changes the
model: the files are the same, byte for byte, however the work is shared out.

| Name | Default | Range | Meaning |
|---|---|---|---|
| `WORKERS` | `0` | int ≥ 0 | Threads or processes that work at once. Threads where the 2D geometry library does the work (it runs outside Python's lock): the copper layers and the solder mask's minimum web width, group by group, in stage 3; both sides of the solder mask and the silkscreen, and the finish's copper layers and groups of bores, in stage 4; the faces of the visual-mode skin and the test for its hidden triangles, in stage 6; the Verifier's overlap check in stage 8. Processes of their own, each started afresh, where much of the work is Python's: in stage 3 the copper layers of a board of `PROCESS_MIN_NETS` nets or more (1,000), in stage 6 the parts built at once in simulation mode and the parts sliced for the visual skin, in stage 7 the parts of a STEP file (`PROCESS_WORKERS` and `PROCESS_MIN_COORDINATES` below). `0` = one per processor thread the run may use (all of the machine's, unless a job scheduler, `taskset` or a container limits it); `1` = everything in turn, in one process. |
| `PROCESS_WORKERS` | `0` | int ≥ 0 | At most this many worker processes at once, in stages 3, 6 and 7; `0` = as many as `WORKERS` (a higher value is the same as `WORKERS`). Each process holds its own Python, numpy and shapely (about 36 MB) and the part it builds: NE_Delta, one of the biggest boards tried, peaks at 2.80 GB in all with 4 workers and 4.37 GB with 32 in simulation mode, and at 3.65 GB with 4 when it writes the STEP file too, whose parts the processes also work on. A thread costs little memory, so a machine with many threads and little memory can keep `WORKERS` and lower this; `1` starts no process: stages 6 and 7 build their parts in the main process, stage 3 joins the copper layers in threads, and the threads are kept. If one is stopped or runs out of memory, the parts left go to half as many processes, and to the main process once that would be one; if the processes cannot start, the main process builds them; each time with a note ([Checks, Errors And Warnings](Checks-Errors-And-Warnings.md#2013-notes-worth-knowing)). Windows holds at most 61 processes at once. |
| `PROCESS_MIN_COORDINATES` | `20000` | int ≥ 0 | Stage 6 starts worker processes only when the parts hold this many coordinates or more in all their prisms, the STEP writer only when their faces do, and stage 3 only when the copper items do, on a board of `PROCESS_MIN_NETS` nets or more ([Working Principle](Working-Principle.md#74-work-done-in-parallel)); smaller boards are built part after part in the main process, which is faster than starting the processes (about 0.3 s for 4): one of the test boards takes 0.10 s that way, and 0.35 s in processes. `0` = processes for every board of more than one part (in stage 3, of `PROCESS_MIN_NETS` nets or more). |
| `GIVE_BACK_MEMORY` | `True` | bool | Hand the memory that threads freed back to the system after each step done in threads, and in each worker process after each part (glibc's `malloc_trim`, on Linux; elsewhere nothing is done). glibc keeps a pool for each thread and holds on to what is freed in it: NE_Delta in visual mode peaks at 2.65 GB with 4 workers and 3.57 GB with 32 with this, and 3.45 GB and 4.76 GB without. Tens of milliseconds per run. |
| `SKIN_PROBES_AT_A_TIME` | `2000000` | int ≥ 1 | Visual skin, the test for hidden triangles: triangles probed at once. Their probe points and normals take about a quarter of a gigabyte; fewer take less memory and a little more time |
| `VERIFY_TRIANGLES_AT_A_TIME` | `200000` | int ≥ 1 | The Verifier's vertical rays: triangles tested at once |
| `STEP_ROWS_AT_A_TIME` | `100000` | int ≥ 1 | The STEP writer: points, edges or faces turned into text at once. The file is the same, byte for byte, whatever the size |
| `PROCESS_MIN_NETS` | `1000` | int ≥ 0 | Stage 3 joins the copper layers in processes of their own only on a board of this many nets or more, counted layer by layer (and `PROCESS_MIN_COORDINATES`), else in threads: with many nets much of the work is Python's (CIAA ACC, 6,200 nets: 13.2 s in four processes, 24.3 s in four threads); with fewer most of it is GEOS's, which threads run as fast without sending the shapes to the processes and back (NE_Delta, 804 nets: 8.0 s in threads, 9.3 s in processes) |
| `SKIN_PROBES_PER_SHARE` | `100000` | int ≥ 1 | Visual skin, the test for hidden triangles: a slice's probes are shared among up to `WORKERS` threads in shares of at least this many, each share on a copy of the slice of its own. A slice can take far longer a probe than the others (NE_Delta's core, with every via hole in it, 20 times as long: the test took 12.8 s, 11 of them on one thread, and takes 6.7 s shared); a copy of a slice and its index take about as long as 30,000 of its probes (3,200 of that core's). The result is the same whatever the value |
| `VERIFY_POLYGONS_PER_THREAD` | `2000` | int ≥ 1 | The Verifier's overlap check: fewer polygons in all are tested in one thread; more in groups of at least this many |
| `VERIFY_GROUPS_PER_WORKER` | `4` | int ≥ 1 | and up to this many groups per worker, so that a slow group is made up for by the others |
| `WORKER_STOP_WAIT_S` | `10` | s ≥ 0 | When a run stops its worker processes (an error, Ctrl+C), how long it waits at most for them to be gone, so that none writes a file after |

## 19.10 Verifier (`parameters/Run_KESE/Verifier.py`)

Whether the Verifier runs, and what it lets pass ([Checks, Errors And Warnings](Checks-Errors-And-Warnings.md#203-the-verifier)).
How many triangles its rays test at once is `Parallel.VERIFY_TRIANGLES_AT_A_TIME`.

| Name | Default | Range | Meaning |
|---|---|---|---|
| `VERIFY` | `False` | bool | Run the Verifier after generation, as `--verify` does (at most about 1.5 s more on the example boards, the checks stage 6 makes of each part included; longer on dense boards) |
| `VERIFY_RAYS` | `3000` | int ≥ 1 | Rays the Verifier casts through a visual model, along the board's normal, to test its surfaces |
| `VERIFY_VOLUME_TOLERANCE` | `1e-7` | ≥ 0 | How far a part's volumes from its faces, its slices and its mesh may differ, as a share of its volume (the numerical noise of areas and meshes), and still pass |
| `VERIFY_VOLUME_NOISE_MM3` | `1e-9` | mm³ ≥ 0 | and by this many mm³ more, whatever the volume |
| `VERIFY_OPENED_VOLUME_MM3` | `1e-3` | mm³ ≥ 0 | How much volume opening pinch points and sharing vertices may take from a part's prisms (or add), and the part still pass: in all, or else in every piece of every slice, with no piece gone |
| `VERIFY_GONE_AREA_MM2` | `1e-4` | mm² ≥ 0 | A piece this small may be gone in the piece-by-piece comparison (prisms with no slice left on them: a speck of finish that a pinch point's cut takes whole); a bigger piece gone fails the part |
| `VERIFY_MERGE_EXTRA_DIGITS` | `2` | int ≥ 0 | The closed-mesh check merges a mesh's vertices this many decimal digits finer than the snapping grid (1e-6 mm), whatever `Run.UNITS` |

## 19.11 Presets (`parameters/Run_KESE/Presets.py`)

| Name | Default | Range | Meaning |
|---|---|---|---|
| `PRESETS` | `freecad`, `elmer`, `calculix`, `openems`, `viewer`, `blender_glb`, `blender_obj` | `{name: {"Module.NAME": value}}` | Sets of overrides applied with `--for <name>`, before any `--set`. An entry is `Module.NAME: value`, `Stackup.<line>: True / False` for a line of `Stackup.py` (in both stack-ups), or one of its short names (`Stackup.finish`); each name is checked as a `--set` is, and a new entry is a new preset. A preset leaves `Stackup.FUSION_BUILD` as `Stackup.py` has it ([Choosing An Export](Choosing-An-Export.md#102-the-presets)) |

## 19.12 Step (`parameters/Fileformats/Step.py`)

The STEP files: true arcs and cylinders, and what counts as an arc. The file's units are `Run.UNITS`;
how many rows the writer turns into text at once is `Parallel.STEP_ROWS_AT_A_TIME`.

| Name | Default | Range | Meaning |
|---|---|---|---|
| `STEP_EXACT_ARCS` | `True` | bool | Write circles and arcs as true curves: where a part's outline runs through vertices on one circle (holes, vias, round pads, track ends, arc tracks, round outlines), their chords become one `CIRCLE` edge and the walls on them one `CYLINDRICAL_SURFACE` face, at every height alike; every other edge stays a line and every other face a plane. Left straight where another edge at that height passes closer to the vertices than the arc bulges out from them, which the arc would cross. Written by KESE's own writer; files are about 2.5 to 3 times smaller (the RF module in `Input/`, in m: 117 MB instead of 335 MB, written in 2.2 s against 3.2 s, measured with `CIRCLE_CHORD_TOLERANCE_MM = 0.002`). Meshes are unchanged |
| `STEP_ARC_FIT_TOLERANCE_MM` | `0.0002` | mm > 0 | Vertices within this of one circle form an arc (2 x the snap grid) |
| `STEP_ARC_MIN_POINTS` | `5` | int ≥ 3 | An arc runs through at least this many vertices |
| `STEP_ARC_MIN_SWEEP_DEG` | `10.0` | degrees | and turns at least this far |
| `STEP_ARC_MAX_TURN_DEG` | `30.0` | degrees | but at most this far at one vertex, so that a polygon of fewer than 12 sides (an octagonal pad, a square) stays a polygon |
| `STEP_ARC_TURN_RATIO_MAX` | `1.3` | ≥ 1 | and evenly, as a faceted circle does: no chord of the arc spans more than this many times the median chord's angle about the centre |
| `STEP_ARC_TURN_RATIO_MIN` | `0.7` | 0 to 1 | and none but the first and last less than this many times (those two may be shorter, where a boolean cut the arc) |
| `STEP_ARC_MAX_SWEEP_DEG` | `181.0` | degrees > 0 | A longer arc is cut into the fewest pieces that keep each about this long, at vertices spread evenly (a piece can run up to one chord over). A whole circle is two arcs on one `CIRCLE`; below 180 it is cut into more, each on a circle of its own |

Every format holds the same parts: the ones whose line in
[Stackup](#191-stackup-parameterspcb_elementsstackuppy) is `True` (the solder mask and the silkscreen
are `False` by default). A STEP file with the mask and silkscreen is 1.4 to 1.9 times as big
(the PCIe card in `Input/`, in mm: 151 MB and 1,024 solids written in 2.9 s, against 81 MB and 788 solids
in 1.9 s without them, measured with `Geometry.CIRCLE_CHORD_TOLERANCE_MM = 0.002`).

With `STEP_EXACT_ARCS` the file uses these entities beside the planar ones: `CIRCLE` (on an
`AXIS2_PLACEMENT_3D` at the centre, its axis the board's normal), referenced by the `EDGE_CURVE` of
an arc edge whose sense says which way it runs, and `CYLINDRICAL_SURFACE` (on the circle's placement
at the wall's lower height) under the `ADVANCED_FACE` of a curved wall. An arc turns at most about
half a circle (`STEP_ARC_MAX_SWEEP_DEG`): a whole circle is two arcs between two vertices, on one
`CIRCLE`, so there are no seam edges and every edge has two vertices and two faces.

An arc is written only where nothing can cross it, since its bulge is up to
`Geometry.CIRCLE_CHORD_TOLERANCE_MM` off its chords; these three settings say when:

| Name | Default | Range | Meaning |
|---|---|---|---|
| `STEP_ARC_CHECK_FACTOR` | `3.0` | ≥ 0 | An arc is dropped where a vertex lies further from its written circle than this many times `STEP_ARC_FIT_TOLERANCE_MM` |
| `STEP_STRIP_MAX_TURN_DEG` | `45.0` | degrees > 0 | The strip kept clear around an arc is drawn with corners at most this far apart about its centre (closer where its margin needs) |
| `STEP_TANGENT_MM` | `5e-8` | mm ≥ 0 | An edge that leaves an arc's end and cuts into its circle by less than this only touches the arc, as a line along its tangent does (OpenCascade takes two curves within about 2e-7 of the file's unit for touching: in mm, the stricter unit, 2e-7 mm) |

## 19.13 Mesh (`parameters/Fileformats/Mesh.py`)

The mesh files GLB, STL and OBJ: normals and shading. The files' units are `Run.UNITS`; how finely a
curve is cut into flat faces is in [19.8 Geometry](#198-geometry-parametersrun_kesegeometrypy), and
every colour is in its element's file.

| Name | Default | Range | Meaning |
|---|---|---|---|
| `EXPORT_INCLUDE_NORMALS` | `True` | bool | Write vertex normals in the GLB (OBJ always has them) |
| `EXPORT_SET_BUFFERVIEW_TARGETS` | `True` | bool | Set glTF bufferView targets, which keeps the Khronos validator report free of hints |
| `SMOOTH_SHADE_ANGLE_DEG` | `25.0` | degrees | Edges sharper than this stay crisp; flatter ones (cylinders) shade smooth |

## 19.14 Names Of Before 25.2

Version 25.2 put the parameter files into the three folders above, made every part's switch a line
of `Stackup.py`, gave each element's file its own colours and split the copper's settings by top,
inner and bottom. Of the 166 settings of before, 130 kept their name and their module, 35 have a
new name or module and one is gone. An old name still works in `--set` and in a preset: the run
uses the value under the new name, and `report.txt` notes it.

| Old name | Now |
|---|---|
| `Silkscreen.<NAME>` (13 settings) | `SilkScreen.<NAME>`: the module has the file's name, `SilkScreen.py` |
| `Silkscreen.SILKSCREEN_ENABLED` | The lines `top_silkscreen` and `bottom_silkscreen` of `Stackup.py` |
| `SolderMask.SOLDER_MASK_ENABLED` | The lines `top_solder_mask` and `bottom_solder_mask` |
| `Finish.FINISH_ENABLED` | The lines `top_finish`, `bottom_finish` and `hole_finish` |
| `Copper.COPPER_ENABLED` | The lines `top_copper`, `inner_copper`, `bottom_copper` and `plated_holes` |
| `Copper.VIA_RESIN_ENABLED` | The line `via_resin` |
| `Board.BOARD_ENABLED` | The lines `board` (plies fused), `prepreg_plies` and `cores` (plies separate) |
| `Board.RESIN_FILL_BETWEEN_INNER_COPPER` | The line `resin_between_traces` |
| `Copper.DEFAULT_OUTER_FOIL_MM` | `Copper.DEFAULT_TOP_FOIL_MM` and `Copper.DEFAULT_BOTTOM_FOIL_MM` |
| `Copper.OUTER_PLATING_ADDED_MM` | `Copper.TOP_PLATING_ADDED_MM` and `Copper.BOTTOM_PLATING_ADDED_MM` |
| `Copper.ETCH_FACTOR` | `Copper.TOP_ETCH_FACTOR` and `Copper.BOTTOM_ETCH_FACTOR` |
| `Copper.ETCH_APPLY_TO_INNER_LAYERS` | `Copper.INNER_ETCH_FACTOR`: `True` gives the inner copper the top's factor, `False` gives it 0, in either order of `--set` |
| `Copper.COPPER_SURFACE_ROUGHNESS_UM` | `Copper.COPPER_ROUGHNESS_RMS_TREATED_UM` and `Copper.COPPER_ROUGHNESS_RMS_OTHER_UM` |
| `Copper.VIA_TENTING` | `SolderMask.VIA_TENTING` |
| `Color.VISUAL_MASK_OPAQUE` | `SolderMask.VISUAL_MASK_OPAQUE` |
| `Color.USE_STACKUP_COLORS` | `SolderMask.USE_STACKUP_MASK_COLOR` and `SilkScreen.USE_STACKUP_SILK_COLOR` |
| `Color.STACKUP_MASK_COLORS`, `Color.STACKUP_MASK_OVER_COPPER_COLORS`, `Color.USER_MASK_OVER_COPPER_LIGHTEN` | The same names in `SolderMask` |
| `Color.STACKUP_SILK_COLORS` | `SilkScreen.STACKUP_SILK_COLORS` |
| `Color.MATERIALS` | Gone: every colour is a setting of its own in its element's file (`Board.CORE_COLOR`, `Copper.COPPER_COLOR`, `Finish.FINISH_COLORS`, `SolderMask.TOP_MASK_COLOR`, `SilkScreen.TOP_SILK_COLOR` and the others in the Color tables above). `--set Color.MATERIALS=...` stops the run with a message that lists them |
| `Run.EXPORT_INCLUDE_NORMALS`, `Run.EXPORT_SET_BUFFERVIEW_TARGETS`, `Run.SMOOTH_SHADE_ANGLE_DEG` | The same names in `Mesh` |

Names that moved in earlier versions still work too: `Run.WORKERS` is `Parallel.WORKERS`,
`Run.STEP_EXACT_ARCS` and the other four STEP settings that were in `Run` are in `Step`,
`Run.VERIFY`, `Run.VERIFY_RAYS`, `Run.VERIFY_VOLUME_TOLERANCE` and `Run.VERIFY_OPENED_VOLUME_MM3` are
in `Verifier`, and `Run.PRESETS` is `Presets.PRESETS`.

> [!NOTE]
> A value edited under an old name in a parameter file would do nothing, so the run refuses it
> instead: a parameter file that still sets one of the old names stops the run with a message that
> names the new setting and its file, and a file of before 25.2 left in `parameters/` itself
> (`parameters/copper.py`, `parameters/color.py` and the other ten) stops it with
> `parameters/copper.py is not read any more: its settings are now in
> parameters/PCB_elements/Copper.py: move your values there and delete it`.

| Previous | Next |
|:---|---:|
| [Feature Test Collection](Feature-Test-Collection.md) | [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md) |
