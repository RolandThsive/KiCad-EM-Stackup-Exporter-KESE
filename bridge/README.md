# The bridge

The bridge takes a KiCad board into an Elmer simulation and reads the answer back. It is general: nothing in it names a board, a coil or an example. Every example under [`../Examples`](../Examples) imports it, and adds only what belongs to its own board: which nets are coils, where each coil is opened for its terminals, what to sweep, and what to compare the answer with.

KESE stays a geometry exporter. The bridge runs it as a program and reads what it writes; it changes nothing in KESE.

## What happens to a board

1. **Export** (`study.kese_geometry` or `study.kese_export`, `geometry.run_kese`): KESE exports the `.kicad_pcb` for Elmer, as one STL per solid and a `materials.json`, plus a STEP and its report. `kese_geometry` keeps the export in a folder of its own, meant to be committed beside the board (the coil examples use `3D_Geometry/`), with a `source.json` holding the board file's hash; `kese_export` keeps it in a scratch cache named by that hash. Either way an unchanged board is not exported twice.
2. **Parts** (`geometry.load_parts`): each solid becomes a part in model coordinates (x and y as KiCad's with y up, z = 0 at the top of the top copper), named by its net or its role. A board can be flipped copper side down, moved up by an air gap and turned about an axis the caller gives: that is how a rotor is placed over a stator.
3. **Mesh** (`mesh25d`): the 2.5D mesh. One triangle mesh holds every copper edge of every layer, and it is swept through the stack as prism (wedge) layers, several through each copper layer so the skin depth is resolved. Tetrahedra fill the air above and below, out to the domain's edge. No 3D Booleans, so 35 µm copper on a 1.6 mm board stays a few hundred thousand nodes.
4. **Ports** (`ports`): each coil is opened at two faces of its copper (the two ends of a cut trace, or the two pads of a left-out via), its electrodes, with a small sheet across the gap between them that pins the voltage.
5. **Case** (`elmer_case`): the Elmer input. Materials, every coil a massive coil of Elmer's circuit module (a fixed current: 1 A in the driven coil, 0 A in a receiver, whose voltage is then its open-circuit EMF), and the linear solver. FR-4 and solder mask are air to this solve; other conductors (a rotor, a shield) carry eddy currents.
6. **Solve and read back** (`study.solve`): one Elmer solve per frequency. It reads back each coil's V, I and impedance, so L, R and the mutual inductance M of each receiver, plus the field energy, the linear solver's iterations and residual, the peak memory and the time.

## The modules

| File | What it does | Called as |
|---|---|---|
| [`geometry.py`](geometry.py) | runs KESE, reads its solids and `materials.json`, places them | `run_kese`, `load_parts`, `copper_top` |
| [`mesh25d.py`](mesh25d.py) | the 2.5D mesh, its boundaries, and writing it in Elmer's format | `Layout`, `Settings`, `build_mesh`, `relabel`, `outer_faces`, `write_elmer` |
| [`ports.py`](ports.py) | a coil's two electrodes and its port sheet | `electrodes`, `sheet_at_level`, `sheet_vertical` |
| [`elmer_case.py`](elmer_case.py) | the case (`.sif`), its circuit, running ElmerSolver and reading its scalars | `Coil`, `Material`, `Case`, `write_sif`, `run` |
| [`study.py`](study.py) | a study: KESE's export (kept or cached), one solve per frequency, the numbers back, the versions used | `kese_geometry`, `kese_export`, `solve`, `merge_run`, `versions` |

## Using it

An example's `simulation.py` puts the branch on its path and imports the modules:

```python
import json
from bridge import elmer_case as E, geometry as G, mesh25d as M, ports as P, study as S

export = S.kese_export('board.kicad_pcb', 'case/kese')                  # KESE, cached
mats = json.loads((export / 'materials.json').read_text())
parts, _ = G.load_parts(export, z_shift=-G.copper_top(mats))              # z = 0 at the top copper
lay = M.Layout(parts, M.disc(centre, 60.0), (-60.0, 60.0)).build()        # the domain: a disc 60 mm round
m = M.build_mesh(lay, M.Settings(h_edge=0.1, h_in=0.2, h_max=6.0, grade=0.5,
                                 dz_copper=0.018, dz_max=0.4, tet_max=8.0, tet_grade=0.7))
e1, e2 = P.electrodes(m, body, gap, z0, z1)                               # where the coil is opened
sheet = P.sheet_at_level(m, gap, z0)
M.write_elmer(m, 'case/run/mesh_files', boundaries)
case = E.Case(mesh_dir='case/run/mesh_files', bodies=materials,
              coils=[E.Coil('LOOP', 'LOOP', 'T1', 'T2', 'SHEET', 1.0)])
rows = S.solve(case, [3.5e6], 'case/run')                                 # L, R, M, residual, memory, time
```

[`../Examples/E01_circular_loop/simulation.py`](../Examples/E01_circular_loop/simulation.py) is the shortest complete one. The inductive coils' [`simulation.py`](../Examples/Inductive%20Coils/S0_1x_OD21_2L_tiny/Elmer%20Simulation/simulation.py) adds a rotor turned to each angle.

## What it needs

* KESE: its `Generator/` copied into [`../3D_Geometry`](../3D_Geometry) from `main`, or its path in `KESE_PATH`.
* Elmer, built into [`../Solver_Elmer/install`](../Solver_Elmer).
* The Python packages in [`../requirements.txt`](../requirements.txt) (numpy, scipy, shapely, trimesh, gmsh, mapbox_earcut).

`run_kese(mask=True)`, the default, asks KESE for a 20 µm solder mask over copper and laminate with tented vias, as the coil boards' brief does; `mask=False` leaves it out.

## Where it stops

* **Boards, not arbitrary 3D.** The mesh is 2.5D: it needs a layered stack, flat at a few heights, which every KiCad board is. A board over another (a rotor over a stator) works; a part tilted out of the board's plane does not.
* **Magnetic, harmonic.** Elmer's magneto-quasi-static A-V solver (`WhitneyAVHarmonicSolver`) at a given frequency: inductance, resistance, mutual inductance and eddy currents. Capacitance, temperature and stress are not in it yet. Full-wave fields (S-parameters, radiation) are the openEMS branch's job.
* **The caller places the ports.** The bridge does not guess where a coil is opened; each example says so (S0's `test_spec.json` holds it for the coil boards).
* **Its linear solver.** With no scalar-potential blocks (the default) and GCR with the shifted ILU(1), E01 converges to 1e-10 in 400 iterations. On large coil boards at 3.5 MHz (S0) the iterative solve no longer stalls but converges too slowly to read M. A direct solve (`Case.solver = 'mumps'`) is exact there: about 2.5 minutes and 13 to 17 GB on S0's coarser mesh (level 0.25; more at wider gaps, so add a swap file on a 16 GB machine), and roughly 40 to 55 GB on its production mesh (level 0.75).

## Licence

GPL-3.0, as the rest of this branch's code (see [`../LICENSE`](../LICENSE)).
