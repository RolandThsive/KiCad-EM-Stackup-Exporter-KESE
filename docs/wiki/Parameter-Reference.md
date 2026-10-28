# 16. Parameter Reference

Every setting lives in one of eight files in `parameters/`. These are the only files you edit.
Units are mm unless a name says otherwise. The **Range** column is what the program uses
sensibly; "None" means the program works the value out itself. Any value can be overridden for
one run with `--set Module.NAME=value`, where `Module` is the short name in the heading of each
section. The `parameters.txt` written next to each output records every value as it stood for
the run: `--for`, `--set`, `--mode`, `--format` and `--verify` are all applied as overrides first,
and listed on its first line.

> [!NOTE]
> Defaults are those of the parameter files on `main`. Only a few values are checked by name:
> `MODE`, `FILE_FORMAT` and `DIELECTRIC_SPLIT` (an error or a warning), and `FINISH_TYPE`,
> `FINISH_DEFAULT_TYPE` and `FONT_FILE` (a note in `report.txt`). For the rest, a value outside
> the range below produces a wrong model or a plain Python error, not a named check.

## 16.1 Run (`parameters/run.py`)

What to make, where, and in which formats.

### 16.1.1 Mode, Folders And Formats

| Name | Default | Range | Meaning |
|---|---|---|---|
| `MODE` | `"simulation"` | `"simulation"` / `"visual"` | Closed solids for solvers, or the visible surface for viewers ([Output Modes](Output-Modes.md)) |
| `INPUT_DIR`, `OUTPUT_DIR` | `"Input"`, `"Output"` | paths relative to the current working directory (run from the `Generator/` folder) | Where boards are looked for and outputs written |
| `FILE_FORMAT` | `["glb"]` | any of `"glb"`, `"stl"`, `"obj"`, `"step"` | Files to write; visual mode allows only glb and obj |
| `UNITS` | `"m"` | `"mm"` / `"m"` | Units of the written files. Use `"mm"` for STEP, as CAD tools and solvers expect: the STEP file declares the units it is written in, but with `BUILD_WITH_KERNELS = True` it always declares millimetres, so metre values come in 1000 times too small |
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
| `BUILD_WITH_KERNELS` | `False` | bool | How stage 6 builds the model. `False`: every part's faces are found in 2D from its prisms and go as they are into the meshes and the STEP file ([Working Principle](Working-Principle.md#62-how-a-part-becomes-a-closed-solid)). `True`: the older way, every prism extruded and joined by Manifold, and the STEP file built and fused by OpenCascade (needs `cadquery`; much slower on dense boards) |
| `WORKERS` | `0` | int ≥ 0 | Threads stage 6 works with when `BUILD_WITH_KERNELS` is `False`: parts built at once in simulation mode, slices in visual mode. `0` = one per processor core |
| `SHOW_PROGRESS` | `True` | bool | Live `running <stage> ... 1m 23s` line on a terminal |
| `VERIFY` | `False` | bool | Run the Verifier after generation (about 3 to 8 s on the example boards; longer on dense boards) |
| `WRITE_MATERIALS_JSON` | `True` | bool | Write `materials.json` next to the outputs |

### 16.1.4 Mesh Export (GLB, STL, OBJ)

| Name | Default | Range | Meaning |
|---|---|---|---|
| `EXPORT_INCLUDE_NORMALS` | `True` | bool | Write vertex normals in the GLB (OBJ always has them) |
| `EXPORT_SET_BUFFERVIEW_TARGETS` | `True` | bool | Set glTF bufferView targets, which keeps the Khronos validator report free of hints |
| `SMOOTH_SHADE_ANGLE_DEG` | `25.0` | degrees | Edges sharper than this stay crisp; flatter ones (cylinders) shade smooth |

### 16.1.5 STEP Export

| Name | Default | Range | Meaning |
|---|---|---|---|
| `STEP_EXACT_ARCS` | `True` | bool | Only with `BUILD_WITH_KERNELS = True`: runs of vertices on one circle (vias, round pads, round outlines, track ends, arc tracks) are written as true arcs, except where an arc would cross another outline (16.7.1); smaller files, real cylinders in CAD. The default writer keeps every curve faceted, as in the meshes |
| `STEP_ARC_FIT_TOLERANCE_MM` | `0.0002` | mm > 0 | Vertices within this of one circle form an arc (2 × the snap grid) |
| `STEP_ARC_MIN_POINTS` | `5` | int ≥ 3 | Minimum vertices in a run |
| `STEP_WRITE_ROLES` | `["board", "copper", "plating", "finish"]` | subset of the roles below | Roles written to the STEP file; mask and silk are left out by default since on a dense board they are thousands of solids, which make the file more than twice as big (the Coil board in `Input/`, in mm: 147 MB written in 4.3 s instead of 63 MB in 1.8 s) |
| `STEP_FUSE_ROLES` | `["board", "copper", "plating", "finish"]` | subset of `STEP_WRITE_ROLES` | Only with `BUILD_WITH_KERNELS = True`: roles whose parts are fused into **one** solid each (what solvers need; slow on parts with many pieces); the others are compounds of touching solids (fast; fine for viewing). The default writer writes every part as the closed solids of stage 6, one per separate body |

The roles are `board`, `copper`, `plating`, `finish`, `mask`, `mask_over_copper`, `silk`. A part's role
in STEP is that of its first prism, so in simulation mode the mask on copper belongs to the `mask`
part and `mask_over_copper` selects nothing (STEP is not written in visual mode).

### 16.1.6 KiCad Versions And Presets

| Name | Default | Range | Meaning |
|---|---|---|---|
| `KICAD_VERSION_MIN`, `KICAD_VERSION_MAX` | `20211014`, `20260206` | KiCad file format numbers | Accepted range (KiCad 6 to 10; the repository has boards in each of these formats, [Compatibility](Compatibility.md#201-kicad-files)); outside it the run gives a warning |
| `PRESETS` | `hfss`, `cst`, `openems`, `viewer` | `{name: {"Module.NAME": value}}` | Sets of overrides applied with `--for <name>` ([Choosing An Export](Choosing-An-Export.md)) |

## 16.2 Board (`parameters/board.py`)

The laminate: thickness, dielectrics, outline and holes. Details in [Board](Board.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `BOARD_THICKNESS_MM` | `None` | None or mm > 0 | Laminate thickness; `None` takes it from the file (a usable stack-up, else `(general (thickness))`, else 1.6 mm) |
| `DIELECTRIC_SPLIT` | `"even"` | `"even"` | How the laminate is divided between copper layers when the file has no usable stack-up |
| `DEFAULT_DIELECTRIC_MATERIAL`, `DEFAULT_DIELECTRIC_TYPE` | `"FR4"`, `"core"` | text; `"core"` / `"prepreg"` | Used when the stack-up gives none |
| `DEFAULT_EPSILON_R`, `DEFAULT_LOSS_TANGENT` | `4.5`, `0.02` | > 0 | Typical FR4 at 1 GHz, used when the stack-up gives none |
| `USE_STACKUP_EPSILON_R`, `USE_STACKUP_LOSS_TANGENT` | `True`, `True` | bool | Stack-up values win over the defaults when present |
| `RESIN_FILL_BETWEEN_INNER_COPPER` | `True` | bool | `True`: fill the space beside inner copper from the adjacent prepreg (otherwise from the dielectric above); `False`: those pockets stay empty and `report.txt` notes it (see [Board](Board.md#102-resin-fill-beside-inner-copper)) |
| `INCLUDE_NON_PLATED_HOLES` | `True` | bool | NPTH pads become holes through the board |
| `OUTLINE_LINE_SNAP_MM` | `0.01` | mm > 0 | Open `Edge.Cuts` line and arc ends closer than this are joined, as KiCad joins them (its chaining distance is 0.01 mm) |
| `OUTLINE_FALLBACK` | `"copper_hull"` | `"copper_hull"` / `"error"` | When `Edge.Cuts` gives no closed ring at all: convex hull of the copper plus a margin, or stop |
| `OUTLINE_FALLBACK_MARGIN_MM` | `1.0` | mm ≥ 0 | Margin of the fallback hull |

## 16.3 Copper (`parameters/copper.py`)

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

## 16.4 Solder Mask (`parameters/solder_mask.py`)

Short name `SolderMask`. Details in [Solder Masks](Solder-Masks.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `MASK_OVER_LAMINATE_MM` | `0.010` | mm > 0 | Mask thickness over bare laminate (typical 0.020 to 0.030) |
| `MASK_OVER_COPPER_MM` | `0.010` | mm > 0 | Mask thickness on top of copper (typical 0.010 to 0.015) |
| `USE_STACKUP_MASK_THICKNESS` | `True` | bool | The first mask thickness found in the stack-up (normally `F.Mask`'s) is used for both values on both faces |
| `MASK_EDGE_PULLBACK_MM` | `0.005` | mm ≥ 0 | Mask and silk stop this far short of the board edge |
| `PAD_TO_MASK_CLEARANCE_MM` | `None` | None or mm ≥ 0 | Clearance around pads and untented vias; `None` takes the board setup's value from the file. A number replaces only the board setup's value: a pad's or footprint's own `solder_mask_margin` in the file still wins |
| `MASK_WALL_QUAD_SEGS` | `4` | int ≥ 1 | Segments per quarter circle on the walls where the mask climbs a trace |

## 16.5 Silkscreen (`parameters/silkscreen.py`)

Details in [Silkscreens](Silkscreens.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `SILK_THICKNESS_MM` | `0.010` | mm > 0 | Ink thickness (typical 0.010 to 0.020) |
| `SILKSCREEN_OVER_COPPER` | `False` | bool | Keep ink where the mask is open; `False` clips it off the pads as fabricators do. With `True` the ink lies on the copper and the finish is left out under it |
| `FONT_FILE` | `None` | None or a file in `kese/assets/fonts/` | Custom stroke-font JSON or Hershey `.jhf`; `None` = KiCad newstroke |
| `DRAW_TRUETYPE_TEXT_WITH_STROKE_FONT` | `True` | bool | Text in a TrueType face is drawn with the stroke font |
| `INTERLINE_PITCH` | `1.68` | > 0 | Line pitch as a multiple of the text height (KiCad's value) |
| `INTERLINE_LEGACY_FACTOR` | `0.9583` | > 0 | KiCad's correction for stroke fonts |
| `INTER_CHAR_SPACING` | `0.2` | ≥ 0 | Spacing each glyph width includes, as a fraction of the text width; dropped from the line width ([Silkscreens](Silkscreens.md), equation (14.2)) |
| `ITALIC_TILT` | `0.125` | ≥ 0 | x shift per unit of y for italic text |
| `BOLD_THICKNESS_RATIO`, `NORMAL_THICKNESS_RATIO` | `0.2`, `0.15` | > 0 | Stroke thickness as a fraction of the text height when the file gives none |
| `TEXT_STROKE_QUAD_SEGS` | `4` | int ≥ 1 | Roundness of stroke ends |
| `DRAW_HIDDEN_TEXT` | `False` | bool | Draw text marked `(hide yes)` |
| `SILK_LAYERS` | `["F.SilkS", "B.SilkS"]` | list of `F.*` / `B.*` layer names | Layers whose graphics are drawn as silkscreen, on the side their first letter names (any other name stops the run with a `KeyError` when the board has graphics on that layer); graphics on other non-physical layers are counted as skipped. Text is drawn only on `F.SilkS` / `B.SilkS`; text on other non-physical layers is ignored without a count |

## 16.6 Finish (`parameters/finish.py`)

Details in [Top And Bottom Copper Finishings](Copper-Finishings.md).

| Name | Default | Range | Meaning |
|---|---|---|---|
| `FINISH_ENABLED` | `False` | bool | Build the surface finish on bare copper |
| `FINISH_TYPE` | `"file"` | `"file"` or a key of `FINISH_TYPES` | Take the type from the stack-up's `(copper_finish ...)` (KiCad's `None` builds no finish), or name it |
| `FINISH_DEFAULT_TYPE` | `"ENIG"` | a key of `FINISH_TYPES` | Type when the file gives none, or gives a name that matches no key of `FINISH_TYPES` and no alias |
| `FINISH_GROUPING` | `"metal"` | `"metal"` / `"net"` | One part per side and metal, or per side, metal and net |
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
| `PINCH_POINT_OPENING_MM` | `1e-4` | mm > 0 | Polygons whose rings touch at a single point are opened by this much so they can be meshed |
| `TRIANGULATE_CELL_POINTS` | `5000` | > 0 | A polygon with more points than this has its top and bottom cut into triangles strip by strip, much faster when it has many holes (earcut's time grows with the points times the holes). The points the strips add are taken out again, so the solid keeps exactly the polygon's own vertices |
| `TRIANGULATE_CELL_MM` | `10.0` | mm > 0 | Width of those strips, as KiCad cuts big polygons into 1 cm cells before it triangulates them |
| `SKIN_BURIED_TEST_OFFSET_MM` | `0.0005` | mm > 0 | Visual mode: a face is dropped if a point this far outside it lies inside another solid ([Output Modes](Output-Modes.md), equation (8.1)) |
| `SKIN_TILE_POINTS` | `250_000` | > 0 | Visual mode: a big board's skin is joined in tiles of about this many outline points; smaller tiles need less memory ([Output Modes](Output-Modes.md)) |

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

In STEP files written with `Run.BUILD_WITH_KERNELS = True` and `Run.STEP_EXACT_ARCS`, a run of at
least `STEP_ARC_MIN_POINTS` consecutive ring vertices is written as one true arc when a
least-squares (Kåsa) circle through them fits every vertex within `STEP_ARC_FIT_TOLERANCE_MM`,
the turn between vertices keeps one sense and is nearly the same everywhere, and the run sweeps
at least 10°:

```math
\max_{\mathbf{p} \in \text{run}} \left| d(\mathbf{p}, \mathbf{c}) - r \right| \le \tau_{\mathrm{arc}} \qquad (16.5)
```

where $`d(\mathbf{p}, \mathbf{c})`$ is the distance from vertex $`\mathbf{p}`$ to the fitted
centre $`\mathbf{c}`$, $`r`$ is the fitted radius and $`\tau_{\mathrm{arc}}`$ is
`STEP_ARC_FIT_TOLERANCE_MM` (0.2 µm).

Such an arc is written only where it cannot cross anything. The curve bulges out from every chord
it replaces by the chord's sagitta

```math
s = r \left( 1 - \cos \frac{\Delta\theta}{2} \right) \qquad (16.6)
```

where $`\Delta\theta`$ is the angle the chord spans at the centre: $`s`$ is at most
$`\varepsilon_c`$ (2 µm) on the circles KESE facets, up to about five times that on track ends and
oval drills, which get half as many segments (16.4), and up to 5 µm on outlines the board file
holds already faceted, such as zone fills. Where another edge passes closer to the chords than
that, as along a sliver between two pads, the curve would cross it and the face would be invalid.
So each arc gets a strip that holds its chords and its curve with $`g`$ to spare on both sides of
the curve, where $`g`$ is one step of the snap grid (`SNAP_GRID_MM`, 0.1 µm): from its vertices,
each one that is less than $`g`$ inside the curve (or outside it) moved to $`g`$ inside it, out to
$`g`$ beyond the curve (or its furthest vertex, if that is further out), closed at its two end
vertices; for a whole circle, the ring from $`g`$ inside the circle (or its nearest chord, if that
is further in) out to $`g`$ beyond it (or its furthest vertex). The arc is written only when no
edge of the band's polygons enters its strip, except the two edges at its ends, and when no other
arc's strip overlaps it; otherwise its vertices stay straight edges. The edges at its ends may run
along the curve, where the outline doubles back (as at the corners of a notch as wide as its pad)
or goes on along the tangent, but must not cut into its circle by more than 0.05 nm (`TANGENT_MM`
in `kese/s7_write/step_arcs.py`): OpenCascade takes two curves within about $`2 \times 10^{-7}`$ of
the file's unit for touching, 0.2 nm in mm, the stricter unit, so a line a hair off the tangent
only touches the arc, however far along it meets the circle again. An edge that joins both ends of
an arc, as the straight side of a half round does, cannot cross it. On PC110 this keeps
3 of 144,933 arcs straight: two had made invalid solids of a net's copper and of the dielectric
around it, and the third an invalid band of the copper with no net, which the fuse then dropped,
and with it the whole solid around that oval hole (0.99 mm³ of copper), leaving only valid solids
in the file.

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

| Previous | Next |
|:---|---:|
| [Solder Masks](Solder-Masks.md) | [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md) |
