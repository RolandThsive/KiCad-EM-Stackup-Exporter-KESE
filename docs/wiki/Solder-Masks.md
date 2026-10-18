# 15. Solder Masks

The solder mask is the lacquer (LPI) over both faces of the board. `Generator/Geometry/SolderMask.py`
builds it; the settings are in `Parameters/SolderMask_Parameters.py`.

<!-- Pictures wanted for this page (made by Roland):
     Mask 1: a top view of mask openings: pads with clearance, an untented via, a drawn opening.
     Mask 2: a cross-section of the conformal mask: flat on laminate, raised on a trace, the wall
             beside the trace, with MASK_OVER_LAMINATE_MM and MASK_OVER_COPPER_MM marked. -->

## 15.1 KiCad's Mask Layers Are Negative

Whatever is drawn on `F.Mask` / `B.Mask` is an **opening**, not mask. KESE builds, per side:

```text
mask = outline − openings − open hole bores, pulled back from the board edge
```

The openings are:

| Opening | Size |
|---|---|
| every pad that lists the mask layer (`F.Mask`, `B.Mask`, `*.Mask`) | the pad shape grown by its mask margin: the pad's own `solder_mask_margin`, else the footprint's, else the board's pad-to-mask clearance, or `SolderMask.PAD_TO_MASK_CLEARANCE_MM` when set |
| every untented via (see [via tenting](Copper-And-Traces.md#1132-via-tenting)) | the via pad grown by the board's clearance |
| graphics, text and zone fills drawn on the mask layer | as drawn |

Openings are clipped to the outline. `report.txt` counts `pad mask openings on F.Mask` and the
clearance used on its `vias:` line.

## 15.2 Conformal Mask

LPI mask follows the copper: it is thin on top of a trace and thicker on the bare laminate
beside it, and it climbs the side of every trace. KESE builds three regions per side from the mask
area and the outer copper:

| Region | z range (top side, from the laminate face) |
|---|---|
| **flat**: mask over bare laminate, farther than one mask thickness from any copper | 0 to `MASK_OVER_LAMINATE_MM` |
| **top**: mask on top of copper | copper thickness to copper thickness + `MASK_OVER_COPPER_MM` |
| **wall**: the band one mask thickness wide beside copper, where the mask climbs | 0 to copper thickness + `MASK_OVER_COPPER_MM` |

The wall's outer edge is rounded with `MASK_WALL_QUAD_SEGS` segments per quarter circle. In
simulation mode all three go into one part per side, `Top Solder Mask` / `Bottom Solder Mask`,
one closed solid. In visual mode the **top** region becomes its own part,
`Top Mask over Copper` / `Bottom Mask over Copper`, with its own colour
([Output Modes](Output-Modes.md)).

### 15.2.1 Thickness

Two values, `MASK_OVER_LAMINATE_MM` and `MASK_OVER_COPPER_MM`, both 10 µm by default (KiCad's own
value). Typical production is 10 to 15 µm over copper and 20 to 30 µm over laminate. When the
stack-up gives a mask thickness and `USE_STACKUP_MASK_THICKNESS = True`, that one value is used
for both. `report.txt` notes the values and their source:
`solder mask: 0.01 mm over laminate, 0.01 mm over copper (stackup)`.

## 15.3 Edge Pull-Back

The mask, and the silkscreen on it, stop `MASK_EDGE_PULLBACK_MM` (5 µm) short of the board edge.
Fabricators pull both back from routed edges, and the small step also keeps `<model-viewer>`
from treating a translucent mask flush with the board edge as a baked shadow.

## 15.4 Over Holes

The mask is removed over the open bore of every hole that reaches that side (the drill minus the
plated wall, or the whole drill of an NPTH), so no mask floats over a hole. A tented via keeps its
mask over the annular ring; its bore is still open.

## 15.5 Settings

| Name | Default | Range | Meaning |
|---|---|---|---|
| `MASK_OVER_LAMINATE_MM` | `0.010` | mm > 0 | Mask thickness over bare laminate |
| `MASK_OVER_COPPER_MM` | `0.010` | mm > 0 | Mask thickness on top of copper |
| `USE_STACKUP_MASK_THICKNESS` | `True` | bool | The stack-up's mask thickness wins, for both values |
| `MASK_EDGE_PULLBACK_MM` | `0.005` | mm ≥ 0 | Mask and silk stop this far from the edge |
| `PAD_TO_MASK_CLEARANCE_MM` | `None` | None or mm ≥ 0 | Clearance around pads; `None` follows the board file |
| `MASK_WALL_QUAD_SEGS` | `4` | int ≥ 1 | Curve quality of the walls beside traces |

| Previous | Next |
|:---|---:|
| [Silkscreens](Silkscreens.md) | [Parameter Reference](Parameter-Reference.md) |
