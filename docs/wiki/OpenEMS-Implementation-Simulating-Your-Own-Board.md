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
| `f0_hz`, `fc_hz` | `3e9`, `2e9` | The Gaussian pulse: centre f0 and half-width fc, so it covers f0 − fc to f0 + fc (here 1 to 5 GHz). Keep f0 − fc above zero: a pulse that reaches down to DC leaves charge behind on copper that has no path to ground |
| `f_report_hz` | `[1e9, 2e9, 3e9, 4e9]` | The frequencies written to the log and to the `report` table of `results.json`; the data are kept at 41 frequencies over the band |
| `end_criteria` | `1e-4` | Stop when the field energy has fallen this far below its peak (40 dB) |
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

## 36.5 Before A Large Board

The preflight prints the number of cells before anything runs. openEMS needs roughly a hundred
bytes per cell and its run time grows with the number of cells times the number of time steps; see
[OpenEMS Implementation Hardware](OpenEMS-Implementation-Hardware.md) for what was measured.

| Previous | Next |
|:---|---:|
| [OpenEMS Implementation Workflow](OpenEMS-Implementation-Workflow.md) | [OpenEMS Implementation Test Boards](OpenEMS-Implementation-Test-Boards.md) |
