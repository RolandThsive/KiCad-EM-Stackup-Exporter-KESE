# 8. Stack-Up Model

The stack-up decides the height of every layer. It is read once per board
(`kese/s2_collect/stackup.py`), its heights are computed once (`kese/s4_geometry/heights.py`), and
it is printed at the top of `report.txt`, so every z value in the model can be checked against it.
Which of its layers go into the files is said in one place, `parameters/PCB_elements/Stackup.py`
([8.4](#84-what-is-built-the-lines-of-stackuppy)), and the laminate is built in one of two ways: its
plies fused, one solid for each gap between two copper layers, or its plies separate
([8.3](#83-the-plies-of-a-gap-fused-or-separate)).

![Board tests/boards/six_layer cut through pad 1 of J1 at true scale: the silkscreen on the mask, the mask on the laminate faces, the ENIG finish on the pad, the outer copper on the faces, the four inner copper layers between five dielectrics, the plated barrel; every layer listed with its thickness and its heights from the laminate mid-plane, and close-ups of the silk on the mask and of the pad's top edge, then two closer still: the finish at the pad's edge, 5 µm of nickel under 0.08 µm of gold beside the mask, and the 80 nm of gold alone](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Stack-Up-Model/stackup_1_cross_section.webp)

## 8.1 Heights

All heights are in mm, measured from the **laminate mid-plane** ($`z = 0`$), with the `F.Cu` side
positive. A board has $`N`$ copper layers $`l_0 \dots l_{N-1}`$, counted from `F.Cu`
($`l_0`$) to `B.Cu` ($`l_{N-1}`$), and $`N-1`$ dielectrics $`d_1 \dots d_{N-1}`$, where
$`d_i`$ lies between $`l_{i-1}`$ and $`l_i`$. Equations are numbered per page.

### 8.1.1 Laminate And Faces

The laminate is the stack of dielectrics plus the inner copper layers:

```math
L = \sum_{i=1}^{N-1} h_i + \sum_{k=1}^{N-2} t_k \qquad (8.1)
```

```math
z_{\mathrm{face}} = \pm \frac{L}{2} \qquad (8.2)
```

| Symbol | Meaning | Unit |
|---|---|---|
| $`L`$ | laminate thickness: dielectrics plus inner copper | mm |
| $`h_i`$ | thickness of dielectric $`d_i`$ | mm |
| $`t_k`$ | foil thickness of inner copper layer $`l_k`$ | mm |
| $`z_{\mathrm{face}}`$ | height of the laminate faces: $`+L/2`$ on the `F.Cu` side, $`-L/2`$ on the `B.Cu` side | mm |

### 8.1.2 Outer Copper

Outer copper sits on the laminate faces. Its finished thickness is the foil plus the plating
added during hole plating:

```math
t_{\mathrm{out}} = t_{\mathrm{foil}} + t_{\mathrm{plate}} \qquad (8.3)
```

```math
z_{\mathrm{F.Cu}} \in \left[ \frac{L}{2},\ \frac{L}{2} + t_{\mathrm{out},F} \right] \qquad (8.4)
```

```math
z_{\mathrm{B.Cu}} \in \left[ -\frac{L}{2} - t_{\mathrm{out},B},\ -\frac{L}{2} \right] \qquad (8.5)
```

| Symbol | Meaning | Parameter |
|---|---|---|
| $`t_{\mathrm{out}}`$ | finished outer copper thickness ($`t_{\mathrm{out},F}`$ for `F.Cu`, $`t_{\mathrm{out},B}`$ for `B.Cu`) | |
| $`t_{\mathrm{foil}}`$ | foil thickness of the outer layer | stack-up, else `Copper.DEFAULT_TOP_FOIL_MM` for `F.Cu` and `Copper.DEFAULT_BOTTOM_FOIL_MM` for `B.Cu` |
| $`t_{\mathrm{plate}}`$ | copper added to the outer layer by plating, each side with its own value | `Copper.TOP_PLATING_ADDED_MM`, `Copper.BOTTOM_PLATING_ADDED_MM` |
| $`z_{\mathrm{F.Cu}}`$, $`z_{\mathrm{B.Cu}}`$ | z range of the outer copper | |

### 8.1.3 Inner Copper

Inner copper lies inside the laminate. Walking down from the top face, each dielectric takes its
thickness and each inner copper layer below it its foil thickness:

```math
z_{\mathrm{top}}(l_k) = \frac{L}{2} - \sum_{i=1}^{k} h_i - \sum_{m=1}^{k-1} t_m \qquad (8.6)
```

```math
z_{\mathrm{bot}}(l_k) = z_{\mathrm{top}}(l_k) - t_k \qquad (8.7)
```

for every inner layer, $`k = 1 \dots N-2`$.

| Symbol | Meaning | Unit |
|---|---|---|
| $`z_{\mathrm{top}}(l_k)`$, $`z_{\mathrm{bot}}(l_k)`$ | top and bottom of inner copper layer $`l_k`$ | mm |
| $`h_i`$ | thickness of dielectric $`d_i`$ | mm |
| $`t_m`$ | foil thickness of inner copper layer $`l_m`$ | mm |

### 8.1.4 Dielectrics

Dielectric $`d_i`$ fills the space between the copper layers above and below it, and reaches the
laminate face where there is no copper layer inside the laminate above or below it:

```math
z_{\mathrm{top}}(d_i) = \begin{cases} L/2 & i = 1 \\ z_{\mathrm{bot}}(l_{i-1}) & i > 1 \end{cases} \qquad (8.8)
```

```math
z_{\mathrm{bot}}(d_i) = \begin{cases} -L/2 & i = N-1 \\ z_{\mathrm{top}}(l_i) & i < N-1 \end{cases} \qquad (8.9)
```

The mask starts at the laminate face and the silkscreen lies on top of the mask; their heights
are in [Solder Masks](Solder-Masks.md) and [Silkscreens](Silkscreens.md).

For a 6-layer board with 0.1 / 0.3 / 0.2 / 0.3 / 0.1 mm dielectrics, 17.5 µm inner foil and
35 µm outer foil (the `tests/boards/six_layer.kicad_pcb` board in the picture), equation (8.1) gives
$`L = 1.0 + 4 \times 0.0175 = 1.07`$ mm and equation (8.6) gives the top of `In1.Cu` at
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

## 8.2 Where The Numbers Come From

### 8.2.1 With A Stack-Up In The File

KiCad writes `(setup (stackup (layer ...) ...))` once the stack-up has been confirmed in Board
Setup > Physical Stackup; a board whose stack-up was never set there has no such block (the
three example boards have one, `featureTest/15_stackup_none` has none). KESE reads, per layer:

| From the stack-up | Used for | Switch |
|---|---|---|
| `(thickness ...)` of each `*.Cu` layer | the foil thickness of that layer | `Copper.USE_STACKUP_COPPER_THICKNESS` |
| `(thickness ...)`, `(type "core" / "prepreg")`, `(material ...)`, `(epsilon_r ...)`, `(loss_tangent ...)` of each `dielectric N` layer, sub-layer by sub-layer | the plies of the gap between two copper layers: each sub-layer of a dielectric is one ply, with its own thickness and material | `Board.USE_STACKUP_EPSILON_R`, `Board.USE_STACKUP_LOSS_TANGENT` |
| `(spec_frequency ...)` and `(dielectric_model ...)` of each sub-layer (KiCad's development version, file format 20260511 on) | the frequency a ply's εr and tan δ are given at, and how they change with frequency ([Material Properties](Material-Properties.md#214-how-εr-and-tan-δ-change-with-frequency)) | `Board.USE_STACKUP_SPEC_FREQUENCY`, `Board.USE_STACKUP_DIELECTRIC_MODEL` |
| `(thickness ...)` of the first `*.Mask` layer that has one | the mask thickness, over laminate and over copper | `SolderMask.USE_STACKUP_MASK_THICKNESS` |
| `(material ...)`, `(epsilon_r ...)`, `(loss_tangent ...)` of `F.Mask` and of `B.Mask` | the material of the top and of the bottom mask in `materials.json`, each side its own | `SolderMask.USE_STACKUP_MASK_MATERIAL` |
| `(color ...)` of `F.Mask`, `B.Mask`, `F.SilkS`, `B.SilkS` | the colours in GLB, OBJ and the `look` of `materials.json`, and in STEP | `SolderMask.USE_STACKUP_MASK_COLOR`, `SilkScreen.USE_STACKUP_SILK_COLOR` |
| `(copper_finish "...")` | the finish type, with `Finish.FINISH_TYPE = "file"` (the default is `"ENIG"`; with `"file"` a board that names no finish is an error) | `Finish.FINISH_TYPE` |
| `(edge_plating yes)`, `(castellated_pads yes)` | edge plating and castellations | `Copper.EDGE_PLATING = "file"`, `Copper.CASTELLATION = "file"` |

A stack-up is **usable** when it has exactly one group of dielectric layers between every pair of
consecutive copper layers and every group has a thickness above zero. A gap can be made of several
plies: two prepregs pressed together, or prepreg + core + prepreg. KiCad writes them as sub-layers of
one stack-up dielectric (the word `addsublayer` between them), and KESE reads every one as a ply
with its own thickness, type, material, εr and tan δ. The thickness of the gap is the sum of its
plies, whichever way the laminate is built:

```math
h_i = \sum_{p=1}^{P_i} h_{i,p} \qquad (8.10)
```

| Symbol | Meaning |
|---|---|
| $`h_i`$ | thickness of the dielectric in gap $`i`$ |
| $`P_i`$ | number of plies in gap $`i`$ |
| $`h_{i,p}`$ | thickness of ply $`p`$ of gap $`i`$, from the stack-up |

The laminate thickness is then equation (8.1). The file's `(general (thickness ...))` is not used
when a usable stack-up is present; `report.txt` only shows it as `board total in file`. (KiCad computes
that number from the stack-up as all copper + all dielectrics + both masks, so for a stack-up
saved from Board Setup it equals the laminate plus the two outer foils and the two masks.)

Any value the stack-up leaves out falls back to the parameter defaults:
`Copper.DEFAULT_TOP_FOIL_MM`, `Copper.DEFAULT_INNER_FOIL_MM`, `Copper.DEFAULT_BOTTOM_FOIL_MM`,
`Board.DEFAULT_DIELECTRIC_MATERIAL`, `Board.DEFAULT_DIELECTRIC_TYPE`, `Board.DEFAULT_EPSILON_R`,
`Board.DEFAULT_LOSS_TANGENT`, `Board.DEFAULT_SPEC_FREQUENCY_HZ`, `Board.DIELECTRIC_MODEL`,
`SolderMask.MASK_OVER_LAMINATE_MM` / `MASK_OVER_COPPER_MM`, and `SolderMask.MASK_MATERIAL`,
`MASK_EPSILON_R` and `MASK_LOSS_TANGENT`. A gap can also be given other plies than the file's, for
one board, in `Board.PLIES_BY_HAND` ([Board](Board.md#1214-plies-written-by-hand)).

### 8.2.2 Without A Stack-Up

When the file has no stack-up block, or an unusable one:

- The laminate thickness is the file's `(general (thickness ...))`, or 1.6 mm
  (`Board.DEFAULT_BOARD_THICKNESS_MM`) when the file has none, less the outer copper and the two masks (`SolderMask.MASK_OVER_COPPER_MM` each, unless the block gives a mask thickness), as
  KiCad's default stack-up counts them (`BOARD_STACKUP::BuildDefaultStackupList`), so the
  finished board is KiCad's board thickness, equation (8.10b).
- The laminate minus the inner copper is divided **evenly** between the copper layers
  (`Board.DIELECTRIC_SPLIT = "even"`, the only split implemented), equation (8.11). Each gap
  becomes a dielectric named `dielectric 1`, `dielectric 2`, ... of the default type and material
  with the default εr and tanδ.
- Copper layers without a thickness in the file get the default foil thickness (an unusable
  stack-up block may still supply some).

```math
L = T - t_{l_0} - t_{l_{N-1}} - 2\,m \qquad (8.10b)
```

```math
h_i = \frac{L - \sum_{k=1}^{N-2} t_k}{N - 1} \qquad (8.11)
```

| Symbol | Meaning | Parameter |
|---|---|---|
| $`h_i`$ | thickness of every dielectric | |
| $`L`$ | laminate thickness, equation (8.10b) | |
| $`T`$ | the file's board thickness, else `Board.DEFAULT_BOARD_THICKNESS_MM` (1.6 mm) | `(general (thickness ...))` |
| $`t_{l_0}`$, $`t_{l_{N-1}}`$ | foil of the outer copper layers | `Copper.DEFAULT_TOP_FOIL_MM`, `Copper.DEFAULT_BOTTOM_FOIL_MM` |
| $`m`$ | mask thickness over copper: the stack-up's mask thickness when an unusable stack-up block gives one, else the parameter | `SolderMask.MASK_OVER_COPPER_MM` |
| $`t_k`$ | foil of inner copper layer $`l_k`$ | `Copper.DEFAULT_INNER_FOIL_MM` |
| $`N`$ | number of copper layers | |

The 4-layer `featureTest/15_stackup_none` has no stack-up and a 1.2 mm board:
$`L = 1.2 - 2 \times 0.035 - 2 \times 0.010 = 1.11`$ mm and
$`h_i = (1.11 - 2 \times 0.035) / 3 = 0.3467`$ mm for each of the three dielectrics.

### 8.2.3 Forcing The Laminate Thickness

`Board.BOARD_THICKNESS_MM` (default `None`) overrides the laminate thickness. With a usable
stack-up the dielectric thicknesses are **scaled** so their proportions are kept; without one the
even split of equation (8.11) is applied to the forced value:

```math
s = \frac{L^{*} - \sum_{k=1}^{N-2} t_k}{\sum_{i=1}^{N-1} h_i} \qquad (8.12)
```

```math
h_i^{*} = s \cdot h_i \qquad (8.13)
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
| `file (general (thickness T)) less the outer copper and the masks - no usable stackup` | the file's board thickness less outer copper and masks, split evenly |
| `default 1.6 mm (Board.DEFAULT_BOARD_THICKNESS_MM) less the outer copper and the masks (no thickness in file)` | neither was available |
| `Board.BOARD_THICKNESS_MM` (`... (stackup dielectric proportions kept)`) | forced by the parameter |

> [!IMPORTANT]
> KiCad's defaults (35 µm copper on every layer, 10 µm mask, εr 4.5, tanδ 0.02) are what you get
> when the stack-up is missing. They are typical, not your fabricator's. For lab work, enter the
> fabricator's stack-up in KiCad's Board Setup or set the defaults in `parameters/`.

## 8.3 The Plies Of A Gap: Fused Or Separate

`Stackup.FUSION_BUILD` says how the laminate is built from the plies the file gives. The copper,
the masks, the silkscreen and the finish are the same either way, and so is the laminate as a
whole: the same volume, cut by the same holes.

### 8.3.1 Plies Fused

`FUSION_BUILD = "PLIES_FUSED"`, the default: one solid for each gap between two copper layers,
from equations (8.8) and (8.9). The plies of the gap are fused into it, and so is the resin between
the traces of the inner copper beside it, which belongs to the prepreg next to it (the dielectric
above, where both or neither are prepreg).

![A real four-layer board, JLCPCB's JLC04161H-2116C, cut through as KESE builds it with the plies fused: three laminate solids, each in its own colour. Board_dielectric 1 is one solid of the 2116 and the 1080 ply and the resin beside In1.Cu, 0.2004 mm in all with the 2116 ply's values; Board_dielectric 2 is the core, 1.065 mm; Board_dielectric 3 is one solid of the 1080 and the 2116 ply and the resin beside In2.Cu. Copper is one solid per net, the mask and the silkscreen one solid per side, the finish one per metal and side](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Stack-Up-Model/stackup_2_plies_fused.webp)

The solid takes its **first** ply's type, material, εr and tan δ, top to bottom
(`Board.FUSED_PROPERTIES = "first"`), or its plies' values in series
(`"series"`, [Material Properties](Material-Properties.md#215-a-gap-whose-plies-differ)). Either way
`materials.json` lists every ply of the gap under `plies`, so nothing the file says is lost. Plies
written as sub-layers of one stack-up dielectric keep that dielectric's name (`dielectric 3` in
`six_layer`); separate stack-up dielectrics in one gap give a joined name
(`dielectric 1 + dielectric 2`).

### 8.3.2 Plies Separate

`FUSION_BUILD = "PLIES_SEPARATE"`: every layer of the laminate that a fabricator makes separately is
its own solid, with its own thickness and material.

![The same four-layer board with the plies separate: seven laminate solids. Board_dielectric 1 ply 1, the 2116 prepreg ply of 0.124 mm with εr 4.16; Board_dielectric 1 ply 2, the 1080 ply of 0.0764 mm with εr 3.91; Board_resin In1.Cu, the resin between the traces of In1.Cu, 0.0152 mm; Board_dielectric 2, the core of 1.065 mm; Board_resin In2.Cu; Board_dielectric 3 ply 1, the 1080 ply; and Board_dielectric 3 ply 2, the 2116 ply](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Stack-Up-Model/stackup_3_plies_separate.webp)

The plies of gap $`i`$ are stacked down from the top of the gap, the last one ending at its bottom:

```math
z_{\mathrm{top}}(d_{i,p}) = z_{\mathrm{top}}(d_i) - \sum_{q=1}^{p-1} h_{i,q} \qquad (8.14)
```

```math
z_{\mathrm{bot}}(d_{i,p}) = \begin{cases} z_{\mathrm{bot}}(d_i) & p = P_i \\ z_{\mathrm{top}}(d_{i,p}) - h_{i,p} & p < P_i \end{cases} \qquad (8.15)
```

| Symbol | Meaning |
|---|---|
| $`d_{i,p}`$ | ply $`p`$ of gap $`i`$, counted from the top |
| $`z_{\mathrm{top}}(d_i)`$, $`z_{\mathrm{bot}}(d_i)`$ | top and bottom of the gap, equations (8.8) and (8.9) |
| $`h_{i,q}`$ | thickness of ply $`q`$ of gap $`i`$, from the stack-up |
| $`P_i`$ | number of plies in gap $`i`$ |

The resin between the traces of inner copper layer $`l_k`$ fills that layer's own band, from
$`z_{\mathrm{bot}}(l_k)`$ to $`z_{\mathrm{top}}(l_k)`$, wherever the layer has no copper. A ply
is named `dielectric N ply M` where its dielectric has several and `dielectric N` where it has one;
the resin is `resin In1.Cu`. What happens to a ply too thin to build, to equal neighbours, and to
plies given by hand is in [Board](Board.md#1213-equal-plies-and-thin-plies).

`report.txt` prints the laminate as it is built, under a heading that names the stack-up and its
lines. With the plies fused, a gap of several plies says what it was fused from
(`featureTest/29d_stackup_real`, the board of the two pictures):

```text
stack-up   built: PLIES_FUSED (parameters/PCB_elements/Stackup.py)
  lines built: top_finish, top_copper, board, resin_between_traces, inner_copper, bottom_copper, bottom_finish, plated_holes, hole_finish, via_resin
  lines left out: top_silkscreen, top_solder_mask, bottom_solder_mask, bottom_silkscreen
  ...
  dielectric 1             prepreg  2116       0.2004 mm  er 4.16  tan d 0.02   z +0.5477 .. +0.7481
    fused from dielectric 1 ply 1: prepreg 2116 0.1240 mm  er 4.16  tan d 0.02
    fused from dielectric 1 ply 2: prepreg 1080 0.0764 mm  er 3.91  tan d 0.02
  dielectric 2             core     FR4 core   1.0650 mm  er 4.6  tan d 0.02   z -0.5325 .. +0.5325
```

With the plies separate every ply and every resin band has its own row:

```text
stack-up   built: PLIES_SEPARATE (parameters/PCB_elements/Stackup.py)
  ...
  dielectric 1 ply 1       prepreg  2116       0.1240 mm  er 4.16  tan d 0.02   z +0.6241 .. +0.7481
  dielectric 1 ply 2       prepreg  1080       0.0764 mm  er 3.91  tan d 0.02   z +0.5477 .. +0.6241
  resin In1.Cu             resin    resin      0.0152 mm  er 3.5  tan d 0.02   z +0.5325 .. +0.5477   (flowed from dielectric 1 ply 2)
  dielectric 2             core     FR4 core   1.0650 mm  er 4.6  tan d 0.02   z -0.5325 .. +0.5325
  resin In2.Cu             resin    resin      0.0152 mm  er 3.5  tan d 0.02   z -0.5477 .. -0.5325   (flowed from dielectric 3 ply 1)
  dielectric 3 ply 1       prepreg  1080       0.0764 mm  er 3.91  tan d 0.02   z -0.6241 .. -0.5477
  dielectric 3 ply 2       prepreg  2116       0.1240 mm  er 4.16  tan d 0.02   z -0.7481 .. -0.6241
```

## 8.4 What Is Built: The Lines Of Stackup.py

`parameters/PCB_elements/Stackup.py` lists the board's layers as they lie in a real board, from the
top silkscreen down to the bottom silkscreen, once for each of the two stack-ups. Each line is
`True` (built, and written to every file in every mode and format) or `False` (left out):

```python
FUSION_BUILD = "PLIES_FUSED"

PLIES_FUSED = {
    # ---- the top side, from the outside in ----
    "top_silkscreen":          False,  # the legend ink on the top solder mask
    "top_solder_mask":         False,  # the solder mask on the top face
    "top_finish":              True,   # ENIG, HASL ... on the top copper the mask leaves bare
    "top_copper":              True,   # F.Cu: the foil and the copper plated on it
    # ---- the inside of the board ----
    "board":                   True,   # the laminate: one solid for each gap, its plies fused
    "resin_between_traces":    True,   # the board solids also fill the space between the inner traces
    "inner_copper":            True,   # In1.Cu, In2.Cu ...
    # ---- the bottom side, from the inside out ----
    "bottom_copper":           True,
    "bottom_finish":           True,
    "bottom_solder_mask":      False,
    "bottom_silkscreen":       False,
    # ---- through the board ----
    "plated_holes":            True,   # the plated walls of vias and holes, castellations, the plated edge
    "hole_finish":             True,   # the finish inside the plated holes and on the board's edge
    "via_resin":               True,   # the resin in plugged and resin-filled vias
}
```

`PLIES_SEPARATE` has the same lines, with `prepreg_plies` and `cores` in place of `board`. The file
holds no thickness, material or colour: those are in each element's own file beside it
([Parameter Reference](Parameter-Reference.md#191-stackup-parameterspcb_elementsstackuppy) has
every line and what it builds).

![A four-layer board cut through six times at the same place, thin layers drawn thicker: with every line of Stackup.py True, both silkscreens, both masks, the finish, the copper, the laminate and the plated walls are all there; with the file's defaults the masks and the silkscreens are left out and the finish is still only on the pads; with Stackup.finish False copper and laminate are left; with the four lines of the bottom side False the top side and the inside are unchanged; with resin_between_traces False the space beside the inner copper is empty; and with only board and resin_between_traces True the laminate stands alone, with its holes and the pockets of the inner copper](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Stack-Up-Model/stackup_4_lines.webp)

Three rules hold for every line:

- **A line left out changes no other part.** KESE works every line out first and then leaves out
  the ones set to `False`, so what stays is exactly as it is with every line `True`. With the top
  solder mask left out, the top finish still ends where the mask would begin; with `top_copper`
  left out, a net's copper is the same solid less its `F.Cu` layer, and the laminate under it is
  not changed. `tests/test_stackup_lines.py` holds every line to this, in both stack-ups and both
  modes.
- **The lines of the inside stand for every inner layer.** How many copper layers a board has, and
  the plies between them, come from the board file; `inner_copper` is `In1.Cu`, `In2.Cu` and every
  other, and `board` (or `prepreg_plies` and `cores`) every gap.
- **Something must be built.** A stack-up with every line `False`, a line missing or a line
  misspelt stops the run before the board is read, with the closest name offered
  ([Checks, Errors And Warnings](Checks-Errors-And-Warnings.md#2011-errors)). A
  board that has no part on any line that is `True` (only `top_silkscreen` on a board with no
  silkscreen) is written empty, with a warning.

On the command line `--set Stackup.top_solder_mask=True` sets that line in both stack-ups, and four
short names set several lines at once: `Stackup.silkscreen`, `Stackup.solder_mask`,
`Stackup.finish` (the top, the bottom and the hole finish) and `Stackup.copper` (the three copper
lines and the plated holes).

## 8.5 How The Heights Feed The Model

| Feature | Height used |
|---|---|
| Dielectric $`d_i`$ | equations (8.8) and (8.9); with the plies separate each ply of it, equations (8.14) and (8.15) |
| Resin beside inner copper | the inner copper's own band: with the plies fused a part of the adjacent prepreg's solid, else of the dielectric above (box 2 of the picture at the top); with the plies separate a solid of its own ([Board](Board.md#122-resin-between-the-traces-of-the-inner-copper)) |
| Copper of layer $`l_k`$ | its band, equations (8.4) to (8.7) |
| Via barrel from layer $`l_i`$ to $`l_j`$ | between the copper layers it joins; outer copper caps it, inner copper is drilled through, so the barrel passes through inner bands ([Copper And Traces](Copper-And-Traces.md)) |
| Solder mask | from the laminate face: mask thickness over laminate, copper + mask thickness over copper ([Solder Masks](Solder-Masks.md)) |
| Silkscreen | on top of the mask surface ([Silkscreens](Silkscreens.md)) |
| Surface finish | on every copper face the air reaches: stacked on the outer copper where the mask is open, and a thin shell on the copper's walls, in the plated holes and on the plated edge (boxes 4 and 5 of the picture at the top; [Finish](Finish.md)) |

| Previous | Next |
|:---|---:|
| [Working Principle](Working-Principle.md) | [Output Modes](Output-Modes.md) |
