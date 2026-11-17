# S0_1x_OD21_2L_tiny_TXtop: SIN and COS over the rotor's turn in PyPEEC

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 21 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one PyPEEC solve with its own voxels, checked by working the TX's L and R out two ways: from its voltage, and from the stored energy and the losses (the L and R checks in each table give how far apart they are; a solve is read when both are within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 0.99 / 1.00 nH (22 / 22 mV) | 0.4° rms, 0.5° peak |
| 1.5 mm | 8 of 8 | 1.53 / 1.54 nH (34 / 34 mV) | 0.4° rms, 0.5° peak |
| 1 mm | 8 of 8 | 2.43 / 2.44 nH (53 / 54 mV) | 0.4° rms, 0.6° peak |
| 0.5 mm | 8 of 8 | 3.85 / 3.86 nH (85 / 85 mV) | 0.7° rms, 0.9° peak |
| 0.1 mm | 8 of 8 | 5.23 / 5.24 nH (115 / 115 mV) | 1.5° rms, 1.8° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±0.99 nH and COS ±1.00 nH, that is ±22 and ±22 mV of EMF.*

Best sine fit: SIN amplitude 0.993 nH, offset 0.128 nH, phase -135.7°; COS amplitude 0.996 nH, offset 0.021 nH, phase 134.3°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.5672 | 0.7276 | +0.26° | 129.028 | 285.86 | 2 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 2.6 GB | 5 min |
| 45° | -0.8736 | 0.0386 | -0.37° | 129.075 | 285.91 | 2 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 2.6 GB | 5 min |
| 90° | -0.5728 | -0.6772 | +0.44° | 129.065 | 285.86 | 3 iterations, 6.0e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 6 min |
| 135° | 0.1124 | -0.9812 | -0.23° | 129.096 | 285.80 | 3 iterations, 6.0e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 5 min |
| 180° | 0.8239 | -0.6826 | +0.46° | 129.117 | 285.64 | 3 iterations, 6.0e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 5 min |
| 225° | 1.1200 | 0.0022 | -0.41° | 129.108 | 285.60 | 3 iterations, 5.8e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 4 min |
| 270° | 0.8320 | 0.7200 | +0.37° | 129.080 | 285.58 | 3 iterations, 5.9e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 5 min |
| 315° | 0.1485 | 1.0176 | -0.53° | 129.051 | 285.70 | 3 iterations, 5.7e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 4 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.53 nH and COS ±1.54 nH, that is ±34 and ±34 mV of EMF.*

Best sine fit: SIN amplitude 1.533 nH, offset 0.124 nH, phase -136.1°; COS amplitude 1.537 nH, offset 0.024 nH, phase 133.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.9402 | 1.1222 | +0.25° | 127.406 | 287.39 | 3 iterations, 6.2e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |
| 45° | -1.4234 | 0.0626 | -0.37° | 127.473 | 287.44 | 3 iterations, 6.0e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |
| 90° | -0.9642 | -1.0443 | +0.44° | 127.460 | 287.36 | 3 iterations, 6.4e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 7 min |
| 135° | 0.0890 | -1.5240 | -0.24° | 127.501 | 287.29 | 3 iterations, 6.4e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 6 min |
| 180° | 1.1906 | -1.0678 | +0.48° | 127.536 | 287.05 | 3 iterations, 6.5e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |
| 225° | 1.6565 | -0.0162 | -0.43° | 127.519 | 287.02 | 3 iterations, 6.3e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 6 min |
| 270° | 1.2183 | 1.0952 | +0.37° | 127.484 | 286.98 | 3 iterations, 6.6e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |
| 315° | 0.1664 | 1.5630 | -0.51° | 127.442 | 287.16 | 2 iterations, 2.9e-07 | L +0.000 %, R +0.000 % | 2.5 GB | 5 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.43 nH and COS ±2.44 nH, that is ±53 and ±54 mV of EMF.*

Best sine fit: SIN amplitude 2.429 nH, offset 0.125 nH, phase -137.0°; COS amplitude 2.435 nH, offset 0.035 nH, phase 133.0°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.6° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.1448 | 0.0255 |  | 133.732 | 281.55 | 2 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 0.8 GB | 1 min |
| 0° | -1.5327 | 1.8010 | +0.28° | 123.338 | 290.01 | 3 iterations, 5.7e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 5 min |
| 45° | -2.3278 | 0.1394 | -0.42° | 123.437 | 290.09 | 3 iterations, 6.1e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 5 min |
| 90° | -1.6255 | -1.6279 | +0.47° | 123.418 | 289.93 | 3 iterations, 6.4e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 6 min |
| 135° | 0.0267 | -2.4186 | -0.28° | 123.473 | 289.87 | 3 iterations, 6.5e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 5 min |
| 180° | 1.7878 | -1.7198 | +0.56° | 123.535 | 289.49 | 3 iterations, 6.7e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 5 min |
| 225° | 2.5514 | -0.0721 | -0.49° | 123.505 | 289.49 | 3 iterations, 6.4e-08 | L +0.000 %, R +0.000 % | 1.7 GB | 4 min |
| 270° | 1.8859 | 1.7037 | +0.42° | 123.459 | 289.41 | 3 iterations, 6.8e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 5 min |
| 315° | 0.2342 | 2.4704 | -0.55° | 123.399 | 289.69 | 3 iterations, 6.1e-08 | L +0.000 %, R +0.000 % | 1.7 GB | 4 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.85 nH and COS ±3.86 nH, that is ±85 and ±85 mV of EMF.*

Best sine fit: SIN amplitude 3.848 nH, offset 0.146 nH, phase -139.1°; COS amplitude 3.856 nH, offset 0.071 nH, phase 130.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.7° rms and 0.9° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -2.3916 | 2.9555 | +0.50° | 116.079 | 295.21 | 3 iterations, 6.8e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 45° | -3.7307 | 0.3966 | -0.68° | 116.213 | 295.43 | 3 iterations, 6.2e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 2 min |
| 90° | -2.7127 | -2.4714 | +0.71° | 116.188 | 295.12 | 2 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 135° | -0.1665 | -3.8058 | -0.51° | 116.257 | 295.14 | 3 iterations, 7.1e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 180° | 2.6960 | -2.7896 | +0.88° | 116.370 | 294.52 | 3 iterations, 7.3e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 225° | 3.9698 | -0.2531 | -0.74° | 116.324 | 294.59 | 3 iterations, 7.4e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |
| 270° | 3.0241 | 2.6295 | +0.68° | 116.271 | 294.38 | 3 iterations, 6.2e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 315° | 0.4765 | 3.9090 | -0.83° | 116.179 | 294.84 | 3 iterations, 6.7e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±5.23 nH and COS ±5.24 nH, that is ±115 and ±115 mV of EMF.*

Best sine fit: SIN amplitude 5.229 nH, offset 0.202 nH, phase -142.6°; COS amplitude 5.236 nH, offset 0.143 nH, phase 127.5°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 1.5° rms and 1.8° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -3.0611 | 4.2185 | +1.28° | 103.982 | 312.11 | 4 iterations, 5.4e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 3 min |
| 45° | -5.0269 | 0.9784 | -1.50° | 104.084 | 313.00 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |
| 90° | -3.8359 | -3.1248 | +1.50° | 104.095 | 312.08 | 4 iterations, 6.3e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 4 min |
| 135° | -0.6101 | -5.0871 | -1.28° | 104.128 | 312.71 | 4 iterations, 5.8e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 3 min |
| 180° | 3.4948 | -3.8936 | +1.79° | 104.317 | 311.68 | 4 iterations, 4.4e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 3 min |
| 225° | 5.3352 | -0.6820 | -1.57° | 104.265 | 312.04 | 4 iterations, 4.3e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 3 min |
| 270° | 4.2768 | 3.4441 | +1.53° | 104.258 | 311.17 | 4 iterations, 3.8e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 3 min |
| 315° | 1.0459 | 5.2939 | -1.76° | 104.079 | 312.24 | 4 iterations, 4.1e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 5.27 times and COS 5.26 times larger.*

## Against the expectation

The generator estimates the TX at 130 nH with the rotor away and 106 nH with it (its drop with the rotor is an upper estimate). PyPEEC gives 133.7 nH with the rotor away, and 129.0 to 129.1 nH with the rotor at 2 mm, and 127.4 to 127.5 nH with the rotor at 1.5 mm, and 123.3 to 123.5 nH with the rotor at 1 mm, and 116.1 to 116.4 nH with the rotor at 0.5 mm, and 104.0 to 104.3 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../PyPEEC%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD21_2L_tiny_TXtop_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In PyPEEC, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (109.8, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in PyPEEC](../S0_1x_OD21_2L_tiny_TXtop_pypeec_setup.webp)

*How the boards are set up in PyPEEC, drawn by [`rig_picture.py`](../PyPEEC%20Simulation/rig_picture.py) from the voxels simulation.py solves from: the rotor copper side down over the stator, each receiver opened at a left-out via (its two pads and the gap between them are the terminal, held at 0 A, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
