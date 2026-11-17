# S0_1x_OD22_2L_tiny_TXtop_Cut: SIN and COS over the rotor's turn in FastHenry

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 22.2 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one FastHenry solve: the stator's tracks as filaments and the rotor's copper as a grid of bars turned to that angle, solved directly, so each solve is the exact answer of its model. Each is checked by reciprocity: the M from the TX to a receiver and the M from the receiver back to the TX must agree (the Reciprocity column gives how far apart they are, as a part of the larger receiver's M; a solve is read when it is within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.50 / 1.51 nH (33 / 33 mV) | 0.2° rms, 0.2° peak |
| 1.5 mm | 8 of 8 | 2.25 / 2.25 nH (49 / 50 mV) | 0.1° rms, 0.2° peak |
| 1 mm | 8 of 8 | 3.40 / 3.41 nH (75 / 75 mV) | 0.2° rms, 0.2° peak |
| 0.5 mm | 8 of 8 | 5.12 / 5.12 nH (113 / 113 mV) | 0.3° rms, 0.5° peak |
| 0.1 mm | 8 of 8 | 6.70 / 6.70 nH (147 / 147 mV) | 1.0° rms, 1.3° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.50 nH and COS ±1.51 nH, that is ±33 and ±33 mV of EMF.*

Best sine fit: SIN amplitude 1.504 nH, offset -0.114 nH, phase 45.3°; COS amplitude 1.509 nH, offset -0.111 nH, phase -44.7°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.2° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 0.9505 | -1.1659 | +0.03° | 140.753 | 269.67 | 7,113 | exact | 0.7 GB | 3 min |
| 45° | 1.4016 | -0.1044 | -0.07° | 140.790 | 269.62 | 7,113 | exact | 0.7 GB | 3 min |
| 90° | 0.9324 | 0.9585 | +0.21° | 140.794 | 269.62 | 7,113 | exact | 0.7 GB | 3 min |
| 135° | -0.1177 | 1.4075 | -0.19° | 140.800 | 269.61 | 7,113 | exact | 0.7 GB | 3 min |
| 180° | -1.1805 | 0.9392 | +0.21° | 140.833 | 269.57 | 7,113 | exact | 0.7 GB | 3 min |
| 225° | -1.6254 | -0.1138 | -0.20° | 140.798 | 269.61 | 7,113 | exact | 0.7 GB | 3 min |
| 270° | -1.1661 | -1.1828 | +0.15° | 140.784 | 269.62 | 7,113 | exact | 0.7 GB | 2 min |
| 315° | -0.1101 | -1.6248 | -0.15° | 140.769 | 269.63 | 7,113 | exact | 0.7 GB | 2 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.25 nH and COS ±2.25 nH, that is ±49 and ±50 mV of EMF.*

Best sine fit: SIN amplitude 2.246 nH, offset -0.115 nH, phase 45.0°; COS amplitude 2.252 nH, offset -0.113 nH, phase -45.0°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.2° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 1.4631 | -1.6964 | -0.00° | 138.200 | 271.55 | 7,113 | exact | 0.7 GB | 5 min |
| 45° | 2.1499 | -0.1153 | -0.05° | 138.252 | 271.49 | 7,113 | exact | 0.7 GB | 5 min |
| 90° | 1.4557 | 1.4719 | +0.19° | 138.256 | 271.48 | 7,113 | exact | 0.7 GB | 5 min |
| 135° | -0.1080 | 2.1558 | -0.17° | 138.261 | 271.48 | 7,113 | exact | 0.7 GB | 5 min |
| 180° | -1.6968 | 1.4625 | +0.20° | 138.313 | 271.42 | 7,113 | exact | 0.7 GB | 5 min |
| 225° | -2.3727 | -0.1041 | -0.20° | 138.262 | 271.49 | 7,113 | exact | 0.7 GB | 5 min |
| 270° | -1.6946 | -1.7019 | +0.13° | 138.246 | 271.49 | 7,113 | exact | 0.7 GB | 3 min |
| 315° | -0.1203 | -2.3736 | -0.10° | 138.228 | 271.50 | 7,113 | exact | 0.7 GB | 3 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.40 nH and COS ±3.41 nH, that is ±75 and ±75 mV of EMF.*

Best sine fit: SIN amplitude 3.403 nH, offset -0.125 nH, phase 44.2°; COS amplitude 3.410 nH, offset -0.122 nH, phase -45.8°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.2° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | -0.1286 | -0.1217 |  | 146.898 | 264.07 | 3,511 | exact | 0.2 GB | 26 s |
| 0° | 2.2339 | -2.5543 | -0.02° | 133.988 | 274.49 | 7,113 | exact | 0.7 GB | 3 min |
| 45° | 3.3087 | -0.1740 | -0.06° | 134.062 | 274.40 | 7,113 | exact | 0.7 GB | 3 min |
| 90° | 2.2876 | 2.2432 | +0.19° | 134.066 | 274.38 | 7,113 | exact | 0.7 GB | 3 min |
| 135° | -0.0668 | 3.3146 | -0.16° | 134.071 | 274.39 | 7,113 | exact | 0.7 GB | 3 min |
| 180° | -2.4893 | 2.2940 | +0.24° | 134.154 | 274.29 | 7,113 | exact | 0.7 GB | 3 min |
| 225° | -3.5425 | -0.0616 | -0.22° | 134.077 | 274.40 | 7,113 | exact | 0.7 GB | 3 min |
| 270° | -2.5505 | -2.4968 | +0.13° | 134.059 | 274.40 | 7,113 | exact | 0.7 GB | 2 min |
| 315° | -0.1773 | -3.5447 | -0.09° | 134.038 | 274.41 | 7,113 | exact | 0.7 GB | 2 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±5.12 nH and COS ±5.12 nH, that is ±113 and ±113 mV of EMF.*

Best sine fit: SIN amplitude 5.117 nH, offset -0.157 nH, phase 42.5°; COS amplitude 5.124 nH, offset -0.156 nH, phase -47.5°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.3° rms and 0.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 3.2965 | -3.9140 | +0.11° | 126.074 | 280.19 | 7,113 | exact | 0.7 GB | 3 min |
| 45° | 4.9938 | -0.4022 | -0.24° | 126.173 | 280.08 | 7,113 | exact | 0.7 GB | 3 min |
| 90° | 3.5688 | 3.3055 | +0.34° | 126.176 | 280.07 | 7,113 | exact | 0.7 GB | 3 min |
| 135° | 0.0946 | 4.9996 | -0.31° | 126.181 | 280.08 | 7,113 | exact | 0.7 GB | 4 min |
| 180° | -3.6260 | 3.5720 | +0.47° | 126.321 | 279.93 | 7,113 | exact | 0.7 GB | 4 min |
| 225° | -5.2738 | 0.1029 | -0.40° | 126.211 | 280.08 | 7,113 | exact | 0.7 GB | 4 min |
| 270° | -3.9089 | -3.6349 | +0.29° | 126.192 | 280.07 | 7,113 | exact | 0.7 GB | 2 min |
| 315° | -0.4023 | -5.2773 | -0.26° | 126.166 | 280.09 | 7,113 | exact | 0.7 GB | 2 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.70 nH and COS ±6.70 nH, that is ±147 and ±147 mV of EMF.*

Best sine fit: SIN amplitude 6.695 nH, offset -0.218 nH, phase 39.7°; COS amplitude 6.700 nH, offset -0.217 nH, phase -50.3°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 1.0° rms and 1.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 4.1219 | -5.3129 | +0.75° | 111.641 | 297.70 | 7,113 | exact | 0.7 GB | 5 min |
| 45° | 6.4873 | -0.9532 | -0.95° | 111.728 | 297.69 | 7,113 | exact | 0.7 GB | 5 min |
| 90° | 4.8293 | 4.1295 | +1.03° | 111.731 | 297.68 | 7,113 | exact | 0.7 GB | 5 min |
| 135° | 0.5194 | 6.4932 | -0.96° | 111.735 | 297.68 | 7,113 | exact | 0.7 GB | 5 min |
| 180° | -4.5893 | 4.8244 | +1.26° | 111.938 | 297.65 | 7,113 | exact | 0.7 GB | 5 min |
| 225° | -6.8483 | 0.5301 | -1.12° | 111.834 | 297.69 | 7,113 | exact | 0.7 GB | 5 min |
| 270° | -5.3106 | -4.5977 | +0.99° | 111.813 | 297.71 | 7,113 | exact | 0.7 GB | 3 min |
| 315° | -0.9509 | -6.8528 | -1.00° | 111.787 | 297.71 | 7,113 | exact | 0.7 GB | 3 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 4.45 times and COS 4.44 times larger.*

## Against the expectation

The generator estimates the TX at 144 nH with the rotor away and 116 nH with it (its drop with the rotor is an upper estimate). FastHenry gives 146.9 nH with the rotor away, and 140.8 to 140.8 nH with the rotor at 2 mm, and 138.2 to 138.3 nH with the rotor at 1.5 mm, and 134.0 to 134.2 nH with the rotor at 1 mm, and 126.1 to 126.3 nH with the rotor at 0.5 mm, and 111.6 to 111.9 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../FastHenry%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD22_2L_tiny_TXtop_Cut_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In FastHenry, SIN is opened by a cut in its top trace at (97.16, 101.63) and COS at (98.37, 97.16), the TX at its ends at (110.4, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in FastHenry](../S0_1x_OD22_2L_tiny_TXtop_Cut_fasthenry_setup.webp)

*How the boards are set up in FastHenry, drawn by [`rig_picture.py`](../FastHenry%20Simulation/rig_picture.py) from the model simulation.py solves: the stator's tracks as segments split into filaments, the rotor copper side down over the stator as a grid of bars, each receiver opened by a cut across a top trace (the port is between the two cut faces, and the receiver is open there, so the voltage across the cut is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
