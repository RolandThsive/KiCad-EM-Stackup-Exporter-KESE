# 16. Parameter Reference

Every setting lives in one of eight files in `Parameters/`. These are the only files you edit.
Units are mm unless a name says otherwise. The **Range** column is what the program uses
sensibly; "None" means the program works the value out itself. Every value is recorded in the
`parameters.txt` written next to each output, and any value can be overridden for one run with
`--set Module.NAME=value`, where `Module` is the short name in the heading of each section.

> [!NOTE]
> Defaults are those of the parameter files on `main`. KESE does not validate ranges: a value
> outside the range below produces a wrong model or an error from the geometry library, not a
> named check.

## 16.1 Run (`Run_Parameters.py`)

What to make, where, and in which formats.

### 16.1.1 Mode, Folders And Formats

| Name | Default | Range | Meaning |
|---|---|---|---|
| `MODE` | `"simulation"` | `"simulation"` / `"visual"` | Closed solids for solvers, or the visible surface for viewers ([Output Modes](Output-Modes.md)) |
| `INPUT_DIR`, `OUTPUT_DIR` | `"Input"`, `"Output"` | paths relative to the project root | Where boards are looked for and outputs written |
| `FILE_FORMAT` | `["glb"]` | any of `"glb"`, `"stl"`, `"obj"`, `"step"` | Files to write; visual mode allows only glb and obj |
| `UNITS` | `"m"` | `"mm"` / `"m"` | Units of the written files |
| `ORIGIN` | `"center"` | `"center"` / `"kicad"` | Outline centre at (0, 0), or KiCad's page origin kept |
| `ORIENTATION` | `"upright"` | `"upright"` / `"flat"` | Board in XY with `F.Cu` toward +Z, or in XZ with `F.Cu` toward +Y |

### 16.1.2 Grouping

| Name | Default | Range | Meaning |
|---|---|---|---|
| `COPPER_GROUPING` | `"net"` | `"net"` / `"layer"` / `"merged"` | One copper solid per net, per layer (plating separate), or one in all |
| `DIELECTRIC_GROUPING` | `"layer"` | `"layer"` / `"merged"` | One solid per core / prepreg, or the whole laminate as one |

### 16.1.3 Run Behaviour

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SHOW_PROGRESS` | `True` | bool | Live `running <stage> ... 1m 23s` line on a terminal |
| `VERIFY` | `False` | bool | Run the Verifier after generation (10 to 60 s per board) |
| `WRITE_MATERIALS_JSON` | `True` | bool | Write `materials.json` next to the outputs |

### 16.1.4 Mesh Export (GLB, STL, OBJ)

| Name | Default | Range | Meaning |
|---|---|---|---|
| `EXPORT_INCLUDE_NORMALS` | `True` | bool | Write vertex normals |
| `EXPORT_SET_BUFFERVIEW_TARGETS` | `True` | bool | Set glTF bufferView targets, which keeps the Khronos validator report free of hints |
| `SMOOTH_SHADE_ANGLE_DEG` | `25.0` | degrees | Edges sharper than this stay crisp; flatter ones (cylinders) shade smooth |

### 16.1.5 STEP Export

| Name | Default | Range | Meaning |
|---|---|---|---|
| `STEP_EXACT_ARCS` | `True` | bool | Runs of vertices on one circle (vias, round pads, round outlines, track ends, arc tracks) are written as true arcs; smaller files, real cylinders in CAD |
| `STEP_ARC_FIT_TOLERANCE_MM` | `0.0002` | mm > 0 | Vertices within this of one circle form an arc (2 × the snap grid) |
| `STEP_ARC_MIN_POINTS` | `5` | int ≥ 3 | Minimum vertices in a run |
| `STEP_WRITE_ROLES` | `["board", "copper", "plating", "finish"]` | subset of the roles below | Roles written to the STEP file; mask and silk are left out by default since on a dense board they are thousands of solids and need many GB of memory |
| `STEP_FUSE_ROLES` | `["board", "copper", "plating", "finish"]` | subset of `STEP_WRITE_ROLES` | Roles whose parts are fused into **one** solid each (what solvers need; slow on parts with many pieces); the others are compounds of touching solids (fast; fine for viewing) |

The roles are `board`, `copper`, `plating`, `finish`, `mask`, `mask_over_copper`, `silk`.

### 16.1.6 KiCad Versions And Presets

| Name | Default | Range | Meaning |
|---|---|---|---|
| `KICAD_VERSION_MIN`, `KICAD_VERSION_MAX` | `20211014`, `20260206` | KiCad file format numbers | Tested range (KiCad 6 to 10); the Reader warns outside it |
| `PRESETS` | `hfss`, `cst`, `openems`, `viewer` | `{name: {"Module.NAME": value}}` | Sets of overrides applied with `--for <name>` ([Choosing An Export](Choosing-An-Export.md)) |

## 16.2 Board (`Board_Parameters.py`)

The laminate: thickness, dielectrics, outline and holes. Details in [Board](Board.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `BOARD_THICKNESS_MM` | `None` | None or mm > 0 | Laminate thickness; `None` takes it from the file (stack-up, else `(general (thickness))`) |
| `DIELECTRIC_SPLIT` | `"even"` | `"even"` | How the laminate is divided between copper layers when the file has no stack-up |
| `DEFAULT_DIELECTRIC_MATERIAL`, `DEFAULT_DIELECTRIC_TYPE` | `"FR4"`, `"core"` | text; `"core"` / `"prepreg"` | Used when the stack-up gives none |
| `DEFAULT_EPSILON_R`, `DEFAULT_LOSS_TANGENT` | `4.5`, `0.02` | > 0 | Typical FR4 at 1 GHz, used when the stack-up gives none |
| `USE_STACKUP_EPSILON_R`, `USE_STACKUP_LOSS_TANGENT` | `True`, `True` | bool | Stack-up values win over the defaults when present |
| `RESIN_FILL_BETWEEN_INNER_COPPER` | `True` | bool | Prepreg resin fills the space between inner copper traces |
| `INCLUDE_NON_PLATED_HOLES` | `True` | bool | NPTH pads become holes through the board |
| `OUTLINE_LINE_SNAP_MM` | `1e-5` | mm > 0 | `Edge.Cuts` end points closer than this are joined |
| `OUTLINE_FALLBACK` | `"copper_hull"` | `"copper_hull"` / `"error"` | Without `Edge.Cuts`: convex hull of the copper plus a margin, or stop |
| `OUTLINE_FALLBACK_MARGIN_MM` | `1.0` | mm ≥ 0 | Margin of the fallback hull |

## 16.3 Copper (`Copper_Parameters.py`)

Copper foils, plating, vias and the finished copper geometry. Details in
[Copper And Traces](Copper-And-Traces.md).

### 16.3.1 Thickness And Plating

| Name | Default | Range | Meaning |
|---|---|---|---|
| `DEFAULT_OUTER_FOIL_MM`, `DEFAULT_INNER_FOIL_MM` | `0.035`, `0.035` | mm > 0 | Foil when the stack-up gives none (1 oz = 0.035, 0.5 oz = 0.0175) |
| `USE_STACKUP_COPPER_THICKNESS` | `True` | bool | Stack-up `(layer "F.Cu" (thickness ...))` wins when present |
| `OUTER_PLATING_ADDED_MM` | `0.0` | mm ≥ 0 | Electroplated copper added to the outer layers; typical 0.020; 0 = foil only, as KiCad models |
| `VIA_WALL_MM` | `0.025` | mm > 0 | Plated wall of vias (typical 0.020 to 0.025) |
| `PTH_WALL_MM` | `0.025` | mm > 0 | Plated wall of through-hole pads |

### 16.3.2 Etch Factor

| Name | Default | Range | Meaning |
|---|---|---|---|
| `ETCH_FACTOR` | `0.0` | ≥ 0 | Each side wall leans in by this × copper thickness over the copper height; 0 = rectangular, as KiCad |
| `ETCH_STEPS` | `4` | int ≥ 1 | Slices the trapezoid is built from |
| `ETCH_APPLY_TO_INNER_LAYERS` | `False` | bool | Etch inner copper too (foot toward the board centre) |

### 16.3.3 Castellations And Edge Plating

| Name | Default | Range | Meaning |
|---|---|---|---|
| `CASTELLATION` | `"auto"` | `"auto"` / `"file"` / `"off"` | Plated holes crossing `Edge.Cuts`: always plated as castellations, only when the stack-up says `(castellated_pads yes)`, or not plated |
| `CASTELLATION_WALL_MM` | `0.025` | mm > 0 | Plated wall of a castellation |
| `EDGE_PLATING` | `"file"` | `"file"` / `"yes"` / `"no"` | Copper on the routed edge: follow `(edge_plating yes)`, always, never |
| `EDGE_PLATING_WALL_MM` | `0.025` | mm > 0 | Width of the edge band inside the outline |
| `EDGE_PLATING_NET` | `"auto"` | `"auto"` or a net name | Net of the edge copper; `"auto"` = the named net with the most copper touching the band |

### 16.3.4 Vias And Nets

| Name | Default | Range | Meaning |
|---|---|---|---|
| `VIA_TENTING` | `"file"` | `"file"` / `"tented"` / `"open"` | Mask over vias: follow the board, cover all, open all |
| `HONOUR_REMOVE_UNUSED_LAYERS` | `True` | bool | Drop via annular rings on layers nothing connects to, as KiCad's option does |
| `NO_NET_NAME` | `"no_net"` | text | Name of copper that belongs to no net |

### 16.3.5 Electrical Properties

| Name | Default | Range | Meaning |
|---|---|---|---|
| `COPPER_CONDUCTIVITY_S_PER_M` | `5.8e7` | S/m | Written to `materials.json` for every copper part |
| `COPPER_SURFACE_ROUGHNESS_UM` | `0.0` | µm ≥ 0 | Written to `materials.json`; 0 = ignore; e.g. 1.5 for standard foil. A solver setting, not geometry |

## 16.4 Solder Mask (`SolderMask_Parameters.py`)

Short name `SolderMask`. Details in [Solder Masks](Solder-Masks.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `MASK_OVER_LAMINATE_MM` | `0.010` | mm > 0 | Mask thickness over bare laminate (typical 0.020 to 0.030) |
| `MASK_OVER_COPPER_MM` | `0.010` | mm > 0 | Mask thickness on top of copper (typical 0.010 to 0.015) |
| `USE_STACKUP_MASK_THICKNESS` | `True` | bool | The stack-up's one mask value is used for both when present |
| `MASK_EDGE_PULLBACK_MM` | `0.005` | mm ≥ 0 | Mask and silk stop this far short of the board edge |
| `PAD_TO_MASK_CLEARANCE_MM` | `None` | None or mm ≥ 0 | Clearance around pads; `None` follows the board file (pad, footprint, board setup) |
| `MASK_WALL_QUAD_SEGS` | `4` | int ≥ 1 | Segments per quarter circle on the walls where the mask climbs a trace |

## 16.5 Silkscreen (`Silkscreen_Parameters.py`)

Details in [Silkscreens](Silkscreens.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SILK_THICKNESS_MM` | `0.010` | mm > 0 | Ink thickness (typical 0.010 to 0.020) |
| `SILKSCREEN_OVER_COPPER` | `False` | bool | Keep ink where the mask is open; `False` clips it off the pads as fabricators do |
| `FONT_FILE` | `None` | None or a file in `Parameters/Fonts/` | Custom stroke-font JSON or Hershey `.jhf`; `None` = KiCad newstroke |
| `DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT` | `True` | bool | Text in a TrueType face is drawn with the stroke font |
| `INTERLINE_PITCH` | `1.68` | > 0 | Line pitch as a multiple of the text height (KiCad's value) |
| `INTERLINE_LEGACY_FACTOR` | `0.9583` | > 0 | KiCad's correction for stroke fonts |
| `INTER_CHAR_SPACING` | `0.2` | ≥ 0 | Extra advance between glyphs, as a fraction of the text width |
| `ITALIC_TILT` | `0.125` | ≥ 0 | x shift per unit of y for italic text |
| `BOLD_THICKNESS_RATIO`, `NORMAL_THICKNESS_RATIO` | `0.2`, `0.15` | > 0 | Stroke thickness as a fraction of the text height when the file gives none |
| `TEXT_STROKE_QUAD_SEGS` | `4` | int ≥ 1 | Roundness of stroke ends |
| `DRAW_HIDDEN_TEXT` | `False` | bool | Draw text marked `(hide yes)` |
| `SILK_LAYERS` | `["F.SilkS", "B.SilkS"]` | list of layer names | Layers drawn as silkscreen; others are listed as skipped |

## 16.6 Finish (`Finish_Parameters.py`)

Details in [Top And Bottom Copper Finishings](Copper-Finishings.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `FINISH_ENABLED` | `False` | bool | Build the surface finish on bare copper |
| `FINISH_TYPE` | `"file"` | `"file"` or a key of `FINISH_TYPES` | Take the type from the stack-up's `(copper_finish ...)`, or name it |
| `FINISH_DEFAULT_TYPE` | `"ENIG"` | a key of `FINISH_TYPES` | Type when the file gives none |
| `FINISH_GROUPING` | `"metal"` | `"metal"` / `"net"` | One part per side and metal, or per side, metal and net |
| `FINISH_TYPES` | ENIG, HASL, HASL_LF, OSP, ImmersionSilver, ImmersionTin, HardGold | `{key: [(metal, mm), ...]}` bottom to top | Layers of each finish |
| `FINISH_CONDUCTIVITY_S_PER_M` | Nickel `1.4e7`, Gold `4.1e7`, Tin `9.1e6`, Silver `6.3e7`, OSP `0.0` | `{metal: S/m}` | Written to `materials.json` |

## 16.7 Geometry (`Geometry_Parameters.py`)

Numerical quality: how finely curves are faceted and how neighbouring layers share exact edges.
These do not change dimensions.

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SNAP_GRID_MM` | `0.0001` | mm > 0 | All 2D shapes are snapped to this grid (0.1 µm) so touching layers share identical vertices: no hairline gaps, no T-junctions |
| `SIMPLIFY_TOLERANCE_MM` | `0.0005` | mm ≥ 0 | Simplification of copper outlines after union; 0 = none |
| `ARC_STEP_DEG` | `3.0` | degrees > 0 | Maximum angle per segment when flattening arcs |
| `CIRCLE_CHORD_TOLERANCE_MM` | `0.002` | mm > 0 | Maximum deviation of a flattened circle from the true one |
| `CIRCLE_MIN_QUAD_SEGS`, `CIRCLE_MAX_QUAD_SEGS` | `8`, `128` | int | Bounds on segments per quarter circle |
| `TRACK_END_MIN_QUAD_SEGS` | `4` | int ≥ 1 | Roundness of track ends |
| `BEZIER_SEGMENTS` | `32` | int ≥ 1 | Straight pieces per Bézier curve |
| `PINCH_POINT_OPENING_MM` | `1e-4` | mm > 0 | Polygons whose rings touch at a single point are opened by this much so they can be meshed |
| `SKIN_BURIED_TEST_OFFSET_MM` | `0.0005` | mm > 0 | Visual mode: a face is dropped if a point this far outside it lies inside another solid |

## 16.8 Color (`Color_Parameters.py`)

The look of every part for GLB and OBJ. Details in [Colorizing](Colorizing.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `MATERIALS` | 19 entries (Board, Board_core, Board_prepreg, Copper, Copper_exposed, Plating, the masks, mask over copper, silkscreens, Nickel, Gold, Tin, Silver, OSP) | `{key: {color hex, alpha 0-1, metallic 0-1, roughness 0-1}}` | Material of each part kind; alpha < 1 writes a glTF BLEND material |
| `VISUAL_MASK_OPAQUE` | `True` | bool | In visual mode the mask is opaque whatever its alpha |
| `USE_STACKUP_COLORS` | `True` | bool | Honour the colour names in the board's stack-up |
| `STACKUP_MASK_COLORS` | 11 names | `{name: hex}` | Mask colour names |
| `STACKUP_SILK_COLORS` | white, black, yellow | `{name: hex}` | Silkscreen colour names |
| `STACKUP_MASK_OVER_COPPER_COLORS` | 11 names | `{name: hex}` or `None` | Visual-mode colour of the mask over copper per stack-up colour |

| Previous | Next |
|:---|---:|
| [Solder Masks](Solder-Masks.md) | [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md) |
