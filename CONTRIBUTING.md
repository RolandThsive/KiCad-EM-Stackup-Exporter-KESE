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
the licence files, `docs/` and `.github/`. The paths below are inside `Generator/`.

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
setting lives in `parameters/`.

These rules keep each piece small and the flow one way:

1. **Forward only.** A stage imports only `core/`, `model/`, `parameters/` and stages with a
   smaller number.
2. **Shared layers stay below.** `core/` imports only `core/` and `parameters/`; `model/`
   imports only `model/` and holds data classes only.
3. **One entry per stage.** Each stage has one `run(previous_result, job)`, in its entry file
   (`read.py`, `collect.py`, `resolve.py`, ...), and `kese/pipeline.py` calls them in order.
4. **No cycles inside a stage.** Files in a stage import each other in one direction only.
5. **No file in `kese/` over 200 lines.** A file that grows past it is split by concern.
6. **One concern per file.** One kind of KiCad item per collect file, one output format per
   write file, one check per verify file.
7. **One naming style.** Lowercase module and folder names (PEP 8), CamelCase for data classes.
8. **KESE stays in `Generator/`.** No Python or TOML file anywhere else in the repository.

`tests/test_layout.py` checks every rule except the sixth, which needs a person's judgement.

Where new work goes:

- A new kind of KiCad item: a file in `s2_collect/`, called from `collect.py`.
- A new output format: a file in `s7_write/`, called from `write.py`, and its name added to
  `FORMATS` in `kese/job.py`.
- A new check: a file in `s8_verify/`, called from `verify.py`.
- A new setting: in the matching `parameters/` file. `parameters.txt` lists it by itself.

## Before a pull request

```bash
cd Generator
python tests/test_layout.py      # the layout rules, about a second
python tests/test_colors.py      # stack-up colours: named, user-defined and unknown
python tests/test_text_layout.py # text laid out where KiCad 7.0.11 plots it
python tests/test_step_native.py # a solid written from its faces, with no kernel, read back by OpenCascade
python tests/test_step_file.py   # a STEP file written part by part against OpenCascade's own
python tests/test_step_kernel.py # a STEP file in metres read back at the right size
python tests/test_step_arcs.py   # true arcs in STEP only where they cannot cross another outline
python tests/test_boards.py      # every test board through both modes, against tests/baseline.json
```

`python -m pytest tests` runs all eight. When a change is meant to move the geometry, re-record the
baseline with `python tests/test_boards.py --accept` and say why in the pull request.
