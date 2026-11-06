# 16. Parameter Reference

Every setting lives in one of twelve files in `parameters/`. These are the only files you edit.
Units are mm unless a name says otherwise. The **Range** column is what the program uses
sensibly; "None" means the program works the value out itself. Any value can be overridden for
one run with `--set Module.NAME=value`, where `Module` is the short name in the heading of each
section. The `parameters.txt` written next to each output records every value as it stood for
the run: `--for`, `--set`, `--mode`, `--format` and `--verify` are all applied as overrides first,
and listed on its first line.

> [!NOTE]
> Defaults are those of the parameter files on `main`. Before the board is read, the run checks
> `MODE`, `FILE_FORMAT`, the settings of `parameters/parallel.py`, the rounds, counts, digits and
> margins of `parameters/geometry.py`, the Verifier's tolerances, rays and merge digits, the finish's
> mitre limit, the STEP arcs' settings that count or divide, the names in the preset of `--for`,
> every setting whose range below is a few words with `/` between them (such as `"mm"` / `"m"`), and
> the kind of every value: `True` or `False` where the file has one of them, a number where it has a
> number, text, a list or a dict likewise (a setting that is `None` in its file takes any value). It
> stops with an error that names the setting.
> `FINISH_TYPE` and `DIELECTRIC_SPLIT` are checked where they are used (an error or a warning), and
> `FONT_FILE` gives a note in `report.txt`. For the rest, a value outside the range below produces
> a wrong model or a plain Python error, not a named check.

## 16.1 Run (`parameters/run.py`)

What to make, where, and in which formats.

### 16.1.1 Mode, Folders And Formats

| Name | Default | Range | Meaning |
|---|---|---|---|
| `MODE` | `"simulation"` | `"simulation"` / `"visual"` | Closed solids for solvers, or the visible surface for viewers ([Output Modes](Output-Modes.md)) |
| `INPUT_DIR`, `OUTPUT_DIR` | `"Input"`, `"Output"` | paths relative to the current working directory (run from the `Generator/` folder) | Where boards are looked for and outputs written |
| `FILE_FORMAT` | `["glb"]` | any of `"glb"`, `"stl"`, `"obj"`, `"step"` | Files to write; visual mode allows only glb and obj |
| `UNITS` | `"m"` | `"mm"` / `"m"` | Units of the written files. Use `"mm"` for STEP, as CAD tools and solvers expect; the STEP file declares the units it is written in |
| `ORIGIN` | `"center"` | `"center"` / `"kicad"` | Outline centre at (0, 0), or KiCad's page origin kept |
| `ORIENTATION` | `"upright"` | `"upright"` / `"flat"` | Board in XY with `F.Cu` toward +Z, or in XZ with `F.Cu` toward +Y |

### 16.1.2 Run Behaviour

How many threads and processes work at once is set in [16.9 Parallel](#169-parallel-parametersparallelpy), the
STEP files' own settings in [16.10 Step](#1610-step-parameterssteppy), the Verifier's in
[16.11 Verifier](#1611-verifier-parametersverifierpy) and the presets in [16.12 Presets](#1612-presets-parameterspresetspy).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SHOW_PROGRESS` | `True` | bool | Live `running <stage> ... 1m 23s` line on a terminal |
| `WRITE_MATERIALS_JSON` | `True` | bool | Write `materials.json` next to the outputs |

### 16.1.3 Mesh Export (GLB, STL, OBJ)

| Name | Default | Range | Meaning |
|---|---|---|---|
| `EXPORT_INCLUDE_NORMALS` | `True` | bool | Write vertex normals in the GLB (OBJ always has them) |
| `EXPORT_SET_BUFFERVIEW_TARGETS` | `True` | bool | Set glTF bufferView targets, which keeps the Khronos validator report free of hints |
| `SMOOTH_SHADE_ANGLE_DEG` | `25.0` | degrees | Edges sharper than this stay crisp; flatter ones (cylinders) shade smooth |

### 16.1.4 KiCad Versions

| Name | Default | Range | Meaning |
|---|---|---|---|
| `KICAD_VERSION_MIN`, `KICAD_VERSION_MAX` | `3`, `20260206` | KiCad file format numbers | Tested range, from the 2013 builds before KiCad 4 (format 3) to KiCad 10 (KiCad 4 files say `(version 4)`, KiCad 5 files `20171130`); a file outside it is read with a warning ([Compatibility](Compatibility.md#201-kicad-files)) |
| `TESTED_COPPER_LAYERS` | `8` | int > 0 | Stage 1 warns above this many copper layers (the most among the test boards); they are still modelled |

## 16.2 Board (`parameters/board.py`)

The laminate: thickness, dielectrics, outline and holes. Details in [Board](Board.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `DIELECTRIC_GROUPING` | `"layer"` | `"layer"` / `"merged"` | One solid per core / prepreg, or the whole laminate as one |
| `BOARD_ENABLED` | `True` | bool | Build the laminate (the `Board` parts) and write it to every file |
| `BOARD_THICKNESS_MM` | `None` | None or mm > 0 | Laminate thickness; `None` takes it from the file (a usable stack-up, else `(general (thickness))` less the outer copper and the masks, else 1.6 mm less the same) |
| `DEFAULT_BOARD_THICKNESS_MM` | `1.6` | mm > 0 | Finished board thickness when the file gives none (KiCad's default) |
| `DIELECTRIC_SPLIT` | `"even"` | `"even"` | How the laminate is divided between copper layers when the file has no usable stack-up |
| `DEFAULT_DIELECTRIC_MATERIAL`, `DEFAULT_DIELECTRIC_TYPE` | `"FR4"`, `"core"` | text; `"core"` / `"prepreg"` | Used when the stack-up gives none |
| `DEFAULT_EPSILON_R`, `DEFAULT_LOSS_TANGENT` | `4.5`, `0.02` | > 0 | Typical FR4 at 1 GHz, used when the stack-up gives none |
| `USE_STACKUP_EPSILON_R`, `USE_STACKUP_LOSS_TANGENT` | `True`, `True` | bool | Stack-up values win over the defaults when present |
| `RESIN_FILL_BETWEEN_INNER_COPPER` | `True` | bool | `True`: fill the space beside inner copper from the adjacent prepreg (otherwise from the dielectric above); `False`: those pockets stay empty and `report.txt` notes it (see [Board](Board.md#102-resin-fill-beside-inner-copper)) |
| `INCLUDE_NON_PLATED_HOLES` | `True` | bool | NPTH pads become holes through the board |
| `OUTLINE_LINE_SNAP_MM` | `0.01` | mm > 0 | Open `Edge.Cuts` line and arc ends closer than this are joined, as KiCad joins them (its chaining distance is 0.01 mm) |
| `OUTLINE_FALLBACK` | `"copper_hull"` | `"copper_hull"` / `"error"` | When `Edge.Cuts` gives no closed ring at all: convex hull of the copper plus a margin, or stop |
| `OUTLINE_FALLBACK_MARGIN_MM` | `1.0` | mm ≥ 0 | Margin of the fallback hull |
| `OUTLINE_DUPLICATE_AREA_MM2` | `1e-6` | mm² > 0 | Two closed `Edge.Cuts` outlines that differ by less than this area are one (a ring drawn twice) |
| `OUTLINE_MIN_AREA_MM2` | `1e-9` | mm² ≥ 0 | A closed `Edge.Cuts` outline of this area or less is left out (a line drawn there and back, a circle of no size) |

## 16.3 Copper (`parameters/copper.py`)

Copper foils, plating, vias and the finished copper geometry. Details in
[Copper And Traces](Copper-And-Traces.md).

### 16.3.1 Thickness And Plating

| Name | Default | Range | Meaning |
|---|---|---|---|
| `COPPER_GROUPING` | `"net"` | `"net"` / `"layer"` / `"merged"` | One copper solid per net, per layer (plating separate), or one in all |
| `COPPER_ENABLED` | `True` | bool | Build the copper (layers and the plated barrels of holes and vias) and write it to every file |
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
| `ETCH_UNETCHED_REACH` | `1.5` | ≥ 0 | Copper within this × the etch inset of a hole wall or the board edge keeps its outline |

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
| `HONOUR_REMOVE_UNUSED_LAYERS` | `True` | bool | Drop via and through-hole pad annular rings on layers nothing connects to, as KiCad's option does |
| `NO_NET_NAME` | `"no_net"` | text | Name of copper that belongs to no net |
| `HAIRLINE_HOLE_MM` | `1e-3` | mm ≥ 0 | A hole in one net's copper narrower than this on average (2 × area / perimeter) is filled: the hair-wide gap KiCad leaves between a zone fill and a pad of its own net |

### 16.3.5 Electrical Properties

| Name | Default | Range | Meaning |
|---|---|---|---|
| `COPPER_CONDUCTIVITY_S_PER_M` | `5.8e7` | S/m | Written to `materials.json` for every copper part |
| `COPPER_SURFACE_ROUGHNESS_UM` | `0.0` | µm ≥ 0 | Written to `materials.json`; 0 = ignore; e.g. 1.5 for standard foil. A solver setting, not geometry |

## 16.4 Solder Mask (`parameters/solder_mask.py`)

Short name `SolderMask`. Details in [Solder Masks](Solder-Masks.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SOLDER_MASK_ENABLED` | `False` | bool | Build the solder mask and write it to every file (off by default: many more solids, much bigger STEP files) |
| `MASK_OVER_LAMINATE_MM` | `0.010` | mm > 0 | Mask thickness over bare laminate (typical 0.020 to 0.030) |
| `MASK_OVER_COPPER_MM` | `0.010` | mm > 0 | Mask thickness on top of copper (typical 0.010 to 0.015) |
| `USE_STACKUP_MASK_THICKNESS` | `True` | bool | The first mask thickness found in the stack-up (normally `F.Mask`'s) is used for both values on both faces |
| `MASK_EDGE_PULLBACK_MM` | `0.005` | mm ≥ 0 | Mask and silk stop this far short of the board edge |
| `PAD_TO_MASK_CLEARANCE_MM` | `None` | None or mm ≥ 0 | Clearance around pads and untented vias; `None` takes the board setup's value from the file. A number replaces only the board setup's value: a pad's or footprint's own `solder_mask_margin` in the file still wins |
| `MASK_MIN_WIDTH_MM` | `None` | None or mm ≥ 0 | Narrowest web of mask kept between two openings; `None` follows Board Setup (`solder_mask_min_width`), 0 keeps every web |
| `MASK_WEB_HAIRLINE_MM` | `1e-3` | mm ≥ 0 | A web the minimum width adds that is narrower than twice this is dropped |
| `MASK_OVER_COPPER_HAIRLINE_MM` | `1e-3` | mm ≥ 0 | A piece of mask on top of copper narrower than twice this is left out, and the finish covers it instead: the slivers left where an opening's outline follows the copper's with other points ([Solder Masks](Solder-Masks.md#152-conformal-mask)); 0 keeps them |
| `MASK_WALL_QUAD_SEGS` | `4` | int ≥ 1 | Segments per quarter circle on the walls where the mask climbs a trace |

## 16.5 Silkscreen (`parameters/silkscreen.py`)

Details in [Silkscreens](Silkscreens.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SILKSCREEN_ENABLED` | `False` | bool | Build the silkscreen and write it to every file (off by default) |
| `SILK_THICKNESS_MM` | `0.010` | mm > 0 | Ink thickness (typical 0.010 to 0.020) |
| `SILKSCREEN_OVER_COPPER` | `False` | bool | Keep ink where the mask is open; `False` clips it off the pads as fabricators do. With `True` the ink lies on the copper and the finish is left out under it |
| `FONT_FILE` | `None` | None or a file in `kese/assets/fonts/` | Custom stroke-font JSON or Hershey `.jhf`; `None` = KiCad newstroke |
| `DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT` | `True` | bool | Text in a TrueType face with no usable `render_cache` is drawn with the stroke font |
| `INTERLINE_PITCH` | `1.68` | > 0 | Line pitch as a multiple of the text height (KiCad's value) |
| `INTERLINE_LEGACY_FACTOR` | `0.9583` | > 0 | KiCad's correction for stroke fonts |
| `ITALIC_TILT` | `0.125` | ≥ 0 | x shift per unit of y for italic text |
| `BOLD_THICKNESS_RATIO`, `NORMAL_THICKNESS_RATIO` | `0.2`, `0.125` | > 0 | Stroke thickness as a fraction of the text width when the file gives none (KiCad's `GetPenSizeForBold` and `GetPenSizeForNormal`) |
| `MAX_PEN_RATIO` | `0.25` | > 0 | A stroke is at most this × the smaller of the text's width and height, whatever the file says (KiCad's `ClampTextPenSize`) |
| `TEXT_STROKE_QUAD_SEGS` | `4` | int ≥ 1 | Roundness of stroke ends |
| `DRAW_HIDDEN_TEXT` | `False` | bool | Draw text marked `(hide yes)` |
| `SILK_LAYERS` | `["F.SilkS", "B.SilkS"]` | list of `F.*` / `B.*` layer names | Layers whose graphics are drawn as silkscreen, on the side their first letter names (any other name stops the run with a `KeyError` when the board has graphics on that layer); graphics on other non-physical layers are counted as skipped. Text is drawn only on `F.SilkS` / `B.SilkS`; text on other non-physical layers is ignored without a count |

## 16.6 Finish (`parameters/finish.py`)

Details in [Finish](Finish.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `FINISH_ENABLED` | `True` | bool | Build the surface finish and write it to every file, on every bare copper face: tops and walls in the mask openings, plated holes, the plated edge and castellations, copper cut by the edge |
| `FINISH_TYPE` | `"ENIG"` | `"file"` or a key of `FINISH_TYPES` | The finish type, or `"file"` to take it from the stack-up's `(copper_finish ...)` (KiCad's `None` builds no finish; no finish in the file, or a name that matches no key and no alias, stops the run with an error) |
| `FINISH_GROUPING` | `"metal"` | `"metal"` / `"net"` | One part per side and metal, or per side, metal and net |
| `FINISH_BEFORE_SOLDER_MASK` | `False` | bool | The finish goes on before the mask: on all the outer copper, with the mask and silkscreen on top of it; `False` puts it only in the mask openings |
| `FINISH_MITRE_LIMIT` | `2.0` | ≥ 1 | How the finish follows the copper's sharp corners: the outer side of each finish layer (and of the copper the mask wraps, with `FINISH_BEFORE_SOLDER_MASK`) keeps a corner's point out to this many times the finish's thickness from the copper's corner, and is cut straight across there. At `2.0` a corner of 60° or more keeps its point (a square pad's corners stay square) and a sharper tip is cut; `1.0` cuts every corner at the finish's thickness; below 1 the finish would be thinner at a corner than its thickness, so the run stops |
| `FINISH_TYPES` | ENIG, ENEPIG, HASL, HASL_LF, OSP, ImmersionSilver, ImmersionTin, HardGold | `{key: [(metal, mm), ...]}` bottom to top | Layers of each finish |
| `FINISH_NAME_ALIASES` | 6 KiCad names (`HAL SnPb` → `HASL`, `HAL lead-free` → `HASL_LF`, `Hard gold`, `Immersion tin`, `Immersion silver`, `HT_OSP` → `OSP`) | `{KiCad name: key of FINISH_TYPES}` | KiCad finish names that differ from a key; matching ignores case, spaces, `-` and `_` |
| `FINISH_CONDUCTIVITY_S_PER_M` | Nickel `1.4e7`, Gold `4.1e7`, Palladium `9.5e6`, Tin `9.1e6`, Silver `6.3e7`, OSP `0.0` | `{metal: S/m}` | Written to `materials.json` |

## 16.7 Geometry (`parameters/geometry.py`)

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
| `ELLIPSE_MIN_SEGMENTS` | `8` | int ≥ 3 | An ellipse or elliptical arc has at least this many straight pieces (else one per `ARC_STEP_DEG`) |
| `PINCH_POINT_OPENING_MM` | `1e-4` | mm > 0 | Polygons whose rings touch at a single point are opened by this much so they can be meshed |
| `PINCH_CUT_ROUNDS` | `10` | int ≥ 1 | Tries at opening one, the cut's radius doubling each time |
| `PINCH_DISC_TURN_DEG` | `17.0` | degrees | Turn of the octagon cut at a pinch, off the axes a board's edges follow |
| `PINCH_DISC_SIDES` | `8` | int ≥ 3 | Sides of that disc (an octagon) |
| `HEIGHT_DIGITS` | `9` | int ≥ 0 | Heights are told apart to 10^-9 mm (a picometre): two closer are one height, in stage 6's slices and the Verifier's checks |
| `VERTEX_SHARING_ROUNDS` | `20` | int ≥ 1 | Stage 6: rounds of cutting a part's faces and giving its slices each other's vertices, until nothing changes (mostly one to three; a hole's finish in visual mode has taken twelve). Slices still changing then are cut open where a round still moves them, as at a pinch point, for at most `PINCH_CUT_ROUNDS` more rounds; a part still changing after that is noted in `report.txt` and may be open ([Working Principle](Working-Principle.md#62-how-a-part-becomes-a-closed-solid)) |
| `NODING_ROUNDS` | `8` | int ≥ 1 | Rounds of noding a region on the snapping grid again (GEOS's hot pixels) until it changes nothing (one or two in practice) |
| `SLIVER_AREA_MM2` | `1e-10` | mm² > 0 | A polygon of less area is a sliver left by the set operations, and is dropped |
| `TRIANGULATE_CELL_POINTS` | `5000` | > 0 | A polygon with more points than this has its top and bottom cut into triangles strip by strip, much faster when it has many holes (earcut's time grows with the points times the holes). The points the strips add are taken out again, so the solid keeps exactly the polygon's own vertices |
| `TRIANGULATE_CELL_MM` | `10.0` | mm > 0 | Width of those strips, as KiCad cuts big polygons into 1 cm cells before it triangulates them |
| `SKIN_BURIED_TEST_OFFSET_MM` | `0.0005` | mm > 0 | Visual mode: a face is dropped if a point this far outside it lies inside another solid ([Output Modes](Output-Modes.md), equation (8.1)) |
| `MESH_MERGE_DIGITS` | `8` | int | 10^-8: a triangle's corner angle under 10^-8 rad counts as none (it gives no weight to smooth shading), and normals whose values spread less than that are not kept. No vertices are merged |
| `FLAT_FACET_THRESHOLD` | `5000` | > 0 | Smooth shading: two faces are one flat facet where (edge radius / edge span)² exceeds this |
| `SMOOTH_FACET_AREA_DIVISOR` | `10` | > 0 | Smooth shading: a flat facet of more than the part's area divided by this keeps flat normals (trimesh's `facet_minarea`) |
| `REACH_MARGIN_STEPS` | `8` | int ≥ 0 | Grid steps added to how far the conformal coating or the silkscreen ink can reach, where the copper near it is picked out first; a bigger margin picks out more and changes nothing else |
| `AIR_NEAR_MARGIN_STEPS` | `4` | int ≥ 0 | The holes' finish: grid steps past a band's part within which the solid beside it is taken, and further apart than their shells' reach by which bores are not grouped |
| `AIR_TILE_VERTICES`, `AIR_TILE_DEPTH` | `2000`, `16` | int ≥ 1, int ≥ 0 | The holes' finish: a bigger part of the solid beside the bores is cut first into tiles of about this many vertices, by at most this many halvings of its box (64k tiles a side), so that each bore clips only the tiles near it |
| `FINISH_BORES_AT_A_TIME` | `200` | int ≥ 1 | The holes' finish: a span's bores are worked on in groups of about this many, each group in a thread |
| `SKIN_FEW_PIECES`, `SKIN_BIG_PIECE_COORDINATES` | `200`, `10000` | int ≥ 0 | Visual skin: up to this many pieces of material reaching a face are cut away from it piece by piece, more at once, and a piece of this many coordinates (a dielectric, with every via hole in it) on its own |

The last four rows say how the work is cut up: other values make the same model, but where an edge
crossing rounds onto the grid another way, a sliver thinner than a grid step.

### 16.7.1 How The Curve Settings Are Used

A circle of radius $`r`$ (a via, a round pad) is flattened to $`4q`$ straight
segments, with $`q`$ segments per quarter circle chosen so that no chord strays more than
$`\varepsilon_c`$ from the true circle:

```math
n_c = \frac{\pi}{\arccos\left( 1 - \min\left( \frac{\varepsilon_c}{r},\ 1 \right) \right)} \qquad (16.1)
```

```math
q = \min\left( q_{\max},\ \max\left( q_{\min},\ \left\lceil \frac{n_c}{4} \right\rceil \right) \right) \qquad (16.2)
```

An arc (an arc track, an arc on a drawing layer) of sweep $`\varphi`$ is cut into

```math
n_a = \max\left( 2,\ \left\lceil \frac{|\varphi|}{\Delta\varphi} \right\rceil \right) \qquad (16.3)
```

segments, and the round ends of a track of width $`w`$ use

```math
q_{\mathrm{end}} = \max\left( q_{\mathrm{track}},\ \left\lfloor \frac{q(w/2)}{2} \right\rfloor \right) \qquad (16.4)
```

segments per quarter circle.

| Symbol | Meaning | Parameter |
|---|---|---|
| $`\varepsilon_c`$ | chord tolerance (2 µm) | `CIRCLE_CHORD_TOLERANCE_MM` |
| $`n_c`$ | segments a full circle needs for that tolerance | |
| $`q`$, $`q_{\min}`$, $`q_{\max}`$ | segments per quarter circle and its bounds (8, 128) | `CIRCLE_MIN_QUAD_SEGS`, `CIRCLE_MAX_QUAD_SEGS` |
| $`\varphi`$, $`\Delta\varphi`$ | arc sweep and maximum step (3°) | `ARC_STEP_DEG` |
| $`q_{\mathrm{track}}`$ | minimum roundness of track ends (4) | `TRACK_END_MIN_QUAD_SEGS` |
| $`q(w/2)`$ | equation (16.2) for radius $`w/2`$ | |

Example: a 0.3 mm via ($`r = 0.15`$ mm) gives $`n_c = 19.2`$, so $`q = \max(8, \lceil 4.8 \rceil) = 8`$, 32
segments around the via; the floor $`q_{\min}`$ decides for every circle below about 0.4 mm radius.

## 16.8 Color (`parameters/color.py`)

The look of every part: the GLB and OBJ materials, the part colours in STEP and the `look` field of
`materials.json`. Details in [Colorizing](Colorizing.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `MATERIALS` | 18 entries (Board, Board_core, Board_prepreg, Copper, Copper_exposed, Plating, the masks, mask over copper, silkscreens, Nickel, Gold, Tin, Silver, Palladium, OSP) | `{key: {color hex, alpha 0-1, metallic 0-1, roughness 0-1}}` | Material of each part kind; alpha < 1 writes a glTF BLEND material |
| `VISUAL_MASK_OPAQUE` | `True` | bool | In visual mode the mask is opaque whatever its alpha |
| `USE_STACKUP_COLORS` | `True` | bool | Honour the mask and silkscreen colours in the board's stack-up, named or user-defined (`#RRGGBBAA`, its opacity not used) |
| `STACKUP_MASK_COLORS` | 11 names | `{name: hex}` | Mask colour names |
| `STACKUP_SILK_COLORS` | white, black, yellow, green, red, blue, purple | `{name: hex}` | Silkscreen colour names |
| `STACKUP_MASK_OVER_COPPER_COLORS` | 11 names | `{name: hex or None}` | Visual-mode colour of the mask over copper per stack-up colour; an entry set to `None` (or left out) keeps the `MATERIALS` colour |
| `USER_MASK_OVER_COPPER_LIGHTEN` | `0.15` | 0-1 | With a user-defined (`#RRGGBBAA`) mask colour in the stack-up, how far the visual-mode mask over copper is mixed toward white |

## 16.9 Parallel (`parameters/parallel.py`)

How many processor cores work at once, and how much the work holds in memory at once
([Working Principle](Working-Principle.md#64-work-done-in-parallel)). None of these changes the
model: the files are the same, byte for byte, however the work is shared out.

| Name | Default | Range | Meaning |
|---|---|---|---|
| `WORKERS` | `0` | int ≥ 0 | Threads or processes that work at once. Threads where the 2D geometry library does the work (it runs outside Python's lock): the copper layers and the solder mask's minimum web width, group by group, in stage 3; both sides of the solder mask and the silkscreen, and the finish's copper layers and groups of bores, in stage 4; the faces of the visual-mode skin and the test for its hidden triangles, in stage 6; the Verifier's overlap check in stage 8. Processes of their own, each started afresh, where much of the work is Python's: in stage 3 the copper layers of a board of `PROCESS_MIN_NETS` nets or more (1,000), in stage 6 the parts built at once in simulation mode and the parts sliced for the visual skin, in stage 7 the parts of a STEP file (`PROCESS_WORKERS` and `PROCESS_MIN_COORDINATES` below). `0` = one per processor thread the run may use (all of the machine's, unless a job scheduler, `taskset` or a container limits it); `1` = everything in turn, in one process. |
| `PROCESS_WORKERS` | `0` | int ≥ 0 | At most this many worker processes at once, in stages 3, 6 and 7; `0` = as many as `WORKERS` (a higher value is the same as `WORKERS`). Each process holds its own Python, numpy and shapely (about 36 MB) and the part it builds: NE_Delta, one of the biggest boards tried, peaks at 2.80 GB in all with 4 workers and 4.37 GB with 32 in simulation mode, and at 3.65 GB with 4 when it writes the STEP file too, whose parts the processes also work on. A thread costs little memory, so a machine with many threads and little memory can keep `WORKERS` and lower this; `1` starts no process: stages 6 and 7 build their parts in the main process, stage 3 joins the copper layers in threads, and the threads are kept. If one is stopped or runs out of memory, the parts left go to half as many processes, and to the main process once that would be one; if the processes cannot start, the main process builds them; each time with a note ([Checks, Errors And Warnings](Checks-Errors-And-Warnings.md#1713-notes-worth-knowing)). Windows holds at most 61 processes at once. |
| `PROCESS_MIN_COORDINATES` | `20000` | int ≥ 0 | Stage 6 starts worker processes only when the parts hold this many coordinates or more in all their prisms, the STEP writer only when their faces do, and stage 3 only when the copper items do, on a board of `PROCESS_MIN_NETS` nets or more ([Working Principle](Working-Principle.md#64-work-done-in-parallel)); smaller boards are built part after part in the main process, which is faster than starting the processes (about 0.3 s for 4): one of the test boards takes 0.10 s that way, and 0.35 s in processes. `0` = processes for every board of more than one part (in stage 3, of `PROCESS_MIN_NETS` nets or more). |
| `GIVE_BACK_MEMORY` | `True` | bool | Hand the memory that threads freed back to the system after each step done in threads, and in each worker process after each part (glibc's `malloc_trim`, on Linux; elsewhere nothing is done). glibc keeps a pool for each thread and holds on to what is freed in it: NE_Delta in visual mode peaks at 2.65 GB with 4 workers and 3.57 GB with 32 with this, and 3.45 GB and 4.76 GB without. Tens of milliseconds per run. |
| `SKIN_PROBES_AT_A_TIME` | `2000000` | int ≥ 1 | Visual skin, the test for hidden triangles: triangles probed at once. Their probe points and normals take about a quarter of a gigabyte; fewer take less memory and a little more time |
| `VERIFY_TRIANGLES_AT_A_TIME` | `200000` | int ≥ 1 | The Verifier's vertical rays: triangles tested at once |
| `STEP_ROWS_AT_A_TIME` | `100000` | int ≥ 1 | The STEP writer: points, edges or faces turned into text at once. The file is the same, byte for byte, whatever the size |
| `PROCESS_MIN_NETS` | `1000` | int ≥ 0 | Stage 3 joins the copper layers in processes of their own only on a board of this many nets or more, counted layer by layer (and `PROCESS_MIN_COORDINATES`), else in threads: with many nets much of the work is Python's (CIAA ACC, 6,200 nets: 13.2 s in four processes, 24.3 s in four threads); with fewer most of it is GEOS's, which threads run as fast without sending the shapes to the processes and back (NE_Delta, 804 nets: 8.0 s in threads, 9.3 s in processes) |
| `VERIFY_POLYGONS_PER_THREAD` | `2000` | int ≥ 1 | The Verifier's overlap check: fewer polygons in all are tested in one thread; more in groups of at least this many |
| `VERIFY_GROUPS_PER_WORKER` | `4` | int ≥ 1 | and up to this many groups per worker, so that a slow group is made up for by the others |
| `WORKER_STOP_WAIT_S` | `10` | s ≥ 0 | When a run stops its worker processes (an error, Ctrl+C), how long it waits at most for them to be gone, so that none writes a file after |

> [!NOTE]
> `WORKERS` was `Run.WORKERS` before. `--set Run.WORKERS=N` still works: it sets
> `Parallel.WORKERS`, and `report.txt` notes that. A `parameters/run.py` that still sets `WORKERS`
> stops the run with a message that names `parameters/parallel.py`, so the value is not lost.

## 16.10 Step (`parameters/step.py`)

The STEP files: true arcs and cylinders, and what counts as an arc. The file's units are `Run.UNITS`;
how many rows the writer turns into text at once is `Parallel.STEP_ROWS_AT_A_TIME`.

| Name | Default | Range | Meaning |
|---|---|---|---|
| `STEP_EXACT_ARCS` | `True` | bool | Write circles and arcs as true curves: where a part's outline runs through vertices on one circle (holes, vias, round pads, track ends, arc tracks, round outlines), their chords become one `CIRCLE` edge and the walls on them one `CYLINDRICAL_SURFACE` face, at every height alike; every other edge stays a line and every other face a plane. Left straight where another edge at that height passes closer to the vertices than the arc bulges out from them, which the arc would cross. Written by KESE's own writer; files are about 2.5 to 3 times smaller (the RF module in `Input/`, in m: 117 MB instead of 335 MB, written in 2.2 s against 3.2 s). Meshes are unchanged |
| `STEP_ARC_FIT_TOLERANCE_MM` | `0.0002` | mm > 0 | Vertices within this of one circle form an arc (2 x the snap grid) |
| `STEP_ARC_MIN_POINTS` | `5` | int ≥ 3 | An arc runs through at least this many vertices |
| `STEP_ARC_MIN_SWEEP_DEG` | `10.0` | degrees | and turns at least this far |
| `STEP_ARC_MAX_TURN_DEG` | `30.0` | degrees | but at most this far at one vertex, so that a polygon of fewer than 12 sides (an octagonal pad, a square) stays a polygon |
| `STEP_ARC_TURN_RATIO_MAX` | `1.3` | ≥ 1 | and evenly, as a faceted circle does: no chord of the arc spans more than this many times the median chord's angle about the centre |
| `STEP_ARC_TURN_RATIO_MIN` | `0.7` | 0 to 1 | and none but the first and last less than this many times (those two may be shorter, where a boolean cut the arc) |
| `STEP_ARC_MAX_SWEEP_DEG` | `181.0` | degrees > 0 | A longer arc is cut into the fewest pieces that keep each about this long, at vertices spread evenly (a piece can run up to one chord over). A whole circle is two arcs on one `CIRCLE`; below 180 it is cut into more, each on a circle of its own |

Every format holds the same parts: the ones switched on with the `..._ENABLED` switch of their module
(`Board.BOARD_ENABLED`, `Copper.COPPER_ENABLED`, `Finish.FINISH_ENABLED`, `SolderMask.SOLDER_MASK_ENABLED`,
`Silkscreen.SILKSCREEN_ENABLED`; mask and silkscreen are off by default). A STEP file with the mask and silkscreen is 1.4 to 1.9 times as big
(the PCIe card in `Input/`, in mm: 151 MB and 1,024 solids written in 2.9 s, against 81 MB and 788 solids
in 1.9 s without them).

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

## 16.11 Verifier (`parameters/verifier.py`)

Whether the Verifier runs, and what it lets pass ([Checks, Errors And Warnings](Checks-Errors-And-Warnings.md#173-the-verifier)).
How many triangles its rays test at once is `Parallel.VERIFY_TRIANGLES_AT_A_TIME`.

| Name | Default | Range | Meaning |
|---|---|---|---|
| `VERIFY` | `False` | bool | Run the Verifier after generation, as `--verify` does (at most about 1.5 s more on the example boards, the checks stage 6 makes of each part included; longer on dense boards) |
| `VERIFY_RAYS` | `3000` | int ≥ 1 | Rays the Verifier casts through a visual model, along the board's normal, to test its surfaces |
| `VERIFY_VOLUME_TOLERANCE` | `1e-7` | ≥ 0 | How far a part's volumes from its faces, its slices and its mesh may differ, as a share of its volume (the numerical noise of areas and meshes), and still pass |
| `VERIFY_VOLUME_NOISE_MM3` | `1e-9` | mm³ ≥ 0 | and by this many mm³ more, whatever the volume |
| `VERIFY_OPENED_VOLUME_MM3` | `1e-3` | mm³ ≥ 0 | How much volume opening pinch points and sharing vertices may take from a part's prisms (or add), and the part still pass: in all, or else in every piece of every slice, with no piece gone |
| `VERIFY_MERGE_EXTRA_DIGITS` | `2` | int ≥ 0 | The closed-mesh check merges a mesh's vertices this many decimal digits finer than the snapping grid (1e-6 mm), whatever `Run.UNITS` |

## 16.12 Presets (`parameters/presets.py`)

| Name | Default | Range | Meaning |
|---|---|---|---|
| `PRESETS` | `freecad`, `elmer`, `calculix`, `openems`, `viewer`, `blender_glb`, `blender_obj` | `{name: {"Module.NAME": value}}` | Sets of overrides applied with `--for <name>`, before any `--set`; each name is checked as a `--set` is, and a new entry is a new preset ([Choosing An Export](Choosing-An-Export.md#92-the-presets)) |

> [!NOTE]
> The settings of `parameters/step.py`, `parameters/verifier.py` and `parameters/presets.py` were in
> `parameters/run.py` before, as `Run.STEP_EXACT_ARCS`, `Run.VERIFY`, `Run.PRESETS` and so on. Their
> old names still work in `--set`, with a note in `report.txt`; a `parameters/run.py` that still sets
> one of them stops the run with a message that names its new file.

| Previous | Next |
|:---|---:|
| [Solder Masks](Solder-Masks.md) | [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md) |
