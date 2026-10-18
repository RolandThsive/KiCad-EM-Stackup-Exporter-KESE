# Kicad_PCB__to__3D_Model

Converts a KiCad board file (`.kicad_pcb`, KiCad 6–10, 1–6 copper layers) into a 3D model.

Two modes:

- **real** – the physical stack-up as it leaves the factory. Every layer is a closed solid at its
  true height: each dielectric (core / prepreg), every net's copper (all its layers and vias
  joined), the via and hole plating, top and bottom solder mask (conformal over the copper), top
  and bottom silkscreen, and optionally the surface finish. Meant for EM simulation (HFSS, CST,
  openEMS, FEKO, COMSOL) and CAD.
- **pretty** – the board's visible surface only, for web viewers such as `<model-viewer>`.
  Same geometry, but surfaces that are only microns apart no longer fight in the depth buffer.

Nothing is hard-coded in the generator: every number lives in `Parameters/`, and each output
comes with a `parameters.txt` listing exactly what produced it.

## Install

    pip install -r requirements.txt            # numpy shapely trimesh manifold3d mapbox_earcut rtree
    pip install -r requirements-step.txt       # optional, for STEP output (cadquery; large)

## Use

    python run.py                                   # every board in Input/, settings from Parameters/
    python run.py Input/board.kicad_pcb
    python run.py board.kicad_pcb --mode pretty
    python run.py board.kicad_pcb --format glb step stl
    python run.py board.kicad_pcb --verify          # opt-in checks, results in report.txt
    python run.py board.kicad_pcb --set Copper.VIA_WALL_MM=0.02 --set Board.BOARD_THICKNESS_MM=0.8

Output goes to `Output/<board>/<mode>/`:

| file | what |
|---|---|
| `<board>.glb` | binary glTF, one mesh per part, materials from `Color_Parameters` |
| `<board>.step` | STEP assembly, one named exact solid per part: dielectrics, copper per net, plating, finish (real mode only; mask/silk optional via `STEP_WRITE_ROLES`, memory-heavy) |
| `stl/<part>.stl` | one STL per part (real mode only) |
| `<board>.obj` + `.mtl` | Wavefront OBJ, one object per part |
| `materials.json` | per part: role, layer, net, z range, thickness, εr, tanδ, conductivity, colour |
| `parameters.txt` | every parameter value used for this output, plus command-line overrides |
| `report.txt` | stack-up heights, what was read, what was skipped and why, timings, verifier |

## Workflow (Generator/)

    Reader          .kicad_pcb -> parsed tree, version and layer check
    BoardBreakdown  tree -> tracks, zones, pads, vias, holes, outline, mask openings, silk, text
                    -> flat regions per layer, per net, holes drilled per layer span, heights
    Geometry/       regions -> prisms (flat region + z range + part + role + properties)
        Board.py        one prism per dielectric, resin around inner copper
        Copper.py       every copper layer per net, plating of every hole, etch factor
        SolderMask.py   top/bottom mask, thicker on laminate than on copper, walls at traces
        Silkscreen.py   ink on the mask surface (Text.py renders KiCad's own stroke font)
        Finish.py       ENIG / HASL / ... on bare copper (off by default)
        Skin.py         pretty mode: prisms -> visible surface
    Colorer         material per part from Color_Parameters (stackup colours honoured)
    Assembler       one in-memory Model: meshes + prisms in output units and orientation
    Verifier        opt-in: closed solids, no overlaps, one visible surface, glTF validation
    Packager/       the Model -> glb / stl / obj / step / materials.json / report, nothing rebuilt per format

## Parameters/

| file | covers |
|---|---|
| `Run_Parameters.py` | mode, folders, file formats, units, origin, orientation, copper/dielectric grouping, verifier, export details |
| `Board_Parameters.py` | laminate thickness source, dielectric defaults (εr, tanδ), resin fill, holes, outline fallback |
| `Copper_Parameters.py` | foil thicknesses, plating added to outer copper, via/PTH wall, etch factor, tenting, conductivity |
| `SolderMask_Parameters.py` | mask thickness over laminate / over copper, edge pullback, pad clearance, silk subtraction |
| `Silkscreen_Parameters.py` | ink thickness, font file, KiCad text metrics |
| `Finish_Parameters.py` | finish on/off, type, layer thicknesses per finish, conductivities |
| `Geometry_Parameters.py` | snap grid, curve faceting, simplification, skin test offset |
| `Color_Parameters.py` | colour / alpha / metallic / roughness per material, KiCad stackup colour tables |

Thicknesses default to KiCad's own values (35 µm copper, 10 µm mask) so a fresh run matches
KiCad. For an as-fabricated model set your fabricator's numbers: `OUTER_PLATING_ADDED_MM`,
`VIA_WALL_MM`, `MASK_OVER_LAMINATE_MM` / `MASK_OVER_COPPER_MM`, `ETCH_FACTOR`, `FINISH_ENABLED`.

## Fonts

Text is drawn with KiCad's own stroke font (`Parameters/Fonts/kicad_newstroke.json.gz`, see
`LICENSE_fonts.txt`) using KiCad's layout rules, so silkscreen labels match the layout. A custom
font (this JSON format or a Hershey `.jhf`) can be named in `Silkscreen_Parameters.FONT_FILE`;
if it is missing the default is used and `report.txt` says so. TrueType faces named in a board
are drawn with the stroke font.

## Not modelled

Component 3D models, text boxes and dimensions, edge plating / castellations, rigid-flex. Every
skipped item is counted in `report.txt`.

## Tests/boards

Synthetic boards covering a single-sided board, a 6-layer board with a full stackup, blind /
buried / micro vias, `remove_unused_layers`, KiCad 9 layer numbering, and a board with every pad
shape, mask openings, zones and text.
