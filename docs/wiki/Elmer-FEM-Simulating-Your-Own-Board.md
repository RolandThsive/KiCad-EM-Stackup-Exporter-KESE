# 25. Elmer FEM Simulating Your Own Board

Every example on the `Elmer_Integration` branch is one folder with its board and a `simulation.py`
whose settings are all in one dictionary, `SETTINGS`, at the top of the file. To simulate a board of
your own, copy the example closest to it and change those settings; this page lists every one.

## 25.1 Start From An Example

| Your board has | Start from |
|---|---|
| One coil, opened by a gap between two trace ends | `Examples/E01_circular_loop/` |
| Two coils, one driven and one sensing (mutual inductance) | `Examples/E02_coaxial_loops/` |
| A coil set from the Sinusoidal Coil Generator: a stator with a TX, SIN and COS, and a rotor turned to a series of angles | `Examples/Inductive Coils/new_coil.py`, which sets the board up as a folder like `S0d2_1x_OD23_2L_tiny_TX3top_Cut/` ([27.8](#258-a-coil-set-from-the-generator)) |

```bash
cp -r Examples/E01_circular_loop Examples/MY_BOARD
cd Examples/MY_BOARD
cp ~/my_board.kicad_pcb .          # and set SETTINGS['board'] to its name
../../.venv/bin/python simulation.py --levels 0.75 --freqs 1e4      # a first, coarse run
```

Every run writes `results.json` beside the script and its working files under `case/` (the KESE
export, the mesh, the `.sif` files, Elmer's logs), which is not committed.

## 25.2 The Board And Its Coils

| Setting | Example (E01) | What it is |
|---|---|---|
| `board` | `'E01_circular_loop.kicad_pcb'` | The KiCad board, beside the script |
| `centre` | `(100.0, -100.0)` | The centre of the air domain in model coordinates: KiCad's (x, y) becomes (x, −y) |
| `gap_box` | `(109.75, -100.35, 110.25, -99.65)` | A rectangle (x0, y0, x1, y1, model coordinates) that holds the coil's gap; the gap is this box less the coil's copper |
| `sigma` | `5.8e7` | Copper's conductivity, S/m |
| `insulators` (E02) | `False` | `False` leaves FR-4 and mask out (air to this solve); `True` meshes them, which only adds layers |

The coil itself is named in `main()`: `E.Coil(name, body, t_low, t_high, sheet, current)`, where
`body` is the mesh body of the coil's copper (KESE's net name, or the name given in `body_of`),
`t_low` and `t_high` the two electrode boundaries, `sheet` the port sheet, and `current` 1.0 for a
driven coil or 0.0 for a sensing one. The electrodes and the sheet are found in `build()`:

| Coil opened at | Electrodes | Sheet |
|---|---|---|
| A gap between two trace ends on one layer | `P.electrodes(m, body, gap, z_bottom, z_top)` with the copper's height | `P.sheet_at_level(m, gap, z)` at a level of the copper |
| Two ends stacked on two layers (the coil board's TX) | `P.electrodes` with the dielectric's height and a small disc round the ends as the gap | `P.sheet_vertical(m, line, z0, z1)` along a line drawn into the mesh (`extra_lines`) |
| A cut across a top trace (the coil board's SIN and COS) | a `void` part (air of priority 4) that takes the copper inside the cut's box out of the top copper; then `P.electrodes` on the box with the top copper's height | `P.sheet_at_level(m, box, z)` at the copper's lower face, with the box's outline drawn into the mesh |

## 25.3 The Domain And The Frequencies

| Setting | Example | What it is |
|---|---|---|
| `domain_radius_mm` | `60.0` | Radius of the air disc. At 6 coil radii the outer boundary (n × A = 0) holds L down by about 0.3 %: twice as big, E01's L rose 0.26 %. The coil board uses 3 board radii, 35.1 mm, and the same margin above the rotor and below the stator |
| `domain_half_height_mm` | `60.0` | The air reaches this far above and below z = 0 |
| `freqs_hz` | `[1e4, 3.5e6]` | One solve per frequency. Choose one low enough that the current is uniform (here 10 kHz, skin depth 0.66 mm) and the working frequency. The coil board solves at its TX's 3.5 MHz only |
| `order` | `1` | Edge element order. `--order 2` uses second-order (quadratic) elements, with several times the unknowns and the memory |
| `levels` | `[0.75, 1.0, 1.3]` | The mesh ladder: each level divides `h_edge`, `h_in` and `dz_copper` by itself; the air's sizes and grading stay as they are. A run of two or three levels shows how far the answer still moves with the copper's mesh, not with the air's: check the air with `grade` and `tet_grade` halved as well |

## 25.4 The Mesh

These go to `mesh25d.Settings` (in `SETTINGS['mesh']`):

| Setting | Example | What it is |
|---|---|---|
| `h_edge` | `0.09` | Element size at copper edges, mm. At least three elements across the narrowest trace is a good start |
| `h_in` | `0.18` | Largest element inside copper, mm |
| `h_max` | `6.0` | Largest triangle anywhere, mm (the far field) |
| `grade` | `0.5` | How fast the size grows away from copper, mm per mm. Halved to 0.25 (with `tet_grade` 0.35), E01's L rose 2.3 % with half again the nodes; quartered, another 1.1 % with 2.8 times the nodes ([Elmer FEM Accuracy](Elmer-FEM-Accuracy.md#271-the-error-budget-on-e01)) |
| `dz_copper` | `0.018` | Thickest wedge layer in a copper foil, mm. Half the skin depth or less at the highest frequency (copper: 35 µm at 3.5 MHz) |
| `dz_max` | `0.4` | Thickest wedge layer elsewhere (through the board, in an air gap), mm |
| `tet_max` | `8.0` | Largest tetrahedron in the air above and below, mm |
| `tet_grade` | `0.7` | How fast the tetrahedra grow with height, mm per mm |
| `foil_max` (default) | `0.15` | The thickest slab still treated as a copper foil; thicker slabs with copper (via barrels) get `dz_max` |
| `pads` (default) | `(0.03, 0.08)` | The two air layers of wedges just above and below the boards, mm |

## 25.5 The Linear Solver

| Setting | E01 | Coil board | What it is |
|---|---|---|---|
| `solver` | `'iterative'` (the default) | `'mumps'` | The A-V solve: iterative, or a direct solve with serial MUMPS. MUMPS is exact, but needs far more memory ([Elmer FEM Simulating Your Own Board](#257-before-a-large-board)) |
| `method` | BiCGStab(l) | `'GCR'` | The Krylov method of an iterative solve. The coil board's script notes that GCR(50) falls slowly but steadily there while BiCGStab(l) wanders |
| `ilu_order`, `ilu_factor` | none | `1`, `0.1` | An ILU of the field's block under the circuit preconditioner, the matrix factored with its diagonal times 1.1: the air's curl-curl block is singular, and an unshifted ILU of it breaks down on tiny pivots |
| `threads` | `4` | `4` | OpenMP threads for ElmerSolver |
| `tol` | `1e-7` | `1e-7` | The iterative solver's relative residual to stop at |
| `max_iter` | `3000` | `1500` | The iteration cap. On E01 at 10 kHz the residual stalls near 10⁻⁶ (see [Elmer FEM Troubleshooting](Elmer-FEM-Troubleshooting.md)); the run then stops at the cap and goes on, which is why the cap matters. `--max-iter` changes it for one run |

The last four matter only to an iterative solve; a direct solve ignores them.

## 25.6 The Command Line

| Option | What it does |
|---|---|
| `--levels 1 1.3` | Only these mesh levels |
| `--freqs 1e4` | Only these frequencies |
| `--order 2` | Second-order elements, written to `results_order2.json` |
| `--max-iter 1500` | Another iteration cap |
| `--out DIR` | Working files somewhere else than `case/` |
| `--results FILE` | Results somewhere else than `results.json` |

E01's script has four more, for studies of the model itself; copy them into a script of your own when
you need them:

| Option | What it does |
|---|---|
| `--mesh KEY=VALUE` | Changes one setting of `SETTINGS['mesh']` for this run, such as `--mesh grade=0.25`; repeat it for more. Give the run its own `--results` and `--out` |
| `--domain-mm R` | The air domain's radius and half height, mm |
| `--fields` | Also writes the fields as VTU files, for pictures (large) |
| `--mesh-only` | Builds the meshes and prints their size, and solves nothing |

A rerun of the same level adds to `results.json`: a solve at a frequency already there is replaced,
the others are kept.

## 25.7 Before A Large Board

Check the memory first: build the mesh alone (`--mesh-only` in the E01 script and the coil board's),
read its node count from the log, and multiply by the memory per node measured for the solver you
will use. A run that does not fit is better held for a larger machine than run on a coarser mesh whose
error is unknown.

| Solve | Measured | Memory |
|---|---|---|
| Iterative, BiCGStab(l) (E01 and E02, 4 cores, 15 GB) | nine meshes from 59,782 to 166,471 nodes, at both frequencies | 59 to 61 kB per node (E01 at level 1: 4.86 GB), whatever the frequency or the iterations |
| Iterative, GCR (the coil board) | | about 57 kB per node, but too slow on the coil board at 3.5 MHz to read M |
| Direct, MUMPS (the coil board at level 0.25, 16 GB machines) | 118,416 to 161,126 nodes | more than 13 GB a solve: each held 13.3 GB in memory and put the rest in swap; 8 GB of swap was enough at a 0.1 mm gap, from 0.5 mm on about 24 GB, 40 GB of memory and swap together. `new_coil.py` estimates roughly 200 kB a node |

On Linux a swap file makes up the difference
([Elmer FEM Walkthrough](Elmer-FEM-Walkthrough.md#245-linux-ubuntu-2404)). Meshing takes seconds;
an iterative solve on E01 took about 4 µs per node and iteration with the machine to itself, and a
direct solve on the coil board 3 to 15 minutes. Every coil board angle is one solve, so a gap of 16
angles took one to two and a half hours.

## 25.8 A Coil Set From The Generator

`Examples/Inductive Coils/new_coil.py` turns one output folder of the
[Sinusoidal Coil Generator](https://github.com/RolandThsive/Sinusoidal-Inductive-Encoders-Coil-Generator)
into a board folder that its scripts run as they are:

```bash
cd "Examples/Inductive Coils"
python new_coil.py <generator output folder> <name>            # --angles 16, --level 1.0, --no-estimate
cd "<name>/Elmer Simulation"
python simulation.py                   # the rotor away, then every angle in test_spec.json
```

Everything that belongs to the board is in `Elmer Simulation/test_spec.json`, which `new_coil.py`
reads from the generator's `Parameters.txt` and `Stator.kicad_pcb`; `simulation.py` itself is the
same for every single-set board. Unless `--no-estimate` is given, it builds the mesh at one angle and
prints the memory a direct solve needs. Single-set boards only: a dual board has two coil sets.

| `test_spec.json` key | Coil board | What it is |
|---|---|---|
| `nets` | `"2": "SIN"`, `"1": "COS"`, `"TX": "TX"` | KESE's copper part per net, and the coil it is |
| `air_gap_mm` | `1.0` | Stator F.Cu top face to rotor copper face; `--gap` sets another |
| `air_box.radius_or_half_width_mm` | `35.1` | 3 × the board's radius |
| `terminals.TX.ends_xy_kicad` | `[111.0, 100.0]` | Where the TX's two ends sit stacked |
| `terminals.<net>.cut` | `xy_kicad`, `along_kicad`, `gap_mm` 0.2, `half_width_mm` 0.2, `layer` F.Cu | Where each receiver's top trace is cut, which way the trace runs, and the cut's size |
| `rx_port` | `"cut"` | `"cut"` opens SIN and COS by the cuts; `"via"` by leaving one layer-change via out |
| `sets[0].f_Hz` | `3.5e6` | The TX's frequency |
| `sets[0].sweep_angles_mech_deg` | 0 to 337.5 every 22.5 | The rotor angles, one solve each |
| `sets[0].rotor_period_mech_deg` | `180.0` | The rotor repeats itself after this |
| `mesh_level` | `0.25` | The copper's mesh sizes divided by this |

| Coil board option | What it does |
|---|---|
| `--gap 0.5` | Another air gap |
| `--angles 0 90`, `--step 10` | Only these angles, or every 10° over the whole turn |
| `--no-away` | Skips the solve with the rotor away |
| `--level 0.4` | A finer mesh, at more memory |
| `--solver iterative` | GCR instead of MUMPS: far less memory, but on this board at 3.5 MHz it converges too slowly to read M |
| `--mesh-only` | Builds the meshes and solves nothing |
| `--merge a.json b.json` | Adds solves made on other machines (each some angles of this gap) to this gap's results |
| `--plot` | Only redraws the table, the curves and `Results/SINCOS_Results.md` |

The results go into `Results/<gap>_AirGap/` (`1mm_AirGap`, `0d5mm_AirGap`, the point written as d):
`results_gap<gap>mm.json`, a `.csv` and the chart, and `Results/SINCOS_Results.md` is rewritten after
every solve. `make_charts.py`, `angle_error.py`, `rig_picture.py` and `angle_setup.py` redraw the
charts, the angle error, the set-up picture and the rotor at each angle.

| Previous | Next |
|:---|---:|
| [Elmer FEM Walkthrough](Elmer-FEM-Walkthrough.md) | [Elmer FEM Test Boards And Results](Elmer-FEM-Test-Boards-And-Results.md) |
