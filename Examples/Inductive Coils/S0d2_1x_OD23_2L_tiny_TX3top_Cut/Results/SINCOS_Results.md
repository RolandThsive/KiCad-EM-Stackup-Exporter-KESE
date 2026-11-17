# S0d2_1x_OD23_2L_tiny_TX3top_Cut: SIN and COS over the rotor's turn in Elmer

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 23.4 mm across, 2 copper layers, 2 electrical periods per turn and a rotor of 2 copper sectors. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one Elmer solve with its own mesh, checked by working the TX's L and R out two ways: from its voltage, and from the field energy and the eddy power (the L and R checks in each table give how far apart they are; a solve is read when both are within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 16 of 16 | 1.86 / 1.86 nH (41 / 41 mV) | 0.2° rms, 0.4° peak |
| 1.5 mm | 16 of 16 | 2.88 / 2.88 nH (63 / 63 mV) | 0.2° rms, 0.4° peak |
| 1 mm | 16 of 16 | 4.51 / 4.51 nH (99 / 99 mV) | 0.2° rms, 0.4° peak |
| 0.5 mm | 16 of 16 | 6.97 / 6.98 nH (153 / 153 mV) | 0.4° rms, 0.6° peak |
| 0.1 mm | 16 of 16 | 9.44 / 9.44 nH (208 / 208 mV) | 0.9° rms, 1.2° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.86 nH and COS ±1.86 nH, that is ±41 and ±41 mV of EMF.*

Best sine fit: SIN amplitude 1.856 nH, offset 0.104 nH, phase -137.0°; COS amplitude 1.857 nH, offset 0.040 nH, phase -46.8°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.4° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.2° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.1601 | -1.3136 | -0.07° | 262.661 | 449.92 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 8 min |
| 22.5° | -1.7661 | -0.0142 | +0.22° | 262.668 | 449.62 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 8 min |
| 45° | -1.2449 | 1.3038 | +0.00° | 262.689 | 449.51 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 8 min |
| 67.5° | 0.0394 | 1.8998 | -0.10° | 262.785 | 449.12 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 8 min |
| 90° | 1.3725 | 1.3898 | +0.13° | 262.820 | 449.14 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 8 min |
| 112.5° | 1.9544 | 0.1011 | +0.01° | 262.687 | 449.27 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 10 min |
| 135° | 1.4505 | -1.2205 | -0.01° | 262.418 | 449.23 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 9 min |
| 157.5° | 0.1785 | -1.8175 | -0.42° | 262.414 | 449.31 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 10 min |
| 180° | -1.1601 | -1.3136 | -0.07° | 262.661 | 449.92 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 13 min |
| 202.5° | -1.7661 | -0.0142 | +0.22° | 262.668 | 449.62 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 11 min |
| 225° | -1.2404 | 1.3110 | +0.26° | 262.589 | 449.46 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 15 min |
| 247.5° | 0.0394 | 1.8998 | -0.10° | 262.785 | 449.12 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 14 min |
| 270° | 1.3725 | 1.3898 | +0.13° | 262.820 | 449.14 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 9 min |
| 292.5° | 1.9544 | 0.1011 | +0.01° | 262.687 | 449.27 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 9 min |
| 315° | 1.4594 | -1.2395 | +0.23° | 262.599 | 449.26 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 9 min |
| 337.5° | 0.1785 | -1.8175 | -0.42° | 262.414 | 449.31 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 9 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.88 nH and COS ±2.88 nH, that is ±63 and ±63 mV of EMF.*

Best sine fit: SIN amplitude 2.882 nH, offset 0.101 nH, phase -137.0°; COS amplitude 2.884 nH, offset 0.034 nH, phase -46.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.4° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.1° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.8635 | -2.0694 | -0.00° | 257.863 | 454.22 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 7 min |
| 22.5° | -2.8031 | -0.0592 | +0.10° | 257.921 | 453.83 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 7 min |
| 45° | -1.9926 | 1.9978 | +0.09° | 257.922 | 453.63 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 7 min |
| 67.5° | -0.0002 | 2.9257 | -0.06° | 258.051 | 453.15 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 7 min |
| 90° | 2.0670 | 2.1279 | +0.16° | 258.107 | 453.06 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 7 min |
| 112.5° | 2.9758 | 0.1349 | -0.07° | 257.955 | 453.21 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 8 min |
| 135° | 2.1954 | -1.9263 | +0.02° | 257.661 | 453.23 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 7 min |
| 157.5° | 0.2188 | -2.8514 | -0.41° | 257.640 | 453.37 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 7 min |
| 180° | -1.8635 | -2.0694 | -0.00° | 257.863 | 454.22 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 9 min |
| 202.5° | -2.8031 | -0.0592 | +0.10° | 257.921 | 453.83 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 8 min |
| 225° | -1.9879 | 2.0037 | +0.25° | 257.821 | 453.58 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 8 min |
| 247.5° | -0.0002 | 2.9257 | -0.06° | 258.051 | 453.15 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 8 min |
| 270° | 2.0670 | 2.1279 | +0.16° | 258.107 | 453.06 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 8 min |
| 292.5° | 2.9758 | 0.1349 | -0.07° | 257.955 | 453.21 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 8 min |
| 315° | 2.2052 | -1.9468 | +0.19° | 257.848 | 453.27 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 8 min |
| 337.5° | 0.2188 | -2.8514 | -0.41° | 257.640 | 453.37 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 7 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±4.51 nH and COS ±4.51 nH, that is ±99 and ±99 mV of EMF.*

Best sine fit: SIN amplitude 4.511 nH, offset 0.100 nH, phase -137.5°; COS amplitude 4.514 nH, offset 0.020 nH, phase -47.4°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.4° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.1° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.0992 | 0.0334 |  | 274.189 | 437.59 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 7 min |
| 0° | -2.9508 | -3.2948 | +0.06° | 250.192 | 461.01 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 6 min |
| 22.5° | -4.4453 | -0.1723 | -0.01° | 250.317 | 460.53 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 7 min |
| 45° | -3.1955 | 3.0705 | +0.18° | 250.293 | 460.17 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |
| 67.5° | -0.0955 | 4.5515 | -0.06° | 250.456 | 459.63 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 7 min |
| 90° | 3.1518 | 3.3152 | +0.24° | 250.565 | 459.29 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 7 min |
| 112.5° | 4.5991 | 0.2231 | -0.16° | 250.375 | 459.53 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |
| 135° | 3.4049 | -3.0276 | +0.09° | 250.054 | 459.56 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 7 min |
| 157.5° | 0.3254 | -4.4929 | -0.44° | 250.003 | 459.83 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |
| 180° | -2.9508 | -3.2948 | +0.06° | 250.192 | 461.01 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 6 min |
| 202.5° | -4.4453 | -0.1723 | -0.01° | 250.317 | 460.53 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 7 min |
| 225° | -3.1905 | 3.0746 | +0.27° | 250.193 | 460.12 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |
| 247.5° | -0.0955 | 4.5515 | -0.06° | 250.456 | 459.63 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 7 min |
| 270° | 3.1518 | 3.3152 | +0.24° | 250.565 | 459.29 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |
| 292.5° | 4.5991 | 0.2231 | -0.16° | 250.375 | 459.53 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |
| 315° | 3.4157 | -3.0502 | +0.21° | 250.246 | 459.60 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |
| 337.5° | 0.3254 | -4.4929 | -0.44° | 250.003 | 459.83 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±6.97 nH and COS ±6.98 nH, that is ±153 and ±153 mV of EMF.*

Best sine fit: SIN amplitude 6.974 nH, offset 0.112 nH, phase -138.8°; COS amplitude 6.976 nH, offset -0.010 nH, phase -48.7°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.6° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.1° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -4.5044 | -5.2330 | +0.21° | 236.467 | 474.46 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 22.5° | -6.9072 | -0.4963 | -0.23° | 236.640 | 474.13 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 45° | -5.0738 | 4.6043 | +0.38° | 236.605 | 473.38 | direct | L -0.001 %, R +0.000 % | 13.3 GB | 4 min |
| 67.5° | -0.3681 | 6.9919 | -0.19° | 236.771 | 473.04 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 90° | 4.7333 | 5.1686 | +0.48° | 237.020 | 472.12 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 5 min |
| 112.5° | 7.0435 | 0.4873 | -0.37° | 236.741 | 472.65 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 4 min |
| 135° | 5.3211 | -4.6306 | +0.29° | 236.416 | 472.37 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 157.5° | 0.6422 | -6.9612 | -0.63° | 236.300 | 473.04 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 4 min |
| 180° | -4.5044 | -5.2330 | +0.21° | 236.467 | 474.46 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 202.5° | -6.9072 | -0.4963 | -0.23° | 236.640 | 474.13 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 225° | -5.0688 | 4.6058 | +0.42° | 236.509 | 473.32 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 5 min |
| 247.5° | -0.3681 | 6.9919 | -0.19° | 236.771 | 473.04 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 5 min |
| 270° | 4.7333 | 5.1686 | +0.48° | 237.020 | 472.12 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 6 min |
| 292.5° | 7.0435 | 0.4873 | -0.37° | 236.741 | 472.65 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 5 min |
| 315° | 5.3338 | -4.6563 | +0.38° | 236.618 | 472.41 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 6 min |
| 337.5° | 0.6422 | -6.9612 | -0.63° | 236.300 | 473.04 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 6 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±9.44 nH and COS ±9.44 nH, that is ±208 and ±208 mV of EMF.*

Best sine fit: SIN amplitude 9.436 nH, offset 0.141 nH, phase -140.9°; COS amplitude 9.437 nH, offset -0.051 nH, phase -50.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.9° rms and 1.2° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.1° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -5.8941 | -7.2976 | +0.68° | 213.509 | 510.00 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 4 min |
| 22.5° | -9.3383 | -1.1601 | -0.79° | 213.490 | 511.69 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 45° | -7.0421 | 5.9805 | +0.90° | 213.652 | 508.57 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 67.5° | -0.9439 | 9.4092 | -0.66° | 213.583 | 510.52 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 4 min |
| 90° | 6.2027 | 7.1152 | +1.12° | 214.192 | 507.42 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 112.5° | 9.4561 | 1.0609 | -0.92° | 213.623 | 510.02 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 135° | 7.3720 | -6.1109 | +0.85° | 213.526 | 507.14 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 157.5° | 1.3067 | -9.3909 | -1.23° | 213.134 | 510.30 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 180° | -5.8941 | -7.2976 | +0.68° | 213.509 | 510.00 | direct | L -0.003 %, R +0.000 % | 13.3 GB | 4 min |
| 202.5° | -9.3383 | -1.1601 | -0.79° | 213.490 | 511.69 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 225° | -7.0372 | 5.9793 | +0.92° | 213.565 | 508.50 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 247.5° | -0.9439 | 9.4092 | -0.66° | 213.583 | 510.52 | direct | L -0.004 %, R +0.000 % | 13.3 GB | 3 min |
| 270° | 6.2027 | 7.1152 | +1.12° | 214.192 | 507.42 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |
| 292.5° | 9.4561 | 1.0609 | -0.92° | 213.623 | 510.02 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 315° | 7.3861 | -6.1396 | +0.93° | 213.740 | 507.15 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 3 min |
| 337.5° | 1.3067 | -9.3909 | -1.23° | 213.134 | 510.30 | direct | L -0.002 %, R +0.000 % | 13.3 GB | 4 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 5.08 times and COS 5.08 times larger.*

## Against the expectation

The generator estimates the TX at 292 nH with the rotor away and 226 nH with it (its drop with the rotor is an upper estimate). Elmer gives 274.2 nH with the rotor away, and 262.4 to 262.8 nH with the rotor at 2 mm, and 257.6 to 258.1 nH with the rotor at 1.5 mm, and 250.0 to 250.6 nH with the rotor at 1 mm, and 236.3 to 237.0 nH with the rotor at 0.5 mm, and 213.1 to 214.2 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../Elmer%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0d2_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Elmer, SIN is opened by a cut in its top trace at (96.59, 100.5) and COS at (97.24, 97.94), the TX at its ends at (111, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in Elmer](../S0d2_1x_OD23_2L_tiny_TX3top_Cut_elmer_setup.webp)

*How the boards are set up in Elmer, drawn by [`rig_picture.py`](../Elmer%20Simulation/rig_picture.py) from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened by a 0.2 mm cut across a top trace (the two cut faces are the terminal, held at 0 A, so the voltage across the cut is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
