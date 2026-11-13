# 25. Future Upgrades And Planning

The project will be upgraded substantially with new features as they are identified along the
way.

The work is in three groups, in this order: how exact the model is, how fast and how large the
exports are, and the tools around the generator. Two parts of the first group are built: every
ply as its own solid ([25.2.1](#2521-every-ply-as-its-own-solid)) and material data that depends
on frequency ([25.2.3](#2523-material-data-that-depends-on-frequency)). The rest is not built yet.
An EM solver of KESE's own is not planned: the geometry and the materials have to be shown
correct first.

## 25.1 Where The Project Stands

| What is checked | Today | How |
|---|---|---|
| Reading the board file | tested | The [Feature Test Collection](Feature-Test-Collection.md), KiCad 4 to 10 ([Compatibility](Compatibility.md)), and the open hardware boards of [Corpus Testing](Corpus-Testing.md) |
| The solids | tested | The Verifier on every run: closed, wound one way, no two parts overlapping, volumes agreeing ([Checks, Errors And Warnings](Checks-Errors-And-Warnings.md)) |
| The EM result a solver gets from the model | **not yet checked** | No model has been compared with a measured board or with a reference solver result |
| The material numbers | typical values, with their frequency and a model of how they change with it | The stack-up's or the defaults of [Material Properties](Material-Properties.md#213-the-default-numbers); they are not measured values, and the copper roughness is a solver's starting values, not a foil's |

So a model from KESE is known to be the geometry the board file describes, as closed solids. It is
not yet known how close a simulation of it comes to the fabricated board. [25.2](#252-model-accuracy)
is the work that closes this gap.

## 25.2 Model Accuracy

### 25.2.1 Every Ply As Its Own Solid

**Built.** `Stackup.FUSION_BUILD` in `parameters/PCB_elements/Stackup.py` picks one of two
stack-ups ([Stack-Up Model](Stack-Up-Model.md), [Board](Board.md#121-dielectric-solids)):

- **`"PLIES_FUSED"`:** a gap between two copper layers is one dielectric solid, as
  before, so with it every board gives the files it gave before. The plies it was fused from are now
  listed under it in `materials.json` and `report.txt`, and `Board.FUSED_PROPERTIES = "series"`
  gives the solid the εr and tanδ of its plies in series instead of the first ply's.
- **`"PLIES_SEPARATE"`, the default:** one solid per prepreg ply and per core, each with its own thickness,
  material, εr and tanδ, and one solid for the resin beside each inner copper layer.
  `Board.JOIN_EQUAL_PLIES = True` joins neighbouring plies of the same material and values, to
  keep the part count down.
- **The two open questions:** the resin beside an inner copper layer flows from the prepreg next
  to it (the one below when a core is above, else the one above) and, with the plies separate, is
  a solid of its own with the values of the resin without its glass (`Board.RESIN_EPSILON_R`,
  `Board.RESIN_LOSS_TANGENT`). A ply thinner than `Board.PLY_MIN_THICKNESS_MM` (1 µm) is joined
  to its thicker neighbour, with a warning.
- **Plies the board file does not hold** can be written by hand for one board in
  `Board.PLIES_BY_HAND`.
- **Checked by** the feature test boards 29, 29b, 29c and 29d
  ([Feature Test Collection](Feature-Test-Collection.md)): each exports one solid per ply, the
  Verifier passes it, and the plies' thicknesses add up to their gap (`tests/test_plies.py`,
  `tests/test_plies_built.py`).

### 25.2.2 Comparison With Measured Boards And Reference Solvers

- **Today:** not done. The routes into openEMS, and into Elmer and CalculiX through FreeCAD, are
  also still to be confirmed on each tool ([openEMS Workflow](OpenEMS-Workflow.md)).
- **Planned:** a small set of test structures, designed in KiCad, exported by KESE, simulated, and
  compared with two things: the same structure in an independent reference solver, and the
  fabricated board measured with a vector network analyser (S-parameters) and, for impedance, a
  time domain reflectometer.
- **Structures, simplest first:** a microstrip line and a stripline of known length; a coupled
  (differential) pair; a through via between two lines, with and without a stub; a ring or line
  resonator, which gives εr and tanδ at its resonances; a grounded coplanar line with a via fence;
  an edge-plated board edge.
- **What is compared:** impedance, phase (so effective εr), insertion loss per length, return
  loss, and resonant frequencies, each with the measurement's own uncertainty beside it. The
  fabricated boards' cross-sections (trace width and etch angle, copper and dielectric thickness)
  are measured too, so a difference can be put down to the model or to the fabrication.
- **Done when:** the results are a wiki page with the boards, the measurements and the scripts in
  the repository, and each disagreement beyond the uncertainty is either corrected in KESE or
  written down as a known limit.

### 25.2.3 Material Data That Depends On Frequency

**Built**, as data handed to the solver: KESE does not apply any of it itself
([Material Properties](Material-Properties.md)).

- **Dielectrics:** `materials.json` carries, for every laminate solid and every ply, the
  frequency its εr and tanδ are given at (`spec_frequency_hz`) and a `dielectric_model`:
  `constant`, the fitted parameters of the Djordjevic-Sarkar model, or a table of εr and tanδ
  over frequency (`Board.DIELECTRIC_MODEL`, or the board file's own model and frequency).
- **Copper:** for every layer of a copper part its foil, its plating, its etch factor and which
  face is the treated one, and a roughness model with its parameters for the treated and the
  other face: Hammerstad or Huray (`Copper.COPPER_ROUGHNESS_MODEL`).
- **Also:** an εr and tanδ for the solder mask (the board file's, else `SolderMask.MASK_EPSILON_R`
  and `MASK_LOSS_TANGENT`), for the silkscreen (`SilkScreen.SILK_EPSILON_R`, `SILK_LOSS_TANGENT`)
  and for the resin beside inner copper.
- **Still open:** the numbers are typical values or best guesses. The resin's, the ink's and the
  roughness parameters have no maker's data sheet behind them yet, and nothing is measured:
  the values measured in [25.2.2](#2522-comparison-with-measured-boards-and-reference-solvers)
  are to be entered here once they exist. One table serves every dielectric of a board; a table
  per material is not built.

## 25.3 Speed And Output Size

The corpus runs give the sizes and times of real boards on a 4-core machine
([Corpus Testing](Corpus-Testing.md)). In simulation mode, about:

| File | Half the boards are under | One board in ten is over | Largest |
|---|---:|---:|---:|
| GLB | 39 MB | 230 MB | 1.8 GB |
| STEP | 177 MB | 950 MB | 5.6 GB |
| STL | 58 MB | 340 MB | 2.2 GB |
| OBJ | 115 MB | 640 MB | 1.9 GB |

Half the boards take under 15 s for a run, one in ten over 70 to 90 s, and the largest over half
an hour. The models are correct at these sizes, but a mesher or a solver may not open a file of
several gigabytes. On the three [example boards](Time-Distribution.md) stage 4 (geometry) and
stage 6 (assemble) take most of the time, and STEP and OBJ are the slow formats to write.

- **Fewer faces for the same shape.** Find where a part carries more triangles or STEP faces than
  its shape needs (candidates: flat faces split more than needed, side walls split at every
  height, arcs kept as many short chords) and join them, with the Verifier's volumes unchanged.
- **A smaller STEP file.** Share points, edges and surfaces that parts have in common, write more
  round shapes as exact circles and cylinders instead of facets, and measure what each saves.
- **A setting for the level of detail.** One setting that coarsens what matters least to the
  fields (chords of arcs far from any gap, text, silkscreen) and never what matters most (trace
  width, gaps, dielectric thickness, via barrels), with the change in copper volume reported.
- **Exporting a part of a board.** A region, a set of nets or a set of layers, so a solver gets
  the structure under study and not the whole board.
- **Clipper2 for the grid operations that are still slow.** The solder mask's minimum web width,
  the solid beside the outer copper's walls and each net's union in stage 3 could be done by
  Clipper2, on whole numbers of grid steps: measured on the big boards, from 1.4 to about 20 times
  faster at each, but together about 1% of a big board's run. It is a new dependency, and its
  output needs repair where it leaves invalid slivers, spikes or a hole with no outer ring.
- **A fast view mode.** A third mode, for GLB and OBJ only, that draws each item's faces on its
  own, overlaps and all, as KiCad's 3D viewer does: a big board in seconds instead of minutes, at
  the cost of faces that flicker where they overlap and parts not split per net.
- **Done when:** each change is measured on the same corpus boards, with size, time and peak
  memory before and after on this page, and all boards still pass the Verifier.

## 25.4 Planned Directions

In no fixed order:

- **A web application.**
- **A desktop application.**
- **Maybe a KiCad add-on.**
- **Integration with openEMS** ([openEMS Workflow](OpenEMS-Workflow.md) describes today's manual
  route) **or other solvers.** One way: an openEMS model whose overlapping primitives are settled
  by CSXCAD's priorities, with no booleans, which would skip stages 3, 4 and 6 for openEMS users. It
  is a new output with its own physics checks, and the finish shells and the conformal mask do not
  map onto priorities.

| Previous | Next |
|:---|---:|
| [Glossary](Glossary.md) | [Real PCB Stackup](Real-PCB-Stackup.md) |
