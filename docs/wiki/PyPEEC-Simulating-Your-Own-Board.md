# 46. PyPEEC Simulating Your Own Board

Every example on the `PyPEEC_Integration` branch is one folder with its board and a `simulation.py`.
The proof boards keep all their settings in one dictionary, `SETTINGS`, at the top of the script; the
coil board keeps every fact about the board in a `test_spec.json` beside its script, so the same script
runs any coil set the Sinusoidal Coil Generator makes. To simulate a board of your own, copy the example
closest to it; this page lists every setting.

## 46.1 Start From An Example

| Your board has | Start from |
|---|---|
| One coil, opened by a gap between two trace ends | `Examples/E01_circular_loop/` |
| Two coils, one driven and one sensing (mutual inductance) | `Examples/E02_coaxial_loops/` |
| An inductive encoder from the Sinusoidal Coil Generator: a stator with TX, SIN and COS, and a rotor at many angles | `Examples/Inductive Coils/S0d2_1x_OD23_2L_tiny_TX3top_Cut/`, set up for a new board by `Examples/Inductive Coils/new_coil.py` ([46.5](#465-a-new-coil-board-in-one-command)) |

```bash
cp -r Examples/E01_circular_loop Examples/MY_BOARD
cd Examples/MY_BOARD
cp ~/my_board.kicad_pcb .                       # and set SETTINGS['board'] to its name
../../.venv/bin/python simulation.py --voxels-only --voxels 0.05     # draw the voxels, solve nothing
../../.venv/bin/python simulation.py --voxels 0.1                    # a first, coarse run
```

E01 and E02 write `results.json` beside the script and their working files under `case/` (KESE's
export, PyPEEC's inputs and logs), which git ignores.

## 46.2 The Proof Boards' Settings

`SETTINGS` in E01's `simulation.py` (E02's is the same, with two coils):

| Setting | Example (E01) | What it is |
|---|---|---|
| `board` | `'E01_circular_loop.kicad_pcb'` | The KiCad board, beside the script |
| `centre` | `(100.0, -100.0)` | The loop's centre in model coordinates: KiCad's (x, y) becomes (x, −y) |
| `radius_mm`, `width_mm`, `gap_mm`, `copper_mm` | `10.0`, `0.5`, `0.2`, `0.035` | The loop's size, used by the references and by the grid's dz |
| `gap_box` | `(109.75, -100.35, 110.25, -99.65)` | A rectangle (x0, y0, x1, y1, model coordinates) that holds the coil's gap; the gap is this box less the coil's copper |
| `sigma` | `5.8e7` | Copper's conductivity, S/m |
| `freqs_hz` | `[1e4, 3.5e6]` | One solve per frequency: one low enough that the current is uniform (10 kHz, skin depth 0.66 mm) and the working frequency |
| `voxels_mm` | `[0.1, 0.05, 0.025, 0.0125]` | The voxel ladder: the voxels' size in the board's plane, one run each |
| `n_cu` | `1` | Voxel layers through the copper (dz = 35 µm / `n_cu`) |
| `threads` | `4` | Threads for PyPEEC's numerics |

The coil itself is named in `build()`: `C.Coil(name, body, t1, t2, current)`, where `body` is the
coil's copper (KESE's net name), `t1` and `t2` its two terminals from
`P.terminals(grid, vox, body, gap, z0, z1)` with the copper's height, and `current` 1.0 for a driven
coil or 0.0 for a sensing one.

| Option | What it does |
|---|---|
| `--voxels 0.05` | Only these voxel sizes |
| `--freqs 1e4` | Only these frequencies |
| `--n-cu 2` | Two voxel layers through the copper |
| `--results FILE` | Results somewhere else than `results.json` |
| `--out DIR` | Working files somewhere else than `case/` |
| `--voxels-only` | Draw the voxels and print how many, solve nothing |

A rerun of the same voxel size adds to `results.json`: a solve at a frequency already there is
replaced, the others are kept.

## 46.3 The Coil Board's `test_spec.json`

Every board fact `simulation.py` needs, with paths from the board folder:

| Key | On S0d2_1x_OD23_2L_tiny_TX3top_Cut | What it is |
|---|---|---|
| `files` | `Boards/Stator.kicad_pcb`, `Boards/Rotor.kicad_pcb`, `Boards/Parameters.txt`, `Results/expected_results.json` | The two boards, the generator's parameters, and its estimates |
| `coordinates` | axis at KiCad (100, 100); z up from the stator, F.Cu top face at z = 0, B.Cu at z = −0.8 | Where the model's origin is |
| `stator` | F.Cu and B.Cu, board 0.8 mm, copper 35 µm, bore and outer radius 2 and 11.7 mm, RX band 3.2 to 6.1 mm, TX ring 7.2 to 8.4 mm | The stator's stack and rings |
| `rotor` | one ring, r 2.52 to 9.0 mm, 2 sectors, duty 0.5; copper side towards the stator, not mirrored | The rotor and how it is placed |
| `air_gap_mm` | `1.0` | The default air gap, copper to copper (`--gap` sets another) |
| `nets` | `"2"` SIN, `"1"` COS, `"TX"` TX | KESE's net names for each coil |
| `terminals` | TX: its two ends stacked at (111, 100), end radius 0.1 mm. SIN and COS: `"RX trace cut"`, each with its `cut` (`xy_kicad`, `along_kicad`, `gap_mm` 0.2, `half_width_mm` 0.2, `layer` F.Cu) | Where each coil is opened |
| `rx_port` | `"cut"` | How SIN and COS are opened: `"cut"` (a cut across a top trace) or `"via"` (a via left out) |
| `sets` | TX `TX`, SIN `2`, COS `1`, 3.5 MHz, 2 loops, electrical and rotor period 180°, 16 angles every 22.5° from 0 to 337.5° | The coil set, its frequency and the sweep |
| `voxel_mm` | `0.05` | The voxels' size in the board's plane |

The script's own `SETTINGS` takes these and adds `sigma` 5.8e7, `insulators` False, `n_cu` 1,
`threads` 4 and `tolerance` {} (changes to `bridge/tolerance.yaml`, none by default).

## 46.4 The Coil Board's Command Line

Run from the board's `PyPEEC Simulation/` folder:

| Command | What it does |
|---|---|
| `python simulation.py` | The rotor away, then every angle of `test_spec.json`, at the default 1 mm gap |
| `--gap 0.5` | Another air gap, copper to copper (mm) |
| `--angles 0 90` | Only these rotor angles |
| `--step 10` | Every 10 degrees over the whole turn |
| `--no-away` | Skip the run with the rotor away |
| `--voxel 0.035` | Voxels of another size in the plane: a trial, kept in `case/` |
| `--n-cu 2` | Voxel layers through each copper sheet |
| `--threads 8` | Threads for PyPEEC |
| `--trial NAME` | A name for a trial setting: its results stay in `case/` |
| `--voxels-only` | Draw the voxels and say how many, solve nothing (with `--angles 0`, to judge the memory) |
| `--plot` | Only redraw the table, the curves and `SINCOS_Results.md` |
| `--merge a.json b.json` | Add the solves in results files from other machines, each of which ran some angles of this gap, and redraw |

An angle already in the gap's results file is skipped, so a stopped sweep picks up where it was.
`SINCOS_Results.md` is rewritten after every solve. Beside `simulation.py`: `angle_error.py` prints the
angle error at each angle, `make_charts.py` redraws every chart (WebP), `rig_picture.py` draws how the
boards sit in PyPEEC voxel by voxel, and `angle_setup.py` draws the rotor at each angle into
`RotorStator_AngleSetup/`.

![The coil board at a rotor angle of 45°, as PyPEEC solves it, seen from above: the stator's three grey TX turns, SIN in blue and COS in orange on F.Cu and B.Cu with their vias as rings, the rotor's two copper sectors in grey face down over them, turned 45° from the dotted 0° line; the SIN and COS ports are circled at their cuts and the TX port at its stacked ends on the right](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/PyPEEC-Simulating-Your-Own-Board/S0d2_1x_OD23_2L_tiny_TX3top_Cut/rotor_045deg.webp)

`angle_setup.py`'s picture at 45°, one of the 16 in `RotorStator_AngleSetup/`: a quick check that the
rotor turns the right way and the ports sit where they should, before any solve.

## 46.5 A New Coil Board In One Command

`Examples/Inductive Coils/new_coil.py` turns the generator's output folder into a board folder laid
out as S0d2's, whose scripts run it as they are, since they read every board fact from
`test_spec.json`:

```bash
cd "Examples/Inductive Coils"
python new_coil.py "<checkout>/Generators/Single Coil Set Generator/Output/Coil_..." MY_COIL
python new_coil.py <folder> MY_COIL --angles 16 --voxel 0.035 --no-estimate
```

| Step | What to do |
|---|---|
| 1. Make the coil | Set the generator's parameters and run it; read its warnings (a via too close to other copper means the board is not right yet; the TX tank warning does not matter to the simulation) |
| 2. Set it up | `new_coil.py` makes `Boards/` (straight from the generator), `PyPEEC Simulation/` (with `test_spec.json` and the scripts), `Results/` (with `expected_results.json`) and a README. With KESE in place it exports the two boards into `3D_Geometry/`, draws the voxels at one angle and prints the grid's size and the memory and time a solve needs (`--no-estimate` skips this) |
| 3. Check it | Check the estimate ([PyPEEC Hardware](PyPEEC-Hardware.md)), then the terminals in the new README against `python rig_picture.py`. `new_coil.py` opens the TX at its stacked ends and each RX at a layer-change via; to open SIN and COS by a cut, as on S0d2, set `"rx_port": "cut"` and give each receiver a `cut` in `test_spec.json` |
| 4. Run it | `python simulation.py` in `PyPEEC Simulation/`, then other gaps with `--gap` |
| 5. Read the results | `Results/<gap>_AirGap/` and `Results/SINCOS_Results.md` ([PyPEEC Test Board Results](PyPEEC-Test-Board-Results.md)); commit the folder without `case/` |

The limits: single coil sets only, since a `DualCoil_` board has two sets.

## 46.6 Before A Large Board

Check the size first: `--voxels-only` draws the voxels and prints the grid's size. The memory and the
time follow the whole grid, copper or not, at about 0.31 GB and 0.9 minute a million voxels on 4 cores
([PyPEEC Hardware](PyPEEC-Hardware.md#505-estimating-a-board)). The grid is uniform, so its height
runs from the lowest copper to the highest, and a wider air gap makes it taller.

| Previous | Next |
|:---|---:|
| [PyPEEC Workflow](PyPEEC-Workflow.md) | [PyPEEC Test Boards](PyPEEC-Test-Boards.md) |
