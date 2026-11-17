# Inductive Coils

Inductive angle-encoder boards from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator), one folder each, the same boards as on the Elmer branch and laid out the same way. A **stator** board carries one TX coil and two RX coils (SIN and COS). A **rotor** board with copper sectors sits 1.0 mm above it by default. The TX is driven at 3 to 5 MHz, the rotor's eddy currents change how much of the TX's field reaches each RX coil, and the two RX voltages follow the sine and cosine of the rotor's angle.

## What this branch checks

At 3 to 5 MHz the boards are about 1/2000 of a wavelength across, so the physics is magneto-quasi-static, which is what PyPEEC solves. Per board it gives the TX's inductance and resistance with the rotor away and over the stator, the coupling from the TX to SIN and COS against the rotor's angle at each air gap, and what follows from it: how well SIN and COS match and the angle error. Every solve is checked by working the TX's L and R out two ways, from its voltage and from the stored energy and the losses; a solve is read when both agree within 1 %.

PyPEEC draws the copper as voxels on one uniform grid: 50 µm in the board's plane on these boards (a 0.2 mm trace is 4 voxels across), and one voxel layer of about 35 µm through each copper sheet. The air needs no voxels, so there is no air box. Going to 35 µm voxels on S0_1x_OD23_2L_tiny_TX3top_Cut at a 1 mm gap moved L TX by 0.35 % and M by 0.3 % at twice the memory and 2.6 times the time, so 50 µm is what every board here is solved with.

## The boards here

All of them are S0 and boards made from it. A solve takes 2 to 4 GB and 4 to 10 minutes on 4 cores, more at the wider gaps (the grid grows taller with the gap), so any 8 GB machine runs them:

| Board | What it is |
|---|---|
| [S0_1x_OD21_2L_tiny](S0_1x_OD21_2L_tiny/) | S0: 21 mm across, one period per turn, the TX one turn on each layer, a half-ring rotor |
| [S0_1x_OD21_2L_tiny_TXtop](S0_1x_OD21_2L_tiny_TXtop/) | the same board with the TX two turns on the top layer (the generator narrows the RX band to fit them) |
| [S0_1x_OD22_2L_tiny_TXtop](S0_1x_OD22_2L_tiny_TXtop/) | the TX two turns on the top layer around S0's own RX coils, the board grown to 22.2 mm |
| [S0_1x_OD22_2L_tiny_TXtop_Cut](S0_1x_OD22_2L_tiny_TXtop_Cut/) | the 22 mm board with SIN and COS opened by a cut in a top trace instead of a left-out via |
| [S0_1x_OD23_2L_tiny_TX3top_Cut](S0_1x_OD23_2L_tiny_TX3top_Cut/) | the TX three turns on the top layer around S0's RX coils, 23.4 mm, opened by cuts |
| [S0d2_1x_OD23_2L_tiny_TX3top_Cut](S0d2_1x_OD23_2L_tiny_TX3top_Cut/) | the three-turn board with two electrical periods per turn and a rotor of two sectors, so the curves repeat every 180° |

Every board folder holds the same files and stands on its own: its README has the board, its results at each air gap and how to run it. [`Comparisons/`](Comparisons/) sets the boards side by side once they are solved, with the scripts that print those tables and draw the charts.

## A small board for the SIN and COS curves

[S0_1x_OD21_2L_tiny](S0_1x_OD21_2L_tiny/) is the smallest coil set the generator makes that is still a whole sensor (OD 21 mm, one period per turn, a TX of one turn per layer, a half-ring rotor). Its README says how it was made and how to run it.

Any other single coil set from the generator is set up the same way, in one command: [`new_coil.py`](new_coil.py) turns the generator's output folder into a folder here laid out as S0's (`Boards/` straight from the generator, `PyPEEC Simulation/` with S0's `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py`, which run it as they are, `Results/`, and `3D_Geometry/` with KESE's export of the boards once the first run makes it), and prints the voxels, memory and time a solve needs. The steps are in [S0's README](S0_1x_OD21_2L_tiny/README.md#the-workflow-for-any-generated-coil).

## Placement and terminals, in short

* The rotation axis is KiCad's point (100, 100), z points up from the stator towards the rotor, and the top face of the stator's F.Cu copper is z = 0. KiCad's y axis points down, which flips every rotation sense in a y-up model; each results file says which convention the run used.
* The rotor is `Rotor.kicad_pcb` as drawn, not mirrored, copper side down, its copper face at z = +1.0 mm. Rotor angle θ turns it about the axis by (x, y) → (x cos θ − y sin θ, x sin θ + y cos θ) in KiCad's coordinates.
* KESE exports both boards with solder mask on both faces, as on the Elmer branch; FR-4 and mask are insulators with μr 1, which to a magneto-quasi-static solve are air, so only the copper is drawn.
* Each coil is opened where the real board gets its leads (`test_spec.json` → `terminals`): the TX at its two stacked ends, an RX by leaving one layer-change via out, or, in the `_Cut` folders, by a 0.2 mm cut across a top trace. Its two terminals are its voxels that share a face with the gap, one group each side: 1 A is driven into the TX's first and taken out of its second (held at 0 V); SIN and COS carry 0 A, so the voltage between their terminals is the open-circuit EMF. The rotor carries eddy currents only.

## Licence

These boards are output of the Sinusoidal Coil Generator, for non-commercial use only. See [LICENSE.md](LICENSE.md); this branch's GPL-3.0 covers only the scripts here (`new_coil.py`, each board's `simulation.py`, `angle_error.py`, `make_charts.py`, `rig_picture.py` and `angle_setup.py`, and those in `Comparisons/`).
