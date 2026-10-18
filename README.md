<div align="center">

# KiCad EM Stackup Exporter (KESE)

**Real 3D Models Of KiCad Boards, With The True Stack-Up And Copper Split Per Net**

Python · KiCad 6 To 10 · 1 To 6 Copper Layers · GLB, STEP, STL And OBJ · Free For Non-Commercial Use

</div>

---

## Contents

1. [Disclaimer](#disclaimer)
2. [Goal](#goal)
3. [Introduction](#introduction)
4. [Project Capabilities](#project-capabilities)
5. [Examples](#examples)
6. [Quick Start](#quick-start)
7. [Where To Read More](#where-to-read-more)
8. [Licensing](#licensing)
9. [About Me](#about-me)

---

## Disclaimer

> [!IMPORTANT]
> **Validation Against Measurements Is Pending.** The models have not yet been compared with
> measured boards or with reference solver results. Thicknesses default to KiCad's own values
> (35 µm copper, 10 µm solder mask), not to any fabricator's process. Set your fabricator's
> numbers in `Parameters/` before trusting a simulation built on the output.

- This is an open, non-commercial project. The source code is free to read, use, study and
  improve for non-commercial purposes.
- **Commercial use requires a separate written license.** See [Licensing](#licensing).

---

## Goal

The goal is a **one-step path from a KiCad board to a simulation-ready 3D model**: every
dielectric, every net's copper and every via at its true height, ready to drop into an EM solver
such as HFSS, CST, openEMS, FEKO or COMSOL, with no hand cleanup in CAD. The same board should also
come out as a light, good-looking model for web viewers and renders.

---

## Introduction

KiCad's own 3D export is made for mechanical fit. Copper is flattened onto the board, and nothing
in the file says which net a piece of copper belongs to. An EM solver needs the opposite: each
dielectric as its own body with its own εr and tanδ, copper at its real thickness, and one closed
solid per net so ports and excitations can be assigned.

KESE reads the `.kicad_pcb` file directly (KiCad itself does not need to be installed), rebuilds
the stack-up layer by layer and writes it out in two modes:

- **real**: the physical board as it leaves the factory. Every layer is a closed solid: each core
  and prepreg, each net's copper with all its layers and vias joined, via and hole plating, solder
  mask conformal over the copper, silkscreen, and optionally the surface finish.
- **pretty**: only the visible surface of the same geometry, for web viewers such as
  `<model-viewer>`. Surfaces only microns apart no longer fight in the depth buffer.

Nothing is hard-coded: every number lives in `Parameters/`, and each output comes with a
`parameters.txt` listing exactly what produced it.

---

## Project Capabilities

| Area | Capability |
|---|---|
| Input | `.kicad_pcb` from KiCad 6 to 10, 1 to 6 copper layers, stack-up read from Board Setup |
| Copper | One solid per net (default), per layer, or all merged; through, blind, buried and micro vias; etch factor |
| Dielectrics | One solid per core / prepreg with εr and tanδ, or the whole laminate as one solid |
| Mask, Silk, Finish | Solder mask over laminate and copper, silkscreen in KiCad's own stroke font, ENIG / HASL and other finishes |
| Output | GLB, STEP (one named exact solid per part), one STL per part, OBJ with `.mtl`, in mm or m |
| Records | `materials.json` per part (role, layer, net, z range, εr, tanδ, conductivity), `parameters.txt`, `report.txt` |
| Checks | Opt-in verifier: closed solids, no overlaps, one visible surface, glTF validation |
| Not Modelled | Component 3D models, text boxes, dimensions, edge plating, castellations, rigid-flex |

---

## Examples

The repository includes one example board in `Input/`: a 4-layer inductive encoder stator
(50 mm outer radius, 4 loops, SIN, COS and TX coils). Exporting it in real mode takes about
20 seconds and produces one solid per net and per dielectric:

| Part | Triangles |
|---|---|
| `Copper_SIN_Signal` | 42,436 |
| `Copper_COS_Signal` | 42,444 |
| `Copper_TX` | 24,384 |
| `Board_dielectric 1` to `3` (FR4 core, 0.51 mm each) | 57,220 |
| `Top Solder Mask`, `Bottom Solder Mask` | 212,518 |

The real-mode GLB is about 15 MB; the pretty-mode GLB of the same board is about 10 MB.

---

## Quick Start

```bash
python -m pip install -r requirements.txt     # Python 3.10 or later; cadquery is only needed for STEP

python run.py                                  # Every board in Input/, settings from Parameters/
python run.py --format glb stl obj             # The default format is STEP
python run.py Input/board.kicad_pcb --mode pretty
python run.py board.kicad_pcb --verify         # Opt-in checks, results in report.txt
python run.py board.kicad_pcb --set Copper.VIA_WALL_MM=0.02
```

Edit only the files in `Parameters/`, or override one value for a single run with `--set`. Each
run writes to `Output/<board>/<mode>/`: the model files, `materials.json`, `parameters.txt` and
`report.txt`, which lists the stack-up heights, what was read and what was skipped and why.

---

## Where To Read More

A wiki with full documentation of every parameter, the generator workflow and the output formats
is being made and will be available shortly.

---

## Licensing

**License:** [PolyForm Noncommercial License 1.0.0](LICENSE) (SPDX: `PolyForm-Noncommercial-1.0.0`).

| Free Under The License | Needs A Commercial License |
|---|---|
| Research and teaching at schools, universities and public research bodies | Running KESE at, or for, a for-profit company, including internal design and simulation work |
| Personal study, hobby projects and private research | Designing, modelling or simulating a product that is sold, or meant to be sold |
| Use by charities and government institutions | Paid consulting, contract or client work, or selling KESE or anything built on it |

**Commercial Use.** Companies and startups are welcome once terms are agreed. See
[COMMERCIAL.md](COMMERCIAL.md) for what counts as commercial use, how to ask for a license and
the list of approved companies. If you are not sure which side you are on, ask first.

**Contributing.** Code, documentation and other material are accepted under the Contributor
License Agreement in [CONTRIBUTING.md](CONTRIBUTING.md). Bug reports and ideas do not need it.

The stroke font data in `Parameters/Fonts/` comes from KiCad and keeps its own notice; see
[`LICENSE_fonts.txt`](Parameters/Fonts/LICENSE_fonts.txt).

---

<div align="center">

## About Me

A traveller and mechatronics engineer who loves building machines that move, from the mechanics
to the electronics and the firmware. Trained in mechanical design and robotics, with a research
master's in mechatronics, I have built robotic hands, a humanoid torso, industrial bin-picking
cells and rocket electronics, designing PCBs in KiCad and firmware for STM32 and Espressif chips.

Without a job at the moment, I put my full time into building industrial-grade software and making
well-researched but hard-to-find scientific knowledge free for everyone. KESE exists so that a
board designed in KiCad can go straight into an EM solver without being rebuilt by hand in CAD. I
will keep maintaining it until it becomes the go-to bridge from KiCad to EM simulation, with
models that match real, fabricated boards.

**[Website](https://ro-h-bots.blogspot.com/)** ·
**[Instagram](https://www.instagram.com/ro_h_bots)** ·
**[MyAnimeList](https://myanimelist.net/profile/RolandThsive)** ·
**[Email](mailto:rolandthsive@yahoo.com)**

*Contributions of every kind are welcome. Together we can make this the reference tool for turning
KiCad boards into EM-ready models.*

</div>
