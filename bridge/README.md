# The bridge

The bridge takes a KiCad board into a PyPEEC simulation and reads the answer back. It is general: nothing in it names a board, a coil or an example. Every example under [`../Examples`](../Examples) imports it, and adds only what belongs to its own board: which nets are coils, where each coil is opened for its terminals, what to sweep, and what to compare the answer with.

KESE stays a geometry exporter. The bridge runs it as a program and reads what it writes; it changes nothing in KESE.

[PyPEEC](https://github.com/otvam/pypeec) (MPL-2.0, by Thomas Guillod) solves the magneto-quasi-static field with the PEEC method: only the copper carries unknowns, drawn as voxels on a uniform grid, the air needs no mesh at all, and the couplings between voxels are products with FFTs over the grid.

## What happens to a board

1. **Export** (`study.kese_geometry` or `study.kese_export`, `geometry.run_kese`): KESE exports the `.kicad_pcb`, as one STL per solid and a `materials.json`, plus a STEP and its report. `kese_geometry` keeps the export in a folder of its own, meant to be committed beside the board (the coil examples use `3D_Geometry/`), with a `source.json` holding the board file's hash; `kese_export` keeps it in a scratch cache named by that hash. Either way an unchanged board is not exported twice. The export is the same as the Elmer branch's (KESE's `elmer` preset: its simulation mode, STL and `materials.json`), so the two branches solve the same copper.
2. **Parts** (`geometry.load_parts`): each solid becomes a part in model coordinates (x and y as KiCad's with y up, z = 0 at the top of the top copper), named by its net or its role. A board can be flipped copper side down, moved up by an air gap and turned about an axis the caller gives: that is how a rotor is placed over a stator.
3. **Layers** (`layers.Layout`): the model is cut into slabs at every height any part has, and each part is sectioned in the middle of each slab. FR-4 and solder mask are left out: to a magneto-quasi-static solve an insulator with μr 1 is air.
4. **Voxels** (`voxels.build`): every conductor drawn onto one uniform grid, d in the board's plane (50 µm on the coil boards) and dz through it. A voxel is copper when its centre lies in the part's section. The grid's z follows the copper: each copper sheet is one voxel thick (or `n_cu`), centred on its own height, and dz (close to the copper's 35 µm) is chosen so that the distance between any two sheets is a whole number of voxels to within a micron or so. Each sheet's resistivity is scaled by its voxels' thickness over the copper's, so it keeps its sheet resistance. A via's barrel is drawn as a solid column of its outer diameter.
5. **Ports** (`ports`): each coil is opened at a gap (a cut across a trace, a via left out, or two trace ends stacked on two layers). Its two terminals are its voxels that share a face with the gap, one group each side, as the Elmer branch's electrodes are the copper faces that border the gap.
6. **Case and solve** (`pypeec_case`, `study.solve`): every coil gets a current source on its first terminal (1 A in the driven coil, 0 A in a receiver, whose voltage is then its open-circuit EMF) and a 0 V source on its second. A conductor with no terminals (a rotor) carries eddy currents only; one of its voxels is held at 0 V, as PyPEEC needs a source on every piece of copper, and no current can flow through it. PyPEEC's mesher (here only its checks: every coil in one piece, no two conductors touching) and solver run in a process of their own, so the peak memory is measured. The bridge reads back each coil's V, I and impedance, so L, R and the mutual inductance M of each receiver, plus the stored energy and the losses, the iterative solver's iterations and residual, PyPEEC's own checks, the peak memory and the time.

## The modules

| File | What it does | Called as |
|---|---|---|
| [`geometry.py`](geometry.py) | runs KESE, reads its solids and `materials.json`, places them (the Elmer branch's, unchanged but for where `Part` comes from) | `run_kese`, `load_parts`, `copper_top` |
| [`layers.py`](layers.py) | the parts, their sections and the slabs they make (the Elmer branch's `mesh25d.py` without the mesh) | `Part`, `Layout`, `section` |
| [`voxels.py`](voxels.py) | the grid and every conductor drawn onto it | `Grid`, `build`, `choose_dz`, `copper_sheets` |
| [`ports.py`](ports.py) | where a coil is opened and its two terminals | `cut`, `terminals`, `groups` |
| [`pypeec_case.py`](pypeec_case.py) | PyPEEC's input (geometry and problem), running it, each coil's V, I, Z and M | `Coil`, `Case`, `inputs`, `run`, `coil_results` |
| [`study.py`](study.py) | a study: KESE's export (kept or cached), one solve per frequency, the numbers back, the versions used | `kese_geometry`, `kese_export`, `solve`, `versions` |
| [`tolerance.yaml`](tolerance.yaml) | PyPEEC's own default tolerances (MPL-2.0, from its examples), unchanged | read by `pypeec_case.tolerance` |
| [`setup_machine.sh`](setup_machine.sh) | a fresh Ubuntu machine: `.venv` with the packages of `requirements.txt` | `bash bridge/setup_machine.sh` |

## Using it

An example's `simulation.py` puts the branch on its path and imports the modules:

```python
import json
from bridge import geometry as G, layers as L, ports as P, pypeec_case as C, study as S, voxels as V

export = S.kese_export('board.kicad_pcb', 'case/kese')                  # KESE, cached
mats = json.loads((export / 'materials.json').read_text())
parts, _ = G.load_parts(export, z_shift=-G.copper_top(mats))              # z = 0 at the top copper
lay = L.Layout(parts).build(insulators=False)                             # the slabs and sections
grid, vox = V.build(lay, 0.05, copper_mm=0.035)                           # 50 um voxels in the plane
t1, t2 = P.terminals(grid, vox, 'LOOP', gap, -0.035, 0.0)                 # where the coil is opened
case = C.Case(grid=grid, vox=vox, coils=[C.Coil('LOOP', 'LOOP', t1, t2, 1.0)])
rows = S.solve(case, [3.5e6], 'case/run')                                 # L, R, M, residual, memory, time
```

[`../Examples/E01_circular_loop/simulation.py`](../Examples/E01_circular_loop/simulation.py) is the shortest complete one. The inductive coils' [`simulation.py`](../Examples/Inductive%20Coils/S0_1x_OD21_2L_tiny/PyPEEC%20Simulation/simulation.py) adds a rotor turned to each angle.

## What it needs

* KESE, only to export a board whose `3D_Geometry/` is not committed: its `Generator/` copied into [`../3D_Geometry`](../3D_Geometry) from `main`, or its path in `KESE_PATH`.
* PyPEEC and the other Python packages in [`../requirements.txt`](../requirements.txt): see [`../Solver_PyPEEC`](../Solver_PyPEEC). PyPEEC is pure Python and runs on Linux, Windows and macOS.

## Where it stops

* **Boards, not arbitrary 3D.** The voxels follow a layered stack, flat at a few heights, which every KiCad board is. A board over another (a rotor over a stator) works; a part tilted out of the board's plane does not.
* **A uniform grid.** Every voxel is the same size, so the grid's height runs from the lowest copper to the highest in steps of about the copper's thickness, and its cost grows with the air gap. A wide board with fine traces needs many voxels: a 0.2 mm trace is only 4 voxels across at 50 µm, and its edges are drawn as steps.
* **One voxel through the copper.** With `n_cu` 1 the current is uniform through each sheet's thickness, so the skin effect through the 35 µm copper (whose skin depth at 3.5 MHz is about the same) is not resolved; the crowding to the traces' edges is, as far as the voxels across a trace allow. `n_cu` 2 halves dz and doubles the layers.
* **Magnetic, harmonic.** Inductance, resistance, mutual inductance and eddy currents at a given frequency. No capacitance (PyPEEC has no charges on the surfaces), temperature or stress.
* **The caller places the ports.** The bridge does not guess where a coil is opened; each example says so (S0's `test_spec.json` holds it for the coil boards).

## Licence

GPL-3.0, as the rest of this branch's code (see [`../LICENSE`](../LICENSE)). `tolerance.yaml` is PyPEEC's, MPL-2.0, as its header says.
