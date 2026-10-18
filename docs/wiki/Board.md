# 10. Board

The board is the laminate: the dielectric layers between and around the copper, with the
outline, the cut-outs and the holes. `Generator/Geometry/Board.py` builds it from the resolved
outline and stack-up; the settings are in `Parameters/Board_Parameters.py`.

<!-- Pictures wanted for this page (made by Roland):
     Board 1: the outline of a board with a cut-out and NPTH holes, as KESE resolves it.
     Board 2: a cross-section of a 4-layer laminate: cores, prepregs, inner copper with the
              resin fill beside it (one colour per dielectric). -->

## 10.1 Dielectric Solids

Each gap between two consecutive copper layers is one dielectric from the
[Stack-Up Model](Stack-Up-Model.md): a core or a prepreg with its own thickness, material, εr
and tanδ. With `Run.DIELECTRIC_GROUPING = "layer"` (the default) each becomes its own part,
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
D_i = O \setminus \bigcup_{h : a_h \le i-1,\ b_h \ge i} H_h \qquad (10.1)
```

With edge plating on (section 11.7 of [Copper And Traces](Copper-And-Traces.md)), the edge band
is also removed from every $`D_i`$, since the plating takes the laminate's place at the edge.

| Symbol | Meaning |
|---|---|
| $`D_i`$ | 2D region of dielectric $`d_i`$ (between copper layers $`l_{i-1}`$ and $`l_i`$) |
| $`O`$ | the board outline region (section 10.3) |
| $`H_h`$ | the drill of hole $`h`$ (round or slot) |
| $`a_h, b_h`$ | index of the first and last copper layer hole $`h`$ spans ($`0`$ to $`N-1`$ for a through hole) |
| $`\setminus`$, $`\cup`$, $`\cap`$ | region difference, union and intersection |

The prism is extruded over the z range of equations (7.8) and (7.9) in
[Stack-Up Model](Stack-Up-Model.md).

In `materials.json` every dielectric part carries `kind` (core / prepreg), `material`,
`thickness_mm`, `epsilon_r`, `loss_tangent` and `between` (the two copper layers it separates).

## 10.2 Resin Fill Beside Inner Copper

In a pressed laminate the resin of the prepreg flows into the spaces between the inner-layer
traces, so there is no air inside the board. KESE models this with
`Board.RESIN_FILL_BETWEEN_INNER_COPPER = True` (the default): for every inner copper layer, the
area of the outline that carries **no** copper on that layer, minus the holes through that
layer, is filled over the copper's own z band:

```math
F_k = \left( O \setminus \bigcup_{h : a_h \le k \le b_h} H_h \right) \setminus C_k, \qquad z \in \left[ z_{\mathrm{bot}}(l_k),\ z_{\mathrm{top}}(l_k) \right] \qquad (10.2)
```

| Symbol | Meaning |
|---|---|
| $`F_k`$ | resin-fill region beside inner copper layer $`l_k`$ |
| $`C_k`$ | all copper of layer $`l_k`$, every net |
| $`z_{\mathrm{bot}}(l_k)`$, $`z_{\mathrm{top}}(l_k)`$ | the copper band of $`l_k`$, equations (7.6) and (7.7) |

With edge plating on, the edge band is also removed from $`F_k`$. The fill is added to a
dielectric part:

- the prepreg **below** the copper layer when the layer above is a core and the one below a
  prepreg;
- otherwise the dielectric **above** it.

So a core-prepreg-core stack-up gets its inner pockets filled from the prepreg, as in the
factory. Inside KESE these prisms are tagged `resin_fill_beside: <layer>`; `materials.json` takes
a part's properties from its first prism, the dielectric slab itself, so the tag does not appear
there. With the setting
`False`, the pockets stay empty and `report.txt` notes it. With `Run.DIELECTRIC_GROUPING =
"merged"` the fill goes into the single `Board` part.

> [!NOTE]
> Where inner copper exists, dielectric *k* and dielectric *k* + 1 are separated by the copper
> band; the resin fill is what joins the laminate through the copper-free area of that band.
> Without it the laminate would be two separate solids touching only through copper.

## 10.3 Outline And Cut-Outs

The outline comes from `Edge.Cuts`:

1. Closed shapes (circles, rectangles, polygons) are taken as rings.
2. Open lines, arcs and Béziers have every coordinate rounded to a grid set by
   `Board.OUTLINE_LINE_SNAP_MM` (10 nm by default; the value counts only to the nearest power of
   ten), so end points that round to the same grid point join, and are then polygonized into
   faces. If they form no face at all, the run warns
   `Edge.Cuts lines/arcs do not form a closed outline`.
3. Rings nested at an **even** depth are board, rings at an **odd** depth are cut-outs. A circle
   drawn inside the outer outline is a hole through the whole board; a ring inside that would be
   board again:

```math
O = \bigcup_{r : n_r \text{ even}} r \ \setminus \bigcup_{r : n_r \text{ odd}} r \qquad (10.3)
```

| Symbol | Meaning |
|---|---|
| $`O`$ | the board outline region |
| $`r`$ | one closed ring found on `Edge.Cuts` |
| $`n_r`$ | how many other rings contain $`r`$ |

When `Edge.Cuts` gives no closed outline (nothing drawn, or lines that do not close), the
fallback outline is

```math
O = \mathrm{hull}\left( \bigcup C \right) \oplus m \qquad (10.4)
```

where $`\mathrm{hull}`$ is the convex hull of all copper, $`\oplus m`$ grows a region
outward by $`m`$ (a buffer), and $`m`$ is `Board.OUTLINE_FALLBACK_MARGIN_MM`.

`Board.OUTLINE_FALLBACK` decides whether the fallback is used: `"copper_hull"` (the default)
uses equation (10.4) with $`m = 1`$ mm and warns; `"error"` stops the run.

Everything on every layer is clipped to the outline: copper, mask openings and silkscreen never
reach past the board edge.

## 10.4 Holes

| Source | Hole | Setting |
|---|---|---|
| Via | drill of the via's `(drill ...)`, spanning the via's layers | plated, wall `Copper.VIA_WALL_MM` |
| Through-hole pad (`thru_hole`) | the pad's drill, round or oval (slot), at the pad position; the drill's `(offset ...)` moves the copper pad, not the hole, as in KiCad | plated, wall `Copper.PTH_WALL_MM` |
| Non-plated pad (`np_thru_hole`) | the pad's drill | not plated; included when `Board.INCLUDE_NON_PLATED_HOLES` (default `True`) |

A plated hole leaves its barrel in the laminate: the dielectric is cut by the full drill and the
copper barrel fills the ring between the drill and the drill minus the wall. See
[Copper And Traces](Copper-And-Traces.md) for the plating.

## 10.5 Board Thickness

`Board.BOARD_THICKNESS_MM = None` (the default) takes the laminate from the stack-up, or from the
file's `(general (thickness ...))` when there is no usable stack-up (1.6 mm when the file gives no
thickness either). A number forces the laminate
thickness; see [Stack-Up Model](Stack-Up-Model.md) for how the dielectrics are scaled.

## 10.6 Settings

| Name | Default | Range | Meaning |
|---|---|---|---|
| `BOARD_THICKNESS_MM` | `None` | None or mm > 0 | Laminate thickness; `None` takes it from the file |
| `DIELECTRIC_SPLIT` | `"even"` | `"even"` | How the laminate is divided when the file has no stack-up |
| `DEFAULT_DIELECTRIC_MATERIAL`, `DEFAULT_DIELECTRIC_TYPE` | `"FR4"`, `"core"` | text; `"core"` / `"prepreg"` | Material and type when the stack-up gives none |
| `DEFAULT_EPSILON_R`, `DEFAULT_LOSS_TANGENT` | `4.5`, `0.02` | > 0 | Typical FR4 at 1 GHz, used when the stack-up gives none |
| `USE_STACKUP_EPSILON_R`, `USE_STACKUP_LOSS_TANGENT` | `True`, `True` | bool | Stack-up values win over the defaults when present |
| `RESIN_FILL_BETWEEN_INNER_COPPER` | `True` | bool | Fill the space beside inner copper from the adjacent prepreg, else from the dielectric above (section 10.2) |
| `INCLUDE_NON_PLATED_HOLES` | `True` | bool | NPTH pads become holes through the board |
| `OUTLINE_LINE_SNAP_MM` | `1e-5` | mm > 0 | Grid that open `Edge.Cuts` coordinates are rounded to (nearest power of ten), so their end points join |
| `OUTLINE_FALLBACK` | `"copper_hull"` | `"copper_hull"` / `"error"` | What to do when `Edge.Cuts` gives no closed outline |
| `OUTLINE_FALLBACK_MARGIN_MM` | `1.0` | mm ≥ 0 | Margin around the copper hull in the fallback |

| Previous | Next |
|:---|---:|
| [Choosing An Export](Choosing-An-Export.md) | [Copper And Traces](Copper-And-Traces.md) |
