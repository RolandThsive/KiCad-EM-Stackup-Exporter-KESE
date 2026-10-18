# 1. KiCad EM Stackup Exporter (KESE) Wiki

KESE reads a KiCad board file (`.kicad_pcb`) and writes a real 3D model of the board: every
dielectric, every net's copper and every via at its true height, with every copper solid named
after its net (for example `Copper_GND`). The same board can also be written as a light surface
model for web viewers and renders. Output formats are GLB, STEP, STL and OBJ.

The goal is a one-step path from a KiCad board to a simulation-ready 3D model, with no hand
cleanup in CAD.

## 1.1 Why This Project

KiCad's own 3D export is made for mechanical fit: copper is flattened onto the board and nothing in
the file says which net a piece of copper belongs to. An EM solver needs the opposite: each
dielectric as its own body with its own εr and tanδ, copper at its real thickness, and one closed
solid per net so that ports and excitations can be assigned. KESE reads the `.kicad_pcb` file
directly (KiCad itself does not need to be installed), rebuilds the stack-up layer by layer and
writes it out as closed solids for solvers, or as the visible surface for viewers. Every number
that shapes the model lives in `Parameters/`, and each output comes with a `parameters.txt` that
lists exactly what produced it.

> [!IMPORTANT]
> **Validation against measurements is pending.** The models have not yet been compared with
> measured boards or with reference solver results. Thicknesses default to KiCad's own values
> (35 µm copper, 10 µm solder mask), not to any fabricator's process. Set your fabricator's
> numbers in `Parameters/` before trusting a simulation built on the output.

This wiki documents KESE version 1.1.0 (`Generator/__init__.py`). Defaults quoted on every page
are those of the parameter files on `main`.

## 1.2 Links

- [Repository README](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE-#readme)
- [Getting Started](Getting-Started.md): install and export a first board.
- [Contents](Contents.md): every page of this wiki.

| Previous | Next |
|:---|---:|
|  | [Contents](Contents.md) |
