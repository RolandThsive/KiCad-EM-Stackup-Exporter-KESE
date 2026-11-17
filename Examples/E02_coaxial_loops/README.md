# E02 Coaxial Loops

The second proof board of the PyPEEC bridge: E01's loop twice, one on each face of the board, so that the mutual
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
| Loop to loop | 1.565 mm between the two coppers' middles (1.6 mm less one copper thickness) |
| Made by | `make_board.py`, with [`../kicad_writer.py`](../kicad_writer.py) |

## What PyPEEC Checks

TX carries 1 A; RX carries none (a 0 A source between its terminals), so the voltage across its gap is the EMF the
TX induces in it.

| Check | How | Reference |
|---|---|---|
| M at 10 kHz | Im(V_RX / I_TX) / ω | Maxwell's formula for two coaxial circular filaments, μ0 √(ab) ((2/k − k) K(k) − (2/k) E(k)), averaged over 41 × 41 filaments across both traces' widths, times the share of the circle the TX's copper covers (0.989): 24.13 nH |
| The TX's L beside the open RX | as E01 | E01's L at the same voxels: an open loop carries no current, so it must not change the TX |
| M at 3.5 MHz | as above, with the skin depth at the copper's thickness | the same 24.13 nH as an estimate: the current moves within each trace, not between them |
| The voxels | 100 and 50 µm in the board's plane | M should settle as the voxels shrink |

The two copper sheets are 1.565 mm apart, and the grid's z step is chosen so that this is a whole number of voxel
layers to within a micron (45 steps of 34.8 µm: 46 layers, the sheets the first and the last); the layers between
the sheets hold no copper and add no unknowns, only grid to the FFTs.

## How It Runs

```bash
python simulation.py                      # the voxel ladder at both frequencies
python simulation.py --voxels 0.05        # one voxel size only
python simulation.py --voxels-only        # draw the voxels and print how many, solve nothing
```

Every setting is in `SETTINGS` at the top of `simulation.py`, the same as E01's: 10 kHz and 3.5 MHz, voxels of
100 and 50 µm (25 µm would take a grid of 30 million voxels and about 9 GB), one voxel layer through each copper sheet, PyPEEC's default tolerances (`../../bridge/tolerance.yaml`), 4 threads.

## Results

See [results.md](results.md): expected against what came out, and the voxel ladder.

## Licence

GPL-3.0, as the rest of this branch.
