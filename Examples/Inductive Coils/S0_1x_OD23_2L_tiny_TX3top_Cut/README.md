# S0_1x_OD23_2L_tiny_TX3top_Cut

A coil set from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator) (`Coil_2_11.7_1_1_3_Single_SteppedDiagonal`), set up for Elmer by [`../new_coil.py`](../new_coil.py). The steps that made it are in [S0's README](../S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

**What differs from S0.** The TX: three turns, all on the top layer (F.Cu, r = 7.2, 7.8 and 8.4 mm), instead of S0's one turn on each layer. S0's RX coils are kept exactly (band r = 3.2 to 6.1 mm), the board edge is fitted to the TX and the rotor to the stator, so the board grows to make room for the turns: 23.4 mm across instead of 21, and the rotor copper reaches r = 9.0 mm instead of 7.8. The parameter files are those of [`../S0_1x_OD22_2L_tiny_TXtop`](../S0_1x_OD22_2L_tiny_TXtop) (the same board with two TX turns) with one change, `TX_TURNS = 3` in `TX_Parameters.py`, run with the generator at commit 32bf9cb. A spiral needs its inner end brought back out, so a short tail runs under the turns on B.Cu to the terminal, where the two ends sit stacked as on S0.

**SIN and COS are opened by a 0.2 mm cut across a top trace**, because that is how the real board is opened and routed to the IC. The voltage across each cut is the receiver's open-circuit EMF, reported as the mutual inductance M = V / (jωI) with 1 A in the TX. The cut is made in the model; the board files are as the generator wrote them. `test_spec.json` sets `"rx_port": "cut"` and gives each receiver a `cut` (where, which way the trace runs, 0.2 mm long, 0.4 mm across), and `simulation.py` takes the copper inside that box out of the top copper. The receivers' layer-change vias all stay in.

## The board

Bore and outer radius 2 and 11.7 mm, 2 copper layers, board 0.8 mm, air gap 1 mm by default (any other with `--gap`). 1 electrical period per turn; the rotor has 1 sector and repeats itself every 360°.

![stator and rotor](S0_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp)

*Drawn by the generator.*

![where SIN and COS are opened](S0_1x_OD23_2L_tiny_TX3top_Cut_cuts.webp)

*Each cut is the spot on the receiver's top trace nearest its layer-change via where a 0.2 mm cut has at least 0.45 mm of free board round it and sits at least 0.75 mm from any via centre: 0.86 mm from the via on both receivers. The two spots are a quarter turn apart about the axis, as SIN and COS are.*

![how the stator and rotor are set up in Elmer](S0_1x_OD23_2L_tiny_TX3top_Cut_elmer_setup.webp)

*How the boards sit in Elmer, drawn by `rig_picture.py` from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened by the cut, and the TX opened between its two stacked ends, where 1 A is driven. The copper inside each cut box is air. The two copper faces that border the gap are the terminal's electrodes, and the port sheet spans the gap at the copper's lower face, as in Elmer's E01 example. SIN and COS carry 0 A, so the voltage across the gap is the open-circuit EMF. The outline of each cut is drawn into the 2D mesh, so both cut faces are meshed exactly. [`Elmer Simulation/RotorStator_AngleSetup/`](Elmer%20Simulation/RotorStator_AngleSetup/) has the rotor over the stator at each of the 8 angles, with the two cuts and the TX port ringed (`python angle_setup.py`).*

| Coil | Net | Opened at (KiCad mm) | How |
|---|---|---|---|
| TX | `TX` | (111, 100), F.Cu and B.Cu | its two stacked ends |
| SIN | `2` | cut at (97.160, 101.626), F.Cu | a 0.2 mm gap across the top trace, running (-0.63, -0.78); the via at (97.737, 102.263) stays |
| COS | `1` | cut at (98.374, 97.160), F.Cu | a 0.2 mm gap across the top trace, running (0.78, -0.63); the via at (97.737, 97.737) stays |

The generator's estimate for the TX: 0.29 µH with the rotor away and 0.23 µH with it, 0.38 Ω DC. Its warnings for this board:

* the tank's parallel resistance at the nominal air gap may be as low as 32 ohm (if the AC resistance is 2 x the DC value); the IPS2550 needs at least 250 ohm.  More TX turns, wider TX traces, thicker copper or a higher EXCITATION_FREQ_HZ raise it
* no spot on 2 within 30 deg of 0 deg, 4 mm from the other marks, has room for two vias (layers F.Cu, B.Cu); widen SILKSCREEN_SEARCH_SPAN_DEG, lower SILKSCREEN_BREAK_SEPARATION_MM, or cut the coil by hand
* no spot on 1 within 30 deg of 0 deg, 4 mm from the other marks, has room for two vias (layers F.Cu, B.Cu); widen SILKSCREEN_SEARCH_SPAN_DEG, lower SILKSCREEN_BREAK_SEPARATION_MM, or cut the coil by hand

## Results at each air gap

Every angle at every gap, one Elmer solve each: 8 angles at each of 5 gaps, and the rotor taken away at 1 mm. Each gap's curves, fits and angle error are in [`Results/SINCOS_Results.md`](Results/SINCOS_Results.md).

| Air gap | Amplitude SIN / COS | Angle error | Solves below the residual limit | L TX over the turn |
|---|---|---|---|---|
| 2 mm | 2.18 / 2.19 nH (48 / 48 mV) | 1.7° rms, 2.6° peak | 8 of 8 | 248 to 252 nH |
| 1.5 mm | 3.26 / 3.17 nH (72 / 70 mV) | 2.8° rms, 4.3° peak | 6 of 8 | 241 to 250 nH |
| 1 mm | 4.28 / 4.62 nH (94 / 102 mV) | 3.5° rms, 6.8° peak | 6 of 8 | 229 to 243 nH |
| 0.5 mm | 6.43 / 6.27 nH (141 / 138 mV) | 2.9° rms, 5.4° peak | 6 of 8 | 205 to 231 nH |
| 0.1 mm | 8.94 / 8.15 nH (197 / 179 mV) | 7.4° rms, 10.6° peak | 1 of 8 | 177 to 291 nH |

![SIN at each air gap](Results/SINCOS_gaps_SIN.webp)

*SIN at each air gap, one dot per solve; rings mark the solves that stopped above a residual of 5e-4 or give the TX a negative resistance. [`SINCOS_gaps_COS.webp`](Results/SINCOS_gaps_COS.webp) is the same for COS, and [`SINCOS_gaps.webp`](Results/SINCOS_gaps.webp) has both.*

From 0.5 mm out the curves are close to a sine and cosine, with 1.7° to 3.5° rms of angle error, and SIN and COS match in amplitude within 8 %. Every 2 mm solve stays below the residual limit; at 0.5, 1 and 1.5 mm two of the eight stop just above it, none above 7.2e-4. The signal is 6.43 nH for SIN at 0.5 mm and falls to 4.28, 3.26 and 2.18 nH at 1, 1.5 and 2 mm (141 down to 48 mV of EMF at 1 A). L TX is 205 to 252 nH with the rotor between 0.5 and 2 mm and 261.4 nH with it away, where the generator estimated 226 and 292 nH. At 0.1 mm the solver stalls at 7 of the 8 angles, so that row is not yet the board's answer.

## The folder

| Folder | What is in it |
|---|---|
| [`Boards/`](Boards/) | straight from the generator: the stator and rotor boards, `Parameters.txt`, the pictures and the parameter files it was run with |
| [`3D_Geometry/`](3D_Geometry/) | KESE's export of the stator and rotor (STL solids, `materials.json`, STEP, KESE's report), written by the first run; `source.json` records the board's hash, so a changed board is exported again |
| [`Elmer Simulation/`](Elmer%20Simulation/) | `test_spec.json` (every board fact the simulation needs, with `"rx_port": "cut"` and each receiver's `cut`), `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` (S0's, unchanged), [`RotorStator_AngleSetup/`](Elmer%20Simulation/RotorStator_AngleSetup/) (the rotor over the stator at each angle), and the runs under `case/`, which git ignores |
| [`Results/`](Results/) | `expected_results.json` (the generator's estimates), [`SINCOS_Results.md`](Results/SINCOS_Results.md) with every gap on one page, the charts of every gap together (`SINCOS_gaps.webp`, and `_SIN` and `_COS` apart), and a folder for each air gap (`0d1mm_AirGap`, `0d5mm_AirGap`, `1mm_AirGap`, `1d5mm_AirGap`, `2mm_AirGap`, the point written as d) with the runs' `results_gap<gap>mm.json`, `.csv` and `.webp` |

Beside this README, `S0_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp` is the generator's picture of the boards, `S0_1x_OD23_2L_tiny_TX3top_Cut_elmer_setup.webp` shows how they sit in Elmer, and `S0_1x_OD23_2L_tiny_TX3top_Cut_cuts.webp` shows where SIN and COS are opened.

## Running it

| Air gap | Mesh level | Nodes | Memory a solve |
|---|---|---|---|
| 1 mm | 0.75 | 257,362 | about 14.7 GB (at 57 kB a node) |
| 2 mm | 0.75 | 288,278 | about 16.4 GB |

A larger gap adds air layers to the mesh, so it needs more memory. Where that does not fit, a swapfile lets the solve finish on the same mesh, which is how every solve here ran: on 15 GB machines each held 13.3 GB in memory and put the rest in an 8 GB swapfile. If that does not fit the machine either, `--level` below the one above makes the mesh coarser and the solve smaller (the memory goes about with the number of nodes).

    cd "Elmer Simulation"
    python simulation.py                   # the rotor away, then 0, 45, 90, 135, 180, 225, 270, 315 degrees
    python simulation.py --gap 0.5         # the same at a 0.5 mm air gap
    python simulation.py --plot            # redraw the table, the curves and SINCOS_Results.md
    python angle_error.py                  # print the angle error at each angle, and rewrite SINCOS_Results.md
    python make_charts.py                  # redraw every chart (WebP) and rewrite SINCOS_Results.md
    python rig_picture.py                  # redraw how the boards sit in Elmer
    python angle_setup.py                  # redraw the rotor at each angle

`SINCOS_Results.md` is rewritten after every solve: each gap's graph with a caption, the fit, the angle error at each angle and every solve.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [../LICENSE.md](../LICENSE.md); this branch's GPL-3.0 covers `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` only.
