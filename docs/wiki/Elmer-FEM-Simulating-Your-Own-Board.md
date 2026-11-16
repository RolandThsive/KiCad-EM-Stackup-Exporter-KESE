# 27. Elmer FEM Simulating Your Own Board

Every example on the `Elmer_Integration` branch is one folder with its board and a `simulation.py`
whose settings are all in one dictionary, `SETTINGS`, at the top of the file. To simulate a board of
your own, copy the example closest to it and change those settings; this page lists every one.

## 27.1 Start From An Example

| Your board has | Start from |
|---|---|
| One coil, opened by a gap between two trace ends | `Examples/E01_circular_loop/` |
| Two coils, one driven and one sensing (mutual inductance) | `Examples/E02_coaxial_loops/` |
| A stator with TX and RX coils and a rotor at several angles, coils opened at stacked ends or at a via left out | `Examples/Inductive Coils/S2_4x_OD40_2L_small/simulation.py` |

```bash
cp -r Examples/E01_circular_loop Examples/MY_BOARD
cd Examples/MY_BOARD
cp ~/my_board.kicad_pcb .          # and set SETTINGS['board'] to its name
../../.venv/bin/python simulation.py --levels 0.75 --freqs 1e4      # a first, coarse run
```

Every run writes `results.json` beside the script and its working files under `case/` (the KESE
export, the mesh, the `.sif` files, Elmer's logs), which is not committed.

## 27.2 The Board And Its Coils

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
| Two ends stacked on two layers (a TX) | `P.electrodes` with the dielectric's height and a small disc round the ends as the gap | `P.sheet_vertical(m, line, z0, z1)` along a line drawn into the mesh (`extra_lines`) |
| A via left out | the same, with a `void` part (air of priority 4) that removes the barrel | as above, across the barrel |

## 27.3 The Domain And The Frequencies

| Setting | Example | What it is |
|---|---|---|
| `domain_radius_mm` | `60.0` | Radius of the air disc. At 6 coil radii the outer boundary (n × A = 0) costs about 0.2 % of L |
| `domain_half_height_mm` | `60.0` | The air reaches this far above and below z = 0 |
| `freqs_hz` | `[1e4, 3.5e6]` | One solve per frequency. Choose one low enough that the current is uniform (here 10 kHz, skin depth 0.66 mm) and the working frequency |
| `order` | `1` | Edge element order. `--order 2` uses second-order (quadratic) elements, with several times the unknowns and the memory |
| `levels` | `[0.75, 1.0, 1.3]` | The mesh ladder: each level divides `h_edge`, `h_in` and `dz_copper` by itself; the air's sizes and grading stay as they are. A run of two or three levels shows how far the answer still moves with the copper's mesh |

## 27.4 The Mesh

These go to `mesh25d.Settings` (in `SETTINGS['mesh']`):

| Setting | Example | What it is |
|---|---|---|
| `h_edge` | `0.09` | Element size at copper edges, mm. At least three elements across the narrowest trace is a good start |
| `h_in` | `0.18` | Largest element inside copper, mm |
| `h_max` | `6.0` | Largest triangle anywhere, mm (the far field) |
| `grade` | `0.5` | How fast the size grows away from copper, mm per mm |
| `dz_copper` | `0.018` | Thickest wedge layer in a copper foil, mm. Half the skin depth or less at the highest frequency (copper: 35 µm at 3.5 MHz) |
| `dz_max` | `0.4` | Thickest wedge layer elsewhere (through the board, in an air gap), mm |
| `tet_max` | `8.0` | Largest tetrahedron in the air above and below, mm |
| `tet_grade` | `0.7` | How fast the tetrahedra grow with height, mm per mm |
| `foil_max` (default) | `0.15` | The thickest slab still treated as a copper foil; thicker slabs with copper (via barrels) get `dz_max` |
| `pads` (default) | `(0.03, 0.08)` | The two air layers of wedges just above and below the boards, mm |

## 27.5 The Linear Solver

| Setting | Example | What it is |
|---|---|---|
| `threads` | `4` | OpenMP threads for ElmerSolver |
| `tol` | `1e-7` | The iterative solver's relative residual to stop at |
| `max_iter` | `3000` | The iteration cap. At low frequency the residual stalls near 10⁻⁶ (see [Elmer FEM Troubleshooting](Elmer-FEM-Troubleshooting.md)); the run then stops at the cap and goes on, which is why the cap matters. `--max-iter` changes it for one run |

## 27.6 The Command Line

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

## 27.7 Before A Large Board

Check the memory first ([Elmer FEM Hardware](Elmer-FEM-Hardware.md)): build the mesh alone (the S2
and E01 scripts have `--mesh-only`), read its node count from the log, and multiply by the measured memory per
node. A run that does not fit is better held for a larger machine than run on a coarser mesh whose
error is unknown.

| Previous | Next |
|:---|---:|
| [Elmer FEM Workflow](Elmer-FEM-Workflow.md) | [Elmer FEM Test Boards](Elmer-FEM-Test-Boards.md) |
