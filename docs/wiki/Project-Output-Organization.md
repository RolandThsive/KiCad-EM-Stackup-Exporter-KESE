# 11. Project Output Organization

## 11.1 The Repository

```text
KiCad-EM-Stackup-Exporter-KESE/
├── Generator/                   KESE itself; run every command from here
│   ├── run_KESE.py              the command-line entry point (python run_KESE.py; the code is in kese/cli.py)
│   ├── requirements.txt         pinned Python packages
│   ├── pyproject.toml           for pip install -e . (the kese command), unpinned
│   ├── README.md                what is in this folder, and the first commands
│   ├── parameters/              every setting, one file per subject (the only files you edit)
│   │   ├── PCB_elements/        the board: Stackup.py (what is built, line by line), Board.py, Copper.py,
│   │   │                        Finish.py, SolderMask.py, SilkScreen.py
│   │   ├── Run_KESE/            the run: Run.py, Geometry.py, Parallel.py, Verifier.py, Presets.py
│   │   └── Fileformats/         the files written: Step.py, Mesh.py
│   ├── kese/                    the program
│   │   ├── pipeline.py          runs the nine stages in order
│   │   ├── cli.py, job.py, progress.py   command-line options, one run's request, the live status line
│   │   ├── core/                shared tools: s-expression parser, 2D maths and shapes, the
│   │   │                        boundary of a stack of prisms and its mesh, triangulation,
│   │   │                        shared vertices, the coating over raised copper, files written
│   │   │                        whole, work in threads and processes,
│   │   │                        the copies of shapes they use and the memory they hand back,
│   │   │                        stroke font, safe file names
│   │   ├── model/               the data handed from stage to stage: RawBoard, Items, Stackup,
│   │   │                        Regions, PrismSet, Model, Files
│   │   ├── s1_read/             the file, parsed and checked
│   │   ├── s2_collect/          every item as a flat shape on its layer, one file per kind of item
│   │   ├── s3_resolve/          outline, holes and their machining, copper per net, edge plating, mask openings, silk clipping
│   │   ├── s4_geometry/         prisms: laminate, copper, plating, via fills, solder mask, silkscreen, finish
│   │   ├── s5_materials/        a material (the look) per part
│   │   ├── s6_assemble/         meshes: closed solids or the visible skin, in output units
│   │   ├── s7_write/            glb, obj, stl, step, materials.json, and the run folder
│   │   ├── s8_verify/           the Verifier
│   │   ├── s9_report/           report.txt and parameters.txt
│   │   └── assets/fonts/        kicad_newstroke.json.gz and its notice; custom fonts go here
│   ├── Input/                   boards to export (three examples included)
│   ├── Output/                  one folder per board and run (ignored by git, except .gitkeep and
│   │                            four example runs of rf_module in Output/rf_module/)
│   ├── tests/                   regression suite, layout rules, test boards, baseline.json
│   └── tools/                   make_swatches.py: the colour boxes of docs/images/Colorizing/ColorSwatches/;
│                                font_lines.py: a stroke font rewritten as JSON Lines
├── featureTest/                 the feature test boards, one feature each
├── docs/wiki/                   this wiki
├── docs/images/                 its pictures, one folder for each page, named as the page: Examples/ (the
│                                example boards), Feature-Test-Collection/ (the feature test boards),
│                                Colorizing/ColorSwatches/ (the colour squares in the colour tables), ...;
│                                README/ holds the main README's
├── docs/logo/                   the KESE logo as SVG and WebP, and favicon.ico
├── .github/                     the workflow that copies docs/wiki/ to the wiki, and Dependabot's settings
├── licenses/                    KiCad copyright headers and AUTHORS.txt
├── LICENSE, NOTICE.md, CONTRIBUTING.md
└── README.md
```

Everything KESE is made of is in `Generator/`; the root holds what belongs to the repository.
The paths on every other page of this wiki, such as `parameters/` or `kese/s2_collect/`, are
inside `Generator/`.

## 11.2 Run Folders

Every run writes to:

<h3 align="center"><code>&lt;OUTPUT_DIR&gt;/&lt;board&gt;/&lt;mode&gt;_&lt;FORMATS&gt;/</code></h3>

- `<OUTPUT_DIR>` is `Run.OUTPUT_DIR` (`Output/`) or `--out`.
- `<board>` is the file name without `.kicad_pcb`.
- `<mode>` is `simulation` or `visual`.
- `<FORMATS>` are the requested formats, in upper case, joined by `_`, in the order given by
  `--format` or `Run.FILE_FORMAT` (not sorted; a format given twice appears twice):
  the default gives `simulation_STEP`, `--format glb stl obj` gives `simulation_GLB_STL_OBJ`, `--format step stl`
  gives `simulation_STEP_STL`.

**No run overwrites another.** When the folder already exists, the new one gets a suffix:
`simulation_STEP__1`, `simulation_STEP__2`, ... Runs started together (a batch of boards in
parallel, into the same output root) each get a folder of their own: a name is taken by making the
folder, so the second run moves on to the next name. The terminal line at the end of every board
names the folder that was written.

### 11.2.1 Files In A Run Folder

| File | Written when | Content |
|---|---|---|
| `<board>.glb` | `glb` requested | binary glTF 2.0; one node and one mesh per part, named after the part; PBR materials; no glTF extensions |
| `<board>.obj` + `<board>.mtl` | `obj` requested | one `o <name>` object per part with vertices, normals and faces; the `.mtl` has one material per part (`Kd`, `d`); object and material names are sanitised as for STL (`Top_Solder_Mask`) |
| `stl/<name>.stl` | `stl` requested | one binary STL per part, in a `stl/` sub-folder; the name is the part name with every run of characters other than letters (of any script), digits and `_ . + -` replaced by `_`, and leading or trailing `_` and `.` removed (`Top_Solder_Mask.stl`, `Board_dielectric_1.stl`, `Copper__RESET.stl` for net `~{RESET}`); a name Windows reserves, such as `CON`, gets a `_` after it |
| `<board>.step` | `step` requested (simulation mode) | STEP AP214 assembly named after the board, one named shape per part, with colours: the part's closed solids, one per separate body, in `Run.UNITS`. The parts are the ones whose lines of the stack-up are `True` (`parameters/PCB_elements/Stackup.py`), as in every other file. It is written straight into the file one part at a time |
| `materials.json` | `Run.WRITE_MATERIALS_JSON` | per part: role, layer, net, z range, properties, look, file names ([Material Properties](Material-Properties.md)) |
| `parameters.txt` | always | every parameter of every `parameters/` file as it stood for the run; when `--for`, `--set`, `--mode`, `--format`, `--verify` or `--no-verify` was used, the first line lists those overrides (`--out` is not recorded) |
| `report.txt` | always | see below |

A file is written whole or not at all: when writing fails on the way (a full disk, or a part that
cannot be written), the file being written is removed, an OBJ with its MTL, and the run folder too
when nothing in it was written whole (and the board's folder, when it holds no other run). The
error that comes out is the one that stopped the write, even when a file or folder cannot be
removed after it (that one is left)
([Checks, Errors And Warnings](Checks-Errors-And-Warnings.md#2011-errors)). While a big board's
STEP file is written in worker processes, its parts are first written into a hidden folder beside
it, `.<board>.step.parts` (`<board>.step` cut to its first 40 characters), which is removed once
the file is done or the write fails
([Working Principle](Working-Principle.md#74-work-done-in-parallel)).

### 11.2.2 `report.txt`

`Input/rf_module.kicad_pcb` in simulation mode with the solder mask and silkscreen turned on
(`--set Stackup.solder_mask=True --set Stackup.silkscreen=True`), the plies fused, three mesh formats
in metres with the board centred, and `Geometry.CIRCLE_CHORD_TOLERANCE_MM = 0.002`, the default until
0.005, `...` where lines are left out. With the plies separate, the default, the `stack-up` block
lists every ply and every resin fill on a line of its own ([Board](Board.md#1212-plies-separate)):

```text
rf_module  (rf_module.kicad_pcb)   generated 2026-11-06 09:17
mode: simulation   formats: glb, stl, obj   units: m
KiCad format 20221018 (KiCad 7), generator pcbnew

stack-up   built: PLIES_FUSED (parameters/PCB_elements/Stackup.py)
  lines built: top_silkscreen, top_solder_mask, top_finish, top_copper, board, resin_between_traces, inner_copper, bottom_copper, bottom_finish, bottom_solder_mask, bottom_silkscreen, plated_holes, hole_finish, via_resin
  lines left out: none
  copper layers: F.Cu, In1.Cu, In2.Cu, B.Cu
  laminate 1.5300 mm (stackup dielectrics (+ inner copper); board total in file 1.6 mm)
  F.Cu     z +0.7650 .. +0.8000 mm  (foil 0.035 mm)
  In1.Cu   z +0.5475 .. +0.5650 mm  (foil 0.0175 mm)
  In2.Cu   z -0.5650 .. -0.5475 mm  (foil 0.0175 mm)
  B.Cu     z -0.8000 .. -0.7650 mm  (foil 0.035 mm)
  dielectric 1             prepreg  FR4        0.2000 mm  er 4.5  tan d 0.02   z +0.5650 .. +0.7650
  dielectric 2             core     FR4        1.0950 mm  er 4.5  tan d 0.02   z -0.5475 .. +0.5475
  dielectric 3             prepreg  FR4        0.2000 mm  er 4.5  tan d 0.02   z -0.7650 .. -0.5650
  vias: plot setting viasonmask; pad-to-mask clearance 0.05 mm; silkscreen over copper (mask openings): False
  origin: outline centre (132.0000, 122.0000) in KiCad coordinates

read
       9  arc tracks on B.Cu
       8  arc tracks on F.Cu
       8  arc tracks on In1.Cu
       8  arc tracks on In2.Cu
       1  edge plating band (net GND)
       2  footprint graphics on B.SilkS
      37  footprint graphics on F.SilkS
      46  footprints
       1  graphics on B.Cu
      18  graphics on B.Mask
       5  graphics on B.SilkS
      23  graphics on F.Mask
       1  graphics on F.SilkS
      16  outline shapes on Edge.Cuts
      18  pad mask openings on B.Mask
     154  pad mask openings on F.Mask
     162  pads
       1  text on B.Cu
      11  text on B.SilkS
       1  text on F.Cu
      46  text on F.SilkS
       1  text on In1.Cu
       1  text on In2.Cu
     307  through vias
      30  tracks on B.Cu
     144  tracks on F.Cu
       8  tracks on In1.Cu
       8  tracks on In2.Cu
       1  zone fills on B.Cu
       3  zone fills on F.Cu
       1  zone fills on In1.Cu
       2  zone fills on In2.Cu
skipped
       3  keepout / rule areas (no copper by design)

notes
  font: KiCad newstroke (kicad_newstroke.json.gz)
  solder mask: 0.01 mm over laminate, 0.01 mm over copper (stackup)
  finish: ENIG Nickel 0.005 mm + Gold 8e-05 mm
  finish: also on the plated edge (Gold 8e-05 mm drawn 0.0001 mm thick across the edge, the snapping grid)
  ...

parts
  Board_dielectric 1                      53960 triangles  material Board_prepreg #A89C66 alpha 1.0
  Board_dielectric 2                      43812 triangles  material Board_core #968A58 alpha 1.0
  Board_dielectric 3                      88468 triangles  material Board_prepreg #A89C66 alpha 1.0
  Copper_+3V3                             40400 triangles  material Copper #CD803E alpha 1.0
  ...
  Top Solder Mask                        154968 triangles  material Top Solder Mask #14328C alpha 0.8
  Bottom Solder Mask                      75038 triangles  material Bottom Solder Mask #14328C alpha 0.8
  Top Silkscreen                          40466 triangles  material Top Silkscreen #F0F0EC alpha 1.0
  Bottom Silkscreen                       15824 triangles  material Bottom Silkscreen #F0F0EC alpha 1.0
  Top Finish Gold                        111594 triangles  material Gold #E6C15A alpha 1.0
  ...

timing
  read              0.0667 s
  collect           0.1691 s
  resolve           1.5408 s
  geometry          6.0711 s
  materials         0.0004 s
  assemble          5.3236 s
  write             7.5092 s
  verify            0.5813 s

Verifier: PASS
  ...
```

| Section | Content |
|---|---|
| header | board, file, time of the run, mode, formats, units, KiCad format and generator, the title from the title block |
| warnings | the warnings from reading the file, if any |
| `stack-up` | the stack-up built (`PLIES_FUSED` or `PLIES_SEPARATE`) with the lines built and the lines left out, laminate thickness and its source, the z band and foil of every copper layer, every dielectric with type, material, thickness, εr, tanδ and z range (with the plies fused, under a gap of several plies a `fused from` line for each; with the plies separate, a line for each ply and each resin fill), the via tenting source, the pad-to-mask clearance, the silk-over-copper setting, the origin used |
| `read` | a count of every kind of item read from the file (non-plated holes are counted here even when `Board.INCLUDE_NON_PLATED_HOLES = False` leaves them out) |
| `skipped` | a count of the items left out, with the reason (hidden text and text on layers that are not drawn are left out without a count) |
| `notes` | the font, the mask thickness and its source, finish, resin fill, castellation and edge plating notes, warnings raised while building (in the parts' order, however many worker processes ran), and the notes when worker processes failed and fewer processes, or the main process, did the parts left |
| `parts` | every part with its triangle count, material key, colour and alpha |
| `timing` | seconds per stage, to 0.1 ms (verify only when the Verifier ran) |
| Verifier | unless `--no-verify` or `Verifier.VERIFY = False` leaves it out; see [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md) |

## 11.3 Part Names

The GLB node, the STEP solid and the `materials.json` key carry the part name exactly. The STL
file name and the OBJ object and material names carry it sanitised (the rule in section 11.2.1).

| Role | Names |
|---|---|
| board | `Board_dielectric 1`, `Board_dielectric 2`, ... or `Board`; a gap of several stack-up dielectrics: `Board_dielectric 1 + dielectric 2`. With the plies separate: `Board_dielectric 1 ply 1`, `Board_dielectric 1 ply 2` for the plies of a gap, `Board_dielectric 2` for a core or a gap of one ply, `Board_dielectric 3 ply 2-3` for equal plies joined, and `Board_resin In1.Cu` for the resin beside an inner copper layer |
| copper | `Copper_<net>` (`Copper_GND`, `Copper_no_net`, `Copper_~{RESET}`), or `Copper_F.Cu` ... and `Plating`, or `Copper` |
| via resin | `Via Resin`: the plugs and resin fills of KiCad 10's protected vias |
| mask | `Top Solder Mask`, `Bottom Solder Mask`; visual mode also `Top Mask over Copper`, `Bottom Mask over Copper` |
| silk | `Top Silkscreen`, `Bottom Silkscreen` |
| finish | `Top Finish Nickel`, `Bottom Finish Gold`, `Edge Finish Nickel` (plated edge, castellations, inner copper cut by the edge), `Hole Finish Gold` (inside the plated holes), or `Top Finish Gold_<net>` |

Net names are used as KiCad shows them: the escapes KiCad stores for characters a net name cannot
hold (`{slash}`, `{colon}`, `{dblquote}` and the rest of KiCad's `UnescapeString`) are turned back
into those characters, and markup such as `~{RESET}` is kept as written. Names with characters
such as `~{RESET}`, `/SDA` or `Net-(R1-Pad2)` therefore give STL and OBJ names that differ from
the part name (`Copper__RESET`, `Copper__SDA`, `Copper_Net-_R1-Pad2`: letters of any script,
digits and `_ . + -` are kept, every other run of characters becomes one `_`). `materials.json`
gives the STL name under `file_names.stl`, built with the same rule, so it always matches the file
on disk.

Two part names that sanitise to the same string (for example nets `/SDA` and `~{SDA}`, or
`VCC(3V3)` and `VCC_3V3`) get a counter on the second, `Copper__SDA_2`, compared without regard to
case as Windows and macOS file systems do, so no file replaces another.

## 11.4 Tests Output

`tests/test_boards.py` writes its runs to `tests/out/`, which is deleted at the start of every
test run and ignored by git. `tests/test_layout.py`, `tests/test_colors.py`,
`tests/test_kicad_version.py`, `tests/test_stackup_lines.py`, `tests/test_parameters.py`,
`tests/test_plies.py`, `tests/test_material_models.py`, `tests/test_verifier.py`,
`tests/test_boundary.py`, `tests/test_copper_union.py`, `tests/test_finish_shells.py`,
`tests/test_mask.py`, `tests/test_pairs.py`, `tests/test_hatch.py`, `tests/test_machining.py`,
`tests/test_tall_walls.py`, `tests/test_via_protection.py` and `tests/test_threads.py` write nothing, and
`tests/test_step_native.py`, `tests/test_step_arcs.py`, `tests/test_text_layout.py`, `tests/test_font.py`,
`tests/test_text_vars.py`, `tests/test_bad_input.py`, `tests/test_same_result.py`, `tests/test_workers.py`,
`tests/test_plies_built.py`, `tests/test_defaults.py` and `tests/test_full_disk.py` write only in a temporary folder that they remove.

| Previous | Next |
|:---|---:|
| [Choosing An Export](Choosing-An-Export.md) | [Board](Board.md) |
