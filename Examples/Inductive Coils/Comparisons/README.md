# Comparisons

Each board folder beside this one stands on its own and holds the same files: its boards, its geometry, the same five scripts, and its own results. This folder is extra, for our own understanding: it sets the boards side by side. Nothing here is solved; the four scripts read each board's `Results/` and print the tables below, and three of them draw the charts.

The signal is each receiver's mutual inductance from the TX, M = V / (jωI), with 1 A at 3.5 MHz in the TX, so 1 nH is 22 mV of EMF. Every solve is Palace's, on the mesh the boards' pages describe. A solve is **readable** when its linear solve converged, R TX is positive and the TX's L from its port's voltage agrees with the L from the magnetic energy of the whole field within 1 %, and, where SIN and COS were driven in turn too, M from the TX to each agrees with M back within 1 % (`readable()` in the boards' `make_charts.py`); every solve here is readable, the two Ls within 0.01 % of each other at worst. Every chart runs over the whole turn, 0 to 360°.

| Board | What it is |
|---|---|
| [S0_1x_OD21_2L_tiny](../S0_1x_OD21_2L_tiny/) | S0: 21 mm across, the TX one turn on each layer, SIN and COS opened at a left-out via |
| [S0_1x_OD21_2L_tiny_TXtop](../S0_1x_OD21_2L_tiny_TXtop/) | S0 with the TX two turns on the top layer; the generator narrows the RX band to fit them |
| [S0_1x_OD22_2L_tiny_TXtop](../S0_1x_OD22_2L_tiny_TXtop/) | the TX two turns on the top layer around S0's own RX coils, the board grown to 22.2 mm |
| [S0_1x_OD22_2L_tiny_TXtop_Cut](../S0_1x_OD22_2L_tiny_TXtop_Cut/) | the 22 mm board with SIN and COS opened by a 0.2 mm cut in a top trace instead of a left-out via |
| [S0_1x_OD23_2L_tiny_TX3top_Cut](../S0_1x_OD23_2L_tiny_TX3top_Cut/) | the TX three turns on the top layer around S0's RX coils, 23.4 mm, opened by the same cuts |
| [S0d2_1x_OD23_2L_tiny_TX3top_Cut](../S0d2_1x_OD23_2L_tiny_TX3top_Cut/) | the three-turn board with two periods per turn instead of one: the RX coils and a rotor of two sectors, opened by cuts, solved at 16 angles over the whole turn |

## The TX on the top layer against S0

`python compare_boards.py` prints this table first. The amplitude is each board's best sine through all its solves, as on its own results page.

| Air gap | Board | Angles | Amplitude SIN / COS | Angle error | SIN to COS | L TX over the turn | Checks | Not readable |
|---|---|---|---|---|---|---|---|---|
| 2 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 1.23 / 1.23 nH (27 / 27 mV) | 0.2° rms, 0.2° peak | 90.0° | 122.9 to 123.0 nH | L within 0.001 %, M reciprocal within 0.0001 % | 0 of 8 |
| 2 mm | 21 mm, 2 TX turns on top | 8 of 8 | 1.00 / 1.00 nH (22 / 22 mV) | 0.4° rms, 0.6° peak | 89.9° | 120.5 to 120.6 nH | L within 0.001 %, M reciprocal within 9.7e-05 % | 0 of 8 |
| 2 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 1.49 / 1.50 nH (33 / 33 mV) | 0.2° rms, 0.3° peak | 89.9° | 132.9 to 133.0 nH | L within 0.002 %, M reciprocal within 0.00018 % | 0 of 8 |
| 1.5 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 1.88 / 1.88 nH (41 / 41 mV) | 0.1° rms, 0.2° peak | 90.0° | 121.2 to 121.3 nH | L within 0.001 %, M reciprocal within 3.1e-05 % | 0 of 8 |
| 1.5 mm | 21 mm, 2 TX turns on top | 8 of 8 | 1.53 / 1.54 nH (34 / 34 mV) | 0.4° rms, 0.6° peak | 89.9° | 118.4 to 118.5 nH | L within 0.001 %, M reciprocal within 0.00015 % | 0 of 8 |
| 1.5 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 2.23 / 2.23 nH (49 / 49 mV) | 0.2° rms, 0.3° peak | 90.0° | 130.4 to 130.5 nH | L within 0.002 %, M reciprocal within 0.00013 % | 0 of 8 |
| 1 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 2.93 / 2.93 nH (64 / 64 mV) | 0.1° rms, 0.1° peak | 90.0° | 118.3 to 118.4 nH | L within 0.001 %, M reciprocal within 0.00013 % | 0 of 8 |
| 1 mm | 21 mm, 2 TX turns on top | 8 of 8 | 2.42 / 2.42 nH (53 / 53 mV) | 0.4° rms, 0.6° peak | 90.0° | 114.7 to 114.9 nH | L within 0.001 %, M reciprocal within 4.7e-05 % | 0 of 8 |
| 1 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 3.37 / 3.37 nH (74 / 74 mV) | 0.2° rms, 0.3° peak | 90.0° | 126.2 to 126.3 nH | L within 0.002 %, M reciprocal within 1.4e-05 % | 0 of 8 |
| 0.5 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 4.62 / 4.62 nH (102 / 102 mV) | 0.1° rms, 0.1° peak | 90.0° | 113.0 to 113.2 nH | L within 0.001 %, M reciprocal within 2.3e-05 % | 0 of 8 |
| 0.5 mm | 21 mm, 2 TX turns on top | 8 of 8 | 3.82 / 3.82 nH (84 / 84 mV) | 0.7° rms, 0.8° peak | 90.0° | 107.9 to 108.2 nH | L within 0.001 %, M reciprocal within 5.4e-05 % | 0 of 8 |
| 0.5 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 5.07 / 5.07 nH (111 / 112 mV) | 0.4° rms, 0.5° peak | 90.0° | 118.4 to 118.6 nH | L within 0.002 %, M reciprocal within 4.1e-05 % | 0 of 8 |
| 0.1 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 6.44 / 6.44 nH (142 / 142 mV) | 0.5° rms, 0.6° peak | 90.0° | 103.0 to 103.3 nH | L within 0.001 %, M reciprocal within 3.4e-05 % | 0 of 8 |
| 0.1 mm | 21 mm, 2 TX turns on top | 8 of 8 | 5.20 / 5.20 nH (114 / 114 mV) | 1.5° rms, 1.7° peak | 90.0° | 94.8 to 95.2 nH | L within 0.002 %, M reciprocal within 6.6e-06 % | 0 of 8 |
| 0.1 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 6.66 / 6.66 nH (146 / 146 mV) | 1.1° rms, 1.3° peak | 90.0° | 103.9 to 104.2 nH | L within 0.002 %, M reciprocal within 1e-05 % | 0 of 8 |

* **Every solve on all three boards is readable**, and every curve is close to a sine and cosine: SIN and COS within 0.3 % of each other in amplitude and 89.9° to 90.0° apart.
* **On S0's 21 mm board, moving the TX to the top layer costs 17 to 19 % of the signal.** Where the generator narrows the RX band to make room, SIN is 0.81 to 0.83 times S0's at every gap (2.42 nH against 2.93 at 1 mm), with more angle error of 0.4° rms from 1 to 2 mm, against 0.1° to 0.2° on S0.
* **Where S0's RX coils are kept and the board grows to 22 mm, the signal rises,** to 1.03 times S0's at 0.1 mm and 1.21 times at 2 mm (3.37 nH against 2.93 at 1 mm, 74 mV of EMF at 1 A), with 0.2° to 0.4° rms of angle error from 0.5 to 2 mm.
* **S0 has the cleanest curves:** 0.1° to 0.2° rms of angle error from 0.5 to 2 mm.
* **At 0.1 mm the angle error rises on every board** (0.5°, 1.5° and 1.1° rms) and alternates in sign from one angle to the next: a ripple at four periods per turn. That is the fourth harmonic two-coil sensors typically show, which the third and fifth harmonics of the sine and cosine both give (Kuntz, Gerlach and Fella, arXiv 2503.14627), and it fades with the gap faster than the sine itself.

## The cut against the via

The 22 mm board opened two ways: [`S0_1x_OD22_2L_tiny_TXtop`](../S0_1x_OD22_2L_tiny_TXtop/) leaves out one layer-change via of each receiver, and [`S0_1x_OD22_2L_tiny_TXtop_Cut`](../S0_1x_OD22_2L_tiny_TXtop_Cut/) cuts a 0.2 mm gap across a top trace instead, as the real board is opened, and keeps the via. Same boards, same mesh settings, same TX port. `python compare_ports.py` prints the table and draws the chart.

![the cut against the via port](SINCOS_cut_vs_via.webp)

*Solve by solve: the cut solid and filled, the via dashed and hollow. Which side of a port counts as plus is a convention, and here both boards use the same one. A ring would mark a solve that is not readable (none is).*

| Air gap | Port | Amplitude SIN / COS, all solves | The same, readable solves only | Angle error | SIN to COS | L TX over the turn | Not readable | Cut against via, where both are readable |
|---|---|---|---|---|---|---|---|---|
| 2 mm | via (left out) | 1.49 / 1.50 nH (33 / 33 mV) | 1.49 / 1.50 nH (8 solves) | 0.2° rms, 0.3° peak | 89.9° | 132.9 to 133.0 nH | 0 of 8 |  |
| 2 mm | cut | 1.49 / 1.50 nH (33 / 33 mV) | 1.49 / 1.50 nH (8 solves) | 0.2° rms, 0.3° peak | 90.0° | 132.9 to 133.0 nH | 0 of 8 | 8 angles; mean difference SIN 0.1 %, COS 0.1 % of the amplitude |
| 1.5 mm | via (left out) | 2.23 / 2.23 nH (49 / 49 mV) | 2.23 / 2.23 nH (8 solves) | 0.2° rms, 0.3° peak | 90.0° | 130.4 to 130.5 nH | 0 of 8 |  |
| 1.5 mm | cut | 2.23 / 2.23 nH (49 / 49 mV) | 2.23 / 2.23 nH (8 solves) | 0.2° rms, 0.2° peak | 90.0° | 130.4 to 130.5 nH | 0 of 8 | 8 angles; mean difference SIN 0.0 %, COS 0.1 % of the amplitude |
| 1 mm | via (left out) | 3.37 / 3.37 nH (74 / 74 mV) | 3.37 / 3.37 nH (8 solves) | 0.2° rms, 0.3° peak | 90.0° | 126.2 to 126.3 nH | 0 of 8 |  |
| 1 mm | cut | 3.37 / 3.37 nH (74 / 74 mV) | 3.37 / 3.37 nH (8 solves) | 0.2° rms, 0.3° peak | 90.0° | 126.2 to 126.3 nH | 0 of 8 | 8 angles; mean difference SIN 0.0 %, COS 0.0 % of the amplitude |
| 0.5 mm | via (left out) | 5.07 / 5.07 nH (111 / 112 mV) | 5.07 / 5.07 nH (8 solves) | 0.4° rms, 0.5° peak | 90.0° | 118.4 to 118.6 nH | 0 of 8 |  |
| 0.5 mm | cut | 5.07 / 5.08 nH (111 / 112 mV) | 5.07 / 5.08 nH (8 solves) | 0.4° rms, 0.5° peak | 90.0° | 118.4 to 118.6 nH | 0 of 8 | 8 angles; mean difference SIN 0.0 %, COS 0.0 % of the amplitude |
| 0.1 mm | via (left out) | 6.66 / 6.66 nH (146 / 146 mV) | 6.66 / 6.66 nH (8 solves) | 1.1° rms, 1.3° peak | 90.0° | 103.9 to 104.2 nH | 0 of 8 |  |
| 0.1 mm | cut | 6.66 / 6.66 nH (146 / 147 mV) | 6.66 / 6.66 nH (8 solves) | 1.1° rms, 1.3° peak | 90.0° | 103.9 to 104.2 nH | 0 of 8 | 8 angles; mean difference SIN 0.0 %, COS 0.1 % of the amplitude |

* **The two ports give the same curves, within 0.2 % of the amplitude.** Solve by solve they differ by 0.00 to 0.01 nH at most, which is 0.1 % of the amplitude at 0.1 mm and 0.2 % at 2 mm, since part of the difference is a small offset that stays as the signal falls.
* **SIN to COS is 89.9° to 90.0° on both,** the angle error is the same at every gap, and L TX is the same: 138.9 nH with the rotor away on both.
* **Where a port's sheet stands hardly matters here.** In Palace a port is a sheet across the opening with a resistance across it, and the receiver's voltage is the field along the sheet. The via board's sheet stands between the via's two pads, 0.7 mm through the board; the cut board's fills the 0.2 mm cut across the top trace. The two close the receiver's loop over different paths, and the 0.01 nH between them at most is all that changes; the real board's reading also includes its leads, which neither model has.

## Three TX turns against two

[`S0_1x_OD23_2L_tiny_TX3top_Cut`](../S0_1x_OD23_2L_tiny_TX3top_Cut/) against the two-turn board it grew from, [`S0_1x_OD22_2L_tiny_TXtop_Cut`](../S0_1x_OD22_2L_tiny_TXtop_Cut/): the same RX coils and the same cuts, one more TX turn on the top layer, and the board 23.4 mm across instead of 22.2. `python compare_turns.py` prints the table and the ratios and draws the chart.

![two TX turns against three](SINCOS_2_vs_3_turns.webp)

*Above, the amplitude of SIN and COS at each air gap; below, the TX inductance over the turn. Three turns solid and filled, two turns dashed and hollow. Each amplitude is the best sine through the readable solves, all eight on both boards at every gap. Diamonds: L TX with the rotor away.*

| Air gap | TX | Amplitude SIN / COS | Fitted through | Angle error | L TX over the turn | Not readable |
|---|---|---|---|---|---|---|
| 2 mm | 2 turns | 1.49 / 1.50 nH (33 / 33 mV) | the readable solves | 0.2° rms, 0.3° peak | 132.9 to 133.0 nH | 0 of 8 |
| 2 mm | 3 turns | 2.36 / 2.37 nH (52 / 52 mV) | the readable solves | 0.3° rms, 0.4° peak | 266.4 to 266.6 nH | 0 of 8 |
| 1.5 mm | 2 turns | 2.23 / 2.23 nH (49 / 49 mV) | the readable solves | 0.2° rms, 0.2° peak | 130.4 to 130.5 nH | 0 of 8 |
| 1.5 mm | 3 turns | 3.43 / 3.43 nH (75 / 76 mV) | the readable solves | 0.3° rms, 0.4° peak | 260.6 to 260.8 nH | 0 of 8 |
| 1 mm | 2 turns | 3.37 / 3.37 nH (74 / 74 mV) | the readable solves | 0.2° rms, 0.3° peak | 126.2 to 126.3 nH | 0 of 8 |
| 1 mm | 3 turns | 5.03 / 5.04 nH (111 / 111 mV) | the readable solves | 0.3° rms, 0.5° peak | 251.0 to 251.4 nH | 0 of 8 |
| 0.5 mm | 2 turns | 5.07 / 5.08 nH (111 / 112 mV) | the readable solves | 0.4° rms, 0.5° peak | 118.4 to 118.6 nH | 0 of 8 |
| 0.5 mm | 3 turns | 7.31 / 7.32 nH (161 / 161 mV) | the readable solves | 0.6° rms, 0.7° peak | 234.7 to 235.2 nH | 0 of 8 |
| 0.1 mm | 2 turns | 6.66 / 6.66 nH (146 / 147 mV) | the readable solves | 1.1° rms, 1.3° peak | 103.9 to 104.2 nH | 0 of 8 |
| 0.1 mm | 3 turns | 9.38 / 9.39 nH (206 / 206 mV) | the readable solves | 1.2° rms, 1.5° peak | 208.6 to 209.2 nH | 0 of 8 |

* **The third turn raises the signal by 1.41 times at 0.1 mm, and more as the gap grows, to 1.58 times at 2 mm:** 9.38 nH against 6.66 at 0.1 mm, 5.03 against 3.37 at 1 mm, and 2.36 against 1.49 at 2 mm (52 mV of EMF at 1 A against 33).
* **L TX doubles:** 1.98 to 2.01 times the two-turn board's at every gap, and 281.4 nH against 138.9 nH with the rotor away.
* **So per ampere in the TX the signal grows, but per volt across it, it shrinks:** at a fixed TX voltage the current falls with L (V = 2πf L I), so the EMF goes with M / L, 0.70 of the two-turn board's at 0.1 mm and 0.79 at 2 mm. Which of the two counts depends on what the drive holds fixed.
* **Both boards' curves are clean at every gap:** three turns 0.3° rms of angle error from 1 to 2 mm, 0.6° at 0.5 mm and 1.2° at 0.1 mm; two turns 0.2° rms of angle error from 1 to 2 mm, 0.4° at 0.5 mm and 1.1° at 0.1 mm.

## Two periods per turn against one

[`S0d2_1x_OD23_2L_tiny_TX3top_Cut`](../S0d2_1x_OD23_2L_tiny_TX3top_Cut/) against [`S0_1x_OD23_2L_tiny_TX3top_Cut`](../S0_1x_OD23_2L_tiny_TX3top_Cut/): the same TX of three turns on the top layer and the same 23.4 mm board, both opened by cuts, but the RX coils have two periods per turn instead of one, and the rotor two copper sectors, so its period is 180°. The two-period board is solved at 16 angles over the whole turn, eight per period, so that both boards have the same eight points per period. `python compare_periods.py` prints the table and the ratios and draws the chart.

![one period per turn against two](SINCOS_1_vs_2_periods.webp)

*Above, the amplitude of SIN and COS at each air gap (SIN lies under COS: the two match within 0.2 %); below, the angle error in mechanical degrees. Two periods solid and filled, one period dashed and hollow. Each amplitude is the best sine through the readable solves: all 16 on the two-period board and all eight on the other, at every gap.*

| Air gap | Periods per turn | Amplitude SIN / COS | Angle error, electrical | Angle error, mechanical | L TX over the turn | Not readable |
|---|---|---|---|---|---|---|
| 2 mm | 1 | 2.36 / 2.37 nH (52 / 52 mV) | 0.3° rms, 0.4° peak | 0.29° rms, 0.39° peak | 266.4 to 266.6 nH | 0 of 8 |
| 2 mm | 2 | 1.91 / 1.92 nH (42 / 42 mV) | 0.1° rms, 0.2° peak | 0.06° rms, 0.12° peak | 269.0 to 269.2 nH | 0 of 16 |
| 1.5 mm | 1 | 3.43 / 3.43 nH (75 / 76 mV) | 0.3° rms, 0.4° peak | 0.30° rms, 0.40° peak | 260.6 to 260.8 nH | 0 of 8 |
| 1.5 mm | 2 | 2.97 / 2.98 nH (65 / 65 mV) | 0.1° rms, 0.3° peak | 0.07° rms, 0.15° peak | 264.2 to 264.5 nH | 0 of 16 |
| 1 mm | 1 | 5.03 / 5.04 nH (111 / 111 mV) | 0.3° rms, 0.5° peak | 0.35° rms, 0.45° peak | 251.0 to 251.4 nH | 0 of 8 |
| 1 mm | 2 | 4.65 / 4.66 nH (102 / 102 mV) | 0.2° rms, 0.4° peak | 0.10° rms, 0.18° peak | 256.2 to 256.7 nH | 0 of 16 |
| 0.5 mm | 1 | 7.31 / 7.32 nH (161 / 161 mV) | 0.6° rms, 0.7° peak | 0.57° rms, 0.72° peak | 234.7 to 235.2 nH | 0 of 8 |
| 0.5 mm | 2 | 7.18 / 7.19 nH (158 / 158 mV) | 0.4° rms, 0.6° peak | 0.19° rms, 0.28° peak | 242.4 to 243.0 nH | 0 of 16 |
| 0.1 mm | 1 | 9.38 / 9.39 nH (206 / 206 mV) | 1.2° rms, 1.5° peak | 1.23° rms, 1.46° peak | 208.6 to 209.2 nH | 0 of 8 |
| 0.1 mm | 2 | 9.71 / 9.71 nH (213 / 213 mV) | 0.9° rms, 1.2° peak | 0.45° rms, 0.58° peak | 219.3 to 220.1 nH | 0 of 16 |

* **The signal is about the same up close and falls faster with the gap:** two periods give 1.03 times the one-period signal at 0.1 mm, 0.92 times at 1 mm and 0.81 times at 2 mm (1.91 nH against 2.36). A pattern with twice the periods is finer, and a finer field pattern fades faster with distance.
* **In mechanical degrees, the angle error is 0.20 to 0.28 times the one-period board's from 1 to 2 mm:** 0.45° rms against 1.23° at 0.1 mm, and 0.06 to 0.10° against 0.29 to 0.35° from 1 to 2 mm. In electrical degrees it is 0.1° to 0.2° against 0.3° from 1 to 2 mm, and each electrical degree is half a mechanical one.
* **The TX hardly changes:** L TX is 1.01 to 1.05 times the one-period board's.
* **What two periods give up:** the reading repeats every 180°, so the sensor alone cannot tell which half of the turn the rotor is in. What they should gain beyond these centred solves: a rotor off-centre moves a one-period board's curves directly, while with two periods that first-order effect cancels.

## The signal on every board

`python compare_boards.py` prints this table second. Here the amplitude is the best sine through the readable solves where at least five are readable; where fewer are it goes through all of them and is marked with ?. Every solve is readable, so none is marked.

| Board | SIN at 0.1 mm | SIN at 0.5 mm | SIN at 1 mm | SIN at 1.5 mm | SIN at 2 mm |
|---|---|---|---|---|---|
| [S0](../S0_1x_OD21_2L_tiny/) | 6.44 nH | 4.62 nH | 2.93 nH | 1.88 nH | 1.23 nH |
| [21 mm, 2 TX turns on top](../S0_1x_OD21_2L_tiny_TXtop/) | 5.20 nH | 3.82 nH | 2.42 nH | 1.53 nH | 1.00 nH |
| [22 mm, 2 TX turns on top](../S0_1x_OD22_2L_tiny_TXtop/) | 6.66 nH | 5.07 nH | 3.37 nH | 2.23 nH | 1.49 nH |
| [22 mm, 2 TX turns on top, opened by cuts](../S0_1x_OD22_2L_tiny_TXtop_Cut/) | 6.66 nH | 5.07 nH | 3.37 nH | 2.23 nH | 1.49 nH |
| [23 mm, 3 TX turns on top, opened by cuts](../S0_1x_OD23_2L_tiny_TX3top_Cut/) | 9.38 nH | 7.31 nH | 5.03 nH | 3.43 nH | 2.36 nH |
| [23 mm, 3 TX turns on top, opened by cuts, 2 periods per turn](../S0d2_1x_OD23_2L_tiny_TX3top_Cut/) | 9.71 nH | 7.18 nH | 4.65 nH | 2.97 nH | 1.91 nH |

The two three-turn boards give the most signal. With one period per turn it is 1.46 times S0's at 0.1 mm and 1.91 times at 2 mm, the most at every gap from 0.5 mm out; with two periods it is a little more at 0.1 mm (9.71 nH) and falls faster after that, to 1.91 nH at 2 mm. The 21 mm board with the TX on top gives the least.

## Running it

From this folder, with the boards' results in place:

    python compare_boards.py       # the TX on top against S0, and every board's SIN amplitude
    python compare_ports.py        # the cut against the via: the table and SINCOS_cut_vs_via.webp
    python compare_turns.py        # three TX turns against two: the table, the ratios and SINCOS_2_vs_3_turns.webp
    python compare_periods.py      # two periods per turn against one: the table, the ratios and SINCOS_1_vs_2_periods.webp

`compare_ports.py`, `compare_turns.py` and `compare_periods.py` borrow the sine fit and the chart style from a board's `Palace Simulation/angle_error.py` and `make_charts.py`, so the charts look like the boards' own.

## Licence

This branch's GPL-3.0 covers the four scripts here. The boards they read are output of the Sinusoidal Coil Generator, for non-commercial use only; see [../LICENSE.md](../LICENSE.md).
