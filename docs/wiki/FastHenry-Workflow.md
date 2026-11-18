# 54. FastHenry Workflow

What happens between `python simulation.py` and the numbers in the results file, step by step. Every step is one
function of the bridge on the `FastHenry_Integration` branch; the file is named with each. The bridge is general:
nothing in it names a board, a coil or an example. Each example adds only what belongs to its own board: which nets
are coils, where each coil is opened, what to sweep, and what to compare the answer with.

## 54.1 Export The Stack-Up With KESE

`bridge/stackup.py` runs KESE as a program, never as a library:

```bash
python run_KESE.py board.kicad_pcb --for elmer --format step stl --out <folder> \
    --set Stackup.solder_mask=True --set SolderMask.MASK_OVER_COPPER_MM=0.020 ...
```

The `elmer` preset is KESE's solver preset: one STL per solid and a `materials.json`
([Choosing An Export](Choosing-An-Export.md)). The solder mask is set to 20 µm over copper and laminate, with vias
tented, so the export is the same for any solver; to FastHenry it is air. From `materials.json` the bridge takes the
height and thickness of every copper layer: each dielectric says which two layers it lies between, and each copper
part gives its layer's thickness (`copper_layers`). The export is kept beside the board (the coil board keeps it in
`3D_Geometry/`) with a `source.json` holding the board file's hash, so an unchanged board is not exported twice
(`kese_geometry`).

What FastHenry takes from KESE is the stack-up only. The model's coordinates: x and y as KiCad's with y up
(y_model = −y_KiCad), and z shifted so that the top face of the top copper is z = 0.

## 54.2 Read The Copper From The Board File

`bridge/kicad.py` (`read`) reads the `.kicad_pcb` itself (KiCad 6 to 9): every track and arc, every via, and every
copper polygon (`gr_poly` on a copper layer, and zones' filled polygons), with its net and layer. A KiCad track is a
centre line with a width, which is exactly a FastHenry segment, so the board file is where the conductors come from.

## 54.3 Build The Filament Model

`bridge/fasthenry_case.py` (`add_board`, `add_polygon`) turns the copper into FastHenry's nodes and segments:

| Copper | In the model |
|---|---|
| A track | a segment between nodes at its ends, at the middle of its layer's copper, as wide as the track and as thick as the copper, split into `nwinc` filaments across its width (the edge ones `rw` times narrower than the next in, so the current can crowd to the edges) and `nhinc` through its thickness |
| An arc | chords of at most 5° and 0.5 mm, each a segment as above |
| Tracks of one net that meet | one shared node |
| Two consecutive pieces of a trace straight to within 0.01° | one segment (`merge_collinear`), for the reason in [FastHenry Troubleshooting](FastHenry-Troubleshooting.md#601-nan-in-the-impedance-matrix) |
| A via | a vertical bar between its nodes on the layers it joins, a square with the copper section of a barrel plated 25 µm; its pads are left out |
| A copper polygon (the rotor) | a grid of bars at its layer's height, each as wide as the cell it stands for: a polar grid graded towards all four edges where the polygon is a sector of a ring, so its arcs are not stair steps; a square grid clipped to it otherwise |

A board can be turned copper side down, raised by an air gap and turned about an axis: that is how a rotor is placed
over a stator. Only the stator's filaments stay where they are, and only the rotor's grid turns from angle to angle,
so there is no meshing noise between angles.

![How S0d2_1x_OD23_2L_tiny_TX3top_Cut is set up in FastHenry. Left, seen from above: the TX's three turns on F.Cu in dark grey round SIN in blue and COS in orange (F.Cu strong, B.Cu pale), and the rotor at 0° in grey, its two quarter-ring sectors drawn as a grid of bars finer at their edges; the SIN and COS ports are ringed where a 0.2 mm cut crosses each top trace, the TX port where its two ends lie stacked at the right. Top right, a section through the stack true to scale: the stator's tracks at z = 0 and −0.76 mm, the rotor's bars 1 mm above, and a TX track magnified, 3 filaments across with the edge ones twice as narrow, 1 through its 35 µm. Bottom right, in 3D: SIN's port between the two cut faces of its top trace, and the TX's port between its two stacked ends on F.Cu and B.Cu](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/FastHenry-Workflow/S0d2_1x_OD23_2L_tiny_TX3top_Cut/S0d2_1x_OD23_2L_tiny_TX3top_Cut_fasthenry_setup.webp)

The coil board as FastHenry solves it, drawn by its `rig_picture.py` from the model's own segments. FR-4 and solder
mask are air to this solve, so the section shows nothing round the copper: nothing bounds the air. The counts in the
picture's title (9,306 filaments, 1,602 track segments) are from before straight pieces of a trace were merged; the
solves have 9,264 filaments and 1,588 stator segments.

## 54.4 Open Each Coil At Its Port

A FastHenry port (`.external`) is a pair of nodes. The bridge opens each coil where the real board gets its leads;
the example says where, since the bridge does not guess:

| Coil opened at | Port | Function |
|---|---|---|
| Two trace ends stacked on two layers (the TX) | between those two nodes | `nearest_node`, `via_nodes` |
| A via left out | between where the coil's tracks reach the via on its two layers; the via's bar is left out | `via_nodes`, `add_board(open_vias=...)` |
| A cut across a trace (SIN and COS on the coil board) | the copper inside the cut is taken out of the trace, and the port is between the two cut faces | `cut_nodes`, `add_board(cuts=...)` |
| A gap between two trace ends on one layer (E01, E02) | between the nodes at the two trace ends | `nearest_node` |

FastHenry gives back the open-circuit impedance matrix between the ports: Z[i][j] is the voltage at port i over the
current into port j, with every other port open. So with 1 A into the TX, a receiver's voltage is its open-circuit
EMF, and its mutual inductance is M = Im(Z[receiver][TX]) / 2πf.

## 54.5 Write FastHenry's Input

`Model.text` writes one `model.inp` per solve, kept under the example's `case/` (which git ignores):

| Item | Value |
|---|---|
| Units | millimetres |
| Copper | σ = 5.8e7 S/m |
| Coordinates | x and y measured from the model's middle (rounded to the whole millimetre), to 12 significant digits, for the reason in [FastHenry Troubleshooting](FastHenry-Troubleshooting.md#601-nan-in-the-impedance-matrix) |
| Content | the nodes, the segments with their width, height and filaments, the `.external` ports, and one frequency |

## 54.6 Solve And Read Back

`run` starts FastHenry in the case's folder with the dense direct solve:

```bash
fasthenry model.inp -s ludecomp -m direct -a off
```

| Option | What it does |
|---|---|
| `-s ludecomp` | the LU factorisation of the whole system |
| `-m direct` | builds the dense matrix of every filament's coupling to every other |
| `-a off` | the multipole refinement off: it splits filaments that come close, which the direct solve does not need |

This gives the exact answer of the filament model, with no iteration to converge, so the impedance matrix comes out
symmetric to the last digit. `run` measures FastHenry's peak memory and time and reads `Zc.mat`; `coil_rows` gives
per coil:

| Result | From |
|---|---|
| Z, R = Re Z, L = Im Z / ω of the driven coil | its diagonal entry |
| Zm, M = Im(Zm) / ω of each other coil | Z[coil][driven] |
| The reverse M | Z[driven][coil]: the reciprocity check |
| Each other coil's own L | its diagonal entry |

The examples write all of it, with the settings, the versions, the model's size and the time and memory of every
solve, to their results files; on the coil board each air gap gets its own folder in `Results/`, with
`results_gap<gap>mm.json`, a `.csv` and the chart, and `SINCOS_Results.md` gathers every gap on one page.

## 54.7 SIN, COS And The Angle Error

On the coil board, `simulation.py` solves the rotor away once, then each angle of `test_spec.json`.
`angle_error.py` then gives each channel its best sine over the rotor's period, M = offset + amplitude ×
sin(θ + phase), takes each channel's offset out and divides it by its amplitude, so both swing between −1 and +1, as
a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS). The error at each angle
is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is;
the rms and the worst of them are the angle error, in electrical degrees.

| Previous | Next |
|:---|---:|
| [FastHenry Installation](FastHenry-Installation.md) | [FastHenry Simulating Your Own Board](FastHenry-Simulating-Your-Own-Board.md) |
