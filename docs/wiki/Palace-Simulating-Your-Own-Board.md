# 25.4 Palace Simulating Your Own Board

Every example on the `Palace_Integration` branch is one folder with its board and a `simulation.py` whose settings
are all in one dictionary, `SETTINGS`, at the top of the file. A coil board from the Sinusoidal Coil Generator is set
up by one command, and its scripts read every board fact from a `test_spec.json`. This page lists every setting.

## 25.4.1 Start From An Example

| Your board has | Start from |
|---|---|
| One coil, opened by a gap between two trace ends | `Examples/E01_circular_loop/` |
| Two coils, both driven in turn (the whole impedance matrix, M both ways) | `Examples/E02_coaxial_loops/` |
| A generator coil set: a stator with TX, SIN and COS and a rotor at several angles and air gaps | `Examples/Inductive Coils/S0d2_1x_OD23_2L_tiny_TX3top_Cut/`, or a new folder made by `new_coil.py` (40.5) |

```bash
cp -r Examples/E01_circular_loop Examples/MY_BOARD
cd Examples/MY_BOARD
cp ~/my_board.kicad_pcb .                     # and set SETTINGS['board'] to its name
../../.venv/bin/python simulation.py --mesh-only --levels 0.25    # the mesh's size first
../../.venv/bin/python simulation.py --levels 0.25 --freqs 3.5e6  # one coarse solve
```

The first run writes KESE's export into `3D_Geometry/` (KESE is needed for that run; see
[Palace Walkthrough](Palace-Walkthrough.md#2446-linux-ubuntu-2404)); later runs reuse it while the board file is unchanged. The runs' working
files (the mesh, `config.json`, Palace's log and output) go under `case/`, which git ignores.

## 25.4.2 The Proof Boards' Settings

| Setting | E01 | What it is |
|---|---|---|
| `board` | `'E01_circular_loop.kicad_pcb'` | The KiCad board, beside the script |
| `centre` | `(100.0, -100.0)` | The loop's centre in model coordinates: KiCad's (x, y) becomes (x, −y) |
| `radius_mm`, `width_mm`, `gap_mm` | `10.0`, `0.5`, `0.2` | The trace, for the references only |
| `gap_box` | `(109.75, -100.35, 110.25, -99.65)` | A rectangle (x0, y0, x1, y1, model coordinates) that holds the gap; the port's line is found inside it |
| `port_direction` | `'+Y'` | Across the gap, from one round end to the other |
| `port_ohm` (E02) | `50.0` | Each port's resistance; E02 drives both ports in turn |
| `sigma` | `5.8e7` | Copper's conductivity, S/m |
| `domain_radius_mm`, `domain_half_height_mm` | `60.0`, `60.0` | The air cylinder (6 loop radii); its outside is a perfect conductor |
| `freqs_hz` | `[1e4, 3.5e6]` | One solve per frequency: uniform current (10 kHz, skin depth 0.66 mm) and the coil boards' frequency |
| `order` | `1` | Nédélec element order |
| `levels` | `[0.25, 0.5, 0.75, 1.0]` | The mesh ladder: each level divides `h_edge`, `h_in` and `dz_copper` by itself |
| `mesh` | `h_edge=0.09, h_in=0.18, h_max=6.0, grade=0.5, dz_copper=0.018, dz_max=0.4, tet_max=8.0, tet_grade=0.7` | The mesh (40.4) |
| `ranks` | `4` | MPI ranks |
| `solvers['ams']` | `Type='AMS', KSPType='GMRES', Tol=1e-10, MaxIts=3000, MaxSize=300, AMSSingularOperator=True` | The linear solver. `AMSSingularOperator` is needed at 10 kHz ([Palace Troubleshooting](Palace-Troubleshooting.md)) |

E01's command line: `--levels`, `--freqs`, `--ranks`, `--solver`, `--mesh-only` (build the meshes, solve nothing),
`--mesh KEY=VALUE` (one mesh setting for this run, such as `--mesh grade=0.125`), `--domain-mm R` (the domain's radius
and half height), `--results FILE` and `--out DIR`. E02 has the same but `--domain-mm`, and `--restart N`
(GMRES restarts every N iterations instead of 300, with fewer vectors and less memory).

## 25.4.3 The Coil Board's Settings

The coil board's `SETTINGS` take every board fact from `test_spec.json` beside the script; for
`S0d2_1x_OD23_2L_tiny_TX3top_Cut`:

| `test_spec.json` | Value | What it is |
|---|---|---|
| `files` | `Boards/Stator.kicad_pcb`, `Boards/Rotor.kicad_pcb` | The two boards, from the board folder |
| `nets` | `"2": "SIN"`, `"1": "COS"`, `"TX": "TX"` | KESE's copper part per net, and the coil it is |
| `sets[0].f_Hz` | `3500000.0` | The TX's frequency |
| `sets[0].sweep_angles_mech_deg` | 0 to 337.5 in 22.5° steps | The rotor angles of a sweep |
| `sets[0].rotor_period_mech_deg` | `180.0` | The rotor repeats itself after this |
| `air_gap_mm` | `1.0` | Stator F.Cu top face to rotor copper face |
| `air_box.radius_or_half_width_mm` | `35.1` | 3 × the board's radius: the domain's radius and the air above the rotor and below the stator |
| `terminals.TX` | ends at (111, 100), `end_radius_mm` 0.1 | Where the TX's two stacked ends are |
| `terminals."2"`, `terminals."1"` | each a `cut`: `xy_kicad`, `along_kicad`, `gap_mm` 0.2, `half_width_mm` 0.2, `layer` F.Cu | Where SIN and COS are cut; `via_xy_kicad` names the via that stays |
| `rx_port` | `"cut"` | How SIN and COS are opened: `"cut"` or `"via"` (a via left out) |
| `mesh_level` | `0.25` | Divides the copper's mesh sizes |

What `simulation.py` adds itself:

| Setting | Value | What it is |
|---|---|---|
| `insulators` | `False` | FR-4 and mask are air |
| `mesh` | `h_edge=0.1, h_in=0.2, h_max=6.0, grade=0.125, dz_copper=0.018, dz_max=0.2, tet_max=8.0, tet_grade=0.175` | The air graded four times as finely as the bridge's default and wedge layers half as thick ([Palace Accuracy](Palace-Accuracy.md)) |
| `sheet_half_mm` | 0.08 | Half the TX port's width (0.16 mm) |
| `tx_ohm` | `50.0` | The TX port's resistance; the receivers' are 1 MΩ |
| `solvers['ams']` | `GMRES` with `AMS`, `Tol=1e-8`, `MaxIts=2000`, `MaxSize=300` | `ams_1e-10` and `ams_1e-6` are the trials the tolerance was chosen by |
| `reciprocity` | `'first'` | SIN and COS driven too at the first angle of each gap (three solves in one) |
| `ranks`, `jobs` | `2`, `1` | MPI ranks per solve and solves at once (the committed results ran on 4 ranks) |

![The rotor of S0d2_1x_OD23_2L_tiny_TX3top_Cut at 45°, seen from above as Palace meshes it: its two grey quarter-ring sectors turned 45° from the 0° mark over the stator's TX turns in dark grey and SIN and COS in blue and orange, with the SIN and COS cut ports and the TX port ringed](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Palace-Simulating-Your-Own-Board/S0d2_1x_OD23_2L_tiny_TX3top_Cut/rotor_045deg.webp)

`python angle_setup.py` draws the rotor over the stator at every angle of the sweep, as above, to check the
placement and the ports before solving.

## 25.4.4 The Mesh

These go to `mesh25d.Settings` (in `SETTINGS['mesh']`):

| Setting | Bridge default | What it is |
|---|---|---|
| `h_edge` | `0.03` | Element size at copper edges, mm (divided by the level) |
| `h_in` | `0.10` | Largest element inside copper, mm (divided by the level) |
| `h_max` | `4.0` | Largest triangle anywhere, mm |
| `grade` | `0.3` | How fast the triangles grow away from copper, mm per mm |
| `box_margin` | `2.0` | mm round the copper where the size raster is kept |
| `grid`, `simplify` | `0.0005` | The plane's snap grid, and how far copper outlines are simplified, mm |
| `dz_copper` | `0.012` | Thickest wedge layer in a slab with copper, mm (divided by the level) |
| `dz_max` | `0.25` | Thickest wedge layer elsewhere, mm |
| `foil_max` | `0.15` | The thickest slab still treated as a copper foil |
| `pads` | `(0.03, 0.08)` | The air layers of wedges above and below the boards, mm |
| `tet_max` | `8.0` | Largest tetrahedron, mm |
| `tet_grade` | `0.7` | How fast the tetrahedra grow with height, mm per mm |

## 25.4.5 A New Coil Board

Any single coil set from the generator's Single Coil Set Generator is set up the same way:

1. **Make the coil** with the generator, and read its warnings.
2. **Set it up for Palace**, in `Examples/Inductive Coils/`:

   ```bash
   python new_coil.py "<checkout>/Generators/Single Coil Set Generator/Output/Coil_..." my_board
   ```

   It makes `my_board/` with `Boards/` (straight from the generator), `Palace Simulation/` (`test_spec.json` and
   the five scripts, unchanged), `Results/` (`expected_results.json`, the generator's estimates) and a README, then
   builds the mesh at one angle and prints its size and the memory a solve needs. `--angles N` sets the angles over
   one rotor period (default 8), `--level` the mesh level, `--no-estimate` skips the mesh, `--force` writes into a
   folder that exists.
3. **Check it**: the memory (a solve needs about 33 kB per mesh node with the TX driven alone and 44 kB where the
   three coils are driven in turn, on 2 MPI ranks or 4 alike) and the terminals in the new README against the
   picture. `new_coil.py` opens the TX at its stacked ends and each RX at a layer-change via; to open them by a cut, as
   `S0d2_1x_OD23_2L_tiny_TX3top_Cut` is, set `"rx_port": "cut"` and give each receiver a `cut` in `test_spec.json`.
4. **Run it**: `python simulation.py` in `Palace Simulation/`.
5. **Read the results** in `Results/`.

Single coil sets only: a `DualCoil_` board has two sets.

## 25.4.6 The Coil Board's Command Line

| Option | What it does |
|---|---|
| `--gap 0.5` | Another air gap, copper to copper, mm |
| `--angles 0 90`, `--step 10` | These angles only, or every 10° over the whole turn |
| `--no-away` | Skip the solve with the rotor away |
| `--level 0.4` | A finer copper mesh (a trial, kept in `case/`) |
| `--mesh grade=0.25` | One mesh setting changed (a trial, kept in `case/`) |
| `--solver ams_1e-10` | Another linear solver setting, by name |
| `--reciprocity first\|all\|none` | Where SIN and COS are driven too |
| `--ranks 2`, `--jobs 2` | MPI ranks per solve, and solves at once |
| `--port-segment L` | Each port line drawn into the mesh in pieces at most L mm long |
| `--trial NAME` | A name for a trial setting; its results stay in `case/` |
| `--mesh-only` | Build the meshes and say their size, solve nothing |
| `--plot` | Only redraw the table, the curves and `SINCOS_Results.md` |
| `--merge a.json b.json` | Add other machines' solves of the same gap |
| `--out DIR` | Working files somewhere else than `case/` |

An angle already in the results is skipped, so a stopped sweep picks up where it was. `angle_error.py`,
`make_charts.py`, `rig_picture.py` and `angle_setup.py` redraw the angle error, the charts, the set-up picture and
the rotor at each angle.

| Previous | Next |
|:---|---:|
| [FastHenry Simulating Your Own Board](FastHenry-Simulating-Your-Own-Board.md) | [Test Boards And Results](Test-Boards-And-Results.md) |
