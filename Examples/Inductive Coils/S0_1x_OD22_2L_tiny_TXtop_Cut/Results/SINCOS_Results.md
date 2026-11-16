# S0_1x_OD22_2L_tiny_TXtop_Cut: SIN and COS over the rotor's turn in Elmer

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 22.2 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one Elmer solve with its own mesh. This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.42 / 1.42 nH (31 / 31 mV) | 2.2° rms, 3.4° peak |
| 1.5 mm | 8 of 8 | 2.21 / 2.10 nH (49 / 46 mV) | 3.2° rms, 5.9° peak |
| 1 mm | 8 of 8 | 2.81 / 3.14 nH (62 / 69 mV) | 4.8° rms, 11.3° peak |
| 0.5 mm | 8 of 8 | 4.39 / 4.46 nH (97 / 98 mV) | 1.8° rms, 3.5° peak |
| 0.1 mm | 8 of 8 | 5.98 / 6.22 nH (131 / 137 mV) | 10.9° rms, 24.6° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.42 nH and COS ±1.42 nH, that is ±31 and ±31 mV of EMF.*

Best sine fit: SIN amplitude 1.420 nH, offset -0.057 nH, phase 44.8°; COS amplitude 1.419 nH, offset 0.093 nH, phase 132.5°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 2.2° rms and 3.4° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 87.7° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 0.8799 | 1.1373 | -1.77° | 124.960 | 326.50 | 1500 | 2.7e-04 | 13.3 GB | 31 min |
| 45° | 1.5060 | 0.2227 | -3.41° | 126.945 | 316.58 | 1500 | 2.9e-04 | 13.3 GB | 27 min |
| 90° | 0.9053 | -0.9261 | +2.97° | 126.140 | 328.48 | 1500 | 2.2e-04 | 13.3 GB | 28 min |
| 135° | -0.1101 | -1.3441 | +3.42° | 126.021 | 332.04 | 1500 | 2.1e-04 | 13.3 GB | 32 min |
| 180° | -1.0558 | -0.9127 | +1.08° | 126.005 | 330.58 | 1500 | 2.0e-04 | 13.3 GB | 28 min |
| 225° | -1.4186 | 0.0525 | -0.41° | 124.830 | 333.05 | 1500 | 2.3e-04 | 13.3 GB | 31 min |
| 270° | -1.0532 | 1.0123 | -0.97° | 125.193 | 324.68 | 1500 | 2.3e-04 | 13.3 GB | 26 min |
| 315° | -0.1125 | 1.5059 | -0.92° | 125.178 | 321.92 | 1500 | 2.8e-04 | 13.3 GB | 29 min |

8 of 8 solves stopped at the 1500-iteration cap, with the residual between 2.0e-04 and 2.9e-04 rather than the 1e-07 asked for. The TX is round, so turning the rotor should not change its inductance: its spread here, 124.8 to 126.9 nH, is a measure of what the solver leaves.

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.21 nH and COS ±2.10 nH, that is ±49 and ±46 mV of EMF.*

Best sine fit: SIN amplitude 2.210 nH, offset 0.034 nH, phase 43.7°; COS amplitude 2.102 nH, offset 0.120 nH, phase 131.7°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 3.2° rms and 5.9° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 88.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 1.3791 | 1.6578 | -3.02° | 122.889 | 326.88 | 1500 | 3.7e-04 | 13.3 GB | 25 min |
| 45° | 2.5543 | 0.4261 | -5.06° | 125.998 | 296.11 | 1500 | 4.5e-04 | 13.3 GB | 29 min |
| 90° | 1.6160 | -1.4327 | +3.11° | 124.459 | 370.98 | 1500 | 3.4e-04 | 13.3 GB | 25 min |
| 135° | -0.1104 | -2.0118 | +5.90° | 123.737 | 334.36 | 1500 | 2.0e-04 | 13.3 GB | 33 min |
| 180° | -1.4896 | -1.3770 | +1.28° | 123.684 | 327.62 | 1500 | 1.9e-04 | 13.3 GB | 26 min |
| 225° | -2.0416 | 0.0400 | -0.10° | 122.252 | 334.31 | 1500 | 2.3e-04 | 13.3 GB | 28 min |
| 270° | -1.5159 | 1.4737 | -0.22° | 122.782 | 323.67 | 1500 | 2.3e-04 | 13.3 GB | 29 min |
| 315° | -0.1215 | 2.1829 | -1.88° | 122.738 | 321.81 | 1500 | 2.5e-04 | 13.3 GB | 29 min |

8 of 8 solves stopped at the 1500-iteration cap, with the residual between 1.9e-04 and 4.5e-04 rather than the 1e-07 asked for. The TX is round, so turning the rotor should not change its inductance: its spread here, 122.3 to 126.0 nH, is a measure of what the solver leaves.

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.81 nH and COS ±3.14 nH, that is ±62 and ±69 mV of EMF.*

Best sine fit: SIN amplitude 2.805 nH, offset -0.162 nH, phase 43.8°; COS amplitude 3.136 nH, offset 0.018 nH, phase 136.4°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 4.8° rms and 11.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 92.6° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | -0.1711 | 0.1381 |  | 130.231 | 324.29 | 1500 | 2.7e-04 | 12.8 GB | 26 min |
| 0° | 2.1363 | 2.4962 | +0.62° | 119.508 | 326.11 | 1500 | 2.6e-04 | 12.8 GB | 28 min |
| 45° | 2.0315 | -0.4910 | +11.31° | 117.347 | 365.06 | 1500 | 6.0e-04 | 12.8 GB | 24 min |
| 90° | 2.2076 | -2.1225 | -6.48° | 120.633 | 328.89 | 1500 | 2.1e-04 | 12.8 GB | 24 min |
| 135° | -0.0691 | -3.0419 | -2.36° | 119.900 | 340.31 | 1500 | 2.0e-04 | 12.8 GB | 27 min |
| 180° | -2.1688 | -2.0963 | +1.28° | 119.494 | 335.70 | 1500 | 2.0e-04 | 12.8 GB | 25 min |
| 225° | -2.9779 | 0.0119 | -0.54° | 117.582 | 334.58 | 1500 | 2.4e-04 | 12.7 GB | 27 min |
| 270° | -2.2685 | 2.1797 | -2.88° | 118.648 | 329.48 | 1500 | 2.6e-04 | 12.7 GB | 25 min |
| 315° | -0.1858 | 3.2100 | -0.90° | 118.381 | 325.61 | 1500 | 2.6e-04 | 12.7 GB | 24 min |

8 of 8 solves stopped at the 1500-iteration cap, with the residual between 2.0e-04 and 6.0e-04 rather than the 1e-07 asked for. The TX is round, so turning the rotor should not change its inductance: its spread here, 117.3 to 120.6 nH, is a measure of what the solver leaves.

**Not converged enough to read:** 1 of 8 solves (45°) stopped above a residual of 5e-04 or give the TX a negative resistance. On S0, every 1 mm solve stopped below it and the 0.5 mm solves above it are the ones that fall off the sine. Read this gap's curve with that in mind.

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±4.39 nH and COS ±4.46 nH, that is ±97 and ±98 mV of EMF.*

Best sine fit: SIN amplitude 4.389 nH, offset -0.055 nH, phase 42.3°; COS amplitude 4.456 nH, offset 0.056 nH, phase 132.7°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 1.8° rms and 3.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.4° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 3.0495 | 3.6601 | -1.34° | 112.740 | 330.33 | 1500 | 2.0e-04 | 12.0 GB | 24 min |
| 45° | 4.4979 | 0.0493 | +2.58° | 112.744 | 365.20 | 1500 | 9.7e-04 | 12.1 GB | 24 min |
| 90° | 3.0499 | -2.9349 | +0.99° | 111.430 | 362.06 | 1500 | 2.3e-04 | 12.1 GB | 29 min |
| 135° | 0.0893 | -4.4793 | +0.65° | 111.984 | 361.87 | 1500 | 2.2e-04 | 12.1 GB | 24 min |
| 180° | -3.0752 | -3.0943 | +1.72° | 110.545 | 364.63 | 1500 | 2.4e-04 | 12.0 GB | 22 min |
| 225° | -4.1361 | -0.1342 | -0.14° | 106.529 | 354.33 | 1500 | 3.1e-04 | 12.0 GB | 24 min |
| 270° | -3.4163 | 3.0855 | -0.92° | 110.398 | 343.69 | 1500 | 2.6e-04 | 12.0 GB | 23 min |
| 315° | -0.4958 | 4.2981 | -3.54° | 107.205 | 336.47 | 1500 | 3.2e-04 | 12.0 GB | 23 min |

8 of 8 solves stopped at the 1500-iteration cap, with the residual between 2.0e-04 and 9.7e-04 rather than the 1e-07 asked for. The TX is round, so turning the rotor should not change its inductance: its spread here, 106.5 to 112.7 nH, is a measure of what the solver leaves.

**Not converged enough to read:** 1 of 8 solves (45°) stopped above a residual of 5e-04 or give the TX a negative resistance. On S0, every 1 mm solve stopped below it and the 0.5 mm solves above it are the ones that fall off the sine. Read this gap's curve with that in mind.

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±5.98 nH and COS ±6.22 nH, that is ±131 and ±137 mV of EMF.*

Best sine fit: SIN amplitude 5.977 nH, offset -0.502 nH, phase 31.8°; COS amplitude 6.219 nH, offset 1.217 nH, phase 112.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 10.9° rms and 24.6° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 81.1° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | 2.8174 | 5.0222 | +13.90° | 95.903 | 319.39 | 1500 | 3.9e-04 | 11.2 GB | 21 min |
| 45° | 5.2558 | 6.4667 | -24.56° | 115.221 | 180.49 | 1500 | 3.0e-03 | 11.3 GB | 22 min |
| 90° | 4.6771 | -2.8292 | +8.57° | 104.706 | 341.47 | 1500 | 9.5e-04 | 11.3 GB | 23 min |
| 135° | 0.5325 | -5.0918 | +6.99° | 93.983 | 440.67 | 1500 | 4.4e-04 | 11.3 GB | 22 min |
| 180° | -3.0913 | -3.5535 | +1.13° | 90.930 | 416.14 | 1500 | 5.3e-04 | 11.2 GB | 21 min |
| 225° | -6.8940 | -1.1387 | -2.83° | 122.076 | -635.46 | 1500 | 3.0e-03 | 11.2 GB | 22 min |
| 270° | -5.1482 | 3.2803 | -5.21° | 97.685 | -202.64 | 1500 | 1.6e-03 | 11.2 GB | 25 min |
| 315° | -2.1677 | 7.5761 | +1.43° | 112.890 | 25.43 | 1500 | 1.1e-03 | 11.2 GB | 23 min |

8 of 8 solves stopped at the 1500-iteration cap, with the residual between 3.9e-04 and 3.0e-03 rather than the 1e-07 asked for. The TX is round, so turning the rotor should not change its inductance: its spread here, 90.9 to 122.1 nH, is a measure of what the solver leaves.

**Not converged enough to read:** 6 of 8 solves (45°, 90°, 180°, 225°, 270°, 315°) stopped above a residual of 5e-04 or give the TX a negative resistance. On S0, every 1 mm solve stopped below it and the 0.5 mm solves above it are the ones that fall off the sine. Read this gap's curve with that in mind.

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 4.21 times and COS 4.38 times larger.*

## Against the expectation

The generator estimates the TX at 144 nH with the rotor away and 116 nH with it (its drop with the rotor is an upper estimate). Elmer gives 130.2 nH with the rotor away, and 124.8 to 126.9 nH with the rotor at 2 mm, and 122.3 to 126.0 nH with the rotor at 1.5 mm, and 117.3 to 120.6 nH with the rotor at 1 mm, and 106.5 to 112.7 nH with the rotor at 0.5 mm, and 90.9 to 122.1 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../Elmer%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD22_2L_tiny_TXtop_Cut_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Elmer, SIN is opened by a cut in its top trace at (97.16, 101.63) and COS at (98.37, 97.16), the TX at its ends at (110.4, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in Elmer](../S0_1x_OD22_2L_tiny_TXtop_Cut_elmer_setup.webp)

*How the boards are set up in Elmer, drawn by [`rig_picture.py`](../Elmer%20Simulation/rig_picture.py) from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened by a 0.2 mm cut across a top trace (the two cut faces are the terminal, held at 0 A, so the voltage across the cut is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
