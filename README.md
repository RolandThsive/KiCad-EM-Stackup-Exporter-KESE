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

> [!WARNING]
> **Fill Your Zones Before Exporting.** KESE uses the zone fills KiCad stores in the board file.
> A ground plane or copper pour that has not been filled (press **B** in KiCad) and saved is left
> out entirely; `report.txt` counts it under "zones with no fill".

- This is an open, non-commercial project. The source code is free to read, use, study and
  improve for non-commercial purposes.
- **Commercial use requires a separate written license.** See [Licensing](#licensing).

---

## Goal

The goal is a **one-step path from a KiCad board to a simulation-ready 3D model**: every
dielectric, every net's copper and every via at its true height, with every copper solid named
after its net (for example `Copper_GND`), ready to drop into an EM solver such as HFSS, CST,
openEMS, FEKO or COMSOL, with no hand cleanup in CAD. The same board should also come out as a
light, good-looking model for web viewers and renders.

---

## Introduction

KiCad's own 3D export is made for mechanical fit. Copper is flattened onto the board, and nothing
in the file says which net a piece of copper belongs to. An EM solver needs the opposite: each
dielectric as its own body with its own εr and tanδ, copper at its real thickness, and one closed
solid per net so ports and excitations can be assigned.

KESE reads the `.kicad_pcb` file directly (KiCad itself does not need to be installed), rebuilds
the stack-up layer by layer and writes it out in one of two modes:

- **simulation**: the physical board as it leaves the factory. Every layer is a closed solid: each
  core and prepreg, each net's copper with all its layers and vias joined, via and hole plating,
  solder mask conformal over the copper, silkscreen, and optionally the surface finish.
- **visual**: only the visible surface of the same geometry, for web viewers such as
  `<model-viewer>` and three.js. Surfaces only microns apart no longer fight in the depth buffer.

Nothing is hard-coded: every number lives in `Parameters/`, and each output comes with a
`parameters.txt` listing exactly what produced it, including every command-line override.

---

## Project Capabilities

| Area | Capability |
|---|---|
| Input | `.kicad_pcb` from KiCad 6 to 10, 1 to 6 copper layers, stack-up read from Board Setup |
| Copper | One solid per net (default), per layer, or all merged; through, blind and buried vias; etch trapezoid |
| Edges | Castellated holes plated on the notch wall; edge plating joined to its net |
| Dielectrics | One solid per core / prepreg with εr and tanδ, or the whole laminate as one solid |
| Mask And Silk | Solder mask over laminate and copper; silkscreen in KiCad's own stroke font, clipped off the pads as fabricators do |
| Finish | ENIG, ENEPIG, HASL, OSP, immersion tin and silver, hard gold; one part per metal, or per metal and net (off by default) |
| Output | GLB, STEP with exact arcs (one named solid per part), one STL per part, OBJ with `.mtl`, in mm or m |
| Presets | `--for hfss`, `cst`, `openems` or `viewer` set units, origin, grouping and formats in one go |
| Records | `materials.json` per part (role, layer, net, z range, εr, tanδ, conductivity), `parameters.txt`, `report.txt` |
| Checks | Opt-in verifier (closed solids, no overlaps, one visible surface, glTF validation) and a regression suite in `Tests/` |
| Not Modelled | Component 3D models, text boxes, dimensions, images, rigid-flex |

### What The Simulation Model Is Good For

These uses rely on the simulation-mode output: per-net copper, dielectrics with εr and tanδ,
plating and finish.

- **Full-wave EM.** S-parameters, impedance, crosstalk, antenna patterns and resonances. For an
  inductive encoder stator like the example boards, the TX/RX coil coupling and the
  position-dependent signal can be simulated instead of only measured.
- **Signal Integrity.** Trace impedance and eye diagrams, where the exact copper thickness, the
  etch trapezoid and the prepreg-versus-core εr matter.
- **Power Integrity And DC-IR Drop.** A per-net GND or power solid with real plating thickness is
  exactly what PDN tools need.
- **Thermal.** The same solids with electrical conductivity swapped for thermal conductivity;
  copper planes, via barrels and the laminate are the heat paths.
- **Mechanical And FEA.** Warp and stress with the real copper distribution and core/prepreg
  layers, since every layer is a closed solid.
- **Parasitic Extraction.** Capacitance and inductance between nets, because each net is its own
  body.
- **What-If On Fabrication.** Change plating, via wall, mask thickness or etch factor in
  `Parameters/` and re-simulate to see how much fab tolerances move your results.

---

## Examples

`Input/` holds two inductive encoder stators. Exported in simulation mode, each comes out as one
solid per net and per dielectric:

| Board | Copper Parts | Dielectrics | Simulation GLB | Visual GLB |
|---|---|---|---|---|
| `Coil_30_50_4_1_3_Series_SteppedDiagonal_Stator` (4 layers, 53 vias) | `Copper_SIN_Signal`, `Copper_COS_Signal`, `Copper_TX` | 3 FR4 cores, 0.51 mm each | 15 MB | 10 MB |
| `Stator` (2 layers, 13 vias) | `Copper_1`, `Copper_2`, `Copper_TX` | 1 FR4 core, 1.6 mm | 5.0 MB | 4.1 MB |

Copper parts take the board's net names as they are, so the second board's unnamed nets `1` and
`2` become `Copper_1` and `Copper_2`. Both boards also get a top and bottom solder mask part.

---

## Quick Start

```bash
python -m pip install -r requirements.txt     # Python 3.12 or later; cadquery is only needed for STEP

python run_KESE.py                                     # Every board in Input/, settings from Parameters/
python run_KESE.py Input/Stator.kicad_pcb --for hfss   # STEP in mm with KiCad's origin, for HFSS
python run_KESE.py --mode simulation --format glb stl obj
python run_KESE.py --for viewer                        # Visual surface, GLB in metres, centred
python run_KESE.py board.kicad_pcb --verify            # Opt-in checks, results in report.txt
python run_KESE.py board.kicad_pcb --set Copper.VIA_WALL_MM=0.02
```

With no options a run uses `Parameters/Run_Parameters.py`: simulation mode, GLB, metres, board
centred at the origin. Run the commands from the project folder. Edit only the files in
`Parameters/`, or override one value for a single run with `--set`. Each run writes to
`Output/<board>/<mode>_<FORMATS>/`, numbered `__1`, `__2` and so on so no run overwrites another.
The folder holds the model files, `materials.json`, `parameters.txt` and `report.txt`, which lists
the stack-up heights, what was read and what was skipped and why.

On Python 3.11, install the same packages without the version pins. With cadquery installed,
`python -m pytest Tests` checks a change against the recorded results.

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
