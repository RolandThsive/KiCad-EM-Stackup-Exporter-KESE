# 3. Getting Started

KESE is a pure Python program. It reads the `.kicad_pcb` text file itself, so KiCad does not need
to be installed on the machine that runs it. With the versions pinned in `requirements.txt` it
needs Python 3.12 or later: `numpy` 2.5.3 and `scipy` 1.18.1 require it. On Python 3.11, install
the same packages without the pinned versions (`python -m pip install numpy scipy ...`) and pip
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
| `numpy`, `scipy`, `networkx` | Numerics and the mesh libraries' dependencies |
| `shapely` | All 2D geometry: tracks, pads, zones, outline, mask, silk, and the faces of every solid |
| `mapbox_earcut`, `manifold3d` | Cutting the faces into triangles: earcut, and Manifold's triangulator where earcut's triangles do not close on the edges |
| `trimesh`, `rtree` | The meshes, GLB and STL export, and the Verifier's ray tests (KESE writes OBJ and STEP itself) |
| `cadquery`, `cadquery-ocp` | Optional: only for `Run.BUILD_WITH_KERNELS = True`, the older way that joins the solids with Manifold and builds the STEP file with OpenCascade, and for the tests that read STEP files back |

KESE writes STEP itself, so every format works without `cadquery`. Only a run with
`Run.BUILD_WITH_KERNELS = True` that asks for STEP needs it, and stops with a message that names
the missing package. The program checks the packages before it starts and prints the
`pip install` line to run, instead of a traceback.

Or install the project itself through `pyproject.toml`, with the packages unpinned (it also
accepts Python 3.11, which is not tested):

```bash
python -m pip install -e .            # the kese command, the same as python run_KESE.py
python -m pip install -e ".[step]"    # the same, with cadquery (Run.BUILD_WITH_KERNELS)
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
   hdi_module: KiCad format 20221018, 6 copper layers, mode simulation
     -> Output/hdi_module/simulation_GLB  (hdi_module.glb, materials.json)  in 0m 12s
   pcie_card: KiCad format 20221018, 4 copper layers, mode simulation
     -> Output/pcie_card/simulation_GLB  (pcie_card.glb, materials.json)  in 0m 14s
   rf_module: KiCad format 20221018, 4 copper layers, mode simulation
     -> Output/rf_module/simulation_GLB  (rf_module.glb, materials.json)  in 0m 16s
   ```

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
python run_KESE.py board.kicad_pcb --for hfss        # a preset: hfss, cst, openems or viewer
python run_KESE.py board.kicad_pcb --verify          # run the Verifier; results in report.txt
python run_KESE.py board.kicad_pcb --out /some/dir   # output root other than Output/
python run_KESE.py board.kicad_pcb --set Copper.VIA_WALL_MM=0.02 --set Board.BOARD_THICKNESS_MM=0.8
python run_KESE.py --version
```

| Option | Meaning |
|---|---|
| `boards` | One or more `.kicad_pcb` paths. With none, every board in `Run.INPUT_DIR` (`Input/`) is exported. |
| `--mode` | `simulation` or `visual`. The old names `real` and `pretty` are still accepted. Default: `Run.MODE`. |
| `--format` | Any of `glb`, `stl`, `obj`, `step`, several at once. Default: `Run.FILE_FORMAT` (`["glb"]`). Visual mode allows only `glb` and `obj`. |
| `--for` | Applies a preset from `Run.PRESETS` before any `--set`: `hfss`, `cst`, `openems`, `viewer`. See [Choosing An Export](Choosing-An-Export.md). |
| `--verify` | Runs the Verifier after the model files are written (2 to 4 s on the example boards). See [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md). |
| `--out` | Output root. Default: `Run.OUTPUT_DIR` (`Output/`). |
| `--set Module.NAME=value` | Overrides one parameter for this run. `Module` is the short name of the parameter file (`Run`, `Board`, `Copper`, `SolderMask`, `Silkscreen`, `Finish`, `Geometry`, `Color`). The value is parsed as a Python literal (`0.02`, `True`); anything that does not parse, such as `net`, is kept as a string. Quote a list for the shell, as in `--set 'Run.FILE_FORMAT=["glb","stl"]'`: unquoted, the shell strips its inner quotes and the run stops. An unknown name stops the run. |
| `--version` | Prints `kese 2.2.0`. |

Every preset, `--set`, `--mode`, `--format` and `--verify` is applied as an override of the
parameters (`--mode` sets `Run.MODE`, `--format` sets `Run.FILE_FORMAT`, `--verify` sets
`Run.VERIFY`), so all of them are listed on the first line of the run's `parameters.txt` and show
in its values. Only `--out` is not recorded there; the run folder's path shows it.

> [!NOTE]
> Run the program from the `Generator/` folder: `Input/` and `Output/` (`Run.INPUT_DIR`,
> `Run.OUTPUT_DIR`) are relative to the folder the command is run from. The
> exit code is 0 when every board succeeded and 1 when any board failed; with a single board the
> full traceback is shown, with several the failing board is reported and the run continues.

## 3.4 What Happens In A Run

1. **Read.** The `.kicad_pcb` is parsed; the KiCad format version, the copper layers and the
   board thickness are taken from it. Formats outside KiCad 6 to 10 give a warning, not an error.
2. **Collect.** Tracks, arcs, vias, pads, zone fills, graphics and text are collected per layer
   and per net; the stack-up is read from Board Setup or built from the defaults.
3. **Resolve.** The outline is built from `Edge.Cuts`; the copper of every layer and net is
   joined, clipped to the outline and drilled; plating, mask openings and silkscreen follow.
4. **Geometry.** Every layer becomes flat regions between two heights: dielectrics, copper per
   net, via barrels, solder mask, silkscreen and, if enabled, the surface finish.
5. **Materials.** Each part gets a material from `parameters/color.py` (or the stack-up's colour
   names).
6. **Assemble.** In simulation mode the surface of every part is worked out in 2D, height by
   height: the faces looking up and down at each height and the walls between them, cut into
   triangles. Each part comes out as closed solids without any 3D boolean operation (pieces that
   do not touch, such as silkscreen letters, stay separate bodies in the part). In visual mode
   only the surface that can be seen is kept, found the same way for all parts at once.
7. **Write.** The requested model files are written, with `materials.json` next to them.
8. **Verify** (only with `--verify` or `Run.VERIFY = True`), on the model just written; the GLB
   file also goes through `gltf_validator` when that tool is on the PATH.
9. **Report.** `parameters.txt` and `report.txt` are written last, so the report carries the
   Verifier's result.

The stages are described in [Working Principle](Working-Principle.md). While a board runs, a
live `running <stage> ... 1m 23s` line shows the current stage on a terminal
(`Run.SHOW_PROGRESS`).

## 3.5 Next

- Decide what to export for your solver: [Choosing An Export](Choosing-An-Export.md).
- Set your fabricator's thicknesses: [Parameter Reference](Parameter-Reference.md).
- See what the model contains: [Board](Board.md) and [Copper And Traces](Copper-And-Traces.md).

| Previous | Next |
|:---|---:|
| [Contents](Contents.md) | [Project Capabilities](Project-Capabilities.md) |
