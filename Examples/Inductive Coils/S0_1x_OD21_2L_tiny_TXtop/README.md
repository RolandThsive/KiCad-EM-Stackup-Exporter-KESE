# S0_1x_OD21_2L_tiny_TXtop

A coil set from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator) (`Coil_2_10.5_1_1_2_Single_SteppedDiagonal`), set up for Elmer by [`../new_coil.py`](../new_coil.py). The steps that made it are in [S0's README](../S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

**What differs from S0.** Only the TX, as Roland asked: two turns, both on the top layer (F.Cu, r = 6.6 and 7.2 mm), instead of S0's one turn on each layer. The parameter files differ from S0's in three values of `TX_Parameters.py`: `TX_TURNS = 2`, `TX_WIRING = "single"`, `TX_LAYER_A = 1`. A spiral of two turns needs its inner end brought back out, so a short tail runs under the turns on B.Cu to the terminal, where the two ends sit stacked as on S0. The generator keeps the board edge, so it narrows the RX band to make room for the second turn (r = 3.2 to 5.5 mm, against 3.2 to 6.1 on S0); the rotor is S0's, file for file.

## The board

Bore and outer radius 2 and 10.5 mm, 2 copper layers, board 0.8 mm, air gap 1 mm by default (any other with `--gap`). 1 electrical period per turn; the rotor has 1 sector and repeats itself every 360°.

![stator and rotor](S0_1x_OD21_2L_tiny_TXtop_stator_and_rotor.webp)

*Drawn by the generator.*

![how the stator and rotor are set up in Elmer](S0_1x_OD21_2L_tiny_TXtop_elmer_setup.webp)

*How the boards sit in Elmer, drawn by `rig_picture.py` from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened at a left-out via (0 A, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*

| Coil | Net | Opened at (KiCad mm) | How |
|---|---|---|---|
| TX | `TX` | (109.8, 100), F.Cu and B.Cu | its two stacked ends |
| SIN | `2` | via at (97.737, 102.263) | the generator found no cut spot; the layer-change via farthest from the TX copper (3.40 mm), of those the farthest from the TX ends; the via is left out |
| COS | `1` | via at (97.737, 97.737) | the generator found no cut spot; the layer-change via farthest from the TX copper (3.40 mm), of those the farthest from the TX ends; the via is left out |

The generator's estimate for the TX: 0.13 µH with the rotor away and 0.11 µH with it, 0.23 Ω DC. Its warnings for this board:

* a via sits only 0.088 mm from other copper (wanted 0.2 mm); phase/node (0, 10)
* the tank's parallel resistance at the nominal air gap may be as low as 12 ohm (if the AC resistance is 2 x the DC value); the IPS2550 needs at least 250 ohm.  More TX turns, wider TX traces, thicker copper or a higher EXCITATION_FREQ_HZ raise it
* no spot on 2 within 30 deg of 0 deg, 4 mm from the other marks, has room for two vias (layers F.Cu, B.Cu); widen SILKSCREEN_SEARCH_SPAN_DEG, lower SILKSCREEN_BREAK_SEPARATION_MM, or cut the coil by hand
* no spot on 1 within 30 deg of 0 deg, 4 mm from the other marks, has room for two vias (layers F.Cu, B.Cu); widen SILKSCREEN_SEARCH_SPAN_DEG, lower SILKSCREEN_BREAK_SEPARATION_MM, or cut the coil by hand

## Results at each air gap

Every angle at every gap, one Elmer solve each: 8 angles at each of 5 gaps, and the rotor taken away at 1 mm. Each gap's curves, fits and angle error are in [`Results/SINCOS_Results.md`](Results/SINCOS_Results.md).

| Air gap | Amplitude SIN / COS | Angle error | Solves below the residual limit | L TX over the turn |
|---|---|---|---|---|
| 2 mm | 0.89 / 0.88 nH (19 / 19 mV) | 2.1° rms, 3.9° peak | 8 of 8 | 111 to 113 nH |
| 1.5 mm | 1.40 / 1.37 nH (31 / 30 mV) | 2.4° rms, 4.0° peak | 8 of 8 | 109 to 112 nH |
| 1 mm | 2.24 / 2.15 nH (49 / 47 mV) | 3.2° rms, 5.6° peak | 8 of 8 | 105 to 110 nH |
| 0.5 mm | 3.32 / 3.18 nH (73 / 70 mV) | 3.2° rms, 5.7° peak | 8 of 8 | 93 to 104 nH |
| 0.1 mm | 5.12 / 4.86 nH (113 / 107 mV) | 17.5° rms, 44.0° peak | 0 of 8 | 67 to 125 nH |

![SIN at each air gap](Results/SINCOS_gaps_SIN.webp)

*SIN at each air gap, one dot per solve; rings mark the solves that stopped above a residual of 5e-4 or give the TX a negative resistance. [`SINCOS_gaps_COS.webp`](Results/SINCOS_gaps_COS.webp) is the same for COS, and [`SINCOS_gaps.webp`](Results/SINCOS_gaps.webp) has both.*

From 0.5 mm out every solve stays below the residual limit and the curves are close to a sine and cosine, with 2.1° to 3.2° rms of angle error. The signal is 3.32 nH for SIN at 0.5 mm and falls to 2.24, 1.40 and 0.89 nH at 1, 1.5 and 2 mm, and SIN and COS match in amplitude within 5 % at each of these gaps. At 0.1 mm the solver stalls at all 8 angles, so that row is not yet the board's answer. With the rotor away L TX is 115.7 nH.

## The folder

| Folder | What is in it |
|---|---|
| [`Boards/`](Boards/) | straight from the generator: the stator and rotor boards, `Parameters.txt`, the pictures and the parameter files it was run with |
| [`3D_Geometry/`](3D_Geometry/) | KESE's export of the stator and rotor (STL solids, `materials.json`, STEP, KESE's report), written by the first run; `source.json` records the board's hash, so a changed board is exported again |
| [`Elmer Simulation/`](Elmer%20Simulation/) | `test_spec.json` (every board fact the simulation needs), `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` (S0's, unchanged), [`RotorStator_AngleSetup/`](Elmer%20Simulation/RotorStator_AngleSetup/) (the rotor over the stator at each angle), and the runs under `case/`, which git ignores |
| [`Results/`](Results/) | `expected_results.json` (the generator's estimates), [`SINCOS_Results.md`](Results/SINCOS_Results.md) with every gap on one page, the charts of every gap together (`SINCOS_gaps.webp`, and `_SIN` and `_COS` apart), and a folder for each air gap (`0d1mm_AirGap`, `0d5mm_AirGap`, `1mm_AirGap`, `1d5mm_AirGap`, `2mm_AirGap`, the point written as d) with the runs' `results_gap<gap>mm.json`, `.csv` and `.webp` |

Beside this README, `S0_1x_OD21_2L_tiny_TXtop_stator_and_rotor.webp` is the generator's picture of the boards and `S0_1x_OD21_2L_tiny_TXtop_elmer_setup.webp` shows how they sit in Elmer.

## Running it

| Air gap | Mesh level | Nodes | Memory a solve |
|---|---|---|---|
| 1 mm | 0.75 | 213,657 | about 12.2 GB (at 57 kB a node) |
| 1.5 mm | 0.75 | about 226,000 | 12.6 to 12.7 GB seen |
| 2 mm | 0.75 | about 239,000 | 13.3 GB seen; the first tries on 15 GB machines were killed for memory, and an 8 GB swapfile let them finish on the same mesh |

If that does not fit the machine, `--level` below the one above makes the mesh coarser and the solve smaller (the memory goes about with the number of nodes).

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
