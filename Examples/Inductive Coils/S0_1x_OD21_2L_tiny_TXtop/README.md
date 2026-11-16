# S0_1x_OD21_2L_tiny_TXtop

A coil set from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator) (`Coil_2_10.5_1_1_2_Single_SteppedDiagonal`), set up for Elmer by [`../new_coil.py`](../new_coil.py). The steps that made it are in [S0's README](../S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

**What differs from S0.** Only the TX, as Roland asked: two turns, both on the top layer (F.Cu, r = 6.6 and 7.2 mm), instead of S0's one turn on each layer. The parameter files differ from S0's in three values of `TX_Parameters.py`: `TX_TURNS = 2`, `TX_WIRING = "single"`, `TX_LAYER_A = 1`. A spiral of two turns needs its inner end brought back out, so a short tail runs under the turns on B.Cu to the terminal, where the two ends sit stacked as on S0. The generator keeps the board edge, so it narrows the RX band to make room for the second turn (r = 3.2 to 5.5 mm, against 3.2 to 6.1 on S0); the rotor is S0's, file for file.

## The board

Bore and outer radius 2 and 10.5 mm, 2 copper layers, board 0.8 mm, air gap 1 mm by default (any other with `--gap`). 1 electrical period(s) per turn; the rotor has 1 sector(s) and repeats itself every 360°.

![stator and rotor](S0_1x_OD21_2L_tiny_TXtop_stator_and_rotor.webp)

*Drawn by the generator.*

![how the stator and rotor are set up in Elmer](S0_1x_OD21_2L_tiny_TXtop_elmer_setup.webp)

*How the boards sit in Elmer, drawn by `rig_picture.py` from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened at a left-out via (0 A, so the voltage across it is the open-circuit EMF), and the TX opened between its two stacked ends, where 1 A is driven.*

| Coil | Net | Opened at (KiCad mm) | How |
|---|---|---|---|
| TX | `TX` | (109.8, 100), F.Cu and B.Cu | its two stacked ends |
| SIN | `2` | via at (97.737, 102.263) | the generator found no cut spot; the layer-change via farthest from the TX copper (3.40 mm), of those the farthest from the TX ends; the via is left out |
| COS | `1` | via at (97.737, 97.737) | the generator found no cut spot; the layer-change via farthest from the TX copper (3.40 mm), of those the farthest from the TX ends; the via is left out |

The generator's warnings for this board:

* a via sits only 0.088 mm from other copper (wanted 0.2 mm); phase/node (0, 10)
* the tank's parallel resistance at the nominal air gap may be as low as 12 ohm (if the AC resistance is 2 x the DC value); the IPS2550 needs at least 250 ohm.  More TX turns, wider TX traces, thicker copper or a higher EXCITATION_FREQ_HZ raise it
* no spot on 2 within 30 deg of 0 deg, 4 mm from the other marks, has room for two vias (layers F.Cu, B.Cu); widen SILKSCREEN_SEARCH_SPAN_DEG, lower SILKSCREEN_BREAK_SEPARATION_MM, or cut the coil by hand
* no spot on 1 within 30 deg of 0 deg, 4 mm from the other marks, has room for two vias (layers F.Cu, B.Cu); widen SILKSCREEN_SEARCH_SPAN_DEG, lower SILKSCREEN_BREAK_SEPARATION_MM, or cut the coil by hand

## Against S0

Every angle at every gap, one Elmer solve each, run in parallel: 25 machines for 1, 0.5 and 0.1 mm (24 angles and the rotor taken away), and 16 more for 1.5 and 2 mm. The numbers are from [`Results/SINCOS_Results.md`](Results/SINCOS_Results.md) and S0's, with the [22 mm board](../S0_1x_OD22_2L_tiny_TXtop) (the same TX, S0's RX kept) for reference. "Not converged" counts the solves that stopped above a residual of 5e-4 or give the TX a negative resistance.

| Air gap | Board | Angles | Amplitude SIN / COS | Angle error | SIN to COS | L TX over the turn | Residual | Not converged |
|---|---|---|---|---|---|---|---|---|
| 2 mm | S0 (TX: 1 turn on each layer) | 8 of 8 | 0.89 / 0.84 nH (19 / 18 mV) | 3.3° rms, 5.1° peak | 91.5° | 106 to 111 nH | 2.8e-04 to 4.2e-04 | 0 of 8 |
| 2 mm | this board (21 mm, 2 TX turns on top) | 8 of 8 | 0.89 / 0.88 nH (19 / 19 mV) | 2.1° rms, 3.9° peak | 91.9° | 111 to 113 nH | 2.8e-04 to 3.7e-04 | 0 of 8 |
| 2 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 1.41 / 1.41 nH (31 / 31 mV) | 1.8° rms, 2.8° peak | 92.0° | 124 to 127 nH | 2.0e-04 to 2.8e-04 | 0 of 8 |
| 1.5 mm | S0 (TX: 1 turn on each layer) | 8 of 8 | 1.37 / 1.32 nH (30 / 29 mV) | 3.6° rms, 5.6° peak | 91.8° | 103 to 110 nH | 2.8e-04 to 4.7e-04 | 0 of 8 |
| 1.5 mm | this board (21 mm, 2 TX turns on top) | 8 of 8 | 1.40 / 1.37 nH (31 / 30 mV) | 2.4° rms, 4.0° peak | 92.5° | 109 to 112 nH | 2.8e-04 to 4.1e-04 | 0 of 8 |
| 1.5 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 2.12 / 2.09 nH (47 / 46 mV) | 2.2° rms, 3.3° peak | 91.9° | 122 to 125 nH | 1.9e-04 to 3.3e-04 | 0 of 8 |
| 1 mm | S0 (TX: 1 turn on each layer) | 8 of 8 | 2.15 / 2.07 nH (47 / 45 mV) | 4.6° rms, 7.1° peak | 91.2° | 99 to 108 nH | 2.7e-04 to 4.8e-04 | 0 of 8 |
| 1 mm | this board (21 mm, 2 TX turns on top) | 8 of 8 | 2.24 / 2.15 nH (49 / 47 mV) | 3.2° rms, 5.6° peak | 92.7° | 105 to 110 nH | 2.6e-04 to 4.9e-04 | 0 of 8 |
| 1 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 3.25 / 3.14 nH (72 / 69 mV) | 3.0° rms, 4.7° peak | 92.6° | 118 to 123 nH | 1.9e-04 to 6.1e-04 | 1 of 8 |
| 0.5 mm | S0 (TX: 1 turn on each layer) | 8 of 8 | 3.26 / 2.81 nH (72 / 62 mV) | 14.3° rms, 28.3° peak | 89.3° | 79 to 106 nH | 2.4e-04 to 1.0e-03 | 3 of 8 |
| 0.5 mm | this board (21 mm, 2 TX turns on top) | 8 of 8 | 3.32 / 3.18 nH (73 / 70 mV) | 3.2° rms, 5.7° peak | 90.1° | 93 to 104 nH | 2.9e-04 to 4.9e-04 | 0 of 8 |
| 0.5 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 4.62 / 4.59 nH (102 / 101 mV) | 2.3° rms, 4.6° peak | 89.2° | 107 to 117 nH | 2.2e-04 to 5.4e-04 | 1 of 8 |
| 0.1 mm | S0 (TX: 1 turn on each layer) | 8 of 8 | 2.45 / 5.04 nH (54 / 111 mV) | 67.6° rms, 172.9° peak | 81.5° | 31 to 109 nH | 6.9e-04 to 4.4e-03 | 8 of 8 |
| 0.1 mm | this board (21 mm, 2 TX turns on top) | 8 of 8 | 5.12 / 4.86 nH (113 / 107 mV) | 17.5° rms, 44.0° peak | 70.6° | 67 to 125 nH | 5.2e-04 to 4.5e-03 | 8 of 8 |
| 0.1 mm | 22 mm, 2 TX turns on top, S0's RX | 8 of 8 | 3.82 / 6.46 nH (84 / 142 mV) | 58.5° rms, 159.3° peak | 66.0° | 43 to 118 nH | 4.1e-04 to 5.8e-03 | 7 of 8 |

* **At 1.5 and 2 mm every solve on all three boards stays below 5e-4.** The signal falls to 1.40 / 1.37 nH at 1.5 mm and 0.89 / 0.88 nH at 2 mm, within 6 % of S0's (at 2 mm the SIN amplitudes are the same, 0.885 nH), and the angle error stays lower than S0's at every gap: 2.4° and 2.1° rms against 3.6° and 3.3°.
* **The solver copes better with this TX.** At 1 and 0.5 mm every solve stops below 5e-4 and the angle error is about 3° rms at both gaps; on S0 three of the 0.5 mm solves stalled higher and its 0.5 mm curve is off by 14° rms. At 0.1 mm both boards stall too high to read, this one less so.
* **The signal is about the same at 1 mm** (2.2 nH against 2.1, about 48 mV of EMF at 1 A) although the RX band is narrower, and it grows to about 3.2 nH at 0.5 mm.
* **SIN and COS are matched in amplitude** within 5 % at 1 and 0.5 mm (S0: 4 % at 1 mm, 16 % at 0.5 mm).

## The folder

| Folder | What is in it |
|---|---|
| [`Boards/`](Boards/) | straight from the generator: the stator and rotor boards, `Parameters.txt`, the pictures and the parameter files it was run with |
| [`3D_Geometry/`](3D_Geometry/) | KESE's export of the stator and rotor (STL solids, `materials.json`, STEP, KESE's report), written by the first run; `source.json` records the board's hash, so a changed board is exported again |
| [`Elmer Simulation/`](Elmer%20Simulation/) | `test_spec.json` (every board fact the simulation needs), `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` (S0's, unchanged; `python rig_picture.py` draws how the boards sit in Elmer), [`RotorStator_AngleSetup/`](Elmer%20Simulation/RotorStator_AngleSetup/) (the rotor over the stator at each angle, drawn by `python angle_setup.py`), and the runs under `case/`, which git ignores |
| [`Results/`](Results/) | `expected_results.json` (the generator's estimates), [`SINCOS_Results.md`](Results/SINCOS_Results.md) with every gap on one page, the charts of every gap together (`SINCOS_gaps.webp`, and `_SIN` and `_COS` apart), and a folder for each air gap (`0d1mm_AirGap`, `0d5mm_AirGap`, `1mm_AirGap`, `1d5mm_AirGap`, `2mm_AirGap`, the point written as d) with the runs' `results_gap<gap>mm.json`, `.csv` and `.webp` |

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

`SINCOS_Results.md` is rewritten after every solve: each gap's graph with a caption, the fit, the angle error at each angle and every solve.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [../LICENSE.md](../LICENSE.md); this branch's GPL-3.0 covers `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` only.
