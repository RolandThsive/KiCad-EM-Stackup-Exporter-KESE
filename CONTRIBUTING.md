# Contributing to KESE

Contributions of every kind are welcome: code, bug reports, test boards,
documentation and research.

KESE is licensed under the GNU General Public License, version 3 or later
(see [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md)). By submitting a
contribution, you agree that it is licensed under those same terms, and you
confirm that you have the right to submit it. You keep the copyright in your
contribution.

If your contribution includes or is derived from someone else's work, such as
code from KiCad, say where it comes from and keep its copyright notice, and
make sure its license is compatible with GPL-3.0-or-later.

## How the code is laid out

All of KESE lives in `Generator/`: the `kese/` package, the settings in `parameters/`, the
tests in `tests/`, `run_KESE.py`, `pyproject.toml` and `requirements.txt`, and the `Input/` and
`Output/` folders. The repository root keeps only what belongs to the repository: the README,
the licence files, `docs/`, `.github/` and the feature test boards in `featureTest/`. The paths
below are inside `Generator/`.

`kese/pipeline.py` runs nine stages in order, one folder each in `kese/`. Each stage takes what
the stage before it made and hands its own result to the next:

| Stage | Takes | Makes |
|---|---|---|
| `s1_read` | the `.kicad_pcb` file | `RawBoard`: the parsed tree, checked |
| `s2_collect` | `RawBoard` | `Items`: every item as a flat shape on its layer, with its net |
| `s3_resolve` | `Items` | `Regions`: 2D regions per layer and net, holes applied |
| `s4_geometry` | `Regions` | `PrismSet`: flat regions between two heights |
| `s5_materials` | `PrismSet` | the same, with a material for every part |
| `s6_assemble` | `PrismSet` | `Model`: meshes in output units and orientation |
| `s7_write` | `Model` | `Files`: GLB, OBJ, STL, STEP, `materials.json` |
| `s8_verify` | `Files` | the same, with the Verifier's result (opt-in) |
| `s9_report` | `Files` | `report.txt` and `parameters.txt` |

Below the stages, `kese/core/` holds the tools that know nothing about stages (parser, 2D shapes,
extrusion, stroke font) and `kese/model/` holds the data classes named in the table. Every
setting lives in `parameters/`, in three folders: `PCB_elements/` (what the board is made of:
`Stackup.py` says which parts are built, and `Board.py`, `Copper.py`, `Finish.py`, `SolderMask.py`
and `SilkScreen.py` hold one element each), `Run_KESE/` (how KESE runs) and `Fileformats/` (the
files it writes). `parameters/__init__.py` loads them, and `kese/settings_check.py` checks every
value before a run starts.

These rules keep each piece small and the flow one way:

1. **Forward only.** A stage imports only `core/`, `model/`, `parameters/` and stages with a
   smaller number.
2. **Shared layers stay below.** `core/` imports only `core/` and `parameters/`; `model/`
   imports only `model/` and holds data classes only.
3. **One entry per stage.** Each stage has one `run(previous_result, job)`, in its entry file
   (`read.py`, `collect.py`, `resolve.py`, ...), and `kese/pipeline.py` calls them in order.
4. **No cycles inside a stage.** Files in a stage import each other in one direction only.
5. **No file in `kese/` over 200 lines.** A file that grows past it is split by concern. The one
   exception is `kese/s1_read/parse_kicad_version.py`, allowed 500, which holds every rule that
   depends on the KiCad version.
6. **One concern per file.** One kind of KiCad item per collect file, one output format per
   write file, one check per verify file.
7. **One naming style.** Lowercase module and folder names (PEP 8), CamelCase for data classes.
   The parameter files are the one exception: each is named as its module is in `--set` and in
   the code (`Copper.py` holds `Copper.VIA_WALL_MM`, read as `P.Copper.VIA_WALL_MM`), and their
   folders are `PCB_elements/`, `Run_KESE/` and `Fileformats/`.
8. **KESE stays in `Generator/`.** No Python or TOML file anywhere else in the repository.
9. **Version rules in one place.** No file but `kese/s1_read/parse_kicad_version.py` tests a KiCad
   file format number or release; the others ask it.
10. **A thread makes shapes only from its own.** Code that runs in threads (`in_parallel`, a
    `ThreadPoolExecutor`) takes `own()` copies (`kese/core/shape_copies.py`) of every shape another
    thread may use at the same time, before it makes anything from it. GEOS 3.14 counts the shapes
    of each of its factories without a lock, and a shape on the grid shares its factory with every
    shape made from it: two threads making shapes from one shared shape can crash the run. Where
    the grid is not used (coordinates read, a coverage union), `floating()` copies are cheaper and
    may be shared. On GEOS 3.15 or newer both return the shapes themselves. A prepared shape is
    used by one thread at a time.

`tests/test_layout.py` checks every rule except the sixth and the tenth, which need a person's
judgement. It also checks that `parameters/` holds exactly its thirteen files, each named as its
module.

Where new work goes:

- A new kind of KiCad item: a file in `s2_collect/`, called from `collect.py`.
- A new output format: a file in `s7_write/`, called from `write.py`, and its name added to
  `FORMATS` in `kese/job.py`.
- A new check: a file in `s8_verify/`, called from `verify.py`.
- A new setting: in the matching `parameters/` file, in the section of that file it belongs to
  (Parts, Thickness, Shape, Material, Color). `parameters.txt` lists it by itself, and
  `kese/settings_check.py` checks its kind by itself; give it a range there if it has one.
- A new part that can be left out: a line in both stack-ups of `parameters/PCB_elements/Stackup.py`,
  in `LINES` of `parameters/__init__.py`, and in `kese/s4_geometry/switches.py`, which says which
  lines a prism needs.
- A setting that is renamed or moved: an entry in `MOVED` of `parameters/__init__.py`, so that its
  old name still works in `--set` and in a preset, and a line in `tests/settings_before_25_2.txt`
  stays true.

## Before a pull request

```bash
cd Generator
python tests/test_layout.py      # the layout rules, about a second
python tests/test_colors.py      # stack-up colours: named, user-defined and unknown
python tests/test_text_layout.py # text laid out where KiCad 7.0.11 plots it
python tests/test_font.py        # the stroke font glyph by glyph, custom fonts, TrueType faces
python tests/test_text_vars.py   # variables inside variables, as each KiCad version expands them
python tests/test_kicad_version.py # the rules of each KiCad version and the file's tokens, against KiCad's own parser
python tests/test_stackup_lines.py # each line of Stackup.py leaves out or builds its own parts and nothing else, in both stack-ups
python tests/test_parameters.py  # every setting of before 25.2 still has a home; old files and old names refused or carried over
python tests/test_plies.py       # the plies of the board file: sub-layers, frequency and model, plies by hand, fused or built apart
python tests/test_plies_built.py # the laminate ply by ply: a real four-layer build, the same volume as fused, materials.json
python tests/test_material_models.py # Djordjevic-Sarkar as KiCad fits it, the table, copper roughness, copper by top, inner and bottom
python tests/test_bad_input.py   # wrong settings and damaged files: an error or a warning, not a crash
python tests/test_threads.py     # threads: their own copies of shapes, one prepared slice, the skin's probes and meshes, memory
python tests/test_workers.py     # worker processes: shapes and settings reach them, caps, lost workers, errors, ending
python tests/test_same_result.py # the work in batches or processes of any size gives the same result, to the byte
python tests/test_verifier.py    # the Verifier: the visual check upright and flat, on 32-bit Python, at loose faces; checks in the workers; overlaps in threads
python tests/test_boundary.py    # stage 6's shortcuts give what the long way gives, and parts close
python tests/test_tall_walls.py  # walls joined across the heights only a counterbore, a countersink or a plug brings
python tests/test_copper_union.py # a net's copper joined with no crack and no burr past the edge
python tests/test_finish_shells.py # the finish's air cut bore by bore, as the whole board's union cuts it
python tests/test_mask.py        # no slivers of mask on the copper where an opening follows a pad's edge: the finish covers them
python tests/test_hatch.py       # KiCad 10's hatched fills, against what KiCad 10 itself draws
python tests/test_machining.py   # KiCad 10's backdrills, counterbores and countersinks, against KiCad 10 and the cone
python tests/test_via_protection.py # KiCad 10's via covering, plugging, capping and filling, as the file and the board say
python tests/test_pairs.py       # pieces within a distance of each other, as an STRtree finds them; a tree threads share
python tests/test_degenerate_shapes.py # shapes of no area, cracks thinner than a grid step and openings a micrometre across
python tests/test_full_disk.py   # a full disk leaves no half-written file; runs at once, a folder each
python tests/test_step_native.py # a solid written from its faces, read back by OpenCascade
python tests/test_step_arcs.py   # true arcs and cylinders in STEP (Step.STEP_EXACT_ARCS), read back too
python tests/test_boards.py      # every test board through both modes, against tests/baseline.json
```

`python -m pytest tests` runs all thirty. When a change is meant to move the geometry, re-record the
baseline with `python tests/test_boards.py --accept` and say why in the pull request; a new board is
recorded with `python tests/test_boards.py --add`, which leaves the others as they are. What several test
files share (the folders, settings changed for a block, a board run through the first stages, the plain
`python tests/test_x.py` run) is in `tests/helpers.py`.
