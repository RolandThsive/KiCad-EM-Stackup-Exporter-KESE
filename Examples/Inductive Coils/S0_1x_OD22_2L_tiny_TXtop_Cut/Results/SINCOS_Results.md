# S0_1x_OD22_2L_tiny_TXtop_Cut: SIN and COS over the rotor's turn in Elmer

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 22.2 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one Elmer solve with its own mesh, checked by working the TX's L and R out two ways: from its voltage, and from the field energy and the eddy power (the L and R checks in each table give how far apart they are; a solve is read when both are within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.44 / 1.45 nH (32 / 32 mV) | 0.3° rms, 0.4° peak |
| 1.5 mm | 8 of 8 | 2.15 / 2.16 nH (47 / 47 mV) | 0.2° rms, 0.3° peak |
| 1 mm | 8 of 8 | 3.26 / 3.27 nH (72 / 72 mV) | 0.2° rms, 0.3° peak |
| 0.5 mm | 8 of 8 | 4.91 / 4.92 nH (108 / 108 mV) | 0.4° rms, 0.5° peak |
| 0.1 mm | 8 of 8 | 6.47 / 6.48 nH (142 / 142 mV) | 1.1° rms, 1.3° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.44 nH and COS ±1.45 nH, that is ±32 and ±32 mV of EMF.*

Best sine fit: SIN amplitude 1.441 nH, offset -0.080 nH, phase 45.6°; COS amplitude 1.447 nH, offset -0.012 nH, phase 135.4°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.3° rms and 0.4° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.8° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 0.9493 | 0.9981 | +0.17° | 129.175 | 281.61 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |
| 45° | 1.3757 | -0.0196 | -0.19° | 129.221 | 281.55 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |
| 90° | 0.9142 | -1.0382 | +0.30° | 129.217 | 281.49 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |
| 135° | -0.0902 | -1.4630 | -0.09° | 129.065 | 281.33 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |
| 180° | -1.1106 | -1.0257 | +0.09° | 129.077 | 281.19 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 6 min |
| 225° | -1.5237 | -0.0055 | -0.23° | 129.040 | 281.20 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 6 min |
| 270° | -1.0790 | 1.0202 | +0.35° | 129.159 | 281.37 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |
| 315° | -0.0784 | 1.4377 | -0.41° | 129.121 | 281.46 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.15 nH and COS ±2.16 nH, that is ±47 and ±47 mV of EMF.*

Best sine fit: SIN amplitude 2.149 nH, offset -0.076 nH, phase 45.2°; COS amplitude 2.156 nH, offset -0.010 nH, phase 135.1°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 1.4460 | 1.5038 | +0.12° | 126.721 | 283.66 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 45° | 2.0952 | -0.0085 | -0.17° | 126.782 | 283.58 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 4 min |
| 90° | 1.4190 | -1.5306 | +0.26° | 126.786 | 283.47 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 135° | -0.0781 | -2.1762 | -0.07° | 126.636 | 283.29 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 180° | -1.5988 | -1.5241 | +0.13° | 126.672 | 283.07 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 225° | -2.2291 | -0.0125 | -0.21° | 126.618 | 283.13 | direct | L -0.002 %, R +0.000 % | 13.2 GB | 4 min |
| 270° | -1.5772 | 1.5185 | +0.28° | 126.729 | 283.29 | direct | L -0.005 %, R +0.000 % | 13.2 GB | 4 min |
| 315° | -0.0833 | 2.1517 | -0.33° | 126.686 | 283.45 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.26 nH and COS ±3.27 nH, that is ±72 and ±72 mV of EMF.*

Best sine fit: SIN amplitude 3.257 nH, offset -0.075 nH, phase 44.4°; COS amplitude 3.267 nH, offset 0.000 nH, phase 134.3°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 2.1961 | 2.3250 | +0.09° | 122.684 | 286.86 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 45° | 3.2139 | 0.0493 | -0.18° | 122.767 | 286.76 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 3 min |
| 90° | 2.2259 | -2.2739 | +0.25° | 122.782 | 286.58 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 135° | -0.0329 | -3.2859 | -0.07° | 122.631 | 286.40 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 180° | -2.3505 | -2.3203 | +0.19° | 122.711 | 286.04 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 3 min |
| 225° | -3.3374 | -0.0506 | -0.21° | 122.630 | 286.17 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 270° | -2.3878 | 2.2846 | +0.24° | 122.732 | 286.30 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 315° | -0.1311 | 3.2723 | -0.30° | 122.680 | 286.57 | direct | L -0.001 %, R +0.000 % | 13.2 GB | 3 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±4.91 nH and COS ±4.92 nH, that is ±108 and ±108 mV of EMF.*

Best sine fit: SIN amplitude 4.912 nH, offset -0.094 nH, phase 42.6°; COS amplitude 4.923 nH, offset 0.033 nH, phase 132.6°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 3.2376 | 3.6373 | +0.23° | 115.088 | 293.34 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 3 min |
| 45° | 4.8522 | 0.2740 | -0.37° | 115.187 | 293.35 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 90° | 3.4798 | -3.3060 | +0.40° | 115.224 | 293.03 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 135° | 0.1337 | -4.9126 | -0.23° | 115.058 | 292.94 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 3 min |
| 180° | -3.4361 | -3.5564 | +0.44° | 115.216 | 292.35 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 3 min |
| 225° | -4.9903 | -0.2072 | -0.38° | 115.100 | 292.56 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 270° | -3.6877 | 3.3895 | +0.40° | 115.200 | 292.55 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 315° | -0.3417 | 4.9417 | -0.48° | 115.132 | 293.03 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 3 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.47 nH and COS ±6.48 nH, that is ±142 and ±142 mV of EMF.*

Best sine fit: SIN amplitude 6.466 nH, offset -0.142 nH, phase 39.7°; COS amplitude 6.476 nH, offset 0.090 nH, phase 129.7°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 1.1° rms and 1.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | -0.1019 | -0.0032 |  | 134.605 | 280.12 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 2 min |
| 0° | 4.0662 | 5.0085 | +0.90° | 100.796 | 313.51 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 2 min |
| 45° | 6.3311 | 0.8168 | -1.10° | 100.824 | 314.27 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 90° | 4.7396 | -4.1281 | +1.08° | 100.942 | 313.29 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 135° | 0.5599 | -6.3836 | -0.90° | 100.692 | 313.83 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 180° | -4.3758 | -4.7982 | +1.24° | 100.988 | 312.70 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 2 min |
| 225° | -6.5263 | -0.6278 | -1.10° | 100.837 | 313.25 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 270° | -5.0572 | 4.3414 | +1.12° | 101.003 | 312.47 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |
| 315° | -0.8763 | 6.4888 | -1.25° | 100.856 | 313.72 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 2 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 4.49 times and COS 4.48 times larger.*

## Against the expectation

The generator estimates the TX at 144 nH with the rotor away and 116 nH with it (its drop with the rotor is an upper estimate). Elmer gives 134.6 nH with the rotor away, and 129.0 to 129.2 nH with the rotor at 2 mm, and 126.6 to 126.8 nH with the rotor at 1.5 mm, and 122.6 to 122.8 nH with the rotor at 1 mm, and 115.1 to 115.2 nH with the rotor at 0.5 mm, and 100.7 to 101.0 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../Elmer%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD22_2L_tiny_TXtop_Cut_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Elmer, SIN is opened by a cut in its top trace at (97.16, 101.63) and COS at (98.37, 97.16), the TX at its ends at (110.4, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in Elmer](../S0_1x_OD22_2L_tiny_TXtop_Cut_elmer_setup.webp)

*How the boards are set up in Elmer, drawn by [`rig_picture.py`](../Elmer%20Simulation/rig_picture.py) from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened by a 0.2 mm cut across a top trace (the two cut faces are the terminal, held at 0 A, so the voltage across the cut is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
