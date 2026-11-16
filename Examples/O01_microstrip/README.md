# O01 Microstrip

The first proof board of the openEMS bridge: one straight microstrip, so that every part of the chain
(KESE's export, the mesh, the ports, the solver and the read-back) is checked against numbers that
are known without any solver.

| Top | Bottom |
|:---:|:---:|
| ![O01, top](O01_microstrip_top.webp) | ![O01, bottom](O01_microstrip_bottom.webp) |

Rendered by KESE's static renderer from the board's own export.

## The Board

| Item | Value |
|---|---|
| Board | 50 mm × 30 mm, two copper layers, 1.6 mm finished (a 1.53 mm FR-4 core, εr 4.4, tan δ 0.02 at 1 GHz) |
| Trace | net `RF` on F.Cu, 2.9 mm wide, 35 µm thick, along x across the whole board; its round ends just touch the board's edges |
| Ground | B.Cu, one filled polygon with no net under the whole board |
| Made by | `make_board.py`, with the bridge's `kicad_writer.py` |

2.9 mm on this core is a 50 Ω line by Hammerstad and Jensen's formulas, so a port ended in 50 Ω
barely reflects and the line's own numbers stand out.

## What openEMS Checks

| Check | How | Reference |
|---|---|---|
| Characteristic impedance Z0 | port 1's own probes, √(E·dE / (H·dH)) | Hammerstad and Jensen with the strip's thickness: 49.83 Ω |
| Effective permittivity εeff, from the port | the propagation constant β of port 1's probes, εeff = (βc₀/ω)² | Kirschning and Jansen's dispersion: 3.318 at 1 GHz to 3.397 at 4 GHz |
| εeff, a second way | the phase of S21 over the 38 mm between the two ports' measurement planes | the same |
| S21 | port 2's outgoing wave over port 1's incident one | the dielectric's loss alone (Pozar, section 3.8): −0.347 dB at 3 GHz |
| S11 | port 1's reflected wave | well below −20 dB for a line ended in about its own impedance |

The run excites port 1 only, so it gives one column of S, S11 and S21, and nothing is filled in by
symmetry.

## How It Runs

```bash
python simulation.py                   # about 1.5 minutes on 4 cores
python simulation.py --h-edge 0.1      # a finer mesh at the copper's edges, to results_h0.1.json
python simulation.py --engine default  # openEMS's default engine, to results_h0.2_default.json
python simulation.py --dump            # also dump E halfway through the core, for make_pictures.py
python simulation.py --section         # also dump E and H across the line at 1 and 3 GHz, for make_pictures.py
python make_pictures.py                # the wiki's charts, the field across the line and the animation, into pictures/
python simulation.py --reuse           # read the last run again without running openEMS
```

Every setting is in `SETTINGS` at the top of `simulation.py`:

| Setting | Value | Why |
|---|---|---|
| Pulse | f0 3 GHz, fc 2 GHz: 1 to 5 GHz, DC-free (`dc_free=True`, a sine carrier) | the band the line is checked over; the DC-free pulse leaves no static charge on the copper |
| Ports | 10 mm long at each end of the line, measurement plane 6 mm in, 50 Ω at the end | the probes sit away from the feed's near field |
| Mesh | λ/30 in the FR-4 at 5 GHz, thirds rule with h 0.2 mm at the copper's edges, 6 cells through the core, 1 through each copper, neighbours within 1.4 | 411,424 cells |
| Boundaries | MUR on all six sides, 15 mm (a quarter wavelength at 5 GHz) from the board | |
| Stop | the field energy 50 dB under its peak | about 23,000 time steps |
| Engine | openEMS's CPU engine | the same numbers as the default engine within 0.005 %, faster and with less memory |

The dielectric's loss is a conductivity κ = 2πf0 ε₀ εr tan δ, which gives tan δ exactly at f0 (3 GHz)
and tan δ · f0 / f at another frequency; the S21 reference uses the same.

## Results

See [results.md](results.md): expected against what came out, the mesh study and the bugs this
board found.

## Licence

GPL-3.0, as the rest of this branch.
