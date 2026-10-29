# 7. Stack-Up Model

The stack-up decides the height of every layer. It is read once per board
(`kese/s2_collect/stackup.py`), its heights are computed once (`kese/s4_geometry/heights.py`), and
it is printed at the top of `report.txt`, so every z value in the model can be checked against it.

![Board tests/boards/six_layer cut through pad 1 of J1 at true scale: the silkscreen on the mask, the mask on the laminate faces, the ENIG finish on the pad, the outer copper on the faces, the four inner copper layers between five dielectrics, the plated barrel; every layer listed with its thickness and its heights from the laminate mid-plane, and close-ups of the silk on the mask and of the pad's top edge, then two closer still: the finish at the pad's edge, 5 µm of nickel under 0.08 µm of gold beside the mask, and the 80 nm of gold alone](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/stackup_1_cross_section.webp)

## 7.1 Heights

All heights are in mm, measured from the **laminate mid-plane** ($`z = 0`$), with the `F.Cu` side
positive. A board has $`N`$ copper layers $`l_0 \dots l_{N-1}`$, counted from `F.Cu`
($`l_0`$) to `B.Cu` ($`l_{N-1}`$), and $`N-1`$ dielectrics $`d_1 \dots d_{N-1}`$, where
$`d_i`$ lies between $`l_{i-1}`$ and $`l_i`$. Equations are numbered per page.

### 7.1.1 Laminate And Faces

The laminate is the stack of dielectrics plus the inner copper layers:

```math
L = \sum_{i=1}^{N-1} h_i + \sum_{k=1}^{N-2} t_k \qquad (7.1)
```

```math
z_{\mathrm{face}} = \pm \frac{L}{2} \qquad (7.2)
```

| Symbol | Meaning | Unit |
|---|---|---|
| $`L`$ | laminate thickness: dielectrics plus inner copper | mm |
| $`h_i`$ | thickness of dielectric $`d_i`$ | mm |
| $`t_k`$ | foil thickness of inner copper layer $`l_k`$ | mm |
| $`z_{\mathrm{face}}`$ | height of the laminate faces: $`+L/2`$ on the `F.Cu` side, $`-L/2`$ on the `B.Cu` side | mm |

### 7.1.2 Outer Copper

Outer copper sits on the laminate faces. Its finished thickness is the foil plus the plating
added during hole plating:

```math
t_{\mathrm{out}} = t_{\mathrm{foil}} + t_{\mathrm{plate}} \qquad (7.3)
```

```math
z_{\mathrm{F.Cu}} \in \left[ \frac{L}{2},\ \frac{L}{2} + t_{\mathrm{out},F} \right] \qquad (7.4)
```

```math
z_{\mathrm{B.Cu}} \in \left[ -\frac{L}{2} - t_{\mathrm{out},B},\ -\frac{L}{2} \right] \qquad (7.5)
```

| Symbol | Meaning | Parameter |
|---|---|---|
| $`t_{\mathrm{out}}`$ | finished outer copper thickness ($`t_{\mathrm{out},F}`$ for `F.Cu`, $`t_{\mathrm{out},B}`$ for `B.Cu`) | |
| $`t_{\mathrm{foil}}`$ | foil thickness of the outer layer | stack-up, else `Copper.DEFAULT_OUTER_FOIL_MM` |
| $`t_{\mathrm{plate}}`$ | copper added to the outer layers by plating | `Copper.OUTER_PLATING_ADDED_MM` |
| $`z_{\mathrm{F.Cu}}`$, $`z_{\mathrm{B.Cu}}`$ | z range of the outer copper | |

### 7.1.3 Inner Copper

Inner copper lies inside the laminate. Walking down from the top face, each dielectric takes its
thickness and each inner copper layer below it its foil thickness:

```math
z_{\mathrm{top}}(l_k) = \frac{L}{2} - \sum_{i=1}^{k} h_i - \sum_{m=1}^{k-1} t_m \qquad (7.6)
```

```math
z_{\mathrm{bot}}(l_k) = z_{\mathrm{top}}(l_k) - t_k \qquad (7.7)
```

for every inner layer, $`k = 1 \dots N-2`$.

| Symbol | Meaning | Unit |
|---|---|---|
| $`z_{\mathrm{top}}(l_k)`$, $`z_{\mathrm{bot}}(l_k)`$ | top and bottom of inner copper layer $`l_k`$ | mm |
| $`h_i`$ | thickness of dielectric $`d_i`$ | mm |
| $`t_m`$ | foil thickness of inner copper layer $`l_m`$ | mm |

### 7.1.4 Dielectrics

Dielectric $`d_i`$ fills the space between the copper layers above and below it, and reaches the
laminate face where there is no copper layer inside the laminate above or below it:

```math
z_{\mathrm{top}}(d_i) = \begin{cases} L/2 & i = 1 \\ z_{\mathrm{bot}}(l_{i-1}) & i > 1 \end{cases} \qquad (7.8)
```

```math
z_{\mathrm{bot}}(d_i) = \begin{cases} -L/2 & i = N-1 \\ z_{\mathrm{top}}(l_i) & i < N-1 \end{cases} \qquad (7.9)
```

The mask starts at the laminate face and the silkscreen lies on top of the mask; their heights
are in [Solder Masks](Solder-Masks.md) and [Silkscreens](Silkscreens.md).

For a 6-layer board with 0.1 / 0.3 / 0.2 / 0.3 / 0.1 mm dielectrics, 17.5 µm inner foil and
35 µm outer foil (the `tests/boards/six_layer.kicad_pcb` board in the picture), equation (7.1) gives
$`L = 1.0 + 4 \times 0.0175 = 1.07`$ mm and equation (7.6) gives the top of `In1.Cu` at
$`0.535 - 0.1 = 0.435`$ mm, as `report.txt` shows:

```text
  laminate 1.0700 mm (stackup dielectrics (+ inner copper); board total in file 1.2 mm)
  F.Cu     z +0.5350 .. +0.5700 mm  (foil 0.035 mm)
  In1.Cu   z +0.4175 .. +0.4350 mm  (foil 0.0175 mm)
  In2.Cu   z +0.1000 .. +0.1175 mm  (foil 0.0175 mm)
  In3.Cu   z -0.1175 .. -0.1000 mm  (foil 0.0175 mm)
  In4.Cu   z -0.4350 .. -0.4175 mm  (foil 0.0175 mm)
  B.Cu     z -0.5700 .. -0.5350 mm  (foil 0.035 mm)
  dielectric 1             prepreg  FR4        0.1000 mm  er 4.5  tan d 0.02   z +0.4350 .. +0.5350
  dielectric 2             core     FR4        0.3000 mm  er 4.5  tan d 0.02   z +0.1175 .. +0.4175
  ...
```

## 7.2 Where The Numbers Come From

### 7.2.1 With A Stack-Up In The File

KiCad writes `(setup (stackup (layer ...) ...))` once the stack-up has been confirmed in Board
Setup > Physical Stackup; a board whose stack-up was never set there has no such block (none of
the example boards has one). KESE reads, per layer:

| From the stack-up | Used for | Switch |
|---|---|---|
| `(thickness ...)` of each `*.Cu` layer | the foil thickness of that layer | `Copper.USE_STACKUP_COPPER_THICKNESS` |
| `(thickness ...)`, `(type "core" / "prepreg")`, `(material ...)`, `(epsilon_r ...)`, `(loss_tangent ...)` of each `dielectric N` layer | one `Dielectric` per gap between copper layers | `Board.USE_STACKUP_EPSILON_R`, `Board.USE_STACKUP_LOSS_TANGENT` |
| `(thickness ...)` of the first `*.Mask` layer that has one | the mask thickness, over laminate and over copper | `SolderMask.USE_STACKUP_MASK_THICKNESS` |
| `(color ...)` of `F.Mask`, `B.Mask`, `F.SilkS`, `B.SilkS` | the colours in GLB, OBJ and the `look` of `materials.json`, and in STEP when `"mask"` / `"silk"` are added to `Run.STEP_WRITE_ROLES` | `Color.USE_STACKUP_COLORS` |
| `(copper_finish "...")` | the finish type, when `Finish.FINISH_ENABLED = True` (off by default) | `Finish.FINISH_TYPE = "file"` |
| `(edge_plating yes)`, `(castellated_pads yes)` | edge plating and castellations | `Copper.EDGE_PLATING = "file"`, `Copper.CASTELLATION = "file"` |

A stack-up is **usable** when it has exactly one group of dielectric layers between every pair of
consecutive copper layers and every group has a thickness above zero. A gap made of several plies
(two prepregs, or prepreg + core + prepreg) becomes **one** dielectric solid with the summed
thickness and the first ply's type, material, εr and tanδ. Plies written as sub-layers of one
stack-up dielectric keep that dielectric's name (`dielectric 3` in `six_layer`); separate stack-up
dielectrics in one gap give a joined name (`dielectric 1 + dielectric 2`):

```math
h_i = \sum_{p=1}^{P_i} h_{i,p} \qquad (7.10)
```

| Symbol | Meaning |
|---|---|
| $`h_i`$ | thickness of the dielectric solid in gap $`i`$ |
| $`P_i`$ | number of plies in gap $`i`$ |
| $`h_{i,p}`$ | thickness of ply $`p`$ of gap $`i`$, from the stack-up |

The laminate thickness is then equation (7.1). The file's `(general (thickness ...))` is not used
when a usable stack-up is present; `report.txt` only shows it as `board total in file`. (KiCad computes
that number from the stack-up as all copper + all dielectrics + both masks, so for a stack-up
saved from Board Setup it equals the laminate plus the two outer foils and the two masks.)

Any value the stack-up leaves out falls back to the parameter defaults:
`Copper.DEFAULT_OUTER_FOIL_MM`, `Copper.DEFAULT_INNER_FOIL_MM`, `Board.DEFAULT_DIELECTRIC_MATERIAL`,
`Board.DEFAULT_DIELECTRIC_TYPE`, `Board.DEFAULT_EPSILON_R`, `Board.DEFAULT_LOSS_TANGENT`,
`SolderMask.MASK_OVER_LAMINATE_MM` / `MASK_OVER_COPPER_MM`.

### 7.2.2 Without A Stack-Up

When the file has no stack-up block, or an unusable one:

- The laminate thickness is the file's `(general (thickness ...))`, or 1.6 mm when the file has
  none.
- The laminate minus the inner copper is divided **evenly** between the copper layers
  (`Board.DIELECTRIC_SPLIT = "even"`, the only split implemented), equation (7.11). Each gap
  becomes a dielectric named `dielectric 1`, `dielectric 2`, ... of the default type and material
  with the default εr and tanδ.
- Copper layers without a thickness in the file get the default foil thickness (an unusable
  stack-up block may still supply some).

```math
h_i = \frac{L - \sum_{k=1}^{N-2} t_k}{N - 1} \qquad (7.11)
```

| Symbol | Meaning | Parameter |
|---|---|---|
| $`h_i`$ | thickness of every dielectric | |
| $`L`$ | laminate thickness: the file's board thickness, else 1.6 mm | `(general (thickness ...))` |
| $`t_k`$ | foil of inner copper layer $`l_k`$ | `Copper.DEFAULT_INNER_FOIL_MM` |
| $`N`$ | number of copper layers | |

The 4-layer `Coil_30_50_...` example has no stack-up: $`h_i = (1.6 - 2 \times 0.035) / 3 = 0.51`$
mm for each of the three dielectrics.

### 7.2.3 Forcing The Laminate Thickness

`Board.BOARD_THICKNESS_MM` (default `None`) overrides the laminate thickness. With a usable
stack-up the dielectric thicknesses are **scaled** so their proportions are kept; without one the
even split of equation (7.11) is applied to the forced value:

```math
s = \frac{L^{*} - \sum_{k=1}^{N-2} t_k}{\sum_{i=1}^{N-1} h_i} \qquad (7.12)
```

```math
h_i^{*} = s \cdot h_i \qquad (7.13)
```

| Symbol | Meaning | Parameter |
|---|---|---|
| $`L^{*}`$ | forced laminate thickness | `Board.BOARD_THICKNESS_MM` |
| $`h_i`$ | dielectric thickness from the stack-up | |
| $`h_i^{*}`$ | dielectric thickness used | |
| $`s`$ | scale factor | |

`report.txt` states the source on the `laminate` line:

| `report.txt` says | Meaning |
|---|---|
| `stackup dielectrics (+ inner copper); board total in file X mm` | summed from the stack-up |
| `file (general (thickness)) - no usable stackup` | the file's board thickness, split evenly |
| `default 1.6 mm (no thickness in file)` | neither was available |
| `Board.BOARD_THICKNESS_MM` (`... (stackup dielectric proportions kept)`) | forced by the parameter |

> [!IMPORTANT]
> KiCad's defaults (35 µm copper on every layer, 10 µm mask, εr 4.5, tanδ 0.02) are what you get
> when the stack-up is missing. They are typical, not your fabricator's. For lab work, enter the
> fabricator's stack-up in KiCad's Board Setup or set the defaults in `parameters/`.

## 7.3 How The Heights Feed The Model

| Feature | Height used |
|---|---|
| Dielectric $`d_i`$ | equations (7.8) and (7.9) |
| Resin beside inner copper | the inner copper's own band, filled from the adjacent prepreg, else from the dielectric above (box 2 of the picture; [Board](Board.md)) |
| Copper of layer $`l_k`$ | its band, equations (7.4) to (7.7) |
| Via barrel from layer $`l_i`$ to $`l_j`$ | between the copper layers it joins; outer copper caps it, inner copper is drilled through, so the barrel passes through inner bands ([Copper And Traces](Copper-And-Traces.md)) |
| Solder mask | from the laminate face: mask thickness over laminate, copper + mask thickness over copper ([Solder Masks](Solder-Masks.md)) |
| Silkscreen | on top of the mask surface ([Silkscreens](Silkscreens.md)) |
| Surface finish | stacked on top of the outer copper where the mask is open (boxes 4 and 5 of the picture; [Top And Bottom Copper Finishings](Copper-Finishings.md)) |

| Previous | Next |
|:---|---:|
| [Working Principle](Working-Principle.md) | [Output Modes](Output-Modes.md) |
