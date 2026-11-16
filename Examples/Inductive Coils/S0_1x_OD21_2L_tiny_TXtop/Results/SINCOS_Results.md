# S0_1x_OD21_2L_tiny_TXtop: SIN and COS over the rotor's turn in Elmer

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 21 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one Elmer solve with its own mesh. This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 0.89 / 0.88 nH (19 / 19 mV) | 2.1° rms, 3.9° peak |
| 1.5 mm | 8 of 8 | 1.40 / 1.37 nH (31 / 30 mV) | 2.4° rms, 4.0° peak |
| 1 mm | 8 of 8 | 2.24 / 2.15 nH (49 / 47 mV) | 3.2° rms, 5.6° peak |
| 0.5 mm | 8 of 8 | 3.32 / 3.18 nH (73 / 70 mV) | 3.2° rms, 5.7° peak |
| 0.1 mm | 8 of 8 | 5.12 / 4.86 nH (113 / 107 mV) | 17.5° rms, 44.0° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±0.89 nH and COS ±0.88 nH, that is ±19 and ±19 mV of EMF.*

Best sine fit: SIN amplitude 0.885 nH, offset 0.119 nH, phase -136.5°; COS amplitude 0.884 nH, offset 0.107 nH, phase 131.6°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 2.1° rms and 3.9° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 91.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.4411 | 0.7515 | -1.64° | 111.080 | 309.09 | 1500 | 3.5e-04 | 13.3 GB | 26 min |
| 45° | -0.8510 | 0.2147 | -3.95° | 113.372 | 312.38 | 1500 | 3.1e-04 | 13.3 GB | 25 min |
| 90° | -0.5104 | -0.5040 | +1.58° | 112.462 | 318.65 | 1500 | 3.1e-04 | 13.3 GB | 29 min |
| 135° | 0.1287 | -0.8087 | +3.01° | 112.499 | 321.20 | 1500 | 3.1e-04 | 13.3 GB | 26 min |
| 180° | 0.7443 | -0.5300 | +1.84° | 112.533 | 315.82 | 1500 | 2.8e-04 | 13.3 GB | 26 min |
| 225° | 0.9710 | 0.0744 | +0.21° | 111.327 | 312.71 | 1500 | 3.0e-04 | 13.3 GB | 26 min |
| 270° | 0.7327 | 0.6790 | +0.43° | 111.057 | 309.83 | 1500 | 3.3e-04 | 13.3 GB | 27 min |
| 315° | 0.1784 | 0.9784 | -1.49° | 111.171 | 306.99 | 1500 | 3.7e-04 | 13.2 GB | 27 min |

8 of 8 solves stopped at the 1500-iteration cap, with the residual between 2.8e-04 and 3.7e-04 rather than the 1e-07 asked for. The TX is round, so turning the rotor should not change its inductance: its spread here, 111.1 to 113.4 nH, is a measure of what the solver leaves.

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.40 nH and COS ±1.37 nH, that is ±31 and ±30 mV of EMF.*

Best sine fit: SIN amplitude 1.396 nH, offset 0.095 nH, phase -136.6°; COS amplitude 1.369 nH, offset 0.114 nH, phase 130.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 2.4° rms and 4.0° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 92.5° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.7872 | 1.1337 | -1.84° | 109.223 | 308.66 | 1500 | 3.6e-04 | 12.7 GB | 27 min |
| 45° | -1.4350 | 0.2945 | -4.04° | 112.073 | 309.63 | 1500 | 3.4e-04 | 12.7 GB | 28 min |
| 90° | -0.8841 | -0.8363 | +2.49° | 110.830 | 320.94 | 1500 | 3.0e-04 | 12.7 GB | 26 min |
| 135° | 0.0969 | -1.2967 | +2.88° | 110.938 | 320.30 | 1500 | 2.8e-04 | 12.7 GB | 25 min |
| 180° | 1.0631 | -0.8520 | +2.34° | 110.277 | 327.77 | 1500 | 2.8e-04 | 12.6 GB | 24 min |
| 225° | 1.4646 | 0.0000 | -2.01° | 109.448 | 356.18 | 1500 | 4.1e-04 | 12.6 GB | 28 min |
| 270° | 1.0576 | 1.0061 | +1.22° | 108.935 | 308.02 | 1500 | 3.3e-04 | 12.6 GB | 23 min |
| 315° | 0.1879 | 1.4598 | -1.03° | 108.748 | 306.65 | 1500 | 3.4e-04 | 12.6 GB | 26 min |

8 of 8 solves stopped at the 1500-iteration cap, with the residual between 2.8e-04 and 4.1e-04 rather than the 1e-07 asked for. The TX is round, so turning the rotor should not change its inductance: its spread here, 108.7 to 112.1 nH, is a measure of what the solver leaves.

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.24 nH and COS ±2.15 nH, that is ±49 and ±47 mV of EMF.*

Best sine fit: SIN amplitude 2.238 nH, offset 0.045 nH, phase -137.9°; COS amplitude 2.146 nH, offset 0.147 nH, phase 129.5°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 3.2° rms and 5.6° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 92.7° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.1890 | 0.1096 |  | 115.702 | 308.51 | 1500 | 3.3e-04 | 12.0 GB | 26 min |
| 0° | -1.3258 | 1.7857 | -2.15° | 106.256 | 309.36 | 1500 | 3.6e-04 | 12.0 GB | 22 min |
| 45° | -2.5099 | 0.5645 | -5.56° | 110.308 | 298.44 | 1500 | 4.2e-04 | 11.9 GB | 25 min |
| 90° | -1.5035 | -1.3494 | +4.33° | 107.931 | 316.63 | 1500 | 2.9e-04 | 12.0 GB | 23 min |
| 135° | 0.0389 | -2.0881 | +3.95° | 107.778 | 325.16 | 1500 | 2.7e-04 | 11.9 GB | 23 min |
| 180° | 1.5757 | -1.4178 | +2.25° | 106.968 | 325.26 | 1500 | 2.6e-04 | 11.9 GB | 27 min |
| 225° | 2.1151 | 0.0216 | +0.47° | 104.656 | 319.02 | 1500 | 3.2e-04 | 11.9 GB | 24 min |
| 270° | 1.7003 | 1.4555 | -1.40° | 107.522 | 285.57 | 1500 | 4.9e-04 | 11.9 GB | 24 min |
| 315° | 0.2712 | 2.2081 | -1.90° | 104.903 | 310.46 | 1500 | 3.6e-04 | 11.9 GB | 23 min |

8 of 8 solves stopped at the 1500-iteration cap, with the residual between 2.6e-04 and 4.9e-04 rather than the 1e-07 asked for. The TX is round, so turning the rotor should not change its inductance: its spread here, 104.7 to 110.3 nH, is a measure of what the solver leaves.

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.32 nH and COS ±3.18 nH, that is ±73 and ±70 mV of EMF.*

Best sine fit: SIN amplitude 3.316 nH, offset 0.034 nH, phase -140.6°; COS amplitude 3.181 nH, offset 0.113 nH, phase 129.3°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 3.2° rms and 5.7° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.1° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.9956 | 2.7824 | -3.22° | 99.702 | 322.64 | 1500 | 3.3e-04 | 11.3 GB | 23 min |
| 45° | -3.6035 | 0.6170 | -2.55° | 103.521 | 295.79 | 1500 | 3.8e-04 | 11.2 GB | 23 min |
| 90° | -2.4736 | -2.0354 | +2.43° | 101.891 | 329.80 | 1500 | 2.9e-04 | 11.3 GB | 23 min |
| 135° | -0.1225 | -3.2506 | +3.10° | 100.899 | 344.70 | 1500 | 2.9e-04 | 11.2 GB | 22 min |
| 180° | 2.2655 | -2.1859 | +3.62° | 98.507 | 344.23 | 1500 | 2.9e-04 | 11.2 GB | 21 min |
| 225° | 3.0206 | -0.1245 | +0.91° | 94.271 | 337.54 | 1500 | 3.9e-04 | 11.2 GB | 22 min |
| 270° | 2.5649 | 2.2037 | +1.39° | 97.410 | 321.37 | 1500 | 3.4e-04 | 11.2 GB | 22 min |
| 315° | 0.6176 | 2.9013 | -5.69° | 92.903 | 328.15 | 1500 | 4.9e-04 | 11.2 GB | 26 min |

8 of 8 solves stopped at the 1500-iteration cap, with the residual between 2.9e-04 and 4.9e-04 rather than the 1e-07 asked for. The TX is round, so turning the rotor should not change its inductance: its spread here, 92.9 to 103.5 nH, is a measure of what the solver leaves.

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one Elmer solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±5.12 nH and COS ±4.86 nH, that is ±113 and ±107 mV of EMF.*

Best sine fit: SIN amplitude 5.117 nH, offset 1.153 nH, phase -153.5°; COS amplitude 4.862 nH, offset -0.057 nH, phase 135.9°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 17.5° rms and 44.0° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 70.6° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Iterations | Residual | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.5502 | 4.1469 | -4.36° | 84.257 | 237.07 | 1500 | 5.2e-04 | 10.6 GB | 21 min |
| 45° | -3.0078 | -2.8010 | +43.99° | 67.014 | 480.74 | 1500 | 2.6e-03 | 10.5 GB | 24 min |
| 90° | -3.3950 | -2.2895 | -8.46° | 93.535 | 411.72 | 1500 | 6.9e-04 | 10.6 GB | 27 min |
| 135° | -0.6193 | -4.2682 | -12.57° | 89.111 | 439.23 | 1500 | 5.4e-04 | 10.5 GB | 21 min |
| 180° | 2.5191 | -3.1738 | -13.17° | 87.894 | 463.34 | 1500 | 1.0e-03 | 10.5 GB | 21 min |
| 225° | 7.3469 | -1.5199 | -4.74° | 125.144 | -478.02 | 1500 | 2.9e-03 | 10.5 GB | 23 min |
| 270° | 5.3390 | 3.6394 | +7.13° | 107.772 | -1117.13 | 1500 | 4.5e-03 | 10.5 GB | 22 min |
| 315° | 2.5890 | 5.8071 | -3.88° | 101.659 | 23.90 | 1500 | 1.3e-03 | 10.5 GB | 20 min |

8 of 8 solves stopped at the 1500-iteration cap, with the residual between 5.2e-04 and 4.5e-03 rather than the 1e-07 asked for. The TX is round, so turning the rotor should not change its inductance: its spread here, 67.0 to 125.1 nH, is a measure of what the solver leaves.

**Not converged enough to read:** 8 of 8 solves (0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°) stopped above a residual of 5e-04 or give the TX a negative resistance. On S0, every 1 mm solve stopped below it and the 0.5 mm solves above it are the ones that fall off the sine. Read this gap's curve with that in mind.

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 5.78 times and COS 5.50 times larger.*

## Against the expectation

The generator estimates the TX at 130 nH with the rotor away and 106 nH with it (its drop with the rotor is an upper estimate). Elmer gives 115.7 nH with the rotor away, and 111.1 to 113.4 nH with the rotor at 2 mm, and 108.7 to 112.1 nH with the rotor at 1.5 mm, and 104.7 to 110.3 nH with the rotor at 1 mm, and 92.9 to 103.5 nH with the rotor at 0.5 mm, and 67.0 to 125.1 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../Elmer%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD21_2L_tiny_TXtop_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In Elmer, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (109.8, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in Elmer](../S0_1x_OD21_2L_tiny_TXtop_elmer_setup.webp)

*How the boards are set up in Elmer, drawn by [`rig_picture.py`](../Elmer%20Simulation/rig_picture.py) from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened at a left-out via (its two pads and the gap between them are the terminal, held at 0 A, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
