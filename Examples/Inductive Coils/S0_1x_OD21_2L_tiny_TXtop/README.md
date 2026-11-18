# S0_1x_OD21_2L_tiny_TXtop

A coil set from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator) (`Coil_2_10.5_1_1_2_Single_SteppedDiagonal`), set up for Palace by [`../new_coil.py`](../new_coil.py). The steps that made it are in [S0's README](../S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

**What differs from S0.** Only the TX, as Roland asked: two turns, both on the top layer (F.Cu, r = 6.6 and 7.2 mm), instead of S0's one turn on each layer. The parameter files differ from S0's in three values of `TX_Parameters.py`: `TX_TURNS = 2`, `TX_WIRING = "single"`, `TX_LAYER_A = 1`. A spiral of two turns needs its inner end brought back out, so a short tail runs under the turns on B.Cu to the terminal, where the two ends sit stacked as on S0. The generator keeps the board edge, so it narrows the RX band to make room for the second turn (r = 3.2 to 5.5 mm, against 3.2 to 6.1 on S0); the rotor is S0's, file for file.

## The board

Bore and outer radius 2 and 10.5 mm, 2 copper layers, board 0.8 mm, air gap 1 mm by default (any other with `--gap`). 1 electrical period per turn; the rotor has 1 sector and repeats itself every 360°.

![stator and rotor](S0_1x_OD21_2L_tiny_TXtop_stator_and_rotor.webp)

*Drawn by the generator.*

![how the stator and rotor are set up in Palace](S0_1x_OD21_2L_tiny_TXtop_palace_setup.webp)

*How the boards sit in Palace, drawn by `rig_picture.py` from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened at a left-out via and the TX between its two stacked ends. A receiver's port is a sheet standing between the via's two pads across the board, 0.5 mm wide, with 1 MΩ across it. The TX's port, 0.16 mm wide, stands between its two ends with 50 Ω and the drive. 1 MΩ leaves a receiver open to a few parts in a million, so the voltage across its port is its open-circuit EMF.*

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

Every angle at every gap, one Palace solve each: 8 angles at each of 5 gaps, and the rotor taken away once (with the 1 mm results). Each gap's curves, fits and angle error are in [`Results/SINCOS_Results.md`](Results/SINCOS_Results.md).

| Air gap | Amplitude SIN / COS | Angle error | Solves passing the checks | L TX over the turn |
|---|---|---|---|---|
| 2 mm | 1.00 / 1.00 nH (22 / 22 mV) | 0.4° rms, 0.6° peak | 8 of 8 | 120.5 to 120.6 nH |
| 1.5 mm | 1.53 / 1.54 nH (34 / 34 mV) | 0.4° rms, 0.6° peak | 8 of 8 | 118.4 to 118.5 nH |
| 1 mm | 2.42 / 2.42 nH (53 / 53 mV) | 0.4° rms, 0.6° peak | 8 of 8 | 114.7 to 114.9 nH |
| 0.5 mm | 3.82 / 3.82 nH (84 / 84 mV) | 0.7° rms, 0.8° peak | 8 of 8 | 107.9 to 108.2 nH |
| 0.1 mm | 5.20 / 5.20 nH (114 / 114 mV) | 1.5° rms, 1.7° peak | 8 of 8 | 94.8 to 95.2 nH |

![SIN at each air gap](Results/SINCOS_gaps_SIN.webp)

*SIN at each air gap, one dot per solve; a ring would mark a solve that fails the checks (none does). [`SINCOS_gaps_COS.webp`](Results/SINCOS_gaps_COS.webp) is the same for COS, and [`SINCOS_gaps.webp`](Results/SINCOS_gaps.webp) has both.*

Every solve converged and passes the checks: the TX's L from its port and from the field's energy agree within 0.005 %, where 1 % is allowed, and M back from SIN and COS to the TX, where they were driven too, equals M from the TX within 0.001 %. At every gap SIN and COS are within 0.2 % of each other in amplitude and 89.9° to 90.0° apart, and the angle error is 0.4° to 1.5° rms over the gaps. At 0.1 mm the angle error alternates in sign from one angle to the next: a ripple at four periods per electrical period, the fastest the angles can show, which third or fifth harmonics of the coupling would give, and those fade faster with the gap than the sine itself. SIN's amplitude is 5.20 nH at 0.1 mm, 3.82 nH at 0.5 mm, 2.42 nH at 1 mm, 1.53 nH at 1.5 mm and 1.00 nH at 2 mm (114 down to 22 mV of EMF at 1 A). L TX moves by 0.4 nH at most over the turn, and rises from 95.0 nH at 0.1 mm to 120.5 nH at 2 mm; with the rotor away it is 125.1 nH, where the generator estimated 106 nH with the rotor and 130 nH without. The meshes have 137,854 to 225,117 nodes, 12 to 21 element layers through the copper, board and gap, and each solve took 1.5 to 8.7 min and 4.6 to 9.7 GB on 4 MPI ranks.

## The folder

| Folder | What is in it |
|---|---|
| [`Boards/`](Boards/) | straight from the generator: the stator and rotor boards, `Parameters.txt`, the pictures and the parameter files it was run with |
| [`3D_Geometry/`](3D_Geometry/) | KESE's export of the stator and rotor (STL solids, `materials.json`, STEP, KESE's report), written by the first run; `source.json` records the board's hash, so a changed board is exported again |
| [`Palace Simulation/`](Palace%20Simulation/) | `test_spec.json` (every board fact the simulation needs), `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` (S0's, unchanged): `simulation.py` meshes and solves each angle and writes the results, [`RotorStator_AngleSetup/`](Palace%20Simulation/RotorStator_AngleSetup/) (the rotor over the stator at each angle), and the runs under `case/`, which git ignores |
| [`Results/`](Results/) | `expected_results.json` (the generator's estimates), [`SINCOS_Results.md`](Results/SINCOS_Results.md) with every gap on one page, the charts of every gap together (`SINCOS_gaps.webp`, and `_SIN` and `_COS` apart), and a folder for each air gap (`0d1mm_AirGap`, `0d5mm_AirGap`, `1mm_AirGap`, `1d5mm_AirGap`, `2mm_AirGap`, the point written as d) with the runs' `results_gap<gap>mm.json`, `.csv` and `.webp` |

Beside this README, `S0_1x_OD21_2L_tiny_TXtop_stator_and_rotor.webp` is the generator's picture of the boards and `S0_1x_OD21_2L_tiny_TXtop_palace_setup.webp` shows how they sit in Palace.

## Running it

| Air gap | Mesh level | Nodes | Element layers | MPI ranks | Memory a solve | Time a solve |
|---|---|---|---|---|---|---|
| 0.1 mm | 0.25 | 137,854 to 138,897 | 12 | 4 | 4.6 to 6.1 GB | 1.5 to 4.6 min |
| 0.5 mm | 0.25 | 156,898 to 158,057 | 14 | 4 | 5.2 to 6.9 GB | 1.5 to 4.9 min |
| 1 mm | 0.25 | 175,942 to 177,217 | 16 | 4 | 5.7 to 7.6 GB | 1.9 to 6.0 min |
| 1.5 mm | 0.25 | 204,508 to 205,957 | 19 | 4 | 6.6 to 8.8 GB | 2.3 to 7.2 min |
| 2 mm | 0.25 | 223,552 to 225,117 | 21 | 4 | 7.2 to 9.7 GB | 2.5 to 8.7 min |

Each solve is GMRES with hypre's AMS, at about 33 kB a mesh node, and 44 kB at the first angle of each gap, where the three coils are driven in turn (4.6 to 9.7 GB here), on 2 MPI ranks or 4 alike; a 16 GB machine runs two at once (`--jobs 2`) where a solve stays under 7 GB. Level 0.25 is the default (`--level` makes the copper's mesh finer); see [S0's README](../S0_1x_OD21_2L_tiny/README.md#what-the-solver-does) for what a finer mesh moves.

    cd "Palace Simulation"
    python simulation.py                      # the rotor away, then 0, 45, 90, 135, 180, 225, 270, 315 degrees, at a 1 mm gap
    python simulation.py --gap 0.5            # the same at a 0.5 mm air gap
    python simulation.py --step 10            # every 10 degrees
    python simulation.py --level 0.4          # a finer mesh, a trial kept in case/ (more memory and time)
    python simulation.py --jobs 2 --ranks 2   # two solves at once, each on 2 MPI ranks
    python simulation.py --mesh-only          # build the meshes and say their size, solve nothing
    python simulation.py --plot               # redraw the table, the curves and SINCOS_Results.md
    python angle_error.py                     # print the angle error at each angle, and rewrite SINCOS_Results.md
    python make_charts.py                     # redraw every chart (WebP) and rewrite SINCOS_Results.md
    python rig_picture.py                     # redraw how the boards sit in Palace
    python angle_setup.py                     # redraw the rotor at each angle

Use the Python of the branch's `.venv` (`bash bridge/setup_machine.sh` makes it, and installs what Palace runs with). `SINCOS_Results.md` is rewritten after every solve: each gap's graph with a caption, the fit, the angle error at each angle and every solve.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [../LICENSE.md](../LICENSE.md); this branch's GPL-3.0 covers `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` only.
