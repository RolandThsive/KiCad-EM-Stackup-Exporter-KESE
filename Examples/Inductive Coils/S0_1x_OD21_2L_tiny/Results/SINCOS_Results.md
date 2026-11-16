# S0_1x_OD21_2L_tiny: SIN and COS over the rotor's turn in Elmer

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 21 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one Elmer solve with its own mesh. This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 1 mm | 8 of 8 | 2.15 / 2.07 nH (47 / 45 mV) | 4.6° rms, 7.1° peak |
| 0.5 mm | 8 of 8 | 3.26 / 2.81 nH (72 / 62 mV) | 14.3° rms, 28.3° peak |
| 0.1 mm | 8 of 8 | 2.45 / 5.04 nH (54 / 111 mV) | 67.6° rms, 172.9° peak |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.15 nH and COS ±2.07 nH, that is ±47 and ±45 mV of EMF.*

Best sine fit: SIN amplitude 2.151 nH, offset -0.077 nH, phase -133.8°; COS amplitude 2.069 nH, offset -0.124 nH, phase 135.0°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 4.6° rms and 7.1° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 91.2° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.0591 | -0.1012 |  | 110.885 | 438.92 | 1500 | 4.5e-04 | 11.4 GB | 28 min |
| 0° | -1.4155 | 1.4914 | -7.07° | 103.084 | 358.78 | 1500 | 4.0e-04 | 11.4 GB | 25 min |
| 45° | -2.5211 | 0.0766 | -5.50° | 108.283 | 332.80 | 1500 | 2.8e-04 | 11.4 GB | 26 min |
| 90° | -1.6190 | -1.6767 | +0.69° | 107.701 | 333.28 | 1500 | 2.7e-04 | 11.5 GB | 24 min |
| 135° | 0.1041 | -2.3979 | +3.76° | 107.784 | 334.86 | 1500 | 2.7e-04 | 11.4 GB | 24 min |
| 180° | 1.6682 | -1.5147 | +4.73° | 106.140 | 329.85 | 1500 | 2.9e-04 | 11.3 GB | 25 min |
| 225° | 1.8161 | 0.0767 | +5.65° | 101.053 | 365.87 | 1500 | 4.8e-04 | 11.3 GB | 25 min |
| 270° | 1.3267 | 1.3324 | +1.52° | 101.022 | 326.93 | 1500 | 4.3e-04 | 11.3 GB | 25 min |
| 315° | 0.0230 | 1.6238 | -3.79° | 98.618 | 318.65 | 1500 | 4.7e-04 | 11.4 GB | 25 min |

8 of 8 solves stopped at the 1500-iteration cap, with the residual between 2.7e-04 and 4.8e-04 rather than the 1e-07 asked for. The TX is round, so turning the rotor should not change its inductance: its spread here, 98.6 to 108.3 nH, is a measure of what the solver leaves.

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.26 nH and COS ±2.81 nH, that is ±72 and ±62 mV of EMF.*

Best sine fit: SIN amplitude 3.257 nH, offset -0.271 nH, phase -137.5°; COS amplitude 2.809 nH, offset -0.378 nH, phase 133.3°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 14.3° rms and 28.3° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.3° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -2.2371 | 2.6498 | -12.58° | 98.762 | 357.06 | 1500 | 3.7e-04 | 10.7 GB | 27 min |
| 45° | -4.2701 | 0.3094 | -8.11° | 106.020 | 322.16 | 1500 | 2.7e-04 | 10.7 GB | 22 min |
| 90° | -2.7809 | -2.6806 | +4.93° | 104.109 | 335.26 | 1500 | 2.4e-04 | 10.8 GB | 21 min |
| 135° | 0.0946 | -3.7914 | +8.44° | 102.680 | 345.51 | 1500 | 2.9e-04 | 10.8 GB | 21 min |
| 180° | 2.4928 | -2.3068 | +9.18° | 99.148 | 344.93 | 1500 | 3.3e-04 | 10.7 GB | 22 min |
| 225° | 1.8453 | 0.1726 | +19.95° | 87.868 | 381.08 | 1500 | 7.9e-04 | 10.7 GB | 22 min |
| 270° | 2.2467 | 1.9950 | +5.70° | 99.459 | 295.36 | 1500 | 6.0e-04 | 10.7 GB | 22 min |
| 315° | 0.4424 | 0.6283 | -28.28° | 78.886 | 208.81 | 1500 | 1.0e-03 | 10.7 GB | 21 min |

8 of 8 solves stopped at the 1500-iteration cap, with the residual between 2.4e-04 and 1.0e-03 rather than the 1e-07 asked for. The TX is round, so turning the rotor should not change its inductance: its spread here, 78.9 to 106.0 nH, is a measure of what the solver leaves.

**Not converged enough to read:** 3 of 8 solves (225°, 270°, 315°) stopped above a residual of 5e-04 or give the TX a negative resistance. On S0, every 1 mm solve stopped below it and the 0.5 mm solves above it are the ones that fall off the sine. Read this gap's curve with that in mind.

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.45 nH and COS ±5.04 nH, that is ±54 and ±111 mV of EMF.*

Best sine fit: SIN amplitude 2.447 nH, offset -1.646 nH, phase -144.6°; COS amplitude 5.036 nH, offset -0.342 nH, phase 133.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 67.6° rms and 172.9° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 81.5° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -2.5343 | 3.5374 | -11.29° | 84.928 | 635.73 | 1500 | 8.8e-04 | 10.1 GB | 20 min |
| 45° | -5.8690 | -0.7143 | +10.94° | 98.921 | 302.69 | 1500 | 1.5e-03 | 10.1 GB | 19 min |
| 90° | -5.3363 | -4.2902 | -9.05° | 107.976 | 117.17 | 1500 | 1.7e-03 | 10.1 GB | 22 min |
| 135° | -0.0142 | -6.0607 | +38.91° | 97.096 | 269.68 | 1500 | 8.1e-04 | 10.1 GB | 21 min |
| 180° | 3.0468 | -2.7029 | +39.75° | 83.267 | 452.34 | 1500 | 6.9e-04 | 10.0 GB | 19 min |
| 225° | -4.4842 | 1.2860 | +172.91° | 30.506 | -653.47 | 1500 | 4.4e-03 | 10.0 GB | 19 min |
| 270° | 0.7708 | -1.4429 | -49.00° | 46.791 | 37.51 | 1500 | 2.0e-03 | 10.0 GB | 20 min |
| 315° | 1.2500 | 7.6531 | -28.23° | 108.789 | -395.40 | 1500 | 2.0e-03 | 10.0 GB | 18 min |

8 of 8 solves stopped at the 1500-iteration cap, with the residual between 6.9e-04 and 4.4e-03 rather than the 1e-07 asked for. The TX is round, so turning the rotor should not change its inductance: its spread here, 30.5 to 108.8 nH, is a measure of what the solver leaves.

**Not converged enough to read:** 8 of 8 solves (0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°) stopped above a residual of 5e-04 or give the TX a negative resistance. On S0, every 1 mm solve stopped below it and the 0.5 mm solves above it are the ones that fall off the sine. Read this gap's curve with that in mind.

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 4. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 1 to 0.1 mm makes SIN 1.14 times and COS 2.43 times larger.*

## Against the expectation

The generator estimates the TX at 132 nH with the rotor away and 109 nH with it (its drop with the rotor is an upper estimate). Elmer gives 110.9 nH with the rotor away, and 98.6 to 108.3 nH with the rotor at 1 mm, and 78.9 to 106.0 nH with the rotor at 0.5 mm, and 30.5 to 108.8 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../Elmer%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD21_2L_tiny_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Elmer, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (109.8, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in Elmer](../S0_1x_OD21_2L_tiny_elmer_setup.webp)

*How the boards are set up in Elmer, drawn by [`rig_picture.py`](../Elmer%20Simulation/rig_picture.py) from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened at a left-out via (its two pads and the gap between them are the terminal, held at 0 A, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
