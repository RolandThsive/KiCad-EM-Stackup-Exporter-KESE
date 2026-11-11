# 25. Future Upgrades And Planning

The project will be upgraded substantially with new features as they are identified along the
way.

The work is in three groups, in this order: how exact the model is, how fast and how large the
exports are, and the tools around the generator. Nothing here is built yet. An EM solver of KESE's
own is not planned: the geometry and the materials have to be shown correct first.

## 25.1 Where The Project Stands

| What is checked | Today | How |
|---|---|---|
| Reading the board file | tested | The [Feature Test Collection](Feature-Test-Collection.md), KiCad 4 to 10 ([Compatibility](Compatibility.md)), and the open hardware boards of [Corpus Testing](Corpus-Testing.md) |
| The solids | tested | The Verifier on every run: closed, wound one way, no two parts overlapping, volumes agreeing ([Checks, Errors And Warnings](Checks-Errors-And-Warnings.md)) |
| The EM result a solver gets from the model | **not yet checked** | No model has been compared with a measured board or with a reference solver result |
| The material numbers | typical values, the same at every frequency | The stack-up's or the defaults of [Material Properties](Material-Properties.md#213-the-default-numbers); copper roughness is 0 unless set |

So a model from KESE is known to be the geometry the board file describes, as closed solids. It is
not yet known how close a simulation of it comes to the fabricated board. [25.2](#252-model-accuracy)
is the work that closes this gap.

## 25.2 Model Accuracy

### 25.2.1 Every Ply As Its Own Solid

- **Today:** a gap between two copper layers that holds several plies (two prepregs, or prepreg +
  core + prepreg) becomes one dielectric solid with the summed thickness and the **first** ply's
  type, material, εr and tanδ ([Stack-Up Model](Stack-Up-Model.md)). Where the plies differ, the
  other plies' properties are lost.
- **Planned:** one solid per ply, each with its own thickness, material, εr and tanδ in
  `materials.json`. Plies of the same material may still be joined, as a setting, to keep the part
  count down.
- **Where:** `one_per_gap()` in `Generator/kese/s2_collect/stackup.py` joins the plies. The
  heights (`s3_resolve/heights.py`), the cuts of drills and machining (`s3_resolve/machining.py`),
  the laminate's prisms and the resin beside inner copper (`s4_geometry/laminate.py`) and the
  report (`s9_report/report.py`) all count one dielectric per gap and have to count plies instead.
- **Open questions:** which ply's resin fills the band beside inner copper when the plies on its
  two sides differ, and how very thin plies are kept.
- **Done when:** a feature test board with mixed plies in one gap exports one solid per ply, the
  Verifier passes it, the plies' thicknesses add up to the gap, and every board of the corpus
  that has no mixed gap gives the volumes it gives today.

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

- **Today:** one εr and one tanδ per dielectric, with no frequency beside them, and one
  conductivity and one roughness number per copper part (`Copper.COPPER_SURFACE_ROUGHNESS_UM`,
  0 by default, which means a perfectly smooth conductor). These are typical values, not measured
  ones.
- **Planned:** `materials.json` able to carry, for each dielectric, the frequency its εr and tanδ
  were measured at, or a table of them over frequency, or the parameters of a wideband model
  (Djordjevic-Sarkar is the usual one for laminates); and for copper, the roughness model and its
  parameters (Hammerstad or Huray) per foil side. KESE keeps handing these to the solver: it does
  not apply them itself.
- **Also:** properties for the solder mask and the silkscreen, which carry none today, and the
  resin-rich band beside inner copper, whose εr differs from the glass-filled ply it comes from.
- **Done when:** the values measured in [25.2.2](#2522-comparison-with-measured-boards-and-reference-solvers)
  can be entered once and reach the solver without editing by hand.

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
| [Glossary](Glossary.md) | [License](License.md) |
