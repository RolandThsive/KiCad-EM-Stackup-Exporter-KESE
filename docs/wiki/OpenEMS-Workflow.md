# 21. openEMS Workflow

openEMS is a free FDTD solver; its geometry front end CSXCAD has no STEP reader but imports STL
files, each into one material. KESE's `openems` preset writes one closed STL per net and per
dielectric, in mm, on KiCad's origin, with `materials.json` carrying εr, tanδ and conductivity.

> [!NOTE]
> This page describes the intended route and a script skeleton built from the CSXCAD Python
> API. A full openEMS simulation of a KESE export, compared against a measurement, is planned
> but has not been done yet. Research underway.

## 21.1 Export

```bash
python run_KESE.py Input/board.kicad_pcb --for openems --verify
```

gives `Output/board/simulation_STL/`:

```text
stl/Board_dielectric_1.stl
stl/Copper_GND.stl
stl/Copper_RF_IN.stl
stl/Copper_no_net.stl
stl/Top_Solder_Mask.stl
stl/Bottom_Solder_Mask.stl
stl/Top_Silkscreen.stl
...
materials.json
parameters.txt
report.txt
```

The preset sets simulation mode, STL, mm, `ORIGIN = "kicad"`, copper per net and dielectrics per
layer, so x in the STL files equals the layout's x in mm and y is the layout's y negated (KiCad's Y axis
points down, KESE's up, with the same origin; `report.txt` names the origin on its `origin:`
line).

Consider before exporting:

- `--set Run.DIELECTRIC_GROUPING=merged` if all dielectrics share one material: one STL instead of
  several.
- The mask and silk STL files exist too; leave them out of the simulation unless their εr matters
  to you, since `materials.json` carries no εr for them.
- `Finish.FINISH_ENABLED` stays off: 80 nm gold cannot be resolved by an FDTD mesh.

## 21.2 Building The CSXCAD Model

For each part in `materials.json`, create one property from its `properties` and import the
STL named in `file_names.stl`. Metals become `AddMetal` (PEC) or a lossy material with
`kappa` = conductivity; dielectrics become `AddMaterial` with `epsilon` and a
`kappa` derived from tanδ at the frequency of interest. FDTD models dielectric loss as a
conductivity, which equals the loss tangent at one frequency:

```math
\kappa = 2 \pi f_0 \varepsilon_0 \varepsilon_r \tan\delta \qquad (21.1)
```

| Symbol | Meaning | Source |
|---|---|---|
| $`\kappa`$ | equivalent conductivity of the dielectric, S/m | |
| $`f_0`$ | frequency at which the loss is matched, Hz | your choice |
| $`\varepsilon_0`$ | vacuum permittivity, $`8.854 \times 10^{-12}`$ F/m | |
| $`\varepsilon_r`$, $`\tan\delta`$ | relative permittivity and loss tangent of the part | `materials.json`: `epsilon_r`, `loss_tangent` |

Example: FR4 with $`\varepsilon_r = 4.5`$, $`\tan\delta = 0.02`$ at $`f_0 = 2.45`$ GHz gives
$`\kappa \approx 0.0123`$ S/m. The loss is exact at $`f_0`$ only; away from it a constant
$`\kappa`$ gives a loss tangent that falls as $`1/f`$.

```python
import json, os
from CSXCAD import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import EPS0

run = "Output/board/simulation_STL"
mats = json.load(open(os.path.join(run, "materials.json")))
f0 = 2.45e9                                  # frequency used to turn tan d into a conductivity
unit = 1e-3                                  # the STL files are in mm (Run.UNITS = "mm")

FDTD = openEMS(NrTS=200000, EndCriteria=1e-4)
FDTD.SetGaussExcite(f0, f0)
FDTD.SetBoundaryCond(["PML_8"] * 6)
CSX = ContinuousStructure()
FDTD.SetCSX(CSX)

for name, part in mats["parts"].items():
    role, pr = part["role"], part["properties"]
    stl = os.path.join(run, "stl", part["file_names"]["stl"])
    if not os.path.exists(stl):
        continue                                          # parts with an empty mesh have no file
    if role in ("copper", "plating"):
        prop = CSX.AddMetal(name)                        # or a lossy metal:
        # prop = CSX.AddMaterial(name, kappa=pr["conductivity_S_per_m"])
    elif role == "board":
        kappa = 2 * 3.141592653589793 * f0 * EPS0 * pr["epsilon_r"] * pr["loss_tangent"]
        prop = CSX.AddMaterial(name, epsilon=pr["epsilon_r"], kappa=kappa)
    else:
        continue                                          # mask, silk: skipped here
    prop.AddPolyhedronReader(stl, priority=10 if role == "board" else 20).ReadFile()

mesh = CSX.GetGrid()
mesh.SetDeltaUnit(unit)
# ... mesh lines, ports and dumps as in any openEMS script ...
```

Points that matter:

- **Priority.** Copper must win over the dielectric where both claim a cell; give the metal
  properties the higher priority, as above.
- **Mesh lines at the copper heights.** `report.txt` lists the z band of every copper layer in
  mm (`F.Cu z +0.8000 .. +0.8350 mm`). Put mesh lines on those values, and on the dielectric
  boundaries, so the 35 µm copper is resolved or, with coarser cells, is at least on a cell
  boundary. openEMS's other way to avoid cells of 35 µm, `AddConductingSheet`, works only on
  flat (2D) shapes: KESE's STL parts are closed solids, so openEMS treats a sheet made from them
  as PEC. To use a conducting sheet, draw the copper as flat polygons at its height instead of
  importing its STL.
- **Units.** `SetDeltaUnit(1e-3)` matches `Run.UNITS = "mm"`. If you exported in metres, use `1`.
- **Ports.** Place them in the layout's coordinates: with `ORIGIN = "kicad"` the x of a pad is the
  same as in KiCad, and y is KiCad's y negated.

## 21.3 Octave / MATLAB

The same route exists with the Octave interface: `ImportSTL(CSX, 'Copper_GND', 20,
'stl/Copper_GND.stl')` after `AddMetal(CSX, 'Copper_GND')`, and `AddMaterial` /
`SetMaterialProperty(CSX, 'Board_dielectric_1', 'Epsilon', 4.5, 'Kappa', kappa)` for the
dielectrics; read the property values from `materials.json` with `jsondecode`.

## 21.4 Checking The Import

- The number of imported STL files should equal the number of parts you kept from
  `materials.json` (a part whose mesh came out empty has an entry but no file).
- View the structure with AppCSXCAD before running: every net should be a separate colour, and
  the vias should pass through the dielectrics.
- Run `--verify` on the export first: an STL that is not closed (`closed=False` in the Verifier)
  will not voxelize correctly.

| Previous | Next |
|:---|---:|
| [KiCad And Solver Compatibility](Compatibility.md) | [Glossary](Glossary.md) |
