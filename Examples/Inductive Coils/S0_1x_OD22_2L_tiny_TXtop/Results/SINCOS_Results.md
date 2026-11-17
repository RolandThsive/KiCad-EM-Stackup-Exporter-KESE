# S0_1x_OD22_2L_tiny_TXtop: SIN and COS over the rotor's turn in PyPEEC

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 22.2 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one PyPEEC solve with its own voxels, checked by working the TX's L and R out two ways: from its voltage, and from the stored energy and the losses (the L and R checks in each table give how far apart they are; a solve is read when both are within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.41 / 1.41 nH (31 / 31 mV) | 0.3° rms, 0.5° peak |
| 1.5 mm | 8 of 8 | 2.11 / 2.12 nH (46 / 47 mV) | 0.3° rms, 0.6° peak |
| 1 mm | 8 of 8 | 3.23 / 3.24 nH (71 / 71 mV) | 0.3° rms, 0.6° peak |
| 0.5 mm | 8 of 8 | 4.92 / 4.93 nH (108 / 108 mV) | 0.5° rms, 0.8° peak |
| 0.1 mm | 8 of 8 | 6.55 / 6.55 nH (144 / 144 mV) | 1.2° rms, 1.5° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.41 nH and COS ±1.41 nH, that is ±31 and ±31 mV of EMF.*

Best sine fit: SIN amplitude 1.409 nH, offset 0.336 nH, phase -134.6°; COS amplitude 1.413 nH, offset 0.246 nH, phase 135.4°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.3° rms and 0.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.6667 | 1.2315 | +0.17° | 141.796 | 310.16 | 4 iterations, 4.9e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 7 min |
| 45° | -1.0808 | 0.2334 | +0.12° | 141.788 | 310.58 | 4 iterations, 5.9e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 7 min |
| 90° | -0.6394 | -0.7542 | +0.26° | 141.721 | 310.82 | 3 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 3.0 GB | 6 min |
| 135° | 0.3369 | -1.1701 | -0.36° | 141.808 | 310.49 | 3 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 6 min |
| 180° | 1.3358 | -0.7364 | +0.16° | 141.888 | 309.96 | 4 iterations, 5.3e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 6 min |
| 225° | 1.7524 | 0.2431 | -0.54° | 141.960 | 309.49 | 3 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 6 min |
| 270° | 1.3226 | 1.2564 | +0.19° | 141.968 | 309.17 | 3 iterations, 2.6e-07 | L +0.000 %, R +0.000 % | 3.0 GB | 6 min |
| 315° | 0.3254 | 1.6673 | +0.01° | 141.925 | 309.56 | 4 iterations, 5.1e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 6 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.11 nH and COS ±2.12 nH, that is ±46 and ±47 mV of EMF.*

Best sine fit: SIN amplitude 2.113 nH, offset 0.334 nH, phase -135.0°; COS amplitude 2.118 nH, offset 0.249 nH, phase 135.0°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.3° rms and 0.6° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.1581 | 1.7368 | +0.10° | 139.750 | 312.08 | 4 iterations, 5.4e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 9 min |
| 45° | -1.7921 | 0.2416 | +0.16° | 139.732 | 312.71 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 9 min |
| 90° | -1.1379 | -1.2396 | +0.23° | 139.627 | 313.08 | 4 iterations, 4.9e-08 | L +0.000 %, R +0.000 % | 3.0 GB | 11 min |
| 135° | 0.3212 | -1.8759 | -0.38° | 139.757 | 312.58 | 4 iterations, 5.2e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 10 min |
| 180° | 1.8241 | -1.2320 | +0.20° | 139.883 | 311.78 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 9 min |
| 225° | 2.4591 | 0.2298 | -0.57° | 139.989 | 311.13 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 2.8 GB | 9 min |
| 270° | 1.8231 | 1.7533 | +0.17° | 140.014 | 310.61 | 4 iterations, 4.7e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 9 min |
| 315° | 0.3288 | 2.3806 | +0.08° | 139.943 | 311.24 | 3 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 2.8 GB | 7 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.23 nH and COS ±3.24 nH, that is ±71 and ±71 mV of EMF.*

Best sine fit: SIN amplitude 3.230 nH, offset 0.340 nH, phase -135.8°; COS amplitude 3.236 nH, offset 0.261 nH, phase 134.2°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.3° rms and 0.6° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.3644 | 0.2635 |  | 147.877 | 305.04 | 2 iterations, 2.0e-07 | L +0.000 %, R +0.000 % | 0.9 GB | 1 min |
| 0° | -1.9057 | 2.5686 | +0.03° | 134.926 | 315.57 | 4 iterations, 5.1e-08 | L +0.000 %, R +0.000 % | 2.0 GB | 6 min |
| 45° | -2.9084 | 0.2938 | +0.19° | 134.874 | 316.66 | 4 iterations, 4.7e-08 | L +0.000 %, R +0.000 % | 2.0 GB | 6 min |
| 90° | -1.9418 | -1.9818 | +0.23° | 134.697 | 317.29 | 4 iterations, 5.0e-08 | L +0.000 %, R +0.000 % | 2.1 GB | 6 min |
| 135° | 0.2719 | -2.9868 | -0.43° | 134.905 | 316.48 | 4 iterations, 5.2e-08 | L +0.000 %, R +0.000 % | 2.0 GB | 6 min |
| 180° | 2.5899 | -2.0315 | +0.29° | 135.122 | 315.12 | 4 iterations, 4.3e-08 | L +0.000 %, R +0.000 % | 2.0 GB | 5 min |
| 225° | 3.5862 | 0.1814 | -0.63° | 135.297 | 314.12 | 3 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 2.0 GB | 4 min |
| 270° | 2.6498 | 2.5277 | +0.18° | 135.366 | 313.14 | 3 iterations, 2.6e-07 | L +0.000 %, R -0.001 % | 2.0 GB | 5 min |
| 315° | 0.3760 | 3.5141 | +0.13° | 135.240 | 314.27 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 2.0 GB | 4 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±4.92 nH and COS ±4.93 nH, that is ±108 and ±108 mV of EMF.*

Best sine fit: SIN amplitude 4.921 nH, offset 0.355 nH, phase -137.5°; COS amplitude 4.927 nH, offset 0.277 nH, phase 132.5°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.5° rms and 0.8° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -2.9722 | 3.8952 | +0.11° | 126.400 | 322.78 | 3 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |
| 45° | -4.5790 | 0.4881 | +0.03° | 126.237 | 325.01 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 2 min |
| 90° | -3.2212 | -3.0528 | +0.40° | 125.908 | 326.21 | 3 iterations, 2.4e-07 | L +0.000 %, R +0.000 % | 1.5 GB | 3 min |
| 135° | 0.0852 | -4.6571 | -0.67° | 126.274 | 324.79 | 3 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |
| 180° | 3.7054 | -3.3011 | +0.61° | 126.684 | 322.21 | 3 iterations, 2.3e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 2 min |
| 225° | 5.2764 | -0.0062 | -0.82° | 127.026 | 320.46 | 3 iterations, 2.7e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 270° | 3.9770 | 3.6476 | +0.38° | 127.206 | 318.35 | 3 iterations, 1.9e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 315° | 0.5721 | 5.2055 | -0.05° | 126.959 | 320.64 | 4 iterations, 4.4e-08 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.55 nH and COS ±6.55 nH, that is ±144 and ±144 mV of EMF.*

Best sine fit: SIN amplitude 6.549 nH, offset 0.351 nH, phase -140.2°; COS amplitude 6.549 nH, offset 0.242 nH, phase 130.0°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 1.2° rms and 1.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.8° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -3.9165 | 5.2126 | +0.77° | 112.352 | 344.88 | 3 iterations, 2.4e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 45° | -6.1771 | 0.9088 | -0.71° | 111.884 | 349.95 | 3 iterations, 2.1e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |
| 90° | -4.5798 | -4.0483 | +1.14° | 111.306 | 352.22 | 3 iterations, 2.3e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |
| 135° | -0.3950 | -6.2835 | -1.40° | 111.918 | 349.72 | 3 iterations, 2.1e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 180° | 4.6666 | -4.6639 | +1.46° | 112.675 | 344.58 | 3 iterations, 1.7e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 225° | 6.8215 | -0.5052 | -1.46° | 113.371 | 341.17 | 3 iterations, 2.1e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 270° | 5.3458 | 4.5907 | +1.17° | 113.811 | 336.22 | 3 iterations, 2.0e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 315° | 1.0443 | 6.7213 | -0.98° | 113.304 | 341.35 | 3 iterations, 2.3e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 4.65 times and COS 4.64 times larger.*

## Against the expectation

The generator estimates the TX at 144 nH with the rotor away and 116 nH with it (its drop with the rotor is an upper estimate). PyPEEC gives 147.9 nH with the rotor away, and 141.7 to 142.0 nH with the rotor at 2 mm, and 139.6 to 140.0 nH with the rotor at 1.5 mm, and 134.7 to 135.4 nH with the rotor at 1 mm, and 125.9 to 127.2 nH with the rotor at 0.5 mm, and 111.3 to 113.8 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../PyPEEC%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD22_2L_tiny_TXtop_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In PyPEEC, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (110.4, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in PyPEEC](../S0_1x_OD22_2L_tiny_TXtop_pypeec_setup.webp)

*How the boards are set up in PyPEEC, drawn by [`rig_picture.py`](../PyPEEC%20Simulation/rig_picture.py) from the voxels simulation.py solves from: the rotor copper side down over the stator, each receiver opened at a left-out via (its two pads and the gap between them are the terminal, held at 0 A, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
