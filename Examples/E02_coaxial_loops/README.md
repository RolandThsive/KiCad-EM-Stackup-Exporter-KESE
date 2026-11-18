# E02 Coaxial Loops

The second proof board of the Palace bridge: E01's loop twice, one on each face of the board, so that the mutual inductance between two coils (the number every encoder check rests on) is checked against a formula known without any solver.

| Top | Bottom |
|:---:|:---:|
| ![E02, top](E02_coaxial_loops_top.webp) | ![E02, bottom](E02_coaxial_loops_bottom.webp) |

Rendered by KESE's static renderer from the board's own export. Seen from below, the bottom loop's gap shows on the left.

## The Board

| Item | Value |
|---|---|
| Board | 30 mm × 30 mm, two copper layers, 1.6 mm, no stack-up |
| Copper | E01's loop on F.Cu, net `TX`, and the same loop on B.Cu, net `RX`, directly under it: 10 mm radius to the centre line, 0.5 mm wide, 35 µm thick, each opened at +x by a 0.2 mm gap |
| Loop to loop | 1.565 mm between the two coppers' middles (from KESE's stack-up) |
| Made by | `make_board.py`, with [`../kicad_writer.py`](../kicad_writer.py) |

The board is meshed as E01's, with both loops in the same 2.5D mesh, and each gap holds a lumped port: a rectangle across it, through the copper, with 50 Ω across it. Palace drives the two ports in turn and gives back the impedance matrix between them.

## What Palace Checks

| Check | How | Reference |
|---|---|---|
| M at 10 kHz | Im(Z[RX][TX]) / ω | two values of Neumann's double integral, averaged over filaments across both traces' widths ([`../references.py`](../references.py), `arc_mutual`): the two open arcs (each 356°, between its round ends' centres, the gaps one above the other), 23.886 nH, and the closed rings (Maxwell's formula), 24.400 nH. Palace's port sheets close each loop across its gap: the TX's current crosses its sheet, and the RX's EMF is taken across its sheet. So once the mesh is fine enough its M should lie above the open arcs, which leave both gaps out, and near the closed rings. The percentages in results.md are against the open arcs, the reference every solver's branch shares |
| Reciprocity | Im(Z[TX][RX]) / ω, the M from the RX back to the TX | the same M |
| The TX's L and R beside the RX | Z[TX][TX], the TX with the RX open | E01's at the same mesh: an open loop carries no current round it, so at 10 kHz it must not change the TX |
| M at 3.5 MHz | as above, with the skin depth at the copper's thickness | close to the 10 kHz value: the current moves within each trace, and eddy currents in the RX take a little from the TX |
| The mesh | levels 0.25, 0.5, 0.75, 1, and one run with the coil boards' air grading, at 100 kHz and 3.5 MHz | M should settle as the mesh gets finer |

## How It Runs

```bash
python make_board.py                      # write the board (it is committed)
python simulation.py --ranks 4            # the mesh ladder at both frequencies
python simulation.py --levels 0.75 --freqs 1e5 3.5e6 --mesh grade=0.125 --mesh tet_grade=0.175 \
    --mesh dz_max=0.2 --results results_grade.json --out case_grade --restart 100
                                          # the air graded as the coil boards' is
python simulation.py --levels 0.75 --freqs 1e5 --results results_100k.json --out case_100k
                                          # M at 100 kHz on the default mesh
```

Every setting is in `SETTINGS` at the top of `simulation.py`, the same as E01's: 10 kHz and 3.5 MHz, copper at 5.8e7 S/m, the same domain, the same mesh ladder and the same solver settings. The graded run differs in two ways. Its mesh carries the fine wedges through the board to the RX, 303,129 nodes, and 300 of GMRES's vectors on it would not fit in 15 GB, so GMRES restarts every 100 iterations. And at 10 kHz GMRES does not converge on that mesh, so its low frequency is 100 kHz, where AMS needs no singular-operator flag; `results_100k.json` sets 100 kHz beside 10 kHz on the default mesh (see results.md).

## Results

See [results.md](results.md): expected against what came out, and the mesh ladder.

## Licence

GPL-3.0, as the rest of this branch.
