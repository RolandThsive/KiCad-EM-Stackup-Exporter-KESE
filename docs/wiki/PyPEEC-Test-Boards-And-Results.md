# 26.2 PyPEEC Test Boards And Results

Three boards: the proof boards E01 and E02 in `Examples/`, whose answers are known without any solver,
and the inductive encoder board S0d2_1x_OD23_2L_tiny_TX3top_Cut in `Examples/Inductive Coils/`, all on
the `PyPEEC_Integration` branch. Every number here is in their results files, with the settings, the
versions, the grid, the time, the memory and PyPEEC's own checks of every solve. The branch solves five
more coil boards in the same way, listed in
[`Examples/Inductive Coils/README.md`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/PyPEEC_Integration/Examples/Inductive%20Coils/README.md).

## 26.2.1 E01 Circular Loop

One circular trace on F.Cu, 10 mm in radius to its centre line, 0.5 mm wide and 35 µm thick, opened by
a 0.2 mm gap where the bridge puts its two terminals, on a 30 mm square board; PyPEEC drives 1 A
through it.

| Top | Bottom |
|:---:|:---:|
| <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Test-Boards/E01_circular_loop/E01_circular_loop_top.webp" width="320" alt="E01 from the top, rendered by KESE: a 30 mm square board with one yellow copper loop, 10 mm in radius and 0.5 mm wide, opened on the right by a small gap between its two round ends"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Test-Boards/E01_circular_loop/E01_circular_loop_bottom.webp" width="320" alt="E01 from the bottom, rendered by KESE: the bare board, since B.Cu holds no copper"> |

| Quantity | Reference | 100 µm | 50 µm | 25 µm | 12.5 µm |
|---|---|---|---|---|---|
| Grid (one voxel layer, 35 µm) | | 208 × 208 | 412 × 412 | 822 × 822 | 1642 × 1642 |
| Copper voxels | | 3,102 | 12,467 | 49,979 | 199,997 |
| L at 10 kHz | 55.99 to 56.44 nH | 57.00 nH (+1.8 %) | 56.59 nH (+1.1 %) | 56.24 nH (+0.44 %) | 56.09 nH (+0.18 %) |
| L from the stored energy at 10 kHz | the same | 57.00 nH | 56.59 nH | 56.24 nH | 56.09 nH |
| R at 10 kHz | 61.20 mΩ | 69.25 mΩ (+13 %) | 65.23 mΩ (+6.6 %) | 63.20 mΩ (+3.3 %) | 62.30 mΩ (+1.8 %) |
| R from the losses at 10 kHz | the same | 69.25 mΩ | 65.23 mΩ | 63.20 mΩ | 62.30 mΩ |
| L at 3.5 MHz | about 55.44 nH (an estimate) | 56.14 nH | 55.61 nH | 55.16 nH | 54.99 nH (−0.8 %) |
| R at 3.5 MHz | | 83.37 mΩ | 81.93 mΩ | 80.53 mΩ | 79.79 mΩ |
| R at 3.5 MHz over R at 10 kHz | | 1.20 | 1.26 | 1.27 | 1.28 |

L settles from above into the band that Grover's ring formula gives the open loop (55.99 nH with the
current stopped at the round ends' centres, 56.44 nH with it taken on to the gap's faces), each step
about half the one before, which puts its limit at about 55.9 to 56.0 nH, the band's lower end. R's
excess over the annular sector's DC resistance halves with each halving of the voxels, since the
trace's round edges are drawn as steps, and taken to zero voxel size it is 61.4 mΩ, 0.3 % over the
sector, which the two half-discs past the sector's ends add. L and R from the terminals' voltage and
from the stored energy and the losses agree to the last digit at every size, so the terminals and the
read-back measure what the field holds. At 3.5 MHz R rises by 28 % as the current crowds to the trace's
edges, and every solve took one GMRES iteration and passed PyPEEC's own checks.

## 26.2.2 E02 Coaxial Loops

E01's loop twice on the same 30 mm board, TX on F.Cu and RX on B.Cu directly under it, 1.565 mm apart;
TX carries 1 A and RX is open (0 A), so the voltage across RX's gap gives the mutual inductance M.

| Top | Bottom |
|:---:|:---:|
| <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Test-Boards/E02_coaxial_loops/E02_coaxial_loops_top.webp" width="320" alt="E02 from the top, rendered by KESE: the TX loop on F.Cu, opened on the right"> | <img src="https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Test-Boards/E02_coaxial_loops/E02_coaxial_loops_bottom.webp" width="320" alt="E02 from the bottom, rendered by KESE: the RX loop on B.Cu right under the TX, its gap showing on the left as the board is seen from below"> |

| Quantity | Reference | 100 µm | 50 µm |
|---|---|---|---|
| Grid | | 208 × 208 × 46 | 412 × 412 × 46 |
| M at 10 kHz | 24.13 nH | 24.01 nH (−0.51 %) | 24.09 nH (−0.17 %) |
| M at 3.5 MHz | about 24.13 nH | 23.78 nH | 23.84 nH |
| TX's L at 10 kHz | E01's: 57.00 and 56.59 nH | 57.00 nH | 56.60 nH (+0.01 %) |
| TX's L from the stored energy at 10 kHz | the same | 57.00 nH | 56.60 nH |
| TX's R at 10 kHz | E01's: 69.25 and 65.23 mΩ | 69.25 mΩ | 65.23 mΩ |
| TX's L at 3.5 MHz | E01's: 56.14 and 55.61 nH | 56.09 nH (−0.08 %) | 55.55 nH (−0.09 %) |
| TX's R at 3.5 MHz | E01's: 83.37 and 81.93 mΩ | 83.88 mΩ (+0.6 %) | 82.56 mΩ (+0.8 %) |

M is 0.17 % under Maxwell's formula for two coaxial loops at 50 µm, and its error fell from 0.51 % when
the voxels halved, so its limit is at or a little over 24.13 nH; the reference carries the same 0.8 %
open-loop uncertainty as E01's L, so the board cannot tell the two apart more finely than that. The open
RX leaves the TX's L and R as E01's to 0.01 % at 10 kHz, as a loop with no current round it must. At
3.5 MHz the RX's eddy currents, circulating across its trace, add 0.8 % to the TX's R and show as a real
part of the mutual impedance, 3.2 mΩ at 50 µm: the proximity effect.

## 26.2.3 S0d2_1x_OD23_2L_tiny_TX3top_Cut

An inductive angle encoder from the
[Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator),
23.4 mm across: a stator with a three-turn TX on the top layer round two receivers, SIN and COS, each
making two sine periods per turn, under a rotor of two quarter-ring copper sectors, solved at 16 angles
over the whole turn at each of five air gaps with 1 A at 3.5 MHz in the TX (non-commercial licence, see
`Examples/Inductive Coils/LICENSE.md`).

![S0d2_1x_OD23_2L_tiny_TX3top_Cut drawn by the coil generator: the stator on the left, a round board 2 to 11.7 mm in radius, with three red TX turns on the top layer round the outside and the SIN and COS receivers inside them, red on Top and blue on Bottom with vias as dots, each making two sine periods per turn; the rotor on the right with two red quarter-ring copper sectors opposite each other](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Test-Boards/S0d2_1x_OD23_2L_tiny_TX3top_Cut/S0d2_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp)

| Air gap | Amplitude SIN / COS | Angle error (electrical) | Solves passing both checks | L TX over the turn |
|---|---|---|---|---|
| 2 mm | 1.89 / 1.90 nH (42 / 42 mV) | 0.2° rms, 0.3° peak | 16 of 16 | 284.1 to 284.3 nH |
| 1.5 mm | 2.94 / 2.95 nH (65 / 65 mV) | 0.2° rms, 0.4° peak | 16 of 16 | 280.1 to 280.4 nH |
| 1 mm | 4.61 / 4.63 nH (101 / 102 mV) | 0.2° rms, 0.4° peak | 16 of 16 | 271.5 to 272.0 nH |
| 0.5 mm | 7.14 / 7.16 nH (157 / 157 mV) | 0.4° rms, 0.7° peak | 16 of 16 | 257.1 to 257.7 nH |
| 0.1 mm | 9.60 / 9.62 nH (211 / 212 mV) | 0.9° rms, 1.3° peak | 16 of 16 | 235.7 to 236.6 nH |
| rotor away | | | 1 of 1 | 296.4 nH |

![SIN and COS of S0d2_1x_OD23_2L_tiny_TX3top_Cut against the rotor angle at a 1 mm air gap, 0 to 360°: the mutual inductance from the TX in nH, SIN in blue and COS in orange, one dot per PyPEEC solve joined by solid lines, each swinging about ±4.6 nH twice per turn, COS leading SIN by a quarter of the 180° period; the dotted ideal sine and cosine, each channel's best fit, lie almost on the solves](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Test-Board-Results/S0d2_1x_OD23_2L_tiny_TX3top_Cut/results_gap1mm.webp)

![SIN of S0d2_1x_OD23_2L_tiny_TX3top_Cut at each air gap against the rotor angle, 0 to 360°: five curves, one per gap, from ±9.6 nH at 0.1 mm (red) through 0.5, 1 and 1.5 mm to ±1.9 nH at 2 mm (teal), each with its dotted best sine; below, each solve less its ideal curve, within ±0.02 nH at 2 mm and up to about ±0.2 nH at 0.1 mm, alternating in sign from one angle to the next](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Test-Board-Results/S0d2_1x_OD23_2L_tiny_TX3top_Cut/SINCOS_gaps_SIN.webp)

All 81 solves pass both checks, the TX's L and R from its voltage agreeing with the stored energy and
the losses within 0.001 %, and at every gap SIN and COS are within 0.4 % of each other in amplitude and
89.9° to 90.1° apart. The signal grows 5.1 times from 2 mm to 0.1 mm, and the angle error is 0.2° rms
from 1 to 2 mm, 0.4° at 0.5 mm and 0.9° at 0.1 mm in electrical degrees (half that in mechanical
degrees), where it alternates in sign from one angle to the next: the fourth-harmonic ripple that
two-coil sensors typically show (Kuntz, Gerlach and Fella, [arXiv 2503.14627](https://arxiv.org/abs/2503.14627)).
The second half turn repeats the first to the last digit, because the rotor's two sectors, turned by
180°, fall on the very same voxels. The rotor lowers L TX from 296.4 nH by 8.3 % at 1 mm and by 20 % at
0.1 mm, where the generator estimated 292 nH with the rotor away and 226 nH with it, an upper estimate
of the drop. Every solve, with its M, L, R, iterations, residual, memory and time, is in the board's
[`Results/SINCOS_Results.md`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/PyPEEC_Integration/Examples/Inductive%20Coils/S0d2_1x_OD23_2L_tiny_TX3top_Cut/Results/SINCOS_Results.md).

| Previous | Next |
|:---|---:|
| [Elmer FEM Test Boards And Results](Elmer-FEM-Test-Boards-And-Results.md) | [FastHenry Test Boards And Results](FastHenry-Test-Boards-And-Results.md) |
