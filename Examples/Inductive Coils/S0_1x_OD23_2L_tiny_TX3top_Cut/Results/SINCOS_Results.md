# S0_1x_OD23_2L_tiny_TX3top_Cut: SIN and COS over the rotor's turn in FastHenry

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 23.4 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one FastHenry solve: the stator's tracks as filaments and the rotor's copper as a grid of bars turned to that angle, solved directly, so each solve is the exact answer of its model. Each is checked by reciprocity: the M from the TX to a receiver and the M from the receiver back to the TX must agree (the Reciprocity column gives how far apart they are, as a part of the larger receiver's M; a solve is read when it is within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 2.38 / 2.38 nH (52 / 52 mV) | 0.3° rms, 0.3° peak |
| 1.5 mm | 8 of 8 | 3.46 / 3.46 nH (76 / 76 mV) | 0.3° rms, 0.3° peak |
| 1 mm | 8 of 8 | 5.07 / 5.08 nH (112 / 112 mV) | 0.3° rms, 0.4° peak |
| 0.5 mm | 8 of 8 | 7.36 / 7.37 nH (162 / 162 mV) | 0.5° rms, 0.7° peak |
| 0.1 mm | 8 of 8 | 9.41 / 9.41 nH (207 / 207 mV) | 1.2° rms, 1.4° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.38 nH and COS ±2.38 nH, that is ±52 and ±52 mV of EMF.*

Best sine fit: SIN amplitude 2.377 nH, offset -0.158 nH, phase 44.2°; COS amplitude 2.382 nH, offset -0.155 nH, phase -45.7°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.3° rms and 0.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 1.4968 | -1.8496 | +0.13° | 279.068 | 425.98 | 8,221 | exact | 0.9 GB | 2 min |
| 45° | 2.2377 | -0.1945 | -0.19° | 279.146 | 425.89 | 8,221 | exact | 0.9 GB | 2 min |
| 90° | 1.5246 | 1.5047 | +0.31° | 279.153 | 425.88 | 8,221 | exact | 0.9 GB | 2 min |
| 135° | -0.1152 | 2.2430 | -0.27° | 279.164 | 425.86 | 8,221 | exact | 0.9 GB | 2 min |
| 180° | -1.8153 | 1.5306 | +0.32° | 279.230 | 425.80 | 8,221 | exact | 0.9 GB | 2 min |
| 225° | -2.5424 | -0.1124 | -0.27° | 279.147 | 425.88 | 8,221 | exact | 0.9 GB | 2 min |
| 270° | -1.8494 | -1.8200 | +0.24° | 279.118 | 425.89 | 8,221 | exact | 0.9 GB | 2 min |
| 315° | -0.2004 | -2.5428 | -0.27° | 279.090 | 425.91 | 8,221 | exact | 0.9 GB | 2 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.46 nH and COS ±3.46 nH, that is ±76 and ±76 mV of EMF.*

Best sine fit: SIN amplitude 3.457 nH, offset -0.163 nH, phase 43.9°; COS amplitude 3.462 nH, offset -0.161 nH, phase -46.1°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.3° rms and 0.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 2.2249 | -2.6388 | +0.11° | 273.123 | 429.92 | 8,221 | exact | 0.9 GB | 2 min |
| 45° | 3.3224 | -0.2405 | -0.19° | 273.230 | 429.79 | 8,221 | exact | 0.9 GB | 2 min |
| 90° | 2.2958 | 2.2335 | +0.30° | 273.237 | 429.78 | 8,221 | exact | 0.9 GB | 2 min |
| 135° | -0.0792 | 3.3276 | -0.27° | 273.249 | 429.76 | 8,221 | exact | 0.9 GB | 2 min |
| 180° | -2.5572 | 2.3017 | +0.35° | 273.351 | 429.67 | 8,221 | exact | 0.9 GB | 2 min |
| 225° | -3.6314 | -0.0758 | -0.30° | 273.229 | 429.78 | 8,221 | exact | 0.9 GB | 2 min |
| 270° | -2.6370 | -2.5646 | +0.24° | 273.196 | 429.79 | 8,221 | exact | 0.9 GB | 2 min |
| 315° | -0.2458 | -3.6329 | -0.25° | 273.161 | 429.81 | 8,221 | exact | 0.9 GB | 2 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±5.07 nH and COS ±5.08 nH, that is ±112 and ±112 mV of EMF.*

Best sine fit: SIN amplitude 5.074 nH, offset -0.182 nH, phase 43.1°; COS amplitude 5.081 nH, offset -0.180 nH, phase -46.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.3° rms and 0.4° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | -0.1725 | -0.1660 |  | 294.556 | 413.21 | 4,180 | exact | 0.4 GB | 22 s |
| 0° | 3.2761 | -3.8631 | +0.12° | 263.700 | 435.82 | 8,221 | exact | 0.9 GB | 2 min |
| 45° | 4.9362 | -0.3702 | -0.23° | 263.848 | 435.62 | 8,221 | exact | 0.9 GB | 2 min |
| 90° | 3.4726 | 3.2849 | +0.34° | 263.853 | 435.62 | 8,221 | exact | 0.9 GB | 2 min |
| 135° | 0.0147 | 4.9413 | -0.30° | 263.866 | 435.59 | 8,221 | exact | 0.9 GB | 2 min |
| 180° | -3.6504 | 3.4777 | +0.42° | 264.029 | 435.45 | 8,221 | exact | 0.9 GB | 2 min |
| 225° | -5.2680 | 0.0208 | -0.36° | 263.847 | 435.62 | 8,221 | exact | 0.9 GB | 2 min |
| 270° | -3.8598 | -3.6599 | +0.28° | 263.809 | 435.63 | 8,221 | exact | 0.9 GB | 2 min |
| 315° | -0.3736 | -5.2701 | -0.27° | 263.767 | 435.66 | 8,221 | exact | 0.9 GB | 2 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±7.36 nH and COS ±7.37 nH, that is ±162 and ±162 mV of EMF.*

Best sine fit: SIN amplitude 7.361 nH, offset -0.231 nH, phase 41.5°; COS amplitude 7.367 nH, offset -0.230 nH, phase -48.5°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.5° rms and 0.7° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 4.6592 | -5.7041 | +0.29° | 247.211 | 446.40 | 8,221 | exact | 0.9 GB | 2 min |
| 45° | 7.1759 | -0.7414 | -0.45° | 247.407 | 446.12 | 8,221 | exact | 0.9 GB | 2 min |
| 90° | 5.1951 | 4.6668 | +0.54° | 247.411 | 446.11 | 8,221 | exact | 0.9 GB | 2 min |
| 135° | 0.2839 | 7.1810 | -0.48° | 247.423 | 446.09 | 8,221 | exact | 0.9 GB | 2 min |
| 180° | -5.1458 | 5.1955 | +0.69° | 247.697 | 445.89 | 8,221 | exact | 0.9 GB | 2 min |
| 225° | -7.5760 | 0.2955 | -0.59° | 247.420 | 446.10 | 8,221 | exact | 0.9 GB | 2 min |
| 270° | -5.6998 | -5.1557 | +0.48° | 247.377 | 446.12 | 8,221 | exact | 0.9 GB | 2 min |
| 315° | -0.7405 | -7.5787 | -0.47° | 247.327 | 446.15 | 8,221 | exact | 0.9 GB | 2 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±9.41 nH and COS ±9.41 nH, that is ±207 and ±207 mV of EMF.*

Best sine fit: SIN amplitude 9.407 nH, offset -0.311 nH, phase 39.0°; COS amplitude 9.410 nH, offset -0.312 nH, phase -51.0°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 1.2° rms and 1.4° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 5.7119 | -7.5239 | +0.86° | 221.389 | 471.79 | 8,221 | exact | 0.9 GB | 2 min |
| 45° | 9.1093 | -1.4817 | -1.09° | 221.586 | 471.52 | 8,221 | exact | 0.9 GB | 2 min |
| 90° | 6.8276 | 5.7173 | +1.16° | 221.588 | 471.48 | 8,221 | exact | 0.9 GB | 2 min |
| 135° | 0.8551 | 9.1146 | -1.07° | 221.597 | 471.49 | 8,221 | exact | 0.9 GB | 2 min |
| 180° | -6.3834 | 6.8164 | +1.42° | 221.992 | 471.57 | 8,221 | exact | 0.9 GB | 2 min |
| 225° | -9.6125 | 0.8707 | -1.26° | 221.614 | 471.60 | 8,221 | exact | 0.9 GB | 2 min |
| 270° | -7.5218 | -6.3918 | +1.12° | 221.566 | 471.63 | 8,221 | exact | 0.9 GB | 2 min |
| 315° | -1.4769 | -9.6162 | -1.15° | 221.510 | 471.66 | 8,221 | exact | 0.9 GB | 2 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 3.96 times and COS 3.95 times larger.*

## Against the expectation

The generator estimates the TX at 292 nH with the rotor away and 226 nH with it (its drop with the rotor is an upper estimate). FastHenry gives 294.6 nH with the rotor away, and 279.1 to 279.2 nH with the rotor at 2 mm, and 273.1 to 273.4 nH with the rotor at 1.5 mm, and 263.7 to 264.0 nH with the rotor at 1 mm, and 247.2 to 247.7 nH with the rotor at 0.5 mm, and 221.4 to 222.0 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../FastHenry%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In FastHenry, SIN is opened by a cut in its top trace at (97.16, 101.63) and COS at (98.37, 97.16), the TX at its ends at (111, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in FastHenry](../S0_1x_OD23_2L_tiny_TX3top_Cut_fasthenry_setup.webp)

*How the boards are set up in FastHenry, drawn by [`rig_picture.py`](../FastHenry%20Simulation/rig_picture.py) from the model simulation.py solves: the stator's tracks as segments split into filaments, the rotor copper side down over the stator as a grid of bars, each receiver opened by a cut across a top trace (the port is between the two cut faces, and the receiver is open there, so the voltage across the cut is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
