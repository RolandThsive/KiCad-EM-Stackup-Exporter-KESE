# S0_1x_OD22_2L_tiny_TXtop_Cut

A coil set from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator) (`Coil_2_11.1_1_1_2_Single_SteppedDiagonal`), set up for FastHenry by [`../new_coil.py`](../new_coil.py). The steps that made it are in [S0's README](../S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

**What differs from S0.** The TX, as Roland asked: two turns, both on the top layer (F.Cu, r = 7.2 and 7.8 mm), instead of S0's one turn on each layer. S0's RX coils are kept exactly (band r = 3.2 to 6.1 mm), so the board grows to make room for the second turn: 22.2 mm across instead of 21, and the generator's rotor, fitted to the stator, now reaches r = 8.4 mm instead of 7.8. The parameter files differ from S0's in `TX_Parameters.py` (`TX_TURNS = 2`, `TX_WIRING = "single"`, `TX_LAYER_A = 1`), `RX_Parameters.py` (`INSIDE_RADIUS_MM = 3.2`, `OUTSIDE_RADIUS_MM = 6.1`: S0's band, fixed) and `Board_Parameters.py` (`OUTER_EDGE_RADIUS_MM = None`: the edge fitted to the TX). A spiral of two turns needs its inner end brought back out, so a short tail runs under the turns on B.Cu to the terminal, where the two ends sit stacked as on S0.

**SIN and COS are opened by a 0.2 mm cut across a top trace**, because that is how the real board is opened and routed to the IC. The voltage across each cut is the receiver's open-circuit EMF, reported as the mutual inductance M = V / (jωI) with 1 A in the TX. The cut is made in the model; the board files are as the generator wrote them. `test_spec.json` sets `"rx_port": "cut"` and gives each receiver a `cut` (where, which way the trace runs, 0.2 mm long, 0.4 mm across), and `simulation.py` takes the copper inside that box out of the top copper. The receivers' layer-change vias all stay in.

## The board

Bore and outer radius 2 and 11.1 mm, 2 copper layers, board 0.8 mm, air gap 1 mm by default (any other with `--gap`). 1 electrical period per turn; the rotor has 1 sector and repeats itself every 360°.

![stator and rotor](S0_1x_OD22_2L_tiny_TXtop_Cut_stator_and_rotor.webp)

*Drawn by the generator.*

![where SIN and COS are opened](S0_1x_OD22_2L_tiny_TXtop_Cut_cuts.webp)

*Each cut is the spot on the receiver's top trace nearest its layer-change via where a 0.2 mm cut has at least 0.45 mm of free board round it and sits at least 0.75 mm from any via centre: 0.86 mm from the via on both receivers, with 0.46 mm of free board. The two spots are a quarter turn apart about the axis, as SIN and COS are.*

![how the stator and rotor are set up in FastHenry](S0_1x_OD22_2L_tiny_TXtop_Cut_fasthenry_setup.webp)

*How the boards sit in FastHenry, drawn by `rig_picture.py` from the segments the model is made of: the rotor copper side down over the stator, each receiver opened by its cut and the TX between its two stacked ends. The trace's copper inside each cut box is left out, and a receiver's port is between the nodes of the two cut faces. The TX's port, between its two ends, is driven. FastHenry gives the open-circuit impedances between the three ports, so a receiver's voltage is its open-circuit EMF. [`FastHenry Simulation/RotorStator_AngleSetup/`](FastHenry%20Simulation/RotorStator_AngleSetup/) has the rotor over the stator at each of the 8 angles, with the two cuts and the TX port ringed (`python angle_setup.py`).*

| Coil | Net | Opened at (KiCad mm) | How |
|---|---|---|---|
| TX | `TX` | (110.4, 100), F.Cu and B.Cu | its two stacked ends |
| SIN | `2` | cut at (97.160, 101.626), F.Cu | a 0.2 mm gap across the top trace, running (-0.63, -0.78); the via at (97.737, 102.263) stays |
| COS | `1` | cut at (98.374, 97.160), F.Cu | a 0.2 mm gap across the top trace, running (0.78, -0.63); the via at (97.737, 97.737) stays |

The generator's estimate for the TX: 0.14 µH with the rotor away and 0.12 µH with it, 0.25 Ω DC. Its warnings for this board:

* the tank's parallel resistance at the nominal air gap may be as low as 13 ohm (if the AC resistance is 2 x the DC value); the IPS2550 needs at least 250 ohm.  More TX turns, wider TX traces, thicker copper or a higher EXCITATION_FREQ_HZ raise it
* no spot on 2 within 30 deg of 0 deg, 4 mm from the other marks, has room for two vias (layers F.Cu, B.Cu); widen SILKSCREEN_SEARCH_SPAN_DEG, lower SILKSCREEN_BREAK_SEPARATION_MM, or cut the coil by hand
* no spot on 1 within 30 deg of 0 deg, 4 mm from the other marks, has room for two vias (layers F.Cu, B.Cu); widen SILKSCREEN_SEARCH_SPAN_DEG, lower SILKSCREEN_BREAK_SEPARATION_MM, or cut the coil by hand

## Results at each air gap

Every angle at every gap, one FastHenry solve each: 8 angles at each of 5 gaps, and the rotor taken away once (with the 1 mm results). Each gap's curves, fits and angle error are in [`Results/SINCOS_Results.md`](Results/SINCOS_Results.md).

| Air gap | Amplitude SIN / COS | Angle error | Solves passing the checks | L TX over the turn |
|---|---|---|---|---|
| 2 mm | 1.50 / 1.51 nH (33 / 33 mV) | 0.2° rms, 0.2° peak | 8 of 8 | 140.8 nH |
| 1.5 mm | 2.25 / 2.25 nH (49 / 50 mV) | 0.1° rms, 0.2° peak | 8 of 8 | 138.2 to 138.3 nH |
| 1 mm | 3.40 / 3.41 nH (75 / 75 mV) | 0.2° rms, 0.2° peak | 8 of 8 | 134.0 to 134.2 nH |
| 0.5 mm | 5.12 / 5.12 nH (113 / 113 mV) | 0.3° rms, 0.5° peak | 8 of 8 | 126.1 to 126.3 nH |
| 0.1 mm | 6.70 / 6.70 nH (147 / 147 mV) | 1.0° rms, 1.3° peak | 8 of 8 | 111.6 to 111.9 nH |

![SIN at each air gap](Results/SINCOS_gaps_SIN.webp)

*SIN at each air gap, one dot per solve; a ring would mark a solve that fails the checks (none does). [`SINCOS_gaps_COS.webp`](Results/SINCOS_gaps_COS.webp) is the same for COS, and [`SINCOS_gaps.webp`](Results/SINCOS_gaps.webp) has both.*

Every solve is reciprocal: M from the TX to each receiver and M from the receiver back to the TX agree to the last digit FastHenry writes, as a direct solve of its symmetric matrix must. At every gap SIN and COS are within 0.3 % of each other in amplitude and 90.0° apart, and the angle error is 0.1° to 1.0° rms over the gaps. At 0.1 mm the angle error alternates in sign from one angle to the next: a ripple at four periods per electrical period, the fastest the angles can show, which third or fifth harmonics of the coupling would give, and those fade faster with the gap than the sine itself. SIN's amplitude is 6.70 nH at 0.1 mm, 5.12 nH at 0.5 mm, 3.40 nH at 1 mm, 2.25 nH at 1.5 mm and 1.50 nH at 2 mm (147 down to 33 mV of EMF at 1 A). L TX moves by 0.3 nH at most over the turn, and rises from 111.8 nH at 0.1 mm to 140.8 nH at 2 mm; with the rotor away it is 146.9 nH, where the generator estimated 116 nH with the rotor and 144 nH without. Each model has 7,113 filaments, and each solve took 2.2 to 5.3 min and 0.7 GB on one core.

## The folder

| Folder | What is in it |
|---|---|
| [`Boards/`](Boards/) | straight from the generator: the stator and rotor boards, `Parameters.txt`, the pictures and the parameter files it was run with |
| [`3D_Geometry/`](3D_Geometry/) | KESE's export of the stator and rotor (STL solids, `materials.json`, STEP, KESE's report), written by the first run; `source.json` records the board's hash, so a changed board is exported again (the layers' heights and the copper's thickness are read from it) |
| [`FastHenry Simulation/`](FastHenry%20Simulation/) | `test_spec.json` (every board fact the simulation needs, with `"rx_port": "cut"` and each receiver's `cut`), `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` (S0's, unchanged): `simulation.py` builds the filaments and solves each angle and writes the results, [`RotorStator_AngleSetup/`](FastHenry%20Simulation/RotorStator_AngleSetup/) (the rotor over the stator at each angle), and the runs under `case/`, which git ignores |
| [`Results/`](Results/) | `expected_results.json` (the generator's estimates), [`SINCOS_Results.md`](Results/SINCOS_Results.md) with every gap on one page, the charts of every gap together (`SINCOS_gaps.webp`, and `_SIN` and `_COS` apart), and a folder for each air gap (`0d1mm_AirGap`, `0d5mm_AirGap`, `1mm_AirGap`, `1d5mm_AirGap`, `2mm_AirGap`, the point written as d) with the runs' `results_gap<gap>mm.json`, `.csv` and `.webp` |

Beside this README, `S0_1x_OD22_2L_tiny_TXtop_Cut_stator_and_rotor.webp` is the generator's picture of the boards, `S0_1x_OD22_2L_tiny_TXtop_Cut_fasthenry_setup.webp` shows how they sit in FastHenry, and `S0_1x_OD22_2L_tiny_TXtop_Cut_cuts.webp` shows where SIN and COS are opened.

## Running it

| Air gap | Filaments | Rotor bars | Memory a solve | Time a solve |
|---|---|---|---|---|
| 0.1 mm | 7,113 | 3,602 | 0.7 GB | 3.4 to 5.2 min |
| 0.5 mm | 7,113 | 3,602 | 0.7 GB | 2.3 to 3.7 min |
| 1 mm | 7,113 | 3,602 | 0.7 GB | 2.3 to 3.4 min |
| 1.5 mm | 7,113 | 3,602 | 0.7 GB | 3.0 to 5.3 min |
| 2 mm | 7,113 | 3,602 | 0.7 GB | 2.2 to 3.4 min |

Each solve is FastHenry's dense direct solve on one core, so its memory grows as the square of the filaments and its time as their cube; `--jobs` runs several angles at once. See [S0's README](../S0_1x_OD21_2L_tiny/README.md#what-the-solver-does) for what more filaments move.

    cd "FastHenry Simulation"
    python simulation.py                        # the rotor away, then 0, 45, 90, 135, 180, 225, 270, 315 degrees, at a 1 mm gap
    python simulation.py --gap 0.5              # the same at a 0.5 mm air gap
    python simulation.py --step 10              # every 10 degrees
    python simulation.py --jobs 3               # three solves at once, one core each
    python simulation.py --nwinc 5 --trial w5   # five filaments across each track, kept in case/
    python simulation.py --model-only           # build the filaments and say how many, solve nothing
    python simulation.py --plot                 # redraw the table, the curves and SINCOS_Results.md
    python angle_error.py                       # print the angle error at each angle, and rewrite SINCOS_Results.md
    python make_charts.py                       # redraw every chart (WebP) and rewrite SINCOS_Results.md
    python rig_picture.py                       # redraw how the boards sit in FastHenry
    python angle_setup.py                       # redraw the rotor at each angle

Use the Python of the branch's `.venv` (`bash bridge/setup_machine.sh` makes it, and installs what FastHenry needs). `SINCOS_Results.md` is rewritten after every solve: each gap's graph with a caption, the fit, the angle error at each angle and every solve.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [../LICENSE.md](../LICENSE.md); this branch's GPL-3.0 covers `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` only.
