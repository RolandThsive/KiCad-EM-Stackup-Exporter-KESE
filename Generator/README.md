# KESE

This folder is KiCad EM Stackup Exporter (KESE) itself: the program, its settings, its tests and
the boards it reads and writes. The rest of the repository is its documentation and licences.
What KESE does, its examples and its licence are in the [main README](../README.md).

| Path | What It Is |
|---|---|
| `run_KESE.py` | Runs KESE from this folder without installing it |
| `kese/` | The program: nine stages that run in order, plus `core/` and `model/` |
| `parameters/` | Every setting (the only files you edit), in three folders: `PCB_elements/` for what the board is made of, with `Stackup.py` saying which parts are built, `Run_KESE/` for how KESE runs, and `Fileformats/` for the files it writes |
| `Input/` | Boards to export (three examples included) |
| `Output/` | One folder per board and run |
| `tests/` | The layout rules, the regression suite with its test boards and baseline, the other tests, and `feature_boards/`, which makes the boards in `featureTest/` |
| `tools/` | Scripts for the repository itself: `make_swatches.py` makes the wiki's colour boxes, `font_lines.py` rewrites a stroke font as JSON Lines, a glyph per line |
| `pyproject.toml`, `requirements.txt` | The package, and the Python packages it was tested with |

## Quick Start

```bash
cd Generator
python -m pip install -r requirements.txt     # Python 3.12 or later
python run_KESE.py                            # Every board in Input/, settings from parameters/
python run_KESE.py --help                     # Every option
```

Run the commands from this folder: `Input/` and `Output/` are found from the folder you run in.
`python -m pip install .` here gives a `kese` command that works from any folder.
