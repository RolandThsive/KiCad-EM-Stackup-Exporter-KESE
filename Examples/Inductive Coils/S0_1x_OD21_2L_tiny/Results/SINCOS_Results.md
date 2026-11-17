# S0_1x_OD21_2L_tiny: SIN and COS over the rotor's turn in Elmer

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 21 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one Elmer solve with its own mesh, checked by working the TX's L and R out two ways: from its voltage, and from the field energy and the eddy power (the L and R checks in each table give how far apart they are; a solve is read when both are within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.18 / 1.18 nH (26 / 26 mV) | 0.3° rms, 0.6° peak |
| 1.5 mm | 8 of 8 | 1.80 / 1.80 nH (40 / 40 mV) | 0.2° rms, 0.4° peak |
| 1 mm | 8 of 8 | 2.81 / 2.82 nH (62 / 62 mV) | 0.1° rms, 0.3° peak |
| 0.5 mm | 8 of 8 | 4.45 / 4.46 nH (98 / 98 mV) | 0.1° rms, 0.2° peak |
| 0.1 mm | 8 of 8 | 6.22 / 6.23 nH (137 / 137 mV) | 0.5° rms, 0.6° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.18 nH and COS ±1.18 nH, that is ±26 and ±26 mV of EMF.*

Best sine fit: SIN amplitude 1.178 nH, offset 0.021 nH, phase -133.1°; COS amplitude 1.184 nH, offset -0.076 nH, phase 137.0°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.3° rms and 0.6° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.8° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.8319 | 0.7343 | -0.34° | 118.765 | 267.12 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 5 min |
| 45° | -1.1584 | -0.1285 | +0.60° | 118.755 | 267.08 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 90° | -0.7852 | -0.9389 | -0.13° | 118.850 | 266.95 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 4 min |
| 135° | 0.0600 | -1.2537 | -0.04° | 118.698 | 266.79 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 180° | 0.8761 | -0.8851 | -0.24° | 118.786 | 266.73 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 4 min |
| 225° | 1.2082 | -0.0330 | +0.11° | 118.776 | 266.71 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 4 min |
| 270° | 0.8219 | 0.7829 | -0.08° | 118.770 | 266.81 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 4 min |
| 315° | -0.0219 | 1.1158 | +0.13° | 118.739 | 266.90 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 4 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.80 nH and COS ±1.80 nH, that is ±40 and ±40 mV of EMF.*

Best sine fit: SIN amplitude 1.798 nH, offset 0.013 nH, phase -133.3°; COS amplitude 1.804 nH, offset -0.077 nH, phase 136.8°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.4° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.2841 | 1.1606 | -0.27° | 117.054 | 268.79 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 45° | -1.7916 | -0.1446 | +0.41° | 117.053 | 268.72 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 3 min |
| 90° | -1.2169 | -1.3859 | -0.06° | 117.155 | 268.55 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 135° | 0.0673 | -1.8805 | -0.01° | 117.006 | 268.38 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 180° | 1.3133 | -1.3103 | -0.12° | 117.110 | 268.25 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 225° | 1.8230 | -0.0198 | +0.07° | 117.086 | 268.28 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 3 min |
| 270° | 1.2392 | 1.2273 | -0.07° | 117.072 | 268.38 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 315° | -0.0434 | 1.7385 | +0.07° | 117.037 | 268.53 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 3 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.81 nH and COS ±2.82 nH, that is ±62 and ±62 mV of EMF.*

Best sine fit: SIN amplitude 2.812 nH, offset 0.006 nH, phase -133.9°; COS amplitude 2.820 nH, offset -0.073 nH, phase 136.2°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -2.0039 | 1.8800 | -0.25° | 114.268 | 271.37 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 3 min |
| 45° | -2.8227 | -0.1444 | +0.29° | 114.279 | 271.26 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 3 min |
| 90° | -1.9352 | -2.0972 | -0.03° | 114.393 | 271.01 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 135° | 0.0632 | -2.9016 | +0.02° | 114.244 | 270.85 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 180° | 2.0201 | -2.0174 | -0.05° | 114.376 | 270.60 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 225° | 2.8341 | -0.0141 | +0.06° | 114.330 | 270.71 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 270° | 1.9455 | 1.9451 | -0.08° | 114.308 | 270.81 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 2 min |
| 315° | -0.0524 | 2.7616 | +0.04° | 114.268 | 271.05 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±4.45 nH and COS ±4.46 nH, that is ±98 and ±98 mV of EMF.*

Best sine fit: SIN amplitude 4.452 nH, offset 0.011 nH, phase -135.3°; COS amplitude 4.462 nH, offset -0.052 nH, phase 134.8°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.2° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.0379 | -0.0544 |  | 122.616 | 263.61 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 2 min |
| 0° | -3.1068 | 3.1160 | -0.18° | 109.121 | 276.12 | direct | L -0.002 %, R +0.000 % | 13.2 GB | 2 min |
| 45° | -4.4662 | -0.0455 | +0.13° | 109.142 | 276.04 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 3 min |
| 90° | -3.1371 | -3.1870 | +0.04° | 109.278 | 275.65 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 135° | -0.0069 | -4.5309 | -0.01° | 109.120 | 275.56 | direct | L -0.002 %, R +0.000 % | 13.2 GB | 3 min |
| 180° | 3.1377 | -3.2003 | +0.08° | 109.299 | 275.12 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 3 min |
| 225° | 4.4728 | -0.0685 | +0.01° | 109.223 | 275.38 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 270° | 3.1637 | 3.0791 | -0.03° | 109.201 | 275.40 | direct | L -0.003 %, R +0.000 % | 13.2 GB | 3 min |
| 315° | 0.0323 | 4.4185 | -0.05° | 109.150 | 275.82 | direct | L -0.002 %, R +0.000 % | 13.2 GB | 3 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.22 nH and COS ±6.23 nH, that is ±137 and ±137 mV of EMF.*

Best sine fit: SIN amplitude 6.225 nH, offset 0.047 nH, phase -137.7°; COS amplitude 6.232 nH, offset -0.003 nH, phase 132.4°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.5° rms and 0.6° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -4.1752 | 4.5843 | +0.27° | 99.346 | 290.13 | direct | L -0.002 %, R +0.000 % | 12.8 GB | 2 min |
| 45° | -6.1905 | 0.3240 | -0.39° | 99.310 | 290.70 | direct | L -0.001 %, R +0.000 % | 13.0 GB | 2 min |
| 90° | -4.5128 | -4.2435 | +0.50° | 99.515 | 289.80 | direct | L -0.003 %, R +0.000 % | 13.0 GB | 2 min |
| 135° | -0.2853 | -6.2419 | -0.44° | 99.287 | 290.26 | direct | L -0.003 %, R +0.000 % | 12.8 GB | 2 min |
| 180° | 4.2877 | -4.5567 | +0.61° | 99.573 | 289.24 | direct | L -0.001 %, R +0.000 % | 12.8 GB | 2 min |
| 225° | 6.2382 | -0.3314 | -0.41° | 99.482 | 289.89 | direct | L -0.002 %, R +0.000 % | 13.0 GB | 2 min |
| 270° | 4.6233 | 4.2412 | +0.43° | 99.507 | 289.40 | direct | L -0.002 %, R +0.000 % | 13.1 GB | 2 min |
| 315° | 0.3928 | 6.1966 | -0.58° | 99.408 | 290.39 | direct | L -0.002 %, R +0.000 % | 12.8 GB | 2 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 5.28 times and COS 5.26 times larger.*

## Against the expectation

The generator estimates the TX at 132 nH with the rotor away and 109 nH with it (its drop with the rotor is an upper estimate). Elmer gives 122.6 nH with the rotor away, and 118.7 to 118.8 nH with the rotor at 2 mm, and 117.0 to 117.2 nH with the rotor at 1.5 mm, and 114.2 to 114.4 nH with the rotor at 1 mm, and 109.1 to 109.3 nH with the rotor at 0.5 mm, and 99.3 to 99.6 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../Elmer%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD21_2L_tiny_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Elmer, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (109.8, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in Elmer](../S0_1x_OD21_2L_tiny_elmer_setup.webp)

*How the boards are set up in Elmer, drawn by [`rig_picture.py`](../Elmer%20Simulation/rig_picture.py) from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened at a left-out via (its two pads and the gap between them are the terminal, held at 0 A, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
