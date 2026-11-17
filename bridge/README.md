# The bridge

The bridge takes a KiCad board into a FastHenry simulation and reads the answer back. It is general: nothing in it names a board, a coil or an example. Every example under [`../Examples`](../Examples) imports it, and adds only what belongs to its own board: which nets are coils, where each coil is opened for its port, what to sweep, and what to compare the answer with.

KESE stays a geometry exporter. The bridge runs it as a program and reads what it writes; it changes nothing in KESE.

[FastHenry](../Solver_FastHenry/README.md) (M.I.T.'s, in FastFieldSolvers' release 3.0.1) solves the magneto-quasi-static problem on conductors cut into straight filaments: each filament carries a uniform current along its length, every filament couples to every other through its partial inductance, and only the copper is discretised. The space round it needs no mesh and has no boundary.

## What happens to a board

1. **Stack-up** (`stackup.kese_geometry`, `stackup.copper_layers`): KESE exports the `.kicad_pcb` with its solver preset (one STL per solid, a `materials.json`, a STEP and its report), kept in a folder of its own beside the board (the coil examples use `3D_Geometry/`) with a `source.json` holding the board file's hash, so an unchanged board is not exported twice. From `materials.json` the bridge takes the height and thickness of every copper layer: each dielectric says which two layers it lies between, and each copper part gives its layer's thickness. These are the board's own stack-up, as KESE builds it.
2. **Copper** (`kicad.read`): the board file itself gives the conductors. A KiCad track is a centre line with a width, which is exactly a FastHenry segment, so the bridge reads every track and arc, every via and every copper polygon (`gr_poly` on a copper layer, and zones' filled polygons) with its net and layer, straight from the `.kicad_pcb`.
3. **Model** (`fasthenry_case.add_board`, `add_polygon`): in model coordinates (x and y as KiCad's with y up, z = 0 at the top of the top copper):
   * a track is a segment between nodes at its ends, at the middle of its layer's copper, as wide as the track and as thick as the copper, split into `nwinc` filaments across its width (the edge ones `rw` times narrower than the next in, so the current can crowd to the edges) and `nhinc` through its thickness; an arc is cut into chords of at most 5° and 0.5 mm; tracks of one net that meet at a point share a node;
   * a via is a vertical bar between its nodes on the layers it joins, a square with the copper section of a barrel plated 25 µm (its pads, a fraction of a square millimetre each, are left out);
   * a copper polygon is a grid of bars at its layer's height, each as wide as the cell it stands for: a polar grid graded towards all four edges where the polygon is a sector of a ring (so its arcs are not stair steps), a square grid clipped to it otherwise. A board can be turned copper side down, raised by an air gap and turned about an axis: that is how a rotor is placed over a stator.
4. **Ports** (`via_nodes`, `cut_nodes`): each coil is opened where its leads go. At two trace ends stacked on two layers, the port is between those two nodes; at a via left out, between where the coil's tracks reach the via on its two layers; at a cut across a trace, the copper inside the cut is taken out of the trace and the port is between the two cut faces. FastHenry gives back the open-circuit impedance matrix between the ports: Z[i][j] is the voltage at port i over the current into port j, with every other port open. So with 1 A into the TX, a receiver's voltage is its open-circuit EMF, and its mutual inductance M is Im(Z[receiver][TX]) / 2πf.
5. **Solve** (`fasthenry_case.run`, `coil_rows`): the bridge writes FastHenry's input (`model.inp`: millimetres, copper at 5.8e7 S/m, the nodes, segments and `.external` ports, one frequency), runs FastHenry in that folder, measures its peak memory and time, and reads `Zc.mat` back: the driven coil's Z, R and L, and for each other coil its mutual impedance from the driven one, its M, the reverse M (from the driven coil's row) and its own L. FastHenry's dense direct solve (`-s ludecomp -m direct`, with the multipole refinement off: `-a off`) gives the exact answer of the filament model, so its impedance matrix is symmetric to the last digit; the reverse M is kept as that check (reciprocity).

## The modules

| File | What it does | Called as |
|---|---|---|
| [`kicad.py`](kicad.py) | reads a `.kicad_pcb` (KiCad 6 to 9): nets, tracks and arcs (arcs as chords), vias, copper polygons | `read`, `Track.chords`, `net_name` |
| [`stackup.py`](stackup.py) | runs KESE, keeps its export beside the board, reads the copper layers' heights from `materials.json`; the versions a result depends on | `kese_geometry`, `copper_layers`, `run_kese`, `versions` |
| [`fasthenry_case.py`](fasthenry_case.py) | the model (nodes, segments, filaments, ports), FastHenry's input, running it, reading `Zc.mat`, each coil's Z, R, L and M | `Model`, `add_board`, `add_polygon`, `via_nodes`, `cut_nodes`, `run`, `coil_rows` |
| [`setup_machine.sh`](setup_machine.sh) | a fresh Ubuntu machine: `.venv` with the packages of `requirements.txt`, and FastHenry built if the committed one does not run | `bash bridge/setup_machine.sh` |

## Using it

An example's `simulation.py` puts the branch on its path and imports the modules:

```python
from bridge import fasthenry_case as C, kicad as K, stackup as S

board = K.read('board.kicad_pcb')                                        # tracks, vias, polygons by net
zs = S.copper_layers(S.kese_geometry('board.kicad_pcb', '3D_Geometry'))  # {layer: (z_bottom, z_top)}
top = zs['F.Cu'][1]
zl = {k: (a - top, b - top) for k, (a, b) in zs.items()}                 # z = 0 at the top copper
m = C.Model(title='one loop')
C.add_board(m, board, zl, {'LOOP': 'LOOP'}, nwinc=3, rw=2)               # the net LOOP, 3 filaments across
m.port('LOOP', *C.via_nodes(m, 'LOOP', 110.0, -100.0))                  # opened between its two stacked ends
names, Z, secs, gb, log = C.run(m, 3.5e6, 'case/run', ['-s', 'ludecomp', '-m', 'direct', '-a', 'off'])
rows = C.coil_rows(names, Z, 3.5e6, driven='LOOP')                       # Z, R and L
```

[`../Examples/E01_circular_loop/simulation.py`](../Examples/E01_circular_loop/simulation.py) is the shortest complete one. The inductive coils' [`simulation.py`](../Examples/Inductive%20Coils/S0_1x_OD21_2L_tiny/FastHenry%20Simulation/simulation.py) adds a rotor turned to each angle.

## What it needs

* FastHenry: [`../Solver_FastHenry`](../Solver_FastHenry) has the build every simulation here ran with, and the script that builds it. The bridge uses `$FASTHENRY`, else `Solver_FastHenry/install/bin/fasthenry`, else `fasthenry` on the PATH.
* The Python packages in [`../requirements.txt`](../requirements.txt) (numpy and shapely for the bridge; matplotlib and pillow for the examples' charts and pictures).
* KESE, only to export a board whose `3D_Geometry/` is not committed: its `Generator/` copied into [`../3D_Geometry`](../3D_Geometry) from `main`, or its path in `KESE_PATH`.

## Where it stops

* **Boards, not arbitrary 3D.** The conductors are a board's tracks, vias and polygons, flat at their layers' heights. A board over another (a rotor over a stator) works; a part tilted out of the board's plane does not.
* **Filaments along the tracks.** The current in a segment runs along it; across its width and thickness it may vary from filament to filament but is uniform inside each. With 3 filaments across and 1 through the 35 µm copper (whose skin depth at 3.5 MHz is about the same), M and L settle to a few hundredths of a percent and R to about 1.5 % (see the coil boards' README). A wide pour carrying current across as well as along needs the grid of bars, as the rotor has.
* **Pads and track ends.** A track's round ends and a via's pads are not modelled, only its centre line, width and barrel; on the coil boards they are a small part of the copper.
* **A dense direct solve.** Its memory grows with the square of the filaments and its time with their cube: about 7,000 to 9,500 filaments per coil board, 0.7 to 1.5 GB and half a minute to a few minutes each. FastHenry's multipole solve takes far less on large boards, but it is iterative, and the bridge's coil boards are small enough not to need it.
* **Magnetic, harmonic.** Inductance, resistance, mutual inductance and eddy currents at a given frequency. No capacitance, temperature or stress.
* **The caller places the ports.** The bridge does not guess where a coil is opened; each example says so (the coil boards' `test_spec.json` holds it).

## Licence

GPL-3.0, as the rest of this branch's code (see [`../LICENSE`](../LICENSE)). FastHenry keeps its own licence (see [`../Solver_FastHenry/LICENSE.md`](../Solver_FastHenry/LICENSE.md)).
