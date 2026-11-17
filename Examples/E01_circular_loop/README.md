# E01 Circular Loop

The first proof board of the FastHenry bridge: one circular trace, opened by a small gap for its port, so that
every part of the chain (KESE's stack-up, the board's tracks read as segments, the filaments, the port, FastHenry's
input and the read-back of `Zc.mat`) is checked against an inductance and a resistance known without any solver.

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

The trace is two KiCad arcs. The bridge cuts them into straight segments (chords) of at most 5° and 0.5 mm: 126
segments here, each as wide as the trace and as thick as its copper, split into filaments across its width and
through its thickness. The port is between the two nodes at the trace's ends, the centres of its round ends, 0.7 mm
apart across the gap: FastHenry drives 1 A between them, and closes the loop through the port at no length.

## What FastHenry Checks

| Check | How | Reference |
|---|---|---|
| L at 10 kHz | Im(Z) / ω of the loop's port; the skin depth (0.66 mm) is far above the copper's 35 µm, so the current is uniform | the partial inductance of the open arc between its round ends' centres (356°), as FastHenry sees it with the port closing the loop at no length: Neumann's double integral over the arc with the rectangle's geometric mean distance g = 0.2235 (w + t) (Grover), 55.590 nH ([`../references.py`](../references.py), `arc_inductance`). For scale: Grover's ring formula μ0 R (ln(8R / g) − 2) for the closed ring gives 56.622 nH, and that times the share of the circle the arc covers (0.989) gives 55.991 nH, 0.7 % high, as it misses the ends' effect |
| R at 10 kHz | Re(Z) | the DC resistance of an annular sector between the arc's two ends, θ / (σ t ln(r_out / r_in)): 61.201 mΩ |
| L and R at 3.5 MHz | as above, at the coil boards' frequency, where the skin depth (35 µm) equals the copper's thickness | no exact reference: the same arc integral with a thin strip's high-frequency GMD w / 4 gives 55.04 nH, an estimate that leaves out the current's shift towards the ring's inside edge |
| The filaments | 1, 3, 5, 9 and 15 across the trace, 1 and 3 through its copper, the edge ones twice as narrow as the next in | L and R should settle as the filaments get finer; at 10 kHz to the references, at 3.5 MHz to whatever the crowding to the edges gives |

## How It Runs

```bash
python make_board.py                      # write the board (it is committed)
python simulation.py                      # the filament ladder at both frequencies (about 7 minutes)
python simulation.py --nwinc 9            # 9 filaments across only
python simulation.py --nwinc 9 --nhinc 3  # 9 across and 3 through
python simulation.py --chord-deg 1        # the arcs as chords of at most 1 degree
```

Every setting is in `SETTINGS` at the top of `simulation.py`:

| Setting | Value | Why |
|---|---|---|
| Frequencies | 10 kHz and 3.5 MHz | uniform current, and the coil boards' frequency |
| Filaments | across × through: 1 × 1, 3 × 1, 5 × 1, 9 × 1, 9 × 3, 15 × 3 | the coil boards use 3 × 1; the ladder says what that costs in accuracy |
| Edge grading | each edge filament 2 times narrower than the next one in (FastHenry's `rw` and `rh`) | the current crowds to a trace's edges at 3.5 MHz |
| Chords | at most 5° and 0.5 mm of arc each: 126 segments | an arc's chords are 0.01 % shorter than the arc at 2.9° each |
| Copper | σ = 5.8e7 S/m, 35 µm (KESE's stack-up) | |
| Air | none: FastHenry models only the conductors, and every filament couples to every other through its partial inductance | |
| Solver | FastHenry 3.0.1 (`../../Solver_FastHenry`), `-s ludecomp -m direct -a off`: the dense LU of the whole system | the exact answer of the filament model, with no iteration and no multipole approximation |

## Results

See [results.md](results.md): expected against what came out, and the filament ladder.

## Licence

GPL-3.0, as the rest of this branch.
