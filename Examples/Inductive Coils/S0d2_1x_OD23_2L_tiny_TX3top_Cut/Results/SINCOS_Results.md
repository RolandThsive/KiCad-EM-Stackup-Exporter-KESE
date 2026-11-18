# S0d2_1x_OD23_2L_tiny_TX3top_Cut: SIN and COS over the rotor's turn in FastHenry

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 23.4 mm across, 2 copper layers, 2 electrical periods per turn and a rotor of 2 copper sectors. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one FastHenry solve: the stator's tracks as filaments and the rotor's copper as a grid of bars turned to that angle, solved directly, so each solve is the exact answer of its model. Each is checked by reciprocity: the M from the TX to a receiver and the M from the receiver back to the TX must agree (the Reciprocity column gives how far apart they are, as a part of the larger receiver's M; a solve is read when it is within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 16 of 16 | 1.95 / 1.95 nH (43 / 43 mV) | 0.1° rms, 0.3° peak |
| 1.5 mm | 16 of 16 | 3.03 / 3.03 nH (67 / 67 mV) | 0.1° rms, 0.3° peak |
| 1 mm | 16 of 16 | 4.73 / 4.74 nH (104 / 104 mV) | 0.2° rms, 0.3° peak |
| 0.5 mm | 16 of 16 | 7.28 / 7.28 nH (160 / 160 mV) | 0.3° rms, 0.5° peak |
| 0.1 mm | 16 of 16 | 9.76 / 9.77 nH (215 / 215 mV) | 0.9° rms, 1.1° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.95 nH and COS ±1.95 nH, that is ±43 and ±43 mV of EMF.*

Best sine fit: SIN amplitude 1.946 nH, offset -0.031 nH, phase -137.3°; COS amplitude 1.950 nH, offset -0.029 nH, phase 132.8°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.3° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.3511 | 1.3984 | +0.05° | 282.105 | 425.75 | 9,264 | exact | 1.1 GB | 4 min |
| 22.5° | -1.9859 | 0.0523 | -0.13° | 282.164 | 425.68 | 9,264 | exact | 1.1 GB | 4 min |
| 45° | -1.4546 | -1.3522 | +0.10° | 282.185 | 425.66 | 9,264 | exact | 1.1 GB | 4 min |
| 67.5° | -0.1061 | -1.9848 | +0.04° | 282.209 | 425.62 | 9,264 | exact | 1.1 GB | 4 min |
| 90° | 1.2887 | -1.4536 | +0.09° | 282.248 | 425.59 | 9,264 | exact | 1.1 GB | 4 min |
| 112.5° | 1.9120 | -0.1038 | +0.02° | 282.197 | 425.65 | 9,264 | exact | 1.1 GB | 4 min |
| 135° | 1.3948 | 1.2964 | +0.09° | 282.146 | 425.68 | 9,264 | exact | 1.1 GB | 3 min |
| 157.5° | 0.0538 | 1.9180 | -0.26° | 282.103 | 425.70 | 9,264 | exact | 1.1 GB | 3 min |
| 180° | -1.3511 | 1.3984 | +0.05° | 282.105 | 425.75 | 9,264 | exact | 1.1 GB | 3 min |
| 202.5° | -1.9859 | 0.0523 | -0.13° | 282.164 | 425.68 | 9,264 | exact | 1.1 GB | 3 min |
| 225° | -1.4546 | -1.3522 | +0.10° | 282.185 | 425.66 | 9,264 | exact | 1.1 GB | 3 min |
| 247.5° | -0.1061 | -1.9848 | +0.04° | 282.209 | 425.62 | 9,264 | exact | 1.1 GB | 3 min |
| 270° | 1.2887 | -1.4536 | +0.09° | 282.248 | 425.59 | 9,264 | exact | 1.1 GB | 3 min |
| 292.5° | 1.9120 | -0.1038 | +0.02° | 282.197 | 425.65 | 9,264 | exact | 1.1 GB | 3 min |
| 315° | 1.3948 | 1.2964 | +0.09° | 282.146 | 425.68 | 9,264 | exact | 1.1 GB | 3 min |
| 337.5° | 0.0538 | 1.9180 | -0.26° | 282.103 | 425.70 | 9,264 | exact | 1.1 GB | 3 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.03 nH and COS ±3.03 nH, that is ±67 and ±67 mV of EMF.*

Best sine fit: SIN amplitude 3.026 nH, offset -0.032 nH, phase -137.3°; COS amplitude 3.030 nH, offset -0.028 nH, phase 132.8°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.3° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -2.0831 | 2.1875 | +0.05° | 277.263 | 429.83 | 9,264 | exact | 1.1 GB | 4 min |
| 22.5° | -3.0747 | 0.0987 | -0.16° | 277.350 | 429.73 | 9,264 | exact | 1.1 GB | 4 min |
| 45° | -2.2417 | -2.0844 | +0.12° | 277.373 | 429.69 | 9,264 | exact | 1.1 GB | 4 min |
| 67.5° | -0.1484 | -3.0729 | +0.03° | 277.401 | 429.65 | 9,264 | exact | 1.1 GB | 4 min |
| 90° | 2.0200 | -2.2393 | +0.13° | 277.469 | 429.60 | 9,264 | exact | 1.1 GB | 4 min |
| 112.5° | 2.9894 | -0.1455 | +0.00° | 277.390 | 429.70 | 9,264 | exact | 1.1 GB | 4 min |
| 135° | 2.1820 | 2.0316 | +0.11° | 277.323 | 429.72 | 9,264 | exact | 1.1 GB | 4 min |
| 157.5° | 0.1002 | 2.9983 | -0.28° | 277.264 | 429.75 | 9,264 | exact | 1.1 GB | 4 min |
| 180° | -2.0831 | 2.1875 | +0.05° | 277.263 | 429.83 | 9,264 | exact | 1.1 GB | 4 min |
| 202.5° | -3.0747 | 0.0987 | -0.16° | 277.350 | 429.73 | 9,264 | exact | 1.1 GB | 4 min |
| 225° | -2.2417 | -2.0844 | +0.12° | 277.373 | 429.69 | 9,264 | exact | 1.1 GB | 4 min |
| 247.5° | -0.1484 | -3.0729 | +0.03° | 277.401 | 429.65 | 9,264 | exact | 1.1 GB | 4 min |
| 270° | 2.0200 | -2.2393 | +0.13° | 277.469 | 429.60 | 9,264 | exact | 1.1 GB | 4 min |
| 292.5° | 2.9894 | -0.1455 | +0.00° | 277.390 | 429.70 | 9,264 | exact | 1.1 GB | 4 min |
| 315° | 2.1820 | 2.0316 | +0.11° | 277.323 | 429.72 | 9,264 | exact | 1.1 GB | 4 min |
| 337.5° | 0.1002 | 2.9983 | -0.28° | 277.264 | 429.75 | 9,264 | exact | 1.1 GB | 3 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±4.73 nH and COS ±4.74 nH, that is ±104 and ±104 mV of EMF.*

Best sine fit: SIN amplitude 4.730 nH, offset -0.031 nH, phase -137.7°; COS amplitude 4.736 nH, offset -0.025 nH, phase 132.4°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.3° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | -0.0255 | -0.0272 |  | 294.557 | 413.22 | 4,722 | exact | 0.5 GB | 36 s |
| 0° | -3.2112 | 3.4582 | +0.07° | 269.493 | 436.10 | 9,264 | exact | 1.1 GB | 4 min |
| 22.5° | -4.7917 | 0.2135 | -0.23° | 269.621 | 435.93 | 9,264 | exact | 1.1 GB | 5 min |
| 45° | -3.5027 | -3.2125 | +0.16° | 269.643 | 435.90 | 9,264 | exact | 1.1 GB | 5 min |
| 67.5° | -0.2497 | -4.7894 | +0.01° | 269.675 | 435.85 | 9,264 | exact | 1.1 GB | 6 min |
| 90° | 3.1547 | -3.4980 | +0.21° | 269.798 | 435.76 | 9,264 | exact | 1.1 GB | 4 min |
| 112.5° | 4.6895 | -0.2477 | -0.05° | 269.671 | 435.90 | 9,264 | exact | 1.1 GB | 4 min |
| 135° | 3.4506 | 3.1706 | +0.16° | 269.586 | 435.93 | 9,264 | exact | 1.1 GB | 5 min |
| 157.5° | 0.2145 | 4.7013 | -0.33° | 269.504 | 435.95 | 9,264 | exact | 1.1 GB | 4 min |
| 180° | -3.2112 | 3.4582 | +0.07° | 269.493 | 436.10 | 9,264 | exact | 1.1 GB | 5 min |
| 202.5° | -4.7917 | 0.2135 | -0.23° | 269.621 | 435.93 | 9,264 | exact | 1.1 GB | 5 min |
| 225° | -3.5027 | -3.2125 | +0.16° | 269.643 | 435.90 | 9,264 | exact | 1.1 GB | 3 min |
| 247.5° | -0.2497 | -4.7894 | +0.01° | 269.675 | 435.85 | 9,264 | exact | 1.1 GB | 5 min |
| 270° | 3.1547 | -3.4980 | +0.21° | 269.798 | 435.76 | 9,264 | exact | 1.1 GB | 4 min |
| 292.5° | 4.6895 | -0.2477 | -0.05° | 269.671 | 435.90 | 9,264 | exact | 1.1 GB | 4 min |
| 315° | 3.4506 | 3.1706 | +0.16° | 269.586 | 435.93 | 9,264 | exact | 1.1 GB | 4 min |
| 337.5° | 0.2145 | 4.7013 | -0.33° | 269.504 | 435.95 | 9,264 | exact | 1.1 GB | 4 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±7.28 nH and COS ±7.28 nH, that is ±160 and ±160 mV of EMF.*

Best sine fit: SIN amplitude 7.279 nH, offset -0.021 nH, phase -138.9°; COS amplitude 7.285 nH, offset -0.014 nH, phase 131.1°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.3° rms and 0.5° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -4.8135 | 5.4434 | +0.20° | 255.596 | 447.63 | 9,264 | exact | 1.1 GB | 6 min |
| 22.5° | -7.3432 | 0.5387 | -0.43° | 255.776 | 447.37 | 9,264 | exact | 1.1 GB | 3 min |
| 45° | -5.4550 | -4.8143 | +0.32° | 255.793 | 447.35 | 9,264 | exact | 1.1 GB | 5 min |
| 67.5° | -0.5337 | -7.3408 | -0.12° | 255.827 | 447.28 | 9,264 | exact | 1.1 GB | 5 min |
| 90° | 4.7877 | -5.4445 | +0.44° | 256.053 | 447.16 | 9,264 | exact | 1.1 GB | 4 min |
| 112.5° | 7.2151 | -0.5350 | -0.22° | 255.848 | 447.34 | 9,264 | exact | 1.1 GB | 6 min |
| 135° | 5.4343 | 4.8071 | +0.33° | 255.741 | 447.38 | 9,264 | exact | 1.1 GB | 6 min |
| 157.5° | 0.5375 | 7.2297 | -0.53° | 255.631 | 447.37 | 9,264 | exact | 1.1 GB | 3 min |
| 180° | -4.8135 | 5.4434 | +0.20° | 255.596 | 447.63 | 9,264 | exact | 1.1 GB | 4 min |
| 202.5° | -7.3432 | 0.5387 | -0.43° | 255.776 | 447.37 | 9,264 | exact | 1.1 GB | 5 min |
| 225° | -5.4550 | -4.8143 | +0.32° | 255.793 | 447.35 | 9,264 | exact | 1.1 GB | 5 min |
| 247.5° | -0.5337 | -7.3408 | -0.12° | 255.827 | 447.28 | 9,264 | exact | 1.1 GB | 6 min |
| 270° | 4.7877 | -5.4445 | +0.44° | 256.053 | 447.16 | 9,264 | exact | 1.1 GB | 3 min |
| 292.5° | 7.2151 | -0.5350 | -0.22° | 255.848 | 447.34 | 9,264 | exact | 1.1 GB | 4 min |
| 315° | 5.4343 | 4.8071 | +0.33° | 255.741 | 447.38 | 9,264 | exact | 1.1 GB | 4 min |
| 337.5° | 0.5375 | 7.2297 | -0.53° | 255.631 | 447.37 | 9,264 | exact | 1.1 GB | 4 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±9.76 nH and COS ±9.77 nH, that is ±215 and ±215 mV of EMF.*

Best sine fit: SIN amplitude 9.762 nH, offset -0.003 nH, phase -141.0°; COS amplitude 9.766 nH, offset 0.005 nH, phase 129.0°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.9° rms and 1.1° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -6.2224 | 7.5159 | +0.64° | 233.009 | 474.96 | 9,264 | exact | 1.1 GB | 4 min |
| 22.5° | -9.7992 | 1.2039 | -0.98° | 233.198 | 474.67 | 9,264 | exact | 1.1 GB | 4 min |
| 45° | -7.4675 | -6.2218 | +0.82° | 233.207 | 474.69 | 9,264 | exact | 1.1 GB | 4 min |
| 67.5° | -1.1257 | -9.7975 | -0.53° | 233.239 | 474.61 | 9,264 | exact | 1.1 GB | 4 min |
| 90° | 6.2569 | -7.4459 | +1.05° | 233.580 | 474.78 | 9,264 | exact | 1.1 GB | 4 min |
| 112.5° | 9.6202 | -1.1311 | -0.73° | 233.292 | 474.79 | 9,264 | exact | 1.1 GB | 4 min |
| 135° | 7.5093 | 6.2767 | +0.85° | 233.165 | 474.85 | 9,264 | exact | 1.1 GB | 4 min |
| 157.5° | 1.2008 | 9.6362 | -1.13° | 233.036 | 474.76 | 9,264 | exact | 1.1 GB | 4 min |
| 180° | -6.2224 | 7.5159 | +0.64° | 233.009 | 474.96 | 9,264 | exact | 1.1 GB | 4 min |
| 202.5° | -9.7992 | 1.2039 | -0.98° | 233.198 | 474.67 | 9,264 | exact | 1.1 GB | 4 min |
| 225° | -7.4675 | -6.2218 | +0.82° | 233.207 | 474.69 | 9,264 | exact | 1.1 GB | 4 min |
| 247.5° | -1.1257 | -9.7975 | -0.53° | 233.239 | 474.61 | 9,264 | exact | 1.1 GB | 4 min |
| 270° | 6.2569 | -7.4459 | +1.05° | 233.580 | 474.78 | 9,264 | exact | 1.1 GB | 4 min |
| 292.5° | 9.6202 | -1.1311 | -0.73° | 233.292 | 474.79 | 9,264 | exact | 1.1 GB | 4 min |
| 315° | 7.5093 | 6.2767 | +0.85° | 233.165 | 474.85 | 9,264 | exact | 1.1 GB | 4 min |
| 337.5° | 1.2008 | 9.6362 | -1.13° | 233.036 | 474.76 | 9,264 | exact | 1.1 GB | 3 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 5.02 times and COS 5.01 times larger.*

## Against the expectation

The generator estimates the TX at 292 nH with the rotor away and 226 nH with it (its drop with the rotor is an upper estimate). FastHenry gives 294.6 nH with the rotor away, and 282.1 to 282.2 nH with the rotor at 2 mm, and 277.3 to 277.5 nH with the rotor at 1.5 mm, and 269.5 to 269.8 nH with the rotor at 1 mm, and 255.6 to 256.1 nH with the rotor at 0.5 mm, and 233.0 to 233.6 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../FastHenry%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0d2_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In FastHenry, SIN is opened by a cut in its top trace at (96.59, 100.5) and COS at (97.24, 97.94), the TX at its ends at (111, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in FastHenry](../S0d2_1x_OD23_2L_tiny_TX3top_Cut_fasthenry_setup.webp)

*How the boards are set up in FastHenry, drawn by [`rig_picture.py`](../FastHenry%20Simulation/rig_picture.py) from the model simulation.py solves: the stator's tracks as segments split into filaments, the rotor copper side down over the stator as a grid of bars, each receiver opened by a cut across a top trace (the port is between the two cut faces, and the receiver is open there, so the voltage across the cut is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
