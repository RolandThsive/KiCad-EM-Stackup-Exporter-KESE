# E02 Coaxial Loops

The second proof board of the FastHenry bridge: E01's loop twice, one on each face of the board, so that the mutual
inductance between two coils (the number every encoder check rests on) is checked against a formula known without
any solver.

| Top | Bottom |
|:---:|:---:|
| ![E02, top](E02_coaxial_loops_top.webp) | ![E02, bottom](E02_coaxial_loops_bottom.webp) |

Rendered by KESE's static renderer from the board's own export. Seen from below, the bottom loop's gap shows on the
left.

## The Board

| Item | Value |
|---|---|
| Board | 30 mm × 30 mm, two copper layers, 1.6 mm, no stack-up |
| Copper | E01's loop on F.Cu, net `TX`, and the same loop on B.Cu, net `RX`, directly under it: 10 mm radius to the centre line, 0.5 mm wide, 35 µm thick, each opened at +x by a 0.2 mm gap |
| Loop to loop | 1.565 mm between the two coppers' middles (1.6 mm less one copper thickness, from KESE's stack-up) |
| Made by | `make_board.py`, with [`../kicad_writer.py`](../kicad_writer.py) |

Each loop is modelled as E01's: 126 chords, split into filaments across and through, with a port between the two
nodes at its trace ends.

## What FastHenry Checks

FastHenry gives back the open-circuit impedance matrix between the two ports. With 1 A into the TX and the RX open,
the RX's voltage is the EMF the TX induces in it, so M = Im(Z[RX][TX]) / ω.

| Check | How | Reference |
|---|---|---|
| M at 10 kHz | Im(Z[RX][TX]) / ω | the mutual inductance of the two open arcs (each 356°, between its round ends' centres, the two gaps one above the other) by Neumann's double integral, averaged over 21 × 21 filaments across both traces' widths ([`../references.py`](../references.py), `arc_mutual`): 23.886 nH. For scale: the closed rings by the same integral (Maxwell's formula) give 24.400 nH |
| Reciprocity | Im(Z[TX][RX]) / ω, the M from the RX back to the TX | the same M: FastHenry's direct solve makes the matrix symmetric to the last digit |
| The TX's L and R beside the open RX | as E01 | E01's at the same filaments: an open loop carries no current round it, so at 10 kHz it must not change the TX |
| M at 3.5 MHz | as above, with the skin depth at the copper's thickness | no exact reference: the current moves within each trace, towards its edges, and eddy currents in the RX's trace take a little from the TX |
| The filaments | 1, 3, 5 and 9 across each trace, 1 and 3 through its copper | M should settle as the filaments get finer |

## How It Runs

```bash
python make_board.py                      # write the board (it is committed)
python simulation.py                      # the filament ladder at both frequencies (about 12 minutes)
python simulation.py --nwinc 9            # 9 filaments across each trace only
python simulation.py --nwinc 9 --nhinc 3  # 9 across and 3 through
```

Every setting is in `SETTINGS` at the top of `simulation.py`, the same as E01's: 10 kHz and 3.5 MHz, filaments of
1 × 1 to 9 × 3, the edge ones twice as narrow as the next in, chords of at most 5° and 0.5 mm, copper at
5.8e7 S/m, and FastHenry 3.0.1's dense direct solve (`-s ludecomp -m direct -a off`).

## Results

See [results.md](results.md): expected against what came out, and the filament ladder.

## Licence

GPL-3.0, as the rest of this branch.
