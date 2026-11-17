# S0d2_1x_OD23_2L_tiny_TX3top_Cut

A coil set from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator) (`Coil_2_11.7_2_1_3_Single_SteppedDiagonal`), set up for Elmer by [`../new_coil.py`](../new_coil.py). The steps that made it are in [S0's README](../S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

**What differs from S0.** Two electrical periods per turn instead of one, with a TX of three turns on the top layer. The RX coils keep S0's band (r = 3.2 to 6.1 mm) but each makes two sine periods per turn, and the rotor has two quarter-ring sectors, so the curves repeat every 180° and an angle reading covers half a turn. The TX is three turns, all on the top layer (F.Cu, r = 7.2, 7.8 and 8.4 mm), instead of S0's one turn on each layer; the board is 23.4 mm across and the rotor copper reaches r = 9.0 mm. The parameter files are those of [`../S0_1x_OD23_2L_tiny_TX3top_Cut`](../S0_1x_OD23_2L_tiny_TX3top_Cut) (the same board with one period per turn) with one change, `LOOPS = 2` in `RX_Parameters.py`, run with the generator at commit 32bf9cb. A spiral needs its inner end brought back out, so a short tail runs under the turns on B.Cu to the terminal, where the two ends sit stacked as on S0.

**SIN and COS are opened by a 0.2 mm cut across a top trace**, because that is how the real board is opened and routed to the IC. The voltage across each cut is the receiver's open-circuit EMF, reported as the mutual inductance M = V / (jωI) with 1 A in the TX. The cut is made in the model; the board files are as the generator wrote them. `test_spec.json` sets `"rx_port": "cut"` and gives each receiver a `cut` (where, which way the trace runs, 0.2 mm long, 0.4 mm across), and `simulation.py` takes the copper inside that box out of the top copper. The receivers' layer-change vias all stay in.

## The board

Bore and outer radius 2 and 11.7 mm, 2 copper layers, board 0.8 mm, air gap 1 mm by default (any other with `--gap`). 2 electrical periods per turn; the rotor has 2 sectors and repeats itself every 180°.

![stator and rotor](S0d2_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp)

*Drawn by the generator.*

![where SIN and COS are opened](S0d2_1x_OD23_2L_tiny_TX3top_Cut_cuts.webp)

*Each cut is the spot on the receiver's top trace nearest its layer-change via where a 0.2 mm cut has at least 0.45 mm of free board round it and sits at least 0.75 mm from any via centre: 0.86 mm from the via on both receivers. The two spots are 45° apart about the axis, a quarter of the electrical period, as SIN and COS are.*

![how the stator and rotor are set up in Elmer](S0d2_1x_OD23_2L_tiny_TX3top_Cut_elmer_setup.webp)

*How the boards sit in Elmer, drawn by `rig_picture.py` from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened by the cut, and the TX opened between its two stacked ends, where 1 A is driven. The copper inside each cut box is air. The two copper faces that border the gap are the terminal's electrodes, and the port sheet spans the gap at the copper's lower face, as in Elmer's E01 example. SIN and COS carry 0 A, so the voltage across the gap is the open-circuit EMF. The outline of each cut is drawn into the 2D mesh, so both cut faces are meshed exactly. [`Elmer Simulation/RotorStator_AngleSetup/`](Elmer%20Simulation/RotorStator_AngleSetup/) has the rotor over the stator at each of the 16 angles, with the two cuts and the TX port ringed (`python angle_setup.py`).*

| Coil | Net | Opened at (KiCad mm) | How |
|---|---|---|---|
| TX | `TX` | (111, 100), F.Cu and B.Cu | its two stacked ends |
| SIN | `2` | cut at (96.591, 100.496), F.Cu | a 0.2 mm gap across the top trace, running (-0.60, -0.80); the via at (97.044, 101.225) stays |
| COS | `1` | cut at (97.239, 97.940), F.Cu | a 0.2 mm gap across the top trace, running (0.14, -0.99); the via at (97.044, 98.775) stays |

The generator's estimate for the TX: 0.29 µH with the rotor away and 0.23 µH with it, 0.38 Ω DC. Its warnings for this board:

* the tank's parallel resistance at the nominal air gap may be as low as 32 ohm (if the AC resistance is 2 x the DC value); the IPS2550 needs at least 250 ohm.  More TX turns, wider TX traces, thicker copper or a higher EXCITATION_FREQ_HZ raise it
* no spot on 2 within 30 deg of 0 deg, 4 mm from the other marks, has room for two vias (layers F.Cu, B.Cu); widen SILKSCREEN_SEARCH_SPAN_DEG, lower SILKSCREEN_BREAK_SEPARATION_MM, or cut the coil by hand
* no spot on 1 within 30 deg of 0 deg, 4 mm from the other marks, has room for two vias (layers F.Cu, B.Cu); widen SILKSCREEN_SEARCH_SPAN_DEG, lower SILKSCREEN_BREAK_SEPARATION_MM, or cut the coil by hand

## Results at each air gap

Every angle at every gap, one Elmer solve each: 16 angles over the whole turn, every 22.5° from 0 to 337.5° (two of the rotor's 180° periods), at each of 5 gaps, and the rotor taken away once (with the 1 mm results). Each gap's curves, fits and angle error are in [`Results/SINCOS_Results.md`](Results/SINCOS_Results.md). The angle error is in electrical degrees; with two periods per turn, a mechanical degree is two electrical ones, so the error in mechanical degrees is half.

| Air gap | Amplitude SIN / COS | Angle error (electrical) | Solves passing both checks | L TX over the turn |
|---|---|---|---|---|
| 2 mm | 1.86 / 1.86 nH (41 / 41 mV) | 0.2° rms, 0.4° peak | 16 of 16 | 262.4 to 262.8 nH |
| 1.5 mm | 2.88 / 2.88 nH (63 / 63 mV) | 0.2° rms, 0.4° peak | 16 of 16 | 257.6 to 258.1 nH |
| 1 mm | 4.51 / 4.51 nH (99 / 99 mV) | 0.2° rms, 0.4° peak | 16 of 16 | 250.0 to 250.6 nH |
| 0.5 mm | 6.97 / 6.98 nH (153 / 153 mV) | 0.4° rms, 0.6° peak | 16 of 16 | 236.3 to 237.0 nH |
| 0.1 mm | 9.44 / 9.44 nH (208 / 208 mV) | 0.9° rms, 1.2° peak | 16 of 16 | 213.1 to 214.2 nH |

![SIN at each air gap](Results/SINCOS_gaps_SIN.webp)

*SIN at each air gap, one dot per solve; a ring would mark a solve that fails the two checks (none does). [`SINCOS_gaps_COS.webp`](Results/SINCOS_gaps_COS.webp) is the same for COS, and [`SINCOS_gaps.webp`](Results/SINCOS_gaps.webp) has both.*

Each solve is direct (MUMPS), and every one passes both checks: the TX's L and R from its voltage agree with the L from the field energy and the R from the eddy power within 0.004 %, where 1 % is allowed. At every gap the curves are close to a sine and cosine, 90.06 to 90.18° apart and equal in amplitude within 0.06 %. The signal is 9.44 nH for SIN at 0.1 mm and falls to 6.97, 4.51, 2.88 and 1.86 nH at 0.5, 1, 1.5 and 2 mm (208 down to 41 mV of EMF at 1 A). The angle error is 0.9° rms at 0.1 mm, 0.4° at 0.5 mm and 0.2° from 1 to 2 mm, in electrical degrees; in mechanical degrees it is half that, from 0.46° down to 0.09° rms. At 0.1 mm it alternates in sign from one angle to the next: a ripple at four periods per electrical period, the fastest that eight angles a period can show, which fades with the gap faster than the sine. The second half turn repeats the first: at six of its eight angles each solve gives the same M, to the last digit, as the one 180° before it, and at 225° and 315°, where the 2D mesh comes out a few triangles different, it is within 0.03 nH. L TX moves by 1.1 nH at most over the turn and rises from 213.6 nH at 0.1 mm to 262.6 nH at 2 mm; with the rotor away it is 274.2 nH, where the generator estimated 226 nH with the rotor and 292 nH without.

## The folder

| Folder | What is in it |
|---|---|
| [`Boards/`](Boards/) | straight from the generator: the stator and rotor boards, `Parameters.txt`, the pictures and the parameter files it was run with |
| [`3D_Geometry/`](3D_Geometry/) | KESE's export of the stator and rotor (STL solids, `materials.json`, STEP, KESE's report), written by the first run; `source.json` records the board's hash, so a changed board is exported again |
| [`Elmer Simulation/`](Elmer%20Simulation/) | `test_spec.json` (every board fact the simulation needs, with `"rx_port": "cut"` and each receiver's `cut`), `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` (S0's, unchanged), [`RotorStator_AngleSetup/`](Elmer%20Simulation/RotorStator_AngleSetup/) (the rotor over the stator at each angle), and the runs under `case/`, which git ignores |
| [`Results/`](Results/) | `expected_results.json` (the generator's estimates), [`SINCOS_Results.md`](Results/SINCOS_Results.md) with every gap on one page, the charts of every gap together (`SINCOS_gaps.webp`, and `_SIN` and `_COS` apart), and a folder for each air gap (`0d1mm_AirGap`, `0d5mm_AirGap`, `1mm_AirGap`, `1d5mm_AirGap`, `2mm_AirGap`, the point written as d) with the runs' `results_gap<gap>mm.json`, `.csv` and `.webp` |

Beside this README, `S0d2_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp` is the generator's picture of the boards, `S0d2_1x_OD23_2L_tiny_TX3top_Cut_elmer_setup.webp` shows how they sit in Elmer, and `S0d2_1x_OD23_2L_tiny_TX3top_Cut_cuts.webp` shows where SIN and COS are opened.

## Running it

| Air gap | Mesh level | Nodes | Layers through the gap | Time a solve |
|---|---|---|---|---|
| 0.1 mm | 0.25 | 118,416 to 119,266 | 10 | 3 to 4 min |
| 0.5 mm | 0.25 | 128,812 to 129,731 | 11 | 4 to 6 min |
| 1 mm | 0.25 | 139,208 to 140,196 | 12 | 6 to 7 min |
| 1.5 mm | 0.25 | 149,604 to 150,661 | 13 | 7 to 9 min |
| 2 mm | 0.25 | 160,000 to 161,126 | 14 | 8 to 15 min |

Each solve is direct (MUMPS) and needs more than 13 GB: every one here held 13.3 GB in memory and put the rest in swap. At 0.1 mm an 8 GB swap file was enough; from 0.5 mm on it was not, and the solve was stopped for want of memory, so those ran on 16 GB machines with about 24 GB of swap, 40 GB of memory and swap together. On Linux, `sudo fallocate -l 26G /swapfile && sudo chmod 600 /swapfile && sudo mkswap /swapfile && sudo swapon /swapfile` adds one. `--level` above 0.25 makes the mesh finer at more memory, and `--solver iterative` (GCR) needs far less memory, about 57 kB a node, but on these boards at 3.5 MHz it converges too slowly to read M.

    cd "Elmer Simulation"
    python simulation.py                   # the rotor away, then 0 to 337.5 degrees every 22.5
    python simulation.py --gap 0.5         # the same at a 0.5 mm air gap
    python simulation.py --level 0.4       # a finer mesh, at more memory
    python simulation.py --plot            # redraw the table, the curves and SINCOS_Results.md
    python angle_error.py                  # print the angle error at each angle, and rewrite SINCOS_Results.md
    python make_charts.py                  # redraw every chart (WebP) and rewrite SINCOS_Results.md
    python rig_picture.py                  # redraw how the boards sit in Elmer
    python angle_setup.py                  # redraw the rotor at each angle

`SINCOS_Results.md` is rewritten after every solve: each gap's graph with a caption, the fit, the angle error at each angle and every solve.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [../LICENSE.md](../LICENSE.md); this branch's GPL-3.0 covers `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` only.
