# 23. Corpus Testing

Every board in [Credits](Credits.md), 3,146 KiCad boards from 819 open hardware projects, exported by the current KESE once for every file format each mode writes, board by board, in the style of the [Feature Test Collection](Feature-Test-Collection.md):

- Each board was run six times, **one file format a run**: in simulation mode with GLB, with STEP, with STL and with OBJ, and in visual mode with GLB and with OBJ (visual mode is a surface, not solids, so KESE does not write STEP or STL in it). One format a run gives each format its own time, file size and peak memory.
- Every run had the Verifier, the solder mask and the silkscreen on. Each bar of a board's chart is one stage's seconds in that run, from the `timing` block of [`report.txt`](Project-Output-Organization.md#2022-reporttxt).
- Beside each board's facts, the file each run wrote (STL: all the part files of the run together) and the run's peak memory: the proportional set size (PSS) of KESE and its four workers summed, so shared memory is counted once, sampled every 0.05 s.
- No picture of any board is shown: the boards belong to their authors ([Credits](Credits.md)), and none of them, nor any part of one, is included in KESE.
- The commands, for a board B and a format F (glb, step, stl or obj in simulation mode; glb or obj in visual mode):

```text
python run_KESE.py B --mode simulation --format F --verify \
    --set SolderMask.SOLDER_MASK_ENABLED=True --set Silkscreen.SILKSCREEN_ENABLED=True
python run_KESE.py B --mode visual --format F --verify \
    --set SolderMask.SOLDER_MASK_ENABLED=True --set Silkscreen.SILKSCREEN_ENABLED=True
```

**The runs used KESE version 2.4.0 (`main` at 22fd70c) with the default parameters otherwise and shapely 2.2.0 (GEOS 3.14.1), spread over several Linux machines with 4 cores each (Intel(R) Xeon(R) Processor @ 2.10GHz) and 16 GB of RAM, so `Parallel.WORKERS = 0` gave four workers ([Work Done In Parallel](Working-Principle.md#74-work-done-in-parallel)). A run was stopped after 90 minutes, or once its memory passed 11 GB: that cap is a limit of the measurement on these 15 GB machines, not of KESE, and a board stopped there needs a machine with more memory. On another machine the seconds differ.**

**A run that failed was run again on 10 November 2026, with the same settings: one that KESE had got wrong, with the fixes to KESE made for it, and one stopped at the 11 GB cap, with the cap raised to 14.5 GB. A run that passed then shows the new run, and its board says so in a Run again row; a run that failed again keeps its first result.**

3,087 of the 3,146 boards passed the Verifier in all six runs.

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
| Through vias | `(via (at ...` with no type | 15 | 2,753 |
| Blind and buried vias | `(via blind ...`, `(via buried ...` | 40 | 43 |
| Microvias | `(via micro ...` | 40 | 22 |
| Backdrills | `(backdrill ...`, `(tertiary_drill ...` | 40 | 0 |
| Counterbores and countersinks | `(front_post_machining counterbore ...`, and `countersink`, front or back | 25 | 0 |
| Covered, plugged, capped or filled vias | `(covering ...)` or `(plugging ...)` with a `yes`, `(capping yes)`, `(filling yes)` | 30 | 2 |
| Padstacks | `(padstack ...` | 30 | 21 |
| Slotted holes | `(drill oval ...` | 10 | 1,041 |
| Custom pads | a pad of shape `custom` | 15 | 627 |
| Rounded, trapezoid or chamfered pads | a pad of shape `roundrect` or `trapezoid`, or `(chamfer ...` | 10 | 2,321 |
| Drill offsets | `(drill ... (offset ...))` | 10 | 149 |
| Arc tracks | `(arc (start ...` (KiCad 6 and later) | 15 | 383 |
| Filled zones | `(filled_polygon ...` or `(fill_segments ...` | 20 | 2,590 |
| Copper drawings | a `gr_line`, `gr_arc`, `gr_circle`, `gr_rect`, `gr_poly` or `gr_curve` on a copper layer | 10 | 687 |
| Copper text | a `gr_text` on a copper layer | 10 | 489 |
| Curved board outline | an arc, circle or curve on `Edge.Cuts` | 10 | 1,676 |
| Knockout text | `knockout` | 15 | 459 |
| Truetype text | `(face "...")` other than `"KiCad Font"` | 15 | 241 |
| Hatched fills | `(fill hatch)` | 25 | 2 |
| Tracks bare of mask | a `segment` with `(layers "F.Cu" "F.Mask")` or the back's | 15 | 20 |
| Stack-up | `(stackup ...` | 20 | 1,625 |
| Dielectric εr and tanδ | `(epsilon_r ...` | 10 | 1,625 |
| Copper finish | `(copper_finish ...)` other than `None` | 15 | 302 |
| Mask and silkscreen colours | a `(color ...)` on a mask or silkscreen layer of the stack-up | 5 | 535 |
| Castellated pads | `pad_prop_castellated` or `(castellated_pads yes)` | 25 | 16 |
| Plated board edge | `(edge_plating yes)` | 25 | 6 |
| **All** | | **500** | |

In this corpus the grades run from 17 to 651, half the boards below 275: the top of the scale is left for boards larger and richer in features than any here. Each board's section gives its grade as size plus features, and names its features.

## The Boards, By Project

| Page | Projects | Boards | Boards run | Passed all six runs |
|---|---|---:|---:|---:|
| [Corpus Testing 1: 01GOD To alphaonex86](CorpusTesting/Corpus-Testing-01.md) | 14 | 104 | 104 | 101 |
| [Corpus Testing 2: alvaroalea To andrewpaterson](CorpusTesting/Corpus-Testing-02.md) | 6 | 201 | 201 | 200 |
| [Corpus Testing 3: antevens To antmicro](CorpusTesting/Corpus-Testing-03.md) | 81 | 100 | 100 | 95 |
| [Corpus Testing 4: antmicro To baldengineer](CorpusTesting/Corpus-Testing-04.md) | 35 | 121 | 121 | 117 |
| [Corpus Testing 5: Bambelweeny57 To Board-Folk](CorpusTesting/Corpus-Testing-05.md) | 22 | 103 | 103 | 102 |
| [Corpus Testing 6: Board-Folk To cheyao](CorpusTesting/Corpus-Testing-06.md) | 26 | 104 | 104 | 101 |
| [Corpus Testing 7: chipfoundry To DangerousPrototypes](CorpusTesting/Corpus-Testing-07.md) | 19 | 104 | 104 | 101 |
| [Corpus Testing 8: DangerousPrototypes To epsilon0-dev](CorpusTesting/Corpus-Testing-08.md) | 43 | 101 | 101 | 99 |
| [Corpus Testing 9: esden To ghent360](CorpusTesting/Corpus-Testing-09.md) | 24 | 103 | 103 | 101 |
| [Corpus Testing 10: gitRaksha To greatscottgadgets](CorpusTesting/Corpus-Testing-10.md) | 19 | 111 | 111 | 109 |
| [Corpus Testing 11: greatscottgadgets To intergalaktik](CorpusTesting/Corpus-Testing-11.md) | 34 | 102 | 102 | 99 |
| [Corpus Testing 12: intergalaktik To issuiuc](CorpusTesting/Corpus-Testing-12.md) | 16 | 103 | 103 | 97 |
| [Corpus Testing 13: istedman To KiCad](CorpusTesting/Corpus-Testing-13.md) | 36 | 105 | 105 | 102 |
| [Corpus Testing 14: kitspace-forks To loxodes](CorpusTesting/Corpus-Testing-14.md) | 20 | 124 | 124 | 124 |
| [Corpus Testing 15: ltbrain To mwelling](CorpusTesting/Corpus-Testing-15.md) | 42 | 100 | 100 | 100 |
| [Corpus Testing 16: mwelling To nuclearfutureslab](CorpusTesting/Corpus-Testing-16.md) | 34 | 101 | 101 | 98 |
| [Corpus Testing 17: NUSGreyhats To OLIMEX](CorpusTesting/Corpus-Testing-17.md) | 34 | 103 | 103 | 103 |
| [Corpus Testing 18: OLIMEX To OLIMEX](CorpusTesting/Corpus-Testing-18.md) | 53 | 100 | 100 | 100 |
| [Corpus Testing 19: OLIMEX To open-ephys](CorpusTesting/Corpus-Testing-19.md) | 32 | 100 | 100 | 100 |
| [Corpus Testing 20: open-ephys To oresat](CorpusTesting/Corpus-Testing-20.md) | 22 | 104 | 104 | 103 |
| [Corpus Testing 21: oresat To pms67](CorpusTesting/Corpus-Testing-21.md) | 33 | 100 | 100 | 100 |
| [Corpus Testing 22: polpo To rh1tech](CorpusTesting/Corpus-Testing-22.md) | 31 | 108 | 108 | 108 |
| [Corpus Testing 23: rhaamo To rusefi](CorpusTesting/Corpus-Testing-23.md) | 12 | 114 | 114 | 109 |
| [Corpus Testing 24: rusefi To sparkfun](CorpusTesting/Corpus-Testing-24.md) | 30 | 111 | 111 | 110 |
| [Corpus Testing 25: sparkfun To sufst](CorpusTesting/Corpus-Testing-25.md) | 21 | 115 | 115 | 114 |
| [Corpus Testing 26: SukkoPera To tjeerdie](CorpusTesting/Corpus-Testing-26.md) | 29 | 102 | 102 | 100 |
| [Corpus Testing 27: tjhorner To tzarc](CorpusTesting/Corpus-Testing-27.md) | 13 | 105 | 105 | 105 |
| [Corpus Testing 28: ucdfs To Wren6991](CorpusTesting/Corpus-Testing-28.md) | 29 | 181 | 181 | 173 |
| [Corpus Testing 29: xesscorp To ZeroPhone](CorpusTesting/Corpus-Testing-29.md) | 9 | 16 | 16 | 16 |

| Previous | Next |
|:---|---:|
| [Feature Test Collection](Feature-Test-Collection.md) | [openEMS Workflow](OpenEMS-Workflow.md) |
