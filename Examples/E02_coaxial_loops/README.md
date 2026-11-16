# E02 Coaxial Loops

The second proof board of the Elmer bridge: E01's loop twice, one on each face of the board, so that
the mutual inductance between two coils (the number every encoder check rests on) is checked against
a formula known without any solver.

| Top | Bottom |
|:---:|:---:|
| ![E02, top](E02_coaxial_loops_top.webp) | ![E02, bottom](E02_coaxial_loops_bottom.webp) |

Rendered by KESE's static renderer from the board's own export. Seen from below, the bottom loop's
gap shows on the left.

## The Board

| Item | Value |
|---|---|
| Board | 30 mm × 30 mm, two copper layers, 1.6 mm, no stack-up |
| Copper | E01's loop on F.Cu, net `TX`, and the same loop on B.Cu, net `RX`, directly under it: 10 mm radius to the centre line, 0.5 mm wide, 35 µm thick, each opened at +x by a 0.2 mm gap |
| Loop to loop | 1.565 mm between the two coppers' middles (1.6 mm less one copper thickness) |
| Made by | `make_board.py`, with the bridge's `kicad_writer.py` |

## What Elmer Checks

TX carries 1 A; RX is open and carries none, so the voltage across its gap is the EMF the TX induces
in it.

| Check | How | Reference |
|---|---|---|
| M at 10 kHz | Im(V_RX / I_TX) / ω | Maxwell's formula for two coaxial circular filaments, μ0 √(ab) ((2/k − k) K(k) − (2/k) E(k)), averaged over 41 × 41 filaments across both traces' widths, times the share of the circle the TX's copper covers (0.989): 24.13 nH |
| The TX's L beside the open RX | as E01 | E01's L at the same mesh level: an open loop carries no current, so it must not change the TX |
| M at 3.5 MHz | as above, with the skin depth at the copper's thickness | the same 24.13 nH as an estimate: the current moves within each trace, not between them |
| The mesh | level 0.75 against level 1 | M should rise towards the reference, as E01's L does |

## How It Runs

```bash
python simulation.py                          # levels 0.75 and 1 at both frequencies, about 1.5 hours on 4 cores
python simulation.py --levels 1 --freqs 1e4   # one mesh, one frequency
python simulation.py --levels 0.75 --freqs 1e4 --mesh grade=0.25 --mesh tet_grade=0.35 --results results_grade.json --out case_grade
```

Every setting is in `SETTINGS` at the top of `simulation.py`. They are E01's, with two differences:

| Setting | Value | Why |
|---|---|---|
| Levels | 0.75 and 1 | level 1 took 6.7 GB; level 1.3 would need about 10 GB and was not run on the 15 GB test machine |
| Linear solve | at most 1500 iterations | E01's iteration check: 1500 and 3000 iterations differ by 0.17 % in L |

The insulators (FR-4) are air to the magneto-quasi-static solve: μr 1, and εr plays no part without
displacement current.

## Results

See [results.md](results.md): expected against what came out.

## Licence

GPL-3.0, as the rest of this branch.
