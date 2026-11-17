# Comparisons

Each board folder beside this one stands on its own and holds the same files: its boards, its geometry, the same five scripts, and its own results. This folder is extra, for our own understanding: it sets the boards side by side. Nothing here is solved; the three scripts read each board's `Results/` and print the tables below, and two of them draw the charts.

The signal is each receiver's mutual inductance from the TX, M = V / (jωI), with 1 A at 3.5 MHz in the TX, so 1 nH is 22 mV of EMF. Every solve is direct (MUMPS, mesh level 0.25). A solve is **readable** when the TX's L and R from its voltage agree with the L from the field energy and the R from the eddy power within 1 % (`readable()` in the boards' `make_charts.py`); every solve here does, within 0.007 %.

| Board | What it is |
|---|---|
| [S0_1x_OD21_2L_tiny](../S0_1x_OD21_2L_tiny/) | S0: 21 mm across, the TX one turn on each layer, SIN and COS opened at a left-out via |
| [S0_1x_OD21_2L_tiny_TXtop](../S0_1x_OD21_2L_tiny_TXtop/) | S0 with the TX two turns on the top layer; the generator narrows the RX band to fit them |
| [S0_1x_OD22_2L_tiny_TXtop](../S0_1x_OD22_2L_tiny_TXtop/) | the TX two turns on the top layer around S0's own RX coils, the board grown to 22.2 mm |
| [S0_1x_OD22_2L_tiny_TXtop_Cut](../S0_1x_OD22_2L_tiny_TXtop_Cut/) | the 22 mm board with SIN and COS opened by a 0.2 mm cut in a top trace instead of a left-out via |
| [S0_1x_OD23_2L_tiny_TX3top_Cut](../S0_1x_OD23_2L_tiny_TX3top_Cut/) | the TX three turns on the top layer around S0's RX coils, 23.4 mm, opened by the same cuts |

## The TX on the top layer against S0

`python compare_boards.py` prints this table first. The amplitude is each board's best sine through all eight solves, as on its own results page.

| Air gap | Board | Angles | Amplitude SIN / COS | Angle error | SIN to COS | L TX over the turn | L and R checks | Not readable |
|---|---|---|---|---|---|---|---|---|
| 2 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 1.18 / 1.18 nH (26 / 26 mV) | 0.3° rms, 0.6° peak | 89.8° | 118.7 to 118.8 nH | within 0.003 % | 0 of 8 |
| 2 mm | 21 mm, 2 TX turns on top | 8 of 8 | 0.96 / 0.96 nH (21 / 21 mV) | 0.4° rms, 0.7° peak | 89.8° | 117.0 to 117.1 nH | within 0.004 % | 0 of 8 |
| 2 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 1.44 / 1.44 nH (32 / 32 mV) | 0.3° rms, 0.6° peak | 90.1° | 129.1 to 129.2 nH | within 0.003 % | 0 of 8 |
| 1.5 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 1.80 / 1.80 nH (40 / 40 mV) | 0.2° rms, 0.4° peak | 89.9° | 117.0 to 117.2 nH | within 0.003 % | 0 of 8 |
| 1.5 mm | 21 mm, 2 TX turns on top | 8 of 8 | 1.49 / 1.49 nH (33 / 33 mV) | 0.4° rms, 0.5° peak | 89.8° | 115.0 to 115.1 nH | within 0.003 % | 0 of 8 |
| 1.5 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 2.15 / 2.15 nH (47 / 47 mV) | 0.2° rms, 0.5° peak | 90.1° | 126.6 to 126.8 nH | within 0.004 % | 0 of 8 |
| 1 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 2.81 / 2.82 nH (62 / 62 mV) | 0.1° rms, 0.3° peak | 89.9° | 114.2 to 114.4 nH | within 0.003 % | 0 of 8 |
| 1 mm | 21 mm, 2 TX turns on top | 8 of 8 | 2.35 / 2.35 nH (52 / 52 mV) | 0.4° rms, 0.6° peak | 89.9° | 111.5 to 111.7 nH | within 0.002 % | 0 of 8 |
| 1 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 3.26 / 3.26 nH (72 / 72 mV) | 0.2° rms, 0.4° peak | 90.0° | 122.6 to 122.8 nH | within 0.002 % | 0 of 8 |
| 0.5 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 4.45 / 4.46 nH (98 / 98 mV) | 0.1° rms, 0.2° peak | 89.9° | 109.1 to 109.3 nH | within 0.003 % | 0 of 8 |
| 0.5 mm | 21 mm, 2 TX turns on top | 8 of 8 | 3.71 / 3.71 nH (82 / 82 mV) | 0.7° rms, 0.9° peak | 89.9° | 104.8 to 105.1 nH | within 0.002 % | 0 of 8 |
| 0.5 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 4.92 / 4.92 nH (108 / 108 mV) | 0.4° rms, 0.5° peak | 90.0° | 115.1 to 115.3 nH | within 0.003 % | 0 of 8 |
| 0.1 mm | S0 (21 mm, TX one turn on each layer) | 8 of 8 | 6.22 / 6.23 nH (137 / 137 mV) | 0.5° rms, 0.6° peak | 89.9° | 99.3 to 99.6 nH | within 0.003 % | 0 of 8 |
| 0.1 mm | 21 mm, 2 TX turns on top | 8 of 8 | 5.06 / 5.06 nH (111 / 111 mV) | 1.5° rms, 1.8° peak | 89.9° | 92.0 to 92.3 nH | within 0.004 % | 0 of 8 |
| 0.1 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 6.47 / 6.47 nH (142 / 142 mV) | 1.1° rms, 1.3° peak | 90.0° | 100.7 to 101.1 nH | within 0.003 % | 0 of 8 |

* **Every solve on all three boards is readable**, and every curve is close to a sine and cosine: SIN and COS within 0.5 % of each other in amplitude and 89.8° to 90.1° apart.
* **On S0's 21 mm board, moving the TX to the top layer costs about a sixth of the signal.** Where the generator narrows the RX band to make room, SIN is 0.81 to 0.84 times S0's at every gap (2.35 nH against 2.81 at 1 mm), with a little more angle error (0.4° rms from 1 to 2 mm, against 0.1° to 0.3°).
* **Where S0's RX coils are kept and the board grows to 22 mm, the signal rises,** from 1.04 times S0's at 0.1 mm to 1.22 times at 2 mm (3.26 nH against 2.81 at 1 mm, 72 mV of EMF at 1 A), with 0.2° to 0.4° rms of angle error from 0.5 to 2 mm.
* **S0 has the cleanest curves:** 0.1° to 0.3° rms of angle error from 0.5 to 2 mm.
* **At 0.1 mm the angle error rises on every board** (0.5°, 1.5° and 1.1° rms) and alternates in sign from one angle to the next: a ripple at four periods per turn, which a finer mesh (level 0.4, on the 21 mm board with the TX on top) leaves as it is, so it comes from the boards' own higher harmonics, not the mesh.
* **These replace the iterative results of before 17 November**, which had the boards with the TX on top ahead of S0. S0's stalled solves read its signal about a quarter low (2.15 nH at 1 mm against 2.81 now), while the 22 mm board's were close (3.25 against 3.26).

## The cut against the via

The 22 mm board opened two ways: [`S0_1x_OD22_2L_tiny_TXtop`](../S0_1x_OD22_2L_tiny_TXtop/) leaves out one layer-change via of each receiver, and [`S0_1x_OD22_2L_tiny_TXtop_Cut`](../S0_1x_OD22_2L_tiny_TXtop_Cut/) cuts a 0.2 mm gap across a top trace instead, as the real board is opened, and keeps the via. Same boards, same mesh level, same TX port. `python compare_ports.py` prints the table and draws the chart.

![the cut against the via port](SINCOS_cut_vs_via.webp)

*Solve by solve: the cut solid and filled, the via dashed and hollow. Which cut face counts as plus is a convention, so the via board's SIN is drawn with its sign turned, which moves its curve by half a turn and changes nothing else. A ring would mark a solve that is not readable (none is).*

| Air gap | Port | Amplitude SIN / COS, all solves | The same, readable solves only | Angle error | SIN to COS | L TX over the turn | Not readable | Cut against via, where both are readable |
|---|---|---|---|---|---|---|---|---|
| 2 mm | via (left out) | 1.44 / 1.44 nH (32 / 32 mV) | 1.44 / 1.44 nH (8 solves) | 0.3° rms, 0.6° peak | 90.1° | 129.1 to 129.2 nH | 0 of 8 |  |
| 2 mm | cut | 1.44 / 1.45 nH (32 / 32 mV) | 1.44 / 1.45 nH (8 solves) | 0.3° rms, 0.4° peak | 89.8° | 129.0 to 129.2 nH | 0 of 8 | 8 angles; mean difference SIN 0.4 %, COS 0.5 % of the amplitude |
| 1.5 mm | via (left out) | 2.15 / 2.15 nH (47 / 47 mV) | 2.15 / 2.15 nH (8 solves) | 0.2° rms, 0.5° peak | 90.1° | 126.6 to 126.8 nH | 0 of 8 |  |
| 1.5 mm | cut | 2.15 / 2.16 nH (47 / 47 mV) | 2.15 / 2.16 nH (8 solves) | 0.2° rms, 0.3° peak | 89.9° | 126.6 to 126.8 nH | 0 of 8 | 8 angles; mean difference SIN 0.2 %, COS 0.3 % of the amplitude |
| 1 mm | via (left out) | 3.26 / 3.26 nH (72 / 72 mV) | 3.26 / 3.26 nH (8 solves) | 0.2° rms, 0.4° peak | 90.0° | 122.6 to 122.8 nH | 0 of 8 |  |
| 1 mm | cut | 3.26 / 3.27 nH (72 / 72 mV) | 3.26 / 3.27 nH (8 solves) | 0.2° rms, 0.3° peak | 89.9° | 122.6 to 122.8 nH | 0 of 8 | 8 angles; mean difference SIN 0.1 %, COS 0.2 % of the amplitude |
| 0.5 mm | via (left out) | 4.92 / 4.92 nH (108 / 108 mV) | 4.92 / 4.92 nH (8 solves) | 0.4° rms, 0.5° peak | 90.0° | 115.1 to 115.3 nH | 0 of 8 |  |
| 0.5 mm | cut | 4.91 / 4.92 nH (108 / 108 mV) | 4.91 / 4.92 nH (8 solves) | 0.4° rms, 0.5° peak | 90.0° | 115.1 to 115.2 nH | 0 of 8 | 8 angles; mean difference SIN 0.1 %, COS 0.1 % of the amplitude |
| 0.1 mm | via (left out) | 6.47 / 6.47 nH (142 / 142 mV) | 6.47 / 6.47 nH (8 solves) | 1.1° rms, 1.3° peak | 90.0° | 100.7 to 101.1 nH | 0 of 8 |  |
| 0.1 mm | cut | 6.47 / 6.48 nH (142 / 142 mV) | 6.47 / 6.48 nH (8 solves) | 1.1° rms, 1.3° peak | 90.0° | 100.7 to 101.0 nH | 0 of 8 | 8 angles; mean difference SIN 0.1 %, COS 0.1 % of the amplitude |

* **The two ports give the same curves at every gap.** At no angle do they differ by more than 0.017 nH, which is 0.2 % of the amplitude at 0.1 mm and 1.2 % at 2 mm; on average they differ by 0.1 % to 0.5 %. The fits agree within 0.01 nH.
* **SIN to COS is 89.8° to 90.0° on the cut and 90.0° to 90.1° on the via,** and the angle error is the same within 0.2° at every gap.
* **L TX is the same on both** at every gap, and 134.6 nH with the rotor away on both (134.61 nH with the cut, 134.59 nH with the via).
* So a cut in a top trace, as the real board is opened, reads the same as a left-out via. The differences the iterative results showed at 0.5 and 1 mm (up to 0.8 nH) were the stalled solver's, not the ports'.

## Three TX turns against two

[`S0_1x_OD23_2L_tiny_TX3top_Cut`](../S0_1x_OD23_2L_tiny_TX3top_Cut/) against the two-turn board it grew from, [`S0_1x_OD22_2L_tiny_TXtop_Cut`](../S0_1x_OD22_2L_tiny_TXtop_Cut/): the same RX coils and the same cuts, one more TX turn on the top layer, and the board 23.4 mm across instead of 22.2. `python compare_turns.py` prints the table and the ratios and draws the chart.

![two TX turns against three](SINCOS_2_vs_3_turns.webp)

*Above, the amplitude of SIN and COS at each air gap; below, the TX inductance over the turn. Three turns solid and filled, two turns dashed and hollow. Each amplitude is the best sine through the readable solves, all eight on both boards at every gap. Diamonds: L TX with the rotor away.*

| Air gap | TX | Amplitude SIN / COS | Fitted through | Angle error | L TX over the turn | Not readable |
|---|---|---|---|---|---|---|
| 2 mm | 2 turns | 1.44 / 1.45 nH (32 / 32 mV) | the readable solves | 0.3° rms, 0.4° peak | 129.0 to 129.2 nH | 0 of 8 |
| 2 mm | 3 turns | 2.29 / 2.29 nH (50 / 50 mV) | the readable solves | 0.3° rms, 0.6° peak | 260.0 to 260.3 nH | 0 of 8 |
| 1.5 mm | 2 turns | 2.15 / 2.16 nH (47 / 47 mV) | the readable solves | 0.2° rms, 0.3° peak | 126.6 to 126.8 nH | 0 of 8 |
| 1.5 mm | 3 turns | 3.32 / 3.32 nH (73 / 73 mV) | the readable solves | 0.3° rms, 0.5° peak | 254.2 to 254.5 nH | 0 of 8 |
| 1 mm | 2 turns | 3.26 / 3.27 nH (72 / 72 mV) | the readable solves | 0.2° rms, 0.3° peak | 122.6 to 122.8 nH | 0 of 8 |
| 1 mm | 3 turns | 4.88 / 4.88 nH (107 / 107 mV) | the readable solves | 0.3° rms, 0.6° peak | 245.0 to 245.3 nH | 0 of 8 |
| 0.5 mm | 2 turns | 4.91 / 4.92 nH (108 / 108 mV) | the readable solves | 0.4° rms, 0.5° peak | 115.1 to 115.2 nH | 0 of 8 |
| 0.5 mm | 3 turns | 7.10 / 7.10 nH (156 / 156 mV) | the readable solves | 0.6° rms, 0.8° peak | 228.8 to 229.2 nH | 0 of 8 |
| 0.1 mm | 2 turns | 6.47 / 6.48 nH (142 / 142 mV) | the readable solves | 1.1° rms, 1.3° peak | 100.7 to 101.0 nH | 0 of 8 |
| 0.1 mm | 3 turns | 9.12 / 9.12 nH (201 / 201 mV) | the readable solves | 1.2° rms, 1.5° peak | 202.8 to 203.3 nH | 0 of 8 |

* **The third turn raises the signal by 1.41 times at 0.1 mm, and more as the gap grows, to 1.59 times at 2 mm:** 9.12 nH against 6.47 at 0.1 mm, 4.88 against 3.26 at 1 mm, and 2.29 against 1.44 at 2 mm (50 mV of EMF at 1 A against 32).
* **L TX doubles:** 1.99 to 2.01 times the two-turn board's at every gap, and 273.3 nH against 134.6 nH with the rotor away.
* **So per ampere in the TX the signal grows by a half or more, but per volt across it, it shrinks:** at a fixed TX voltage the current falls with L (V = 2πf L I), so the EMF goes with M / L, 0.70 of the two-turn board's at 0.1 mm and 0.79 at 2 mm. Which of the two counts depends on what the drive holds fixed.
* **Both boards' curves are clean at every gap:** three turns 0.3° rms of angle error from 1 to 2 mm, 0.6° at 0.5 mm and 1.2° at 0.1 mm; two turns 0.2° to 0.4° from 0.5 to 2 mm and 1.1° at 0.1 mm.

## The signal on every board

`python compare_boards.py` prints this table second. Here the amplitude is the best sine through the readable solves where at least five are readable; where fewer are it goes through all of them and is marked with ?. Every solve is readable, so none is marked.

| Board | SIN at 0.1 mm | SIN at 0.5 mm | SIN at 1 mm | SIN at 1.5 mm | SIN at 2 mm |
|---|---|---|---|---|---|
| [S0](../S0_1x_OD21_2L_tiny/) | 6.22 nH | 4.45 nH | 2.81 nH | 1.80 nH | 1.18 nH |
| [21 mm, 2 TX turns on top](../S0_1x_OD21_2L_tiny_TXtop/) | 5.06 nH | 3.71 nH | 2.35 nH | 1.49 nH | 0.96 nH |
| [22 mm, 2 TX turns on top](../S0_1x_OD22_2L_tiny_TXtop/) | 6.47 nH | 4.92 nH | 3.26 nH | 2.15 nH | 1.44 nH |
| [22 mm, 2 TX turns on top, opened by cuts](../S0_1x_OD22_2L_tiny_TXtop_Cut/) | 6.47 nH | 4.91 nH | 3.26 nH | 2.15 nH | 1.44 nH |
| [23 mm, 3 TX turns on top, opened by cuts](../S0_1x_OD23_2L_tiny_TX3top_Cut/) | 9.12 nH | 7.10 nH | 4.88 nH | 3.32 nH | 2.29 nH |

The three-turn board gives the most signal at every gap, 1.47 times S0's at 0.1 mm and 1.94 times at 2 mm; the 21 mm board with the TX on top gives the least.

## Running it

From this folder, with the boards' results in place:

    python compare_boards.py       # the TX on top against S0, and every board's SIN amplitude
    python compare_ports.py        # the cut against the via: the table and SINCOS_cut_vs_via.webp
    python compare_turns.py        # three TX turns against two: the table, the ratios and SINCOS_2_vs_3_turns.webp

`compare_ports.py` and `compare_turns.py` borrow the sine fit and the chart style from a board's `Elmer Simulation/angle_error.py` and `make_charts.py`, so the charts look like the boards' own.

## Licence

This branch's GPL-3.0 covers the three scripts here. The boards they read are output of the Sinusoidal Coil Generator, for non-commercial use only; see [../LICENSE.md](../LICENSE.md).
