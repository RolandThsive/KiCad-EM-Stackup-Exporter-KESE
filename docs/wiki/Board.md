# 12. Board

The board is the laminate: the dielectric layers between and around the copper, with the
outline, the cut-outs and the holes. `kese/s4_geometry/laminate.py` builds it from the resolved
outline and stack-up; the settings are in `parameters/board.py`.

## 12.1 Dielectric Solids

Each gap between two consecutive copper layers is one dielectric from the
[Stack-Up Model](Stack-Up-Model.md): a core or a prepreg with its own thickness, material, εr
and tanδ. With `Board.DIELECTRIC_GROUPING = "layer"` (the default) each becomes its own part,
named `Board_` plus the stack-up's name for that dielectric (`Board_dielectric 1`,
`Board_dielectric 2`, ... from the `F.Cu` side). A gap holds one part however many plies it has:
plies written as sub-layers of one stack-up dielectric keep that dielectric's name, and separate
stack-up dielectrics between the same two copper layers give one part named like
`Board_dielectric 2 + dielectric 3`. With `"merged"` every dielectric prism goes into
one part named `Board`.

Each dielectric prism is the outline minus every hole that passes through that gap: a via from
copper layer $`l_a`$ to $`l_b`$ drills the dielectrics between them, and a through via or a
through-hole pad drills them all.

```math
D_i = O \setminus \bigcup_{h : a_h \le i-1,\ b_h \ge i} H_h \qquad (12.1)
```

With edge plating on (section 13.7 of [Copper And Traces](Copper-And-Traces.md)), the edge band
is also removed from every $`D_i`$, since the plating takes the laminate's place at the edge.

| Symbol | Meaning |
|---|---|
| $`D_i`$ | 2D region of dielectric $`d_i`$ (between copper layers $`l_{i-1}`$ and $`l_i`$) |
| $`O`$ | the board outline region (section 12.3) |
| $`H_h`$ | the drill of hole $`h`$ (round or slot) |
| $`a_h, b_h`$ | index of the first and last copper layer hole $`h`$ spans ($`0`$ to $`N-1`$ for a through hole) |
| $`\setminus`$, $`\cup`$, $`\cap`$ | region difference, union and intersection |

The prism is extruded over the z range of equations (8.8) and (8.9) in
[Stack-Up Model](Stack-Up-Model.md).

In `materials.json`, with `"layer"` grouping, every dielectric part carries `kind` (core /
prepreg), `material`, `thickness_mm`, `epsilon_r`, `loss_tangent` and `between` (the two copper
layers it separates). With `"merged"` the single `Board` part carries only the first dielectric's
values (its kind, material, thickness, εr, tanδ and `between`).

## 12.2 Resin Fill Beside Inner Copper

In a pressed laminate the resin of the prepreg flows into the spaces between the inner-layer
traces, so there is no air inside the board. KESE models this with
`Board.RESIN_FILL_BETWEEN_INNER_COPPER = True` (the default): for every inner copper layer, the
area of the outline that carries **no** copper on that layer, minus the holes through that
layer, is filled over the copper's own z band:

```math
F_k = \left( O \setminus \bigcup_{h : a_h \le k \le b_h} H_h \right) \setminus C_k, \qquad z \in \left[ z_{\mathrm{bot}}(l_k),\ z_{\mathrm{top}}(l_k) \right] \qquad (12.2)
```

| Symbol | Meaning |
|---|---|
| $`F_k`$ | resin-fill region beside inner copper layer $`l_k`$ |
| $`C_k`$ | all copper of layer $`l_k`$, every net |
| $`z_{\mathrm{bot}}(l_k)`$, $`z_{\mathrm{top}}(l_k)`$ | the copper band of $`l_k`$, equations (8.6) and (8.7) |

With edge plating on, the edge band is also removed from $`F_k`$. The fill is added to a
dielectric part:

- the prepreg **below** the copper layer when the layer above is a core and the one below a
  prepreg;
- otherwise the dielectric **above** it.

![Board 11_zones cut at true scale across the track that splits its inner zones, each dielectric part in its own colour: the resin beside In1.Cu belongs to the prepreg above it, the resin beside In2.Cu to the prepreg below it; and the bands of In1.Cu and In2.Cu from above, copper and resin](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Board/board_2_resin_fill.webp)

So both common 4-layer builds, prepreg-core-prepreg (as in the picture) and core-prepreg-core,
get their inner pockets filled from a prepreg, as in the factory. Inside KESE these prisms are tagged `resin_fill_beside: <layer>`; `materials.json` takes
a part's properties from its first prism, the dielectric slab itself, so the tag does not appear
there. With the setting
`False`, the pockets stay empty and `report.txt` notes it. With `Board.DIELECTRIC_GROUPING =
"merged"` the fill goes into the single `Board` part.

> [!NOTE]
> Where inner copper exists, dielectric *k* and dielectric *k* + 1 are separated by the copper
> band; the resin fill is what joins the laminate through the copper-free area of that band.
> Without it the laminate would be two separate solids touching only through copper.

## 12.3 Outline And Cut-Outs

The outline comes from `Edge.Cuts`:

1. Closed shapes (circles, rectangles, polygons) are taken as rings; a rectangle keeps its rounded
   corners when it has them (KiCad 10, `(radius ...)`, at most half its shorter side, as in KiCad).
2. Open lines, arcs and Béziers are joined end to end the way KiCad chains them. An end that
   meets no other end is moved onto the nearest other such end within
   `Board.OUTLINE_LINE_SNAP_MM` (0.01 mm by default, KiCad's own chaining distance), the closest
   pairs first; ends that already meet stay where they are. The lines are then polygonized into
   faces. When a gap was closed this way, `report.txt` notes the widest one. If the lines form no
   face at all, the run warns `Edge.Cuts lines/arcs do not form a closed outline`.
3. A ring of `Board.OUTLINE_MIN_AREA_MM2` (1e-9 mm²) or less, such as a line drawn there and back,
   is left out, and two rings that differ by less than `Board.OUTLINE_DUPLICATE_AREA_MM2` (1e-6 mm²),
   a ring drawn twice, are one. Rings nested at an **even** depth are boards, rings at an **odd**
   depth are cut-outs. As in KiCad, each cut-out is taken out of the ring one level up that holds
   it. A circle drawn inside the outer outline is a hole through the whole board, and a ring drawn
   inside such a cut-out is a board again, like a small board inside a panel frame (`featureTest/13b_outline_two`):

```math
O = \bigcup_{r : n_r \text{ even}} \Big( r \ \setminus \bigcup_{h \subset r,\ n_h = n_r + 1} h \Big) \qquad (12.3)
```

| Symbol | Meaning |
|---|---|
| $`O`$ | the board outline region |
| $`r`$ | one closed ring found on `Edge.Cuts` |
| $`h`$ | a cut-out: a ring inside $`r`$, one level deeper |
| $`n_r`$ | how many other rings contain $`r`$ |

![Board 12_outline_shapes: its Edge.Cuts shapes, open ones in blue and closed ones in red, over the outline KESE resolves from them, with a numbered key; the laminate solid KESE writes for it; and board synthetic with a circular cut-out, a non-plated hole, two plated holes and a via](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Board/board_1_outline.webp)

When `Edge.Cuts` gives no closed ring at all (nothing drawn, or only lines that do not close),
the fallback outline is

```math
O = \mathrm{hull}\left( \bigcup C \right) \oplus m \qquad (12.4)
```

where $`\mathrm{hull}`$ is the convex hull of all copper, $`\oplus m`$ grows a region
outward by $`m`$ (a buffer), and $`m`$ is `Board.OUTLINE_FALLBACK_MARGIN_MM`.

`Board.OUTLINE_FALLBACK` decides whether the fallback is used: `"copper_hull"` (the default)
uses equation (12.4) with $`m = 1`$ mm and warns; `"error"` stops the run. When the lines do not
close but a closed shape (a circle, rectangle or polygon) is drawn on `Edge.Cuts`, there is no
fallback: that shape alone becomes the outline, even if it was meant as a cut-out.

Everything on every layer is clipped to the outline: copper, mask openings and silkscreen never
reach past the board edge.

## 12.4 Holes

| Source | Hole | Setting |
|---|---|---|
| Via | drill of the via's `(drill ...)`, spanning the via's layers | plated, wall `Copper.VIA_WALL_MM` |
| Through-hole pad (`thru_hole`) | the pad's drill, round or oval (slot), at the pad position; the drill's `(offset ...)` moves the copper pad, not the hole, as in KiCad | plated, wall `Copper.PTH_WALL_MM` |
| Non-plated pad (`np_thru_hole`) | the pad's drill | not plated; included when `Board.INCLUDE_NON_PLATED_HOLES` (default `True`) |
| Backdrill, tertiary drill (KiCad 10) | a wider drill into a plated hole from a face, through the layer it must cut | drills out the laminate, plating and copper there; `Board.BACKDRILLS` ([Copper And Traces](Copper-And-Traces.md#1333-backdrills)) |
| Counterbore, countersink (KiCad 10) | a step or a cone cut into a hole's end from a face | `Board.POST_MACHINING`, section 12.4.1 |

A plated hole leaves its barrel in the laminate: the dielectric is cut by the full drill and the
copper barrel fills the ring between the drill and the drill minus the wall. See
[Copper And Traces](Copper-And-Traces.md) for the plating.

### 12.4.1 Counterbores And Countersinks

![Board 25_post_machining cut through its holes at true scale: a plated pad counterbored from F.Cu and countersunk from B.Cu, with the copper each cut knocks out, and six more cuts in unplated holes: two counterbores, countersinks of 82 and 120 degrees, one with a depth and one from B.Cu](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Board/board_3_post_machining.webp)

KiCad 10 can machine the end of a pad's or via's hole from either face:
`(front_post_machining counterbore (size 2.2) (depth 0.5))` cuts a flat-bottomed step,
`(back_post_machining countersink (size 2.4) (angle 90))` a cone of that included angle with its
tip on the hole's axis. With `Board.POST_MACHINING = True` (the default) KESE cuts them as KiCad's
3D board does (`exporter_step.cpp`):

- the depth counts from the copper's outer face; a countersink with no depth, or one deeper than
  its cone, goes down to the tip;
- the laminate is cut down to the floor, even a floor inside an inner copper layer's band, and so
  is the hole's barrel where the cut is wider than the hole;
- the copper of every layer the cut reaches is knocked out, by KiCad's own rule
  (`GetPostMachiningKnockout`): layer $`l_k`$ is reached when $`d_k`$ is less than the depth, and
  loses the disc of radius $`r(d_k)`$ when that is more than 0, equation (12.5); the mask,
  silkscreen and finish leave the knocked-out copper as they leave any hole;
- the solids have upright walls, so a countersink is a stack of cylinders, each at the cone's
  radius halfway up it, short enough to stray from the cone by at most $`\tau`$, equation (12.6),
  with a step at every copper face.

```math
r(d) = \frac{s}{2} - d \tan\frac{\alpha}{2}, \qquad d_k = \begin{cases} 0 & l_k \text{ the outer layer on the machined face} \\ \text{to the middle of } l_k & l_k \text{ an inner layer} \\ \text{through the whole board} & l_k \text{ the outer layer on the far face} \end{cases} \qquad (12.5)
```

```math
h_{\mathrm{step}} \le \frac{2 \tau}{\tan(\alpha / 2)} \qquad (12.6)
```

| Symbol | Meaning | Parameter |
|---|---|---|
| $`s`$ | size (diameter) of the cut at the face | the file's `size` |
| $`\alpha`$ | a countersink's included angle; a counterbore has $`\tan(\alpha/2) = 0`$ and knocks out its whole size | the file's `angle` |
| $`d_k`$ | distance of copper layer $`l_k`$ from the machined face, from the copper's outer face | |
| $`h_{\mathrm{step}}`$ | height of one step of a countersink | |
| $`\tau`$ | how far a step may stray from the cone | `Board.COUNTERSINK_STEP_TOLERANCE_MM` |

KiCad's STEP export cuts each one 1 µm deeper and takes the whole pad off the layers it reaches;
KESE keeps the copper outside the cut, as KiCad's Gerber files have it. `report.txt` counts
`counterbores of pads`, `countersinks of vias` and so on.

## 12.5 Board Thickness

`Board.BOARD_THICKNESS_MM = None` (the default) takes the laminate from the stack-up, or from the
file's `(general (thickness ...))` less the outer copper and the two masks when there is no usable
stack-up (from `Board.DEFAULT_BOARD_THICKNESS_MM`, 1.6 mm as in KiCad, when the file gives no
thickness either), so the finished board is KiCad's board thickness. A number forces the laminate
thickness; see [Stack-Up Model](Stack-Up-Model.md) for how the dielectrics are scaled.

## 12.6 Settings

| Name | Default | Range | Meaning |
|---|---|---|---|
| `BOARD_THICKNESS_MM` | `None` | None or mm > 0 | Laminate thickness; `None` takes it from the file |
| `DEFAULT_BOARD_THICKNESS_MM` | `1.6` | mm > 0 | Finished board thickness when the file gives none (KiCad's default) |
| `DIELECTRIC_SPLIT` | `"even"` | `"even"` | How the laminate is divided when the file has no usable stack-up |
| `DEFAULT_DIELECTRIC_MATERIAL`, `DEFAULT_DIELECTRIC_TYPE` | `"FR4"`, `"core"` | text; `"core"` / `"prepreg"` | Material and type when the stack-up gives none |
| `DEFAULT_EPSILON_R`, `DEFAULT_LOSS_TANGENT` | `4.5`, `0.02` | > 0 | Typical FR4 at 1 GHz, used when the stack-up gives none |
| `USE_STACKUP_EPSILON_R`, `USE_STACKUP_LOSS_TANGENT` | `True`, `True` | bool | Stack-up values win over the defaults when present |
| `RESIN_FILL_BETWEEN_INNER_COPPER` | `True` | bool | `True`: fill the space beside inner copper from the adjacent prepreg (otherwise from the dielectric above); `False`: those pockets stay empty and `report.txt` notes it (section 12.2) |
| `INCLUDE_NON_PLATED_HOLES` | `True` | bool | NPTH pads become holes through the board |
| `BACKDRILLS` | `True` | bool | Drill out KiCad 10's backdrills and tertiary drills ([Copper And Traces](Copper-And-Traces.md#1333-backdrills)) |
| `POST_MACHINING` | `True` | bool | Cut KiCad 10's counterbores and countersinks (section 12.4.1) |
| `COUNTERSINK_STEP_TOLERANCE_MM` | `0.025` | mm > 0 | How far a countersink's steps may stray from its cone, equation (12.6) |
| `OUTLINE_LINE_SNAP_MM` | `0.01` | mm > 0 | Open `Edge.Cuts` line and arc ends closer than this are joined, as KiCad joins them (its chaining distance is 0.01 mm) |
| `OUTLINE_FALLBACK` | `"copper_hull"` | `"copper_hull"` / `"error"` | What to do when `Edge.Cuts` gives no closed ring at all |
| `OUTLINE_FALLBACK_MARGIN_MM` | `1.0` | mm ≥ 0 | Margin around the copper hull in the fallback |
| `OUTLINE_DUPLICATE_AREA_MM2` | `1e-6` | mm² > 0 | Two closed `Edge.Cuts` outlines that differ by less than this area are one (a ring drawn twice; section 12.3) |
| `OUTLINE_MIN_AREA_MM2` | `1e-9` | mm² ≥ 0 | A closed `Edge.Cuts` outline of this area or less is left out (a line drawn there and back, a circle of no size) |

| Previous | Next |
|:---|---:|
| [Project Output Organization](Project-Output-Organization.md) | [Copper And Traces](Copper-And-Traces.md) |
