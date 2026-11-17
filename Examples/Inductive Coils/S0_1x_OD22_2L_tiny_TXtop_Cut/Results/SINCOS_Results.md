# S0_1x_OD22_2L_tiny_TXtop_Cut: SIN and COS over the rotor's turn in PyPEEC

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 22.2 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one PyPEEC solve with its own voxels, checked by working the TX's L and R out two ways: from its voltage, and from the stored energy and the losses (the L and R checks in each table give how far apart they are; a solve is read when both are within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.47 / 1.48 nH (32 / 32 mV) | 0.2° rms, 0.3° peak |
| 1.5 mm | 8 of 8 | 2.20 / 2.20 nH (48 / 48 mV) | 0.2° rms, 0.3° peak |
| 1 mm | 8 of 8 | 3.34 / 3.34 nH (73 / 73 mV) | 0.2° rms, 0.3° peak |
| 0.5 mm | 8 of 8 | 5.04 / 5.04 nH (111 / 111 mV) | 0.3° rms, 0.5° peak |
| 0.1 mm | 8 of 8 | 6.60 / 6.60 nH (145 / 145 mV) | 1.0° rms, 1.3° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.47 nH and COS ±1.48 nH, that is ±32 and ±32 mV of EMF.*

Best sine fit: SIN amplitude 1.473 nH, offset -0.157 nH, phase 45.4°; COS amplitude 1.475 nH, offset 0.090 nH, phase 135.3°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 0.8879 | 1.1237 | +0.04° | 142.149 | 308.28 | 3 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 5 min |
| 45° | 1.3277 | 0.0840 | -0.07° | 142.200 | 308.40 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 6 min |
| 90° | 0.8671 | -0.9547 | +0.23° | 142.182 | 308.45 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 3.0 GB | 7 min |
| 135° | -0.1627 | -1.3924 | -0.11° | 142.217 | 308.42 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 7 min |
| 180° | -1.2027 | -0.9366 | +0.22° | 142.240 | 308.16 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 7 min |
| 225° | -1.6353 | 0.0903 | -0.32° | 142.244 | 308.03 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 6 min |
| 270° | -1.1871 | 1.1384 | +0.15° | 142.207 | 307.96 | 4 iterations, 5.2e-08 | L +0.000 %, R +0.000 % | 3.0 GB | 7 min |
| 315° | -0.1522 | 1.5709 | -0.13° | 142.209 | 308.06 | 3 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 6 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.20 nH and COS ±2.20 nH, that is ±48 and ±48 mV of EMF.*

Best sine fit: SIN amplitude 2.198 nH, offset -0.156 nH, phase 45.0°; COS amplitude 2.200 nH, offset 0.095 nH, phase 134.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 1.3920 | 1.6451 | -0.00° | 140.150 | 309.95 | 3 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 8 min |
| 45° | 2.0612 | 0.0970 | -0.04° | 140.221 | 310.12 | 4 iterations, 5.3e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 8 min |
| 90° | 1.3806 | -1.4530 | +0.20° | 140.196 | 310.18 | 4 iterations, 5.8e-08 | L +0.000 %, R +0.000 % | 3.0 GB | 8 min |
| 135° | -0.1513 | -2.1194 | -0.10° | 140.240 | 310.17 | 4 iterations, 5.5e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 8 min |
| 180° | -1.7054 | -1.4452 | +0.22° | 140.280 | 309.77 | 4 iterations, 5.5e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 8 min |
| 225° | -2.3623 | 0.0817 | -0.32° | 140.281 | 309.63 | 4 iterations, 5.4e-08 | L +0.000 %, R +0.000 % | 2.8 GB | 8 min |
| 270° | -1.7017 | 1.6477 | +0.12° | 140.233 | 309.52 | 3 iterations, 2.7e-07 | L +0.000 %, R -0.001 % | 2.9 GB | 7 min |
| 315° | -0.1597 | 2.3041 | -0.08° | 140.237 | 309.67 | 3 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 2.8 GB | 7 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.34 nH and COS ±3.34 nH, that is ±73 and ±73 mV of EMF.*

Best sine fit: SIN amplitude 3.340 nH, offset -0.162 nH, phase 44.2°; COS amplitude 3.342 nH, offset 0.108 nH, phase 134.2°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | -0.1768 | 0.0992 |  | 148.210 | 303.30 | 2 iterations, 1.9e-07 | L +0.000 %, R +0.000 % | 0.9 GB | 1 min |
| 0° | 2.1561 | 2.4959 | -0.03° | 135.441 | 312.75 | 3 iterations, 2.6e-07 | L +0.000 %, R +0.000 % | 2.0 GB | 4 min |
| 45° | 3.2069 | 0.1576 | -0.04° | 135.542 | 312.99 | 3 iterations, 2.6e-07 | L +0.000 %, R +0.000 % | 2.0 GB | 4 min |
| 90° | 2.2039 | -2.2098 | +0.20° | 135.505 | 313.11 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 2.0 GB | 5 min |
| 135° | -0.1079 | -3.2569 | -0.12° | 135.562 | 313.17 | 3 iterations, 2.6e-07 | L +0.000 %, R +0.000 % | 2.0 GB | 4 min |
| 180° | -2.4855 | -2.2611 | +0.26° | 135.633 | 312.49 | 3 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 2.0 GB | 4 min |
| 225° | -3.5125 | 0.0415 | -0.33° | 135.627 | 312.35 | 3 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 1.9 GB | 4 min |
| 270° | -2.5441 | 2.4356 | +0.12° | 135.567 | 312.14 | 3 iterations, 2.4e-07 | L +0.000 %, R +0.000 % | 2.0 GB | 4 min |
| 315° | -0.2132 | 3.4619 | -0.07° | 135.573 | 312.39 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 2.0 GB | 4 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±5.04 nH and COS ±5.04 nH, that is ±111 and ±111 mV of EMF.*

Best sine fit: SIN amplitude 5.040 nH, offset -0.191 nH, phase 42.5°; COS amplitude 5.042 nH, offset 0.148 nH, phase 132.5°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.3° rms and 0.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 3.2137 | 3.8525 | +0.11° | 127.191 | 318.26 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |
| 45° | 4.8811 | 0.3886 | -0.21° | 127.323 | 318.74 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |
| 90° | 3.4779 | -3.2571 | +0.36° | 127.269 | 318.99 | 3 iterations, 2.3e-07 | L +0.000 %, R +0.000 % | 1.5 GB | 3 min |
| 135° | 0.0584 | -4.9209 | -0.31° | 127.335 | 319.27 | 3 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |
| 180° | -3.6113 | -3.5214 | +0.51° | 127.468 | 318.02 | 3 iterations, 2.4e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 2 min |
| 225° | -5.2254 | -0.1168 | -0.50° | 127.459 | 317.94 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 2 min |
| 270° | -3.8906 | 3.5721 | +0.29° | 127.389 | 317.44 | 3 iterations, 2.4e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 315° | -0.4338 | 5.1851 | -0.25° | 127.397 | 317.92 | 4 iterations, 4.5e-08 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.60 nH and COS ±6.60 nH, that is ±145 and ±145 mV of EMF.*

Best sine fit: SIN amplitude 6.600 nH, offset -0.250 nH, phase 39.7°; COS amplitude 6.600 nH, offset 0.214 nH, phase 129.7°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 1.0° rms and 1.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 4.0285 | 5.2409 | +0.74° | 113.690 | 336.35 | 3 iterations, 1.8e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 45° | 6.3563 | 0.9362 | -0.90° | 113.782 | 337.59 | 3 iterations, 2.0e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 90° | 4.7245 | -4.0659 | +1.05° | 113.747 | 337.65 | 3 iterations, 2.0e-07 | L +0.000 %, R -0.001 % | 1.5 GB | 3 min |
| 135° | 0.4854 | -6.3912 | -1.02° | 113.770 | 338.79 | 3 iterations, 2.7e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 180° | -4.5632 | -4.7533 | +1.30° | 114.003 | 336.55 | 3 iterations, 2.4e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 225° | -6.7808 | -0.5312 | -1.17° | 114.006 | 336.80 | 3 iterations, 2.0e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 270° | -5.2774 | 4.5308 | +0.99° | 113.976 | 335.43 | 3 iterations, 1.8e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 315° | -0.9753 | 6.7469 | -0.99° | 113.947 | 336.59 | 3 iterations, 2.0e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 5 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 4.48 times and COS 4.47 times larger.*

## Against the expectation

The generator estimates the TX at 144 nH with the rotor away and 116 nH with it (its drop with the rotor is an upper estimate). PyPEEC gives 148.2 nH with the rotor away, and 142.1 to 142.2 nH with the rotor at 2 mm, and 140.1 to 140.3 nH with the rotor at 1.5 mm, and 135.4 to 135.6 nH with the rotor at 1 mm, and 127.2 to 127.5 nH with the rotor at 0.5 mm, and 113.7 to 114.0 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../PyPEEC%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD22_2L_tiny_TXtop_Cut_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In PyPEEC, SIN is opened by a cut in its top trace at (97.16, 101.63) and COS at (98.37, 97.16), the TX at its ends at (110.4, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in PyPEEC](../S0_1x_OD22_2L_tiny_TXtop_Cut_pypeec_setup.webp)

*How the boards are set up in PyPEEC, drawn by [`rig_picture.py`](../PyPEEC%20Simulation/rig_picture.py) from the voxels simulation.py solves from: the rotor copper side down over the stator, each receiver opened by a 0.2 mm cut across a top trace (the two cut faces are the terminal, held at 0 A, so the voltage across the cut is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
