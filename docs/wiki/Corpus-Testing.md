# Corpus Testing

Every board in [Credits](Credits.md), 3,100 KiCad boards from 801 open hardware projects, exported by the current KESE once for every file format each mode writes, board by board, in the style of the [Feature Test Collection](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/wiki/Feature-Test-Collection):

- Each board was run six times, **one file format a run**: in simulation mode with GLB, with STEP, with STL and with OBJ, and in visual mode with GLB and with OBJ (visual mode is a surface, not solids, so KESE does not write STEP or STL in it). One format a run gives each format its own time, file size and peak memory.
- Every run had the Verifier, the solder mask and the silkscreen on. Each bar of a board's chart is one stage's seconds in that run, from the `timing` block of [`report.txt`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/wiki/Project-Output-Organization#1122-reporttxt).
- Beside each board's facts, the file each run wrote (STL: all the part files of the run together) and the run's peak memory: the proportional set size (PSS) of KESE and its four workers summed, so shared memory is counted once, sampled every 0.05 s.
- No picture of any board is shown: the boards belong to their authors ([Credits](Credits.md)), and none of them, nor any part of one, is included in KESE.
- The commands, for a board B and a format F (glb, step, stl or obj in simulation mode; glb or obj in visual mode):

```text
python run_KESE.py B --mode simulation --format F --verify \
    --set SolderMask.SOLDER_MASK_ENABLED=True --set Silkscreen.SILKSCREEN_ENABLED=True
python run_KESE.py B --mode visual --format F --verify \
    --set SolderMask.SOLDER_MASK_ENABLED=True --set Silkscreen.SILKSCREEN_ENABLED=True
```

**The runs used KESE version 2.4.0 (`main` at 22fd70c and 39950e6) with the default parameters otherwise and shapely 2.2.0 (GEOS 3.14.1), on a 4-core CPU with 16 GB of RAM, so `Parallel.WORKERS = 0` gave four workers ([Work Done In Parallel](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/wiki/Working-Principle#74-work-done-in-parallel)). A run was stopped after 90 minutes, or once its memory passed 11 GB: that cap is a limit of the measurement, not of KESE, and a board stopped there is left out of the corpus until it passes on a machine with more memory. On another machine the seconds differ.**

**A run that failed was run again on 10 November 2026, with the same settings: one that KESE had got wrong, with the fixes to KESE made for it, and one stopped at the 11 GB cap, with the cap raised to 14.5 GB. A run that passed then shows the new run, and its board says so in a Run again row; a run that failed again keeps its first result.**

3,093 of the 3,100 boards passed the Verifier in all six runs. The 7 others are listed by why under [What Did Not Pass](#what-did-not-pass).

## Grading A Board's Complexity

Each board's Complexity is a grade from 0 to 1000: its **size**, from 0 to 500, plus the **features** of it that KESE models, from 0 to 500. Both are counted from the `.kicad_pcb` file alone, with fixed tops and weights, so any KiCad board can be graded the same way and a board added to the corpus later is graded on this scale.

```text
grade = size + features
```

### The Size

Four counts, each on a log scale with a fixed top:

```text
size = 200 × log10(1 + tracks + 3 × vias) / log10(1 + 200,000)
     + 100 × log10(1 + parts) / log10(1 + 10,000)
     + 100 × log10(1 + 60 × big chips + 150 × BGAs) / log10(1 + 30,000)
     + 100 × log2(copper layers) / 6
```

Each of the four terms is at most its top (200, 100, 100, 100), and the sum is rounded.

- **tracks**: routed copper track segments and arcs. **vias**: vias of every kind.
- **parts**: footprints with two or more pads (mounting holes, fiducials, logos and stitching vias are not counted).
- **big chips**: chips of 32 pads or more in QFP, QFN, BGA, LGA or DIMM-style packages.
- **BGAs**: BGA, LGA or CSP chips of 25 pads or more, counted again on top of the big chips.
- **copper layers**: points as in the table below.

| Copper layers | 1 | 2 | 4 | 6 | 8 | 10 | 12 | 16 | 32 | 64 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Points | 0 | 17 | 33 | 43 | 50 | 55 | 60 | 67 | 83 | 100 |

Ten times the routing adds about 38 to the size, ten times the parts about 25 and ten times the chips about 22.

### The Features

Each feature KESE models that the board uses adds its weight once, however many times it is used. The weights add up to 500: the rarer and harder a feature is to model (vias between inner layers, backdrills, plated edges), the more it weighs.

```text
features = the sum of the weights of the features present
```

| Feature | Present when the file has | Weight | Boards in this corpus |
|---|---|---:|---:|
| Through vias | `(via (at ...` with no type | 15 | 2,712 |
| Blind and buried vias | `(via blind ...`, `(via buried ...` | 40 | 33 |
| Microvias | `(via micro ...` | 40 | 21 |
| Backdrills | `(backdrill ...`, `(tertiary_drill ...` | 40 | 0 |
| Counterbores and countersinks | `(front_post_machining counterbore ...`, and `countersink`, front or back | 25 | 0 |
| Covered, plugged, capped or filled vias | `(covering ...)` or `(plugging ...)` with a `yes`, `(capping yes)`, `(filling yes)` | 30 | 2 |
| Padstacks | `(padstack ...` | 30 | 20 |
| Slotted holes | `(drill oval ...` | 10 | 1,019 |
| Custom pads | a pad of shape `custom` | 15 | 611 |
| Rounded, trapezoid or chamfered pads | a pad of shape `roundrect` or `trapezoid`, or `(chamfer ...` | 10 | 2,279 |
| Drill offsets | `(drill ... (offset ...))` | 10 | 146 |
| Arc tracks | `(arc (start ...` (KiCad 6 and later) | 15 | 373 |
| Filled zones | `(filled_polygon ...` or `(fill_segments ...` | 20 | 2,551 |
| Copper drawings | a `gr_line`, `gr_arc`, `gr_circle`, `gr_rect`, `gr_poly` or `gr_curve` on a copper layer | 10 | 668 |
| Copper text | a `gr_text` on a copper layer | 10 | 475 |
| Curved board outline | an arc, circle or curve on `Edge.Cuts` | 10 | 1,655 |
| Knockout text | `knockout` | 15 | 456 |
| Truetype text | `(face "...")` other than `"KiCad Font"` | 15 | 238 |
| Hatched fills | `(fill hatch)` | 25 | 2 |
| Tracks bare of mask | a `segment` with `(layers "F.Cu" "F.Mask")` or the back's | 15 | 20 |
| Stack-up | `(stackup ...` | 20 | 1,609 |
| Dielectric εr and tanδ | `(epsilon_r ...` | 10 | 1,609 |
| Copper finish | `(copper_finish ...)` other than `None` | 15 | 296 |
| Mask and silkscreen colours | a `(color ...)` on a mask or silkscreen layer of the stack-up | 5 | 527 |
| Castellated pads | `pad_prop_castellated` or `(castellated_pads yes)` | 25 | 16 |
| Plated board edge | `(edge_plating yes)` | 25 | 6 |
| **All** | | **500** | |

In this corpus the grades run from 17 to 651, half the boards below 273: the top of the scale is left for boards larger and richer in features than any here. Each board's section gives its grade as size plus features, and names its features.

## The Boards, By Project

The boards are numbered in order of project and then path, 108 to a page.

| Page | Boards | Projects | Passed all six runs |
|---|---|---:|---:|
| [Corpus Page 1](CorpusTestingPages/Corpus-Testing-01.md) | 1 to 108 | 16 | 108 |
| [Corpus Page 2](CorpusTestingPages/Corpus-Testing-02.md) | 109 to 216 | 3 | 108 |
| [Corpus Page 3](CorpusTestingPages/Corpus-Testing-03.md) | 217 to 324 | 11 | 108 |
| [Corpus Page 4](CorpusTestingPages/Corpus-Testing-04.md) | 325 to 432 | 93 | 107 |
| [Corpus Page 5](CorpusTestingPages/Corpus-Testing-05.md) | 433 to 540 | 20 | 107 |
| [Corpus Page 6](CorpusTestingPages/Corpus-Testing-06.md) | 541 to 648 | 17 | 108 |
| [Corpus Page 7](CorpusTestingPages/Corpus-Testing-07.md) | 649 to 756 | 27 | 107 |
| [Corpus Page 8](CorpusTestingPages/Corpus-Testing-08.md) | 757 to 864 | 33 | 108 |
| [Corpus Page 9](CorpusTestingPages/Corpus-Testing-09.md) | 865 to 972 | 30 | 107 |
| [Corpus Page 10](CorpusTestingPages/Corpus-Testing-10.md) | 973 to 1,080 | 28 | 107 |
| [Corpus Page 11](CorpusTestingPages/Corpus-Testing-11.md) | 1,081 to 1,188 | 21 | 108 |
| [Corpus Page 12](CorpusTestingPages/Corpus-Testing-12.md) | 1,189 to 1,296 | 33 | 108 |
| [Corpus Page 13](CorpusTestingPages/Corpus-Testing-13.md) | 1,297 to 1,404 | 33 | 108 |
| [Corpus Page 14](CorpusTestingPages/Corpus-Testing-14.md) | 1,405 to 1,512 | 24 | 108 |
| [Corpus Page 15](CorpusTestingPages/Corpus-Testing-15.md) | 1,513 to 1,620 | 29 | 108 |
| [Corpus Page 16](CorpusTestingPages/Corpus-Testing-16.md) | 1,621 to 1,728 | 38 | 108 |
| [Corpus Page 17](CorpusTestingPages/Corpus-Testing-17.md) | 1,729 to 1,836 | 44 | 108 |
| [Corpus Page 18](CorpusTestingPages/Corpus-Testing-18.md) | 1,837 to 1,944 | 47 | 108 |
| [Corpus Page 19](CorpusTestingPages/Corpus-Testing-19.md) | 1,945 to 2,052 | 36 | 108 |
| [Corpus Page 20](CorpusTestingPages/Corpus-Testing-20.md) | 2,053 to 2,160 | 26 | 108 |
| [Corpus Page 21](CorpusTestingPages/Corpus-Testing-21.md) | 2,161 to 2,268 | 36 | 108 |
| [Corpus Page 22](CorpusTestingPages/Corpus-Testing-22.md) | 2,269 to 2,376 | 32 | 108 |
| [Corpus Page 23](CorpusTestingPages/Corpus-Testing-23.md) | 2,377 to 2,484 | 15 | 106 |
| [Corpus Page 24](CorpusTestingPages/Corpus-Testing-24.md) | 2,485 to 2,592 | 28 | 108 |
| [Corpus Page 25](CorpusTestingPages/Corpus-Testing-25.md) | 2,593 to 2,700 | 20 | 108 |
| [Corpus Page 26](CorpusTestingPages/Corpus-Testing-26.md) | 2,701 to 2,808 | 32 | 108 |
| [Corpus Page 27](CorpusTestingPages/Corpus-Testing-27.md) | 2,809 to 2,916 | 13 | 108 |
| [Corpus Page 28](CorpusTestingPages/Corpus-Testing-28.md) | 2,917 to 3,024 | 29 | 108 |
| [Corpus Page 29](CorpusTestingPages/Corpus-Testing-29.md) | 3,025 to 3,100 | 10 | 76 |

## What Did Not Pass

Of the 3,100 boards, 7 did not pass in all six runs, none of them for a fault of KESE (each board's section says what stopped it):

- **Bad design according to KESE (7 boards):** the file puts copper of two nets on top of each other, a short KiCad's DRC reports. KESE models what the file says, so the Verifier rightly finds the two nets' solids overlapping: [librem5_mainboard](CorpusTestingPages/Corpus-Testing-10.md#1073-librem5_mainboard), [CM5RevEng](CorpusTestingPages/Corpus-Testing-23.md#2484-cm5reveng), [denso079721_outline-append](CorpusTestingPages/Corpus-Testing-23.md#2431-denso079721_outline-append), [scalenode-cm4-baseboard](CorpusTestingPages/Corpus-Testing-04.md#398-scalenode-cm4-baseboard), [gd VGC proto pcb](CorpusTestingPages/Corpus-Testing-05.md#512-gd-vgc-proto-pcb), [.kicad_pcb](CorpusTestingPages/Corpus-Testing-07.md#744-kicad_pcb), [NewBrain Original](CorpusTestingPages/Corpus-Testing-09.md#970-newbrain-original).
- **Failed because of KESE:** none.
