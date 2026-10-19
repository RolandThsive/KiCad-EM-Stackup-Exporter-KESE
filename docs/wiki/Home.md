# 1. KiCad EM Stackup Exporter (KESE) Wiki

KESE reads a KiCad board file (`.kicad_pcb`) and writes a real 3D model of the board: every
dielectric, every net's copper and every via at its true height, with every copper solid named
after its net (for example `Copper_GND`). The same board can also be written as a light surface
model for web viewers and renders. Output formats are GLB, STEP, STL and OBJ.

The goal is a one-step path from a KiCad board to a simulation-ready 3D model, with no hand
cleanup in CAD.

## 1.1 Why This Project

KiCad's own 3D export is made for mechanical fit. Its STEP export can include copper (KiCad 9
groups it by net), but the laminate stays one body, and nothing in the file carries εr, tanδ or
conductivity. An EM solver needs each dielectric as its own body with its own εr and tanδ, copper
at its real thickness, and one closed solid per net so that ports and excitations can be
assigned, with the material values alongside. KESE reads the `.kicad_pcb` file directly (KiCad
itself does not need to be installed), rebuilds the stack-up layer by layer and writes it out as
closed solids for solvers, or as the visible surface for viewers. Almost every number that
shapes the model lives in `Parameters/` (the 1.6 mm laminate used when the file gives no
thickness is built into the code; `Board.BOARD_THICKNESS_MM` overrides it), and each output
comes with a `parameters.txt` that lists the parameter values behind it.

> [!IMPORTANT]
> **Validation against measurements is pending.** The models have not yet been compared with
> measured boards or with reference solver results. Thicknesses default to KiCad's own values
> (35 µm copper, 10 µm solder mask), not to any fabricator's process. Set your fabricator's
> numbers in `Parameters/` before trusting a simulation built on the output.

This wiki documents KESE version 2.2.0 (`Generator/__init__.py`). Defaults quoted on every page
are those of the parameter files on `main`.

## 1.2 Links

- [Repository README](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE#readme)
- [Getting Started](Getting-Started.md): install and export a first board.
- [Contents](Contents.md): every page of this wiki.

| Previous | Next |
|:---|---:|
|  | [Contents](Contents.md) |
