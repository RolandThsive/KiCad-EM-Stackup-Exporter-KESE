# S0_1x_OD21_2L_tiny

The smallest coil set that is still a whole angle sensor, made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator) for one job: the SIN and COS curves over a full turn of the rotor, at any air gap, on a small machine. It is not one of the ten boards of the brief, and it is not meant to be built: its TX is too small for the IPS2550's tank (the generator warns about it, see below).

The curves, the fits and the angle error are in [Results/SINCOS_Results.md](Results/SINCOS_Results.md), one page for every air gap solved.

## Results at each air gap

| Air gap | Amplitude SIN / COS | Angle error | Solves passing the checks | L TX over the turn |
|---|---|---|---|---|
| 2 mm | 1.23 / 1.23 nH (27 / 27 mV) | 0.2° rms, 0.2° peak | 8 of 8 | 122.9 to 123.0 nH |
| 1.5 mm | 1.88 / 1.88 nH (41 / 41 mV) | 0.1° rms, 0.2° peak | 8 of 8 | 121.2 to 121.3 nH |
| 1 mm | 2.93 / 2.93 nH (64 / 64 mV) | 0.1° rms, 0.1° peak | 8 of 8 | 118.3 to 118.4 nH |
| 0.5 mm | 4.62 / 4.62 nH (102 / 102 mV) | 0.1° rms, 0.1° peak | 8 of 8 | 113.0 to 113.2 nH |
| 0.1 mm | 6.44 / 6.44 nH (142 / 142 mV) | 0.5° rms, 0.6° peak | 8 of 8 | 103.0 to 103.3 nH |

![SIN at each air gap](Results/SINCOS_gaps_SIN.webp)

*SIN at each air gap, one dot per solve; a ring would mark a solve that fails the checks under "What the solver does" (none does). [`SINCOS_gaps_COS.webp`](Results/SINCOS_gaps_COS.webp) is the same for COS, and [`SINCOS_gaps.webp`](Results/SINCOS_gaps.webp) has both.*

Every solve converged and passes the checks: the TX's L from its port and from the field's energy agree within 0.005 %, where 1 % is allowed, and M back from SIN and COS to the TX, where they were driven too, equals M from the TX within 0.001 %. At every gap SIN and COS are within 0.2 % of each other in amplitude and 90.0° apart, and the angle error is 0.1° to 0.5° rms over the gaps. At 0.1 mm the angle error alternates in sign from one angle to the next: a ripple at four periods per electrical period, the fastest the angles can show, which third or fifth harmonics of the coupling would give, and those fade faster with the gap than the sine itself. SIN's amplitude is 6.44 nH at 0.1 mm, 4.62 nH at 0.5 mm, 2.93 nH at 1 mm, 1.88 nH at 1.5 mm and 1.23 nH at 2 mm (142 down to 27 mV of EMF at 1 A). L TX moves by 0.2 nH at most over the turn, and rises from 103.1 nH at 0.1 mm to 123.0 nH at 2 mm; with the rotor away it is 127.1 nH, where the generator estimated 109 nH with the rotor and 132 nH without. The meshes have 132,281 to 216,718 nodes, 12 to 21 element layers through the copper, board and gap, and each solve took 2 to 12 min and 4.4 to 9.3 GB on 2 or 4 MPI ranks.

## The folder

This layout is the template: [`../new_coil.py`](../new_coil.py) makes the same folders for any other single coil set from the generator (`3D_Geometry/` is filled by the first run), and the scripts in `Palace Simulation/` run it without a change.

| Folder | What is in it |
|---|---|
| [`Boards/`](Boards/) | straight from the generator: the stator and rotor boards, `Parameters.txt`, the pictures and the parameter files it was run with |
| [`3D_Geometry/`](3D_Geometry/) | KESE's export of the stator and rotor (STL solids, `materials.json`, STEP, KESE's report), written by the first run; `source.json` records the board's hash, so a changed board is exported again |
| [`Palace Simulation/`](Palace%20Simulation/) | `test_spec.json` (every board fact the simulation needs), `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py`: `simulation.py` meshes and solves each angle and writes the results, [`RotorStator_AngleSetup/`](Palace%20Simulation/RotorStator_AngleSetup/) (the rotor over the stator at each angle), and the runs under `case/`, which git ignores |
| [`Results/`](Results/) | `expected_results.json` (the generator's estimates), [`SINCOS_Results.md`](Results/SINCOS_Results.md) with every gap on one page, the charts of every gap together (`SINCOS_gaps.webp`, and `_SIN` and `_COS` apart), and a folder for each air gap (`0d1mm_AirGap`, `0d5mm_AirGap`, `1mm_AirGap`, `1d5mm_AirGap`, `2mm_AirGap`, the point written as d) with the runs' `results_gap<gap>mm.json`, `.csv` and `.webp` |

Beside this README, `S0_1x_OD21_2L_tiny_stator_and_rotor.webp` is the generator's picture of the boards and `S0_1x_OD21_2L_tiny_palace_setup.webp` shows how they sit in Palace.

## The board

Outline 21.0 mm, bore 4.0 mm, 2 copper layers, board 0.8 mm, air gap 1.0 mm by default (any other with `--gap`). One coil set: a TX of one turn on each layer in series, and two RX coils, SIN and COS, of one period per turn. The rotor is a half ring of copper, so a full turn of it gives one period of each curve: SIN follows the sine of the rotor's angle and COS its cosine.

![stator and rotor](S0_1x_OD21_2L_tiny_stator_and_rotor.webp)

*Drawn by the generator: its `Boards/Coil_2_10.5_1_1_1_Series_SteppedDiagonal_Representative.svg`, as a WebP. `Boards/..._Actual.svg` is the copper at its true size.*

| Coil set | TX | SIN | COS | Frequency | Periods per revolution (N) | Electrical period |
|---|---|---|---|---|---|---|
| 1 | TX, 1 + 1 turns, r = 7.2 mm | SIN (net `2`) | COS (net `1`) | 3.5 MHz | 1 | 360° mechanical |

| RX band | Rotor copper ring | Sectors | Metal fraction |
|---|---|---|---|
| 3.2 to 6.1 mm | 2.52 to 7.8 mm | 1 | 0.50 |

Where each coil is opened for its terminals (KiCad coordinates, mm; the rotation axis is at (100, 100)):

| Net | Kind | Where | Terminals |
|---|---|---|---|
| `TX` (TX) | TX ends | (109.8, 100), F.Cu and B.Cu | the two coil ends, stacked at one point on two layers |
| `2` (SIN) | RX via (fallback) | via at (97.737, 102.263) | the generator found no cut spot: the via is left out, and its two pads are the terminals |
| `1` (COS) | RX via (fallback) | via at (97.737, 97.737) | as for SIN |

The fallback via of each RX coil is its layer-change via farthest from the TX copper (4.0 mm, on the inner edge of the band), of the two such on the side away from the TX terminal.

## How it was made

The generator at commit `32bf9cb`, S2's parameter files with five values changed (the files used are in [`Boards/parameter_files`](Boards/parameter_files/), and [`Boards/Parameters.txt`](Boards/Parameters.txt) is the generator's record of the run):

| Parameter | S2 | S0 | Why |
|---|---|---|---|
| `LOOPS` | 4 | 1 | one period per turn: the curves over a full turn are one sine and one cosine |
| `TX_TURNS` | 3 | 1 | less copper; the TX's turns add little to the coupling's shape |
| `INNER_EDGE_RADIUS_MM` | 10.0 | 2.0 | a small board |
| `OUTER_EDGE_RADIUS_MM` | 20.0 | 10.5 | 10.0 left a via 0.11 mm from other copper; 10.5 gives 0.274 mm (at least 0.2) |
| `PCB_THICKNESS_MM` | 1.6 | 0.8 | two fewer wedge layers through the board |

The generator's two warnings, both expected: the TX tank's parallel resistance would be about 12 Ω where the IPS2550 needs 250 Ω (more TX turns would fix it), and it found no spot with room for the two lead vias of each RX coil (so each RX coil is opened at a via instead).

## What the solver does

Palace, frequency-domain (its driven solve) at 3.5 MHz, with Nédélec edge elements of order 1 on the 2.5D mesh: the copper is a conductor of 5.8e7 S/m, everything else is air (FR-4 and solder mask too), and the outside of the domain, a cylinder whose radius is three board radii and which reaches as far above the rotor and below the stator, is a perfect conductor. Each coil is opened by a lumped port, a sheet across the place where it is opened with a resistance across it: the TX's has 50 Ω and the drive, SIN's and COS's have 1 MΩ. The TX's current comes from its port's voltage and the drive, and each receiver's voltage over that current gives its mutual inductance, M = V / (jωI). The EMF is 2πfM × 1 A: 1 nH is 22 mV at 3.5 MHz.

![How the stator and rotor are set up in Palace](S0_1x_OD21_2L_tiny_palace_setup.webp)

*How the boards are set up in Palace, drawn by [`rig_picture.py`](Palace%20Simulation/rig_picture.py) from the same geometry the mesh is built from. The rotor sits over the stator copper side down, its copper 1 mm above the stator's top copper, and turns about the board's centre. No trace is cut: the generator found no spot on this small board to cut a receiver's trace, so each receiver is opened by leaving out one of its layer-change vias, the one farthest from the TX copper. Its two pads stay, and the port is a sheet standing between them across the board, 0.5 mm wide, from the lower pad's top face to the upper pad's lower face, with 1 MΩ across it; 1 MΩ leaves a receiver open to a few parts in a million, so the voltage across its port is its open-circuit EMF. The TX is opened where its two ends lie stacked on the two layers, and its port, 0.16 mm wide, stands between them in the same way, with 50 Ω and the drive. FR-4 and solder mask are air to this solve.*

Each solve is GMRES preconditioned by hypre's AMS (the auxiliary-space Maxwell solver), iterated until the residual is 1e-8 of where it started (at most 2000 iterations). On S0 at 1 mm, 0°, a residual of 1e-10 moves L, R and M by under 3e-7 of themselves, and 1e-6 by under 4e-5. Two checks say whether a solve can be read: the TX's inductance from its port's voltage must equal the one from the magnetic energy of the whole field (2W/|I|²) within 1 %; and at the first angle of each gap SIN and COS are driven in turn too, so the M from each back to the TX can be checked against the M from the TX to it (reciprocity), within 1 %. Every solve in `Results/` meets both: L within 0.005 % and reciprocity within 0.001 %, in 101 to 168 iterations.

One solve per rotor angle, 0 to 315° in 45° steps by default (8 angles; `--step 10` for every 10°), and one with the rotor away (with the 1 mm results). The rotor is a half ring, so its outline turns with it and every angle gets its own mesh; the stator's mesh therefore differs a little between angles, which shows as small noise on the curves. The best sine fit and the rms of what it leaves are written with the results, so that noise is measured, not guessed.

| Air gap | Mesh level | Nodes | Element layers | MPI ranks | Memory a solve | Time a solve |
|---|---|---|---|---|---|---|
| 0.1 mm | 0.25 | 132,281 to 133,850 | 12 | 4 | 4.4 to 5.9 GB | 1.5 to 4.8 min |
| 0.5 mm | 0.25 | 150,523 to 152,263 | 14 | 2 | 4.9 to 6.5 GB | 3 to 10 min |
| 1 mm | 0.25 | 168,765 to 170,682 | 16 | 2 | 5.5 to 7.3 GB | 4 to 12 min |
| 1.5 mm | 0.25 | 196,125 to 198,306 | 19 | 4 | 6.4 to 8.5 GB | 2.4 to 7.6 min |
| 2 mm | 0.25 | 214,371 to 216,718 | 21 | 4 | 7.0 to 9.3 GB | 2.7 to 8.4 min |

How fine the mesh must be was measured on S0 at 1 mm and 0°, with the TX driven alone, one setting changed at a time from the bridge's defaults (the air's grading is how fast the elements grow away from the copper, in mm per mm, beside it and above and below it; times on 2 MPI ranks of a 4-core machine shared with other work):

| Mesh | Nodes | L TX | M SIN | M COS | Memory | Time |
|---|---|---|---|---|---|---|
| the bridge's defaults: level 0.25, the air graded 0.5 and 0.7, wedge layers up to 0.4 mm | 97,178 | 114.31 nH | −2.015 nH | 1.881 nH | 3.3 GB | 2.9 min |
| the copper's mesh twice as fine (level 0.5) | 129,982 | 116.11 nH | −1.997 nH | 1.890 nH | 4.9 GB | 5.6 min |
| the air graded twice as finely (0.25 and 0.35) | 109,233 | 115.78 nH | −2.065 nH | 1.927 nH | 3.8 GB | 3.4 min |
| the air graded four times as finely (0.125 and 0.175) | 132,857 | 116.62 nH | −2.081 nH | 1.952 nH | 4.8 GB | 4.0 min |
| wedge layers half as thick (up to 0.2 mm) | 126,166 | 115.91 nH | −2.015 nH | 1.884 nH | 4.1 GB | 3.4 min |
| **the air four times as finely and layers half as thick (as solved)** | **169,429** | **118.28 nH** | **−2.082 nH** | **1.955 nH** | **5.6 GB** | **4.4 min** |
| the same with the copper's mesh twice as fine | 256,049 | 120.01 nH | −2.072 nH | 1.954 nH | 9.3 GB | 9.0 min |

The air close round the thin tracks holds most of what a coarse mesh misses: grading it four times as finely raises M by 3 to 4 % and L TX by 2 %, while the copper's own mesh moves M by under 1 %. With the mesh as solved, M is within 0.5 % of the finest mesh that fits in 16 GB. L TX still rises, by 1.5 % with the copper's mesh twice as fine: first-order edge elements give a lower bound on the field's energy, so L TX here reads low, by about 5 % if each refinement keeps adding half as much as the one before.

The receivers' ports were settled on the same board. KESE exports a via with its drill hole through the pads, and a port sheet standing over the hole of a left-out via does not end on copper where it crosses the hole: drawn into the mesh in pieces of 0.025 mm, such a sheet read M 13 % low. A via that is left out is not drilled, so its two pads are filled over the hole (`voids()` in `simulation.py`); the sheet then reads the same M in pieces as drawn whole, within 0.5 %.

## Running it

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

Use the Python of the branch's `.venv` (`bash bridge/setup_machine.sh` makes it, and installs what Palace runs with). Each gap writes into its own folder in `Results/`, named for the gap with the point written as d (`1mm_AirGap`, `0d5mm_AirGap`): `results_gap<gap>mm.json` (every solve, the fit, the angle error), `results_gap<gap>mm.csv` (angle, M of SIN and COS in nH, the TX's L, and the EMFs in mV) and `results_gap<gap>mm.webp` (the chart, drawn by [`make_charts.py`](Palace%20Simulation/make_charts.py): a dot for each solve, a solid line joining them, and dots for the ideal sine and cosine). [`SINCOS_Results.md`](Results/SINCOS_Results.md) puts every gap on one page: each graph with a caption, the fit, the angle error at each angle, every solve and the generator's expectation, and once two gaps are solved, a chart with both. An angle already in the results is skipped, so a stopped sweep picks up where it was; `--merge` adds the solves of the same gap from other machines' results files.

## The angle error

[`angle_error.py`](Palace%20Simulation/angle_error.py) works it out after every solve, and `simulation.py` writes it into `SINCOS_Results.md`. Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS). The error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is; the rms and the worst of them are the angle error, in electrical degrees (the same as mechanical here, with one period per turn). The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair.

## The workflow for any generated coil

Any coil set from the generator's Single Coil Set Generator goes through the same five steps, and S0 was made this way. [`../new_coil.py`](../new_coil.py) does the setting up, and this folder's scripts run every board it sets up without a change, because they read each board fact from `test_spec.json`.

1. **Make the coil.** In the generator's checkout, set the parameters in `Generators/Single Coil Set Generator/Parameters/` (S0's are in [`Boards/parameter_files`](Boards/parameter_files/)) and run `python Generator/Run/RunCoilGenerator.py` from `Generators/Single Coil Set Generator`. It writes `Output/Coil_<...>/`: the two boards, `Parameters.txt` and two pictures. `Generators/resources` must sit beside it, as it does in a full checkout, or the lead-cutting suggestion and the pictures are missing. Read the warnings it prints: a via too close to other copper means the board is not right yet (S0 needed `OUTER_EDGE_RADIUS_MM` 10.5 for that), while the TX tank warning does not matter to the simulation.
2. **Set it up for Palace.** In this folder's parent:

       python new_coil.py "<checkout>/Generators/Single Coil Set Generator/Output/Coil_..." S6_my_board

   It makes `S6_my_board/` laid out as this folder: `Boards/` with the boards, `Parameters.txt`, the parameter files and the pictures; `Palace Simulation/` with `test_spec.json`, `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py`; `Results/` with `expected_results.json`; and a README beside them. The first run fills `3D_Geometry/` with KESE's export of the two boards. Then it builds the mesh at one angle and prints its size and the memory a solve needs. `--angles 16` gives more angles over the rotor's period, `--level` another mesh level, and `--no-estimate` skips the mesh.
3. **Check it.** A solve needs about 33 kB a mesh node, and 44 kB where the three coils are driven in turn, on 2 MPI ranks or 4 alike: S0's meshes of 132,000 to 217,000 nodes took 4.4 to 9.3 GB. If the estimate is too big, make the coil smaller (fewer loops, fewer TX turns, a smaller or thinner board each shrink the mesh) or use a lower `--level`. Then check the terminals in the new README against the picture. The TX is opened at its two stacked ends. Each RX coil is opened at one of its layer-change vias: the one nearest the generator's suggested cut, or, where it found no cut spot, the one farthest from the TX copper.
4. **Run it.** `python simulation.py` in the new folder's `Palace Simulation/` solves the rotor away, then each angle of `test_spec.json`. `--gap 0.5` sets another air gap and `--step 10` solves every 10 degrees over the whole turn. A stopped sweep picks up where it was. An angle of S0's size takes 4 to 7 minutes on 2 cores.
5. **Read the results.** In `Results/<gap>_AirGap/`, `results_gap<gap>mm.json` has every solve, the best sine fit and the angle error, `.csv` the curves in nH and mV, and `.webp` the chart, with a dot for each solve, a solid line joining them and dots for the ideal sine and cosine. `SINCOS_Results.md` gathers all of it, every gap on one page, and is rewritten after every solve. `python simulation.py --plot` or `python make_charts.py` redraws them. Commit the folder without `case/`, which git ignores.

The limits: single coil sets only, since a `DualCoil_` board has two sets. `new_coil.py` also sets up S1 to S5 (two and four layers) with their TX ends found where their own specs have them, but none of those has been solved this way yet.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [../LICENSE.md](../LICENSE.md); this branch's GPL-3.0 covers `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` only.
