# 28. Elmer FEM Test Boards

The boards the Elmer bridge is proved on: two proof boards with textbook answers, and one whole
inductive encoder, a stator under a rotor. E01 and E02 are drawn from above and in section; the coil
board is drawn by the Sinusoidal Coil Generator's own picture tool, the stator beside the rotor.
Every board is a folder under `Examples/` on the `Elmer_Integration` branch, with its KiCad files,
its `simulation.py` and its `README.md`, and all three have run.

## 28.1 E01 Circular Loop

![E01 drawn from above and in section: a 30 mm square FR-4 board with one red loop on Top, 10 mm in radius to the trace's centre and 0.5 mm wide, opened on the right by a 0.2 mm gap where the solver connects it; the section through the centre shows the 1.53 mm core with the 35 µm trace on top, 20 mm apart](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/E01_circular_loop/elmerboards_1_board.webp)

| Item | Value |
|---|---|
| Board | 30 mm × 30 mm, 1.6 mm thick, no stack-up |
| Copper | one trace on F.Cu, net `LOOP`: a circle of 10 mm radius to its centre line, 0.5 mm wide, 35 µm thick, opened by a 0.2 mm gap between its round ends |
| What Elmer checks | the loop's inductance L at 10 kHz (uniform current) and 3.5 MHz (the coil boards' frequency), its resistance R against the DC resistance, and the same L from the field's energy |
| References | Grover's ring formula with the trace's geometric mean distance, times the share of the circle the copper covers; the resistance of an annular sector |
| Status | **run**: [Elmer FEM Test Board Results](Elmer-FEM-Test-Board-Results.md#291-e01-circular-loop) |

## 28.2 E02 Coaxial Loops

![E02 drawn from above and in section: E01's loop twice on a 30 mm square board, the TX in red on Top and the RX in blue on Bottom right under it, so that only the blue edge of the RX shows from above; the section shows the two 35 µm traces on either face of the 1.53 mm core, their centres 1.565 mm apart](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/E02_coaxial_loops/elmerboards_1_board.webp)

| Item | Value |
|---|---|
| Board | 30 mm × 30 mm, 1.6 mm thick, no stack-up |
| Copper | E01's loop twice: TX on F.Cu and RX on B.Cu, one above the other, their centres about 1.565 mm apart in z |
| What Elmer checks | the mutual inductance M from the voltage the TX's 1 A induces in the open RX, and the TX's own L and R beside a second loop |
| References | Maxwell's formula for two coaxial circles, averaged over both traces' widths, times the share of the circle the copper covers |
| Status | **run**: [Elmer FEM Test Board Results](Elmer-FEM-Test-Board-Results.md#292-e02-coaxial-loops) |

## 28.3 S0d2_1x_OD23_2L_tiny_TX3top_Cut

A small angle encoder from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator)
(`Coil_2_11.7_2_1_3_Single_SteppedDiagonal`), in `Examples/Inductive Coils/` (non-commercial licence,
see that folder's `LICENSE.md`). A stator carries one TX and two receivers, SIN and COS; a rotor with
two quarter-ring copper sectors sits above it. The TX runs at 3.5 MHz, where eddy currents in the
rotor change how much of the TX's field reaches each receiver, so SIN and COS follow the sine and
cosine of twice the rotor's angle.

<img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S0d2_1x_OD23_2L_tiny_TX3top_Cut/elmerboards_1_boards.webp" width="760" alt="S0d2_1x_OD23_2L_tiny_TX3top_Cut, drawn by the coil generator. Left, the stator, board radius 2 to 11.7 mm: three TX turns in red on the top layer round the outside, with a short tail to the terminal at the right; inside them the SIN and COS receivers, each weaving between Top (red) and Bottom (blue) through vias (dots), two sine periods per turn. Right, the rotor: two copper quarter-ring sectors on Top, opposite each other round the bore">

| Item | Value |
|---|---|
| Stator | 23.4 mm across (bore and outer radius 2 and 11.7 mm), 0.8 mm thick, 2 copper layers of 35 µm |
| TX | three turns, all on F.Cu (r = 7.2, 7.8 and 8.4 mm); a short tail on B.Cu brings the inner end back out, so the two ends sit stacked at KiCad (111, 100) |
| SIN and COS | the band r = 3.2 to 6.1 mm, each making two sine periods per turn, nets `2` and `1` |
| Rotor | two quarter-ring sectors, r = 2.52 to 9.0 mm; it repeats itself every 180° |
| Air gap | stator F.Cu top face to rotor copper face, 1 mm by default; run at 0.1, 0.5, 1, 1.5 and 2 mm |
| Masks | both boards get 20 µm of solder mask on both faces with tented vias, as the coil boards' brief sets; to this solve it is air |
| What Elmer checks | M from the TX to SIN and to COS at 16 rotor angles, the angle error read back from them, the TX's L and R with the rotor away and present; every solve checks the TX's L and R a second way, from the field energy and the eddy power |
| References | the generator's estimates for the TX (0.29 µH with the rotor away, 0.23 µH with it, 0.38 Ω DC), and a perfect sine and cosine pair 90° apart |
| Status | **run**: [Elmer FEM Test Board Results](Elmer-FEM-Test-Board-Results.md#293-s0d2_1x_od23_2l_tiny_tx3top_cut) |

**How SIN and COS are opened.** A 0.2 mm cut across a top trace of each, because that is how the
real board is opened and routed to the IC. The cut is made in the model; the board files are as the
generator wrote them. Each cut is the spot on the receiver's top trace nearest its layer-change via
where a 0.2 mm cut has at least 0.45 mm of free board round it and sits at least 0.75 mm from any via
centre: 0.86 mm from the via on both receivers. The two spots are 45° apart about the axis, a quarter
of the electrical period, as SIN and COS are.

![Where SIN and COS are opened. Left, the stator from above with the TX in dark grey, SIN in blue and COS in orange, each on F.Cu (dark) and B.Cu (light); a small white box marks each cut and the TX port is ringed at the right. Right, close-ups: SIN cut at KiCad (96.59, 100.50) and COS cut at KiCad (97.24, 97.94), each a 0.2 mm white box across the top trace 0.86 mm from the via, which stays, with 0.46 mm clear of other copper; and the TX's two ends, F.Cu over B.Cu, at KiCad (111.00, 100.00), not cut. A note says the copper inside each box is taken out, the two cut faces become the electrodes and the port sheet spans the gap at the trace's lower face](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Elmer-FEM-Test-Boards/S0d2_1x_OD23_2L_tiny_TX3top_Cut/elmerboards_2_cuts.webp)

| Coil | Net | Opened at (KiCad mm) | How |
|---|---|---|---|
| TX | `TX` | (111, 100), F.Cu and B.Cu | its two stacked ends; 1 A is driven here |
| SIN | `2` | cut at (96.591, 100.496), F.Cu | a 0.2 mm gap across the top trace; the via at (97.044, 101.225) stays |
| COS | `1` | cut at (97.239, 97.940), F.Cu | a 0.2 mm gap across the top trace; the via at (97.044, 98.775) stays |

The generator also warns, for this board, that the tank's parallel resistance at the nominal air
gap may be as low as 32 Ω (if the AC resistance is twice the DC value), where the IPS2550 needs at
least 250 Ω, and that it found no spot on either receiver with room for two vias for its own cut;
the cuts above were placed for Elmer instead.

The branch solves five more coil boards made from the same small coil set; they are in
[`Examples/Inductive Coils/`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/tree/Elmer_Integration/Examples/Inductive%20Coils).

| Previous | Next |
|:---|---:|
| [Elmer FEM Simulating Your Own Board](Elmer-FEM-Simulating-Your-Own-Board.md) | [Elmer FEM Test Board Results](Elmer-FEM-Test-Board-Results.md) |
