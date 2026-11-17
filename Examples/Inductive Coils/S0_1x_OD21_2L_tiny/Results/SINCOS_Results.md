# S0_1x_OD21_2L_tiny: SIN and COS over the rotor's turn in PyPEEC

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 21 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one PyPEEC solve with its own voxels, checked by working the TX's L and R out two ways: from its voltage, and from the stored energy and the losses (the L and R checks in each table give how far apart they are; a solve is read when both are within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.23 / 1.23 nH (27 / 27 mV) | 0.1° rms, 0.2° peak |
| 1.5 mm | 8 of 8 | 1.87 / 1.88 nH (41 / 41 mV) | 0.1° rms, 0.2° peak |
| 1 mm | 8 of 8 | 2.94 / 2.94 nH (65 / 65 mV) | 0.1° rms, 0.1° peak |
| 0.5 mm | 8 of 8 | 4.66 / 4.67 nH (102 / 103 mV) | 0.1° rms, 0.2° peak |
| 0.1 mm | 8 of 8 | 6.48 / 6.49 nH (142 / 143 mV) | 0.5° rms, 0.7° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.23 nH and COS ±1.23 nH, that is ±27 and ±27 mV of EMF.*

Best sine fit: SIN amplitude 1.230 nH, offset 0.038 nH, phase -133.4°; COS amplitude 1.233 nH, offset -0.045 nH, phase 136.6°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.2° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.8525 | 0.7988 | +0.01° | 132.296 | 290.96 | 3 iterations, 6.0e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 7 min |
| 45° | -1.2004 | -0.0783 | -0.07° | 132.329 | 291.02 | 3 iterations, 5.9e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 7 min |
| 90° | -0.7994 | -0.9376 | +0.14° | 132.320 | 290.98 | 3 iterations, 6.2e-08 | L +0.000 %, R +0.000 % | 2.7 GB | 8 min |
| 135° | 0.0727 | -1.2838 | -0.01° | 132.345 | 290.94 | 3 iterations, 6.2e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 5 min |
| 180° | 0.9291 | -0.8848 | +0.14° | 132.361 | 290.78 | 3 iterations, 6.3e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 6 min |
| 225° | 1.2712 | -0.0133 | -0.18° | 132.360 | 290.74 | 3 iterations, 6.1e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 5 min |
| 270° | 0.8773 | 0.8492 | +0.09° | 132.340 | 290.70 | 3 iterations, 6.3e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 6 min |
| 315° | 0.0054 | 1.1936 | -0.12° | 132.316 | 290.81 | 3 iterations, 6.1e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 5 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.87 nH and COS ±1.88 nH, that is ±41 and ±41 mV of EMF.*

Best sine fit: SIN amplitude 1.874 nH, offset 0.031 nH, phase -133.5°; COS amplitude 1.879 nH, offset -0.046 nH, phase 136.4°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.2° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.3195 | 1.2433 | -0.03° | 131.049 | 292.37 | 2 iterations, 2.8e-07 | L +0.000 %, R -0.001 % | 2.5 GB | 7 min |
| 45° | -1.8574 | -0.0929 | -0.02° | 131.096 | 292.45 | 3 iterations, 5.8e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |
| 90° | -1.2490 | -1.4000 | +0.09° | 131.085 | 292.38 | 3 iterations, 5.5e-08 | L +0.000 %, R +0.000 % | 2.6 GB | 8 min |
| 135° | 0.0792 | -1.9356 | +0.02° | 131.117 | 292.33 | 3 iterations, 6.0e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |
| 180° | 1.3832 | -1.3298 | +0.11° | 131.143 | 292.10 | 2 iterations, 2.8e-07 | L +0.000 %, R -0.001 % | 2.5 GB | 6 min |
| 225° | 1.9121 | -0.0032 | -0.15° | 131.139 | 292.06 | 2 iterations, 2.8e-07 | L +0.000 %, R -0.001 % | 2.5 GB | 6 min |
| 270° | 1.3145 | 1.3100 | +0.05° | 131.114 | 292.02 | 3 iterations, 5.4e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 8 min |
| 315° | -0.0142 | 1.8420 | -0.07° | 131.081 | 292.17 | 3 iterations, 6.3e-08 | L +0.000 %, R +0.000 % | 2.5 GB | 7 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.94 nH and COS ±2.94 nH, that is ±65 and ±65 mV of EMF.*

Best sine fit: SIN amplitude 2.937 nH, offset 0.026 nH, phase -134.1°; COS amplitude 2.944 nH, offset -0.044 nH, phase 135.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.1° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.0586 | -0.0339 |  | 136.456 | 286.99 | 2 iterations, 2.6e-07 | L +0.000 %, R +0.000 % | 0.8 GB | 1 min |
| 0° | -2.0689 | 1.9976 | -0.08° | 127.673 | 294.61 | 3 iterations, 6.3e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 45° | -2.9356 | -0.0904 | +0.02° | 127.740 | 294.72 | 3 iterations, 5.8e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 90° | -2.0024 | -2.1431 | +0.04° | 127.727 | 294.59 | 3 iterations, 6.3e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 135° | 0.0737 | -3.0068 | +0.05° | 127.768 | 294.55 | 3 iterations, 6.1e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 180° | 2.1236 | -2.0765 | +0.09° | 127.813 | 294.19 | 3 iterations, 5.4e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 225° | 2.9737 | -0.0037 | -0.11° | 127.802 | 294.18 | 3 iterations, 6.3e-08 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |
| 270° | 2.0594 | 2.0593 | +0.01° | 127.772 | 294.10 | 3 iterations, 5.9e-08 | L +0.000 %, R +0.000 % | 1.8 GB | 4 min |
| 315° | -0.0186 | 2.9142 | -0.02° | 127.723 | 294.34 | 3 iterations, 6.5e-08 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±4.66 nH and COS ±4.67 nH, that is ±102 and ±103 mV of EMF.*

Best sine fit: SIN amplitude 4.657 nH, offset 0.032 nH, phase -135.5°; COS amplitude 4.666 nH, offset -0.025 nH, phase 134.5°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.2° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -3.2198 | 3.2916 | -0.05° | 121.982 | 298.71 | 3 iterations, 6.2e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |
| 45° | -4.6573 | 0.0158 | -0.03° | 122.075 | 298.94 | 3 iterations, 5.8e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |
| 90° | -3.2644 | -3.2833 | +0.07° | 122.062 | 298.66 | 3 iterations, 6.3e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 135° | -0.0048 | -4.7176 | +0.00° | 122.111 | 298.69 | 3 iterations, 6.4e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |
| 180° | 3.2941 | -3.3254 | +0.17° | 122.191 | 298.11 | 3 iterations, 7.1e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |
| 225° | 4.6933 | -0.0717 | -0.12° | 122.175 | 298.20 | 3 iterations, 7.1e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |
| 270° | 3.3413 | 3.2436 | +0.05° | 122.144 | 298.00 | 3 iterations, 6.9e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |
| 315° | 0.0771 | 4.6505 | -0.09° | 122.068 | 298.41 | 3 iterations, 6.5e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.48 nH and COS ±6.49 nH, that is ±142 and ±143 mV of EMF.*

Best sine fit: SIN amplitude 6.478 nH, offset 0.068 nH, phase -137.8°; COS amplitude 6.486 nH, offset 0.022 nH, phase 132.2°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.5° rms and 0.7° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -4.3119 | 4.7967 | +0.39° | 112.958 | 311.29 | 4 iterations, 5.8e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 45° | -6.4308 | 0.4002 | -0.50° | 113.021 | 312.15 | 3 iterations, 7.5e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 90° | -4.6807 | -4.3640 | +0.51° | 113.044 | 311.38 | 3 iterations, 8.1e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 4 min |
| 135° | -0.3019 | -6.4807 | -0.44° | 113.059 | 311.89 | 4 iterations, 4.7e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 180° | 4.4709 | -4.7275 | +0.68° | 113.221 | 310.77 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 225° | 6.5039 | -0.3562 | -0.54° | 113.222 | 311.25 | 4 iterations, 4.3e-08 | L +0.000 %, R +0.000 % | 1.2 GB | 3 min |
| 270° | 4.8428 | 4.4320 | +0.51° | 113.233 | 310.53 | 4 iterations, 4.9e-08 | L +0.000 %, R +0.000 % | 1.3 GB | 3 min |
| 315° | 0.4554 | 6.4759 | -0.61° | 113.084 | 311.44 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 1.2 GB | 2 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 5.27 times and COS 5.26 times larger.*

## Against the expectation

The generator estimates the TX at 132 nH with the rotor away and 109 nH with it (its drop with the rotor is an upper estimate). PyPEEC gives 136.5 nH with the rotor away, and 132.3 to 132.4 nH with the rotor at 2 mm, and 131.0 to 131.1 nH with the rotor at 1.5 mm, and 127.7 to 127.8 nH with the rotor at 1 mm, and 122.0 to 122.2 nH with the rotor at 0.5 mm, and 113.0 to 113.2 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../PyPEEC%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD21_2L_tiny_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In PyPEEC, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (109.8, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in PyPEEC](../S0_1x_OD21_2L_tiny_pypeec_setup.webp)

*How the boards are set up in PyPEEC, drawn by [`rig_picture.py`](../PyPEEC%20Simulation/rig_picture.py) from the voxels simulation.py solves from: the rotor copper side down over the stator, each receiver opened at a left-out via (its two pads and the gap between them are the terminal, held at 0 A, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
