# S0_1x_OD22_2L_tiny_TXtop: SIN and COS over the rotor's turn in Elmer

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 22.2 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one Elmer solve with its own mesh, checked by working the TX's L and R out two ways: from its voltage, and from the field energy and the eddy power (the L and R checks in each table give how far apart they are; a solve is read when both are within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.44 / 1.44 nH (32 / 32 mV) | 0.3° rms, 0.6° peak |
| 1.5 mm | 8 of 8 | 2.15 / 2.15 nH (47 / 47 mV) | 0.2° rms, 0.5° peak |
| 1 mm | 8 of 8 | 3.26 / 3.26 nH (72 / 72 mV) | 0.2° rms, 0.4° peak |
| 0.5 mm | 8 of 8 | 4.92 / 4.92 nH (108 / 108 mV) | 0.4° rms, 0.5° peak |
| 0.1 mm | 8 of 8 | 6.47 / 6.47 nH (142 / 142 mV) | 1.1° rms, 1.3° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.44 nH and COS ±1.44 nH, that is ±32 and ±32 mV of EMF.*

Best sine fit: SIN amplitude 1.445 nH, offset 0.081 nH, phase -134.3°; COS amplitude 1.443 nH, offset -0.006 nH, phase 135.5°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.3° rms and 0.6° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.1° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.9530 | 1.0053 | -0.00° | 129.133 | 281.59 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 45° | -1.3755 | -0.0164 | -0.21° | 129.215 | 281.60 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 90° | -0.9136 | -1.0436 | +0.63° | 129.225 | 281.44 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 135° | 0.0965 | -1.4461 | +0.02° | 129.062 | 281.33 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 180° | 1.1032 | -1.0132 | -0.19° | 129.114 | 281.22 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 225° | 1.5347 | 0.0005 | -0.33° | 129.055 | 281.20 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 5 min |
| 270° | 1.0867 | 1.0271 | +0.20° | 129.213 | 281.39 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 5 min |
| 315° | 0.0685 | 1.4359 | -0.11° | 129.140 | 281.48 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.15 nH and COS ±2.15 nH, that is ±47 and ±47 mV of EMF.*

Best sine fit: SIN amplitude 2.153 nH, offset 0.076 nH, phase -134.7°; COS amplitude 2.153 nH, offset -0.004 nH, phase 135.2°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.1° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.4507 | 1.5098 | +0.03° | 126.679 | 283.64 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 45° | -2.0956 | -0.0060 | -0.17° | 126.775 | 283.62 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 4 min |
| 90° | -1.4181 | -1.5353 | +0.47° | 126.794 | 283.41 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 135° | 0.0838 | -2.1601 | -0.02° | 126.638 | 283.29 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 180° | 1.5933 | -1.5120 | -0.03° | 126.704 | 283.10 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 225° | 2.2392 | -0.0078 | -0.30° | 126.629 | 283.12 | direct | L -0.002 %, R +0.000 % | 13.2 GB | 4 min |
| 270° | 1.5841 | 1.5253 | +0.20° | 126.781 | 283.31 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 4 min |
| 315° | 0.0754 | 2.1500 | -0.19° | 126.702 | 283.47 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.26 nH and COS ±3.26 nH, that is ±72 and ±72 mV of EMF.*

Best sine fit: SIN amplitude 3.261 nH, offset 0.076 nH, phase -135.6°; COS amplitude 3.263 nH, offset 0.005 nH, phase 134.4°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.4° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -2.2026 | 2.3294 | +0.07° | 122.644 | 286.83 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 45° | -3.2155 | 0.0508 | -0.18° | 122.759 | 286.80 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 90° | -2.2247 | -2.2773 | +0.37° | 122.792 | 286.49 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 135° | 0.0375 | -3.2710 | -0.05° | 122.640 | 286.39 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 3 min |
| 180° | 2.3476 | -2.3087 | +0.12° | 122.734 | 286.07 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 225° | 3.3460 | -0.0474 | -0.29° | 122.634 | 286.16 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 3 min |
| 270° | 2.3936 | 2.2910 | +0.22° | 122.782 | 286.32 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 315° | 0.1261 | 3.2710 | -0.26° | 122.693 | 286.58 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±4.92 nH and COS ±4.92 nH, that is ±108 and ±108 mV of EMF.*

Best sine fit: SIN amplitude 4.916 nH, offset 0.094 nH, phase -137.4°; COS amplitude 4.919 nH, offset 0.037 nH, phase 132.6°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -3.2471 | 3.6396 | +0.24° | 115.050 | 293.30 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 45° | -4.8556 | 0.2746 | -0.37° | 115.177 | 293.37 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 2 min |
| 90° | -3.4779 | -3.3069 | +0.47° | 115.235 | 292.89 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 2 min |
| 135° | -0.1311 | -4.9001 | -0.23° | 115.077 | 292.90 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 180° | 3.4369 | -3.5450 | +0.42° | 115.225 | 292.36 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 225° | 4.9965 | -0.2049 | -0.44° | 115.094 | 292.54 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 270° | 3.6914 | 3.3950 | +0.40° | 115.250 | 292.57 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 315° | 0.3408 | 4.9407 | -0.50° | 115.141 | 293.02 | direct | L -0.002 %, R +0.000 % | 13.2 GB | 2 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.47 nH and COS ±6.47 nH, that is ±142 and ±142 mV of EMF.*

Best sine fit: SIN amplitude 6.470 nH, offset 0.141 nH, phase -140.3°; COS amplitude 6.471 nH, offset 0.094 nH, phase 129.7°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 1.1° rms and 1.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.0875 | 0.0058 |  | 134.585 | 280.10 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 3 min |
| 0° | -4.0790 | 5.0096 | +0.93° | 100.763 | 313.46 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 45° | -6.3369 | 0.8179 | -1.09° | 100.813 | 314.23 | direct | L -0.001 %, R +0.000 % | 13.2 GB | 2 min |
| 90° | -4.7352 | -4.1235 | +1.13° | 100.955 | 313.08 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 135° | -0.5616 | -6.3745 | -0.92° | 100.727 | 313.72 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 180° | 4.3789 | -4.7852 | +1.26° | 100.982 | 312.67 | direct | L -0.003 %, R +0.000 % | 13.2 GB | 2 min |
| 225° | 6.5291 | -0.6230 | -1.13° | 100.816 | 313.22 | direct | L -0.002 %, R +0.000 % | 13.2 GB | 3 min |
| 270° | 5.0566 | 4.3449 | +1.13° | 101.055 | 312.50 | direct | L -0.002 %, R +0.000 % | 13.2 GB | 3 min |
| 315° | 0.8786 | 6.4871 | -1.30° | 100.867 | 313.69 | direct | L -0.001 %, R +0.000 % | 13.2 GB | 2 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 4.48 times and COS 4.48 times larger.*

## Against the expectation

The generator estimates the TX at 144 nH with the rotor away and 116 nH with it (its drop with the rotor is an upper estimate). Elmer gives 134.6 nH with the rotor away, and 129.1 to 129.2 nH with the rotor at 2 mm, and 126.6 to 126.8 nH with the rotor at 1.5 mm, and 122.6 to 122.8 nH with the rotor at 1 mm, and 115.1 to 115.3 nH with the rotor at 0.5 mm, and 100.7 to 101.1 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../Elmer%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD22_2L_tiny_TXtop_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Elmer, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (110.4, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in Elmer](../S0_1x_OD22_2L_tiny_TXtop_elmer_setup.webp)

*How the boards are set up in Elmer, drawn by [`rig_picture.py`](../Elmer%20Simulation/rig_picture.py) from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened at a left-out via (its two pads and the gap between them are the terminal, held at 0 A, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
