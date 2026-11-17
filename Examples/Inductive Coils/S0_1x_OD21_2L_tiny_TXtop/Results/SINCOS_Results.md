# S0_1x_OD21_2L_tiny_TXtop: SIN and COS over the rotor's turn in PyPEEC

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 21 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one PyPEEC solve with its own voxels, checked by working the TX's L and R out two ways: from its voltage, and from the stored energy and the losses (the L and R checks in each table give how far apart they are; a solve is read when both are within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 0.93 / 0.94 nH (21 / 21 mV) | 0.4° rms, 0.7° peak |
| 1.5 mm | 8 of 8 | 1.45 / 1.45 nH (32 / 32 mV) | 0.4° rms, 0.8° peak |
| 1 mm | 8 of 8 | 2.31 / 2.32 nH (51 / 51 mV) | 0.5° rms, 0.9° peak |
| 0.5 mm | 8 of 8 | 3.70 / 3.71 nH (81 / 82 mV) | 0.8° rms, 1.2° peak |
| 0.1 mm | 8 of 8 | 5.12 / 5.13 nH (113 / 113 mV) | 1.6° rms, 1.9° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±0.93 nH and COS ±0.94 nH, that is ±21 and ±21 mV of EMF.*

Best sine fit: SIN amplitude 0.934 nH, offset 0.366 nH, phase -135.5°; COS amplitude 0.937 nH, offset 0.232 nH, phase 134.5°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.7° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.2902 | 0.8933 | +0.37° | 128.612 | 288.12 | 3 iterations, 6.4e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 5 min |
| 45° | -0.5734 | 0.2407 | -0.04° | 128.609 | 288.46 | 3 iterations, 6.3e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 5 min |
| 90° | -0.2880 | -0.4244 | +0.49° | 128.554 | 288.66 | 3 iterations, 6.2e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 6 min |
| 135° | 0.3492 | -0.7073 | -0.55° | 128.630 | 288.35 | 3 iterations, 6.5e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 6 min |
| 180° | 1.0209 | -0.4280 | +0.36° | 128.700 | 287.90 | 3 iterations, 6.6e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 6 min |
| 225° | 1.3033 | 0.2120 | -0.71° | 128.749 | 287.54 | 3 iterations, 6.6e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 5 min |
| 270° | 1.0302 | 0.8944 | +0.35° | 128.761 | 287.26 | 3 iterations, 6.7e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 6 min |
| 315° | 0.3788 | 1.1736 | -0.26° | 128.692 | 287.64 | 3 iterations, 6.3e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 5 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.45 nH and COS ±1.45 nH, that is ±32 and ±32 mV of EMF.*

Best sine fit: SIN amplitude 1.451 nH, offset 0.363 nH, phase -136.0°; COS amplitude 1.455 nH, offset 0.236 nH, phase 134.1°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.8° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.6469 | 1.2711 | +0.31° | 126.953 | 289.83 | 3 iterations, 6.5e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |
| 45° | -1.0971 | 0.2599 | -0.01° | 126.943 | 290.34 | 3 iterations, 6.4e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |
| 90° | -0.6598 | -0.7738 | +0.47° | 126.855 | 290.66 | 3 iterations, 6.3e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 8 min |
| 135° | 0.3245 | -1.2235 | -0.59° | 126.971 | 290.19 | 3 iterations, 6.6e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |
| 180° | 1.3725 | -0.7952 | +0.41° | 127.083 | 289.50 | 3 iterations, 6.9e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |
| 225° | 1.8191 | 0.1922 | -0.77° | 127.158 | 288.99 | 3 iterations, 6.9e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 6 min |
| 270° | 1.4021 | 1.2564 | +0.35° | 127.187 | 288.53 | 3 iterations, 7.3e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |
| 315° | 0.3921 | 1.6986 | -0.19° | 127.080 | 289.13 | 3 iterations, 6.7e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 6 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.31 nH and COS ±2.32 nH, that is ±51 and ±51 mV of EMF.*

Best sine fit: SIN amplitude 2.314 nH, offset 0.369 nH, phase -137.0°; COS amplitude 2.319 nH, offset 0.250 nH, phase 133.1°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.5° rms and 0.9° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.3921 | 0.2447 |  | 133.322 | 283.80 | 3 iterations, 4.8e-08 | L +0.000 %, R +0.000 % | 0.8 GB | 1 min |
| 0° | -1.2118 | 1.9296 | +0.27° | 122.782 | 293.08 | 3 iterations, 6.4e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 3 min |
| 45° | -1.9596 | 0.3292 | -0.01° | 122.746 | 293.98 | 3 iterations, 6.6e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 3 min |
| 90° | -1.2893 | -1.3302 | +0.49° | 122.590 | 294.54 | 3 iterations, 6.7e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 135° | 0.2625 | -2.0768 | -0.68° | 122.782 | 293.76 | 3 iterations, 6.9e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 180° | 1.9532 | -1.4176 | +0.55° | 122.979 | 292.55 | 2 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 1.8 GB | 3 min |
| 225° | 2.6889 | 0.1352 | -0.88° | 123.110 | 291.76 | 3 iterations, 7.4e-08 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |
| 270° | 2.0529 | 1.8493 | +0.40° | 123.183 | 290.86 | 3 iterations, 7.6e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 315° | 0.4535 | 2.5796 | -0.15° | 123.002 | 291.97 | 3 iterations, 6.6e-08 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.70 nH and COS ±3.71 nH, that is ±81 and ±82 mV of EMF.*

Best sine fit: SIN amplitude 3.703 nH, offset 0.387 nH, phase -139.1°; COS amplitude 3.708 nH, offset 0.278 nH, phase 131.0°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.8° rms and 1.2° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -2.0512 | 3.0546 | +0.38° | 115.257 | 299.92 | 3 iterations, 5.9e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 2 min |
| 45° | -3.3262 | 0.5551 | -0.21° | 115.121 | 301.87 | 3 iterations, 6.9e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 2 min |
| 90° | -2.3525 | -2.1639 | +0.72° | 114.814 | 302.99 | 2 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 1.3 GB | 2 min |
| 135° | 0.0595 | -3.4341 | -1.00° | 115.165 | 301.59 | 3 iterations, 7.6e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 2 min |
| 180° | 2.8447 | -2.4641 | +0.96° | 115.550 | 299.20 | 3 iterations, 7.0e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 2 min |
| 225° | 4.0797 | -0.0593 | -1.17° | 115.828 | 297.75 | 3 iterations, 6.2e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |
| 270° | 3.1698 | 2.7552 | +0.67° | 116.019 | 295.71 | 3 iterations, 6.9e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 315° | 0.6712 | 3.9828 | -0.35° | 115.678 | 298.02 | 2 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±5.12 nH and COS ±5.13 nH, that is ±113 and ±113 mV of EMF.*

Best sine fit: SIN amplitude 5.124 nH, offset 0.392 nH, phase -142.4°; COS amplitude 5.125 nH, offset 0.263 nH, phase 127.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 1.6° rms and 1.9° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.7° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -2.8140 | 4.2430 | +1.13° | 102.603 | 320.86 | 4 iterations, 5.0e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 4 min |
| 45° | -4.7032 | 1.0071 | -1.04° | 102.169 | 325.62 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 90° | -3.5548 | -2.9704 | +1.60° | 101.602 | 327.86 | 4 iterations, 4.8e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 4 min |
| 135° | -0.4326 | -4.8324 | -1.91° | 102.213 | 325.33 | 4 iterations, 5.2e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 180° | 3.6414 | -3.6563 | +1.94° | 102.941 | 320.38 | 4 iterations, 3.8e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 4 min |
| 225° | 5.4307 | -0.5533 | -1.92° | 103.558 | 317.36 | 3 iterations, 2.8e-07 | L +0.000 %, R -0.001 % | 1.2 GB | 3 min |
| 270° | 4.4019 | 3.5506 | +1.62° | 104.030 | 312.37 | 4 iterations, 3.9e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 4 min |
| 315° | 1.1634 | 5.3139 | -1.41° | 103.358 | 317.66 | 4 iterations, 3.5e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 3 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 5.49 times and COS 5.47 times larger.*

## Against the expectation

The generator estimates the TX at 130 nH with the rotor away and 106 nH with it (its drop with the rotor is an upper estimate). PyPEEC gives 133.3 nH with the rotor away, and 128.6 to 128.8 nH with the rotor at 2 mm, and 126.9 to 127.2 nH with the rotor at 1.5 mm, and 122.6 to 123.2 nH with the rotor at 1 mm, and 114.8 to 116.0 nH with the rotor at 0.5 mm, and 101.6 to 104.0 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../PyPEEC%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD21_2L_tiny_TXtop_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In PyPEEC, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (109.8, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in PyPEEC](../S0_1x_OD21_2L_tiny_TXtop_pypeec_setup.webp)

*How the boards are set up in PyPEEC, drawn by [`rig_picture.py`](../PyPEEC%20Simulation/rig_picture.py) from the voxels simulation.py solves from: the rotor copper side down over the stator, each receiver opened at a left-out via (its two pads and the gap between them are the terminal, held at 0 A, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
