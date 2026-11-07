# 3. Getting Started

KESE is a pure Python program. It reads the `.kicad_pcb` text file itself, so KiCad does not need
to be installed on the machine that runs it. With the versions pinned in `requirements.txt` it
needs Python 3.12 or later: `numpy` 2.5.3 requires it. On Python 3.11, install
the same packages without the pinned versions (`python -m pip install numpy shapely mapbox_earcut`) and pip
picks the last versions built for 3.11, as `requirements.txt` explains.

![The 4-layer RF sensor module from Input/ turning in simulation mode, so that its top and its bottom come round in turn: the blue solder mask translucent over the copper, the planes and tracks showing through it, and the plated board edge and the walls of the cut-out in copper colour](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/start_1_simulation.webp)

## 3.1 Install

```bash
git clone https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE.git
cd KiCad-EM-Stackup-Exporter-KESE/Generator
python -m pip install -r requirements.txt
```

`Generator/` holds everything KESE is made of: the program, its settings, `Input/`, `Output/` and
the tests. Every command on this page runs from there.

`requirements.txt` pins the versions the project was tested with (Python 3.13 on Linux). The
packages are:

| Package | Used for |
|---|---|
| `numpy` | Numerics, and the meshes: KESE builds them, writes GLB, STL, OBJ and STEP, and casts the Verifier's rays itself |
| `shapely` | All 2D geometry: tracks, pads, zones, outline, mask, silk, and the faces of every solid |
| `mapbox_earcut` | Cutting the faces into triangles (GEOS's constrained Delaunay triangulation, through `shapely`, where earcut's triangles do not close on the edges) |

KESE writes every format itself, STEP included, with no CAD kernel. The program checks the
packages before it starts and prints the `pip install` line to run, instead of a traceback. Only
the tests that read STEP files back use OpenCascade, 7.8 by preference
([Compatibility](Compatibility.md#214-python-and-packages)), and they skip that check without it:

```bash
python -m pip install "cadquery-ocp==7.8.1.1.post1"
```

Or install the project itself through `pyproject.toml`, with the packages unpinned (it also
accepts Python 3.11, which is not tested):

```bash
python -m pip install -e .            # the kese command, the same as python run_KESE.py
```

`-e` keeps `parameters/` editable in place. `Input/` and `Output/` stay relative to the folder
the command is run from.

## 3.2 First Run

1. Put a board file in `Input/`, or use one of the three example boards already there (see
   [Examples](Examples.md)). Make sure every copper zone in the board has been filled in KiCad
   (press **B**) and the file saved: KESE takes the zone fill polygons stored in the file, and a
   zone without a stored fill produces no copper.
2. Run the default export: every board in `Input/`, simulation mode, one GLB in metres with
   the board centred at the origin:

   ```bash
   python run_KESE.py
   ```

3. Read the terminal. For each board it prints the KiCad format version, the number of copper
   layers, the mode, any warnings, and the output folder:

   ```text
   hdi_module: KiCad format 20221018 (KiCad 7), 6 copper layers, mode simulation
     -> Output/hdi_module/simulation_GLB  (hdi_module.glb, materials.json)  in 0m 09s
   pcie_card: KiCad format 20221018 (KiCad 7), 4 copper layers, mode simulation
     -> Output/pcie_card/simulation_GLB  (pcie_card.glb, materials.json)  in 0m 11s
   rf_module: KiCad format 20221018 (KiCad 7), 4 copper layers, mode simulation
     -> Output/rf_module/simulation_GLB__1  (rf_module.glb, materials.json)  in 0m 21s
   ```

   The repository already holds example runs of `rf_module` in `Output/rf_module/`, and a run
   never overwrites a folder, so this board's first run goes to `simulation_GLB__1`.  The three
   simulation examples use the default settings with the finish turned off
   (`--set Finish.FINISH_ENABLED=False`): with the finish, this board's STEP file is over 100 MB,
   more than GitHub takes in one file.  The visual example has the finish, the solder mask and
   the silkscreen on.

4. Open `Output/<board>/simulation_GLB/report.txt`. It lists the stack-up heights, every item that
   was read, every item that was skipped and why (hidden text and text on layers that are not drawn
   are left out without a count), and the triangle count of every part. See
   [Project Output Organization](Project-Output-Organization.md).

5. Bring the model into your solver or viewer: [Choosing An Export](Choosing-An-Export.md) and
   [KiCad And Solver Compatibility](Compatibility.md).

## 3.3 All Commands

```bash
python run_KESE.py                                   # every .kicad_pcb in Input/, settings from parameters/
python run_KESE.py Input/board.kicad_pcb             # one board (several paths are allowed)
python run_KESE.py board.kicad_pcb --mode visual     # simulation (solids) or visual (surface for viewers)
python run_KESE.py board.kicad_pcb --format glb step stl obj --set Run.UNITS=mm   # mm for CAD and solvers
python run_KESE.py board.kicad_pcb --for freecad     # a preset: freecad, elmer, calculix, openems, viewer, blender_glb, blender_obj
python run_KESE.py board.kicad_pcb --verify          # run the Verifier; results in report.txt
python run_KESE.py board.kicad_pcb --out /some/dir   # output root other than Output/
python run_KESE.py board.kicad_pcb --set Copper.VIA_WALL_MM=0.02 --set Board.BOARD_THICKNESS_MM=0.8
python run_KESE.py --version
```

| Option | Meaning |
|---|---|
| `boards` | One or more `.kicad_pcb` paths. With none, every board in `Run.INPUT_DIR` (`Input/`) is exported. |
| `--mode` | `simulation` or `visual`. Default: `Run.MODE`. |
| `--format` | Any of `glb`, `stl`, `obj`, `step`, several at once. Default: `Run.FILE_FORMAT` (`["glb"]`). Visual mode allows only `glb` and `obj`. |
| `--for` | Applies a preset from `parameters/presets.py` before any `--set`: `freecad`, `elmer`, `calculix`, `openems`, `viewer`, `blender_glb`, `blender_obj`. See [Choosing An Export](Choosing-An-Export.md). |
| `--verify` | Runs the Verifier after the model files are written (at most about 1.5 s more on the example boards). See [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md). |
| `--out` | Output root. Default: `Run.OUTPUT_DIR` (`Output/`). |
| `--set Module.NAME=value` | Overrides one parameter for this run. `Module` is the short name of the parameter file (`Run`, `Board`, `Copper`, `SolderMask`, `Silkscreen`, `Finish`, `Geometry`, `Color`, `Parallel`, `Step`, `Verifier`, `Presets`). The value is parsed as a Python literal (`0.02`, `True`); anything that does not parse, such as `net`, is kept as a string (so `false` is the word, and stops the run where the setting takes `True` or `False`). Quote a list for the shell, as in `--set 'Run.FILE_FORMAT=["glb","stl"]'`: unquoted, the shell strips its inner quotes and the run stops. An unknown module or name, or a `--set` without `=`, stops the run before it starts, naming the closest setting ([Checks, Errors And Warnings](Checks-Errors-And-Warnings.md#1811-errors)). |
| `--version` | Prints `kese 2.3.0`. |

Every preset, `--set`, `--mode`, `--format` and `--verify` is applied as an override of the
parameters (`--mode` sets `Run.MODE`, `--format` sets `Run.FILE_FORMAT`, `--verify` sets
`Verifier.VERIFY`), so all of them are listed on the first line of the run's `parameters.txt` and show
in its values. Only `--out` is not recorded there; the run folder's path shows it.

> [!NOTE]
> Run the program from the `Generator/` folder: `Input/` and `Output/` (`Run.INPUT_DIR`,
> `Run.OUTPUT_DIR`) are relative to the folder the command is run from. The
> exit code is 0 when every board succeeded and 1 when any board failed; with a single board the
> full traceback is shown, with several the failing board is reported and the run continues.
> A run works on every processor thread it may use (`Parallel.WORKERS`, see
> [Working Principle](Working-Principle.md#74-work-done-in-parallel)); on a machine short of memory,
> `--set Parallel.PROCESS_WORKERS=1` starts no worker process and keeps the threads, and
> `--set Parallel.WORKERS=1` builds everything in one process, in turn. Ctrl-C stops the run and
> its worker processes with one traceback.

## 3.4 Next

- Decide what to export for your solver: [Choosing An Export](Choosing-An-Export.md).
- Set your fabricator's thicknesses: [Parameter Reference](Parameter-Reference.md).
- See what the model contains: [Board](Board.md) and [Copper And Traces](Copper-And-Traces.md).
- See what happens in a run, stage by stage: [Working Principle](Working-Principle.md).

| Previous | Next |
|:---|---:|
| [Contents](Contents.md) | [Project Capabilities](Project-Capabilities.md) |
