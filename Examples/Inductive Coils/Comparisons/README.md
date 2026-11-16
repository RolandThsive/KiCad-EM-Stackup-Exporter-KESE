# Comparisons

Each board folder beside this one stands on its own and holds the same files: its boards, its geometry, the same five scripts, and its own results. This folder is extra, for our own understanding: it sets the boards side by side. Nothing here is solved; the three scripts read each board's `Results/` and print the tables below, and two of them draw the charts.

The signal is each receiver's mutual inductance from the TX, M = V / (jωI), with 1 A at 3.5 MHz in the TX, so 1 nH is 22 mV of EMF. A solve is **not converged** when it stopped above a residual of 5e-4 or gives the TX a negative resistance.

| Board | What it is |
|---|---|
| [S0_1x_OD21_2L_tiny](../S0_1x_OD21_2L_tiny/) | S0: 21 mm across, the TX one turn on each layer, SIN and COS opened at a left-out via |
| [S0_1x_OD21_2L_tiny_TXtop](../S0_1x_OD21_2L_tiny_TXtop/) | S0 with the TX two turns on the top layer; the generator narrows the RX band to fit them |
| [S0_1x_OD22_2L_tiny_TXtop](../S0_1x_OD22_2L_tiny_TXtop/) | the TX two turns on the top layer around S0's own RX coils, the board grown to 22.2 mm |
| [S0_1x_OD22_2L_tiny_TXtop_Cut](../S0_1x_OD22_2L_tiny_TXtop_Cut/) | the 22 mm board with SIN and COS opened by a 0.2 mm cut in a top trace instead of a left-out via |
| [S0_1x_OD23_2L_tiny_TX3top_Cut](../S0_1x_OD23_2L_tiny_TX3top_Cut/) | the TX three turns on the top layer around S0's RX coils, 23.4 mm, opened by the same cuts |

## The TX on the top layer against S0

`python compare_boards.py` prints this table first. The amplitude is each board's best sine through all eight solves, as on its own results page.

| Air gap | Board | Angles | Amplitude SIN / COS | Angle error | SIN to COS | L TX over the turn | Residual | Not converged |
|---|---|---|---|---|---|---|---|---|
| 2 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 0.89 / 0.84 nH (19 / 18 mV) | 3.3° rms, 5.1° peak | 91.5° | 106 to 111 nH | 2.8e-04 to 4.2e-04 | 0 of 8 |
| 2 mm | 21 mm, 2 TX turns on top | 8 of 8 | 0.89 / 0.88 nH (19 / 19 mV) | 2.1° rms, 3.9° peak | 91.9° | 111 to 113 nH | 2.8e-04 to 3.7e-04 | 0 of 8 |
| 2 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 1.41 / 1.41 nH (31 / 31 mV) | 1.8° rms, 2.8° peak | 92.0° | 124 to 127 nH | 2.0e-04 to 2.8e-04 | 0 of 8 |
| 1.5 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 1.37 / 1.32 nH (30 / 29 mV) | 3.6° rms, 5.6° peak | 91.8° | 103 to 110 nH | 2.8e-04 to 4.7e-04 | 0 of 8 |
| 1.5 mm | 21 mm, 2 TX turns on top | 8 of 8 | 1.40 / 1.37 nH (31 / 30 mV) | 2.4° rms, 4.0° peak | 92.5° | 109 to 112 nH | 2.8e-04 to 4.1e-04 | 0 of 8 |
| 1.5 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 2.12 / 2.09 nH (47 / 46 mV) | 2.2° rms, 3.3° peak | 91.9° | 122 to 125 nH | 1.9e-04 to 3.3e-04 | 0 of 8 |
| 1 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 2.15 / 2.07 nH (47 / 45 mV) | 4.6° rms, 7.1° peak | 91.2° | 99 to 108 nH | 2.7e-04 to 4.8e-04 | 0 of 8 |
| 1 mm | 21 mm, 2 TX turns on top | 8 of 8 | 2.24 / 2.15 nH (49 / 47 mV) | 3.2° rms, 5.6° peak | 92.7° | 105 to 110 nH | 2.6e-04 to 4.9e-04 | 0 of 8 |
| 1 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 3.25 / 3.14 nH (72 / 69 mV) | 3.0° rms, 4.7° peak | 92.6° | 118 to 123 nH | 1.9e-04 to 6.1e-04 | 1 of 8 |
| 0.5 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 3.26 / 2.81 nH (72 / 62 mV) | 14.3° rms, 28.3° peak | 89.3° | 79 to 106 nH | 2.4e-04 to 1.0e-03 | 3 of 8 |
| 0.5 mm | 21 mm, 2 TX turns on top | 8 of 8 | 3.32 / 3.18 nH (73 / 70 mV) | 3.2° rms, 5.7° peak | 90.1° | 93 to 104 nH | 2.9e-04 to 4.9e-04 | 0 of 8 |
| 0.5 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 4.62 / 4.59 nH (102 / 101 mV) | 2.3° rms, 4.6° peak | 89.2° | 107 to 117 nH | 2.2e-04 to 5.4e-04 | 1 of 8 |
| 0.1 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 2.45 / 5.04 nH (54 / 111 mV) | 67.6° rms, 172.9° peak | 81.5° | 31 to 109 nH | 6.9e-04 to 4.4e-03 | 8 of 8 |
| 0.1 mm | 21 mm, 2 TX turns on top | 8 of 8 | 5.12 / 4.86 nH (113 / 107 mV) | 17.5° rms, 44.0° peak | 70.6° | 67 to 125 nH | 5.2e-04 to 4.5e-03 | 8 of 8 |
| 0.1 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 3.82 / 6.46 nH (84 / 142 mV) | 58.5° rms, 159.3° peak | 66.0° | 43 to 118 nH | 4.1e-04 to 5.8e-03 | 7 of 8 |

* **At 1.5 and 2 mm every solve on all three boards stays below 5e-4.** The 21 mm board with the TX on top gives within 6 % of S0's signal (at 2 mm the SIN amplitudes are the same, 0.885 nH), with less angle error at every gap: 2.4° and 2.1° rms against 3.6° and 3.3°. The 22 mm board gives about 1.6 times S0's signal (2.12 and 1.41 nH for SIN against 1.37 and 0.89) with the cleanest curves of the three: 2.2° and 1.8° rms.
* **Moving the TX to the top layer keeps the signal or raises it.** On S0's 21 mm board, where the RX band narrows to make room, the signal stays about the same (2.24 nH at 1 mm against 2.15). Where S0's RX coils are kept and the board grows to 22 mm, it is 1.4 to 1.6 times S0's from 1 to 2 mm: 3.25 nH at 1 mm (3.05 through the seven converged solves), about 70 mV of EMF at 1 A.
* **The solver copes better with the TX on top.** At 1 and 0.5 mm every solve of the 21 mm board stops below 5e-4 and its angle error is about 3° rms at both gaps; on S0 three of the 0.5 mm solves stalled higher and its 0.5 mm curve is off by 14° rms. On the 22 mm board one solve at each of these gaps (45° both times) stopped just above 5e-4 (6.1e-4 and 5.4e-4), and both still sit near their sine.
* **SIN and COS are matched in amplitude** within 5 % at 1 and 0.5 mm on the 21 mm board and within 4 % and 1 % on the 22 mm board (S0: 4 % at 1 mm, 16 % at 0.5 mm).
* **At 0.1 mm the solver stalls too high to read** on all three boards.

## The cut against the via

The 22 mm board opened two ways: [`S0_1x_OD22_2L_tiny_TXtop`](../S0_1x_OD22_2L_tiny_TXtop/) leaves out one layer-change via of each receiver, and [`S0_1x_OD22_2L_tiny_TXtop_Cut`](../S0_1x_OD22_2L_tiny_TXtop_Cut/) cuts a 0.2 mm gap across a top trace instead, as the real board is opened, and keeps the via. Same boards, same mesh level, same TX port. `python compare_ports.py` prints the table and draws the chart.

![the cut against the via port](SINCOS_cut_vs_via.webp)

*Solve by solve: the cut solid and filled, the via dashed and hollow. Which cut face counts as plus is a convention, so the via board's SIN is drawn with its sign turned, which moves its curve by half a turn and changes nothing else. Rings: solves that are not converged.*

| Air gap | Port | Amplitude SIN / COS, all solves | The same, converged solves only | Angle error | SIN to COS | L TX over the turn | Not converged | Cut against via, where both converged |
|---|---|---|---|---|---|---|---|---|
| 2 mm | via (left out) | 1.41 / 1.41 nH (31 / 31 mV) | 1.41 / 1.41 nH (8 solves) | 1.8° rms, 2.8° peak | 92.0° | 124 to 127 nH | 0 of 8 |  |
| 2 mm | cut | 1.42 / 1.42 nH (31 / 31 mV) | 1.42 / 1.42 nH (8 solves) | 2.2° rms, 3.4° peak | 87.7° | 125 to 127 nH | 0 of 8 | 8 angles; mean difference SIN 1.7 %, COS 1.8 % of the amplitude |
| 1.5 mm | via (left out) | 2.12 / 2.09 nH (47 / 46 mV) | 2.12 / 2.09 nH (8 solves) | 2.2° rms, 3.3° peak | 91.9° | 122 to 125 nH | 0 of 8 |  |
| 1.5 mm | cut | 2.21 / 2.10 nH (49 / 46 mV) | 2.21 / 2.10 nH (8 solves) | 3.2° rms, 5.9° peak | 88.0° | 122 to 126 nH | 0 of 8 | 8 angles; mean difference SIN 3.4 %, COS 1.7 % of the amplitude |
| 1 mm | via (left out) | 3.25 / 3.14 nH (72 / 69 mV) | 3.05 / 3.14 nH (7 solves) | 3.0° rms, 4.7° peak | 92.6° | 118 to 123 nH | 1 of 8 |  |
| 1 mm | cut | 2.81 / 3.14 nH (62 / 69 mV) | 3.05 / 3.14 nH (7 solves) | 4.8° rms, 11.3° peak | 92.6° | 117 to 121 nH | 1 of 8 | 7 angles; mean difference SIN 0.8 %, COS 0.7 % of the amplitude |
| 0.5 mm | via (left out) | 4.62 / 4.59 nH (102 / 101 mV) | 4.70 / 4.59 nH (7 solves) | 2.3° rms, 4.6° peak | 89.2° | 107 to 117 nH | 1 of 8 |  |
| 0.5 mm | cut | 4.39 / 4.46 nH (97 / 98 mV) | 4.32 / 4.46 nH (7 solves) | 1.8° rms, 3.5° peak | 90.4° | 107 to 113 nH | 1 of 8 | 7 angles; mean difference SIN 4.1 %, COS 2.2 % of the amplitude |
| 0.1 mm | via (left out) | 3.82 / 6.46 nH (84 / 142 mV) | fewer than 5 converged | 58.5° rms, 159.3° peak | 66.0° | 43 to 118 nH | 7 of 8 |  |
| 0.1 mm | cut | 5.98 / 6.22 nH (131 / 137 mV) | fewer than 5 converged | 10.9° rms, 24.6° peak | 81.1° | 91 to 122 nH | 6 of 8 | 1 angle; mean difference SIN 7.0 %, COS 1.6 % of the amplitude |

* **At 1.5 and 2 mm the two ports agree at every angle.** All 16 solves converged on each board, and the cut and the via differ on average by 3.4 % (SIN) and 1.7 % (COS) of the amplitude at 1.5 mm, and by 1.7 % and 1.8 % at 2 mm. SIN to COS reads 88° on the cut and 92° on the via: the same 2° from a quarter turn, mirrored because the cut's SIN has the opposite sign.
* **At 1 mm the two ports give the same answer.** At the 7 angles where both converged they differ by 0.8 % (SIN) and 0.7 % (COS) of the amplitude on average, and the fits through those 7 angles are the same to the hundredth: 3.05 / 3.14 nH. The one angle that differs is 45°, which is not converged in either and falls off the sine the opposite way in each. That one solve alone pulls the cut's all-solve SIN amplitude down to 2.81 nH and its angle error up to 4.8° rms.
* **At 0.5 mm they agree within 2.2 % at 5 of the 7 angles both converged** (135° to 315°). At 0° and 90° they differ by up to 0.8 nH although both are below the limit, so the solver's scatter at this gap is about that big. The cut's curve comes out a little cleaner: 1.8° rms against 2.3°.
* **At 0.1 mm both still stall:** 6 of 8 cut solves and 7 of 8 via solves are not converged, so neither curve can be read yet, and the cut's less wild curve (10.9° rms against 58.5°) says nothing about the port.
* **The rotor taken away** gives L TX 130.2 nH with the cut and 129.7 nH with the via.

## Three TX turns against two

[`S0_1x_OD23_2L_tiny_TX3top_Cut`](../S0_1x_OD23_2L_tiny_TX3top_Cut/) against the two-turn board it grew from, [`S0_1x_OD22_2L_tiny_TXtop_Cut`](../S0_1x_OD22_2L_tiny_TXtop_Cut/): the same RX coils and the same cuts, one more TX turn on the top layer, and the board 23.4 mm across instead of 22.2. `python compare_turns.py` prints the table and the ratios and draws the chart.

![two TX turns against three](SINCOS_2_vs_3_turns.webp)

*Above, the amplitude of SIN and COS at each air gap; below, the TX inductance over the turn. Three turns solid and filled, two turns dashed and hollow. Each amplitude is the best sine through the converged solves; at 0.1 mm fewer than five converged on either board, so those points are fitted through all the solves and ringed, as not to be read. Diamonds: L TX with the rotor away.*

| Air gap | TX | Amplitude SIN / COS | Fitted through | Angle error | L TX over the turn | Not converged |
|---|---|---|---|---|---|---|
| 2 mm | 2 turns | 1.42 / 1.42 nH (31 / 31 mV) | the converged solves | 2.2° rms, 3.4° peak | 125 to 127 nH | 0 of 8 |
| 2 mm | 3 turns | 2.18 / 2.19 nH (48 / 48 mV) | the converged solves | 1.7° rms, 2.6° peak | 248 to 252 nH | 0 of 8 |
| 1.5 mm | 2 turns | 2.21 / 2.10 nH (49 / 46 mV) | the converged solves | 3.2° rms, 5.9° peak | 122 to 126 nH | 0 of 8 |
| 1.5 mm | 3 turns | 3.03 / 3.13 nH (67 / 69 mV) | the converged solves | 2.8° rms, 4.3° peak | 241 to 250 nH | 2 of 8 |
| 1 mm | 2 turns | 3.05 / 3.14 nH (67 / 69 mV) | the converged solves | 4.8° rms, 11.3° peak | 117 to 121 nH | 1 of 8 |
| 1 mm | 3 turns | 4.39 / 4.54 nH (97 / 100 mV) | the converged solves | 3.5° rms, 6.8° peak | 229 to 243 nH | 2 of 8 |
| 0.5 mm | 2 turns | 4.32 / 4.46 nH (95 / 98 mV) | the converged solves | 1.8° rms, 3.5° peak | 107 to 113 nH | 1 of 8 |
| 0.5 mm | 3 turns | 6.32 / 6.37 nH (139 / 140 mV) | the converged solves | 2.9° rms, 5.4° peak | 205 to 231 nH | 2 of 8 |
| 0.1 mm | 2 turns | 5.98 / 6.22 nH (131 / 137 mV) | all solves (fewer than 5 converged) | 10.9° rms, 24.6° peak | 91 to 122 nH | 6 of 8 |
| 0.1 mm | 3 turns | 8.94 / 8.15 nH (197 / 179 mV) | all solves (fewer than 5 converged) | 7.4° rms, 10.6° peak | 177 to 291 nH | 7 of 8 |

* **The third turn raises the signal by about half.** From 0.5 to 2 mm, where at least six of the eight solves converged on both boards, SIN and COS are 1.37 to 1.55 times the two-turn board's: 6.3 nH against 4.3 to 4.5 at 0.5 mm, 4.4 to 4.5 against 3.1 at 1 mm, and 2.2 against 1.4 at 2 mm (48 mV of EMF at 1 A against 31).
* **L TX doubles:** 1.96 to 1.98 times the two-turn board's at every gap from 0.5 to 2 mm, and 261.4 nH against 130.2 nH with the rotor away.
* **So per ampere in the TX the signal grows by half, but per volt across it, it shrinks:** at a fixed TX voltage the current falls with L (V = 2πf L I), so the EMF goes with M / L, about 1.5 / 2.0 = 0.75 of the two-turn board's. Which of the two counts depends on what the drive holds fixed.
* **Both boards' curves are clean from 0.5 mm out**, and the three-turn board's are the cleaner at 1, 1.5 and 2 mm (3.5°, 2.8° and 1.7° rms against 4.8°, 3.2° and 2.2°); at 0.5 mm the two-turn board's are (1.8° against 2.9°).
* **At 0.1 mm the solver stalls** on 7 of the 8 three-turn solves and 6 of the 8 two-turn solves, so neither point can be read yet.

## The signal on every board

`python compare_boards.py` prints this table second. Here the amplitude is the best sine through the converged solves where at least five converged; where fewer did it goes through all of them and is marked with ?. 0.1 mm is left out, because the solver stalls there on every board.

| Board | SIN at 0.5 mm | SIN at 1 mm | SIN at 1.5 mm | SIN at 2 mm |
|---|---|---|---|---|
| [S0](../S0_1x_OD21_2L_tiny/) | 3.97 nH (3 of 8 not converged) | 2.15 nH | 1.37 nH | 0.89 nH |
| [21 mm, 2 TX turns on top](../S0_1x_OD21_2L_tiny_TXtop/) | 3.32 nH | 2.24 nH | 1.40 nH | 0.89 nH |
| [22 mm, 2 TX turns on top](../S0_1x_OD22_2L_tiny_TXtop/) | 4.70 nH (1 of 8 not converged) | 3.05 nH (1 of 8 not converged) | 2.12 nH | 1.41 nH |
| [22 mm, 2 TX turns on top, opened by cuts](../S0_1x_OD22_2L_tiny_TXtop_Cut/) | 4.32 nH (1 of 8 not converged) | 3.05 nH (1 of 8 not converged) | 2.21 nH | 1.42 nH |
| [23 mm, 3 TX turns on top, opened by cuts](../S0_1x_OD23_2L_tiny_TX3top_Cut/) | 6.32 nH (2 of 8 not converged) | 4.39 nH (2 of 8 not converged) | 3.03 nH (2 of 8 not converged) | 2.18 nH |

S0's 0.5 mm fit goes through only the five converged solves, and through all eight it is 3.26 nH, so its 0.5 mm value lies somewhere between the two until the solver is fixed.

## Running it

From this folder, with the boards' results in place:

    python compare_boards.py       # the TX on top against S0, and every board's SIN amplitude
    python compare_ports.py        # the cut against the via: the table and SINCOS_cut_vs_via.webp
    python compare_turns.py        # three TX turns against two: the table, the ratios and SINCOS_2_vs_3_turns.webp

`compare_ports.py` and `compare_turns.py` borrow the sine fit and the chart style from a board's `Elmer Simulation/angle_error.py` and `make_charts.py`, so the charts look like the boards' own.

## Licence

This branch's GPL-3.0 covers the three scripts here. The boards they read are output of the Sinusoidal Coil Generator, for non-commercial use only; see [../LICENSE.md](../LICENSE.md).
