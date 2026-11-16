# 35. OpenEMS Implementation Workflow

What happens between `python simulation.py` and the numbers in `results.json`, step by step. Every
step is one function of `bridge/fdtd.py` on the `OpenEMS_Integration` branch.

## 35.1 Export The Board With KESE

`kese_export()` runs KESE as a program with its `openems` preset:

```bash
python run_KESE.py board.kicad_pcb --for openems --out <case>/kese/<board>_<hash>
```

which writes simulation-mode solids, one closed STL per net and per dielectric, in mm on KiCad's
origin with y up (y_model = −y_KiCad) and z = 0 in the middle of the board, and `materials.json`
with each dielectric's εr, tan δ and the frequency they were given at
([openEMS Workflow](OpenEMS-Workflow.md)). The export is kept under a hash of the board file and of
any `--set` options, and reused while they are unchanged.

## 35.2 Load The Parts

`load()` reads `materials.json` and each STL. Every part keeps its role, net, layer, heights and
bounding box; each copper part also gets its outline, the cross-section of its STL at the middle of
each of its slabs, as a shapely polygon. The outlines serve the mesh and the port checks; the solver
itself reads the STL files.

## 35.3 Place The Mesh Lines

FDTD needs a rectilinear grid. `make_mesh()` places it from the board:

| Axis | Lines |
|---|---|
| x and y | at every straight copper edge along the axis, two lines by the **thirds rule** of openEMS's tutorials: h/3 inside the metal and 2h/3 outside (h = `h_edge`), so the field's edge singularity falls between them and the metal ends on the inner line; the ports' planes; the domain's ends. Then smoothed so that no cell is larger than λ/`res_div` in the densest dielectric and no two neighbours differ by more than `ratio` |
| z | every copper face fixed, `copper_cells` cells through each copper layer; the board graded from the copper up to its thinnest dielectric over `dielectric_cells` cells; the air above and below grown by the same ratio up to λ₀/`res_div` |

The domain is the board's extent plus `air_mm` of air on each side.

## 35.4 Check The Grid And The Ports

`preflight()` stops a run that would give a wrong answer before it starts:

| Check | Pass mark |
|---|---|
| Largest cell in a dielectric, per axis | at most λ/15 in the densest dielectric at `f_max` |
| Largest cell in the air, per axis | at most λ₀/15 |
| Neighbouring cells, per axis | at most 2:1 |
| Each port's strip on copper of its own net | at least 90 % of the strip's area |
| Each port's reference copper under its strip | at least 99 % |
| Cells across each port's strip | at least 3 |

Every line of the check, passed or failed, is written to the log and to `results.json`.

## 35.5 Build The Model

`build()` makes the openEMS and CSXCAD objects:

| Item | How |
|---|---|
| Copper | PEC, every copper STL imported as a polyhedron (`AddPolyhedronReader`) |
| Dielectrics | each STL as a material with its εr, and a conductivity κ = 2πf ε₀ εr tan δ that gives its tan δ at the pulse's centre frequency |
| Excitation | a Gaussian pulse over the band (`f0`, `fc`) |
| Boundaries | MUR (first-order absorbing) on all six sides by default, a quarter wavelength from the board |
| Ports | openEMS microstrip ports (`AddMSLPort`): a strip, a feed, three voltage probes and two current probes at the measurement plane, and a resistor (`feed_r`) that ends the line |

KESE's copper is a solid of its real thickness, where openEMS's microstrip port is made for a strip
of no thickness: its current probes have no height and sit at the strip's underside, so their loop
of H runs through the copper and misses the current on the strip's top and sides. The bridge
stretches each current probe to enclose the whole strip, from its underside to its top and
`probe_pad` wider on each side (`thick_strip_probes()`).

## 35.6 Run

`run()` starts openEMS in the case folder with the CPU engine (`engine='cpu'`) and the number of
threads given, and stops when the field energy has fallen by `end_criteria` (10⁻⁴, that is 40 dB) or
after `max_steps` time steps.

## 35.7 Read Back

`port_results()` evaluates every port at the frequencies asked for:

| Result | From |
|---|---|
| S<sub>i1</sub> for every port i, with port 1 excited | the incident and reflected waves at each port's measurement plane |
| The line's impedance Z₀ at each microstrip port | the port's own probes: √(E·dE / (H·dH)) from the voltage and current and their changes along the line |
| The effective permittivity εeff | the propagation constant β from the same probes: εeff = (βc₀/ω)² |

With no reference impedance given, the S-parameters are referred to each port's own measured line
impedance. Everything, with the preflight's lines, the mesh's size, the run's time, the software
versions and the hashes of the code, is written to the example's `results.json`.

| Previous | Next |
|:---|---:|
| [OpenEMS Implementation Installation](OpenEMS-Implementation-Installation.md) | [OpenEMS Implementation Simulating Your Own Board](OpenEMS-Implementation-Simulating-Your-Own-Board.md) |
