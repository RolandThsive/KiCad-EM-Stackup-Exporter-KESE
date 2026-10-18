# 7. Stack-Up Model

The stack-up decides the height of every layer. It is built once per board in
`Generator/Common/stackup.py` and printed at the top of `report.txt`, so every z value in the model
can be checked against it.

<!-- Picture wanted: Stackup 1, a cross-section of a 4-layer board with the z axis, the laminate
     mid-plane at z = 0, outer copper on the faces, inner copper inside, mask and silk on top. -->

## 7.1 Heights

All heights are in mm, measured from the **laminate mid-plane** (z = 0), with the `F.Cu` side
positive.

- The laminate is the stack of dielectrics plus the inner copper layers, of total thickness
  $L$. Its faces are at $z = \pm L/2$.
- **Outer copper** sits on the laminate faces: `F.Cu` from $+L/2$ up to $+L/2 + t_F$, `B.Cu` from
  $-L/2$ down to $-L/2 - t_B$, where $t$ is the finished outer copper,
  $t = \text{foil} + \texttt{Copper.OUTER\_PLATING\_ADDED\_MM}$.
- **Inner copper** lies inside the laminate. Walking down from the top face, each dielectric
  takes its thickness, then the inner copper below it takes its foil thickness, and so on.
- The solder mask starts at the laminate face and the silkscreen on top of the mask; see
  [Solder Masks](Solder-Masks.md) and [Silkscreens](Silkscreens.md).

For a 6-layer board with 0.1 / 0.3 / 0.2 / 0.3 / 0.1 mm dielectrics, 17.5 µm inner foil and
35 µm outer foil (the `Tests/boards/six_layer.kicad_pcb` board):

```text
laminate 1.0700 mm (stackup dielectrics (+ inner copper); board total in file 1.2 mm)
F.Cu     z +0.5350 .. +0.5700 mm  (foil 0.035 mm)
In1.Cu   z +0.4175 .. +0.4350 mm  (foil 0.0175 mm)
In2.Cu   z +0.1000 .. +0.1175 mm  (foil 0.0175 mm)
In3.Cu   z -0.1175 .. -0.1000 mm  (foil 0.0175 mm)
In4.Cu   z -0.4350 .. -0.4175 mm  (foil 0.0175 mm)
B.Cu     z -0.5700 .. -0.5350 mm  (foil 0.035 mm)
dielectric 1   prepreg  FR4  0.1000 mm  er 4.5  tan d 0.02   z +0.4350 .. +0.5350
dielectric 2   core     FR4  0.3000 mm  er 4.5  tan d 0.02   z +0.1175 .. +0.4175
...
```

## 7.2 Where The Numbers Come From

### 7.2.1 With A Stack-Up In The File

KiCad writes `(setup (stackup (layer ...) ...))` once the stack-up has been edited in Board
Setup > Physical Stackup. KESE reads, per layer:

| From the stack-up | Used for | Switch |
|---|---|---|
| `(thickness ...)` of each `*.Cu` layer | the foil thickness of that layer | `Copper.USE_STACKUP_COPPER_THICKNESS` |
| `(thickness ...)`, `(type "core" / "prepreg")`, `(material ...)`, `(epsilon_r ...)`, `(loss_tangent ...)` of each `dielectric N` layer | one `Dielectric` per gap between copper layers | `Board.USE_STACKUP_EPSILON_R`, `Board.USE_STACKUP_LOSS_TANGENT` |
| `(thickness ...)` of the first `*.Mask` layer | the mask thickness, over laminate and over copper | `SolderMask.USE_STACKUP_MASK_THICKNESS` |
| `(color ...)` of `F.Mask`, `B.Mask`, `F.SilkS`, `B.SilkS` | the colours in GLB / OBJ | `Color.USE_STACKUP_COLORS` |
| `(copper_finish "...")` | the finish type | `Finish.FINISH_TYPE = "file"` |
| `(edge_plating yes)`, `(castellated_pads yes)` | edge plating and castellations | `Copper.EDGE_PLATING = "file"`, `Copper.CASTELLATION = "file"` |

A stack-up is **usable** when it has exactly one group of dielectric layers between every pair of
consecutive copper layers and every group has a thickness above zero. A gap made of several plies
(two prepregs, or prepreg + core + prepreg) becomes **one** dielectric solid with the summed
thickness and the first ply's type, material, εr and tanδ; its name joins the ply names
(`dielectric 1 + dielectric 2`). The laminate thickness is then the sum of all dielectrics plus
the inner copper, so that laminate + outer copper + mask equals KiCad's board thickness.

Any value the stack-up leaves out falls back to the parameter defaults:
`Copper.DEFAULT_OUTER_FOIL_MM`, `Copper.DEFAULT_INNER_FOIL_MM`, `Board.DEFAULT_DIELECTRIC_MATERIAL`,
`Board.DEFAULT_DIELECTRIC_TYPE`, `Board.DEFAULT_EPSILON_R`, `Board.DEFAULT_LOSS_TANGENT`,
`SolderMask.MASK_OVER_LAMINATE_MM` / `MASK_OVER_COPPER_MM`.

### 7.2.2 Without A Stack-Up

When the file has no stack-up block, or an unusable one:

- The laminate thickness is the file's `(general (thickness ...))`, or 1.6 mm when the file has
  none.
- The laminate minus the inner copper is divided **evenly** between the copper layers
  (`Board.DIELECTRIC_SPLIT = "even"`, the only split implemented). Each gap becomes a dielectric
  named `dielectric 1`, `dielectric 2`, ... of the default type and material with the default εr
  and tanδ.
- Every copper layer gets the default foil thickness.

The 4-layer `Coil_30_50_...` example has no stack-up: 1.6 mm minus two 35 µm inner foils gives
three dielectrics of 0.51 mm each.

### 7.2.3 Forcing The Laminate Thickness

`Board.BOARD_THICKNESS_MM` (default `None`) overrides the laminate thickness. With a usable
stack-up the dielectric thicknesses are **scaled** so their proportions are kept; without one the
even split is applied to the forced value. `report.txt` states the source on the `laminate` line:

| `report.txt` says | Meaning |
|---|---|
| `stackup dielectrics (+ inner copper); board total in file X mm` | summed from the stack-up |
| `file (general (thickness)) - no usable stackup` | the file's board thickness, split evenly |
| `default 1.6 mm (no thickness in file)` | neither was available |
| `Board_Parameters.BOARD_THICKNESS_MM` (`... (stackup dielectric proportions kept)`) | forced by the parameter |

> [!IMPORTANT]
> KiCad's defaults (35 µm copper on every layer, 10 µm mask, εr 4.5, tanδ 0.02) are what you get
> when the stack-up is missing. They are typical, not your fabricator's. For lab work, enter the
> fabricator's stack-up in KiCad's Board Setup or set the defaults in `Parameters/`.

## 7.3 How The Heights Feed The Model

| Feature | Height used |
|---|---|
| Dielectric $i$ | from the bottom of the copper layer above it to the top of the copper layer below it (the faces of the laminate for the outermost) |
| Resin beside inner copper | the inner copper's own band, filled by the neighbouring prepreg's material ([Board](Board.md)) |
| Copper of layer $l$ | its band `(z_lo, z_hi)` |
| Via barrel from layer $i$ to $j$ | between the copper layers it joins; outer copper caps it, inner copper is drilled through, so the barrel passes through inner bands ([Copper And Traces](Copper-And-Traces.md)) |
| Solder mask | from the laminate face: mask thickness over laminate, copper + mask thickness over copper ([Solder Masks](Solder-Masks.md)) |
| Silkscreen | on top of the mask surface ([Silkscreens](Silkscreens.md)) |
| Surface finish | stacked on top of the outer copper where the mask is open ([Top And Bottom Copper Finishings](Copper-Finishings.md)) |

| Previous | Next |
|:---|---:|
| [Working Principle](Working-Principle.md) | [Output Modes](Output-Modes.md) |
