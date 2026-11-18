# E01 Circular Loop

The first proof board of the Palace bridge: one circular trace, opened by a small gap for its port, so that every part of the chain (KESE's export, the 2.5D mesh, the lumped port, Palace's input and the read-back of its port impedance) is checked against an inductance and a resistance known without any solver.

| Top | Bottom |
|:---:|:---:|
| ![E01, top](E01_circular_loop_top.webp) | ![E01, bottom](E01_circular_loop_bottom.webp) |

Rendered by KESE's static renderer from the board's own export.

## The Board

| Item | Value |
|---|---|
| Board | 30 mm × 30 mm, two copper layers, 1.6 mm, no stack-up |
| Copper | one trace on F.Cu, net `LOOP`: a circle of 10 mm radius to its centre line, 0.5 mm wide, 35 µm thick, opened at +x by a 0.2 mm gap between its two round ends |
| B.Cu | empty |
| Made by | `make_board.py`, with [`../kicad_writer.py`](../kicad_writer.py) |

The bridge meshes KESE's solids as it meshes the coil boards: the board's plan in triangles, swept through the copper and the air beside it as layers of wedges, with tetrahedra above and below out to a cylinder 60 mm round and 60 mm above and below, whose surface is a perfect conductor. The board's FR-4 is air to this solve (it is not magnetic). The port is a lumped port: a rectangle standing across the gap, through the copper, from one round end's tip to the other's, with 50 Ω across it; Palace drives it and gives back its impedance Z, so L = Im(Z) / ω and R = Re(Z).

## What Palace Checks

| Check | How | Reference |
|---|---|---|
| L at 10 kHz | Im(Z) / ω of the loop's port; the skin depth (0.66 mm) is far above the copper's 35 µm, so the current is uniform | Neumann's double integral over the open arc with the rectangle's geometric mean distance g = 0.2235 (w + t) (Grover, [`../references.py`](../references.py), `arc_inductance`): 55.590 nH for the arc between the round ends' centres (356.0°), 56.293 nH for the arc out to the gap's faces (358.9°); Grover's ring formula for the closed ring, 56.622 nH. Palace's port sheet carries the current across the gap and so closes the loop: once the mesh is fine enough its L should lie above the open arcs and near the closed ring. The percentages in results.md are against the arc between the centres, the reference every solver's branch shares |
| L from the field's energy | 2 W / I², from the magnetic energy Palace stores in the whole domain | the same L as from the port: the two agree only if the port and the field are consistent |
| R at 10 kHz | Re(Z) | the DC resistance of the annular sector between the round ends' centres, θ / (σ t ln(r_out / r_in)): 61.201 mΩ; the half-discs past the centres add a little |
| L and R at 3.5 MHz | as above, at the coil boards' frequency, where the skin depth (35 µm) equals the copper's thickness | no exact reference: L lies between its DC value and the value with all the current at the copper's surface; the arc integral with a thin strip's high-frequency GMD w / 4 gives 55.039 to 55.738 nH, an estimate that leaves out the copper's thickness |
| The mesh | levels 0.25, 0.5, 0.75, 1: each divides the copper's mesh sizes by itself | L should rise as the mesh gets finer; one more run grades the air as the coil boards' mesh does |

## How It Runs

```bash
python make_board.py                      # write the board (it is committed)
python simulation.py --ranks 4            # the mesh ladder at both frequencies
python simulation.py --levels 0.75 --mesh grade=0.125 --mesh tet_grade=0.175 --mesh dz_max=0.2 \
    --results results_grade.json --out case_grade   # the air graded as the coil boards' is
python simulation.py --mesh-only          # build the meshes and print their size, solve nothing
```

The first run fills `3D_Geometry/` with KESE's export of the board. Every setting is in `SETTINGS` at the top of `simulation.py`:

| Setting | Value | Why |
|---|---|---|
| Frequencies | 10 kHz and 3.5 MHz | uniform current, and the coil boards' frequency |
| Copper | σ = 5.8e7 S/m, 35 µm (KESE's stack-up) | |
| Domain | a cylinder 60 mm round, ±60 mm, its surface a perfect conductor | 6 loop radii: the field there is small |
| Solver | Palace's frequency-domain driven solve, Nédélec elements of order 1, GMRES (restarted every 300) preconditioned by hypre's AMS, to a residual of 1e-08 of where it starts, at most 2,000 iterations | as the coil boards |
| Below 100 kHz | AMS told the operator is singular (`AMSSingularOperator`), at most 3,000 iterations | in the air the electric field's gradients cost almost nothing at 10 kHz, so the operator AMS works on is all but singular: without the flag GMRES diverges, with it it converges slowly and may stop at the iteration limit (the residual it reached is in results.md) |

| Mesh setting | Value at level 1 | Why |
|---|---|---|
| `h_edge`, `h_in` | 0.09 mm at the copper's edges, 0.18 mm inside it | the triangles of the board's plan; a level divides both by itself, so 0.25 is four times as coarse |
| `dz_copper` | 0.018 mm | the wedge layers through the 35 µm copper (also divided by the level) |
| `h_max`, `grade` | 6 mm, 0.5 | how far the plan's triangles grow away from the copper, and how fast (per mm) |
| `dz_max` | 0.4 mm | the wedge layers in the air beside the copper |
| `tet_max`, `tet_grade` | 8 mm, 0.7 | the tetrahedra above and below the wedges, out to the domain |

The coil boards grade the air finer: `grade` 0.125, `tet_grade` 0.175 and `dz_max` 0.2. The `results_grade.json` run uses those on E01.

## Results

See [results.md](results.md): expected against what came out, and the mesh ladder.

## Licence

GPL-3.0, as the rest of this branch.
