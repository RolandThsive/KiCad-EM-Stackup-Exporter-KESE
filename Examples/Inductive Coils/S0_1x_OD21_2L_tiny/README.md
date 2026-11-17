# S0_1x_OD21_2L_tiny

The smallest coil set that is still a whole angle sensor, made with the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator) for one job: the SIN and COS curves over a full turn of the rotor, at any air gap, on a small machine. It is not one of the generator pack's ten boards, and it is not meant to be built: its TX is too small for the IPS2550's tank (the generator warns about it, see below).

The curves, the fits and the angle error are in [Results/SINCOS_Results.md](Results/SINCOS_Results.md), one page for every air gap solved.

## Results at each air gap

| Air gap | Amplitude SIN / COS | Angle error | Solves passing both checks | L TX over the turn |
|---|---|---|---|---|
| 2 mm | 1.17 / 1.17 nH (26 / 26 mV) | 0.2° rms, 0.4° peak | 8 of 8 | 131.9 to 132.1 nH |
| 1.5 mm | 1.79 / 1.79 nH (39 / 39 mV) | 0.2° rms, 0.4° peak | 8 of 8 | 130.6 to 130.9 nH |
| 1 mm | 2.82 / 2.83 nH (62 / 62 mV) | 0.2° rms, 0.4° peak | 8 of 8 | 127.0 to 127.5 nH |
| 0.5 mm | 4.52 / 4.53 nH (99 / 100 mV) | 0.3° rms, 0.4° peak | 8 of 8 | 120.9 to 121.9 nH |
| 0.1 mm | 6.38 / 6.39 nH (140 / 140 mV) | 0.6° rms, 0.8° peak | 8 of 8 | 111.0 to 113.0 nH |

![SIN at each air gap](Results/SINCOS_gaps_SIN.webp)

*SIN at each air gap, one dot per solve; a ring would mark a solve that fails the two checks under "What the solver does" (none does). [`SINCOS_gaps_COS.webp`](Results/SINCOS_gaps_COS.webp) is the same for COS, and [`SINCOS_gaps.webp`](Results/SINCOS_gaps.webp) has both.*

Every solve passes both checks, and at every gap the curves are a clean sine and cosine: 0.2° to 0.6° rms of angle error, with SIN and COS within 0.3 % of each other in amplitude and 90.0° apart (89.8° at 0.1 mm). The signal is 6.38 nH for SIN at 0.1 mm and falls by about a third for each half millimetre after that: 4.52, 2.82, 1.79 and 1.17 nH at 0.5, 1, 1.5 and 2 mm (140 down to 26 mV of EMF at 1 A). At 0.1 mm the angle error alternates in sign from one angle to the next: a ripple at four periods per turn, the fastest eight angles can show, which third or fifth harmonics of the coupling would give, and those fade faster with the gap than the sine itself; from 0.5 mm up what is left is about 0.2° rms with no such pattern, the size of the voxels' own noise (the rotor's edges fall on the voxels a little differently at each angle). L TX moves by 2 nH at most over the turn at 0.1 mm and by 0.2 nH at 2 mm, and rises from 112.0 nH at 0.1 mm to 132.0 nH at 2 mm; with the rotor away it is 136.1 nH, where the generator estimated 109 nH with the rotor and 132 nH without. The grid has 33 voxel layers at 0.1 mm and 81 at 2 mm (3.6 to 8.9 million voxels), and each solve took 2 to 12 minutes and at most 2.7 GB.

Against the Elmer branch, which solves the same board from the same export ([`../Comparisons`](../Comparisons/)): SIN's amplitude agrees within 1 % from 1 to 2 mm, and PyPEEC's is 1.5 % higher at 0.5 mm and 2.5 % at 0.1 mm; the angle error has the same alternating pattern at 0.1 mm. L TX is 11 to 13 % higher here than in Elmer at every gap. Two coaxial rings of 7.2 mm radius 0.765 mm apart, in series, have 132.5 nH by Grover's and Maxwell's formulas alone, before the leads to the terminal add theirs: PyPEEC's 136.1 nH with the rotor away is 2.7 % over that and Elmer's 122.6 nH 7.5 % under it.

## The folder

This layout is the template: [`../new_coil.py`](../new_coil.py) makes the same folders for any other single coil set from the generator (`3D_Geometry/` is filled by the first run), and the scripts in `PyPEEC Simulation/` run it without a change.

| Folder | What is in it |
|---|---|
| [`Boards/`](Boards/) | straight from the generator: `Stator.kicad_pcb` and `Rotor.kicad_pcb` with their `.kicad_pro` files, `Parameters.txt` (its record of the run), its two pictures (`_Representative.svg` and `_Actual.svg`), and [`parameter_files/`](Boards/parameter_files/), the six files it was run with |
| [`3D_Geometry/`](3D_Geometry/) | what KESE made from the two boards, the geometry the voxels are drawn from: for each of [`Stator/`](3D_Geometry/Stator/) and [`Rotor/`](3D_Geometry/Rotor/), one STL per solid in `stl/` (each coil net's copper, the laminate, the solder mask), `materials.json` (each solid's role, net, layer and heights), the board as a STEP file, and KESE's `report.txt` and `parameters.txt`. `source.json` records the board file's hash, KESE's version and the settings; `simulation.py` reuses the export while the board is unchanged and runs KESE again when it changes. It is the same export as the Elmer branch's. (This is KESE's output; the `3D_Geometry/` at the branch's root is where KESE itself goes.) |
| [`PyPEEC Simulation/`](PyPEEC%20Simulation/) | [`test_spec.json`](PyPEEC%20Simulation/test_spec.json) (every board fact the simulation needs: layers, gap, terminals, angles, the voxels' size), [`simulation.py`](PyPEEC%20Simulation/simulation.py) (draws the voxels and solves each angle and writes the results), [`angle_error.py`](PyPEEC%20Simulation/angle_error.py) (the angle error at each angle), [`make_charts.py`](PyPEEC%20Simulation/make_charts.py) (the charts, as WebP), [`rig_picture.py`](PyPEEC%20Simulation/rig_picture.py), which draws the picture of how the boards are set up in PyPEEC, and [`angle_setup.py`](PyPEEC%20Simulation/angle_setup.py), which draws the rotor over the stator at each angle into [`RotorStator_AngleSetup/`](PyPEEC%20Simulation/RotorStator_AngleSetup/). The runs go under `case/` here, which git ignores |
| [`Results/`](Results/) | [`expected_results.json`](Results/expected_results.json) (the generator's estimates), [`SINCOS_Results.md`](Results/SINCOS_Results.md) gathering every gap on one page, the charts of every gap together (`SINCOS_gaps.webp`, and `_SIN` and `_COS` apart), and a folder for each air gap ([`0d1mm_AirGap/`](Results/0d1mm_AirGap/), [`0d5mm_AirGap/`](Results/0d5mm_AirGap/), [`1mm_AirGap/`](Results/1mm_AirGap/), [`1d5mm_AirGap/`](Results/1d5mm_AirGap/), [`2mm_AirGap/`](Results/2mm_AirGap/)) with the runs' `results_gap<gap>mm.json` (every solve and the fit), `.csv` (the curves in nH and mV) and `.webp` (the chart, and `_SIN` and `_COS` apart) |

Beside this README, `S0_1x_OD21_2L_tiny_stator_and_rotor.webp` is the generator's Representative SVG as a lossless WebP (the picture below), and `S0_1x_OD21_2L_tiny_pypeec_setup.webp` shows how the stator, rotor and terminals are set up in PyPEEC (under "What the solver does").

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
| `PCB_THICKNESS_MM` | 1.6 | 0.8 | a thinner board, fewer layers through it |

The generator's two warnings, both expected: the TX tank's parallel resistance would be about 12 Ω where the IPS2550 needs 250 Ω (more TX turns would fix it), and it found no spot with room for the two lead vias of each RX coil (so each RX coil is opened at a via instead).

## What the solver does

PyPEEC, magneto-quasi-static, with the PEEC method on voxels: the TX carries 1 A at 3.5 MHz, SIN and COS carry none, and their voltages over the TX's current give their mutual inductances M. The EMF is 2πfM × 1 A: 1 nH is 22 mV at 3.5 MHz.

![How the stator and rotor are set up in PyPEEC](S0_1x_OD21_2L_tiny_pypeec_setup.webp)

*How the boards are set up in PyPEEC, drawn by [`rig_picture.py`](PyPEEC%20Simulation/rig_picture.py) from the voxels simulation.py solves. The rotor sits over the stator copper side down, its copper 1 mm above the stator's top copper, and turns about the board's centre. Every piece of copper is drawn in voxels of 50 µm across and about 35 µm high, one layer through each copper sheet, and a via is a column of them; FR-4 and solder mask are air to this solve, and the air needs no voxels at all. No trace is cut: the generator found no spot on this small board to cut a receiver's trace, so each receiver is opened by leaving out one of its layer-change vias, the one farthest from the TX copper. Its two pads stay, and the receiver's voxels that border the gap between them are its two terminals; SIN and COS carry 0 A between them, so the voltage across the gap is their open-circuit EMF. The TX is opened where its two ends lie stacked on the two layers: 1 A goes into the voxels of one end and out of the other's, held at 0 V.*

Each solve is PyPEEC's own: the copper's voxels carry the unknowns, and the couplings between every pair of voxels are worked by FFTs over the grid, so the air takes nothing; GMRES, preconditioned with a sparse factorisation of the near couplings, solves the system to PyPEEC's default tolerance, in 2 to 4 iterations here. The rotor carries eddy currents only (one of its voxels is held at 0 V, which lets no current in or out). Two checks say whether a solve can be read: the TX's inductance from its voltage must equal the one from the stored magnetic energy (4W/|I|² with PyPEEC's peak phasors), and its resistance from the voltage the one from the losses (2P/|I|²), each within 1 %. Every solve in `Results/` meets both within 0.001 %.

One solve per rotor angle, 0 to 315° in 45° steps by default (8 angles; `--step 10` for every 10°), and one with the rotor away. The rotor's copper is drawn onto the voxels afresh at each angle, while the stator's voxels stay where they are; the rotor's edges then fall on the voxels a little differently at each angle, which shows as small noise on the curves. The best sine fit and the rms of what it leaves are written with the results, so that noise is measured, not guessed.

| Air gap | Grid (voxels of 50 µm, dz) | Copper voxels | Memory a solve | Time a solve |
|---|---|---|---|---|
| 2 mm | 358 × 306 × 81 = 8.9 million, dz 34.5 µm | 66,000 | 2.5 to 2.7 GB | 4 to 7 min |
| 1.5 mm | 358 × 306 × 79 = 8.7 million, dz 29.0 µm | 68,000 | 2.5 to 2.6 GB | 6 to 12 min |
| 1 mm | 358 × 306 × 52 = 5.7 million, dz 34.5 µm | 66,000 | 1.7 to 1.8 GB | 3 to 4 min |
| 0.5 mm | 358 × 306 × 34 = 3.7 million, dz 38.2 µm | 65,000 | 1.2 to 1.3 GB | 2 to 4 min |
| 0.1 mm | 358 × 306 × 33 = 3.6 million, dz 26.9 µm | 69,000 | 1.2 to 1.3 GB | 2 to 5 min |

The grid's z step dz is chosen at each gap so that the three copper sheets (the stator's two and the rotor's) land within a micron of a voxel layer; each sheet's resistivity is scaled by its voxels' thickness over the copper's 35 µm, so it keeps its sheet resistance. The times are of the machines that ran them (4 cores each). On S0_1x_OD23_2L_tiny_TX3top_Cut, voxels of 35 and 25 µm moved M and L TX by 0.6 % at most and R TX by 2.5 and 4.5 % (see the [coils' README](../README.md)).

## Running it

    cd "PyPEEC Simulation"
    python simulation.py                   # the rotor away, then 0 to 315 degrees every 45, at a 1 mm gap
    python simulation.py --gap 0.5         # the same at 0.5 mm
    python simulation.py --step 10         # every 10 degrees
    python simulation.py --voxel 0.035     # smaller voxels, a trial kept in case/ (more memory and time)
    python simulation.py --angles 0 --voxels-only   # draw one angle's voxels and say how many, solve nothing
    python simulation.py --plot            # redraw the table, the curves and SINCOS_Results.md
    python angle_error.py                  # print the angle error at each angle, and rewrite SINCOS_Results.md
    python make_charts.py                  # redraw every chart (WebP) and rewrite SINCOS_Results.md
    python rig_picture.py                  # redraw how the boards sit in PyPEEC, voxel by voxel
    python angle_setup.py                  # redraw the rotor at each angle

Use the Python of the branch's `.venv` (`bash bridge/setup_machine.sh` makes it). Each gap writes into its own folder in `Results/`, named for the gap with the point written as d (`1mm_AirGap`, `0d5mm_AirGap`): `results_gap<gap>mm.json` (every solve, the fit, the angle error), `results_gap<gap>mm.csv` (angle, M of SIN and COS in nH, the TX's L, and the EMFs in mV) and `results_gap<gap>mm.webp` (the chart, drawn by [`make_charts.py`](PyPEEC%20Simulation/make_charts.py): a dot for each solve, a solid line joining them, and dots for the ideal sine and cosine). [`SINCOS_Results.md`](Results/SINCOS_Results.md) puts every gap on one page: each graph with a caption, the fit, the angle error at each angle, every solve and the generator's expectation, and once two gaps are solved, a chart with both. An angle already in the results is skipped, so a stopped sweep picks up where it was. `--merge` adds the solves of the same gap from other machines' results files, which is how these were run: several machines, each taking whole gaps.

## The angle error

[`angle_error.py`](PyPEEC%20Simulation/angle_error.py) works it out after every solve, and `simulation.py` writes it into `SINCOS_Results.md`. Each channel gets its best sine over the rotor's period, M = offset + amplitude × sin(θ + phase). Each channel's offset is taken out and it is divided by its amplitude, so both swing between −1 and +1, as a decoder chip's offset and gain calibration does. The angle is read back as atan2(SIN, COS). The error at each angle is that reading less the true angle, less the average of all of them, since a fixed offset only moves where zero is; the rms and the worst of them are the angle error, in electrical degrees (the same as mechanical here, with one period per turn). The fit uses the same points as the error, so it measures how far the solves are from a perfect sine and cosine pair.

## The workflow for any generated coil

Any coil set from the generator's Single Coil Set Generator goes through the same five steps, and S0 was made this way. [`../new_coil.py`](../new_coil.py) does the setting up, and this folder's scripts run every board it sets up without a change, because they read each board fact from `test_spec.json`.

1. **Make the coil.** In the generator's checkout, set the parameters in `Generators/Single Coil Set Generator/Parameters/` (S0's are in [`Boards/parameter_files`](Boards/parameter_files/)) and run `python Generator/Run/RunCoilGenerator.py` from `Generators/Single Coil Set Generator`. It writes `Output/Coil_<...>/`: the two boards, `Parameters.txt` and two pictures. `Generators/resources` must sit beside it, as it does in a full checkout, or the lead-cutting suggestion and the pictures are missing. Read the warnings it prints: a via too close to other copper means the board is not right yet (S0 needed `OUTER_EDGE_RADIUS_MM` 10.5 for that), while the TX tank warning does not matter to the simulation.
2. **Set it up for PyPEEC.** In this folder's parent, with KESE copied into the branch's `3D_Geometry/` (or `KESE_PATH` set), as a new board needs exporting once:

       python new_coil.py "<checkout>/Generators/Single Coil Set Generator/Output/Coil_..." S6_my_board

   It makes `S6_my_board/` laid out as this folder: `Boards/` with the boards, `Parameters.txt`, the parameter files and the pictures; `PyPEEC Simulation/` with `test_spec.json`, `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py`; `Results/` with `expected_results.json`; and a README beside them. The first run fills `3D_Geometry/` with KESE's export of the two boards. Then it draws the voxels at one angle and prints the grid's size and the memory and time a solve needs. `--angles 16` gives more angles over the rotor's period, `--voxel` another voxel size, and `--no-estimate` skips the voxels.
3. **Check it.** A solve needs about 0.31 GB and 0.9 minute on 4 cores for each million voxels of the grid (copper or not), and the grid grows taller with the air gap: S0's 3.6 to 8.9 million voxels need 1.2 to 2.7 GB. If the estimate is too big, a smaller board or a larger `--voxel` shrinks it. Then check the terminals in the new README against the picture (`python rig_picture.py` draws them voxel by voxel). The TX is opened at its two stacked ends. Each RX coil is opened at one of its layer-change vias: the one nearest the generator's suggested cut, or, where it found no cut spot, the one farthest from the TX copper.
4. **Run it.** `python simulation.py` in the new folder's `PyPEEC Simulation/` solves the rotor away, then each angle of `test_spec.json`. `--gap 0.5` sets another air gap and `--step 10` solves every 10 degrees over the rotor's period. A stopped sweep picks up where it was. An angle of S0's size takes 2 to 12 minutes on 4 cores.
5. **Read the results.** In `Results/<gap>_AirGap/`, `results_gap<gap>mm.json` has every solve, the best sine fit and the angle error, `.csv` the curves in nH and mV, and `.webp` the chart, with a dot for each solve, a solid line joining them and dots for the ideal sine and cosine. `SINCOS_Results.md` gathers all of it, every gap on one page, and is rewritten after every solve. `python simulation.py --plot` or `python make_charts.py` redraws them. Commit the folder without `case/`, which git ignores.

The limits: single coil sets only, since a `DualCoil_` board has two sets. `simulation.py` has solved the S0 boards (two layers); `new_coil.py` also sets up S1 to S5 (two and four layers) with their TX ends found where their own specs have them, but none of those has been solved this way yet.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [../LICENSE.md](../LICENSE.md); this branch's GPL-3.0 covers `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py` only.
