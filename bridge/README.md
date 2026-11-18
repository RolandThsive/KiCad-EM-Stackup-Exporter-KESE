# The bridge

The bridge takes a KiCad board into a Palace simulation and reads the answer back. It is general: nothing in it names a board, a coil or an example. Every example under [`../Examples`](../Examples) imports it, and adds only what belongs to its own board: which nets are coils, where each coil is opened for its port, what to sweep, and what to compare the answer with.

KESE stays a geometry exporter. The bridge runs it as a program and reads what it writes; it changes nothing in KESE.

[Palace](../Solver_Palace/README.md) (AWS Labs, Apache 2.0) solves Maxwell's equations in the frequency domain for the electric field, with Nédélec edge elements on a mesh of the copper and the air round it out to a boundary. Each coil is opened by a lumped port: a sheet across the place where it is opened, with a resistance across it.

## What happens to a board

1. **Export** (`study.kese_geometry` or `study.kese_export`, `geometry.run_kese`): KESE exports the `.kicad_pcb` with its solver preset (`--for elmer`: one STL per solid and a `materials.json`, plus a STEP and its report). `kese_geometry` keeps the export in a folder of its own, meant to be committed beside the board (the coil examples use `3D_Geometry/`), with a `source.json` holding the board file's hash; `kese_export` keeps it in a scratch cache named by that hash. Either way an unchanged board is not exported twice.
2. **Parts** (`geometry.load_parts`): each solid becomes a part in model coordinates (x and y as KiCad's with y up, z = 0 at the top of the top copper), named by its net or its role. A board can be flipped copper side down, moved up by an air gap and turned about an axis the caller gives: that is how a rotor is placed over a stator.
3. **Mesh** (`mesh25d`): the 2.5D mesh. One triangle mesh holds every copper edge of every layer, and it is swept through the stack as prism (wedge) layers, through each copper layer as finely as the settings ask. Tetrahedra fill the air above and below, out to the domain's edge. No 3D Booleans, so 35 µm copper on a 0.8 mm board stays a few hundred thousand nodes. Gmsh triangulates the plane and fills the air; every input point is snapped to a 0.5 µm grid, so that a line given to the mesher lands exactly on mesh edges.
4. **Ports** (`ports`, `mesh25d.vertical_faces`): a lumped port in Palace must be a rectangle, its two ends on conductors, and its direction along one of its sides. The caller gives a straight line in the plane, drawn into the triangle mesh (`build_mesh(extra_lines=...)`), and the port is the stack of vertical mesh faces along that line between two heights: between a coil's two copper layers where it is opened at two stacked trace ends or a left-out via (direction +z), or through the copper's thickness across a cut in a trace (direction along the line). `ports.facing_vertices` finds such a line across a gap between two round trace ends, from the copper's outline as the mesher has it; `ports.electrodes` checks that the copper meets the opening in exactly two places, so that the coil is one open conductor.
5. **Case** (`palace_case`): Palace's JSON input: the mesh (Gmsh 2.2, millimetres), air everywhere and the copper with a conductivity, the outside a perfect conductor, the ports (the driven one with 50 Ω and an excitation, the receivers with 1 MΩ, so they are open to a few parts in a million; or every port driven in turn, for the whole impedance matrix), one frequency, the element order and the linear solver. FR-4 and solder mask are air: at 3.5 MHz their permittivity changes nothing the examples read.
6. **Solve and read back** (`palace_case.run`, `read`, `coil_rows`, `energy_check`): Palace runs on N MPI ranks; the bridge reads each port's voltage and incident voltage (`port-V.csv`) and the field's magnetic energy (`domain-E.csv`). The current into a coil is (2 V_inc − V) / R at a driven port and −V / R at an undriven one, so the impedance matrix between the ports is Z = V I⁻¹ (with only the TX driven, its column: Z[k][TX] = V_k / I_TX). From it: each coil's R and L, and each receiver's mutual inductance M = Im(Z[receiver][TX]) / 2πf. The magnetic energy W gives the driven coil's L a second way, 2W / |I|² (Palace's W is ½ Re ∫ H*·B over the domain, with the fields as complex amplitudes); the two agree for a converged solve. The log gives the linear solve's iterations, its residual, whether it converged, and the peak memory.

## The modules

| File | What it does | Called as |
|---|---|---|
| [`geometry.py`](geometry.py) | runs KESE, reads its solids and `materials.json`, places them | `run_kese`, `load_parts`, `copper_top` |
| [`mesh25d.py`](mesh25d.py) | the 2.5D mesh, its boundaries, and writing it in Gmsh's format for Palace | `Layout`, `Settings`, `build_mesh`, `outer_faces`, `vertical_faces`, `write_gmsh` |
| [`ports.py`](ports.py) | where a coil is opened: the line of a port across a gap, the check that the coil is opened in one place | `facing_vertices`, `electrodes` |
| [`palace_case.py`](palace_case.py) | the case (`config.json`), running Palace, reading its tables, each coil's Z, R, L and M, the energy check | `Port`, `Case`, `config`, `run`, `read`, `coil_rows`, `energy_check` |
| [`study.py`](study.py) | KESE's export (kept or cached) and the versions a result depends on | `kese_geometry`, `kese_export`, `versions` |
| [`setup_machine.sh`](setup_machine.sh) | a fresh Ubuntu 24.04 machine: the system libraries Palace runs with, Palace built if the committed one does not run, and `.venv` with the packages of `requirements.txt` | `bash bridge/setup_machine.sh` |

## Using it

An example's `simulation.py` puts the branch on its path and imports the modules:

```python
import json
import shapely
from shapely.geometry import box
from bridge import geometry as G, mesh25d as M, palace_case as C, ports as P, study as S

export = S.kese_geometry('board.kicad_pcb', '3D_Geometry')               # KESE, kept beside the board
mats = json.loads((export / 'materials.json').read_text())
parts, _ = G.load_parts(export, z_shift=-G.copper_top(mats))              # z = 0 at the top copper
lay = M.Layout(parts, M.disc(centre, 60.0), (-60.0, 60.0)).build(insulators=False)
cu = shapely.unary_union([g for p in lay.parts if p.body == 'LOOP' for g in p.polys.values()])
line = P.facing_vertices(cu, box(*gap_box), axis=1)                       # across the gap, tip to tip
m = M.build_mesh(lay, M.Settings(h_edge=0.09, h_in=0.18, h_max=6.0, grade=0.5, dz_copper=0.018,
                                 dz_max=0.4, tet_max=8.0, tet_grade=0.7), extra_lines=[line])
qs, qsp = M.vertical_faces(m, z0, z1, line)                               # the port: through the copper
t, tp, q, qp = M.outer_faces(m)
tags = M.write_gmsh(m, 'case/run/mesh.msh', [('OUTER', t, tp, q, qp), ('PORT', t[:0], tp[:0], qs, qsp)])
case = C.Case(mesh='case/run/mesh.msh', conductors=[tags['LOOP']], air=[tags['AIR']], outer=[tags['OUTER']],
              ports=[C.Port('LOOP', tags['PORT'], '+Y', R=50.0, excite=1)])
got = C.run(case, 3.5e6, 'case/run', np_=4)                               # Z, V, I, energy, time, memory
row = C.coil_rows(case, got, 'LOOP')['LOOP']                              # Z, R and L
```

[`../Examples/E01_circular_loop/simulation.py`](../Examples/E01_circular_loop/simulation.py) is the shortest complete one. The inductive coils' [`simulation.py`](../Examples/Inductive%20Coils/S0_1x_OD21_2L_tiny/Palace%20Simulation/simulation.py) adds a rotor turned to each angle.

## What it needs

* Palace: [`../Solver_Palace`](../Solver_Palace) has the build every simulation here ran with (Ubuntu 24.04, with Open MPI and OpenBLAS from the system), and the script that builds it. The bridge uses `$PALACE`, else `Solver_Palace/install/bin/palace`, else `palace` on the PATH.
* The Python packages in [`../requirements.txt`](../requirements.txt) (numpy, scipy, shapely, trimesh, gmsh and mapbox_earcut for the bridge; matplotlib and pillow for the examples' charts and pictures).
* KESE, only to export a board whose `3D_Geometry/` is not committed: its `Generator/` copied into [`../3D_Geometry`](../3D_Geometry) from `main`, or its path in `KESE_PATH`.

## Where it stops

* **Boards, not arbitrary 3D.** The mesh is 2.5D: it needs a layered stack, flat at a few heights, which every KiCad board is. A board over another (a rotor over a stator) works; a part tilted out of the board's plane does not.
* **Ports are rectangles.** Palace takes a lumped port only as a rectangle whose ends lie on conductors (it checks the sheet's bounding box against its direction to a part in a million), so a port's line must be straight, its ends on the grid, and nothing else may cross it. The coil boards' ports are built that way; a port across an irregular gap is not.
* **The full-wave equations at low frequency.** Palace solves for the electric field with the displacement current kept. At 10 kHz on a board this size, the field's gradients in the air cost almost nothing, and the operator hypre's AMS preconditioner works on is all but singular there: told so (`AMSSingularOperator`), GMRES converges, slowly (E01: hundreds of iterations); left alone, it diverges. At 3.5 MHz the coil boards converge in one to two hundred iterations without it.
* **No direct solver.** The committed build has hypre's AMS under GMRES only (see [`../Solver_Palace/README.md`](../Solver_Palace/README.md) for why). Each solve's convergence is therefore checked: the residual reached, L from the port against L from the field's energy, and on the coil boards reciprocity at one angle per gap.
* **The caller places the ports.** The bridge does not guess where a coil is opened; each example says so (the coil boards' `test_spec.json` holds it).

## Licence

GPL-3.0, as the rest of this branch's code (see [`../LICENSE`](../LICENSE)). Palace keeps its own licence, Apache 2.0 (see [`../Solver_Palace/README.md`](../Solver_Palace/README.md)).
