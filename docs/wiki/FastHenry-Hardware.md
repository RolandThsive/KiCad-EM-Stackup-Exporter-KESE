# 59. FastHenry Hardware

What FastHenry needed on the test machine, how to estimate a board of your own before you run it, and why every
board of this category fitted a small machine.

## 59.1 The Test Machine

| Item | Value |
|---|---|
| Processor | 4 cores |
| Memory | 15 GB |
| System | Ubuntu 24.04 |
| FastHenry | 3.0.1, the committed build ([FastHenry Installation](FastHenry-Installation.md)) |
| Solve | the dense direct solve (`-s ludecomp -m direct -a off`), one core per solve |

## 59.2 What Grows With What

FastHenry's direct solve holds the dense matrix of every filament's coupling to every other, so its **memory grows
with the square of the filaments and its time with their cube**. The air takes nothing: there is no mesh outside the
copper. The filaments come from the copper alone: every segment times the filaments across and through it, plus one
per rotor bar. The bridge reads FastHenry's peak memory from Linux while it runs and writes it, with the time, into
every results file.

## 59.3 Memory And Time, Measured

On the proof boards, each rung of the filament ladder, one solve per frequency:

| Run | Filaments | Peak memory | Time a solve |
|---|---|---|---|
| E01, 1 × 1 to 9 × 1 | 126 to 1,134 | 0.08 GB | 0.01 to 0.6 s |
| E01, 9 × 3 | 3,402 | 0.31 GB | 28 to 29 s |
| E01, 15 × 3 | 5,670 | 0.82 GB | 2.8 to 3.2 min |
| E02, 1 × 1 to 5 × 1 | 252 to 1,260 | 0.08 GB | 0.04 to 0.7 s |
| E02, 9 × 1 | 2,268 | 0.12 GB | 7 s |
| E02, 9 × 3 | 6,804 | 1.10 GB | 5.2 to 5.3 min |

On `S0d2_1x_OD23_2L_tiny_TX3top_Cut`, 3 filaments across each track and the rotor's 4,542 bars, every air gap:

| Air gap | Filaments | Rotor bars | Memory a solve | Time a solve |
|---|---|---|---|---|
| 0.1 mm | 9,264 | 4,542 | 1.1 GB | 3.1 to 4.3 min |
| 0.5 mm | 9,264 | 4,542 | 1.1 GB | 2.9 to 5.9 min |
| 1 mm | 9,264 | 4,542 | 1.1 GB | 3.4 to 5.6 min |
| 1.5 mm | 9,264 | 4,542 | 1.1 GB | 2.9 to 4.3 min |
| 2 mm | 9,264 | 4,542 | 1.1 GB | 3.2 to 4.0 min |
| Rotor away (1 mm results) | 4,722 | | 0.46 GB | 36 s |

Building the model takes under 2 s. The 81 solves took 5.5 hours of one core in all; `--jobs` runs several angles at
once, one core each, and at 1.1 GB a solve the 15 GB machine holds four. The air gap does not change the size: the
same filaments, only the rotor raised.

## 59.4 Estimating A Board

| Quantity | How to get it | S0d2 at 1 mm |
|---|---|---|
| Filaments | build the model alone: `simulation.py --model-only` prints them; `new_coil.py` does it when it sets a board up | 9,264 |
| Memory | about 0.0158 GB × (filaments / 1000)², the fit `new_coil.py` uses | 1.36 GB, against 1.14 GB measured |
| Time | about 0.0051 min × (filaments / 1000)³ on one core, the same fit | 4.1 min, against 3.4 to 5.6 min measured |
| Solves | one per frequency on the proof boards; one per rotor angle per air gap, and one with the rotor away, on a coil board | 16 per gap and 1 away |

The two constants were fitted to the coil boards' solves (6,555 to 9,306 filaments). The proof boards' runs with 3
filaments through the copper took more than the fit says (E02 at 9 × 3, 6,804 filaments: 1.10 GB and 5.2 min,
against 0.73 GB and 1.6 min), so read the fit for coil boards and check any other board with `--model-only` and one
solve first.

## 59.5 Larger Boards

Twice the filaments is four times the memory and eight times the time, so the dense direct solve has a size it does
not pass: by the fit above, 25,000 filaments would take about 10 GB and 80 min a solve. Three ways keep a board under
it:

| Way | What it gives | What it costs |
|---|---|---|
| A coarser rotor grid (`--rotor-edge`, `--rotor-max`) | fewer rotor bars, which are about half the coil board's filaments | a finer grid than the coil board's moved M by 0.04 % ([FastHenry Accuracy](FastHenry-Accuracy.md#584-the-coil-board)) |
| Fewer filaments across each track | about a third of the stator's filaments at 1 across instead of 3 | M by 0.2 %, and R loses the crowding to the edges |
| FastHenry's multipole solve (its default) | far less memory and time on large boards | iterative: on the coil boards it left M to and from the TX 2.7 % apart, so the bridge does not use it |

| Previous | Next |
|:---|---:|
| [FastHenry Accuracy](FastHenry-Accuracy.md) | [FastHenry Troubleshooting](FastHenry-Troubleshooting.md) |
