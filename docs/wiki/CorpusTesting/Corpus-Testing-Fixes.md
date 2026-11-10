# Corpus Testing: The Failed Boards And Their Fixes

Of the 3,146 boards of [Corpus Testing](../Corpus-Testing.md), 94 did not pass the Verifier in all six runs. This page lists every one of them: what went wrong, whose fault it was (KESE's or the board file's), and what was done about it. The fixes are four commits (`06c8e2b`, `83a8650`, `92a0e9d`, `656c2d5`) on top of the KESE the corpus ran (`main` at 22fd70c, version 2.4.0); every failed run was run again with them on 10 November 2026, with the same settings as the corpus run.

The order is by how much each matters: KESE errors first (KESE stopped and wrote nothing), then Verifier failures that were KESE's, then those that are the board file's, then the runs stopped for memory, and last the files that are not whole boards.

In short, of the 241 failed runs on 94 boards:

| | Boards | Runs |
|---|---:|---:|
| KESE errors, all fixed: now PASS | 3 | 14 |
| Verifier failures that were KESE's, fixed: now PASS | 10 | 30 |
| Runs stopped at the 11 GB cap that pass with a 14.5 GB cap | 39 | 45 |
| Verifier failures that are KESE's, not fixed | 3 | 12 |
| Verifier failures that are the board file's (kept as they are) | 7 | 27 |
| Runs stopped for memory again, to run on a machine with more memory | 38 | 58 |
| Runs stopped for memory, run again but not done at the time of writing | 5 | 7 |
| Files that are not whole boards (kept as they are) | 8 | 48 |

(A board can be in two rows: one run stopped for memory, another failed.) The sub-pages show a run that passes when run again in its board's section, with a "Run again" row that says how; a run that fails again keeps its first result.

## 1. KESE Errors (KESE Stopped)

Three boards, 14 runs. KESE raised an error and wrote no model. Both causes were in GEOS, the geometry library under shapely, on shapes KESE should have kept away from it. Both are fixed in commit `06c8e2b`.

| Board | Runs | What errored | The fix | After the fix |
|---|---|---|---|---|
| loxodes vna `vna_demod` (0590) | all 6 | `GEOSException: TopologyException: Ring edge missing` in a cut on the snapping grid (`shapes2d._overlay`). A copper speck of 2e-24 mm², far smaller than one grid cell, made GEOS's snap rounding fail, and it failed again on the inputs made valid and put on the grid. | `_overlay` tries once more without the parts smaller than a grid cell, which the grid drops anyway. | 6 of 6 PASS |
| loxodes vna `vna_rf` (1231) | all 6 | The same error, the same kind of speck. | The same fix. | 6 of 6 PASS |
| antmicro `d1600e-psu-breakout` (0661) | both visual | GEOS 3.14.1's difference on the grid returned an invalid polygon (a hole nested in a hole) from two valid ones, dropping 0.85 mm² of a visible face; the triangulation then refused it. The float difference of the same shapes is right. | `skin_faces.visible_flats` cuts such a face again in floating point, with only the new vertices put on the grid (`exact_diff`), when the cut on the grid comes back invalid. | 2 of 2 PASS (and the four simulation runs, which passed before, still do) |

## 2. Verifier Failures That Were KESE's

### 2.1 Fixed

| Board | Runs | What failed | Why | The fix | After the fix |
|---|---|---|---|---|---|
| alphaonex86 fpgamotherboard `socket370-ti180` (0028) | 4 simulation | `whole=False` on `Copper_+0V95` and `Copper_+1V1` | The model was right; the Verifier's sum was wrong. Stacked microvias (In2–In3 on top of In3–In4) each plate the In3 foil they share, so two prisms of the part overlap there, and the Verifier added up the prisms one by one, counting each shared ring (5.87e-3 mm² × 0.035 mm) twice. | The Verifier takes a part's prisms per slice as one region when the plain sum is past the limit (`part_checks.volume_check`, commit `83a8650`). | 4 of 4 PASS |
| alphaonex86 fpgamotherboard `socket7-ti180` (0050) | 4 simulation | `whole=False` on four nets | The same stacked microvias. | The same fix. | 4 of 4 PASS |
| rusefi `tle6240_driver` (2209) | 4 simulation | `whole=False` on `Bottom Solder Mask` | The mask's flat and its wall overlap as prisms; counted twice, 1.8e-3 mm³ too much. What is left (9e-4 mm³, a narrow web of mask cut at its pinch points) is within the limit. | The same fix. | 4 of 4 PASS |
| badgeteam `mch2022` (0504) | 4 simulation | `whole=False` on `Top Finish Nickel`: 1.17e-3 mm³ off in all (past the 1e-3 limit), and piece by piece "36 gone" | The pinch cuts take a little from thousands of pads, and 36 specks of nickel of 5e-8 to 1.4e-5 mm² whole. The Verifier failed a part for any piece gone, whatever its size. | A piece of up to `Verifier.VERIFY_GONE_AREA_MM2` (new, 1e-4 mm², a 10 µm square) may be gone; a bigger one still fails the part (commit `83a8650`). **This loosens the Verifier**, by a stated amount, for specks only. | 4 of 4 PASS |
| tinyvision-ai pico2-ice (0850) | 4 simulation | `winding=False` on `Copper_GND` (3 edges) | The ground plane's face, whose rings touch, goes to GEOS's constrained Delaunay triangulation, the last resort. Four points of different holes lie on one 45-degree line, and GEOS gave two triangles of no area stacked along it, wound the wrong way. | Flat triangles are taken out and the triangles beside them split at their points; if that does not close on every edge, GEOS's triangles are kept as they were (`flat_triangles.flats_split_away`, commit `92a0e9d`). | 4 of 4 PASS |
| bluejayracing 22xt `main_board_peripheral_v3` (2304) | both visual | one Verifier ray of 3,000 met the skin once (a crack) | A wall of the visual skin is split at every vertex of the faces at its two heights that lies within ¾ of a grid step of it; the face beside the wall was not. A vertex of the mask's face half a grid step off the ink's edge bent the ink's wall away from the ink's top face, leaving a crack up to 50 nm wide, and a ray fell through it. | The faces take the vertices that lie on their edges, from the faces at their own and the next heights and from the material either side, as the walls do (`skin_vertices.py`, commit `656c2d5`). About 4% more time on a 100 s board. | 2 of 2 PASS |
| bluejayracing 22xt `main_board_peripheral_v3_1` (2358) | both visual | the same crack | The same design. | The same fix. | 2 of 2 PASS |
| rusefi `lambda-x2` (0552) | both visual | one ray met one face | A crack of the same kind. | The same fix. | 2 of 2 PASS |
| OLIMEX iCE40-DAC Rev A1 (1383) | both visual | one ray met four faces | A crack of the same kind. | The same fix. | 2 of 2 PASS |
| softerhardware Hermes-Lite2 `hermeslite` (0388) | both visual | one ray met three faces | A crack of the same kind. | The same fix. | 2 of 2 PASS |

### 2.2 Not Fixed

| Board | Runs | What fails | Why | Why not fixed |
|---|---|---|---|---|
| oresat A3P250 Dev Board (1307) | 4 simulation | `closed=False` on `Top Finish Nickel` and `Bottom Finish Nickel` (17 edges each in four faces) | The board's edge runs a little off the axes. The finish on the castellated pads and the finish on the pads' tops meet along that edge, each put on the grid a step apart, which leaves a needle hole one grid step wide in the nickel. Each pinch cut at the needle's tip opens it further, for all ten rounds ("pinch points left after 10 rounds of cutting"), and two pieces stay touching along a vertical edge. | Filling such needle holes before the pinch cuts fixes this board, but on the MCH2022 badge (0504) the same fill put nickel on a mask sliver lying in such a needle (3e-8 mm³ of overlap), so it was taken back out. A fix needs the finish and the mask to agree on that edge. |
| bwack C64C 250469 (0229) | 4 simulation | `Copper_GND` and `Top Solder Mask` overlap: 2.8e-5 mm³ in 2 places | The ground zone's edge is a 100 mm line 0.127 mm off vertical. The mask's wall beside it moved up to about two grid steps (0.2 µm) into the copper as stage 6 shared vertices between the mask's slices, each move within ¾ of a grid step. The overlap check allows one grid step. | It is a sliver under 0.3 µm wide; a fix belongs in how stage 6 shares vertices along long, slightly slanted edges, which touches every board. |
| Acill A4000 RevB (0015) | 4 simulation | `Top Solder Mask` and `Copper_LRBG_3` overlap: 1.5e-5 mm³ in 2 places | By its shape (a sliver 44 mm long), the same as 0229. | As 0229. |

## 3. Verifier Failures That Are The Board File's

In each of these, copper of two nets lies on top of copper of another in the file itself: two footprints placed on one another, or two vias of different nets in one spot. KiCad's DRC reports these as shorts. KESE models what the file says, and the Verifier rightly finds the two nets' solids overlapping. These boards are kept as they are: the failure is the file's, not KESE's.

| Board | Runs | Where (KiCad coordinates, mm) | What the file has there |
|---|---|---|---|
| ciaa Hardware RX (1789) | 4 simulation | (67.15, 16.50) | Terminal blocks J10 and J11 placed overlapping: J10 pad 1 (net `N-00000409`) and J11 pad 3 (no net), two plated holes 0.06 mm apart. |
| baldengineer Mega-IIe `gd VGC proto pcb` (1519) | 4 simulation | (143.51, 102.87) | Two through-hole pads at the same spot, nets `/UG3-7` and `/VBL.L`. |
| antmicro scalenode-cm4-baseboard (0585) | 4 simulation | (137.41, 83.21) | U4 and U7 placed exactly on top of each other: their TRIM pads (two "unconnected" nets) coincide. |
| flypie NewBrain Original (2290) | 4 simulation | (100.32, 170.52) | C118 pad 2 and C82 pad 1, plated holes 0.25 mm apart with overlapping pads. The file also has no Edge.Cuts outline. |
| rusefi `Breakout_TLE6244` (0515) | 4 simulation | (214.30, 108.84) | A plated hole with no net overlapping a GND plated hole beside it. |
| schlae cm5-reveng (0101) | 4 simulation | (128.38, 64.01) | A GND via and a `CM5_1V8` via 0.056 mm apart. |
| gralco l5-schematic librem5 mainboard, PADS conversion (0020) | 3 simulation | (149.77, 116.06), and 237 more | GND vias and `4G_POWER_KEY` vias about 0.01 mm apart, 238 places: the conversion from PADS left vias of two nets in one spot. (Its OBJ run is a memory stop, below.) |

Every one of these was run again with the fixes (0020 only its STL run, the others take 35 minutes each); each fails as before, as it should. (0515, found later, was run again with them too: 4 of 4 FAIL, as before.)

## 4. Runs Stopped For Memory

110 runs on these machines were stopped once the memory of KESE and its workers passed 11 GB, a cap of the measurement, not of KESE. KESE was not changed for them. They were run again with the same KESE (`main` at 22fd70c) and the same settings, with the cap raised to 14.5 GB:

- 45 runs pass now, and show in their boards' sections.
- 58 runs, on 38 boards, were stopped again: the 16 GB test machines themselves stop a process tree at about 14.3 GB (these peaked at 14.1 to 14.3 GB), below the raised cap, so no higher cap helps on them. Most are the OBJ run of a big board (OBJ writes the most text). They will be run again on a machine with more memory, and their boards' sections say so.
- 7 runs (boards 0008, 0073, 0077, 0091, 0175) were still being run again when this page was written; until then they keep their first result.

The boards stopped again: 0001 (all six runs), 0006, 0007 and 0013 (four or five runs each), 0021, 0022, 0036 and 0008 (two or three), and the simulation OBJ run of 0002, 0003, 0004, 0005, 0009, 0012, 0016, 0017, 0018, 0019, 0020, 0023, 0024, 0025, 0027, 0029, 0030, 0031, 0033, 0034, 0038, 0040, 0042, 0055, 0075, 0093, 0095, 0100, 0102 and 0138.

## 5. Files That Are Not Whole Boards

Eight boards from Wren6991 Snowflake-FPGA's `timelapse` folder (1245, 1250, 1264, 1567, 1715, 2123, 2186, 2365) are snapshots of a board file cut off before its end. KESE stops in all six runs with "the file ends with N parentheses still open: it is cut short (an incomplete download or copy?)", as it should. They are kept as they are, to show a bad input is reported, not modelled.

## How To Check A Fix

The fixes were checked by the full test suite (278 passed, 4 skipped, with new tests for each fix in `tests/test_verifier.py` and `tests/test_degenerate_shapes.py`) and by running every failed run again. The geometry fixes (`92a0e9d`, and `656c2d5`, which changes every visual board's faces) can change boards that passed; only a full corpus run would show none got worse.
