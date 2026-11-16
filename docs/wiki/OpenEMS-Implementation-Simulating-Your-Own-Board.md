# 36. OpenEMS Implementation Simulating Your Own Board

Every example on the `OpenEMS_Integration` branch is one folder with its board and a
`simulation.py` whose settings are all in one dictionary, `SETTINGS`, at the top of the file. To
simulate a board of your own, copy the example closest to it and change those settings; this page
lists every one.

## 36.1 Start From An Example

```bash
cp -r Examples/O01_microstrip Examples/MY_BOARD
cd Examples/MY_BOARD
cp ~/my_board.kicad_pcb .          # and set SETTINGS['board'] to its name
../../Solver_OpenEMS/install/venv/bin/python simulation.py
```

Every run writes `results.json` beside the script and its working files under `case/` (the KESE
export and openEMS's probe files), which is not committed. The ports are placed in `main()` from
the board's geometry; for a board of your own, set each port's corners there (see 36.3).

## 36.2 The Board And The Band

| Setting | Example (O01) | What it is |
|---|---|---|
| `board` | `'O01_microstrip.kicad_pcb'` | The KiCad board, beside the script |
| `length_mm`, `width_mm`, `centre_kicad` | `50.0`, `2.9`, `(100.0, 100.0)` | O01's line, used to place its ports; a board of your own has its own way to name where its ports are |
| `f0_hz`, `fc_hz` | `3e9`, `2e9` | The Gaussian pulse: centre f0 and fc, the distance to its 20 dB corners, so it covers f0 − fc to f0 + fc (here 1 to 5 GHz) |
| `f_report_hz` | `[1e9, 2e9, 3e9, 4e9]` | The frequencies written to the log and to the `report` table of `results.json`; the data are kept at 41 frequencies over the band |
| `dc_free` | `True` | The pulse's sine carrier, which has no DC part. openEMS's default cosine carrier has a small one, which leaves static charge on the copper so that the field energy never falls below about −40 dB. An openEMS build older than the option falls back to the cosine |
| `end_criteria` | `1e-5` | Stop when the field energy has fallen this far below its peak (50 dB) |
| `max_steps` | `80000` | Stop after this many time steps at most |
| `threads` | `4` | Threads for openEMS |
| `engine` | `'cpu'` | openEMS's CPU engine; `None` uses the default engine, for a build that does not have it |

## 36.3 The Ports

Each port is an `F.MSLPortSpec`:

| Field | What it is |
|---|---|
| `number` | 1, 2, ... |
| `net`, `ref_net` | The strip's net and its reference copper's net, as KESE names them (`no_net` for copper with no net, such as a filled polygon) |
| `start` | (x, y, z) in model mm: one corner of the strip at the port's outer end, with z at the strip's underside (y = −y_KiCad) |
| `stop` | (x, y, z): the opposite corner, `port_len_mm` along the line, with z at the reference copper's top |
| `prop_dir` | `'x'` or `'y'`: the direction the line runs |
| `excite` | `1.0` for the excited port, `0.0` for the others |
| `feed_shift` | mm from the port's end to its feed (`feed_shift_mm`, 0 here) |
| `meas_shift` | mm from the port's end to its measurement plane (`meas_shift_mm`) |
| `feed_r` | The resistor at the port's end, Ω (`feed_r_ohm`, 50): it ends the line |
| `strip_top` | z of the strip's top face. Needed with KESE's thick copper: the current probes are stretched to enclose the whole strip |
| `probe_pad` | mm added to each side of the current probes (the mesh's `h_edge` here) |

## 36.4 The Mesh

These go to `F.MeshSpec` (in `SETTINGS['mesh']`):

| Setting | Example | What it is |
|---|---|---|
| `f_max` | `5e9` | The highest frequency of interest, Hz: it sets the wavelengths the cells are measured against |
| `res_div` | `30` | Cells per wavelength in the densest dielectric, at least (and λ₀/`res_div` in the air) |
| `h_edge` | `0.2` | mm: the thirds-rule spacing at copper edges. `--h-edge 0.1` runs a finer mesh, written to `results_h0.1.json` |
| `dielectric_cells` | `6` | Cells through each dielectric, at least |
| `copper_cells` | `1` | Cells through each copper layer |
| `ratio` | `1.4` | The largest ratio between neighbouring cells |
| `air_mm` | `(15.0, 15.0, 15.0)` | mm of air round the board in x, y and z, each side |
| `boundaries` (in `SETTINGS`) | `['MUR'] * 6` | The six boundaries (x min, x max, y min, y max, z min, z max): `'MUR'`, `'PML_8'`, `'PEC'` or `'PMC'` |

A cell of 35 µm through the copper makes the time step small (openEMS warns *the timestep seems to
be very small*); the run is still right, only longer.

## 36.5 The Command Line

| Option | What it does |
|---|---|
| (none) | The run with `SETTINGS` as they are, to `results.json` |
| `--h-edge MM` | Another thirds-rule spacing at the copper's edges, to `results_h<MM>.json` |
| `--dielectric-cells N` | At least N cells through each dielectric, to `results_h<MM>_z<N>.json` |
| `--engine NAME` | `cpu` (the default here), `multithreaded`, `basic`, or `default` for openEMS's own choice; any other than `cpu` adds `_<NAME>` to the results' name |
| `--dump` | Also writes E in the plane halfway through the core as HDF5 under `case/`, sampled at the rate openEMS picks from the pulse's band (for the field pictures); adds `_dump` to the results' name |
| `--out DIR` | The working folder instead of `case/` |
| `--reuse` | Reads the last run's probe files again, without running openEMS: for a change to the read-back only |

The options combine: `--h-edge 0.1 --engine default` writes `results_h0.1_default.json`.

## 36.6 Before A Large Board

The preflight prints the number of cells before anything runs. openEMS needs about 60 bytes per cell
with its CPU engine and about 100 with its default engine, and its run time grows with the number of
cells times the number of time steps; see
[OpenEMS Implementation Hardware](OpenEMS-Implementation-Hardware.md) for what was measured.

| Previous | Next |
|:---|---:|
| [OpenEMS Implementation Workflow](OpenEMS-Implementation-Workflow.md) | [OpenEMS Implementation Test Boards](OpenEMS-Implementation-Test-Boards.md) |
