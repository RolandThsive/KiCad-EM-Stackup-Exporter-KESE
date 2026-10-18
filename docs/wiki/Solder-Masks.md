# 15. Solder Masks

The solder mask is the lacquer (LPI) over both faces of the board. `Generator/Geometry/SolderMask.py`
builds it; the settings are in `Parameters/SolderMask_Parameters.py`.

<!-- Pictures wanted for this page (made by Roland):
     Mask 1: a top view of mask openings: pads with clearance, an untented via, a drawn opening.
     Mask 2: a cross-section of the conformal mask: flat on laminate, raised on a trace, the wall
             beside the trace, with MASK_OVER_LAMINATE_MM and MASK_OVER_COPPER_MM marked. -->

## 15.1 KiCad's Mask Layers Are Negative

Whatever is drawn on `F.Mask` / `B.Mask` is an **opening**, not mask. KESE builds, per side:

```math
M_\sigma = \left( \left( O \setminus B_\sigma \right) \setminus Q_\sigma \right) \cap \left( O \ominus p \right) \qquad (15.1)
```

| Symbol | Meaning | Parameter |
|---|---|---|
| $`M_\sigma`$ | mask region on side $`\sigma`$ (`F` or `B`) | |
| $`O`$ | board outline, equation (10.3) | |
| $`B_\sigma`$ | bores of every hole that reaches side $`\sigma`$, equation (11.4) | |
| $`Q_\sigma`$ | the mask openings on side $`\sigma`$, equation (15.2) | |
| $`p`$ | edge pull-back | `SolderMask.MASK_EDGE_PULLBACK_MM` |

The openings are:

| Opening | Size |
|---|---|
| every pad that lists the mask layer (`F.Mask`, `B.Mask`, `*.Mask`) | the pad shape grown by its mask margin: the pad's own `solder_mask_margin`, else the footprint's, else the board's pad-to-mask clearance, or `SolderMask.PAD_TO_MASK_CLEARANCE_MM` when set |
| every untented via (see [via tenting](Copper-And-Traces.md#1132-via-tenting)) | the via pad grown by the board's clearance |
| graphics, text and zone fills drawn on the mask layer | as drawn |

Together:

```math
Q_\sigma = \left( \bigcup_{\text{pads}} \left( P \oplus m_P \right) \cup \bigcup_{\text{open vias}} \left( V \oplus c \right) \cup \bigcup_{\text{drawn}} G \right) \cap O \qquad (15.2)
```

```math
m_P = \begin{cases} m_{\mathrm{pad}} & \text{if the pad gives one} \\ m_{\mathrm{fp}} & \text{else if the footprint gives one} \\ c & \text{otherwise} \end{cases} \qquad (15.3)
```

| Symbol | Meaning | Parameter |
|---|---|---|
| $`P`$, $`V`$, $`G`$ | a pad shape, a via pad, a shape drawn on the mask layer | |
| $`\oplus m`$ | grows a region outward by $`m`$ (a buffer) | |
| $`m_{\mathrm{pad}}`$, $`m_{\mathrm{fp}}`$ | the pad's and the footprint's `solder_mask_margin` | the board file |
| $`c`$ | pad-to-mask clearance | board setup, or `SolderMask.PAD_TO_MASK_CLEARANCE_MM` when set |

Openings are clipped to the outline. `report.txt` counts `pad mask openings on F.Mask` and the
clearance used on its `vias:` line.

## 15.2 Conformal Mask

LPI mask follows the copper: it is thin on top of a trace and thicker on the bare laminate
beside it, and it climbs the side of every trace. KESE splits the mask region of equation (15.1)
into three regions with the outer copper $`C_\sigma`$ of that side:

```math
M^{\mathrm{flat}} = M_\sigma \setminus \left( C_\sigma \oplus m_L \right) \qquad (15.4)
```

```math
M^{\mathrm{top}} = M_\sigma \cap C_\sigma \qquad (15.5)
```

```math
M^{\mathrm{wall}} = M_\sigma \cap \left( \left( C_\sigma \oplus m_L \right) \setminus C_\sigma \right) \qquad (15.6)
```

and extrudes them, on the `F` side, over

```math
z^{\mathrm{flat}} \in \left[ \frac{L}{2},\ \frac{L}{2} + m_L \right], \qquad z^{\mathrm{top}} \in \left[ \frac{L}{2} + t_{\mathrm{out}},\ \frac{L}{2} + t_{\mathrm{out}} + m_C \right], \qquad z^{\mathrm{wall}} \in \left[ \frac{L}{2},\ \frac{L}{2} + t_{\mathrm{out}} + m_C \right] \qquad (15.7)
```

On the `B` side every z is mirrored ($`z \to -z`$).

| Symbol | Meaning | Parameter |
|---|---|---|
| $`M^{\mathrm{flat}}`$ | mask on bare laminate, farther than $`m_L`$ from any copper | |
| $`M^{\mathrm{top}}`$ | mask on top of copper | |
| $`M^{\mathrm{wall}}`$ | the band $`m_L`$ wide beside copper where the mask climbs | |
| $`C_\sigma`$ | all outer copper of side $`\sigma`$, every net | |
| $`m_L`$ | mask thickness over laminate | `SolderMask.MASK_OVER_LAMINATE_MM` |
| $`m_C`$ | mask thickness over copper | `SolderMask.MASK_OVER_COPPER_MM` |
| $`t_{\mathrm{out}}`$ | finished outer copper thickness, equation (7.3) | |
| $`L`$ | laminate thickness, equation (7.1) | |

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

The mask, and the silkscreen on it, stop `MASK_EDGE_PULLBACK_MM` (5 µm) short of the board edge:
the $`\cap (O \ominus p)`$ term of equation (15.1).
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
