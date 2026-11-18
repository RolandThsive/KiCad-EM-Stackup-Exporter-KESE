# S0_1x_OD22_2L_tiny_TXtop_Cut: SIN and COS over the rotor's turn in Palace

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 22.2 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX is driven at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF for 1 A in the TX). Each angle is one Palace solve with its own mesh, checked by working the TX's L out two ways: from its port's voltage, and from the magnetic energy in the whole field (the Checks column gives how far apart they are; a solve is read when the linear solve converged and the two are within 1 %). At the first angle of each gap SIN and COS are driven too, and the M from each back to the TX is checked against the M from the TX to it (reciprocity, in the same column). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.49 / 1.50 nH (33 / 33 mV) | 0.2° rms, 0.3° peak |
| 1.5 mm | 8 of 8 | 2.23 / 2.23 nH (49 / 49 mV) | 0.2° rms, 0.2° peak |
| 1 mm | 8 of 8 | 3.37 / 3.37 nH (74 / 74 mV) | 0.2° rms, 0.3° peak |
| 0.5 mm | 8 of 8 | 5.07 / 5.08 nH (111 / 112 mV) | 0.4° rms, 0.5° peak |
| 0.1 mm | 8 of 8 | 6.66 / 6.66 nH (146 / 147 mV) | 1.1° rms, 1.3° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.49 nH and COS ±1.50 nH, that is ±33 and ±33 mV of EMF.*

Best sine fit: SIN amplitude 1.495 nH, offset 0.083 nH, phase -134.6°; COS amplitude 1.499 nH, offset -0.004 nH, phase 135.4°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.9789 | 1.0427 | +0.07° | 132.934 | 287.39 | 124 + 165 + 125 iterations, 9e-09 | L -0.002 %, reciprocity 0.00014 % | 9.9 GB | 9 min |
| 45° | -1.4236 | -0.0115 | -0.13° | 132.962 | 287.49 | 112 iterations, 9e-09 | L -0.002 % | 7.4 GB | 3 min |
| 90° | -0.9557 | -1.0697 | +0.26° | 132.951 | 287.43 | 109 iterations, 1e-08 | L -0.002 % | 7.4 GB | 3 min |
| 135° | 0.0895 | -1.5120 | -0.14° | 132.958 | 287.32 | 116 iterations, 8e-09 | L -0.002 % | 7.4 GB | 3 min |
| 180° | 1.1444 | -1.0455 | +0.23° | 132.975 | 287.27 | 115 iterations, 8e-09 | L -0.002 % | 7.4 GB | 3 min |
| 225° | 1.5810 | 0.0017 | -0.18° | 132.937 | 287.40 | 111 iterations, 1e-08 | L -0.002 % | 7.3 GB | 3 min |
| 270° | 1.1262 | 1.0621 | +0.14° | 132.938 | 287.36 | 111 iterations, 1e-08 | L -0.002 % | 7.4 GB | 3 min |
| 315° | 0.0788 | 1.4984 | -0.25° | 132.933 | 287.51 | 116 iterations, 9e-09 | L -0.002 % | 7.4 GB | 3 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.23 nH and COS ±2.23 nH, that is ±49 and ±49 mV of EMF.*

Best sine fit: SIN amplitude 2.226 nH, offset 0.079 nH, phase -135.0°; COS amplitude 2.231 nH, offset -0.002 nH, phase 135.1°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.2° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.4913 | 1.5652 | +0.06° | 130.439 | 289.50 | 115 + 152 + 117 iterations, 1e-08 | L -0.001 %, reciprocity 8.9e-05 % | 9.0 GB | 8 min |
| 45° | -2.1662 | 0.0001 | -0.12° | 130.483 | 289.60 | 123 iterations, 9e-09 | L -0.001 % | 7.0 GB | 3 min |
| 90° | -1.4763 | -1.5766 | +0.23° | 130.475 | 289.49 | 110 iterations, 9e-09 | L -0.001 % | 6.8 GB | 3 min |
| 135° | 0.0770 | -2.2484 | -0.11° | 130.486 | 289.37 | 111 iterations, 8e-09 | L -0.001 % | 6.8 GB | 2 min |
| 180° | 1.6496 | -1.5599 | +0.24° | 130.526 | 289.24 | 117 iterations, 9e-09 | L -0.002 % | 6.9 GB | 3 min |
| 225° | 2.3105 | -0.0071 | -0.19° | 130.471 | 289.41 | 111 iterations, 1e-08 | L -0.002 % | 6.7 GB | 3 min |
| 270° | 1.6412 | 1.5755 | +0.14° | 130.468 | 289.37 | 112 iterations, 9e-09 | L -0.002 % | 6.8 GB | 3 min |
| 315° | 0.0858 | 2.2355 | -0.25° | 130.456 | 289.58 | 110 iterations, 1e-08 | L -0.002 % | 6.8 GB | 3 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.37 nH and COS ±3.37 nH, that is ±74 and ±74 mV of EMF.*

Best sine fit: SIN amplitude 3.368 nH, offset 0.079 nH, phase -135.7°; COS amplitude 3.374 nH, offset 0.007 nH, phase 134.3°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.0919 | 0.0117 |  | 138.858 | 281.67 | 104 iterations, 9e-09 | L -0.002 % | 5.8 GB | 2 min |
| 0° | -2.2651 | 2.4106 | +0.06° | 126.152 | 292.05 | 115 + 152 + 118 iterations, 1e-08 | L -0.001 %, reciprocity 6.7e-05 % | 7.8 GB | 6 min |
| 45° | -3.3193 | 0.0583 | -0.14° | 126.217 | 292.16 | 107 iterations, 1e-08 | L -0.001 % | 5.9 GB | 2 min |
| 90° | -2.3065 | -2.3417 | +0.22° | 126.215 | 291.96 | 110 iterations, 8e-09 | L -0.001 % | 5.9 GB | 2 min |
| 135° | 0.0308 | -3.3923 | -0.10° | 126.227 | 291.85 | 106 iterations, 9e-09 | L -0.001 % | 5.9 GB | 2 min |
| 180° | 2.4259 | -2.3802 | +0.28° | 126.309 | 291.60 | 115 iterations, 1e-08 | L -0.001 % | 6.0 GB | 2 min |
| 225° | 3.4540 | -0.0483 | -0.23° | 126.228 | 291.83 | 108 iterations, 9e-09 | L -0.002 % | 5.8 GB | 2 min |
| 270° | 2.4763 | 2.3629 | +0.16° | 126.222 | 291.76 | 104 iterations, 1e-08 | L -0.002 % | 5.8 GB | 2 min |
| 315° | 0.1367 | 3.3895 | -0.26° | 126.198 | 292.07 | 118 iterations, 8e-09 | L -0.001 % | 6.0 GB | 2 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±5.07 nH and COS ±5.08 nH, that is ±111 and ±112 mV of EMF.*

Best sine fit: SIN amplitude 5.069 nH, offset 0.098 nH, phase -137.4°; COS amplitude 5.075 nH, offset 0.039 nH, phase 132.6°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -3.3397 | 3.7556 | +0.21° | 118.366 | 298.32 | 105 + 139 + 107 iterations, 8e-09 | L -0.001 %, reciprocity 1.2e-05 % | 6.9 GB | 5 min |
| 45° | -5.0051 | 0.2836 | -0.34° | 118.443 | 298.57 | 100 iterations, 9e-09 | L -0.001 % | 5.2 GB | 100 s |
| 90° | -3.5923 | -3.4035 | +0.39° | 118.455 | 298.21 | 104 iterations, 9e-09 | L -0.001 % | 5.3 GB | 106 s |
| 135° | -0.1387 | -5.0656 | -0.25° | 118.457 | 298.18 | 100 iterations, 8e-09 | L -0.001 % | 5.2 GB | 104 s |
| 180° | 3.5443 | -3.6490 | +0.51° | 118.617 | 297.72 | 102 iterations, 9e-09 | L -0.001 % | 5.2 GB | 104 s |
| 225° | 5.1532 | -0.2098 | -0.40° | 118.499 | 298.03 | 102 iterations, 1e-08 | L -0.002 % | 5.2 GB | 111 s |
| 270° | 3.8082 | 3.4956 | +0.35° | 118.502 | 297.84 | 102 iterations, 1e-08 | L -0.002 % | 5.3 GB | 107 s |
| 315° | 0.3513 | 5.1033 | -0.46° | 118.456 | 298.32 | 104 iterations, 1e-08 | L -0.001 % | 5.3 GB | 109 s |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Palace solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.66 nH and COS ±6.66 nH, that is ±146 and ±147 mV of EMF.*

Best sine fit: SIN amplitude 6.661 nH, offset 0.145 nH, phase -140.2°; COS amplitude 6.665 nH, offset 0.094 nH, phase 129.8°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 1.1° rms and 1.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | Checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -4.1972 | 5.1530 | +0.87° | 103.864 | 318.08 | 108 + 141 + 110 iterations, 9e-09 | L -0.002 %, reciprocity 2.4e-05 % | 6.2 GB | 5 min |
| 45° | -6.5243 | 0.8258 | -1.04° | 103.860 | 319.11 | 101 iterations, 8e-09 | L -0.001 % | 4.7 GB | 96 s |
| 90° | -4.8772 | -4.2517 | +1.07° | 103.945 | 318.07 | 100 iterations, 7e-09 | L -0.002 % | 4.7 GB | 90 s |
| 135° | -0.5694 | -6.5760 | -0.90° | 103.871 | 318.66 | 103 iterations, 9e-09 | L -0.002 % | 4.7 GB | 98 s |
| 180° | 4.5097 | -4.9175 | +1.28° | 104.166 | 317.71 | 107 iterations, 9e-09 | L -0.002 % | 4.7 GB | 100 s |
| 225° | 6.7249 | -0.6342 | -1.10° | 104.013 | 318.34 | 104 iterations, 8e-09 | L -0.002 % | 4.7 GB | 100 s |
| 270° | 5.2014 | 4.4698 | +1.06° | 104.093 | 317.40 | 100 iterations, 9e-09 | L -0.002 % | 4.7 GB | 96 s |
| 315° | 0.8885 | 6.6859 | -1.23° | 103.963 | 318.63 | 103 iterations, 9e-09 | L -0.002 % | 4.7 GB | 100 s |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 4.46 times and COS 4.45 times larger.*

## Against the expectation

The generator estimates the TX at 144 nH with the rotor away and 116 nH with it (its drop with the rotor is an upper estimate). Palace gives 138.9 nH with the rotor away, and 132.9 to 133.0 nH with the rotor at 2 mm, and 130.4 to 130.5 nH with the rotor at 1.5 mm, and 126.2 to 126.3 nH with the rotor at 1 mm, and 118.4 to 118.6 nH with the rotor at 0.5 mm, and 103.9 to 104.2 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../Palace%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD22_2L_tiny_TXtop_Cut_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Palace, SIN is opened by a cut in its top trace at (97.16, 101.63) and COS at (98.37, 97.16), the TX at its ends at (110.4, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in Palace](../S0_1x_OD22_2L_tiny_TXtop_Cut_palace_setup.webp)

*How the boards are set up in Palace, drawn by [`rig_picture.py`](../Palace%20Simulation/rig_picture.py) from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened by a 0.2 mm cut across a top trace (its lumped port, a sheet across the cut from one cut face to the other, has 1 MΩ across it, so the voltage across the cut is the open-circuit EMF), and the TX opened between its two stacked ends, where its port drives it.*
