# 24. Future Upgrades And Planning

Planned directions, in no fixed order. Done items are struck through.

| Upgrade | What it would give |
|---|---|
| **Web application** | Upload a `.kicad_pcb`, pick a preset, download the model and view it in the browser, with no Python install. |
| **Desktop application** | The same with a local user interface: parameters as forms, a live preview, batch export. |
| **KiCad add-on** (maybe) | Export straight from pcbnew's menu with the open board, using KiCad's own stack-up and settings. |
| **openEMS integration** | From the exported solids and `materials.json` to a ready openEMS / CSXCAD model: materials, mesh lines on the layer heights, port placement from the layout. See [openEMS Workflow](OpenEMS-Workflow.md). |
| **Other solver integrations** | Import scripts or plug-ins for HFSS, CST, COMSOL, FEKO that assign materials from `materials.json` automatically. |
| Validation against fabricated boards | Measured stack-ups and solver results next to the model, so the defaults become measured values. |
| Component 3D models as an option | The bare board plus the footprints' STEP models, for assembled-board mechanical and thermal work. |
| Rigid-flex and multiple stack-up regions | Boards whose stack-up changes across the outline. |

Ideas and requests are welcome as issues on the repository.

| Previous | Next |
|:---|---:|
| [Immediate Next Steps](Immediate-Next-Steps.md) | [License](License.md) |
