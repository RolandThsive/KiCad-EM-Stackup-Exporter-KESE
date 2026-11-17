# S0d2_1x_OD23_2L_tiny_TX3top_Cut: SIN and COS over the rotor's turn in Elmer

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 23.4 mm across, 2 copper layers, 2 electrical periods per turn and a rotor of 2 copper sectors. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one Elmer solve with its own mesh, checked by working the TX's L and R out two ways: from its voltage, and from the field energy and the eddy power (the L and R checks in each table give how far apart they are; a solve is read when both are within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 0.5 mm | 8 of 8 | 6.97 / 6.97 nH (153 / 153 mV) | 0.4° rms, 0.6° peak |
| 0.1 mm | 8 of 8 | 9.44 / 9.43 nH (207 / 207 mV) | 0.9° rms, 1.2° peak |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.97 nH and COS ±6.97 nH, that is ±153 and ±153 mV of EMF.*

Best sine fit: SIN amplitude 6.973 nH, offset 0.111 nH, phase -138.8°; COS amplitude 6.974 nH, offset -0.009 nH, phase -48.7°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.6° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -4.5044 | -5.2330 | +0.20° | 236.467 | 474.46 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 22.5° | -6.9072 | -0.4963 | -0.24° | 236.640 | 474.13 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 45° | -5.0738 | 4.6043 | +0.39° | 236.605 | 473.38 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 4 min |
| 67.5° | -0.3681 | 6.9919 | -0.18° | 236.771 | 473.04 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 90° | 4.7333 | 5.1686 | +0.50° | 237.020 | 472.12 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 5 min |
| 112.5° | 7.0435 | 0.4873 | -0.35° | 236.741 | 472.65 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 4 min |
| 135° | 5.3211 | -4.6306 | +0.31° | 236.416 | 472.37 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 157.5° | 0.6422 | -6.9612 | -0.63° | 236.300 | 473.04 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 4 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±9.44 nH and COS ±9.43 nH, that is ±207 and ±207 mV of EMF.*

Best sine fit: SIN amplitude 9.435 nH, offset 0.140 nH, phase -140.9°; COS amplitude 9.435 nH, offset -0.049 nH, phase -50.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.9° rms and 1.2° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -5.8941 | -7.2976 | +0.67° | 213.509 | 510.00 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 4 min |
| 22.5° | -9.3383 | -1.1601 | -0.79° | 213.490 | 511.69 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 45° | -7.0421 | 5.9805 | +0.91° | 213.652 | 508.57 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 67.5° | -0.9439 | 9.4092 | -0.64° | 213.583 | 510.52 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 4 min |
| 90° | 6.2027 | 7.1152 | +1.13° | 214.192 | 507.42 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 112.5° | 9.4561 | 1.0609 | -0.90° | 213.623 | 510.02 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 135° | 7.3720 | -6.1109 | +0.86° | 213.526 | 507.14 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 157.5° | 1.3067 | -9.3909 | -1.23° | 213.134 | 510.30 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 3. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 0.5 to 0.1 mm makes SIN 1.35 times and COS 1.35 times larger.*

## Against the expectation

The generator estimates the TX at 292 nH with the rotor away and 226 nH with it (its drop with the rotor is an upper estimate). Elmer gives 236.3 to 237.0 nH with the rotor at 0.5 mm, and 213.1 to 214.2 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../Elmer%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0d2_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Elmer, SIN is opened by a cut in its top trace at (96.59, 100.5) and COS at (97.24, 97.94), the TX at its ends at (111, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in Elmer](../S0d2_1x_OD23_2L_tiny_TX3top_Cut_elmer_setup.webp)

*How the boards are set up in Elmer, drawn by [`rig_picture.py`](../Elmer%20Simulation/rig_picture.py) from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened by a 0.2 mm cut across a top trace (the two cut faces are the terminal, held at 0 A, so the voltage across the cut is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
