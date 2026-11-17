# S0_1x_OD21_2L_tiny: SIN and COS over the rotor's turn in FastHenry

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 21 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one FastHenry solve: the stator's tracks as filaments and the rotor's copper as a grid of bars turned to that angle, solved directly, so each solve is the exact answer of its model. Each is checked by reciprocity: the M from the TX to a receiver and the M from the receiver back to the TX must agree (the Reciprocity column gives how far apart they are, as a part of the larger receiver's M; a solve is read when it is within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.25 / 1.26 nH (28 / 28 mV) | 0.1° rms, 0.1° peak |
| 1.5 mm | 8 of 8 | 1.91 / 1.92 nH (42 / 42 mV) | 0.1° rms, 0.1° peak |
| 1 mm | 8 of 8 | 2.99 / 3.00 nH (66 / 66 mV) | 0.1° rms, 0.1° peak |
| 0.5 mm | 8 of 8 | 4.72 / 4.73 nH (104 / 104 mV) | 0.1° rms, 0.1° peak |
| 0.1 mm | 8 of 8 | 6.56 / 6.57 nH (144 / 144 mV) | 0.5° rms, 0.7° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.25 nH and COS ±1.26 nH, that is ±28 and ±28 mV of EMF.*

Best sine fit: SIN amplitude 1.255 nH, offset -0.004 nH, phase -133.4°; COS amplitude 1.258 nH, offset -0.006 nH, phase 136.6°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.1° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.9109 | 0.8537 | -0.01° | 131.012 | 253.32 | 6,654 | exact | 0.7 GB | 77 s |
| 45° | -1.2669 | -0.0409 | -0.06° | 131.035 | 253.29 | 6,654 | exact | 0.7 GB | 79 s |
| 90° | -0.8580 | -0.9173 | +0.13° | 131.038 | 253.28 | 6,654 | exact | 0.7 GB | 81 s |
| 135° | 0.0302 | -1.2717 | -0.08° | 131.041 | 253.28 | 6,654 | exact | 0.7 GB | 79 s |
| 180° | 0.9047 | -0.8638 | +0.12° | 131.063 | 253.25 | 6,654 | exact | 0.7 GB | 76 s |
| 225° | 1.2557 | 0.0268 | -0.11° | 131.045 | 253.28 | 6,654 | exact | 0.7 GB | 77 s |
| 270° | 0.8529 | 0.9064 | +0.11° | 131.036 | 253.28 | 6,654 | exact | 0.7 GB | 80 s |
| 315° | -0.0371 | 1.2556 | -0.10° | 131.027 | 253.29 | 6,654 | exact | 0.7 GB | 78 s |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.91 nH and COS ±1.92 nH, that is ±42 and ±42 mV of EMF.*

Best sine fit: SIN amplitude 1.913 nH, offset -0.008 nH, phase -133.6°; COS amplitude 1.918 nH, offset -0.010 nH, phase 136.4°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.1° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.3847 | 1.3053 | -0.05° | 129.243 | 254.90 | 6,654 | exact | 0.7 GB | 83 s |
| 45° | -1.9355 | -0.0580 | -0.02° | 129.276 | 254.86 | 6,654 | exact | 0.7 GB | 87 s |
| 90° | -1.3145 | -1.3918 | +0.08° | 129.278 | 254.85 | 6,654 | exact | 0.7 GB | 85 s |
| 135° | 0.0390 | -1.9402 | -0.05° | 129.282 | 254.84 | 6,654 | exact | 0.7 GB | 87 s |
| 180° | 1.3711 | -1.3205 | +0.09° | 129.315 | 254.80 | 6,654 | exact | 0.7 GB | 88 s |
| 225° | 1.9137 | 0.0360 | -0.08° | 129.289 | 254.84 | 6,654 | exact | 0.7 GB | 88 s |
| 270° | 1.3022 | 1.3754 | +0.07° | 129.279 | 254.84 | 6,654 | exact | 0.7 GB | 80 s |
| 315° | -0.0549 | 1.9153 | -0.04° | 129.268 | 254.86 | 6,654 | exact | 0.7 GB | 82 s |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.99 nH and COS ±3.00 nH, that is ±66 and ±66 mV of EMF.*

Best sine fit: SIN amplitude 2.989 nH, offset -0.010 nH, phase -134.1°; COS amplitude 2.995 nH, offset -0.011 nH, phase 135.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.1° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.0124 | 0.0069 |  | 135.275 | 248.86 | 3,467 | exact | 0.2 GB | 12 s |
| 0° | -2.1389 | 2.0654 | -0.10° | 126.342 | 257.33 | 6,654 | exact | 0.7 GB | 94 s |
| 45° | -3.0238 | -0.0585 | +0.02° | 126.389 | 257.27 | 6,654 | exact | 0.7 GB | 94 s |
| 90° | -2.0736 | -2.1468 | +0.04° | 126.392 | 257.26 | 6,654 | exact | 0.7 GB | 93 s |
| 135° | 0.0363 | -3.0285 | -0.00° | 126.396 | 257.26 | 6,654 | exact | 0.7 GB | 91 s |
| 180° | 2.1234 | -2.0793 | +0.07° | 126.447 | 257.19 | 6,654 | exact | 0.7 GB | 88 s |
| 225° | 2.9930 | 0.0332 | -0.05° | 126.409 | 257.25 | 6,654 | exact | 0.7 GB | 93 s |
| 270° | 2.0596 | 2.1306 | +0.03° | 126.398 | 257.25 | 6,654 | exact | 0.7 GB | 86 s |
| 315° | -0.0568 | 2.9967 | +0.01° | 126.385 | 257.27 | 6,654 | exact | 0.7 GB | 87 s |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±4.72 nH and COS ±4.73 nH, that is ±104 and ±104 mV of EMF.*

Best sine fit: SIN amplitude 4.720 nH, offset 0.001 nH, phase -135.4°; COS amplitude 4.728 nH, offset 0.002 nH, phase 134.6°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.1° rms and 0.1° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -3.2915 | 3.3610 | -0.08° | 120.957 | 261.74 | 6,654 | exact | 0.7 GB | 85 s |
| 45° | -4.7523 | 0.0419 | -0.04° | 121.025 | 261.66 | 6,654 | exact | 0.7 GB | 86 s |
| 90° | -3.3383 | -3.3000 | +0.07° | 121.027 | 261.65 | 6,654 | exact | 0.7 GB | 83 s |
| 135° | -0.0372 | -4.7570 | -0.03° | 121.031 | 261.65 | 6,654 | exact | 0.7 GB | 90 s |
| 180° | 3.3055 | -3.3415 | +0.15° | 121.116 | 261.53 | 6,654 | exact | 0.7 GB | 88 s |
| 225° | 4.7300 | -0.0407 | -0.08° | 121.069 | 261.63 | 6,654 | exact | 0.7 GB | 89 s |
| 270° | 3.3533 | 3.3152 | +0.06° | 121.057 | 261.63 | 6,654 | exact | 0.7 GB | 81 s |
| 315° | 0.0413 | 4.7364 | -0.05° | 121.042 | 261.65 | 6,654 | exact | 0.7 GB | 83 s |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.56 nH and COS ±6.57 nH, that is ±144 and ±144 mV of EMF.*

Best sine fit: SIN amplitude 6.561 nH, offset 0.039 nH, phase -137.8°; COS amplitude 6.567 nH, offset 0.041 nH, phase 132.2°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.5° rms and 0.7° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -4.3944 | 4.8753 | +0.34° | 110.910 | 275.02 | 6,654 | exact | 0.7 GB | 91 s |
| 45° | -6.5448 | 0.4227 | -0.53° | 110.976 | 275.07 | 6,654 | exact | 0.7 GB | 92 s |
| 90° | -4.7674 | -4.4025 | +0.51° | 110.977 | 275.07 | 6,654 | exact | 0.7 GB | 87 s |
| 135° | -0.3332 | -6.5498 | -0.45° | 110.981 | 275.07 | 6,654 | exact | 0.7 GB | 2 min |
| 180° | 4.4980 | -4.7646 | +0.68° | 111.122 | 274.86 | 6,654 | exact | 0.7 GB | 2 min |
| 225° | 6.5638 | -0.3362 | -0.51° | 111.118 | 274.94 | 6,654 | exact | 0.7 GB | 2 min |
| 270° | 4.8709 | 4.5081 | +0.52° | 111.109 | 274.95 | 6,654 | exact | 0.7 GB | 88 s |
| 315° | 0.4212 | 6.5720 | -0.56° | 111.095 | 274.94 | 6,654 | exact | 0.7 GB | 86 s |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 5.23 times and COS 5.22 times larger.*

## Against the expectation

The generator estimates the TX at 132 nH with the rotor away and 109 nH with it (its drop with the rotor is an upper estimate). FastHenry gives 135.3 nH with the rotor away, and 131.0 to 131.1 nH with the rotor at 2 mm, and 129.2 to 129.3 nH with the rotor at 1.5 mm, and 126.3 to 126.4 nH with the rotor at 1 mm, and 121.0 to 121.1 nH with the rotor at 0.5 mm, and 110.9 to 111.1 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../FastHenry%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD21_2L_tiny_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In FastHenry, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (109.8, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in FastHenry](../S0_1x_OD21_2L_tiny_fasthenry_setup.webp)

*How the boards are set up in FastHenry, drawn by [`rig_picture.py`](../FastHenry%20Simulation/rig_picture.py) from the model simulation.py solves: the stator's tracks as segments split into filaments, the rotor copper side down over the stator as a grid of bars, each receiver opened at a left-out via (the port is between where its tracks reach the via on the two layers, and the receiver is open there, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
