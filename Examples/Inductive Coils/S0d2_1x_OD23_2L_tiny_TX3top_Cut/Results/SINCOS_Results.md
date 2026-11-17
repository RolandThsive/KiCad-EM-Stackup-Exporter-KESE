# S0d2_1x_OD23_2L_tiny_TX3top_Cut: SIN and COS over the rotor's turn in PyPEEC

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 23.4 mm across, 2 copper layers, 2 electrical periods per turn and a rotor of 2 copper sectors. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one PyPEEC solve with its own voxels, checked by working the TX's L and R out two ways: from its voltage, and from the stored energy and the losses (the L and R checks in each table give how far apart they are; a solve is read when both are within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 16 of 16 | 1.89 / 1.90 nH (42 / 42 mV) | 0.2° rms, 0.3° peak |
| 1.5 mm | 16 of 16 | 2.94 / 2.95 nH (65 / 65 mV) | 0.2° rms, 0.4° peak |
| 1 mm | 16 of 16 | 4.61 / 4.63 nH (101 / 102 mV) | 0.2° rms, 0.4° peak |
| 0.5 mm | 16 of 16 | 7.14 / 7.16 nH (157 / 157 mV) | 0.4° rms, 0.7° peak |
| 0.1 mm | 16 of 16 | 9.60 / 9.62 nH (211 / 212 mV) | 0.9° rms, 1.3° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.89 nH and COS ±1.90 nH, that is ±42 and ±42 mV of EMF.*

Best sine fit: SIN amplitude 1.891 nH, offset 0.020 nH, phase -137.2°; COS amplitude 1.898 nH, offset 0.130 nH, phase -47.2°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.3° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.2652 | -1.2620 | +0.04° | 284.094 | 486.56 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 3.5 GB | 7 min |
| 22.5° | -1.8826 | 0.0531 | -0.09° | 284.186 | 486.75 | 4 iterations, 4.6e-08 | L +0.000 %, R +0.000 % | 3.4 GB | 9 min |
| 45° | -1.3578 | 1.4199 | +0.22° | 284.269 | 486.36 | 4 iterations, 5.2e-08 | L +0.000 %, R +0.000 % | 3.4 GB | 11 min |
| 67.5° | -0.0523 | 2.0338 | +0.02° | 284.273 | 486.08 | 4 iterations, 5.3e-08 | L +0.000 %, R +0.000 % | 3.4 GB | 9 min |
| 90° | 1.3040 | 1.5160 | +0.12° | 284.292 | 485.62 | 4 iterations, 4.2e-08 | L +0.000 %, R +0.000 % | 3.5 GB | 7 min |
| 112.5° | 1.9069 | 0.2015 | +0.05° | 284.300 | 485.69 | 3 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 3.3 GB | 6 min |
| 135° | 1.4051 | -1.1558 | -0.01° | 284.277 | 485.78 | 3 iterations, 2.4e-07 | L +0.000 %, R +0.000 % | 3.3 GB | 8 min |
| 157.5° | 0.1050 | -1.7674 | -0.35° | 284.171 | 486.26 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 3.3 GB | 6 min |
| 180° | -1.2652 | -1.2620 | +0.04° | 284.094 | 486.56 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 3.5 GB | 6 min |
| 202.5° | -1.8826 | 0.0531 | -0.09° | 284.186 | 486.75 | 4 iterations, 4.6e-08 | L +0.000 %, R +0.000 % | 3.4 GB | 8 min |
| 225° | -1.3578 | 1.4199 | +0.22° | 284.269 | 486.36 | 4 iterations, 5.2e-08 | L +0.000 %, R +0.000 % | 3.4 GB | 10 min |
| 247.5° | -0.0523 | 2.0338 | +0.02° | 284.273 | 486.08 | 4 iterations, 5.3e-08 | L +0.000 %, R +0.000 % | 3.4 GB | 9 min |
| 270° | 1.3040 | 1.5160 | +0.12° | 284.292 | 485.62 | 4 iterations, 4.2e-08 | L +0.000 %, R +0.000 % | 3.5 GB | 8 min |
| 292.5° | 1.9069 | 0.2015 | +0.05° | 284.300 | 485.69 | 3 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 3.3 GB | 6 min |
| 315° | 1.4051 | -1.1558 | -0.01° | 284.277 | 485.78 | 3 iterations, 2.4e-07 | L +0.000 %, R +0.000 % | 3.3 GB | 7 min |
| 337.5° | 0.1050 | -1.7674 | -0.35° | 284.171 | 486.26 | 3 iterations, 2.8e-07 | L +0.000 %, R +0.000 % | 3.3 GB | 5 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.94 nH and COS ±2.95 nH, that is ±65 and ±65 mV of EMF.*

Best sine fit: SIN amplitude 2.940 nH, offset 0.016 nH, phase -137.2°; COS amplitude 2.950 nH, offset 0.127 nH, phase -47.2°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.4° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.9817 | -2.0339 | +0.05° | 280.112 | 490.17 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 3.4 GB | 9 min |
| 22.5° | -2.9471 | 0.0064 | -0.12° | 280.239 | 490.45 | 4 iterations, 4.5e-08 | L +0.000 %, R +0.000 % | 3.3 GB | 12 min |
| 45° | -2.1229 | 2.1303 | +0.24° | 280.359 | 489.83 | 4 iterations, 4.6e-08 | L +0.000 %, R +0.000 % | 3.3 GB | 14 min |
| 67.5° | -0.0971 | 3.0910 | +0.03° | 280.356 | 489.45 | 4 iterations, 4.4e-08 | L +0.000 %, R +0.000 % | 3.3 GB | 10 min |
| 90° | 2.0107 | 2.2779 | +0.16° | 280.405 | 488.76 | 4 iterations, 4.2e-08 | L +0.000 %, R +0.000 % | 3.4 GB | 9 min |
| 112.5° | 2.9491 | 0.2404 | +0.01° | 280.400 | 488.92 | 4 iterations, 4.0e-08 | L +0.000 %, R +0.000 % | 3.2 GB | 9 min |
| 135° | 2.1650 | -1.8700 | +0.01° | 280.377 | 489.05 | 4 iterations, 3.9e-08 | L +0.000 %, R +0.000 % | 3.2 GB | 10 min |
| 157.5° | 0.1482 | -2.8227 | -0.37° | 280.221 | 489.77 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 3.2 GB | 8 min |
| 180° | -1.9817 | -2.0339 | +0.05° | 280.112 | 490.17 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 3.4 GB | 11 min |
| 202.5° | -2.9471 | 0.0064 | -0.12° | 280.239 | 490.45 | 4 iterations, 4.5e-08 | L +0.000 %, R +0.000 % | 3.3 GB | 14 min |
| 225° | -2.1229 | 2.1303 | +0.24° | 280.359 | 489.83 | 4 iterations, 4.6e-08 | L +0.000 %, R +0.000 % | 3.3 GB | 16 min |
| 247.5° | -0.0971 | 3.0910 | +0.03° | 280.356 | 489.45 | 4 iterations, 4.4e-08 | L +0.000 %, R +0.000 % | 3.3 GB | 14 min |
| 270° | 2.0107 | 2.2779 | +0.16° | 280.405 | 488.76 | 4 iterations, 4.2e-08 | L +0.000 %, R +0.000 % | 3.4 GB | 11 min |
| 292.5° | 2.9491 | 0.2404 | +0.01° | 280.400 | 488.92 | 4 iterations, 4.0e-08 | L +0.000 %, R +0.000 % | 3.2 GB | 10 min |
| 315° | 2.1650 | -1.8700 | +0.01° | 280.377 | 489.05 | 4 iterations, 3.9e-08 | L +0.000 %, R +0.000 % | 3.2 GB | 15 min |
| 337.5° | 0.1482 | -2.8227 | -0.37° | 280.221 | 489.77 | 3 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 3.2 GB | 10 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±4.61 nH and COS ±4.63 nH, that is ±101 and ±102 mV of EMF.*

Best sine fit: SIN amplitude 4.613 nH, offset 0.012 nH, phase -137.6°; COS amplitude 4.627 nH, offset 0.122 nH, phase -47.7°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.2° rms and 0.4° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.0323 | 0.1332 |  | 296.381 | 475.15 | 2 iterations, 2.7e-07 | L +0.000 %, R +0.000 % | 1.0 GB | 1 min |
| 0° | -3.0957 | -3.2878 | +0.07° | 271.544 | 496.85 | 3 iterations, 2.3e-07 | L +0.000 %, R +0.000 % | 2.4 GB | 4 min |
| 22.5° | -4.6427 | -0.1083 | -0.19° | 271.712 | 497.33 | 3 iterations, 2.6e-07 | L +0.000 %, R +0.000 % | 2.3 GB | 5 min |
| 45° | -3.3594 | 3.2360 | +0.28° | 271.902 | 496.23 | 3 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 2.3 GB | 7 min |
| 67.5° | -0.2010 | 4.7774 | +0.01° | 271.873 | 495.70 | 4 iterations, 4.0e-08 | L +0.000 %, R +0.000 % | 2.3 GB | 5 min |
| 90° | 3.1189 | 3.5114 | +0.24° | 271.985 | 494.60 | 4 iterations, 4.3e-08 | L +0.000 %, R +0.000 % | 2.4 GB | 5 min |
| 112.5° | 4.6123 | 0.3395 | -0.05° | 271.948 | 494.97 | 3 iterations, 2.6e-07 | L +0.000 %, R +0.000 % | 2.3 GB | 4 min |
| 135° | 3.4027 | -2.9863 | +0.07° | 271.941 | 495.12 | 3 iterations, 2.4e-07 | L +0.000 %, R +0.000 % | 2.3 GB | 5 min |
| 157.5° | 0.2595 | -4.5032 | -0.43° | 271.699 | 496.31 | 3 iterations, 2.2e-07 | L +0.000 %, R +0.000 % | 2.3 GB | 4 min |
| 180° | -3.0957 | -3.2878 | +0.07° | 271.544 | 496.85 | 3 iterations, 2.3e-07 | L +0.000 %, R +0.000 % | 2.4 GB | 4 min |
| 202.5° | -4.6427 | -0.1083 | -0.19° | 271.712 | 497.33 | 3 iterations, 2.6e-07 | L +0.000 %, R +0.000 % | 2.3 GB | 5 min |
| 225° | -3.3594 | 3.2360 | +0.28° | 271.902 | 496.23 | 3 iterations, 2.5e-07 | L +0.000 %, R +0.000 % | 2.3 GB | 6 min |
| 247.5° | -0.2010 | 4.7774 | +0.01° | 271.873 | 495.70 | 4 iterations, 4.0e-08 | L +0.000 %, R +0.000 % | 2.3 GB | 6 min |
| 270° | 3.1189 | 3.5114 | +0.24° | 271.985 | 494.60 | 4 iterations, 4.3e-08 | L +0.000 %, R +0.000 % | 2.4 GB | 5 min |
| 292.5° | 4.6123 | 0.3395 | -0.05° | 271.948 | 494.97 | 3 iterations, 2.6e-07 | L +0.000 %, R +0.000 % | 2.2 GB | 4 min |
| 315° | 3.4027 | -2.9863 | +0.07° | 271.941 | 495.12 | 3 iterations, 2.4e-07 | L +0.000 %, R +0.000 % | 2.2 GB | 6 min |
| 337.5° | 0.2595 | -4.5032 | -0.43° | 271.699 | 496.31 | 3 iterations, 2.2e-07 | L +0.000 %, R +0.000 % | 2.2 GB | 5 min |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±7.14 nH and COS ±7.16 nH, that is ±157 and ±157 mV of EMF.*

Best sine fit: SIN amplitude 7.137 nH, offset 0.013 nH, phase -138.9°; COS amplitude 7.157 nH, offset 0.107 nH, phase -48.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.7° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -4.6926 | -5.2630 | +0.21° | 257.054 | 509.42 | 3 iterations, 2.1e-07 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |
| 22.5° | -7.1906 | -0.4351 | -0.39° | 257.235 | 510.55 | 3 iterations, 2.6e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |
| 45° | -5.2889 | 4.8165 | +0.44° | 257.580 | 508.34 | 3 iterations, 2.2e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 4 min |
| 67.5° | -0.4901 | 7.3089 | -0.10° | 257.458 | 507.80 | 4 iterations, 4.5e-08 | L +0.000 %, R +0.000 % | 1.6 GB | 4 min |
| 90° | 4.7258 | 5.4347 | +0.48° | 257.718 | 505.93 | 4 iterations, 4.8e-08 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |
| 112.5° | 7.1072 | 0.6221 | -0.24° | 257.594 | 506.84 | 3 iterations, 2.4e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 2 min |
| 135° | 5.3524 | -4.6042 | +0.25° | 257.662 | 506.84 | 3 iterations, 2.2e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |
| 157.5° | 0.5808 | -7.0247 | -0.66° | 257.251 | 509.04 | 3 iterations, 2.3e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |
| 180° | -4.6926 | -5.2630 | +0.21° | 257.054 | 509.42 | 3 iterations, 2.1e-07 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |
| 202.5° | -7.1906 | -0.4351 | -0.39° | 257.235 | 510.55 | 3 iterations, 2.6e-07 | L +0.000 %, R +0.000 % | 1.7 GB | 4 min |
| 225° | -5.2889 | 4.8165 | +0.44° | 257.580 | 508.34 | 3 iterations, 2.2e-07 | L +0.000 %, R +0.000 % | 1.7 GB | 4 min |
| 247.5° | -0.4901 | 7.3089 | -0.10° | 257.458 | 507.80 | 4 iterations, 4.5e-08 | L +0.000 %, R +0.000 % | 1.7 GB | 4 min |
| 270° | 4.7258 | 5.4347 | +0.48° | 257.718 | 505.93 | 4 iterations, 4.8e-08 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |
| 292.5° | 7.1072 | 0.6221 | -0.24° | 257.594 | 506.84 | 3 iterations, 2.4e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |
| 315° | 5.3524 | -4.6042 | +0.25° | 257.662 | 506.84 | 3 iterations, 2.2e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |
| 337.5° | 0.5808 | -7.0247 | -0.66° | 257.251 | 509.04 | 3 iterations, 2.3e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 16 of 16 angles solved. Each dot is one PyPEEC solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±9.60 nH and COS ±9.62 nH, that is ±211 and ±212 mV of EMF.*

Best sine fit: SIN amplitude 9.604 nH, offset 0.021 nH, phase -141.0°; COS amplitude 9.625 nH, offset 0.083 nH, phase -51.1°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.9° rms and 1.3° at worst, in electrical degrees (0.5 of a mechanical degree each). SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Solve | L and R checks | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -6.0996 | -7.3188 | +0.67° | 235.752 | 540.27 | 3 iterations, 1.6e-07 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |
| 22.5° | -9.6695 | -1.1002 | -0.93° | 235.716 | 543.92 | 3 iterations, 1.6e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |
| 45° | -7.2713 | 6.1988 | +0.94° | 236.478 | 538.34 | 3 iterations, 1.8e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 4 min |
| 67.5° | -1.0815 | 9.7602 | -0.50° | 236.004 | 539.70 | 3 iterations, 1.8e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |
| 90° | 6.1688 | 7.4117 | +1.07° | 236.587 | 535.94 | 3 iterations, 1.5e-07 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |
| 112.5° | 9.4986 | 1.2072 | -0.74° | 236.198 | 538.86 | 3 iterations, 1.7e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |
| 135° | 7.3842 | -6.0545 | +0.77° | 236.590 | 536.96 | 3 iterations, 1.9e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |
| 157.5° | 1.2398 | -9.4443 | -1.29° | 235.767 | 542.11 | 3 iterations, 2.0e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |
| 180° | -6.0996 | -7.3188 | +0.67° | 235.752 | 540.27 | 3 iterations, 1.6e-07 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |
| 202.5° | -9.6695 | -1.1002 | -0.93° | 235.716 | 543.92 | 3 iterations, 1.6e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |
| 225° | -7.2713 | 6.1988 | +0.94° | 236.478 | 538.34 | 3 iterations, 1.8e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 4 min |
| 247.5° | -1.0815 | 9.7602 | -0.50° | 236.004 | 539.70 | 3 iterations, 1.8e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |
| 270° | 6.1688 | 7.4117 | +1.07° | 236.587 | 535.94 | 3 iterations, 1.5e-07 | L +0.000 %, R +0.000 % | 1.7 GB | 3 min |
| 292.5° | 9.4986 | 1.2072 | -0.74° | 236.198 | 538.86 | 3 iterations, 1.7e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 2 min |
| 315° | 7.3842 | -6.0545 | +0.77° | 236.590 | 536.96 | 3 iterations, 1.9e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 3 min |
| 337.5° | 1.2398 | -9.4443 | -1.29° | 235.767 | 542.11 | 3 iterations, 2.0e-07 | L +0.000 %, R +0.000 % | 1.6 GB | 2 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 5.08 times and COS 5.07 times larger.*

## Against the expectation

The generator estimates the TX at 292 nH with the rotor away and 226 nH with it (its drop with the rotor is an upper estimate). PyPEEC gives 296.4 nH with the rotor away, and 284.1 to 284.3 nH with the rotor at 2 mm, and 280.1 to 280.4 nH with the rotor at 1.5 mm, and 271.5 to 272.0 nH with the rotor at 1 mm, and 257.1 to 257.7 nH with the rotor at 0.5 mm, and 235.7 to 236.6 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../PyPEEC%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0d2_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In PyPEEC, SIN is opened by a cut in its top trace at (96.59, 100.5) and COS at (97.24, 97.94), the TX at its ends at (111, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in PyPEEC](../S0d2_1x_OD23_2L_tiny_TX3top_Cut_pypeec_setup.webp)

*How the boards are set up in PyPEEC, drawn by [`rig_picture.py`](../PyPEEC%20Simulation/rig_picture.py) from the voxels simulation.py solves from: the rotor copper side down over the stator, each receiver opened by a 0.2 mm cut across a top trace (the two cut faces are the terminal, held at 0 A, so the voltage across the cut is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
