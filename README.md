# KiCad EM Stackup Exporter (KESE)

KESE exports a KiCad PCB as real 3D geometry: every copper layer, dielectric and
via at its true stackup thickness, with copper split per net. The output is meant
both for electromagnetic (EM) simulation tools and for good-looking visual renders.

> **Status:** early development. This README describes the intended scope; the
> exporter itself is not in the repository yet.

## Why

KiCad's built-in 3D export (STEP/VRML) is aimed at mechanical fit and pretty
pictures. It flattens copper, ignores the real layer stackup, and does not keep
track of which net a piece of copper belongs to. EM solvers need the opposite:
accurate thicknesses, one solid per net, and dielectrics as separate bodies.
KESE fills that gap.

## Features

- **Real stackup geometry.** Copper, prepreg, core, soldermask and silkscreen
  layers are extruded at the thicknesses defined in the board's Physical Stackup
  (Board Setup → Board Stackup).
- **Per-net copper.** Tracks, pads, zones and via barrels are merged into one
  body per net and named after it (for example `GND`, `USB_D+`), so they can be
  selected, assigned materials or excited as ports in an EM tool.
- **Vias and drills.** Plated vias become copper barrels connecting their layers;
  drills are cut out of dielectric and copper.
- **Multiple formats.**

  | Format | Use |
  |--------|-----|
  | GLB (glTF binary) | Web viewers, Blender, game engines; keeps per-net names and materials |
  | STL | Simulation and meshing tools; one file per net or layer |
  | OBJ | General 3D tools; per-net groups with a companion `.mtl` |

- **Two output profiles.**
  - **Full**: exact geometry for simulation, nothing simplified.
  - **Pretty**: a minimized version for visual rendering, with reduced triangle
    count, merged small features and render-friendly materials (copper, gold
    finish, soldermask colour).

## Requirements

- KiCad 8 or later (the exporter reads `.kicad_pcb` files and the board stackup)
- Python 3.10 or later

## Installation

_Coming soon._ Installation will be documented here once the first release is
available, either as a KiCad plugin (Plugin and Content Manager) or as a
standalone command-line tool.

## Usage

The planned command-line interface looks like this:

```sh
# Full-accuracy export for EM simulation
kese export board.kicad_pcb --format glb --profile full -o out/

# Lightweight render version
kese export board.kicad_pcb --format glb --profile pretty -o out/

# Only selected nets, as STL files
kese export board.kicad_pcb --format stl --nets GND,USB_D+,USB_D- -o out/
```

These commands are a design sketch and may change before the first release.

## Output layout

```
out/
├── board_full.glb
├── board_pretty.glb
├── stl/
│   ├── net_GND.stl
│   ├── net_USB_D+.stl
│   └── dielectric_core_1.stl
└── obj/
    ├── board.obj
    └── board.mtl
```

## Roadmap

- [ ] Parse `.kicad_pcb` and the physical stackup
- [ ] Build per-net copper solids (tracks, pads, zones, vias)
- [ ] Dielectric and soldermask bodies
- [ ] GLB, STL and OBJ writers
- [ ] Pretty profile (mesh simplification and materials)
- [ ] KiCad action plugin
- [ ] Packaged release

## Contributing

Issues and pull requests are welcome. Please open an issue first for larger
changes so the approach can be discussed.

## License

KESE is released under the MIT License. See [LICENSE](LICENSE) for details.
