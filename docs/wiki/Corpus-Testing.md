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

The runs are under way: 984 of the 3,146 boards are done so far. A sub-page is added once all its boards are done.

The complexity of each board is the corpus's score: tracks, plus 3 for each via, 2 for each part with two or more pads, 60 for each chip of 32 pads or more and 150 more for each BGA, scaled down in proportion for a board of fewer than 10 parts.

## The Boards, By Project

| Page | Projects | Boards | Boards run | Passed all six runs |
|---|---|---:|---:|---:|
| [Corpus Testing 1: 01GOD To alphaonex86](CorpusTesting/Corpus-Testing-01.md) | 14 | 104 | 104 | 99 |
| [Corpus Testing 2: alvaroalea To andrewpaterson](CorpusTesting/Corpus-Testing-02.md) | 6 | 201 | 201 | 200 |
| Corpus Testing 3: antevens To antmicro (running) | 81 | 100 | 99 | 91 |
| Corpus Testing 4: antmicro To baldengineer (running) | 35 | 121 | 116 | 109 |
| Corpus Testing 5: Bambelweeny57 To Board-Folk (running) | 22 | 103 | 91 | 89 |
| Corpus Testing 6: Board-Folk To cheyao (running) | 26 | 104 | 88 | 84 |
| Corpus Testing 7: chipfoundry To DangerousPrototypes (running) | 19 | 104 | 87 | 84 |
| Corpus Testing 8: DangerousPrototypes To epsilon0-dev (running) | 43 | 101 | 65 | 61 |
| Corpus Testing 9: esden To ghent360 (running) | 24 | 103 | 55 | 52 |
| Corpus Testing 10: gitRaksha To greatscottgadgets (running) | 19 | 111 | 33 | 32 |
| Corpus Testing 11: greatscottgadgets To intergalaktik (running) | 34 | 102 | 18 | 18 |
| Corpus Testing 12: intergalaktik To issuiuc (running) | 16 | 103 | 15 | 13 |
| Corpus Testing 13: istedman To KiCad (running) | 36 | 105 | 6 | 6 |
| Corpus Testing 14: kitspace-forks To loxodes (running) | 20 | 124 | 2 | 2 |
| Corpus Testing 15: ltbrain To mwelling (running) | 42 | 100 | 4 | 3 |
| Corpus Testing 16: mwelling To nuclearfutureslab (running) | 34 | 101 | 0 | 0 |
| Corpus Testing 17: NUSGreyhats To OLIMEX (running) | 34 | 103 | 0 | 0 |
| Corpus Testing 18: OLIMEX To OLIMEX (running) | 53 | 100 | 0 | 0 |
| Corpus Testing 19: OLIMEX To open-ephys (running) | 32 | 100 | 0 | 0 |
| Corpus Testing 20: open-ephys To oresat (running) | 22 | 104 | 0 | 0 |
| Corpus Testing 21: oresat To pms67 (running) | 33 | 100 | 0 | 0 |
| Corpus Testing 22: polpo To rh1tech (running) | 31 | 108 | 0 | 0 |
| Corpus Testing 23: rhaamo To rusefi (running) | 12 | 114 | 0 | 0 |
| Corpus Testing 24: rusefi To sparkfun (running) | 30 | 111 | 0 | 0 |
| Corpus Testing 25: sparkfun To sufst (running) | 21 | 115 | 0 | 0 |
| Corpus Testing 26: SukkoPera To tjeerdie (running) | 29 | 102 | 0 | 0 |
| Corpus Testing 27: tjhorner To tzarc (running) | 13 | 105 | 0 | 0 |
| Corpus Testing 28: ucdfs To Wren6991 (running) | 29 | 181 | 0 | 0 |
| Corpus Testing 29: xesscorp To ZeroPhone (running) | 9 | 16 | 0 | 0 |

| Previous | Next |
|:---|---:|
| [Feature Test Collection](Feature-Test-Collection.md) | [openEMS Workflow](OpenEMS-Workflow.md) |
