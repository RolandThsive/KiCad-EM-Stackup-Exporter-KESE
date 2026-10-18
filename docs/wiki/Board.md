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
`Board_dielectric 1`, `Board_dielectric 2`, ... counted from the `F.Cu` side; with `"merged"`
every dielectric prism goes into one part named `Board`.

Each dielectric prism is the outline minus every hole that passes through that gap (a via from
layer *i* to layer *j* drills dielectrics *i* to *j* − 1, a through via and a through-hole pad
drill them all). The dielectric's z range runs from the bottom of the copper layer above it to the
top of the copper layer below it.

In `materials.json` every dielectric part carries `kind` (core / prepreg), `material`,
`thickness_mm`, `epsilon_r`, `loss_tangent` and `between` (the two copper layers it separates).

## 10.2 Resin Fill Beside Inner Copper

In a pressed laminate the resin of the prepreg flows into the spaces between the inner-layer
traces, so there is no air inside the board. KESE models this with
`Board.RESIN_FILL_BETWEEN_INNER_COPPER = True` (the default): for every inner copper layer, the
area of the outline that carries **no** copper on that layer, minus the holes, is filled over
the copper's own z band and added to a dielectric part:

- the prepreg **below** the copper layer when the layer above is a core and the one below a
  prepreg;
- otherwise the dielectric **above** it.

So a core-prepreg-core stack-up gets its inner pockets filled from the prepreg, as in the
factory. These prisms carry `resin_fill_beside: <layer>` in their properties. With the setting
`False`, the pockets stay empty and `report.txt` notes it. With `Run.DIELECTRIC_GROUPING =
"merged"` the fill goes into the single `Board` part.

> [!NOTE]
> Where inner copper exists, dielectric *k* and dielectric *k* + 1 are separated by the copper
> band; the resin fill is what joins the laminate through the copper-free area of that band.
> Without it the laminate would be two separate solids touching only through copper.

## 10.3 Outline And Cut-Outs

The outline comes from `Edge.Cuts`:

1. Closed shapes (circles, rectangles, polygons) are taken as rings.
2. Open lines, arcs and Béziers are snapped at their end points to `Board.OUTLINE_LINE_SNAP_MM`
   (10 nm by default) and polygonized into faces. If they do not close, the run warns
   `Edge.Cuts lines/arcs do not form a closed outline`.
3. Rings nested at an **even** depth are board, rings at an **odd** depth are cut-outs. A circle
   drawn inside the outer outline is a hole through the whole board; a ring inside that would be
   board again.

Without any `Edge.Cuts` at all, `Board.OUTLINE_FALLBACK` decides: `"copper_hull"` (the default)
uses the convex hull of all copper grown by `Board.OUTLINE_FALLBACK_MARGIN_MM` (1 mm) and warns;
`"error"` stops the run.

Everything on every layer is clipped to the outline: copper, mask openings and silkscreen never
reach past the board edge.

## 10.4 Holes

| Source | Hole | Setting |
|---|---|---|
| Via | drill of the via's `(drill ...)`, spanning the via's layers | plated, wall `Copper.VIA_WALL_MM` |
| Through-hole pad (`thru_hole`) | the pad's drill, round or oval (slot), with its offset | plated, wall `Copper.PTH_WALL_MM` |
| Non-plated pad (`np_thru_hole`) | the pad's drill | not plated; included when `Board.INCLUDE_NON_PLATED_HOLES` (default `True`) |

A plated hole leaves its barrel in the laminate: the dielectric is cut by the full drill and the
copper barrel fills the ring between the drill and the drill minus the wall. See
[Copper And Traces](Copper-And-Traces.md) for the plating.

## 10.5 Board Thickness

`Board.BOARD_THICKNESS_MM = None` (the default) takes the laminate from the stack-up, or from the
file's `(general (thickness ...))` when there is no stack-up. A number forces the laminate
thickness; see [Stack-Up Model](Stack-Up-Model.md) for how the dielectrics are scaled.

## 10.6 Settings

| Name | Default | Range | Meaning |
|---|---|---|---|
| `BOARD_THICKNESS_MM` | `None` | None or mm > 0 | Laminate thickness; `None` takes it from the file |
| `DIELECTRIC_SPLIT` | `"even"` | `"even"` | How the laminate is divided when the file has no stack-up |
| `DEFAULT_DIELECTRIC_MATERIAL`, `DEFAULT_DIELECTRIC_TYPE` | `"FR4"`, `"core"` | text; `"core"` / `"prepreg"` | Material and type when the stack-up gives none |
| `DEFAULT_EPSILON_R`, `DEFAULT_LOSS_TANGENT` | `4.5`, `0.02` | > 0 | Typical FR4 at 1 GHz, used when the stack-up gives none |
| `USE_STACKUP_EPSILON_R`, `USE_STACKUP_LOSS_TANGENT` | `True`, `True` | bool | Stack-up values win over the defaults when present |
| `RESIN_FILL_BETWEEN_INNER_COPPER` | `True` | bool | Fill the space beside inner copper with the neighbouring prepreg |
| `INCLUDE_NON_PLATED_HOLES` | `True` | bool | NPTH pads become holes through the board |
| `OUTLINE_LINE_SNAP_MM` | `1e-5` | mm > 0 | `Edge.Cuts` end points closer than this are joined |
| `OUTLINE_FALLBACK` | `"copper_hull"` | `"copper_hull"` / `"error"` | What to do without `Edge.Cuts` |
| `OUTLINE_FALLBACK_MARGIN_MM` | `1.0` | mm ≥ 0 | Margin around the copper hull in the fallback |

| Previous | Next |
|:---|---:|
| [Choosing An Export](Choosing-An-Export.md) | [Copper And Traces](Copper-And-Traces.md) |
