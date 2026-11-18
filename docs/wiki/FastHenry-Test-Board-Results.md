# 57. FastHenry Test Board Results

What FastHenry gave on each board of [FastHenry Test Boards](FastHenry-Test-Boards.md), against numbers known
without any solver. Every number here is in the examples' results files on the `FastHenry_Integration` branch
(`Examples/E01_circular_loop/results.json`, `Examples/E02_coaxial_loops/results.json`, and the coil board's
`Results/<gap>_AirGap/results_gap<gap>mm.json`), with the settings, the versions, the model's size, and the time and
peak memory of every solve; each example's `results.md` or `SINCOS_Results.md` has the full tables. The charts are
drawn from those files by the coil board's `make_charts.py`; nothing is drawn by hand.

## 57.1 E01 Circular Loop

One circular trace, 10 mm in radius to its centre line, 0.5 mm wide and 35 µm thick, opened by a 0.2 mm gap.
FastHenry drives 1 A between the two trace ends and closes the loop through the port at no length.

### In Short

E01 is one copper loop on a board, the simplest coil there is. Its inductance L (how much magnetic field 1 A makes)
and its resistance R have textbook formulas. FastHenry drives 1 A through the loop and reads both back:

| What | What it means | The formula | FastHenry |
|---|---|---|---|
| L at 10 kHz | the loop's inductance | 55.590 nH | 55.580 nH with 15 × 3 filaments, −0.02 %, settling from below |
| R at 10 kHz | its resistance, the current spread evenly through the copper | 61.201 mΩ | 61.208 mΩ, +0.011 %: the resistance of the model's own straight chords |
| R at 3.5 MHz | the current crowds to the trace's edges, so R rises | no exact formula | 75.43 mΩ, 1.23 times its 10 kHz value |
| L at 3.5 MHz | the crowded current makes a little less field | about 55.04 nH (an estimate) | 54.80 nH, 1.4 % under its 10 kHz value |

| Item | Value |
|---|---|
| Run | 17 November 2026, FastHenry 3.0.1, KESE 3.4.0's stack-up, Python 3.13 |
| Solver | the dense direct solve, `-s ludecomp -m direct -a off` |
| Model | 126 chords, split into 1 × 1 up to 15 × 3 filaments across × through, the edge ones twice as narrow as the next in |
| Air | none: FastHenry models only the conductors |

### Expected Against What Came Out

| Filaments (across × through) | 1 × 1 | 3 × 1 | 5 × 1 | 9 × 1 | 9 × 3 | 15 × 3 |
|---|---|---|---|---|---|---|
| Filaments in the model | 126 | 378 | 630 | 1,134 | 3,402 | 5,670 |
| L at 10 kHz (reference 55.590 nH) | 55.343 nH (−0.44 %) | 55.474 nH (−0.21 %) | 55.516 nH (−0.13 %) | 55.538 nH (−0.09 %) | 55.579 nH (−0.02 %) | 55.580 nH (−0.02 %) |
| R at 10 kHz (reference 61.201 mΩ) | 61.207 mΩ | 61.208 mΩ | 61.208 mΩ | 61.208 mΩ | 61.208 mΩ | 61.208 mΩ |
| L at 3.5 MHz (estimate about 55.04 nH) | 55.343 nH | 54.899 nH | 54.783 nH | 54.771 nH | 54.801 nH | 54.797 nH |
| R at 3.5 MHz | 61.207 mΩ | 69.946 mΩ | 74.351 mΩ | 75.099 mΩ | 75.375 mΩ | 75.433 mΩ |
| R at 3.5 MHz over R at 10 kHz | 1.00 | 1.14 | 1.21 | 1.23 | 1.23 | 1.23 |

The reference L is Neumann's double integral over the open arc (356°, between the centres of the two round ends,
where FastHenry's segments stop too) with the rectangle's geometric mean distance g = 0.2235 (w + t), after Grover.
The reference R is the annular sector's DC resistance between the arc's two ends. At 3.5 MHz the skin depth (35 µm)
equals the copper's thickness, and no formula is exact there: the same arc integral with a thin strip's
high-frequency GMD, w / 4, gives an estimate that leaves out the current's shift towards the ring's inside edge.

* **L settles from below onto the reference.** It rises from 55.343 to 55.538 nH as the filaments across go from 1
  to 9; three through the copper add 0.04 nH (55.579 nH) and 15 across add nothing more (55.580 nH). The split of the
  section into filaments sets how well the current's spread over the section is drawn. The limit is 0.02 % under
  Neumann's integral: the size of the integral's own approximations (the GMD of a straight bar used on a ring, and
  the chords).
* **R is the chords' DC resistance at 10 kHz** whatever the filaments: 61.208 mΩ, the 126 straight strips' own value,
  worked by hand as 61.207 mΩ, and 0.011 % over the annular sector.
* **At 3.5 MHz the current crowds to the edges**, and only the filaments across can show it: one filament holds the
  current uniform (R stays at 61.21 mΩ), three across give 69.95 mΩ, and from nine across R settles at 75.4 mΩ.
  Three filaments through the copper move R by 0.4 % and L by 0.05 %: the skin depth equals the copper's thickness,
  so the current is spread through it nearly as at DC.

## 57.2 E02 Coaxial Loops

E01's loop twice, TX on F.Cu and RX on B.Cu, 1.565 mm apart. TX carries 1 A and RX is open, so the voltage across
RX's gap gives M.

### In Short

E02 puts a second loop right under the first. A current in the top loop (TX) induces a voltage in the bottom one
(RX), and the ratio is their mutual inductance M: the same coupling that carries the coil board's signal from the TX
to SIN and COS.

| What | What it means | The formula | FastHenry |
|---|---|---|---|
| M at 10 kHz | how strongly the two loops couple | 23.886 nH (Neumann, the open arcs) | 23.892 nH, +0.024 %, the same from 1 × 1 to 9 × 3 filaments |
| M back from the RX to the TX | an exact solve of a passive model is reciprocal | the same M | the same to the last digit, at every rung and both frequencies |
| TX's L and R beside the open RX at 10 kHz | an open loop carries no current round it, so it must leave the TX alone | E01's at the same filaments | E01's to the last digit |
| TX's R at 3.5 MHz | eddy currents in the RX's trace take a little from the TX | a little above E01's | 0.01 to 0.06 % above E01's |

### Expected Against What Came Out

| Filaments (across × through, each loop) | 1 × 1 | 3 × 1 | 5 × 1 | 9 × 1 | 9 × 3 |
|---|---|---|---|---|---|
| Filaments in the model | 252 | 756 | 1,260 | 2,268 | 6,804 |
| M at 10 kHz (reference 23.886 nH) | 23.891 nH (+0.022 %) | 23.892 nH (+0.024 %) | 23.892 nH (+0.024 %) | 23.892 nH (+0.024 %) | 23.892 nH (+0.024 %) |
| M back from the RX to the TX at 10 kHz | the same to the last digit | the same | the same | the same | the same |
| M at 3.5 MHz | 23.891 nH | 23.865 nH | 23.859 nH | 23.857 nH | 23.856 nH |
| TX's L at 10 kHz (E01's at the same filaments) | 55.343 nH (55.343) | 55.474 nH (55.474) | 55.516 nH (55.516) | 55.538 nH (55.538) | 55.578 nH (55.579) |
| TX's R at 3.5 MHz (E01's) | 61.207 mΩ (61.207) | 69.955 mΩ (69.946) | 74.361 mΩ (74.351) | 75.110 mΩ (75.099) | 75.423 mΩ (75.375) |

The reference M is Neumann's double integral for the two open arcs (each 356°, the two gaps one above the other),
averaged over 21 × 21 filaments across both traces' widths. That leaves out the traces' thickness and the current's
slight lean to the inside of a ring.

* **M is 0.024 % over Neumann's integral, and the filaments do not move it.** With one filament per segment FastHenry
  already reads 23.891 nH, because it works out the mutual inductance of two bars from their whole cross-sections,
  not only from their centre lines (one filament on each centre line would give 23.997 nH, 0.5 % more).
* **Reciprocity holds to the last digit**: Z[TX][RX] and Z[RX][TX] are the same number at every rung and both
  frequencies, as FastHenry's direct solve of a symmetric system gives.
* **At 3.5 MHz the RX takes a little from the TX**: M falls 0.15 % from its 10 kHz value, and the TX's R rises over
  E01's. The RX carries no net current round it, but the TX's field drives eddy currents across its trace, filament
  against filament, whose loss shows in the TX's R. One filament across cannot carry any of that, so at 1 × 1
  nothing changes with frequency.

## 57.3 S0d2_1x_OD23_2L_tiny_TX3top_Cut

The coil board: a TX of three turns on the top layer, SIN and COS of two electrical periods per turn, each opened by
a 0.2 mm cut, and a rotor of two sectors. 1 A at 3.5 MHz in the TX; the signal is each receiver's mutual inductance
from the TX, M = V / (jωI), so 1 nH is 22 mV of EMF.

### In Short

When the rotor turns, SIN and COS should trace a sine and a cosine, twice per turn, and their ratio gives the angle.
FastHenry solves the board at 16 angles over the whole turn at each of five air gaps, and once with the rotor away:
81 solves, every one reciprocal to the last digit.

| What | What it means | FastHenry |
|---|---|---|
| SIN's amplitude | the signal: how far SIN swings over a turn | 9.76 nH (215 mV) at 0.1 mm down to 1.95 nH (43 mV) at 2 mm; 4.73 nH (104 mV) at 1 mm |
| SIN against COS | a decoder needs them alike, a quarter period apart | within 0.2 % in amplitude, 89.9° to 90.0° apart, at every gap |
| The angle error | how far atan2(SIN, COS) reads from the true angle, after offset and gain calibration | 0.1° to 0.3° rms from 0.5 to 2 mm, 0.9° rms at 0.1 mm, in electrical degrees (half that in mechanical) |
| L TX with the rotor away | the TX alone | 294.6 nH, against the generator's estimate of 292 nH |
| L TX with the rotor over it | the rotor's eddy currents push the TX's field out | 4.2 % lower at 2 mm, 8.5 % at 1 mm, 20.8 % at 0.1 mm |

| Item | Value |
|---|---|
| Run | 17 and 18 November 2026, FastHenry 3.0.1, KESE 3.4.0's stack-up of both boards, Python 3.13 |
| Solver | the dense direct solve, `-s ludecomp -m direct -a off`, one core per solve |
| Model | 3 filaments across each track and 1 through, the rotor as a grid of 4,542 bars 0.05 mm wide at its edges growing to 0.3 mm: 9,264 filaments; 4,722 with the rotor away |
| Check | reciprocity on every solve: M from the TX to a receiver and from the receiver back must agree within 1 % to be read; every solve agreed to the last digit |

### Expected Against What Came Out

| Air gap | Amplitude SIN / COS | Angle error | SIN to COS | L TX over the turn | R TX over the turn | Solves read |
|---|---|---|---|---|---|---|
| 2 mm | 1.95 / 1.95 nH (43 / 43 mV) | 0.1° rms, 0.3° peak | 89.9° | 282.1 to 282.2 nH | 425.6 to 425.8 mΩ | 16 of 16 |
| 1.5 mm | 3.03 / 3.03 nH (67 / 67 mV) | 0.1° rms, 0.3° peak | 89.9° | 277.3 to 277.5 nH | 429.6 to 429.8 mΩ | 16 of 16 |
| 1 mm | 4.73 / 4.74 nH (104 / 104 mV) | 0.2° rms, 0.3° peak | 90.0° | 269.5 to 269.8 nH | 435.8 to 436.1 mΩ | 16 of 16 |
| 0.5 mm | 7.28 / 7.28 nH (160 / 160 mV) | 0.3° rms, 0.5° peak | 90.0° | 255.6 to 256.1 nH | 447.2 to 447.6 mΩ | 16 of 16 |
| 0.1 mm | 9.76 / 9.77 nH (215 / 215 mV) | 0.9° rms, 1.1° peak | 90.0° | 233.0 to 233.6 nH | 474.6 to 475.0 mΩ | 16 of 16 |
| Rotor away | −0.026 / −0.027 nH | | | 294.6 nH | 413.2 mΩ | 1 of 1 |

The amplitude is each channel's best sine through the gap's 16 solves; the EMF is 2πfM × 1 A.

![SIN and COS against the rotor's angle from 0 to 360° at a 1 mm air gap: SIN in blue and COS in orange, one dot per FastHenry solve every 22.5°, joined by solid lines, with each channel's best sine dotted beside it. Each swings between about −4.8 and +4.7 nH twice over the turn, SIN and COS a quarter of a period apart, and the dots lie on the dotted sines](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/FastHenry-Test-Board-Results/S0d2_1x_OD23_2L_tiny_TX3top_Cut/results_gap1mm.webp)

At 1 mm the best sine fit gives SIN 4.730 nH in amplitude with an offset of −0.031 nH, and COS 4.736 nH with an
offset of −0.025 nH; what the fit leaves is 0.019 and 0.018 nH rms. The curves repeat every 180°, as the two-sector
rotor does: the solves at θ and θ + 180° are the same numbers.

![SIN and COS at every air gap on one chart, against the rotor's angle from 0 to 360°: five pairs of curves, SIN in blues and COS in oranges, the 0.1 mm gap in full colour swinging about ±9.8 nH and each larger gap paler and smaller, down to about ±1.95 nH at 2 mm; each gap's ideal sine and cosine dotted beside its solves](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/FastHenry-Test-Board-Results/S0d2_1x_OD23_2L_tiny_TX3top_Cut/SINCOS_gaps.webp)

Going from 2 to 0.1 mm makes SIN 5.02 times and COS 5.01 times larger.

* **Every solve is reciprocal**: M from the TX to each receiver and from the receiver back to the TX agree to the last
  digit FastHenry writes, as a direct solve of its symmetric matrix must.
* **SIN and COS are a matched pair** at every gap: within 0.2 % of each other in amplitude and 89.9° to 90.0° apart.
* **The angle error grows only at the smallest gap.** It is 0.1° to 0.3° rms from 0.5 to 2 mm and 0.9° rms at
  0.1 mm, where it alternates in sign from one angle to the next: a ripple at four periods per electrical period,
  the fastest the 16 angles can show, which third or fifth harmonics of the coupling would give, and those fade
  faster with the gap than the sine itself.
* **The rotor lowers the TX's inductance and raises its resistance.** L TX is 294.6 nH with the rotor away, 282.2 nH
  at 2 mm and 233.3 nH at 0.1 mm, moving by 0.6 nH at most over the turn; R TX rises from 413.2 mΩ with the rotor away
  to 475 mΩ at 0.1 mm, the loss of the rotor's eddy currents.
* **Against the generator's estimates**: FastHenry's 294.6 nH with the rotor away is 0.9 % over the generator's
  292 nH. With the rotor the generator gives 226 nH, which it calls an upper estimate of the drop; FastHenry gives
  282.2 nH at 2 mm down to 233.3 nH at 0.1 mm.
* **With the rotor away SIN and COS are not quite zero**: −0.026 and −0.027 nH, what is left of the TX's direct
  coupling to them. It is of the size of the fits' offsets, −0.03 nH from 1 to 2 mm.

| Previous | Next |
|:---|---:|
| [FastHenry Test Boards](FastHenry-Test-Boards.md) | [FastHenry Accuracy](FastHenry-Accuracy.md) |
