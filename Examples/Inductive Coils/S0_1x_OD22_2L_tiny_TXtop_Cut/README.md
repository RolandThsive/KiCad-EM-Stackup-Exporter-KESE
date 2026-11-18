# S0_1x_OD22_2L_tiny_TXtop_Cut

A coil set from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator) (`Coil_2_11.1_1_1_2_Single_SteppedDiagonal`), set up for Palace by [`../new_coil.py`](../new_coil.py). The steps that made it are in [S0's README](../S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

**What differs from S0.** The TX, as Roland asked: two turns, both on the top layer (F.Cu, r = 7.2 and 7.8 mm), instead of S0's one turn on each layer. S0's RX coils are kept exactly (band r = 3.2 to 6.1 mm), so the board grows to make room for the second turn: 22.2 mm across instead of 21, and the generator's rotor, fitted to the stator, now reaches r = 8.4 mm instead of 7.8. The parameter files differ from S0's in `TX_Parameters.py` (`TX_TURNS = 2`, `TX_WIRING = "single"`, `TX_LAYER_A = 1`), `RX_Parameters.py` (`INSIDE_RADIUS_MM = 3.2`, `OUTSIDE_RADIUS_MM = 6.1`: S0's band, fixed) and `Board_Parameters.py` (`OUTER_EDGE_RADIUS_MM = None`: the edge fitted to the TX). A spiral of two turns needs its inner end brought back out, so a short tail runs under the turns on B.Cu to the terminal, where the two ends sit stacked as on S0.

**SIN and COS are opened by a 0.2 mm cut across a top trace**, because that is how the real board is opened and routed to the IC. The voltage across each cut is the receiver's open-circuit EMF, reported as the mutual inductance M = V / (jωI) with 1 A in the TX. The cut is made in the model; the board files are as the generator wrote them. `test_spec.json` sets `"rx_port": "cut"` and gives each receiver a `cut` (where, which way the trace runs, 0.2 mm long, 0.4 mm across), and `simulation.py` takes the copper inside that box out of the top copper. The receivers' layer-change vias all stay in.

## The board

Bore and outer radius 2 and 11.1 mm, 2 copper layers, board 0.8 mm, air gap 1 mm by default (any other with `--gap`). 1 electrical period per turn; the rotor has 1 sector and repeats itself every 360°.

![stator and rotor](S0_1x_OD22_2L_tiny_TXtop_Cut_stator_and_rotor.webp)

*Drawn by the generator.*

![where SIN and COS are opened](S0_1x_OD22_2L_tiny_TXtop_Cut_cuts.webp)

*Each cut is the spot on the receiver's top trace nearest its layer-change via where a 0.2 mm cut has at least 0.45 mm of free board round it and sits at least 0.75 mm from any via centre: 0.86 mm from the via on both receivers, with 0.46 mm of free board. The two spots are a quarter turn apart about the axis, as SIN and COS are.*

![how the stator and rotor are set up in Palace](S0_1x_OD22_2L_tiny_TXtop_Cut_palace_setup.webp)

*How the boards sit in Palace, drawn by `rig_picture.py` from the geometry the mesh is built from: the rotor copper side down over the stator, each receiver opened by its cut and the TX between its two stacked ends. The copper inside each cut box is air, and a receiver's port is a sheet across the gap, through the copper's thickness, from one cut face to the other, with 1 MΩ across it; the outline of each cut is drawn into the 2D mesh, so both cut faces are meshed exactly. The TX's port, 0.16 mm wide, stands between its two ends with 50 Ω and the drive. 1 MΩ leaves a receiver open to a few parts in a million, so the voltage across its port is its open-circuit EMF. [`Palace Simulation/RotorStator_AngleSetup/`](Palace%20Simulation/RotorStator_AngleSetup/) has the rotor over the stator at each of the 8 angles, with the two cuts and the TX port ringed (`python angle_setup.py`).*

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

Every angle at every gap, one Palace solve each: 8 angles at each of 5 gaps, and the rotor taken away once (with the 1 mm results). Each gap's curves, fits and angle error are in [`Results/SINCOS_Results.md`](Results/SINCOS_Results.md).

| Air gap | Amplitude SIN / COS | Angle error | Solves passing the checks | L TX over the turn |
|---|---|---|---|---|
| 2 mm | 1.49 / 1.50 nH (33 / 33 mV) | 0.2° rms, 0.3° peak | 8 of 8 | 132.9 to 133.0 nH |
| 1.5 mm | 2.23 / 2.23 nH (49 / 49 mV) | 0.2° rms, 0.2° peak | 8 of 8 | 130.4 to 130.5 nH |
| 1 mm | 3.37 / 3.37 nH (74 / 74 mV) | 0.2° rms, 0.3° peak | 8 of 8 | 126.2 to 126.3 nH |
| 0.5 mm | 5.07 / 5.08 nH (111 / 112 mV) | 0.4° rms, 0.5° peak | 8 of 8 | 118.4 to 118.6 nH |
| 0.1 mm | 6.66 / 6.66 nH (146 / 147 mV) | 1.1° rms, 1.3° peak | 8 of 8 | 103.9 to 104.2 nH |

![SIN at each air gap](Results/SINCOS_gaps_SIN.webp)

*SIN at each air gap, one dot per solve; a ring would mark a solve that fails the checks (none does). [`SINCOS_gaps_COS.webp`](Results/SINCOS_gaps_COS.webp) is the same for COS, and [`SINCOS_gaps.webp`](Results/SINCOS_gaps.webp) has both.*

Every solve converged and passes the checks: the TX's L from its port and from the field's energy agree within 0.005 %, where 1 % is allowed, and M back from SIN and COS to the TX, where they were driven too, equals M from the TX within 0.001 %. At every gap SIN and COS are within 0.3 % of each other in amplitude and 90.0° apart, and the angle error is 0.2° to 1.1° rms over the gaps. At 0.1 mm the angle error alternates in sign from one angle to the next: a ripple at four periods per electrical period, the fastest the angles can show, which third or fifth harmonics of the coupling would give, and those fade faster with the gap than the sine itself. SIN's amplitude is 6.66 nH at 0.1 mm, 5.07 nH at 0.5 mm, 3.37 nH at 1 mm, 2.23 nH at 1.5 mm and 1.49 nH at 2 mm (146 down to 33 mV of EMF at 1 A). L TX moves by 0.3 nH at most over the turn, and rises from 104.0 nH at 0.1 mm to 133.0 nH at 2 mm; with the rotor away it is 138.9 nH, where the generator estimated 116 nH with the rotor and 144 nH without. The meshes have 140,795 to 230,357 nodes, 12 to 21 element layers through the copper, board and gap, and each solve took 1.5 to 9.3 min and 4.7 to 9.9 GB on 4 MPI ranks.

## The folder

| Folder | What is in it |
|---|---|
| [`Boards/`](Boards/) | straight from the generator: the stator and rotor boards, `Parameters.txt`, the pictures and the parameter files it was run with |
| [`3D_Geometry/`](3D_Geometry/) | KESE's export of the stator and rotor (STL solids, `materials.json`, STEP, KESE's report), written by the first run; `source.json` records the board's hash, so a changed board is exported again |
| [`Palace Simulation/`](Palace%20Simulation/) | `test_spec.json` (every board fact the simulation needs, with `"rx_port": "cut"` and each receiver's `cut`), `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` (S0's, unchanged): `simulation.py` meshes and solves each angle and writes the results, [`RotorStator_AngleSetup/`](Palace%20Simulation/RotorStator_AngleSetup/) (the rotor over the stator at each angle), and the runs under `case/`, which git ignores |
| [`Results/`](Results/) | `expected_results.json` (the generator's estimates), [`SINCOS_Results.md`](Results/SINCOS_Results.md) with every gap on one page, the charts of every gap together (`SINCOS_gaps.webp`, and `_SIN` and `_COS` apart), and a folder for each air gap (`0d1mm_AirGap`, `0d5mm_AirGap`, `1mm_AirGap`, `1d5mm_AirGap`, `2mm_AirGap`, the point written as d) with the runs' `results_gap<gap>mm.json`, `.csv` and `.webp` |

Beside this README, `S0_1x_OD22_2L_tiny_TXtop_Cut_stator_and_rotor.webp` is the generator's picture of the boards, `S0_1x_OD22_2L_tiny_TXtop_Cut_palace_setup.webp` shows how they sit in Palace, and `S0_1x_OD22_2L_tiny_TXtop_Cut_cuts.webp` shows where SIN and COS are opened.

## Running it

| Air gap | Mesh level | Nodes | Element layers | MPI ranks | Memory a solve | Time a solve |
|---|---|---|---|---|---|---|
| 0.1 mm | 0.25 | 140,795 to 142,127 | 12 | 4 | 4.7 to 6.2 GB | 1.5 to 5.0 min |
| 0.5 mm | 0.25 | 160,259 to 161,729 | 14 | 4 | 5.2 to 6.9 GB | 1.7 to 5.2 min |
| 1 mm | 0.25 | 179,723 to 181,331 | 16 | 4 | 5.8 to 7.8 GB | 2.0 to 6.5 min |
| 1.5 mm | 0.25 | 208,919 to 210,734 | 19 | 4 | 6.7 to 9.0 GB | 2.5 to 7.8 min |
| 2 mm | 0.25 | 228,383 to 230,357 | 21 | 4 | 7.3 to 9.9 GB | 2.6 to 9.3 min |

Each solve is GMRES with hypre's AMS, at about 33 kB a mesh node, and 44 kB at the first angle of each gap, where the three coils are driven in turn (4.7 to 9.9 GB here), on 2 MPI ranks or 4 alike; a 16 GB machine runs two at once (`--jobs 2`) where a solve stays under 7 GB. Level 0.25 is the default (`--level` makes the copper's mesh finer); see [S0's README](../S0_1x_OD21_2L_tiny/README.md#what-the-solver-does) for what a finer mesh moves.

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
