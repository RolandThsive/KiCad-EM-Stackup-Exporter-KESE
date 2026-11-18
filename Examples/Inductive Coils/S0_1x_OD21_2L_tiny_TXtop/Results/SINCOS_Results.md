# S0_1x_OD21_2L_tiny_TXtop: SIN and COS over the rotor's turn in Palace

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 21 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX is driven at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF for 1 A in the TX). Each angle is one Palace solve with its own mesh, checked by working the TX's L out two ways: from its port's voltage, and from the magnetic energy in the whole field (the Checks column gives how far apart they are; a solve is read when the linear solve converged and the two are within 1 %). At the first angle of each gap SIN and COS are driven too, and the M from each back to the TX is checked against the M from the TX to it (reciprocity, in the same column). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.00 / 1.00 nH (22 / 22 mV) | 0.4° rms, 0.6° peak |
| 1.5 mm | 8 of 8 | 1.53 / 1.54 nH (34 / 34 mV) | 0.4° rms, 0.6° peak |
| 1 mm | 8 of 8 | 2.42 / 2.42 nH (53 / 53 mV) | 0.4° rms, 0.6° peak |
| 0.5 mm | 8 of 8 | 3.82 / 3.82 nH (84 / 84 mV) | 0.7° rms, 0.8° peak |
| 0.1 mm | 8 of 8 | 5.20 / 5.20 nH (114 / 114 mV) | 1.5° rms, 1.7° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.00 nH and COS ±1.00 nH, that is ±22 and ±22 mV of EMF.*

Best sine fit: SIN amplitude 0.995 nH, offset 0.118 nH, phase -135.5°; COS amplitude 0.998 nH, offset -0.004 nH, phase 134.6°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.6° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.5807 | 0.7007 | +0.28° | 120.471 | 266.16 | 132 + 168 + 140 iterations, 1e-08 | L -0.001 %, reciprocity 9.7e-05 % | 9.7 GB | 9 min |
| 45° | -0.8858 | 0.0091 | -0.28° | 120.535 | 266.19 | 114 iterations, 9e-09 | L -0.001 % | 7.2 GB | 3 min |
| 90° | -0.5842 | -0.7057 | +0.39° | 120.522 | 266.23 | 119 iterations, 1e-08 | L -0.001 % | 7.3 GB | 3 min |
| 135° | 0.1057 | -1.0067 | -0.22° | 120.517 | 266.12 | 124 iterations, 9e-09 | L -0.001 % | 7.4 GB | 3 min |
| 180° | 0.8164 | -0.7058 | +0.41° | 120.560 | 266.01 | 125 iterations, 1e-08 | L -0.001 % | 7.4 GB | 3 min |
| 225° | 1.1128 | -0.0193 | -0.40° | 120.535 | 266.02 | 118 iterations, 1e-08 | L -0.001 % | 7.3 GB | 3 min |
| 270° | 0.8224 | 0.7002 | +0.39° | 120.525 | 266.04 | 123 iterations, 8e-09 | L -0.001 % | 7.3 GB | 3 min |
| 315° | 0.1358 | 0.9948 | -0.57° | 120.500 | 266.30 | 125 iterations, 9e-09 | L -0.001 % | 7.4 GB | 3 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.53 nH and COS ±1.54 nH, that is ±34 and ±34 mV of EMF.*

Best sine fit: SIN amplitude 1.534 nH, offset 0.114 nH, phase -135.9°; COS amplitude 1.537 nH, offset -0.001 nH, phase 134.2°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.6° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.9549 | 1.0928 | +0.27° | 118.386 | 268.12 | 117 + 154 + 121 iterations, 9e-09 | L -0.001 %, reciprocity 0.00015 % | 8.8 GB | 7 min |
| 45° | -1.4343 | 0.0310 | -0.31° | 118.468 | 268.10 | 114 iterations, 1e-08 | L -0.001 % | 6.7 GB | 2 min |
| 90° | -0.9735 | -1.0734 | +0.42° | 118.456 | 268.11 | 113 iterations, 8e-09 | L -0.001 % | 6.7 GB | 2 min |
| 135° | 0.0838 | -1.5477 | -0.23° | 118.458 | 267.96 | 144 iterations, 9e-09 | L -0.001 % | 7.0 GB | 3 min |
| 180° | 1.1825 | -1.0883 | +0.44° | 118.522 | 267.78 | 141 iterations, 1e-08 | L -0.001 % | 7.0 GB | 3 min |
| 225° | 1.6472 | -0.0357 | -0.43° | 118.482 | 267.82 | 115 iterations, 9e-09 | L -0.001 % | 6.6 GB | 2 min |
| 270° | 1.2060 | 1.0758 | +0.39° | 118.464 | 267.86 | 121 iterations, 1e-08 | L -0.001 % | 6.8 GB | 2 min |
| 315° | 0.1517 | 1.5382 | -0.55° | 118.432 | 268.18 | 111 iterations, 9e-09 | L -0.001 % | 6.6 GB | 2 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.42 nH and COS ±2.42 nH, that is ±53 and ±53 mV of EMF.*

Best sine fit: SIN amplitude 2.420 nH, offset 0.113 nH, phase -136.8°; COS amplitude 2.424 nH, offset 0.010 nH, phase 133.2°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.6° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.1294 | 0.0037 |  | 125.067 | 261.22 | 104 iterations, 8e-09 | L -0.001 % | 5.7 GB | 111 s |
| 0° | -1.5449 | 1.7626 | +0.28° | 114.702 | 270.52 | 114 + 150 + 118 iterations, 1e-08 | L -0.001 %, reciprocity 4.7e-05 % | 7.6 GB | 6 min |
| 45° | -2.3293 | 0.1038 | -0.38° | 114.808 | 270.45 | 112 iterations, 9e-09 | L -0.001 % | 5.8 GB | 112 s |
| 90° | -1.6262 | -1.6524 | +0.47° | 114.799 | 270.40 | 118 iterations, 1e-08 | L -0.001 % | 5.9 GB | 120 s |
| 135° | 0.0243 | -2.4307 | -0.27° | 114.808 | 270.20 | 117 iterations, 8e-09 | L -0.001 % | 5.8 GB | 118 s |
| 180° | 1.7731 | -1.7292 | +0.53° | 114.910 | 269.92 | 116 iterations, 8e-09 | L -0.001 % | 5.8 GB | 115 s |
| 225° | 2.5306 | -0.0869 | -0.49° | 114.846 | 270.01 | 109 iterations, 9e-09 | L -0.001 % | 5.7 GB | 117 s |
| 270° | 1.8627 | 1.6806 | +0.43° | 114.820 | 270.06 | 119 iterations, 9e-09 | L -0.001 % | 5.9 GB | 118 s |
| 315° | 0.2140 | 2.4351 | -0.58° | 114.777 | 270.48 | 116 iterations, 9e-09 | L -0.001 % | 5.8 GB | 115 s |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.82 nH and COS ±3.82 nH, that is ±84 and ±84 mV of EMF.*

Best sine fit: SIN amplitude 3.818 nH, offset 0.132 nH, phase -138.9°; COS amplitude 3.823 nH, offset 0.049 nH, phase 131.1°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.7° rms and 0.8° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -2.3973 | 2.9003 | +0.49° | 107.862 | 276.46 | 115 + 152 + 121 iterations, 9e-09 | L -0.001 %, reciprocity 5.4e-05 % | 6.9 GB | 5 min |
| 45° | -3.7123 | 0.3528 | -0.64° | 107.988 | 276.42 | 109 iterations, 9e-09 | L -0.001 % | 5.2 GB | 97 s |
| 90° | -2.6960 | -2.4863 | +0.71° | 107.986 | 276.26 | 107 iterations, 9e-09 | L -0.001 % | 5.2 GB | 94 s |
| 135° | -0.1608 | -3.7950 | -0.49° | 107.997 | 276.08 | 106 iterations, 9e-09 | L -0.001 % | 5.2 GB | 92 s |
| 180° | 2.6700 | -2.7769 | +0.84° | 108.170 | 275.62 | 109 iterations, 9e-09 | L -0.001 % | 5.2 GB | 93 s |
| 225° | 3.9287 | -0.2571 | -0.73° | 108.073 | 275.76 | 110 iterations, 9e-09 | L -0.001 % | 5.2 GB | 2 min |
| 270° | 2.9812 | 2.5988 | +0.67° | 108.044 | 275.73 | 105 iterations, 9e-09 | L -0.001 % | 5.2 GB | 104 s |
| 315° | 0.4449 | 3.8540 | -0.83° | 107.984 | 276.33 | 118 iterations, 9e-09 | L -0.001 % | 5.3 GB | 116 s |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±5.20 nH and COS ±5.20 nH, that is ±114 and ±114 mV of EMF.*

Best sine fit: SIN amplitude 5.202 nH, offset 0.190 nH, phase -142.3°; COS amplitude 5.204 nH, offset 0.123 nH, phase 127.7°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 1.5° rms and 1.7° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -3.0750 | 4.1643 | +1.25° | 94.831 | 295.13 | 109 + 145 + 115 iterations, 1e-08 | L -0.001 %, reciprocity 6.6e-06 % | 6.1 GB | 5 min |
| 45° | -5.0106 | 0.9259 | -1.47° | 94.889 | 295.72 | 105 iterations, 1e-08 | L -0.001 % | 4.6 GB | 92 s |
| 90° | -3.8165 | -3.1460 | +1.51° | 94.953 | 294.93 | 115 iterations, 8e-09 | L -0.001 % | 4.7 GB | 99 s |
| 135° | -0.5930 | -5.0761 | -1.26° | 94.896 | 295.36 | 104 iterations, 9e-09 | L -0.001 % | 4.6 GB | 90 s |
| 180° | 3.4765 | -3.8739 | +1.74° | 95.192 | 294.48 | 108 iterations, 1e-08 | L -0.001 % | 4.6 GB | 92 s |
| 225° | 5.3020 | -0.6731 | -1.55° | 95.064 | 294.90 | 111 iterations, 8e-09 | L -0.002 % | 4.6 GB | 96 s |
| 270° | 4.2334 | 3.4213 | +1.49° | 95.093 | 294.18 | 103 iterations, 7e-09 | L -0.002 % | 4.6 GB | 90 s |
| 315° | 1.0018 | 5.2446 | -1.71° | 94.969 | 295.42 | 112 iterations, 1e-08 | L -0.002 % | 4.6 GB | 98 s |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 5.23 times and COS 5.22 times larger.*

## Against the expectation

The generator estimates the TX at 130 nH with the rotor away and 106 nH with it (its drop with the rotor is an upper estimate). Palace gives 125.1 nH with the rotor away, and 120.5 to 120.6 nH with the rotor at 2 mm, and 118.4 to 118.5 nH with the rotor at 1.5 mm, and 114.7 to 114.9 nH with the rotor at 1 mm, and 107.9 to 108.2 nH with the rotor at 0.5 mm, and 94.8 to 95.2 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../Palace%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD21_2L_tiny_TXtop_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Palace, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (109.8, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in Palace](../S0_1x_OD21_2L_tiny_TXtop_palace_setup.webp)

*How the boards are set up in Palace, drawn by [`rig_picture.py`](../Palace%20Simulation/rig_picture.py) from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened at a left-out via (its lumped port, a sheet standing between the via's two pads, has 1 MΩ across it, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where its port drives it.*
