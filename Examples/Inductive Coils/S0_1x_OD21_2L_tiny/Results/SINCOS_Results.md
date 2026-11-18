# S0_1x_OD21_2L_tiny: SIN and COS over the rotor's turn in Palace

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 21 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX is driven at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF for 1 A in the TX). Each angle is one Palace solve with its own mesh, checked by working the TX's L out two ways: from its port's voltage, and from the magnetic energy in the whole field (the Checks column gives how far apart they are; a solve is read when the linear solve converged and the two are within 1 %). At the first angle of each gap SIN and COS are driven too, and the M from each back to the TX is checked against the M from the TX to it (reciprocity, in the same column). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.23 / 1.23 nH (27 / 27 mV) | 0.2° rms, 0.2° peak |
| 1.5 mm | 8 of 8 | 1.88 / 1.88 nH (41 / 41 mV) | 0.1° rms, 0.2° peak |
| 1 mm | 8 of 8 | 2.93 / 2.93 nH (64 / 64 mV) | 0.1° rms, 0.1° peak |
| 0.5 mm | 8 of 8 | 4.62 / 4.62 nH (102 / 102 mV) | 0.1° rms, 0.1° peak |
| 0.1 mm | 8 of 8 | 6.44 / 6.44 nH (142 / 142 mV) | 0.5° rms, 0.6° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.23 nH and COS ±1.23 nH, that is ±27 and ±27 mV of EMF.*

Best sine fit: SIN amplitude 1.233 nH, offset 0.024 nH, phase -133.2°; COS amplitude 1.234 nH, offset -0.074 nH, phase 136.8°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.2° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.8718 | 0.7668 | +0.07° | 122.966 | 272.04 | 127 + 168 + 128 iterations, 1e-08 | L -0.001 %, reciprocity 0.0001 % | 9.3 GB | 8 min |
| 45° | -1.2172 | -0.1115 | -0.06° | 123.006 | 271.98 | 126 iterations, 8e-09 | L -0.001 % | 7.1 GB | 3 min |
| 90° | -0.8106 | -0.9705 | +0.21° | 122.990 | 271.95 | 127 iterations, 9e-09 | L -0.001 % | 7.2 GB | 3 min |
| 135° | 0.0604 | -1.3138 | -0.14° | 122.999 | 271.89 | 125 iterations, 1e-08 | L -0.001 % | 7.1 GB | 3 min |
| 180° | 0.9193 | -0.9120 | +0.10° | 122.989 | 271.97 | 126 iterations, 9e-09 | L -0.001 % | 7.1 GB | 3 min |
| 225° | 1.2636 | -0.0381 | -0.16° | 122.989 | 271.91 | 121 iterations, 9e-09 | L -0.001 % | 7.0 GB | 3 min |
| 270° | 0.8610 | 0.8253 | +0.22° | 122.950 | 271.50 | 125 iterations, 8e-09 | L -0.001 % | 7.1 GB | 3 min |
| 315° | -0.0096 | 1.1645 | -0.23° | 122.999 | 271.95 | 128 iterations, 1e-08 | L -0.001 % | 7.1 GB | 3 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.88 nH and COS ±1.88 nH, that is ±41 and ±41 mV of EMF.*

Best sine fit: SIN amplitude 1.875 nH, offset 0.017 nH, phase -133.4°; COS amplitude 1.878 nH, offset -0.075 nH, phase 136.6°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.2° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.3388 | 1.2097 | +0.00° | 121.226 | 273.74 | 121 + 163 + 123 iterations, 1e-08 | L -0.001 %, reciprocity 3.1e-05 % | 8.5 GB | 8 min |
| 45° | -1.8731 | -0.1272 | -0.01° | 121.278 | 273.66 | 121 iterations, 8e-09 | L -0.001 % | 6.5 GB | 3 min |
| 90° | -1.2583 | -1.4325 | +0.14° | 121.266 | 273.58 | 112 iterations, 1e-08 | L -0.001 % | 6.4 GB | 2 min |
| 135° | 0.0681 | -1.9639 | -0.06° | 121.278 | 273.51 | 124 iterations, 1e-08 | L -0.001 % | 6.5 GB | 2 min |
| 180° | 1.3722 | -1.3540 | +0.08° | 121.285 | 273.52 | 118 iterations, 1e-08 | L -0.001 % | 6.4 GB | 2 min |
| 225° | 1.9027 | -0.0262 | -0.13° | 121.273 | 273.51 | 129 iterations, 8e-09 | L -0.001 % | 6.6 GB | 3 min |
| 270° | 1.2961 | 1.2861 | +0.14° | 121.232 | 273.11 | 126 iterations, 9e-09 | L -0.001 % | 6.5 GB | 3 min |
| 315° | -0.0300 | 1.8112 | -0.16° | 121.273 | 273.61 | 118 iterations, 9e-09 | L -0.001 % | 6.4 GB | 2 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.93 nH and COS ±2.93 nH, that is ±64 and ±64 mV of EMF.*

Best sine fit: SIN amplitude 2.926 nH, offset 0.011 nH, phase -134.0°; COS amplitude 2.930 nH, offset -0.071 nH, phase 136.0°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.1° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.0355 | -0.0627 |  | 127.069 | 267.46 | 111 iterations, 8e-09 | L -0.001 % | 5.5 GB | 4 min |
| 0° | -2.0815 | 1.9548 | -0.06° | 118.281 | 275.99 | 120 + 160 + 122 iterations, 1e-08 | L -0.001 %, reciprocity 0.00013 % | 7.3 GB | 12 min |
| 45° | -2.9396 | -0.1261 | +0.03° | 118.348 | 275.90 | 117 iterations, 8e-09 | L -0.001 % | 5.6 GB | 4 min |
| 90° | -2.0018 | -2.1671 | +0.08° | 118.343 | 275.72 | 112 iterations, 1e-08 | L -0.001 % | 5.5 GB | 4 min |
| 135° | 0.0643 | -3.0214 | +0.01° | 118.359 | 275.66 | 118 iterations, 9e-09 | L -0.001 % | 5.6 GB | 4 min |
| 180° | 2.1033 | -2.0880 | +0.07° | 118.394 | 275.55 | 116 iterations, 8e-09 | L -0.001 % | 5.5 GB | 4 min |
| 225° | 2.9512 | -0.0232 | -0.09° | 118.363 | 275.63 | 126 iterations, 9e-09 | L -0.001 % | 5.6 GB | 4 min |
| 270° | 2.0299 | 2.0287 | +0.06° | 118.321 | 275.23 | 118 iterations, 9e-09 | L -0.001 % | 5.6 GB | 4 min |
| 315° | -0.0365 | 2.8711 | -0.10° | 118.351 | 275.83 | 120 iterations, 8e-09 | L -0.001 % | 5.6 GB | 4 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±4.62 nH and COS ±4.62 nH, that is ±102 and ±102 mV of EMF.*

Best sine fit: SIN amplitude 4.618 nH, offset 0.017 nH, phase -135.3°; COS amplitude 4.624 nH, offset -0.050 nH, phase 134.7°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.1° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -3.2172 | 3.2284 | -0.05° | 112.985 | 280.61 | 111 + 146 + 113 iterations, 1e-08 | L -0.001 %, reciprocity 2.3e-05 % | 6.5 GB | 10 min |
| 45° | -4.6347 | -0.0246 | -0.01° | 113.065 | 280.59 | 107 iterations, 9e-09 | L -0.001 % | 4.9 GB | 3 min |
| 90° | -3.2419 | -3.2899 | +0.09° | 113.078 | 280.25 | 107 iterations, 1e-08 | L -0.001 % | 4.9 GB | 3 min |
| 135° | -0.0082 | -4.7030 | -0.01° | 113.087 | 280.26 | 112 iterations, 9e-09 | L -0.001 % | 5.0 GB | 4 min |
| 180° | 3.2561 | -3.3107 | +0.15° | 113.176 | 279.94 | 107 iterations, 1e-08 | L -0.001 % | 4.9 GB | 3 min |
| 225° | 4.6436 | -0.0831 | -0.10° | 113.119 | 280.17 | 105 iterations, 1e-08 | L -0.001 % | 4.9 GB | 3 min |
| 270° | 3.2885 | 3.1981 | +0.07° | 113.086 | 279.71 | 105 iterations, 9e-09 | L -0.001 % | 4.9 GB | 3 min |
| 315° | 0.0531 | 4.5809 | -0.14° | 113.095 | 280.47 | 104 iterations, 1e-08 | L -0.001 % | 4.9 GB | 3 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.44 nH and COS ±6.44 nH, that is ±142 and ±142 mV of EMF.*

Best sine fit: SIN amplitude 6.437 nH, offset 0.054 nH, phase -137.7°; COS amplitude 6.440 nH, offset -0.002 nH, phase 132.4°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.5° rms and 0.6° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -4.3132 | 4.7302 | +0.37° | 103.011 | 294.50 | 113 + 145 + 112 iterations, 9e-09 | L -0.001 %, reciprocity 3.4e-05 % | 5.9 GB | 5 min |
| 45° | -6.4048 | 0.3503 | -0.47° | 103.025 | 295.19 | 101 iterations, 9e-09 | L -0.001 % | 4.4 GB | 92 s |
| 90° | -4.6527 | -4.3729 | +0.52° | 103.105 | 294.28 | 106 iterations, 1e-08 | L -0.001 % | 4.5 GB | 96 s |
| 135° | -0.2936 | -6.4603 | -0.44° | 103.055 | 294.82 | 109 iterations, 9e-09 | L -0.001 % | 4.5 GB | 101 s |
| 180° | 4.4369 | -4.7031 | +0.65° | 103.258 | 293.88 | 109 iterations, 9e-09 | L -0.001 % | 4.5 GB | 102 s |
| 225° | 6.4560 | -0.3544 | -0.51° | 103.190 | 294.54 | 105 iterations, 9e-09 | L -0.001 % | 4.4 GB | 99 s |
| 270° | 4.7847 | 4.3908 | +0.51° | 103.219 | 293.57 | 105 iterations, 8e-09 | L -0.001 % | 4.4 GB | 96 s |
| 315° | 0.4201 | 6.4072 | -0.62° | 103.164 | 294.92 | 105 iterations, 8e-09 | L -0.001 % | 4.4 GB | 92 s |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 5.22 times and COS 5.22 times larger.*

## Against the expectation

The generator estimates the TX at 132 nH with the rotor away and 109 nH with it (its drop with the rotor is an upper estimate). Palace gives 127.1 nH with the rotor away, and 122.9 to 123.0 nH with the rotor at 2 mm, and 121.2 to 121.3 nH with the rotor at 1.5 mm, and 118.3 to 118.4 nH with the rotor at 1 mm, and 113.0 to 113.2 nH with the rotor at 0.5 mm, and 103.0 to 103.3 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../Palace%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD21_2L_tiny_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Palace, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (109.8, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in Palace](../S0_1x_OD21_2L_tiny_palace_setup.webp)

*How the boards are set up in Palace, drawn by [`rig_picture.py`](../Palace%20Simulation/rig_picture.py) from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened at a left-out via (its lumped port, a sheet standing between the via's two pads, has 1 MΩ across it, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where its port drives it.*
