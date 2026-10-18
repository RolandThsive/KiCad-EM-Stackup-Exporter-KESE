# 23. Immediate Next Steps

KESE is developed in the open and in use on real boards. The project will be upgraded
substantially with new features as they are identified along the way: each board that goes
through it shows the next thing to model, and that goes in next.

What is in front right now:

- **Validation against measurements.** Compare the model of a fabricated board with the
  measured board (cross-sections, thicknesses) and with reference solver results, and record the
  outcome here. Until then every dimension is a model value.
- **Pictures for this wiki.** Overview and feature pictures made from KESE's own output.
- **Items not yet modelled**, in the order they come up on real boards: text boxes and
  dimensions on physical layers, footprint 3D models as an option, rigid-flex stack-ups.
- **More boards in the regression suite**, so that a fix for one board cannot silently change
  another.

Found something missing on your board? Open an issue on the repository with the `.kicad_pcb`
file and the `report.txt` of the run.

| Previous | Next |
|:---|---:|
| [Glossary](Glossary.md) | [Future Upgrades And Planning](Future-Upgrades-And-Planning.md) |
