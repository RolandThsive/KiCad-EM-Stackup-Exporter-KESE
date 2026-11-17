# S0_1x_OD21_2L_tiny_TXtop: SIN and COS over the rotor's turn in FastHenry

A coil set made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator): 21 mm across, 2 copper layers, one electrical period per turn and a half-ring rotor. The TX carries 1 A at 3.5 MHz; the curves are the mutual inductance from the TX to SIN and to COS (1 nH is 22 mV of EMF). Each angle is one FastHenry solve: the stator's tracks as filaments and the rotor's copper as a grid of bars turned to that angle, solved directly, so each solve is the exact answer of its model. Each is checked by reciprocity: the M from the TX to a receiver and the M from the receiver back to the TX must agree (the Reciprocity column gives how far apart they are, as a part of the larger receiver's M; a solve is read when it is within 1 %). This page is rewritten by `simulation.py` after every solve.

| Air gap | Angles solved | Amplitude SIN / COS | Angle error |
|---|---|---|---|
| 2 mm | 8 of 8 | 1.02 / 1.02 nH (22 / 22 mV) | 0.4° rms, 0.5° peak |
| 1.5 mm | 8 of 8 | 1.57 / 1.57 nH (35 / 35 mV) | 0.4° rms, 0.5° peak |
| 1 mm | 8 of 8 | 2.48 / 2.49 nH (55 / 55 mV) | 0.4° rms, 0.5° peak |
| 0.5 mm | 8 of 8 | 3.91 / 3.92 nH (86 / 86 mV) | 0.7° rms, 0.8° peak |
| 0.1 mm | 8 of 8 | 5.31 / 5.32 nH (117 / 117 mV) | 1.5° rms, 1.8° peak |

## 2 mm air gap

![SIN and COS against the rotor angle at a 2 mm air gap](2mm_AirGap/results_gap2mm.webp)

*Figure 1. SIN (blue) and COS (orange) at a 2 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.02 nH and COS ±1.02 nH, that is ±22 and ±22 mV of EMF.*

Best sine fit: SIN amplitude 1.016 nH, offset 0.081 nH, phase -135.6°; COS amplitude 1.019 nH, offset 0.074 nH, phase 134.4°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 89.9° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -0.6301 | 0.7974 | +0.23° | 127.730 | 249.15 | 6,555 | exact | 0.7 GB | 4 min |
| 45° | -0.9434 | 0.0919 | -0.36° | 127.764 | 249.11 | 6,555 | exact | 0.7 GB | 4 min |
| 90° | -0.6365 | -0.6401 | +0.41° | 127.769 | 249.10 | 6,555 | exact | 0.7 GB | 4 min |
| 135° | 0.0642 | -0.9515 | -0.31° | 127.774 | 249.09 | 6,555 | exact | 0.7 GB | 4 min |
| 180° | 0.7931 | -0.6453 | +0.42° | 127.804 | 249.06 | 6,555 | exact | 0.7 GB | 4 min |
| 225° | 1.0972 | 0.0577 | -0.32° | 127.771 | 249.10 | 6,555 | exact | 0.7 GB | 4 min |
| 270° | 0.8012 | 0.7917 | +0.40° | 127.758 | 249.11 | 6,555 | exact | 0.7 GB | 3 min |
| 315° | 0.1001 | 1.0933 | -0.47° | 127.744 | 249.12 | 6,555 | exact | 0.7 GB | 3 min |

## 1.5 mm air gap

![SIN and COS against the rotor angle at a 1.5 mm air gap](1d5mm_AirGap/results_gap1.5mm.webp)

*Figure 2. SIN (blue) and COS (orange) at a 1.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±1.57 nH and COS ±1.57 nH, that is ±35 and ±35 mV of EMF.*

Best sine fit: SIN amplitude 1.570 nH, offset 0.080 nH, phase -136.0°; COS amplitude 1.574 nH, offset 0.074 nH, phase 134.0°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -1.0095 | 1.1981 | +0.21° | 125.594 | 250.92 | 6,555 | exact | 0.7 GB | 3 min |
| 45° | -1.5035 | 0.1125 | -0.36° | 125.643 | 250.85 | 6,555 | exact | 0.7 GB | 3 min |
| 90° | -1.0346 | -1.0202 | +0.41° | 125.647 | 250.84 | 6,555 | exact | 0.7 GB | 3 min |
| 135° | 0.0437 | -1.5115 | -0.30° | 125.653 | 250.83 | 6,555 | exact | 0.7 GB | 4 min |
| 180° | 1.1727 | -1.0434 | +0.44° | 125.700 | 250.78 | 6,555 | exact | 0.7 GB | 4 min |
| 225° | 1.6511 | 0.0373 | -0.34° | 125.652 | 250.85 | 6,555 | exact | 0.7 GB | 4 min |
| 270° | 1.2001 | 1.1739 | +0.40° | 125.636 | 250.85 | 6,555 | exact | 0.7 GB | 2 min |
| 315° | 0.1201 | 1.6485 | -0.45° | 125.618 | 250.87 | 6,555 | exact | 0.7 GB | 2 min |

## 1 mm air gap

![SIN and COS against the rotor angle at a 1 mm air gap](1mm_AirGap/results_gap1mm.webp)

*Figure 3. SIN (blue) and COS (orange) at a 1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±2.48 nH and COS ±2.49 nH, that is ±55 and ±55 mV of EMF.*

Best sine fit: SIN amplitude 2.481 nH, offset 0.085 nH, phase -137.0°; COS amplitude 2.486 nH, offset 0.080 nH, phase 133.1°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.4° rms and 0.5° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| away | 0.0923 | 0.0833 |  | 132.514 | 244.31 | 3,368 | exact | 0.2 GB | 12 s |
| 0° | -1.6074 | 1.8822 | +0.23° | 121.981 | 253.70 | 6,555 | exact | 0.7 GB | 76 s |
| 45° | -2.4179 | 0.1841 | -0.42° | 122.053 | 253.60 | 6,555 | exact | 0.7 GB | 77 s |
| 90° | -1.7023 | -1.6189 | +0.44° | 122.056 | 253.59 | 6,555 | exact | 0.7 GB | 74 s |
| 135° | -0.0146 | -2.4257 | -0.33° | 122.063 | 253.58 | 6,555 | exact | 0.7 GB | 79 s |
| 180° | 1.7841 | -1.7108 | +0.52° | 122.139 | 253.50 | 6,555 | exact | 0.7 GB | 76 s |
| 225° | 2.5658 | -0.0222 | -0.40° | 122.066 | 253.59 | 6,555 | exact | 0.7 GB | 87 s |
| 270° | 1.8823 | 1.7881 | +0.43° | 122.047 | 253.60 | 6,555 | exact | 0.7 GB | 110 s |
| 315° | 0.1904 | 2.5644 | -0.48° | 122.026 | 253.62 | 6,555 | exact | 0.7 GB | 110 s |

## 0.5 mm air gap

![SIN and COS against the rotor angle at a 0.5 mm air gap](0d5mm_AirGap/results_gap0.5mm.webp)

*Figure 4. SIN (blue) and COS (orange) at a 0.5 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±3.91 nH and COS ±3.92 nH, that is ±86 and ±86 mV of EMF.*

Best sine fit: SIN amplitude 3.915 nH, offset 0.112 nH, phase -139.0°; COS amplitude 3.921 nH, offset 0.108 nH, phase 131.0°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 0.7° rms and 0.8° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -2.4697 | 3.0382 | +0.43° | 115.026 | 259.13 | 6,555 | exact | 0.7 GB | 3 min |
| 45° | -3.8286 | 0.4315 | -0.68° | 115.124 | 259.00 | 6,555 | exact | 0.7 GB | 3 min |
| 90° | -2.7938 | -2.4814 | +0.67° | 115.126 | 258.99 | 6,555 | exact | 0.7 GB | 3 min |
| 135° | -0.2004 | -3.8363 | -0.52° | 115.133 | 258.98 | 6,555 | exact | 0.7 GB | 3 min |
| 180° | 2.7084 | -2.7994 | +0.82° | 115.265 | 258.86 | 6,555 | exact | 0.7 GB | 3 min |
| 225° | 4.0069 | -0.2109 | -0.66° | 115.160 | 258.99 | 6,555 | exact | 0.7 GB | 3 min |
| 270° | 3.0366 | 2.7147 | +0.67° | 115.137 | 259.00 | 6,555 | exact | 0.7 GB | 108 s |
| 315° | 0.4348 | 4.0071 | -0.73° | 115.112 | 259.02 | 6,555 | exact | 0.7 GB | 106 s |

## 0.1 mm air gap

![SIN and COS against the rotor angle at a 0.1 mm air gap](0d1mm_AirGap/results_gap0.1mm.webp)

*Figure 5. SIN (blue) and COS (orange) at a 0.1 mm air gap: the mutual inductance from the TX against the rotor's angle, 8 of 8 angles solved. Each dot is one FastHenry solve and the solid line joins them; the dotted lines are the ideal sine and cosine, each channel's best sine fit, which is what the angle error is measured against. SIN swings ±5.31 nH and COS ±5.32 nH, that is ±117 and ±117 mV of EMF.*

Best sine fit: SIN amplitude 5.314 nH, offset 0.172 nH, phase -142.4°; COS amplitude 5.319 nH, offset 0.170 nH, phase 127.6°. Angle error, with the offset and gain of each channel calibrated out (worked out as below): 1.5° rms and 1.8° at worst, in electrical degrees, the same as mechanical degrees here. SIN and COS are 90.0° apart, against 90° for perfect quadrature.

| Rotor | M SIN (nH) | M COS (nH) | Angle error | L TX (nH) | R TX (mΩ) | Filaments | Reciprocity | Memory | Time |
|---|---|---|---|---|---|---|---|---|---|
| 0° | -3.1478 | 4.3071 | +1.20° | 102.065 | 275.59 | 6,555 | exact | 0.7 GB | 3 min |
| 45° | -5.1416 | 1.0064 | -1.51° | 102.155 | 275.55 | 6,555 | exact | 0.7 GB | 3 min |
| 90° | -3.9272 | -3.1588 | +1.47° | 102.155 | 275.54 | 6,555 | exact | 0.7 GB | 3 min |
| 135° | -0.6401 | -5.1494 | -1.26° | 102.162 | 275.53 | 6,555 | exact | 0.7 GB | 4 min |
| 180° | 3.5236 | -3.9250 | +1.76° | 102.355 | 275.51 | 6,555 | exact | 0.7 GB | 4 min |
| 225° | 5.3958 | -0.6524 | -1.51° | 102.255 | 275.56 | 6,555 | exact | 0.7 GB | 4 min |
| 270° | 4.3074 | 3.5308 | +1.51° | 102.231 | 275.58 | 6,555 | exact | 0.7 GB | 2 min |
| 315° | 1.0071 | 5.3975 | -1.65° | 102.206 | 275.58 | 6,555 | exact | 0.7 GB | 2 min |

## The air gaps together

![SIN and COS at each air gap](SINCOS_gaps.webp)

*Figure 6. Every air gap on one chart, the 0.1 mm gap in full colour, the solves of each joined by a solid line, and each gap's ideal sine and cosine dotted. Going from 2 to 0.1 mm makes SIN 5.23 times and COS 5.22 times larger.*

## Against the expectation

The generator estimates the TX at 130 nH with the rotor away and 106 nH with it (its drop with the rotor is an upper estimate). FastHenry gives 132.5 nH with the rotor away, and 127.7 to 127.8 nH with the rotor at 2 mm, and 125.6 to 125.7 nH with the rotor at 1.5 mm, and 122.0 to 122.1 nH with the rotor at 1 mm, and 115.0 to 115.3 nH with the rotor at 0.5 mm, and 102.1 to 102.4 nH with the rotor at 0.1 mm. The expected values are in [expected_results.json](expected_results.json).

## How the angle error is worked out

Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS); the error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is. The rms and the worst of them are the angle error. The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair. [`angle_error.py`](../FastHenry%20Simulation/angle_error.py) does it.

## The boards

![stator and rotor](../S0_1x_OD21_2L_tiny_TXtop_stator_and_rotor.webp)

*Drawn by the generator. Red is the top layer, blue the bottom; the dots are vias. In FastHenry, SIN is opened at (97.74, 102.26) and COS at (97.74, 97.74), the TX at its ends at (109.8, 100) (KiCad mm). The [README](../README.md) has the board and how it was made.*

![how the stator and rotor are set up in FastHenry](../S0_1x_OD21_2L_tiny_TXtop_fasthenry_setup.webp)

*How the boards are set up in FastHenry, drawn by [`rig_picture.py`](../FastHenry%20Simulation/rig_picture.py) from the model simulation.py solves: the stator's tracks as segments split into filaments, the rotor copper side down over the stator as a grid of bars, each receiver opened at a left-out via (the port is between where its tracks reach the via on the two layers, and the receiver is open there, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*
