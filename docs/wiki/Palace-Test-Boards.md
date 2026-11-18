# 65. Palace Test Boards

The boards the Palace bridge is proved on. E01 and E02 are KESE's own renders of the proof boards, from the top and
from the bottom; the coil board is drawn by the Sinusoidal Coil Generator's own picture tool, the stator beside the
rotor. Every board is a folder under `Examples/` on the `Palace_Integration` branch, with its KiCad files, its
`simulation.py` and KESE's export in `3D_Geometry/`.

## 65.1 E01 Circular Loop

| Top | Bottom |
|:---:|:---:|
| <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Palace-Test-Boards/E01_circular_loop/E01_circular_loop_top.webp" width="380" alt="E01 from the top: a 30 mm square board with one copper loop on F.Cu, 10 mm in radius and 0.5 mm wide, opened on the right by a 0.2 mm gap between its two round ends"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Palace-Test-Boards/E01_circular_loop/E01_circular_loop_bottom.webp" width="380" alt="E01 from the bottom: the same loop seen through the bare back of the board, mirrored, so its gap is on the left"> |

| Item | Value |
|---|---|
| Board | 30 mm × 30 mm, 1.6 mm thick, written by `make_board.py` |
| Copper | one trace on F.Cu, net `LOOP`: a circle of 10 mm radius to its centre line, 0.5 mm wide, 35 µm thick, opened by a 0.2 mm gap between its round ends |
| Port | a lumped port of 50 Ω across the gap, through the copper's thickness, from one round end's tip to the other's, direction +Y |
| What Palace checks | the loop's L and R at 10 kHz (uniform current) and 3.5 MHz (the coil board's frequency), on a mesh ladder of four levels and once with the coil board's air grading, and L from the field's energy |
| References | Neumann's double integral over the open arc with the trace's geometric mean distance: 55.590 nH for the arc between the round ends' centres (356.0°), 56.293 nH out to the gap's faces (358.9°); Grover's ring formula for the closed ring, 56.622 nH. Palace's port sheet carries the current across the gap and so closes the loop, so once the mesh is fine enough its L should lie above the open arcs and near the closed ring. Percentages are against the arc between the centres, the reference every solver's branch shares. R against the annular sector's DC resistance, 61.201 mΩ |
| Status | **run**: [Palace Test Board Results](Palace-Test-Board-Results.md#661-e01-circular-loop) |

## 65.2 E02 Coaxial Loops

| Top | Bottom |
|:---:|:---:|
| <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Palace-Test-Boards/E02_coaxial_loops/E02_coaxial_loops_top.webp" width="380" alt="E02 from the top: E01's loop on F.Cu, the TX, its gap on the right"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Palace-Test-Boards/E02_coaxial_loops/E02_coaxial_loops_bottom.webp" width="380" alt="E02 from the bottom: the RX, the same loop on B.Cu right under the TX, seen mirrored with its gap on the left"> |

| Item | Value |
|---|---|
| Board | 30 mm × 30 mm, 1.6 mm thick, written by `make_board.py` |
| Copper | E01's loop twice: `TX` on F.Cu and `RX` on B.Cu, one above the other, their gaps one above the other, the traces' centres 1.565 mm apart in z |
| Ports | one lumped port of 50 Ω across each gap; both are driven in turn, so Palace gives the whole 2 × 2 impedance matrix |
| What Palace checks | M from the TX to the RX, M back from the RX to the TX (reciprocity), and the TX's L beside the open RX against E01's loop, at 10 kHz and 3.5 MHz on a mesh ladder of four levels, and once with the coil board's air grading |
| References | Neumann's double integral averaged over filaments across both traces' widths: the two open arcs (356° each, between the round ends' centres), 23.886 nH, and the closed rings (Maxwell's formula), 24.400 nH. The port sheets close both loops, so once the mesh is fine enough M should lie above the open arcs and near the closed rings. Percentages are against the open arcs |
| Status | **run**: [Palace Test Board Results](Palace-Test-Board-Results.md#662-e02-coaxial-loops) |

## 65.3 S0d2_1x_OD23_2L_tiny_TX3top_Cut

An inductive angle encoder from the
[Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator)
(`Coil_2_11.7_2_1_3_Single_SteppedDiagonal`), in `Examples/Inductive Coils/S0d2_1x_OD23_2L_tiny_TX3top_Cut/` (non-commercial licence, see
that folder's `LICENSE.md`). A stator carries one TX coil and two RX coils, SIN and COS; a rotor with copper sectors
sits over it, its eddy currents change how much of the TX's field reaches each RX coil, and the two RX voltages follow
the sine and cosine of the rotor's angle.

![S0d2_1x_OD23_2L_tiny_TX3top_Cut drawn by the coil generator: left, the stator, 23.4 mm across with a 4 mm bore, the TX's three turns in red on Top round the outside with its lead to the right, and SIN and COS, two sine periods per turn each, in red on Top and blue on Bottom with their vias as dots; right, the rotor, with two copper quarter-ring sectors opposite each other](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Palace-Test-Boards/S0d2_1x_OD23_2L_tiny_TX3top_Cut/S0d2_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp)

| Item | Value |
|---|---|
| Stator | bore and outer radius 2 and 11.7 mm (23.4 mm across), 2 copper layers, 35 µm copper, board 0.8 mm |
| TX | three turns, all on F.Cu (r = 7.2, 7.8 and 8.4 mm), with a short tail on B.Cu back to the terminal, where its two ends sit stacked at KiCad (111, 100) |
| SIN and COS | nets `2` and `1`, band r = 3.2 to 6.1 mm, two sine periods per turn, on F.Cu and B.Cu |
| Rotor | two quarter-ring copper sectors (r = 2.52 to 9.0 mm), copper side down, not mirrored, its copper face `air_gap` above the stator's top copper; the curves repeat every 180° |
| Frequency | 3.5 MHz |
| How each coil is opened | the TX between its two stacked ends (50 Ω and the drive); SIN and COS by a 0.2 mm cut across a top trace, 0.86 mm from a layer-change via that stays (1 MΩ each). The cut is made in the model; the board files are as the generator wrote them |
| What Palace checks | SIN and COS against the rotor's angle (16 angles over the turn) at 0.1, 0.5, 1, 1.5 and 2 mm air gaps, the TX's L and R, the rotor taken away once, the angle error |
| The generator's estimate | TX 0.29 µH with the rotor away and 0.23 µH with it, 0.38 Ω DC |
| Status | **run**: [Palace Test Board Results](Palace-Test-Board-Results.md#663-s0d2_1x_od23_2l_tiny_tx3top_cut) |

![Where SIN and COS of S0d2_1x_OD23_2L_tiny_TX3top_Cut are opened. Left, the whole stator with the SIN cut and the COS cut ringed and the TX port at the right. Top right, close-ups: SIN cut at KiCad (96.59, 100.50) and COS cut at (97.24, 97.94), each a 0.2 mm white box across the top trace, 0.86 mm from the via that stays and 0.46 mm clear of other copper. Bottom, the TX's stacked ends at (111.00, 100.00), not cut](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Palace-Test-Boards/S0d2_1x_OD23_2L_tiny_TX3top_Cut/S0d2_1x_OD23_2L_tiny_TX3top_Cut_cuts.webp)

The two cuts are 45° apart about the axis, a quarter of the electrical period, as SIN and COS are.

The branch solves five more coil boards in the same way; they are in
[`Examples/Inductive Coils/`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/tree/Palace_Integration/Examples/Inductive%20Coils).

| Previous | Next |
|:---|---:|
| [Palace Simulating Your Own Board](Palace-Simulating-Your-Own-Board.md) | [Palace Test Board Results](Palace-Test-Board-Results.md) |
