# S0_1x_OD22_2L_tiny_TXtop: SIN and COS over the rotor's turn in PyPEEC

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 22.2 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one PyPEEC solve with its own voxels, checked by working the TX's L and R out two ways: from its voltage, and from the stored energy and the losses (the L and R checks in each table give how far apart they are; a solve is read when both are within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.49 / 1.49 nH (33 / 33 mV) | 0.2° rms, 0.3° peak |
| 1.5 mm | 8 of 8 | 2.22 / 2.23 nH (49 / 49 mV) | 0.2° rms, 0.3° peak |
| 1 mm | 8 of 8 | 3.38 / 3.38 nH (74 / 74 mV) | 0.2° rms, 0.3° peak |
| 0.5 mm | 8 of 8 | 5.10 / 5.10 nH (112 / 112 mV) | 0.4° rms, 0.5° peak |
| 0.1 mm | 8 of 8 | 6.68 / 6.68 nH (147 / 147 mV) | 1.1° rms, 1.3° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.49 nH and COS ±1.49 nH, that is ±33 and ±33 mV of EMF.*

Best sine fit: SIN amplitude 1.490 nH, offset 0.094 nH, phase -134.7°; COS amplitude 1.494 nH, offset 0.022 nH, phase 135.3°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.9632 | 1.0682 | +0.08° | 142.152 | 308.23 | 4 iterations, 5.3e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 6 min |
| 45° | -1.4083 | 0.0192 | -0.18° | 142.204 | 308.31 | 4 iterations, 5.5e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 6 min |
| 90° | -0.9449 | -1.0382 | +0.23° | 142.188 | 308.26 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 3.0 GB | 6 min |
| 135° | 0.0988 | -1.4810 | -0.08° | 142.224 | 308.21 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 5 min |
| 180° | 1.1519 | -1.0197 | +0.25° | 142.245 | 308.03 | 4 iterations, 5.0e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 6 min |
| 225° | 1.5861 | 0.0226 | -0.24° | 142.247 | 307.93 | 4 iterations, 4.9e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 6 min |
| 270° | 1.1359 | 1.0842 | +0.21° | 142.209 | 307.92 | 4 iterations, 5.2e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 6 min |
| 315° | 0.0937 | 1.5179 | -0.27° | 142.211 | 308.01 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 5 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.22 nH and COS ±2.23 nH, that is ±49 and ±49 mV of EMF.*

Best sine fit: SIN amplitude 2.223 nH, offset 0.090 nH, phase -135.1°; COS amplitude 2.228 nH, offset 0.023 nH, phase 134.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.4755 | 1.5930 | +0.05° | 140.152 | 309.90 | 4 iterations, 5.0e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 8 min |
| 45° | -2.1520 | 0.0327 | -0.17° | 140.226 | 309.99 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 8 min |
| 90° | -1.4677 | -1.5457 | +0.22° | 140.205 | 309.91 | 3 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 3.0 GB | 8 min |
| 135° | 0.0847 | -2.2191 | -0.07° | 140.251 | 309.87 | 4 iterations, 5.0e-08 | L +0.000 %, R +0.000 % | 2.9 GB | 9 min |
| 180° | 1.6580 | -1.5376 | +0.26° | 140.285 | 309.60 | 3 iterations, 2.6e-07 | L +0.000 %, R +0.000 % | 2.9 GB | 8 min |
| 225° | 2.3167 | 0.0116 | -0.24° | 140.285 | 309.50 | 3 iterations, 2.6e-07 | L +0.000 %, R +0.000 % | 2.8 GB | 7 min |
| 270° | 1.6535 | 1.5975 | +0.20° | 140.236 | 309.47 | 3 iterations, 2.8e-07 | L +0.000 %, R -0.001 % | 2.9 GB | 8 min |
| 315° | 0.1022 | 2.2553 | -0.25° | 140.240 | 309.61 | 4 iterations, 5.3e-08 | L +0.000 %, R +0.000 % | 2.8 GB | 8 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.38 nH and COS ±3.38 nH, that is ±74 and ±74 mV of EMF.*

Best sine fit: SIN amplitude 3.377 nH, offset 0.091 nH, phase -135.8°; COS amplitude 3.383 nH, offset 0.032 nH, phase 134.1°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.1129 | 0.0295 |  | 148.213 | 303.22 | 2 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 0.9 GB | 1 min |
| 0° | -2.2545 | 2.4484 | +0.05° | 135.445 | 312.68 | 4 iterations, 4.7e-08 | L +0.000 %, R +0.000 % | 2.0 GB | 5 min |
| 45° | -3.3154 | 0.0943 | -0.19° | 135.549 | 312.82 | 4 iterations, 4.5e-08 | L +0.000 %, R +0.000 % | 2.0 GB | 5 min |
| 90° | -2.3074 | -2.3179 | +0.22° | 135.520 | 312.68 | 4 iterations, 5.2e-08 | L +0.000 %, R +0.000 % | 2.0 GB | 5 min |
| 135° | 0.0356 | -3.3753 | -0.08° | 135.580 | 312.64 | 4 iterations, 5.3e-08 | L +0.000 %, R +0.000 % | 2.0 GB | 5 min |
| 180° | 2.4423 | -2.3701 | +0.30° | 135.640 | 312.24 | 3 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 2.0 GB | 4 min |
| 225° | 3.4712 | -0.0342 | -0.26° | 135.634 | 312.14 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 1.9 GB | 4 min |
| 270° | 2.4997 | 2.3908 | +0.21° | 135.570 | 312.08 | 3 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 2.0 GB | 5 min |
| 315° | 0.1569 | 3.4185 | -0.26° | 135.577 | 312.30 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 1.9 GB | 4 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±5.10 nH and COS ±5.10 nH, that is ±112 and ±112 mV of EMF.*

Best sine fit: SIN amplitude 5.098 nH, offset 0.110 nH, phase -137.6°; COS amplitude 5.104 nH, offset 0.062 nH, phase 132.4°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -3.3380 | 3.8103 | +0.21° | 127.198 | 318.16 | 4 iterations, 4.6e-08 | L +0.000 %, R +0.000 % | 1.4 GB | 4 min |
| 45° | -5.0203 | 0.3274 | -0.39° | 127.336 | 318.47 | 3 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |
| 90° | -3.6102 | -3.3906 | +0.39° | 127.298 | 318.18 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 1.5 GB | 3 min |
| 135° | -0.1411 | -5.0698 | -0.24° | 127.371 | 318.25 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |
| 180° | 3.5729 | -3.6598 | +0.54° | 127.480 | 317.62 | 3 iterations, 2.3e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |
| 225° | 5.1888 | -0.2045 | -0.43° | 127.471 | 317.55 | 3 iterations, 2.4e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 270° | 3.8507 | 3.5337 | +0.40° | 127.393 | 317.36 | 3 iterations, 2.6e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 315° | 0.3798 | 5.1482 | -0.47° | 127.404 | 317.74 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.68 nH and COS ±6.68 nH, that is ±147 and ±147 mV of EMF.*

Best sine fit: SIN amplitude 6.680 nH, offset 0.157 nH, phase -140.4°; COS amplitude 6.684 nH, offset 0.117 nH, phase 129.6°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 1.1° rms and 1.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -4.1831 | 5.2043 | +0.88° | 113.702 | 336.20 | 3 iterations, 2.3e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 2 min |
| 45° | -6.5311 | 0.8794 | -1.11° | 113.806 | 337.20 | 4 iterations, 3.4e-08 | L +0.000 %, R +0.000 % | 1.4 GB | 3 min |
| 90° | -4.8903 | -4.2247 | +1.07° | 113.801 | 336.31 | 3 iterations, 2.5e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 135° | -0.5800 | -6.5719 | -0.90° | 113.839 | 336.99 | 3 iterations, 2.5e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 180° | 4.5282 | -4.9262 | +1.32° | 114.023 | 335.95 | 3 iterations, 2.0e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 225° | 6.7473 | -0.6359 | -1.13° | 114.028 | 336.14 | 3 iterations, 1.8e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 2 min |
| 270° | 5.2418 | 4.4982 | +1.12° | 113.981 | 335.31 | 3 iterations, 1.9e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 3 min |
| 315° | 0.9251 | 6.7163 | -1.25° | 113.960 | 336.32 | 3 iterations, 1.8e-07 | L +0.000 %, R -0.001 % | 1.4 GB | 2 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 4.48 times and COS 4.47 times larger.*

## Against the expectation

The generator estimates the TX at 144 nH with the rotor away and 116 nH with it (its drop with the rotor is an upper estimate). PyPEEC gives 148.2 nH with the rotor away, and 142.2 to 142.2 nH with the rotor at 2 mm, and 140.2 to 140.3 nH with the rotor at 1.5 mm, and 135.4 to 135.6 nH with the rotor at 1 mm, and 127.2 to 127.5 nH with the rotor at 0.5 mm, and 113.7 to 114.0 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../PyPEEC%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD22_2L_tiny_TXtop_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In PyPEEC, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (110.4, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in PyPEEC](../S0_1x_OD22_2L_tiny_TXtop_pypeec_setup.webp)

*How the boards are set up in PyPEEC, drawn by [`rig_picture.py`](../PyPEEC%20Simulation/rig_picture.py) from the voxels simulation.py solves from: the rotor copper side down over the stator, each receiver opened at a left-out via (its two pads and the gap between them are the terminal, held at 0 A, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
