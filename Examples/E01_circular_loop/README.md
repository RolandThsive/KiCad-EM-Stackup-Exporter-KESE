# E01 Circular Loop

The first proof board of the Elmer bridge: one circular trace, opened by a small gap for its
terminals, so that every part of the chain (KESE's export, the 2.5D mesh, the electrodes, Elmer's
circuit and the read-back) is checked against an inductance and a resistance known without any
solver.

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

The gap is where the terminals sit: the bridge puts an electrode on each round end's face and a
sheet across the gap, and Elmer's circuit drives 1 A between them.

## What Elmer Checks

| Check | How | Reference |
|---|---|---|
| L at 10 kHz | Im(V / I) / ω of the loop; the skin depth (0.66 mm) is far above the copper's 35 µm, so the current is uniform | Grover's ring formula μ0 R (ln(8R / g) − 2) with the rectangle's geometric mean distance g = 0.2235 (w + t), times the share of the circle the copper covers (0.989): 55.99 nH, a lower bound by up to 0.8 % (see results.md) |
| L from the field's energy | 2W / I² from Elmer's field energy | the same L, as a check on the circuit's read-back |
| R at 10 kHz | Re(V / I) | the DC resistance of an annular sector, θ / (σ t ln(r_out / r_in)): 61.20 mΩ |
| R_dc | Elmer's own DC solve of the coil's current direction | the same 61.20 mΩ |
| L and R at 3.5 MHz | as above, at the coil boards' frequency, where the skin depth (35 µm) equals the copper's thickness | no exact reference: Grover's formula with the thin strip's high-frequency GMD w / 4 gives 55.44 nH, an estimate |
| The mesh | the same at three mesh levels, 0.75, 1 and 1.3 | L should rise towards the reference as the mesh is refined (first-order edge elements with the current imposed give a lower bound) |
| The iterative solve | level 1 at 1500 and at 3000 iterations | L should not move |
| The air's mesh and domain | level 0.75 with `grade` and `tet_grade` halved; level 0.75 in a domain twice as big | L should not move much: the mesh ladder leaves the air as it is |

## How It Runs

```bash
python simulation.py                          # the mesh ladder at both frequencies, about 2 hours on 4 cores
python simulation.py --levels 1 --freqs 1e4   # one mesh, one frequency
python simulation.py --levels 1 --freqs 1e4 --max-iter 1500 --results results_iter1500.json --out case_iter1500
python simulation.py --levels 0.75 --freqs 1e4 --mesh grade=0.25 --mesh tet_grade=0.35 --results results_grade.json --out case_grade
python simulation.py --levels 0.75 --domain-mm 120 --results results_domain120.json --out case_domain120
python simulation.py --levels 0.75 --max-iter 1500 --fields --results results_fields.json --out case_fields
python make_pictures.py                       # the wiki's charts and pictures, from the results and case_*/
python simulation.py --mesh-only              # build the meshes and print their size, solve nothing
```

Every setting is in `SETTINGS` at the top of `simulation.py`:

| Setting | Value | Why |
|---|---|---|
| Frequencies | 10 kHz and 3.5 MHz | uniform current, and the coil boards' frequency |
| Air domain | a cylinder 60 mm in radius and 120 mm high (6 loop radii each way), n × A = 0 on its outside | far enough that the outside barely holds the field back |
| Mesh | at level 1: 0.09 mm at the copper's edges, 0.18 mm inside it, growing by 0.5 mm per mm away from it to 6 mm at most; 18 µm wedge layers through the copper; tetrahedra in the air growing by 0.7 mm per mm up to 8 mm | a level divides the copper's three sizes by itself; the air's grading stays |
| Elements | first order (`--order 2` for second order) | second order has several times the unknowns; it has not been run on the 15 GB test machine |
| Linear solve | BiCGStab(l) of degree 4 with Elmer's circuit preconditioner, tolerance 1e-7, at most 3000 iterations | see results.md for what the cap does |
| Threads | 4 | |

## Results

See [results.md](results.md): expected against what came out, the mesh ladder, the iteration check
and the two diagnostic runs.

## Licence

GPL-3.0, as the rest of this branch.
