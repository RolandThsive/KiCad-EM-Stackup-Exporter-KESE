# 23. openEMS Workflow

openEMS is a free FDTD solver; its geometry front end CSXCAD has no STEP reader but imports STL
files, each into one material. KESE's `openems` preset writes one closed STL per net and per
dielectric, in mm, on KiCad's origin, with `materials.json` carrying εr, tanδ, the frequency they
were measured at, how they change with frequency, and the copper's conductivity.

> [!NOTE]
> This page describes the intended route and a script skeleton built from the CSXCAD Python
> API. A full openEMS simulation of a KESE export, compared against a measurement, is planned
> but has not been done yet. Research underway.

## 23.1 Export

```bash
cd Generator
python run_KESE.py Input/board.kicad_pcb --for openems --verify
```

gives `Output/board/simulation_STL/`:

```text
stl/Board_dielectric_1.stl
stl/Copper_GND.stl
stl/Copper_RF_IN.stl
stl/Copper_no_net.stl
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

- `--set Board.DIELECTRIC_GROUPING=merged` if all dielectrics share one material: one STL instead of
  several.
- The solder mask and silkscreen are off, as by default. Turn them on
  (`--set Stackup.solder_mask=True --set Stackup.silkscreen=True`) only if their εr matters to
  you. `materials.json` then carries an εr and a tan δ for each: the mask's from the board's
  stack-up, else 3.8 and 0.03 ([Solder Masks](Solder-Masks.md#175-material-for-the-solver)), the
  ink's a best guess of 5.0 and 0.03 ([Silkscreens](Silkscreens.md#164-material-for-the-solver)).
- The finish is off in the preset (`Stackup.finish = False`): 80 nm gold cannot be resolved by an
  FDTD mesh.
- `--set Stackup.FUSION_BUILD=PLIES_SEPARATE` if the plies of a gap differ and the solver should
  see each one: every ply, every core and the resin beside each inner copper layer is then its
  own STL with its own εr and tan δ ([Board](Board.md#121-dielectric-solids)). With the plies
  fused, the default, each gap is one STL.

## 23.2 Building The CSXCAD Model

For each part in `materials.json`, create one property from its `properties` and import the
STL named in `file_names.stl`. Metals become `AddMetal` (PEC) or a lossy material with
`kappa` = conductivity; dielectrics become `AddMaterial` with `epsilon` and a
`kappa` derived from tanδ at the frequency of interest. The dielectrics are the laminate
solids (`role` `board`: the gaps, or the plies, cores and resin with the plies separate) and,
when they are built, the solder mask, the silkscreen and the via resin. FDTD models dielectric
loss as a conductivity, which equals the loss tangent at one frequency:

```math
\kappa = 2 \pi f_0 \varepsilon_0 \varepsilon_r \tan\delta \qquad (23.1)
```

| Symbol | Meaning | Source |
|---|---|---|
| $`\kappa`$ | equivalent conductivity of the dielectric, S/m | |
| $`f_0`$ | frequency at which the loss is matched, Hz | your choice |
| $`\varepsilon_0`$ | vacuum permittivity, $`8.854 \times 10^{-12}`$ F/m | |
| $`\varepsilon_r`$, $`\tan\delta`$ | relative permittivity and loss tangent of the part at $`f_0`$ | `materials.json`: `epsilon_r`, `loss_tangent` and `dielectric_model` |

Example: FR4 with $`\varepsilon_r = 4.5`$, $`\tan\delta = 0.02`$ at $`f_0 = 2.45`$ GHz gives
$`\kappa \approx 0.0123`$ S/m. The loss is exact at $`f_0`$ only; away from it a constant
$`\kappa`$ gives a loss tangent that falls as $`1/f`$.

`epsilon_r` and `loss_tangent` are the values at the part's `spec_frequency_hz`, which is seldom
$`f_0`$. A laminate part's `dielectric_model` says how to carry them there
([Material Properties](Material-Properties.md#214-how-εr-and-tan-δ-change-with-frequency)):
`constant` uses them as they are, `djordjevic_sarkar` gives the four numbers of equation (21.1),
and `table` gives rows of frequency, εr and tan δ. The function `at_f0` below reads all three. It
still hands openEMS one εr and one $`\kappa`$: openEMS has dispersive materials of its own (Debye,
Lorentz and Drude), and fitting one of them to the model, for a run whose band is wide enough
for εr to move, is not covered here.

```python
import cmath, json, math, os
from CSXCAD import ContinuousStructure
from openEMS import openEMS
from openEMS.physical_constants import EPS0

run = "Output/board/simulation_STL"
mats = json.load(open(os.path.join(run, "materials.json")))
f0 = 2.45e9                                  # frequency used to turn tan d into a conductivity
unit = 1e-3                                  # the STL files are in mm (Run.UNITS = "mm")

def at_f0(pr):
    """(er, tan d) of a dielectric part at f0, by its dielectric_model when it has one."""
    m = pr.get("dielectric_model", {"model": "constant"})
    if m["model"] == "djordjevic_sarkar":
        lo, hi = m["low_frequency_hz"], m["high_frequency_hz"]
        e = m["epsilon_inf"] + m["delta_epsilon"] / math.log(hi / lo) * cmath.log((hi + 1j * f0) / (lo + 1j * f0))
        return e.real, -e.imag / e.real
    if m["model"] == "table":                             # rows of [Hz, er, tan d]: the nearest two, over log f
        rows = sorted(m["table"])
        lo = max((r for r in rows if r[0] <= f0), default=rows[0])
        hi = min((r for r in rows if r[0] >= f0), default=rows[-1])
        w = 0.0 if hi[0] == lo[0] else math.log(f0 / lo[0]) / math.log(hi[0] / lo[0])
        return lo[1] + w * (hi[1] - lo[1]), lo[2] + w * (hi[2] - lo[2])
    return pr["epsilon_r"], pr["loss_tangent"]


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
    elif role in ("board", "mask", "silk", "via_resin"):  # every dielectric the export holds
        er, tan_d = at_f0(pr)
        prop = CSX.AddMaterial(name, epsilon=er, kappa=2 * math.pi * f0 * EPS0 * er * tan_d)
    else:
        continue                                          # the finish, if it was exported
    prop.AddPolyhedronReader(stl, priority=20 if role in ("copper", "plating") else 10).ReadFile()

mesh = CSX.GetGrid()
mesh.SetDeltaUnit(unit)
# ... mesh lines, ports and dumps as in any openEMS script ...
```

Points that matter:

- **Priority.** Copper must win over the dielectric where both claim a cell; give the metal
  properties the higher priority, as above.
- **Thin dielectrics.** With `Stackup.FUSION_BUILD = "PLIES_SEPARATE"` a ply is 50 to 200 µm
  thick, and the mask 10 to 30 µm. A solid thinner than a mesh cell can be missed or smeared
  when the materials are sampled on the mesh, so put a mesh line on each face of every solid
  whose εr matters to the result. `materials.json` gives each part's `z_range_mm`.
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

## 23.3 Octave

The same route exists with the Octave interface. Each call returns the updated `CSX`, which
must be assigned:

```octave
CSX = AddMetal(CSX, 'Copper_GND');
CSX = ImportSTL(CSX, 'Copper_GND', 20, 'stl/Copper_GND.stl');
CSX = AddMaterial(CSX, 'Board_dielectric_1');
CSX = SetMaterialProperty(CSX, 'Board_dielectric_1', 'Epsilon', 4.5, 'Kappa', kappa);
```

In Octave the STL is read only when openEMS runs, from inside the simulation folder
(`RunOpenEMS` changes into `Sim_Path` first), so give `ImportSTL` an absolute path, for example
`fullfile(pwd, 'Output/board/simulation_STL/stl/Copper_GND.stl')`. Read the property values from
`materials.json` with `jsondecode`.

## 23.4 Checking The Import

- The number of imported STL files should equal the number of parts you kept from
  `materials.json` (a part whose mesh came out empty has an entry but no file).
- View the structure with AppCSXCAD before running: every net should be a separate colour, and
  the vias should pass through the dielectrics.
- Run `--verify` on the export first: an STL that is not closed (`closed=False` in the Verifier)
  will not voxelize correctly.

| Previous | Next |
|:---|---:|
| [KiCad And Solver Compatibility](Compatibility.md) | [Glossary](Glossary.md) |
