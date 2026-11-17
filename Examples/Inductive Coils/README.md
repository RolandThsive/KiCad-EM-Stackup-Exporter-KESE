# Inductive Coils

Inductive angle-encoder boards from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator), one folder each. A **stator** board carries one TX coil and two RX coils (SIN and COS). A **rotor** board with copper sectors sits 1.0 mm above it by default. The TX is driven at 3 to 5 MHz, the rotor's eddy currents change how much of the TX's field reaches each RX coil, and the two RX voltages follow the sine and cosine of the rotor's angle.

## What this branch checks

At 3 to 5 MHz the boards are about 1/2000 of a wavelength across, so the physics is magneto-quasi-static, which is what PyPEEC solves. Per board it gives the TX's inductance and resistance with the rotor away and over the stator, the coupling from the TX to SIN and COS against the rotor's angle at each air gap, and what follows from it: how well SIN and COS match and the angle error. Every solve is checked by working the TX's L and R out two ways, from its voltage and from the stored energy and the losses; a solve is read when both agree within 1 %.

PyPEEC draws the copper as voxels on one uniform grid: 50 µm in the board's plane on these boards (a 0.2 mm trace is 4 voxels across), and one voxel layer of about 35 µm through each copper sheet. The air needs no voxels, so there is no air box. On S0_1x_OD23_2L_tiny_TX3top_Cut at a 1 mm gap and 0°, smaller voxels moved the numbers by less than half a percent, except R, whose traces' stepped edges take longer to settle:

| Voxels | Grid | L TX | R TX | M SIN | M COS | Memory | Time on 4 cores |
|---|---|---|---|---|---|---|---|
| 50 µm | 7.4 million | 266.15 nH | 492.8 mΩ | 3.167 nH | 3.781 nH | 2.3 GB | 5 min |
| 35 µm | 15.1 million | 265.23 nH (−0.35 %) | 480.5 mΩ (−2.5 %) | 3.176 nH (+0.27 %) | 3.786 nH (+0.14 %) | 4.6 GB | 13 min |
| 25 µm | 29.5 million | 264.56 nH (−0.60 %) | 470.8 mΩ (−4.5 %) | 3.177 nH (+0.32 %) | 3.768 nH (−0.35 %) | 9.1 GB | 26 min |

So 50 µm is what every board here is solved with: it reads M and L TX to about half a percent, while R TX reads at least 5 % high (it is still falling at 25 µm). `simulation.py --voxel 0.035` runs another size as a trial, kept in `case/`.

## The boards here

All of them are S0 and boards made from it. A solve takes 2 to 4 GB and 4 to 10 minutes on 4 cores, more at the wider gaps (the grid grows taller with the gap), so any 8 GB machine runs them:

| Board | What it is |
|---|---|
| [S0_1x_OD21_2L_tiny](S0_1x_OD21_2L_tiny/) | S0: 21 mm across, one period per turn, the TX one turn on each layer, a half-ring rotor |
| [S0_1x_OD21_2L_tiny_TXtop](S0_1x_OD21_2L_tiny_TXtop/) | the same board with the TX two turns on the top layer (the generator narrows the RX band to fit them) |
| [S0_1x_OD22_2L_tiny_TXtop](S0_1x_OD22_2L_tiny_TXtop/) | the TX two turns on the top layer around S0's own RX coils, the board grown to 22.2 mm |
| [S0_1x_OD22_2L_tiny_TXtop_Cut](S0_1x_OD22_2L_tiny_TXtop_Cut/) | the 22 mm board with SIN and COS opened by a cut in a top trace instead of a left-out via |
| [S0_1x_OD23_2L_tiny_TX3top_Cut](S0_1x_OD23_2L_tiny_TX3top_Cut/) | the TX three turns on the top layer around S0's RX coils, 23.4 mm, opened by cuts |
| [S0d2_1x_OD23_2L_tiny_TX3top_Cut](S0d2_1x_OD23_2L_tiny_TX3top_Cut/) | the three-turn board with two electrical periods per turn and a rotor of two sectors, so the curves repeat every 180°; solved at 16 angles over the whole turn |

Every board folder holds the same files and stands on its own: its README has the board, its results at each air gap and how to run it. [`Comparisons/`](Comparisons/) sets the boards side by side, with the scripts that print those tables and draw the charts.

## Results in short

Every board is solved at 0.1, 0.5, 1, 1.5 and 2 mm, at 8 angles over the turn (S0d2 at 16), with the rotor taken away once at 1 mm: 286 solves, every one readable, its L and R worked out two ways agreeing within 0.001 %. SIN's amplitude, the best sine through each gap's solves (1 nH is 22 mV of EMF with 1 A at 3.5 MHz in the TX):

| Board | 0.1 mm | 0.5 mm | 1 mm | 1.5 mm | 2 mm |
|---|---|---|---|---|---|
| [S0](S0_1x_OD21_2L_tiny/) | 6.48 nH | 4.66 nH | 2.94 nH | 1.87 nH | 1.23 nH |
| [21 mm, 2 TX turns on top](S0_1x_OD21_2L_tiny_TXtop/) | 5.23 nH | 3.85 nH | 2.43 nH | 1.53 nH | 0.99 nH |
| [22 mm, 2 TX turns on top](S0_1x_OD22_2L_tiny_TXtop/) | 6.68 nH | 5.10 nH | 3.38 nH | 2.22 nH | 1.49 nH |
| [22 mm, 2 TX turns on top, opened by cuts](S0_1x_OD22_2L_tiny_TXtop_Cut/) | 6.60 nH | 5.04 nH | 3.34 nH | 2.20 nH | 1.47 nH |
| [23 mm, 3 TX turns on top, opened by cuts](S0_1x_OD23_2L_tiny_TX3top_Cut/) | 9.28 nH | 7.25 nH | 4.98 nH | 3.39 nH | 2.33 nH |
| [23 mm, 3 TX turns on top, opened by cuts, 2 periods per turn](S0d2_1x_OD23_2L_tiny_TX3top_Cut/) | 9.60 nH | 7.14 nH | 4.61 nH | 2.94 nH | 1.89 nH |

SIN and COS match within 0.4 % and sit 90° apart on every board. The angle error is 0.1° to 0.5° rms from 0.5 to 2 mm and up to 1.5° at 0.1 mm, where every board shows the fourth-harmonic ripple that two-coil sensors typically have. On S0, L TX with the rotor away is 3.0 % over a hand calculation (two coaxial rings in series, by Grover's and Maxwell's formulas). [`Comparisons/`](Comparisons/README.md) sets the boards side by side.

## A small board for the SIN and COS curves

[S0_1x_OD21_2L_tiny](S0_1x_OD21_2L_tiny/) is the smallest coil set the generator makes that is still a whole sensor (OD 21 mm, one period per turn, a TX of one turn per layer, a half-ring rotor). Its README says how it was made and how to run it.

Any other single coil set from the generator is set up the same way, in one command: [`new_coil.py`](new_coil.py) turns the generator's output folder into a folder here laid out as S0's (`Boards/` straight from the generator, `PyPEEC Simulation/` with S0's `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py`, which run it as they are, `Results/`, and `3D_Geometry/` with KESE's export of the boards once the first run makes it), and prints the voxels, memory and time a solve needs. The steps are in [S0's README](S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

## Placement and terminals, in short

* The rotation axis is KiCad's point (100, 100), z points up from the stator towards the rotor, and the top face of the stator's F.Cu copper is z = 0. KiCad's y axis points down, which flips every rotation sense in a y-up model; each results file says which convention the run used.
* The rotor is `Rotor.kicad_pcb` as drawn, not mirrored, copper side down, its copper face at z = +1.0 mm. Rotor angle θ turns it about the axis by (x, y) → (x cos θ − y sin θ, x sin θ + y cos θ) in KiCad's coordinates.
* KESE exports both boards with solder mask on both faces; FR-4 and mask are insulators with μr 1, which to a magneto-quasi-static solve are air, so only the copper is drawn.
* Each coil is opened where the real board gets its leads (`test_spec.json` → `terminals`): the TX at its two stacked ends, an RX by leaving one layer-change via out, or, in the `_Cut` folders, by a 0.2 mm cut across a top trace. At the TX's ends and at a cut, its two terminals are its voxels that share a face with the gap, one group each side; at a left-out via, the two pads are filled over the drill hole and each terminal is the one voxel on the via's axis in its pad (the pads' whole inner rings, tried first, let current circle through them and loaded the TX). 1 A is driven into the TX's first terminal and taken out of its second (held at 0 V); SIN and COS carry 0 A, so the voltage between their terminals is the open-circuit EMF. The rotor carries eddy currents only: one voxel of each separate piece of it is held at 0 V, which lets no current in or out.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [LICENSE.md](LICENSE.md); this branch's GPL-3.0 covers only the scripts here (`new_coil.py`, each board's `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py`, and those in `Comparisons/`).
