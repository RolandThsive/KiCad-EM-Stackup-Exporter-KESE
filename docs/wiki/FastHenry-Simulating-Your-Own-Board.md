# 35. FastHenry Simulating Your Own Board

Every example on the `FastHenry_Integration` branch is one folder with its board and a `simulation.py` whose settings
are all in one dictionary, `SETTINGS`, at the top of the file. To simulate a board of your own, copy the example
closest to it and change those settings; this page lists every one.

## 35.1 Start From An Example

| Your board has | Start from |
|---|---|
| One coil, opened by a gap between two trace ends | `Examples/E01_circular_loop/` |
| Two coils, one driven and one sensing (mutual inductance) | `Examples/E02_coaxial_loops/` |
| A coil set from the Sinusoidal Coil Generator: a stator with TX, SIN and COS, and a rotor at several angles | `Examples/Inductive Coils/new_coil.py`, which sets the folder up as `S0d2_1x_OD23_2L_tiny_TX3top_Cut/` is |

```bash
cp -r Examples/E01_circular_loop Examples/MY_BOARD
cd Examples/MY_BOARD
cp ~/my_board.kicad_pcb .               # and set SETTINGS['board'] to its name
../../.venv/bin/python simulation.py --nwinc 3      # a first run, 3 filaments across each track
```

The first run exports the board's stack-up with KESE (see [FastHenry Walkthrough 34.5](FastHenry-Walkthrough.md#345-installing-on-linux-ubuntu-2404) for
KESE) into the folder's `3D_Geometry/`. Every run writes the results file beside the script and its working files
under `case/` (each solve's `model.inp`, `Zc.mat` and FastHenry's log), which is not committed.

## 35.2 The Proof Boards' Settings

| Setting | Example (E01) | What it is |
|---|---|---|
| `board` | `'E01_circular_loop.kicad_pcb'` | The KiCad board, beside the script |
| `radius_mm`, `width_mm`, `gap_mm` | `10.0`, `0.5`, `0.2` | The loop's size, for the references only |
| `ends_mm` | `((109.993873, -100.35), (109.993873, -99.65))` | The two trace ends at the gap, in model coordinates (KiCad's x, −y): the port goes between the nodes nearest them, within 0.01 mm |
| `layers` (E02) | `{'TX': 'F.Cu', 'RX': 'B.Cu'}` | Which layer each coil's ends are on |
| `sigma` | `5.8e7` | Copper's conductivity, S/m |
| `freqs_hz` | `[1e4, 3.5e6]` | One solve per frequency: one low enough that the current is uniform (10 kHz, skin depth 0.66 mm) and the working frequency |
| `ladder` | `[(1, 1), (3, 1), (5, 1), (9, 1), (9, 3), (15, 3)]` | The filament ladder, (across, through) each track; E02 stops at 9 × 3 |
| `rw` | `2.0` | Each edge filament this many times narrower than the next one in |
| `chord_deg` | `5.0` | An arc as chords of at most this many degrees (and 0.5 mm) |
| `options` | `['-s', 'ludecomp', '-m', 'direct', '-a', 'off']` | FastHenry's dense direct solve |

The coil itself is named in `build()`: `C.add_board(m, board, zl, {'LOOP': 'LOOP'}, nwinc=..., nhinc=...)` takes the
nets to model, as `{net: coil name}`, and `m.port(name, a, b)` opens each coil between two nodes, found with
`C.nearest_node(m, net, layer, x, y, within)`. For the other ways to open a coil (two stacked ends, a via left out,
a cut across a trace) see [FastHenry Walkthrough 34.11](FastHenry-Walkthrough.md#3411-open-each-coil-at-its-port).

| Option | What it does |
|---|---|
| `--nwinc 9` | Only 9 filaments across (several values may follow) |
| `--nhinc 3` | Filaments through the copper, with `--nwinc` |
| `--chord-deg 1` | Arcs as chords of at most 1° (E01) |
| `--freqs 1e4` | Only these frequencies |
| `--out DIR` | Working files somewhere else than `case/` |

A rerun of the same rung replaces it in `results.json`; the other rungs are kept.

## 35.3 A Coil Board From The Generator

Any single coil set from the [Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator)
is set up in one command, from the branch's `Examples/Inductive Coils/`:

```bash
python new_coil.py "<checkout>/Generators/Single Coil Set Generator/Output/Coil_..." MY_COIL
```

It makes `MY_COIL/` laid out as `S0d2_1x_OD23_2L_tiny_TX3top_Cut/`: `Boards/` straight from the generator,
`FastHenry Simulation/` with `test_spec.json` and the five scripts (`simulation.py`, `angle_error.py`,
`make_charts.py`, `rig_picture.py`, `angle_setup.py`), which run any board it sets up without a change, `Results/`
with `expected_results.json` (the generator's estimates), and a README. It then builds the filaments at one angle and
prints how many, and the memory and time a solve needs. `--angles 16` gives more angles over the rotor's period, and
`--no-estimate` skips the count. Single coil sets only: a dual board has two sets.

Then check the terminals in the new README against the picture. `new_coil.py` opens the TX at its two stacked ends
and each RX coil at one of its layer-change vias: the one nearest the generator's suggested cut, or, where it found
no cut spot, the one farthest from the TX copper. To open SIN and COS by a cut across a top trace instead, as on
`S0d2_1x_OD23_2L_tiny_TX3top_Cut`, set `"rx_port": "cut"` in `test_spec.json` and give each receiver a `cut`.

## 35.4 The Coil Board's test_spec.json

Everything that belongs to the board is in `test_spec.json`; `simulation.py` reads it. On
`S0d2_1x_OD23_2L_tiny_TX3top_Cut`:

| Entry | Value | What it is |
|---|---|---|
| `files` | `Boards/Stator.kicad_pcb`, `Boards/Rotor.kicad_pcb` | The two boards, from the board folder |
| `coordinates.kicad_axis_xy` | `[100.0, 100.0]` | The rotation axis in KiCad's coordinates |
| `nets` | `{"2": "SIN", "1": "COS", "TX": "TX"}` | The board's nets and the coils they are |
| `air_gap_mm` | `1.0` | Stator F.Cu top face to rotor copper face, copper to copper; `--gap` sets another |
| `terminals.TX` | ends at `[111.0, 100.0]`, `end_radius_mm` 0.1 | The TX's two stacked ends, and how near the two must reach that point |
| `terminals."2".cut` | at `[96.591, 100.4961]`, running `[-0.5975, -0.8019]`, `gap_mm` 0.2, `half_width_mm` 0.2, F.Cu | SIN's cut across its top trace; the via at `via_xy_kicad` stays |
| `terminals."1".cut` | at `[97.2386, 97.9403]`, running `[0.1446, -0.9895]`, the same size | COS's cut |
| `rx_port` | `"cut"` | How SIN and COS are opened: `"cut"` or `"via"` (a via left out) |
| `sets[0].f_Hz` | `3500000.0` | The TX's frequency |
| `sets[0].rotor_period_mech_deg` | `180.0` | The rotor repeats itself after this; the curves are drawn over it |
| `sets[0].sweep_angles_mech_deg` | 0 to 337.5 in steps of 22.5 | The angles solved |

And in `SETTINGS` at the top of `simulation.py`:

| Setting | Value | What it is |
|---|---|---|
| `sigma` | `5.8e7` | Copper, S/m |
| `nwinc` | `3` | Filaments across each track's width |
| `rw` | `2.0` | Each edge filament this much narrower than the next one in |
| `nhinc` | `1` | Filaments through each track's copper |
| `max_arc_deg` | `5.0` | An arc track as chords of at most 5° (and 0.5 mm) |
| `rotor_edge_mm` | `0.05` | The rotor grid's bars at its edges ... |
| `rotor_max_mm` | `0.3` | ... growing to this in its middle |
| `via_plating_mm` | `0.025` | A via is a bar with the copper section of a barrel plated this thick |
| `options` | `['-s', 'ludecomp', '-m', 'direct', '-a', 'off']` | FastHenry's dense direct solve |
| `jobs` | `1` | Solves at once |

![The rotor of S0d2_1x_OD23_2L_tiny_TX3top_Cut turned to 45°, seen from above as FastHenry solves it: the two grey quarter-ring sectors, drawn as their grid of bars, now cover the top and bottom of the stator, over the TX's three dark grey turns and the blue SIN and orange COS coils; a dotted line marks where 0° was; the SIN and COS ports are ringed at their cuts on the left, and the TX port at its stacked ends on the right](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/FastHenry-Simulating-Your-Own-Board/S0d2_1x_OD23_2L_tiny_TX3top_Cut/rotor_045deg.webp)

One of the 16 rotor angles, drawn by `angle_setup.py`; `FastHenry Simulation/RotorStator_AngleSetup/` has all of
them, with the two cuts and the TX port ringed. Check them before a long sweep: a port in the wrong place shows here.

## 35.5 The Coil Board's Command Line

| Option | What it does |
|---|---|
| (none) | The rotor away, then every angle of `test_spec.json`, at the 1 mm gap |
| `--gap 0.5` | Another air gap, copper to copper, mm |
| `--angles 0 90` | Only these angles; `--no-away` skips the run with the rotor away |
| `--step 10` | Every 10° over the whole turn |
| `--jobs 3` | Three solves at once, one core each |
| `--nwinc 5`, `--nhinc 2` | More filaments across or through each track: a trial, give it `--trial NAME`, and its results stay in `case/` |
| `--rotor-edge`, `--rotor-max` | The rotor grid's bars at its edges and in its middle, mm |
| `--model-only` | Builds the filaments and says how many; solves nothing |
| `--plot` | Only redraws the table, the curves and `SINCOS_Results.md` |
| `--merge a.json b.json` | Adds the solves of the same gap from other machines' results files |
| `--out DIR` | The runs somewhere else than `case/` |

An angle already in the results is skipped, so a stopped sweep picks up where it was. `python angle_error.py` prints
the angle error at each angle, `python make_charts.py` redraws every chart, `python rig_picture.py` redraws how the
boards sit in FastHenry, and `python angle_setup.py` redraws the rotor at each angle.

## 35.6 Before A Large Board

Check the memory first: build the model alone with `--model-only`, read
its filaments, and square them. The dense direct solve holds every filament's coupling to every other, so a board
with twice the filaments needs four times the memory and eight times the time. If it does not fit, make the coil smaller or
the rotor's grid coarser (`--rotor-edge`, `--rotor-max`), as the branch's coil workflow says.

For scale, on the 4-core, 15 GB test machine: the coil board's 9,264 filaments took 1.1 GB and 2.9 to 5.9 min a
solve on one core, its 4,722 with the rotor away 0.46 GB and 36 s, and E02's 6,804 filaments (9 × 3) 1.10 GB and
5.2 min. `new_coil.py` estimates a coil board as about 0.0158 GB × (filaments / 1000)² and 0.0051 min ×
(filaments / 1000)³ on one core, fitted to the coil boards' solves (6,555 to 9,306 filaments); the proof boards' runs
with 3 filaments through the copper took more than that, so check any other board with `--model-only` and one solve
first.

| Previous | Next |
|:---|---:|
| [FastHenry Walkthrough](FastHenry-Walkthrough.md) | [FastHenry Test Boards And Results](FastHenry-Test-Boards-And-Results.md) |
