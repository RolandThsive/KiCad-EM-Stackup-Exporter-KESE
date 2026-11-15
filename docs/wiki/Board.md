# 12. Board

The board is the laminate: the dielectric layers between and around the copper, with the
outline, the cut-outs and the holes. `kese/s4_geometry/laminate.py` builds it from the resolved
outline and stack-up. Its settings are in `parameters/PCB_elements/Board.py`; whether it is
built, and whether the plies of a gap are fused or separate, is in
`parameters/PCB_elements/Stackup.py`
([Stack-Up Model](Stack-Up-Model.md#84-what-is-built-the-lines-of-stackuppy)).

## 12.1 Dielectric Solids

Each gap between two consecutive copper layers is one dielectric of the
[Stack-Up Model](Stack-Up-Model.md): a core or a prepreg with its own thickness, material, εr
and tan δ. A gap can be pressed from several plies: KiCad's Board Setup gives a dielectric
sub-layers, and each sub-layer is a **ply** with its own thickness and values. `Stackup.FUSION_BUILD`
says what the laminate becomes:

| `Stackup.FUSION_BUILD` | The laminate becomes | Names |
|---|---|---|
| `"PLIES_FUSED"` | one solid for each gap between two copper layers | `Board_dielectric 1`, `Board_dielectric 2`, ... from the `F.Cu` side |
| `"PLIES_SEPARATE"` (the default) | one solid for each prepreg ply, one for each core, and one for the resin beside each inner copper layer | `Board_dielectric 1 ply 1`, `Board_dielectric 2`, `Board_resin In1.Cu` |

![Board 29_stackup_plies cut at true scale through its buried via, built three ways, each with the list of its laminate solids: plies fused gives five solids, one for each gap, the prepreg ones holding the resin beside the inner copper; plies separate gives thirteen, one for each ply and core and one for the resin beside each inner copper layer; plies separate with JOIN_EQUAL_PLIES gives eleven, the three 7628 plies of dielectric 3 joined into one](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Board/board_4_plies.webp)

Each solid is the outline minus every hole that passes through its gap: a via from copper
layer $`l_a`$ to $`l_b`$ drills the dielectrics between them, and a through via or a
through-hole pad drills them all. All the plies of one gap have the same region.

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

The solid of a gap is extruded over the z range of equations (8.8) and (8.9) in
[Stack-Up Model](Stack-Up-Model.md); a ply over its own part of that range, section 12.1.2.

### 12.1.1 Plies Fused

With the plies fused, a gap is one solid however many plies it has. Plies written as sub-layers
of one stack-up dielectric keep that dielectric's name, and separate stack-up dielectrics between
the same two copper layers give one solid named like `Board_dielectric 2 + dielectric 3`. This is
what KESE built before 25.2, and it is what most solvers want: one dielectric block between two
copper layers.

`Board.FUSED_PROPERTIES` says which values the one solid has when its plies differ:

| `Board.FUSED_PROPERTIES` | Material, εr and tan δ of the solid |
|---|---|
| `"first"` (the default) | those of the gap's first ply, counted from the top |
| `"series"` | the plies in series, as a field straight across the gap sees them ([Material Properties](Material-Properties.md#215-a-gap-whose-plies-differ)); the material is written as `1080 + 2116` |

In `materials.json` every such solid has `kind` (core / prepreg), `material`, `thickness_mm`,
`epsilon_r`, `loss_tangent`, `fused_properties`, `spec_frequency_hz` and `dielectric_model`
([Material Properties](Material-Properties.md#214-how-εr-and-tan-δ-change-with-frequency)),
`between` (the two copper layers it separates) and `plies`: the plies it was fused from, top to
bottom, each with its own name, kind, material, thickness and values. Nothing the board file says
about a ply is lost by fusing. `report.txt` prints the same, a row `fused from` for each ply:

```text
  dielectric 1             prepreg  1080       0.2000 mm  er 3.9  tan d 0.018   z +0.4853 .. +0.6853
    fused from dielectric 1 ply 1: prepreg 1080 0.0800 mm  er 3.9  tan d 0.018
    fused from dielectric 1 ply 2: prepreg 2116 0.1200 mm  er 4.2  tan d 0.016
```

### 12.1.2 Plies Separate

With `Stackup.FUSION_BUILD = "PLIES_SEPARATE"` every ply is a solid of its own, named after it:
`Board_dielectric 1 ply 1`, `Board_dielectric 1 ply 2`; a gap of one ply keeps the dielectric's
name, `Board_dielectric 2`. The plies of a gap are stacked down from the gap's top face, each
with its own thickness, and the last one ends at the gap's bottom face: equations (8.14) and
(8.15) of [Stack-Up Model](Stack-Up-Model.md#832-plies-separate). When `Board.BOARD_THICKNESS_MM`
forces the laminate to a thickness, the plies are scaled with their gaps.

Two neighbouring solids of the laminate share their face exactly, so the Verifier's checks hold
as they do for the fused build. In `materials.json` a ply has `kind`, `material`, `thickness_mm`,
`epsilon_r`, `loss_tangent`, `spec_frequency_hz`, `dielectric_model`, `between`, `ply` (its place
in the gap, from the top, counted from 1) and `plies_in_gap`. The resin beside each inner copper
layer is a solid too, section 12.2. `Stackup.py` has a line for each kind, so a run can build the
prepreg plies without the cores, or the laminate without the resin
([Stack-Up Model](Stack-Up-Model.md#84-what-is-built-the-lines-of-stackuppy)):

```bash
python run_KESE.py board.kicad_pcb                                # the plies separate: the default
python run_KESE.py board.kicad_pcb --set Stackup.cores=False      # the prepreg plies and the resin, without the cores
python run_KESE.py board.kicad_pcb --set Stackup.FUSION_BUILD=PLIES_FUSED   # one solid for each gap
```

### 12.1.3 Equal Plies And Thin Plies

Two rules change which plies become solids with the plies separate. Neither changes a height:
the gap keeps its thickness.

| Rule | Setting | What happens |
|---|---|---|
| Equal neighbours | `Board.JOIN_EQUAL_PLIES = True` (default `False`) | Neighbouring plies of one gap with the same kind, material, εr, tan δ, spec frequency and model become one solid. A gap pressed from three plies of 7628 is one solid `Board_dielectric 3` again; plies of 1080 and 2116 stay two solids. |
| Thin plies | `Board.PLY_MIN_THICKNESS_MM` (default `0.001`) | A ply thinner than this is joined to its thicker neighbour in the gap, the thinnest first, and `report.txt` warns: `dielectric 4 ply 2 is 0.0005 mm thick, less than Board.PLY_MIN_THICKNESS_MM (0.001 mm): joined to dielectric 4 ply 1`. A solid half a micrometre high cannot be meshed. |

A joined solid has the summed thickness and the values of the ply the others were joined to (the
first of equal plies, the thicker neighbour of a thin one). Its name is the ply's own, the
dielectric's when it holds all of the dielectric's plies, or first to last, as
`Board_dielectric 1 ply 2-3`. `materials.json` lists the file's plies it holds under
`joined_plies`, and its row in `report.txt` ends with them:
`(holds dielectric 4 ply 1, dielectric 4 ply 2)`. A ply the file gives no thickness is joined
to its neighbour whatever `Board.PLY_MIN_THICKNESS_MM` is, with the warning
`dielectric 4 ply 2 has no thickness: joined to dielectric 4 ply 1`.

### 12.1.4 Plies Written By Hand

KiCad 7 to 10 write a ply's thickness, material, εr and tan δ. When the fabricator's stack-up
has plies the board file does not, `Board.PLIES_BY_HAND` gives a gap its plies without editing
the board:

```python
PLIES_BY_HAND = {
    "05_vias_micro": {
        ("F.Cu", "In1.Cu"): [
            {"type": "prepreg", "thickness_mm": 0.100, "material": "1080", "epsilon_r": 3.8, "loss_tangent": 0.015},
            {"type": "prepreg", "thickness_mm": 0.120, "material": "2116", "epsilon_r": 4.1, "loss_tangent": 0.017},
        ],
        ("In1.Cu", "In2.Cu"): [
            {"type": "core",    "thickness_mm": 0.200, "material": "FR4 core", "epsilon_r": 4.6, "loss_tangent": 0.018},
        ],
        ("In2.Cu", "In3.Cu"): [
            {"type": "prepreg", "thickness_mm": 0.100, "material": "1080", "epsilon_r": 3.8, "loss_tangent": 0.015},
            {"type": "prepreg", "thickness_mm": 0.120, "material": "2116", "epsilon_r": 4.1, "loss_tangent": 0.017},
        ],
        ("In3.Cu", "In4.Cu"): [
            {"type": "core",    "thickness_mm": 0.200, "material": "FR4 core", "epsilon_r": 4.6, "loss_tangent": 0.018},
        ],
        ("In4.Cu", "In5.Cu"): [
            {"type": "prepreg", "thickness_mm": 0.120, "material": "2116", "epsilon_r": 4.1, "loss_tangent": 0.017},
            {"type": "prepreg", "thickness_mm": 0.100, "material": "1080", "epsilon_r": 3.8, "loss_tangent": 0.015},
        ],
        ("In5.Cu", "In6.Cu"): [
            {"type": "core",    "thickness_mm": 0.200, "material": "FR4 core", "epsilon_r": 4.6, "loss_tangent": 0.018},
        ],
        ("In6.Cu", "B.Cu"): [
            {"type": "prepreg", "thickness_mm": 0.120, "material": "2116", "epsilon_r": 4.1, "loss_tangent": 0.017},
            {"type": "prepreg", "thickness_mm": 0.100, "material": "1080", "epsilon_r": 3.8, "loss_tangent": 0.015},
        ],
    },
}
```

This example writes a whole eight-layer board: its seven gaps, from the top copper down to the
bottom, prepreg and core in turn. `Board.py` holds it as a comment; with the `#` in front of its
lines removed, board `05_vias_micro` is built with these eleven plies.

The first key is the board file's name without `.kicad_pcb`, so other boards are not touched.
Under it, each gap to change is named by its two copper layers, the upper one first, and gets
its plies top to bottom. A gap that is not listed still comes from the file. A ply takes `type`
(`"core"` or `"prepreg"`), `thickness_mm`, `material`, `epsilon_r` and `loss_tangent`, and may
take `frequency_hz` and `model` (left out: `Board.DEFAULT_SPEC_FREQUENCY_HZ` and
`Board.DIELECTRIC_MODEL`). On a board whose file has no usable stack-up, the gaps written by
hand keep their plies and the rest of the laminate is split evenly between the other gaps.

KESE checks the list before it builds anything. The two copper layers must be neighbours on that
board, every thickness must be more than 0, εr 1 or more and tan δ 0 or more, and a ply may have
no other keys. A mistake stops the run with a message that names the entry, as
`Board.PLIES_BY_HAND['05_vias_micro'][('F.Cu', 'In2.Cu')]: ('F.Cu', 'In2.Cu') is not two
neighbouring copper layers of this board, the upper one first; its gaps are ...`.

### 12.1.5 The Whole Laminate As One Solid

With `Board.DIELECTRIC_GROUPING = "merged"` the laminate is one solid named `Board`, whichever
stack-up is built. In `materials.json` it has only the values of its first solid from the top:
the first gap's with the plies fused, the first ply's with the plies separate. Use it for a
viewer or a mechanical model; a field solver needs the solids apart.

## 12.2 Resin Between The Traces Of The Inner Copper

In a pressed laminate the resin of the prepreg flows into the spaces between the inner-layer
traces, so there is no air inside the board. KESE builds this resin when the line
`resin_between_traces` of `Stackup.py` is `True` (the default): for every inner copper layer,
the area of the outline that carries **no** copper on that layer, minus the holes through that
layer, is filled over the copper's own z band:

```math
F_k = \left( O \setminus \bigcup_{h : a_h \le k \le b_h} H_h \right) \setminus C_k, \qquad z \in \left[ z_{\mathrm{bot}}(l_k),\ z_{\mathrm{top}}(l_k) \right] \qquad (12.2)
```

| Symbol | Meaning |
|---|---|
| $`F_k`$ | resin region beside inner copper layer $`l_k`$ |
| $`C_k`$ | all copper of layer $`l_k`$, every net |
| $`z_{\mathrm{bot}}(l_k)`$, $`z_{\mathrm{top}}(l_k)`$ | the copper band of $`l_k`$, equations (8.6) and (8.7) |

With edge plating on, the edge band is also removed from $`F_k`$. The resin comes from a prepreg,
as in the press:

- from the prepreg **below** the copper layer when the layer above is a core and the one below a
  prepreg;
- otherwise from the dielectric **above** it.

![Board 11_zones cut at true scale across the track that splits its inner zones, with the plies fused and with the plies separate: fused, the resin beside In1.Cu is a part of the solid of the prepreg above it and the resin beside In2.Cu of the prepreg below it; separate, each is a solid of its own, Board_resin In1.Cu and Board_resin In2.Cu; and the bands of In1.Cu and In2.Cu from above, copper and resin](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Board/board_2_resin_fill.webp)

So both common 4-layer builds, prepreg-core-prepreg (as in the picture) and core-prepreg-core,
get their inner pockets filled from a prepreg. The shape of the resin is the same in both
stack-ups; what changes is the solid it belongs to and the values it has:

| | Plies fused | Plies separate |
|---|---|---|
| Solid | a part of the solid of the dielectric it came from, `Board_dielectric 1` | a solid of its own for each inner copper layer, `Board_resin In1.Cu` |
| Values | that dielectric's | `Board.RESIN_MATERIAL`, `Board.RESIN_EPSILON_R` and `Board.RESIN_LOSS_TANGENT`: the prepreg's resin without its glass. `None` for εr or tan δ takes that value from the ply the resin flowed from |
| In `materials.json` | not listed apart: a part's properties are those of the dielectric | `kind: "resin"`, `material`, `thickness_mm`, `epsilon_r`, `loss_tangent`, `resin_fill_beside` (the copper layer) and `flowed_from` (the ply) |
| Color | the dielectric's | `Board.RESIN_COLOR` |

With the plies separate, the ply the resin flowed from is the one that touches the copper layer:
the last ply of the gap above, or the first ply of the gap below. The default εr 3.5 and tan δ
0.02 are a best guess for FR-4 epoxy without glass
([Material Properties](Material-Properties.md#213-the-default-numbers)); a resin-rich region has
a lower εr than the glass-and-resin ply beside it, which is why a solver that resolves the inner
traces may want it apart.

With the line `resin_between_traces` set to `False`, the pockets stay empty and `report.txt` notes
`inner copper pockets left empty ("resin_between_traces" is False)`. With the plies fused the
resin also needs the line `board`: a part of a solid cannot be built without the solid. With
`Board.DIELECTRIC_GROUPING = "merged"` the resin goes into the single `Board` part.

> [!NOTE]
> Where inner copper exists, dielectric *k* and dielectric *k* + 1 are separated by the copper
> band; the resin is what joins the laminate through the copper-free area of that band.
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

All in `parameters/PCB_elements/Board.py`, in the file's five sections. Whether the laminate is
built is not here: it is the lines `board`, `prepreg_plies`, `cores` and `resin_between_traces`
of `Stackup.py`. The names of before 25.2 (`BOARD_ENABLED`, `RESIN_FILL_BETWEEN_INNER_COPPER`)
still work with `--set`; see
[Parameter Reference](Parameter-Reference.md#1914-names-of-before-252).

| Name | Default | Range | Meaning |
|---|---|---|---|
| **1 Parts** | | | |
| `JOIN_EQUAL_PLIES` | `False` | bool | Plies separate: neighbouring plies of one gap with the same material and values become one solid (section 12.1.3) |
| `DIELECTRIC_GROUPING` | `"layer"` | `"layer"` / `"merged"` | `"layer"`: the solids of the stack-up being built; `"merged"`: the whole laminate as one solid `Board` (section 12.1.5) |
| **2 Thickness** | | | |
| `BOARD_THICKNESS_MM` | `None` | None or mm > 0 | Laminate thickness; `None` takes it from the file |
| `DEFAULT_BOARD_THICKNESS_MM` | `1.6` | mm > 0 | Finished board thickness when the file gives none (KiCad's default) |
| `DIELECTRIC_SPLIT` | `"even"` | `"even"` | How the laminate is divided when the file has no usable stack-up |
| `PLY_MIN_THICKNESS_MM` | `0.001` | mm ≥ 0 | Plies separate: a ply thinner than this is joined to its thicker neighbour, with a warning (section 12.1.3) |
| `PLIES_BY_HAND` | `{}` | see 12.1.4 | The plies of the gaps listed, for the boards listed, in place of the file's |
| **3 Shape** | | | |
| `OUTLINE_LINE_SNAP_MM` | `0.01` | mm > 0 | Open `Edge.Cuts` line and arc ends closer than this are joined, as KiCad joins them (its chaining distance is 0.01 mm) |
| `OUTLINE_FALLBACK` | `"copper_hull"` | `"copper_hull"` / `"error"` | What to do when `Edge.Cuts` gives no closed ring at all |
| `OUTLINE_FALLBACK_MARGIN_MM` | `1.0` | mm ≥ 0 | Margin around the copper hull in the fallback |
| `OUTLINE_DUPLICATE_AREA_MM2` | `1e-6` | mm² > 0 | Two closed `Edge.Cuts` outlines that differ by less than this area are one (a ring drawn twice; section 12.3) |
| `OUTLINE_MIN_AREA_MM2` | `1e-9` | mm² ≥ 0 | A closed `Edge.Cuts` outline of this area or less is left out (a line drawn there and back, a circle of no size) |
| `INCLUDE_NON_PLATED_HOLES` | `True` | bool | NPTH pads become holes through the board |
| `BACKDRILLS` | `True` | bool | Drill out KiCad 10's backdrills and tertiary drills ([Copper And Traces](Copper-And-Traces.md#1333-backdrills)) |
| `POST_MACHINING` | `True` | bool | Cut KiCad 10's counterbores and countersinks (section 12.4.1) |
| `COUNTERSINK_STEP_TOLERANCE_MM` | `0.025` | mm > 0 | How far a countersink's steps may stray from its cone, equation (12.6) |
| **4 Material** | | | |
| `DEFAULT_DIELECTRIC_MATERIAL`, `DEFAULT_DIELECTRIC_TYPE` | `"FR4"`, `"core"` | text; `"core"` / `"prepreg"` | Material and type when the stack-up gives none |
| `DEFAULT_EPSILON_R`, `DEFAULT_LOSS_TANGENT` | `4.5`, `0.02` | ≥ 1; ≥ 0 | Typical FR4 at 1 GHz, used when the stack-up gives none |
| `DEFAULT_SPEC_FREQUENCY_HZ` | `1e9` | Hz > 0 | The frequency εr and tan δ are given at, when the stack-up gives none |
| `USE_STACKUP_EPSILON_R`, `USE_STACKUP_LOSS_TANGENT`, `USE_STACKUP_SPEC_FREQUENCY` | `True` | bool | Stack-up values win over the defaults when present |
| `DIELECTRIC_MODEL` | `"djordjevic_sarkar"` | `"constant"` / `"djordjevic_sarkar"` / `"table"` | How εr and tan δ change with frequency ([Material Properties](Material-Properties.md#214-how-εr-and-tan-δ-change-with-frequency)) |
| `USE_STACKUP_DIELECTRIC_MODEL` | `True` | bool | The file's `(dielectric_model ...)` wins when present |
| `DS_LOW_FREQUENCY_HZ`, `DS_HIGH_FREQUENCY_HZ` | `1e3`, `1e12` | Hz > 0, the low one below the high one | Corner frequencies of the Djordjevic-Sarkar model |
| `DIELECTRIC_TABLE` | `()` | rows of (Hz, εr, tan δ) | The table of `DIELECTRIC_MODEL = "table"` |
| `FUSED_PROPERTIES` | `"first"` | `"first"` / `"series"` | Plies fused: the values of a gap whose plies differ (section 12.1.1) |
| `RESIN_MATERIAL` | `"resin"` | text | Plies separate: the material name of the resin solids (section 12.2) |
| `RESIN_EPSILON_R`, `RESIN_LOSS_TANGENT` | `3.5`, `0.02` | None, or ≥ 1; None, or ≥ 0 | Plies separate: the resin's values; `None` takes the value of the ply it flowed from |
| **5 Color** | | | |
| `CORE_COLOR`, `PREPREG_COLOR`, `RESIN_COLOR`, `BOARD_COLOR` | see the file | color, alpha, metallic, roughness | The look of a core, a prepreg, the resin solids, and the merged laminate ([Colorizing](Colorizing.md)) |

| Previous | Next |
|:---|---:|
| [Project Output Organization](Project-Output-Organization.md) | [Copper And Traces](Copper-And-Traces.md) |
