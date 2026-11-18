# S0_1x_OD23_2L_tiny_TX3top_Cut

A coil set from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator) (`Coil_2_11.7_1_1_3_Single_SteppedDiagonal`), set up for Palace by [`../new_coil.py`](../new_coil.py). The steps that made it are in [S0's README](../S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

**What differs from S0.** The TX: three turns, all on the top layer (F.Cu, r = 7.2, 7.8 and 8.4 mm), instead of S0's one turn on each layer. S0's RX coils are kept exactly (band r = 3.2 to 6.1 mm), the board edge is fitted to the TX and the rotor to the stator, so the board grows to make room for the turns: 23.4 mm across instead of 21, and the rotor copper reaches r = 9.0 mm instead of 7.8. The parameter files are those of [`../S0_1x_OD22_2L_tiny_TXtop`](../S0_1x_OD22_2L_tiny_TXtop) (the same board with two TX turns) with one change, `TX_TURNS = 3` in `TX_Parameters.py`, run with the generator at commit 32bf9cb. A spiral needs its inner end brought back out, so a short tail runs under the turns on B.Cu to the terminal, where the two ends sit stacked as on S0.

**SIN and COS are opened by a 0.2 mm cut across a top trace**, because that is how the real board is opened and routed to the IC. The voltage across each cut is the receiver's open-circuit EMF, reported as the mutual inductance M = V / (jωI) with 1 A in the TX. The cut is made in the model; the board files are as the generator wrote them. `test_spec.json` sets `"rx_port": "cut"` and gives each receiver a `cut` (where, which way the trace runs, 0.2 mm long, 0.4 mm across), and `simulation.py` takes the copper inside that box out of the top copper. The receivers' layer-change vias all stay in.

## The board

Bore and outer radius 2 and 11.7 mm, 2 copper layers, board 0.8 mm, air gap 1 mm by default (any other with `--gap`). 1 electrical period per turn; the rotor has 1 sector and repeats itself every 360°.

![stator and rotor](S0_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp)

*Drawn by the generator.*

![where SIN and COS are opened](S0_1x_OD23_2L_tiny_TX3top_Cut_cuts.webp)

*Each cut is the spot on the receiver's top trace nearest its layer-change via where a 0.2 mm cut has at least 0.45 mm of free board round it and sits at least 0.75 mm from any via centre: 0.86 mm from the via on both receivers. The two spots are a quarter turn apart about the axis, as SIN and COS are.*

![how the stator and rotor are set up in Palace](S0_1x_OD23_2L_tiny_TX3top_Cut_palace_setup.webp)

*How the boards sit in Palace, drawn by `rig_picture.py` from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened by its cut and the TX between its two stacked ends. The copper inside each cut box is air, and a receiver's port is a sheet across the gap, through the copper's thickness, from one cut face to the other, with 1 MΩ across it; the outline of each cut is drawn into the 2D mesh, so both cut faces are meshed exactly. The TX's port, 0.16 mm wide, stands between its two ends with 50 Ω and the drive. 1 MΩ leaves a receiver open to a few parts in a million, so the voltage across its port is its open-circuit EMF. [`Palace Simulation/RotorStator_AngleSetup/`](Palace%20Simulation/RotorStator_AngleSetup/) has the rotor over the stator at each of the 8 angles, with the two cuts and the TX port ringed (`python angle_setup.py`).*

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

Every angle at every gap, one Palace solve each: 8 angles at each of 5 gaps, and the rotor taken away once (with the 1 mm results). Each gap's curves, fits and angle error are in [`Results/SINCOS_Results.md`](Results/SINCOS_Results.md).

| Air gap | Amplitude SIN / COS | Angle error | Solves passing the checks | L TX over the turn |
|---|---|---|---|---|
| 2 mm | 2.36 / 2.37 nH (52 / 52 mV) | 0.3° rms, 0.4° peak | 8 of 8 | 266.4 to 266.6 nH |
| 1.5 mm | 3.43 / 3.43 nH (75 / 76 mV) | 0.3° rms, 0.4° peak | 8 of 8 | 260.6 to 260.8 nH |
| 1 mm | 5.03 / 5.04 nH (111 / 111 mV) | 0.3° rms, 0.5° peak | 8 of 8 | 251.0 to 251.4 nH |
| 0.5 mm | 7.31 / 7.32 nH (161 / 161 mV) | 0.6° rms, 0.7° peak | 8 of 8 | 234.7 to 235.2 nH |
| 0.1 mm | 9.38 / 9.39 nH (206 / 206 mV) | 1.2° rms, 1.5° peak | 8 of 8 | 208.6 to 209.2 nH |

![SIN at each air gap](Results/SINCOS_gaps_SIN.webp)

*SIN at each air gap, one dot per solve; a ring would mark a solve that fails the checks (none does). [`SINCOS_gaps_COS.webp`](Results/SINCOS_gaps_COS.webp) is the same for COS, and [`SINCOS_gaps.webp`](Results/SINCOS_gaps.webp) has both.*

Every solve converged and passes the checks: the TX's L from its port and from the field's energy agree within 0.01 %, where 1 % is allowed, and M back from SIN and COS to the TX, where they were driven too, equals M from the TX within 0.001 %. At every gap SIN and COS are within 0.2 % of each other in amplitude and 90.0° apart, and the angle error is 0.3° to 1.2° rms over the gaps. At 0.1 mm the angle error alternates in sign from one angle to the next: a ripple at four periods per electrical period, the fastest the angles can show, which third or fifth harmonics of the coupling would give, and those fade faster with the gap than the sine itself. SIN's amplitude is 9.38 nH at 0.1 mm, 7.31 nH at 0.5 mm, 5.03 nH at 1 mm, 3.43 nH at 1.5 mm and 2.36 nH at 2 mm (206 down to 52 mV of EMF at 1 A). L TX moves by 0.7 nH at most over the turn, and rises from 208.9 nH at 0.1 mm to 266.5 nH at 2 mm; with the rotor away it is 281.4 nH, where the generator estimated 226 nH with the rotor and 292 nH without. The meshes have 155,195 to 254,931 nodes, 12 to 21 element layers through the copper, board and gap, and each solve took 2 to 12 min and 5.1 to 11.4 GB on 4 MPI ranks.

## The folder

| Folder | What is in it |
|---|---|
| [`Boards/`](Boards/) | straight from the generator: the stator and rotor boards, `Parameters.txt`, the pictures and the parameter files it was run with |
| [`3D_Geometry/`](3D_Geometry/) | KESE's export of the stator and rotor (STL solids, `materials.json`, STEP, KESE's report), written by the first run; `source.json` records the board's hash, so a changed board is exported again |
| [`Palace Simulation/`](Palace%20Simulation/) | `test_spec.json` (every board fact the simulation needs, with `"rx_port": "cut"` and each receiver's `cut`), `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` (S0's, unchanged): `simulation.py` meshes and solves each angle and writes the results, [`RotorStator_AngleSetup/`](Palace%20Simulation/RotorStator_AngleSetup/) (the rotor over the stator at each angle), and the runs under `case/`, which git ignores |
| [`Results/`](Results/) | `expected_results.json` (the generator's estimates), [`SINCOS_Results.md`](Results/SINCOS_Results.md) with every gap on one page, the charts of every gap together (`SINCOS_gaps.webp`, and `_SIN` and `_COS` apart), and a folder for each air gap (`0d1mm_AirGap`, `0d5mm_AirGap`, `1mm_AirGap`, `1d5mm_AirGap`, `2mm_AirGap`, the point written as d) with the runs' `results_gap<gap>mm.json`, `.csv` and `.webp` |

Beside this README, `S0_1x_OD23_2L_tiny_TX3top_Cut_stator_and_rotor.webp` is the generator's picture of the boards, `S0_1x_OD23_2L_tiny_TX3top_Cut_palace_setup.webp` shows how they sit in Palace, and `S0_1x_OD23_2L_tiny_TX3top_Cut_cuts.webp` shows where SIN and COS are opened.

## Running it

| Air gap | Mesh level | Nodes | Element layers | MPI ranks | Memory a solve | Time a solve |
|---|---|---|---|---|---|---|
| 0.1 mm | 0.25 | 155,195 to 157,146 | 12 | 4 | 5.1 to 6.9 GB | 1.6 to 5.6 min |
| 0.5 mm | 0.25 | 176,661 to 178,876 | 14 | 4 | 5.7 to 7.8 GB | 1.9 to 6.5 min |
| 1 mm | 0.25 | 198,127 to 200,606 | 16 | 4 | 6.4 to 8.8 GB | 2.3 to 8.0 min |
| 1.5 mm | 0.25 | 230,326 to 233,201 | 19 | 4 | 7.4 to 10.2 GB | 2.7 to 9.2 min |
| 2 mm | 0.25 | 251,792 to 254,931 | 21 | 4 | 8.2 to 11.4 GB | 3 to 12 min |

Each solve is GMRES with hypre's AMS, at about 33 kB a mesh node, and 44 kB at the first angle of each gap, where the three coils are driven in turn (5.1 to 11.4 GB here), on 2 MPI ranks or 4 alike; a 16 GB machine runs two at once (`--jobs 2`) where a solve stays under 7 GB. Level 0.25 is the default (`--level` makes the copper's mesh finer); see [S0's README](../S0_1x_OD21_2L_tiny/README.md#what-the-solver-does) for what a finer mesh moves.

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
