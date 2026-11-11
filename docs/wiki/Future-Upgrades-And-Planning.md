# 25. Future Upgrades And Planning

The project will be upgraded substantially with new features as they are identified along the
way.

## 25.1 Immediate Next Steps

Already known:

- **Validation against measurements is pending.** The models have not yet been compared with
  measured boards or with reference solver results.

## 25.2 Planned Directions

In no fixed order:

- **A web application.**
- **A desktop application.**
- **Maybe a KiCad add-on.**
- **Integration with openEMS** ([openEMS Workflow](OpenEMS-Workflow.md) describes today's manual
  route) **or other solvers.** One way: an openEMS model whose overlapping primitives are settled
  by CSXCAD's priorities, with no booleans, which would skip stages 3, 4 and 6 for openEMS users. It
  is a new output with its own physics checks, and the finish shells and the conformal mask do not
  map onto priorities.
- **A fast view mode.** A third mode, for GLB and OBJ only, that draws each item's faces on its
  own, overlaps and all, as KiCad's 3D viewer does: a big board in seconds instead of minutes, at
  the cost of faces that flicker where they overlap and parts not split per net.
- **Clipper2 for the grid operations that are still slow.** The solder mask's minimum web width,
  the solid beside the outer copper's walls and each net's union in stage 3 could be done by
  Clipper2, on whole numbers of grid steps: measured on the big boards, from 1.4 to about 20 times
  faster at each, but together about 1% of a big board's run. It is a new dependency, and its
  output needs repair where it leaves invalid slivers, spikes or a hole with no outer ring.

| Previous | Next |
|:---|---:|
| [Glossary](Glossary.md) | [Credits](Credits.md) |
