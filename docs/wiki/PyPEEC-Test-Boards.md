# 47. PyPEEC Test Boards

The boards the PyPEEC bridge is proved on in this category: two proof boards whose answers are known
without any solver, and one inductive encoder board from the Sinusoidal Coil Generator. All three have
run, and each links to its results. Every board is a folder under `Examples/` on the
`PyPEEC_Integration` branch, with its KiCad files, its `simulation.py` and its `README.md`. The branch
solves five more coil boards in the same way, listed in
[`Examples/Inductive Coils/README.md`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/PyPEEC_Integration/Examples/Inductive%20Coils/README.md).

## 47.1 E01 Circular Loop

<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Test-Boards/E01_circular_loop/E01_circular_loop_top.webp" width="420" alt="E01 from the top, rendered by KESE: a 30 mm square board with one yellow copper loop, 10 mm in radius and 0.5 mm wide, opened on the right by a small gap between its two round ends">

*E01 from the top, rendered by KESE's static renderer from the board's own export. B.Cu is empty.*

| Item | Value |
|---|---|
| Board | 30 mm × 30 mm, two copper layers, 1.6 mm, no stack-up |
| Copper | one trace on F.Cu, net `LOOP`: a circle of 10 mm radius to its centre line, 0.5 mm wide, 35 µm thick, opened at +x by a 0.2 mm gap between its two round ends |
| Made by | `make_board.py`, with `Examples/kicad_writer.py` |
| Terminals | the loop's voxels that share a face with the gap, one group on each round end; PyPEEC drives 1 A into one and holds the other at 0 V |
| What PyPEEC checks | L and R at 10 kHz (uniform current) and 3.5 MHz (the coil board's frequency), the same L and R from the stored energy and the losses, and how they settle with the voxels: 100, 50, 25 and 12.5 µm in the plane |
| References | Grover's ring formula with the trace's geometric mean distance, times the share of the circle the copper covers: 55.99 to 56.44 nH; the annular sector's DC resistance, 61.20 mΩ |
| Status | **run**: [PyPEEC Test Board Results](PyPEEC-Test-Board-Results.md#481-e01-circular-loop) |

## 47.2 E02 Coaxial Loops

| Top | Bottom |
|:---:|:---:|
| <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Test-Boards/E02_coaxial_loops/E02_coaxial_loops_top.webp" width="320" alt="E02 from the top, rendered by KESE: the TX loop on F.Cu, opened on the right"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Test-Boards/E02_coaxial_loops/E02_coaxial_loops_bottom.webp" width="320" alt="E02 from the bottom, rendered by KESE: the RX loop on B.Cu right under the TX, its gap showing on the left as the board is seen from below"> |

*Rendered by KESE's static renderer. Seen from below, the bottom loop's gap shows on the left.*

| Item | Value |
|---|---|
| Board | 30 mm × 30 mm, two copper layers, 1.6 mm, no stack-up |
| Copper | E01's loop on F.Cu, net `TX`, and the same loop on B.Cu, net `RX`, directly under it, each opened at +x by a 0.2 mm gap |
| Loop to loop | 1.565 mm between the two coppers' middles (1.6 mm less one copper thickness) |
| Terminals | as E01's, on each loop. TX carries 1 A; RX a 0 A source, so the voltage across its gap is the EMF the TX induces in it |
| What PyPEEC checks | M at 10 kHz and 3.5 MHz, and the TX's L and R beside the open RX, at 100 and 50 µm voxels (25 µm would take a grid of 30 million voxels and about 9 GB) |
| References | Maxwell's formula for two coaxial circular filaments, averaged over 41 × 41 filaments across both traces' widths, times the share of the circle the TX's copper covers: 24.13 nH; and E01's own L and R at the same voxels |
| Status | **run**: [PyPEEC Test Board Results](PyPEEC-Test-Board-Results.md#482-e02-coaxial-loops) |

## 47.3 S0d2_1x_OD23_2L_tiny_TX3top_Cut

An inductive angle encoder from the
[Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator)
(`Coil_2_11.7_2_1_3_Single_SteppedDiagonal`), in `Examples/Inductive Coils/` (non-commercial licence,
see that folder's `LICENSE.md`). A stator carries one TX coil and two receivers, SIN and COS; a rotor
with copper sectors sits over it. The TX runs at 3.5 MHz, the rotor's eddy currents change how much of
its field reaches each receiver, and the two receivers' voltages follow the sine and cosine of the
rotor's angle.

![S0d2_1x_OD23_2L_tiny_TX3top_Cut drawn by the coil generator: the stator on the left, a round board 2 to 11.7 mm in radius, with three red TX turns on the top layer round the outside and the SIN and COS receivers inside them, red on Top and blue on Bottom with vias as dots, each making two sine periods per turn; the rotor on the right with two red quarter-ring copper sectors opposite each other](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Test-Boards/S0d2_1x_OD23_2L_tiny_TX3top_Cut/S0d2_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp)

*The stator and the rotor, drawn by the generator. Red is the top layer, blue the bottom; the dots are
vias.*

| Item | Value |
|---|---|
| Stator | 23.4 mm across (bore and outer radius 2 and 11.7 mm), 2 copper layers, board 0.8 mm, copper 35 µm |
| RX coils | SIN (net `2`) and COS (net `1`) in a band from r = 3.2 to 6.1 mm, each making two sine periods per turn |
| TX | three turns, all on F.Cu (r = 7.2, 7.8 and 8.4 mm), with a short tail on B.Cu that brings the spiral's inner end back out to the terminal, where the two ends sit stacked |
| Rotor | two quarter-ring copper sectors, r 2.52 to 9.0 mm, copper side down over the stator, not mirrored; it repeats itself every 180°, so an angle reading covers half a turn |
| Air gap | 1 mm by default, copper to copper; solved at 0.1, 0.5, 1, 1.5 and 2 mm |
| Sweep | 16 rotor angles over the whole turn, every 22.5° from 0 to 337.5° (two of the rotor's periods), and the rotor taken away once, at each gap |
| Frequency | 3.5 MHz, 1 A in the TX |
| Voxels | 50 µm in the plane, about 35 µm (one layer) through each copper sheet |
| The generator's estimate | TX 0.29 µH with the rotor away and 0.23 µH with it (its drop with the rotor is an upper estimate), 0.38 Ω DC |
| Status | **run**, 81 solves: [PyPEEC Test Board Results](PyPEEC-Test-Board-Results.md#483-s0d2_1x_od23_2l_tiny_tx3top_cut) |

### How Each Coil Is Opened

SIN and COS are opened by a 0.2 mm cut across a top trace, because that is how the real board is
opened and routed to the IC. The cut is made in the model; the board files are as the generator wrote
them, and the receivers' layer-change vias all stay in.

![Where SIN and COS are opened on S0d2_1x_OD23_2L_tiny_TX3top_Cut. Left: the whole stator, TX in grey, SIN in blue and COS in orange, with the SIN cut and the COS cut circled near the inner edge of the receivers and the TX port at its stacked ends on the right, unchanged. Right, zoomed: SIN's cut at KiCad (96.59, 100.50) and COS's at (97.24, 97.94), each a white 0.2 mm box across the top trace, 0.86 mm from the via that stays, 0.46 mm clear of other copper; and the TX's two ends, F.Cu over B.Cu, at (111.00, 100.00)](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Test-Boards/S0d2_1x_OD23_2L_tiny_TX3top_Cut/S0d2_1x_OD23_2L_tiny_TX3top_Cut_cuts.webp)

*Each cut is the spot on the receiver's top trace nearest its layer-change via where a 0.2 mm cut has
at least 0.45 mm of free board round it and sits at least 0.75 mm from any via centre: 0.86 mm from the
via on both receivers. The two spots are 45° apart about the axis, a quarter of the electrical period,
as SIN and COS are.*

| Coil | Net | Opened at (KiCad mm) | How |
|---|---|---|---|
| TX | `TX` | (111, 100), F.Cu and B.Cu | between its two stacked ends; 1 A driven |
| SIN | `2` | cut at (96.591, 100.496), F.Cu | a 0.2 mm gap across the top trace, running (−0.60, −0.80); the via at (97.044, 101.225) stays; 0 A |
| COS | `1` | cut at (97.239, 97.940), F.Cu | a 0.2 mm gap across the top trace, running (0.14, −0.99); the via at (97.044, 98.775) stays; 0 A |

The voltage across each cut is the receiver's open-circuit EMF, reported as the mutual inductance
M = V / (jωI) with 1 A in the TX: 1 nH is 22 mV of EMF at 3.5 MHz. How the board looks as voxels,
with its terminals, is on [PyPEEC Workflow](PyPEEC-Workflow.md#454-draw-the-copper-as-voxels).

The solder mask and FR-4 are in KESE's export, but to the magneto-quasi-static solve they are air
(μr 1), so only the copper is drawn.

| Previous | Next |
|:---|---:|
| [PyPEEC Simulating Your Own Board](PyPEEC-Simulating-Your-Own-Board.md) | [PyPEEC Test Board Results](PyPEEC-Test-Board-Results.md) |
