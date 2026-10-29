# 19. Project Output Organization

## 19.1 The Repository

```text
KiCad-EM-Stackup-Exporter-KESE/
├── Generator/                   KESE itself; run every command from here
│   ├── run_KESE.py              the command-line entry point (python run_KESE.py; the code is in kese/cli.py)
│   ├── requirements.txt         pinned Python packages
│   ├── pyproject.toml           for pip install -e . (the kese command), unpinned
│   ├── README.md                what is in this folder, and the first commands
│   ├── parameters/              every setting, one file per subject (the only files you edit)
│   │   └── run.py, board.py, copper.py, solder_mask.py, silkscreen.py, finish.py, geometry.py, color.py
│   ├── kese/                    the program
│   │   ├── pipeline.py          runs the nine stages in order
│   │   ├── cli.py, job.py, progress.py   command-line options, one run's request, the live status line
│   │   ├── core/                shared tools: s-expression parser, 2D maths and shapes, the
│   │   │                        boundary of a stack of prisms and its mesh, triangulation,
│   │   │                        shared vertices, extrusion, stroke font, safe file names
│   │   ├── model/               the data handed from stage to stage: RawBoard, Items, Stackup,
│   │   │                        Regions, PrismSet, Model, Files
│   │   ├── s1_read/             the file, parsed and checked
│   │   ├── s2_collect/          every item as a flat shape on its layer, one file per kind of item
│   │   ├── s3_resolve/          outline, holes, copper per net, edge plating, mask openings, silk clipping
│   │   ├── s4_geometry/         prisms: laminate, copper, plating, solder mask, silkscreen, finish
│   │   ├── s5_materials/        a material (the look) per part
│   │   ├── s6_assemble/         meshes: closed solids or the visible skin, in output units
│   │   ├── s7_write/            glb, obj, stl, step, materials.json, and the run folder
│   │   ├── s8_verify/           the opt-in Verifier
│   │   ├── s9_report/           report.txt and parameters.txt
│   │   └── assets/fonts/        kicad_newstroke.json.gz and its notice; custom fonts go here
│   ├── Input/                   boards to export (two examples included)
│   ├── Output/                  one folder per board and run (ignored by git except .gitkeep)
│   ├── tests/                   regression suite, layout rules, test boards, baseline.json
│   └── tools/                   make_swatches.py: the colour boxes of docs/ColorSwatches/
├── docs/wiki/, docs/images/     this wiki, and its pictures
├── docs/ColorSwatches/          the colour squares in the wiki's colour tables
├── docs/logo/                   the KESE logo as SVG and WebP, and favicon.ico
├── licenses/                    KiCad copyright headers and AUTHORS.txt
├── LICENSE, NOTICE.md, CONTRIBUTING.md
└── README.md
```

Everything KESE is made of is in `Generator/`; the root holds what belongs to the repository.
The paths on every other page of this wiki, such as `parameters/` or `kese/s2_collect/`, are
inside `Generator/`.

## 19.2 Run Folders

Every run writes to:

<h3 align="center"><code>&lt;OUTPUT_DIR&gt;/&lt;board&gt;/&lt;mode&gt;_&lt;FORMATS&gt;/</code></h3>

- `<OUTPUT_DIR>` is `Run.OUTPUT_DIR` (`Output/`) or `--out`.
- `<board>` is the file name without `.kicad_pcb`.
- `<mode>` is `simulation` or `visual`.
- `<FORMATS>` are the requested formats, in upper case, joined by `_`, in the order given by
  `--format` or `Run.FILE_FORMAT` (not sorted; a format given twice appears twice):
  `--format glb stl obj` gives `simulation_GLB_STL_OBJ`, `--for cst` gives `simulation_STEP_STL`.

**No run overwrites another.** When the folder already exists, the new one gets a suffix:
`simulation_GLB__1`, `simulation_GLB__2`, ... The terminal line at the end of every board names
the folder that was written.

### 19.2.1 Files In A Run Folder

| File | Written when | Content |
|---|---|---|
| `<board>.glb` | `glb` requested | binary glTF 2.0; one node and one mesh per part, named after the part; PBR materials; no glTF extensions |
| `<board>.obj` + `<board>.mtl` | `obj` requested | one `o <name>` object per part with vertices, normals and faces; the `.mtl` has one material per part (`Kd`, `d`); object and material names are sanitised as for STL (`Top_Solder_Mask`) |
| `stl/<name>.stl` | `stl` requested | one binary STL per part, in a `stl/` sub-folder; the name is the part name with every run of characters other than `A-Z a-z 0-9 _ . + -` replaced by `_`, and leading or trailing `_` removed (`Top_Solder_Mask.stl`, `Board_dielectric_1.stl`, `Copper__RESET.stl` for net `~{RESET}`) |
| `<board>.step` | `step` requested (simulation mode) | STEP AP214 assembly named after the board, one named shape per part whose role is in `Run.STEP_WRITE_ROLES`, with colours: the part's closed solids, one per separate body, in `Run.UNITS`; mask and silk are left out by default. It is written straight into the file one part at a time and removed when the export fails. With `Run.BUILD_WITH_KERNELS = True` (needs `cadquery`) each part is a fused solid or a compound, also in `Run.UNITS`, and until the file is done `<board>.step.part` and `<board>.step.body` sit beside it; they are removed at the end, also when the export fails |
| `materials.json` | `Run.WRITE_MATERIALS_JSON` | per part: role, layer, net, z range, properties, look, file names ([Material Properties](Material-Properties.md)) |
| `parameters.txt` | always | every parameter of every `parameters/` file as it stood for the run; when `--for`, `--set`, `--mode`, `--format` or `--verify` was used, the first line lists those overrides (`--out` is not recorded) |
| `report.txt` | always | see below |

### 19.2.2 `report.txt`

```text
Stator  (Stator.kicad_pcb)   generated 2026-10-28 18:33
mode: simulation   formats: glb, stl, obj   units: m
KiCad format 20221018, generator pcbnew, title: Stator 1 loop, no sub-coils

stack-up
  copper layers: F.Cu, B.Cu
  laminate 1.6000 mm (file (general (thickness)) - no usable stackup)
  F.Cu     z +0.8000 .. +0.8350 mm  (foil 0.035 mm)
  B.Cu     z -0.8350 .. -0.8000 mm  (foil 0.035 mm)
  dielectric 1             core     FR4        1.6000 mm  er 4.5  tan d 0.02   z -0.8000 .. +0.8000
  vias: KiCad default (vias tented); pad-to-mask clearance 0.0 mm; silkscreen over copper (mask openings): False
  origin: outline centre (100.0000, 100.0000) in KiCad coordinates

read
       2  outline shapes on Edge.Cuts
      13  through vias
    1717  tracks on B.Cu
     697  tracks on F.Cu
skipped
  nothing

notes
  font: KiCad newstroke (kicad_newstroke.json.gz)
  solder mask: 0.01 mm over laminate, 0.01 mm over copper (parameters/solder_mask.py)

parts
  Board_dielectric 1                       3540 triangles  material Board_core #968A58 alpha 1.0
  Copper_1                                 9508 triangles  material Copper #CD803E alpha 1.0
  Copper_2                                 9516 triangles  material Copper #CD803E alpha 1.0
  Copper_TX                                9068 triangles  material Copper #CD803E alpha 1.0
  ...

timing
  read               0.0 s
  collect            0.7 s
  resolve            0.2 s
  geometry           0.1 s
  materials          0.0 s
  assemble           1.3 s
  write              1.2 s
  verify             0.5 s

Verifier: PASS
  ...
```

| Section | Content |
|---|---|
| header | board, file, time of the run, mode, formats, units, KiCad format and generator, the title from the title block |
| warnings | the warnings from reading the file, if any |
| `stack-up` | laminate thickness and its source, the z band and foil of every copper layer, every dielectric with type, material, thickness, εr, tanδ and z range, the via tenting source, the pad-to-mask clearance, the silk-over-copper setting, the origin used |
| `read` | a count of every kind of item read from the file (non-plated holes are counted here even when `Board.INCLUDE_NON_PLATED_HOLES = False` leaves them out) |
| `skipped` | a count of the items left out, with the reason (hidden text and text on layers that are not drawn are left out without a count) |
| `notes` | the font, the mask thickness and its source, finish, resin fill, castellation and edge plating notes, warnings raised while building |
| `parts` | every part with its triangle count, material key, colour and alpha |
| `timing` | seconds per stage (verify only when the Verifier ran) |
| Verifier | only with `--verify` or `Run.VERIFY = True`; see [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md) |

## 19.3 Part Names

The GLB node, the STEP solid and the `materials.json` key carry the part name exactly. The STL
file name and the OBJ object and material names carry it sanitised (the rule in section 19.2.1).

| Role | Names |
|---|---|
| board | `Board_dielectric 1`, `Board_dielectric 2`, ... or `Board`; a gap of several stack-up dielectrics: `Board_dielectric 1 + dielectric 2` |
| copper | `Copper_<net>` (`Copper_GND`, `Copper_no_net`, `Copper_~{RESET}`), or `Copper_F.Cu` ... and `Plating`, or `Copper` |
| mask | `Top Solder Mask`, `Bottom Solder Mask`; visual mode also `Top Mask over Copper`, `Bottom Mask over Copper` |
| silk | `Top Silkscreen`, `Bottom Silkscreen` |
| finish | `Top Finish Nickel`, `Bottom Finish Gold`, or `Top Finish Gold_<net>` |

Net names are used as KiCad stores them, including characters such as `~{RESET}`, `/SDA` or
`Net-(R1-Pad2)`, so for such nets the STL and OBJ names differ from the part name
(`Copper__RESET`, `Copper__SDA`, `Copper_Net-_R1-Pad2`). `materials.json` gives the STL name
under `file_names.stl`, built with the same rule, so it always matches the file on disk.

> [!NOTE]
> Two part names that sanitise to the same string (for example nets `/SDA` and `~{SDA}`) would
> write the same STL file, and the second would replace the first.

## 19.4 Tests Output

`tests/test_boards.py` writes its runs to `tests/out/`, which is deleted at the start of every
test run and ignored by git. `tests/test_layout.py`, `tests/test_colors.py` and
`tests/test_step_arcs.py` write nothing, and `tests/test_step_native.py`, `tests/test_step_file.py`,
`tests/test_step_kernel.py` and `tests/test_text_layout.py` write only in a temporary folder that they
remove.

| Previous | Next |
|:---|---:|
| [Material Properties](Material-Properties.md) | [KiCad And Solver Compatibility](Compatibility.md) |
