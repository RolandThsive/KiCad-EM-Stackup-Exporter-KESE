# 18. Material Properties

Geometry files carry shapes, not physics. Everything a solver needs that the geometry cannot
carry goes into `materials.json`, written next to the outputs (`Run.WRITE_MATERIALS_JSON`, on by
default). This page says what the numbers are and where each one comes from.

## 18.1 The File

```json
{
  "board": "Stator",
  "mode": "simulation",
  "units_of_files": "m",
  "orientation": "board in XY, F.Cu toward +Z, Y up",
  "parts": {
    "Board_dielectric 1": {
      "role": "board",
      "layer": "dielectric 1",
      "net": null,
      "z_range_mm": [-0.8, 0.8],
      "properties": {
        "kind": "core", "material": "FR4", "thickness_mm": 1.6,
        "epsilon_r": 4.5, "loss_tangent": 0.02, "between": ["F.Cu", "B.Cu"]
      },
      "look": {"color": "#968A58", "alpha": 1.0},
      "file_names": {"stl": "Board_dielectric_1.stl", "glb_node": "Board_dielectric 1", "step_solid": "Board_dielectric 1"}
    },
    "Copper_TX": {
      "role": "copper",
      "layer": "F.Cu",
      "net": "TX",
      "z_range_mm": [-0.835, 0.835],
      "properties": {
        "thickness_mm": 0.035, "conductivity_S_per_m": 58000000.0, "surface_roughness_um": 0.0,
        "foil_mm": 0.035, "plating_added_mm": 0.0
      },
      "look": {"color": "#CD803E", "alpha": 1.0},
      "file_names": {"stl": "Copper_TX.stl", "glb_node": "Copper_TX", "step_solid": "Copper_TX"}
    }
  }
}
```

Per part:

| Key | Meaning |
|---|---|
| `role` | `board`, `copper`, `plating`, `finish`, `mask`, `mask_over_copper`, `silk` |
| `layer` | the KiCad layer or dielectric name of the part's first prism (for a per-net copper part, the first layer it was built on; its `z_range_mm` shows the full span); for plating, the span of copper layers (`F.Cu-B.Cu`); for finish, `F.Finish` or `B.Finish` |
| `net` | the part's net with `Run.COPPER_GROUPING = "net"` (and for per-net finish); with `"layer"` or `"merged"` grouping, only the net of the part's first prism; `null` for parts without a net |
| `z_range_mm` | lowest and highest z of the part in KESE's board frame, in mm from the laminate mid-plane, whatever `units_of_files` is (with `Run.ORIENTATION = "flat"` this is the files' Y axis) |
| `properties` | the physical values below |
| `look` | colour and alpha, as in the GLB |
| `file_names` | the STL file name (the part name sanitised by the STL writer's own rule, see [Project Output Organization](Project-Output-Organization.md)), the GLB node name and the STEP solid name, so a script can match files to properties. All three are listed whatever formats were written (mask and silk are not in the STEP file by default) |

`z_range_mm` is always in mm; the geometry files are in `units_of_files`.

## 18.2 Properties Per Role

| Role | Properties | Source |
|---|---|---|
| `board` | `kind` (core / prepreg), `material`, `thickness_mm`, `epsilon_r`, `loss_tangent`, `between` (the two copper layers) | the stack-up's `(material)`, `(epsilon_r)`, `(loss_tangent)`, `(type)`; else `Board.DEFAULT_*` |
| `copper` | `thickness_mm`, `conductivity_S_per_m`, `surface_roughness_um`, `foil_mm`, `plating_added_mm` | stack-up or `Copper.DEFAULT_*_FOIL_MM`; `Copper.OUTER_PLATING_ADDED_MM`; `Copper.COPPER_CONDUCTIVITY_S_PER_M`; `Copper.COPPER_SURFACE_ROUGHNESS_UM` |
| `plating` | `conductivity_S_per_m` | `Copper.COPPER_CONDUCTIVITY_S_PER_M` |
| `finish` | `side`, `metal`, `thickness_mm`, `conductivity_S_per_m` | `Finish.FINISH_TYPES`, `Finish.FINISH_CONDUCTIVITY_S_PER_M` |
| `mask`, `mask_over_copper` | `side`, `thickness_over_laminate_mm`, `thickness_over_copper_mm` | stack-up or `SolderMask.MASK_OVER_*_MM` |
| `silk` | `side`, `thickness_mm` | `Silkscreen.SILK_THICKNESS_MM` |

Properties come from the part's **first** prism. For a copper part with `"net"` grouping this is
the first layer of that net, and its `thickness_mm` is that layer's finished thickness: outer
layers add `Copper.OUTER_PLATING_ADDED_MM`, and the stack-up or the separate outer and inner foil
defaults can make layers differ. The per-layer bands are in `report.txt`. With
`Run.DIELECTRIC_GROUPING = "merged"`, the single `Board` part carries the values of the first
dielectric only.

## 18.3 The Default Numbers

| Value | Default | What it is |
|---|---|---|
| εr of a dielectric | 4.5 | typical FR4 at 1 GHz; `Board.DEFAULT_EPSILON_R` |
| tanδ of a dielectric | 0.02 | typical FR4 at 1 GHz; `Board.DEFAULT_LOSS_TANGENT` |
| copper conductivity | 5.8 × 10⁷ S/m | annealed copper at 20 °C; `Copper.COPPER_CONDUCTIVITY_S_PER_M` |
| copper surface roughness | 0 (ignore) | a solver-side correction (Hammerstad, Huray); `Copper.COPPER_SURFACE_ROUGHNESS_UM` |
| nickel, gold, palladium, tin, silver conductivity | 1.4 × 10⁷, 4.1 × 10⁷, 9.5 × 10⁶, 9.1 × 10⁶, 6.3 × 10⁷ S/m | bulk values; `Finish.FINISH_CONDUCTIVITY_S_PER_M` |
| OSP conductivity | 0 | organic coating |

No property of the mask or the silkscreen (εr, tanδ) is written: the parameter files carry none,
and the mask and silk parts have only their thicknesses in `properties`. A solver that needs
them must be given them by hand.

> [!IMPORTANT]
> These are typical values, not measured ones. FR4's εr and tanδ vary with frequency, resin
> content and vendor; enter the fabricator's datasheet values in KiCad's stack-up or in
> `Board_Parameters.py`. KESE reads the stack-up per gap between copper layers: when a gap holds
> several plies (or sub-layers), it becomes one solid with the summed thickness and the first
> ply's kind, material, εr and tanδ. Research underway.

## 18.4 Using The File

- **openEMS**: read `parts`, create one material per part from `properties`, and import the file
  named in `file_names.stl`. See [openEMS Workflow](OpenEMS-Workflow.md).
- **HFSS / CST / COMSOL / FEKO**: the STEP solids carry the part names; assign the material of
  each name by hand or by script from `properties`.
- **Any script**: `file_names` ties every entry to the STL file, GLB node and STEP solid of the
  same part; the OBJ object and material names are the STL name without `.stl`.

| Previous | Next |
|:---|---:|
| [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md) | [Project Output Organization](Project-Output-Organization.md) |
