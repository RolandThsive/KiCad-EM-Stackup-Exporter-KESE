# 19. Project Output Organization

## 19.1 The Repository

```text
KiCad-EM-Stackup-Exporter-KESE/
├── run_KESE.py              the command-line entry point
├── requirements.txt         pinned Python packages
├── Parameters/              every setting, one file per subject (the only files you edit)
│   ├── Run_Parameters.py, Board_Parameters.py, Copper_Parameters.py,
│   │   SolderMask_Parameters.py, Silkscreen_Parameters.py, Finish_Parameters.py,
│   │   Geometry_Parameters.py, Color_Parameters.py
│   └── Fonts/               kicad_newstroke.json.gz and its notice; custom fonts go here
├── Generator/               the pipeline
│   ├── Pipeline.py          Reader -> BoardBreakdown -> Geometry -> Colorer -> Assembler -> Verifier -> Packager
│   ├── Reader.py, BoardBreakdown.py, Colorer.py, Assembler.py, Verifier.py, Status.py
│   ├── Common/              s-expression parser, 2D shape helpers, stack-up, prisms
│   ├── Geometry/            Board, Copper, SolderMask, Silkscreen, Finish, Skin, Text, geometry maths
│   └── Packager/            glb, stl, obj, step, materials_json, report
├── Input/                   boards to export (three examples included)
├── Output/                  one folder per board and run (ignored by git except .gitkeep)
├── Tests/                   regression suite, test boards, baseline.json
├── docs/wiki/, docs/images/ this wiki and its pictures
├── LICENSE, COMMERCIAL.md, CONTRIBUTING.md
└── README.md
```

## 19.2 Run Folders

Every run writes to:

```text
<OUTPUT_DIR>/<board>/<mode>_<FORMATS>/
```

- `<OUTPUT_DIR>` is `Run.OUTPUT_DIR` (`Output/`) or `--out`.
- `<board>` is the file name without `.kicad_pcb`.
- `<mode>` is `simulation` or `visual`.
- `<FORMATS>` are the formats written, in upper case, joined by `_`, in the order
  `glb`, `obj`, `stl`, `step` as given: `simulation_GLB`, `simulation_STEP_STL`,
  `visual_GLB_OBJ`.

**No run overwrites another.** When the folder already exists, the new one gets a suffix:
`simulation_GLB__1`, `simulation_GLB__2`, ... The terminal line at the end of every board names
the folder that was written.

### 19.2.1 Files In A Run Folder

| File | Written when | Content |
|---|---|---|
| `<board>.glb` | `glb` requested | binary glTF 2.0; one node and one mesh per part, named after the part; PBR materials; `KHR` extensions none |
| `<board>.obj` + `<board>.mtl` | `obj` requested | one `o <part>` object per part with vertices, normals and faces; the `.mtl` has one material per part (`Kd`, `d`) |
| `stl/<part>.stl` | `stl` requested | one binary STL per part, in a `stl/` sub-folder; the name is the part name with spaces and unsafe characters replaced by `_` (`Top_Solder_Mask.stl`, `Board_dielectric_1.stl`) |
| `<board>.step` | `step` requested and `cadquery` installed | STEP AP214 assembly named after the board, one named shape per part (fused solid or compound), with colours |
| `materials.json` | `Run.WRITE_MATERIALS_JSON` | per part: role, layer, net, z range, properties, look, file names ([Material Properties](Material-Properties.md)) |
| `parameters.txt` | always | every parameter of every `Parameters/` file as it was during the run; the first line lists the preset and `--set` overrides |
| `report.txt` | always | see below |

### 19.2.2 `report.txt`

```text
Stator  (Stator.kicad_pcb)   generated 2026-10-18 15:47
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
  solder mask: 0.01 mm over laminate, 0.01 mm over copper (SolderMask_Parameters)

parts
  Board_dielectric 1                       3540 triangles  material Board_core #968A58 alpha 1.0
  Copper_TX                                9068 triangles  material Copper #CD803E alpha 1.0
  ...

timing
  read               0.0 s
  breakdown          1.4 s
  geometry           0.3 s
  assemble           8.9 s
  package            2.4 s
  verify             3.4 s

Verifier: PASS
  ...
```

| Section | Content |
|---|---|
| header | board, file, time of the run, mode, formats, units, KiCad format and generator, title block |
| warnings | the Reader's warnings, if any |
| `stack-up` | laminate thickness and its source, the z band and foil of every copper layer, every dielectric with type, material, thickness, εr, tanδ and z range, the via tenting source, the pad-to-mask clearance, the silk-over-copper setting, the origin used |
| `read` | a count of every kind of item that went into the model |
| `skipped` | a count of every kind of item left out, with the reason |
| `notes` | the font, the mask thickness and its source, finish, resin fill, castellation and edge plating notes, warnings raised while building |
| `parts` | every part with its triangle count, material key, colour and alpha |
| `timing` | seconds per stage |
| Verifier | only with `--verify`; see [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md) |

## 19.3 Part Names

Part names are the same in every file of a run: the GLB node, the OBJ object, the STL file (with
`_` for spaces), the STEP solid and the `materials.json` key.

| Role | Names |
|---|---|
| board | `Board_dielectric 1`, `Board_dielectric 2`, ... or `Board`; a merged gap: `Board_dielectric 1 + dielectric 2` |
| copper | `Copper_<net>` (`Copper_GND`, `Copper_no_net`, `Copper_~{CHG}`), or `Copper_F.Cu` ... and `Plating`, or `Copper` |
| mask | `Top Solder Mask`, `Bottom Solder Mask`; visual mode also `Top Mask over Copper`, `Bottom Mask over Copper` |
| silk | `Top Silkscreen`, `Bottom Silkscreen` |
| finish | `Top Finish Nickel`, `Bottom Finish Gold`, or `Top Finish Gold_<net>` |

Net names are used as KiCad stores them, including characters such as `~{CHG}` or `N$12`; only
the STL file names are sanitised.

## 19.4 Tests Output

`Tests/test_boards.py` writes its runs to `Tests/out/`, which is deleted at the start of every
test run and ignored by git.

| Previous | Next |
|:---|---:|
| [Material Properties](Material-Properties.md) | [KiCad And Solver Compatibility](Compatibility.md) |
