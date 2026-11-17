# S0_1x_OD21_2L_tiny: SIN and COS over the rotor's turn in PyPEEC

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 21 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one PyPEEC solve with its own voxels, checked by working the TX's L and R out two ways: from its voltage, and from the stored energy and the losses (the L and R checks in each table give how far apart they are; a solve is read when both are within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.17 / 1.17 nH (26 / 26 mV) | 0.2° rms, 0.4° peak |
| 1.5 mm | 8 of 8 | 1.79 / 1.79 nH (39 / 39 mV) | 0.2° rms, 0.4° peak |
| 1 mm | 8 of 8 | 2.82 / 2.83 nH (62 / 62 mV) | 0.2° rms, 0.4° peak |
| 0.5 mm | 8 of 8 | 4.52 / 4.53 nH (99 / 100 mV) | 0.3° rms, 0.4° peak |
| 0.1 mm | 8 of 8 | 6.38 / 6.39 nH (140 / 140 mV) | 0.6° rms, 0.8° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.17 nH and COS ±1.17 nH, that is ±26 and ±26 mV of EMF.*

Best sine fit: SIN amplitude 1.167 nH, offset 0.288 nH, phase -133.2°; COS amplitude 1.171 nH, offset 0.188 nH, phase 136.8°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.4° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.5603 | 0.9842 | +0.08° | 131.928 | 292.95 | 3 iterations, 5.6e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 5 min |
| 45° | -0.8845 | 0.1464 | +0.20° | 131.917 | 293.27 | 3 iterations, 6.8e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 5 min |
| 90° | -0.5006 | -0.6599 | +0.16° | 131.868 | 293.46 | 3 iterations, 6.7e-08 | L +0.000 %, R +0.000 % | 2.7 GB | 7 min |
| 135° | 0.3205 | -0.9853 | -0.24° | 131.933 | 293.19 | 2 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 2.6 GB | 5 min |
| 180° | 1.1349 | -0.6076 | +0.05° | 131.993 | 292.77 | 3 iterations, 5.8e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 5 min |
| 225° | 1.4629 | 0.2160 | -0.44° | 132.045 | 292.43 | 3 iterations, 5.7e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 4 min |
| 270° | 1.0853 | 1.0410 | +0.06° | 132.061 | 292.17 | 3 iterations, 5.9e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 5 min |
| 315° | 0.2483 | 1.3672 | +0.13° | 132.002 | 292.51 | 3 iterations, 6.9e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 4 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.79 nH and COS ±1.79 nH, that is ±39 and ±39 mV of EMF.*

Best sine fit: SIN amplitude 1.789 nH, offset 0.281 nH, phase -133.4°; COS amplitude 1.794 nH, offset 0.186 nH, phase 136.6°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.4° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.0123 | 1.4117 | -0.00° | 130.649 | 294.53 | 3 iterations, 5.6e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 12 min |
| 45° | -1.5172 | 0.1261 | +0.28° | 130.628 | 295.01 | 3 iterations, 6.6e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |
| 90° | -0.9323 | -1.1067 | +0.11° | 130.551 | 295.31 | 2 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 2.6 GB | 8 min |
| 135° | 0.3248 | -1.6130 | -0.23° | 130.649 | 294.89 | 3 iterations, 6.7e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 9 min |
| 180° | 1.5737 | -1.0366 | +0.05° | 130.743 | 294.26 | 3 iterations, 5.7e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 8 min |
| 225° | 2.0831 | 0.2231 | -0.44° | 130.821 | 293.79 | 2 iterations, 2.8e-07 | L +0.000 %, R -0.001 % | 2.5 GB | 6 min |
| 270° | 1.5076 | 1.4874 | +0.01° | 130.853 | 293.36 | 3 iterations, 5.9e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 8 min |
| 315° | 0.2233 | 1.9947 | +0.22° | 130.763 | 293.90 | 3 iterations, 5.8e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.82 nH and COS ±2.83 nH, that is ±62 and ±62 mV of EMF.*

Best sine fit: SIN amplitude 2.822 nH, offset 0.279 nH, phase -133.9°; COS amplitude 2.829 nH, offset 0.189 nH, phase 136.0°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.4° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.3191 | 0.2086 |  | 136.096 | 288.96 | 2 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 0.8 GB | 1 min |
| 0° | -1.7382 | 2.1454 | -0.11° | 127.185 | 297.32 | 3 iterations, 5.6e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 45° | -2.5588 | 0.1191 | +0.36° | 127.136 | 298.15 | 3 iterations, 6.7e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 90° | -1.6583 | -1.8281 | +0.05° | 127.004 | 298.65 | 3 iterations, 7.3e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 135° | 0.3184 | -2.6495 | -0.23° | 127.164 | 297.97 | 3 iterations, 6.9e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 180° | 2.2983 | -1.7585 | +0.07° | 127.326 | 296.89 | 3 iterations, 6.3e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 225° | 3.1211 | 0.2192 | -0.42° | 127.456 | 296.17 | 3 iterations, 5.8e-08 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |
| 270° | 2.2357 | 2.2202 | -0.03° | 127.528 | 295.36 | 3 iterations, 6.6e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 315° | 0.2113 | 3.0408 | +0.32° | 127.376 | 296.33 | 3 iterations, 5.7e-08 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±4.52 nH and COS ±4.53 nH, that is ±99 and ±100 mV of EMF.*

Best sine fit: SIN amplitude 4.519 nH, offset 0.280 nH, phase -135.3°; COS amplitude 4.526 nH, offset 0.193 nH, phase 134.7°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.3° rms and 0.4° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -2.8785 | 3.4062 | -0.15° | 121.276 | 302.79 | 3 iterations, 6.8e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 45° | -4.2543 | 0.1882 | +0.35° | 121.139 | 304.53 | 3 iterations, 6.2e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 90° | -2.9031 | -2.9724 | +0.07° | 120.887 | 305.50 | 3 iterations, 6.6e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 4 min |
| 135° | 0.2310 | -4.3434 | -0.34° | 121.175 | 304.28 | 3 iterations, 6.7e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 180° | 3.4554 | -2.9941 | +0.23° | 121.486 | 302.17 | 3 iterations, 6.1e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 4 min |
| 225° | 4.8157 | 0.1345 | -0.45° | 121.747 | 300.92 | 3 iterations, 7.4e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 3 min |
| 270° | 3.4962 | 3.3834 | +0.01° | 121.921 | 299.17 | 3 iterations, 7.7e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 4 min |
| 315° | 0.2814 | 4.7415 | +0.28° | 121.635 | 301.14 | 2 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.38 nH and COS ±6.39 nH, that is ±140 and ±140 mV of EMF.*

Best sine fit: SIN amplitude 6.380 nH, offset 0.269 nH, phase -137.6°; COS amplitude 6.385 nH, offset 0.154 nH, phase 132.6°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.6° rms and 0.8° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.8° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -4.0635 | 4.8375 | +0.29° | 111.796 | 318.78 | 4 iterations, 6.0e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 5 min |
| 45° | -6.1067 | 0.4497 | -0.15° | 111.410 | 322.93 | 4 iterations, 5.6e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 90° | -4.3909 | -4.2040 | +0.56° | 110.952 | 324.85 | 4 iterations, 5.5e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 135° | -0.1035 | -6.2195 | -0.84° | 111.449 | 322.66 | 4 iterations, 4.8e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 180° | 4.6367 | -4.4857 | +0.80° | 112.061 | 318.20 | 4 iterations, 4.2e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 225° | 6.6123 | -0.2130 | -0.81° | 112.622 | 315.75 | 4 iterations, 3.5e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |
| 270° | 4.9763 | 4.5511 | +0.53° | 113.031 | 311.58 | 4 iterations, 5.1e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 315° | 0.5890 | 6.5153 | -0.38° | 112.474 | 316.02 | 4 iterations, 4.4e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 5.47 times and COS 5.45 times larger.*

## Against the expectation

The generator estimates the TX at 132 nH with the rotor away and 109 nH with it (its drop with the rotor is an upper estimate). PyPEEC gives 136.1 nH with the rotor away, and 131.9 to 132.1 nH with the rotor at 2 mm, and 130.6 to 130.9 nH with the rotor at 1.5 mm, and 127.0 to 127.5 nH with the rotor at 1 mm, and 120.9 to 121.9 nH with the rotor at 0.5 mm, and 111.0 to 113.0 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../PyPEEC%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD21_2L_tiny_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In PyPEEC, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (109.8, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in PyPEEC](../S0_1x_OD21_2L_tiny_pypeec_setup.webp)

*How the boards are set up in PyPEEC, drawn by [`rig_picture.py`](../PyPEEC%20Simulation/rig_picture.py) from the voxels simulation.py solves from: the rotor copper side down over the stator, each receiver opened at a left-out via (its two pads and the gap between them are the terminal, held at 0 A, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
