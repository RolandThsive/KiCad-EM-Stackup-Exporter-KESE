# 21. Material Properties

Geometry files carry shapes, not physics. Everything a solver needs that the geometry cannot
carry goes into `materials.json`, written next to the outputs (`Run.WRITE_MATERIALS_JSON`, on by
default). This page says what the numbers are and where each one comes from. None of them changes
the geometry: they are section 4, Material, of each element's parameter file.

## 21.1 The File

```json
{
  "board": "29_stackup_plies",
  "mode": "simulation",
  "units_of_files": "m",
  "orientation": "board in XY, F.Cu toward +Z, Y up",
  "parts": {
    "Board_dielectric 1": {
      "role": "board",
      "layer": "dielectric 1",
      "net": null,
      "z_range_mm": [0.46775, 0.68525],
      "properties": {
        "kind": "prepreg", "material": "1080", "thickness_mm": 0.2,
        "epsilon_r": 3.9, "loss_tangent": 0.018, "fused_properties": "first",
        "spec_frequency_hz": 1000000000.0, "dielectric_model": {"model": "constant"},
        "between": ["F.Cu", "In1.Cu"],
        "plies": [
          {"name": "dielectric 1 ply 1", "kind": "prepreg", "material": "1080", "thickness_mm": 0.08,
           "epsilon_r": 3.9, "loss_tangent": 0.018, "spec_frequency_hz": 1000000000.0, "dielectric_model": {"model": "constant"}},
          {"name": "dielectric 1 ply 2", "kind": "prepreg", "material": "2116", "thickness_mm": 0.12,
           "epsilon_r": 4.2, "loss_tangent": 0.016, "spec_frequency_hz": 1000000000.0, "dielectric_model": {"model": "constant"}}
        ]
      },
      "look": {"color": "#A89C66", "alpha": 1.0},
      "file_names": {"stl": "Board_dielectric_1.stl", "glb_node": "Board_dielectric 1", "step_solid": "Board_dielectric 1"}
    },
    "Copper_IN1": {
      "role": "copper",
      "layer": "In1.Cu",
      "net": "IN1",
      "z_range_mm": [0.46775, 0.48525],
      "properties": {
        "thickness_mm": 0.0175, "conductivity_S_per_m": 58000000.0, "surface_roughness_um": 0.0,
        "foil_mm": 0.0175, "plating_added_mm": 0.0, "material": "copper", "roughness": {"model": "none"},
        "layers": [
          {"layer": "In1.Cu", "position": "inner", "thickness_mm": 0.0175, "foil_mm": 0.0175,
           "plating_added_mm": 0.0, "etch_factor": 0.0, "treated_face": "lower"}
        ]
      },
      "look": {"color": "#CD803E", "alpha": 1.0},
      "file_names": {"stl": "Copper_IN1.stl", "glb_node": "Copper_IN1", "step_solid": "Copper_IN1"}
    }
  }
}
```

Per part:

| Key | Meaning |
|---|---|
| `role` | `board`, `copper`, `plating`, `via_resin`, `finish`, `mask`, `mask_over_copper`, `silk` |
| `layer` | the KiCad layer or dielectric name of the part's first prism (for a per-net copper part, the first layer it was built on; its `z_range_mm` shows the full span); for the resin between the traces built with the plies separate, the copper layer it lies beside; for plating, the span of copper layers (`F.Cu-B.Cu`); for finish, `F.Finish`, `B.Finish`, `Edge.Finish` or `Hole.Finish` |
| `net` | the part's net with `Copper.COPPER_GROUPING = "net"` (and for per-net finish); with `"layer"` or `"merged"` grouping, only the net of the part's first prism; `null` for parts without a net |
| `z_range_mm` | lowest and highest z of the part in KESE's board frame, in mm from the laminate mid-plane, whatever `units_of_files` is (with `Run.ORIENTATION = "flat"` this is the files' Y axis) |
| `properties` | the physical values below |
| `look` | colour and alpha, as in the GLB |
| `file_names` | the STL file name (the part name sanitised by the STL writer's own rule, see [Project Output Organization](Project-Output-Organization.md)), the GLB node name and the STEP solid name, so a script can match files to properties. All three are listed whatever formats were written |

`z_range_mm` is always in mm; the geometry files are in `units_of_files`. A part that a line of
`Stackup.py` leaves out is not in the file: `materials.json` lists exactly the parts that were
written ([Stack-Up Model](Stack-Up-Model.md#84-what-is-built-the-lines-of-stackuppy)).

## 21.2 Properties Per Role

| Role | Properties | Source |
|---|---|---|
| `board`, plies fused | `kind` (core / prepreg), `material`, `thickness_mm`, `epsilon_r`, `loss_tangent`, `fused_properties`, `spec_frequency_hz`, `dielectric_model`, `between` (the two copper layers), `plies` (every ply of the gap with its own values) | the stack-up's `(type)`, `(material)`, `(epsilon_r)`, `(loss_tangent)`, `(spec_frequency)`, `(dielectric_model)`; else `Board.DEFAULT_*` and `Board.DIELECTRIC_MODEL`; `Board.FUSED_PROPERTIES` |
| `board`, plies separate: a ply or a core | `kind`, `material`, `thickness_mm`, `epsilon_r`, `loss_tangent`, `spec_frequency_hz`, `dielectric_model`, `between`, `ply` (its place in the gap, from 1), `plies_in_gap`, and `joined_plies` where it holds several of the file's plies | the same, ply by ply |
| `board`, plies separate: the resin between the traces | `kind` (`resin`), `material`, `thickness_mm`, `epsilon_r`, `loss_tangent`, `spec_frequency_hz`, `dielectric_model`, `resin_fill_beside` (the copper layer), `flowed_from` (the ply) | `Board.RESIN_MATERIAL`, `Board.RESIN_EPSILON_R`, `Board.RESIN_LOSS_TANGENT`; where one is `None`, the ply's value |
| `copper` | `material`, `conductivity_S_per_m`, `roughness`, `layers` (each layer's `position`, `thickness_mm`, `foil_mm`, `plating_added_mm`, `etch_factor`, `treated_face`), and the first layer's `thickness_mm`, `foil_mm`, `plating_added_mm` with `surface_roughness_um` | stack-up or `Copper.DEFAULT_TOP_FOIL_MM`, `DEFAULT_INNER_FOIL_MM`, `DEFAULT_BOTTOM_FOIL_MM`; `Copper.TOP_PLATING_ADDED_MM`, `BOTTOM_PLATING_ADDED_MM`; the etch factors; `Copper.COPPER_MATERIAL`, `COPPER_CONDUCTIVITY_S_PER_M`, `COPPER_ROUGHNESS_MODEL` |
| `plating` | `material`, `conductivity_S_per_m` | `Copper.COPPER_MATERIAL`, `Copper.COPPER_CONDUCTIVITY_S_PER_M` |
| `via_resin` | `material` (`via resin`), `epsilon_r`, `loss_tangent` | `Copper.VIA_RESIN_MATERIAL`, `Copper.VIA_RESIN_EPSILON_R`, `Copper.VIA_RESIN_LOSS_TANGENT` |
| `finish` | `side`, `metal`, `thickness_mm`, `conductivity_S_per_m`, and on the shells round walls, holes and edges `drawn_thickness_mm` | `Finish.FINISH_TYPES`, `Finish.FINISH_CONDUCTIVITY_S_PER_M` |
| `mask`, `mask_over_copper` | `side`, `thickness_over_laminate_mm`, `thickness_over_copper_mm`, `material`, `epsilon_r`, `loss_tangent` | stack-up or `SolderMask.MASK_OVER_*_MM`; the mask layer's `(material)`, `(epsilon_r)`, `(loss_tangent)` in the file (`SolderMask.USE_STACKUP_MASK_MATERIAL`), else `SolderMask.MASK_MATERIAL`, `MASK_EPSILON_R`, `MASK_LOSS_TANGENT` |
| `silk` | `side`, `thickness_mm`, `material`, `epsilon_r`, `loss_tangent` | `SilkScreen.SILK_THICKNESS_MM`, `SILK_MATERIAL`, `SILK_EPSILON_R`, `SILK_LOSS_TANGENT` |

Properties come from the part's **first** prism. For a copper part with `"net"` grouping this is
the first layer of that net, so its `thickness_mm`, `foil_mm` and `plating_added_mm` are that
layer's; `layers` has every layer the part lies on (section 21.6). With
`Board.DIELECTRIC_GROUPING = "merged"`, the single `Board` part carries the values of its first
solid only: the first gap's with the plies fused, the first ply's with the plies separate.

## 21.3 The Default Numbers

| Value | Default | What it is |
|---|---|---|
| εr of a dielectric | 4.5 | typical FR4 at 1 GHz; `Board.DEFAULT_EPSILON_R` |
| tan δ of a dielectric | 0.02 | typical FR4 at 1 GHz; `Board.DEFAULT_LOSS_TANGENT` |
| spec frequency of a dielectric | 1 GHz | the frequency εr and tan δ are given at; `Board.DEFAULT_SPEC_FREQUENCY_HZ` |
| εr and tan δ of the resin between the traces (plies separate) | 3.5, 0.02 | a best guess for FR-4 epoxy without its glass: published figures give εr 3.0 to 3.57 and tan δ 0.021 for the resin, 6.2 and 0.002 for E-glass; no resin maker's sheet has been read; `Board.RESIN_EPSILON_R`, `Board.RESIN_LOSS_TANGENT` |
| copper conductivity | 5.8 × 10⁷ S/m | annealed copper at 20 °C; `Copper.COPPER_CONDUCTIVITY_S_PER_M` |
| copper surface roughness | none (smooth) | a solver-side correction (Hammerstad, Huray), section 21.6; `Copper.COPPER_ROUGHNESS_MODEL` |
| nickel, gold, palladium, tin, silver conductivity | 1.4 × 10⁷, 4.1 × 10⁷, 9.5 × 10⁶, 9.1 × 10⁶, 6.3 × 10⁷ S/m | bulk values; `Finish.FINISH_CONDUCTIVITY_S_PER_M` |
| OSP conductivity | 0 | organic coating |
| εr and tan δ of the via resin | 4.4, 0.02 | San-Ei Kagaku PHP-900 IR-6P hole plugging ink at 1 GHz, from its technical specifications; `Copper.VIA_RESIN_EPSILON_R`, `Copper.VIA_RESIN_LOSS_TANGENT` |
| εr and tan δ of the solder mask | 3.8, 0.03 | generic LPI mask: JLCPCB gives εr 3.8 and OSH Park 3.9; Taiyo PSR-4000BN gives tan δ 0.029 at 1 MHz and OSH Park 0.033; `SolderMask.MASK_EPSILON_R`, `SolderMask.MASK_LOSS_TANGENT` |
| εr and tan δ of the silkscreen | 5.0, 0.03 | a best guess for white legend ink, not a maker's figure; `SilkScreen.SILK_EPSILON_R`, `SilkScreen.SILK_LOSS_TANGENT` |

> [!IMPORTANT]
> These are typical values, not measured ones, and two of them (the resin and the silkscreen) are
> best guesses. FR4's εr and tan δ vary with frequency, resin content and vendor; enter the
> fabricator's datasheet values in KiCad's stack-up, or in `parameters/PCB_elements/Board.py`
> (`DEFAULT_EPSILON_R`, `DEFAULT_LOSS_TANGENT`). Those apply only where the stack-up gives no
> value, unless `USE_STACKUP_EPSILON_R` / `USE_STACKUP_LOSS_TANGENT` are set to `False`. A gap
> pressed from several plies is one solid or one solid per ply, as `Stackup.FUSION_BUILD` says
> ([Board](Board.md#121-dielectric-solids)); either way every ply's own values are in the file.

## 21.4 How εr And tan δ Change With Frequency

A dielectric's εr and tan δ are true at one frequency, the **spec frequency**. KiCad's
development version (file format 20260511 on) writes it for each dielectric as
`(spec_frequency ...)`, with `(dielectric_model constant)` or `(dielectric_model djordjevic_sarkar)`
beside it; KESE reads both (`Board.USE_STACKUP_SPEC_FREQUENCY`,
`Board.USE_STACKUP_DIELECTRIC_MODEL`) and uses `Board.DEFAULT_SPEC_FREQUENCY_HZ` (1 GHz) and
`Board.DIELECTRIC_MODEL` where the file gives none, as every file of KiCad 4 to 10 does. The
model's name is read in small or capital letters; a name KESE does not know takes
`Board.DIELECTRIC_MODEL`, with a warning. Every
laminate part gets `spec_frequency_hz` and `dielectric_model`:

![Two charts of one dielectric with εr 4.5 and tan δ 0.02 given at 1 GHz, from 1 MHz to 100 GHz, for the three dielectric models: constant keeps both values at every frequency; Djordjevic-Sarkar lets εr fall by 0.132 for each decade, from 4.90 at 1 MHz to 4.24 at 100 GHz, while tan δ stays between 0.018 and 0.021; the table model is the three rows of the example table, at 100 MHz, 1 GHz and 10 GHz. All three pass through the given values at 1 GHz](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/Material-Properties/materials_1_dielectric_models.webp)

| `Board.DIELECTRIC_MODEL` | Written as `dielectric_model` | Meaning |
|---|---|---|
| `"constant"` (the default) | `{"model": "constant"}` | εr and tan δ are the same at every frequency: KiCad's default, and what KESE wrote before 25.2 |
| `"djordjevic_sarkar"` | `{"model": "djordjevic_sarkar", "spec_frequency_hz", "low_frequency_hz", "high_frequency_hz", "epsilon_inf", "delta_epsilon"}` | the wideband model usual for glass-epoxy laminates, fitted to εr and tan δ at the spec frequency |
| `"table"` | `{"model": "table", "table": [[Hz, εr, tan δ], ...]}` | the rows of `Board.DIELECTRIC_TABLE`, written as given; an empty table is an error before the board is read (a ply the board file gives the table model is then written with constant values, with a warning) |

The Djordjevic-Sarkar model (Djordjevic, Biljic, Likar-Smiljanic and Sarkar, IEEE Transactions on
Electromagnetic Compatibility 43(4), 2001) is one complex permittivity, causal over the whole band:

```math
\varepsilon(f) = \varepsilon_{\infty} + \frac{\Delta\varepsilon}{\ln\left( f_{\mathrm{high}} / f_{\mathrm{low}} \right)} \, \ln\frac{f_{\mathrm{high}} + j f}{f_{\mathrm{low}} + j f}, \qquad \varepsilon_r(f) = \mathrm{Re}\, \varepsilon(f), \qquad \tan\delta(f) = -\frac{\mathrm{Im}\, \varepsilon(f)}{\mathrm{Re}\, \varepsilon(f)} \qquad (21.1)
```

KESE fits its two parameters so that the model has the given εr and tan δ at the spec frequency,
as KiCad's own transmission line calculator fits it
(`common/transline_calculations/dielectric_djordjevic_sarkar.cpp`):

```math
K = \ln\frac{f_{\mathrm{high}} + j f_s}{f_{\mathrm{low}} + j f_s}, \qquad \Delta\varepsilon = -\frac{\varepsilon_r \tan\delta}{\mathrm{Im}\, K} \, \ln\frac{f_{\mathrm{high}}}{f_{\mathrm{low}}}, \qquad \varepsilon_{\infty} = \varepsilon_r \left( 1 + \tan\delta \, \frac{\mathrm{Re}\, K}{\mathrm{Im}\, K} \right) \qquad (21.2)
```

| Symbol | Meaning | Parameter |
|---|---|---|
| $`\varepsilon_r`$, $`\tan\delta`$ | the dielectric's values at the spec frequency | the stack-up, else `Board.DEFAULT_EPSILON_R`, `Board.DEFAULT_LOSS_TANGENT` |
| $`f_s`$ | the spec frequency | the stack-up's `(spec_frequency ...)`, else `Board.DEFAULT_SPEC_FREQUENCY_HZ` |
| $`f_{\mathrm{low}}`$, $`f_{\mathrm{high}}`$ | the corner frequencies of the model | `Board.DS_LOW_FREQUENCY_HZ` (1 kHz), `Board.DS_HIGH_FREQUENCY_HZ` (1 THz) |
| $`\varepsilon_{\infty}`$, $`\Delta\varepsilon`$ | the model's two parameters, written as `epsilon_inf` and `delta_epsilon` | |

A solver that has the model takes the four numbers; one that has not can evaluate equation (21.1)
at its own frequencies. A dielectric with tan δ 0 is written with $`\Delta\varepsilon = 0`$. When
the spec frequency is not between the two corners the model cannot be fitted: that ply is written
with constant values and `report.txt` warns. `report.txt` names the model and the frequency
beside each dielectric that has one (`featureTest/29c_stackup_frequency`):

```text
  dielectric 2             core     FR4 core   1.0650 mm  er 4.6  tan d 0.02   z -0.5325 .. +0.5325   (djordjevic_sarkar, values given at 10 GHz)
```

```json
"dielectric_model": {"model": "djordjevic_sarkar", "spec_frequency_hz": 10000000000.0,
                     "low_frequency_hz": 1000.0, "high_frequency_hz": 1000000000000.0,
                     "epsilon_inf": 4.328549, "delta_epsilon": 1.221518}
```

With the plies separate each ply has its own model, and the resin between the traces takes the
spec frequency and the model of the ply it flowed from, fitted to the resin's own εr and tan δ (a
resin that flowed from a ply with the table model is written constant: the table is the ply's).

## 21.5 A Gap Whose Plies Differ

With the plies fused, a gap pressed from plies of different glass styles is one solid, and
`Board.FUSED_PROPERTIES` says which values it has:

- `"first"` (the default): the first ply's material, εr and tan δ, counted from the top, as KESE
  has always done;
- `"series"`: the plies in series, as a field that runs straight across the gap sees them (the
  field between a trace and the plane under it):

```math
\frac{h}{\varepsilon_r} = \sum_{p} \frac{h_p}{\varepsilon_{r,p}}, \qquad \tan\delta = \frac{\varepsilon_r}{h} \sum_{p} \frac{h_p \tan\delta_p}{\varepsilon_{r,p}} \qquad (21.3)
```

| Symbol | Meaning |
|---|---|
| $`h`$, $`\varepsilon_r`$, $`\tan\delta`$ | thickness and values of the fused solid |
| $`h_p`$, $`\varepsilon_{r,p}`$, $`\tan\delta_p`$ | thickness and values of ply $`p`$ of the gap |

Example, the top gap of `featureTest/29d_stackup_real` (JLCPCB's JLC04161H-2116C): a 2116 ply of
0.124 mm with εr 4.16 on a 1080 ply of 0.0764 mm with εr 3.91 gives
0.2004 / (0.124 / 4.16 + 0.0764 / 3.91) = 4.061; `"first"` gives 4.16. The material is then
written as `2116 + 1080`, and the spec frequency and the model stay the first ply's. Either way
`plies` lists every ply with its own values, so a script can apply another rule. To keep the
plies as solids of their own, build with `Stackup.FUSION_BUILD = "PLIES_SEPARATE"`.

## 21.6 Copper By Layer

A net's copper is one part across its layers, and the layers differ: the top and bottom copper
are foil plus plating, the inner copper is foil alone, and each may have its own etch factor. So
a copper part has `layers`, one entry for each copper layer it lies on, with `position` (`top`,
`inner` or `bottom`), `thickness_mm`, `foil_mm`, `plating_added_mm`, `etch_factor` and
`treated_face` ([Copper And Traces](Copper-And-Traces.md#138-electrical-properties)).

`roughness` is the surface roughness model, for the conductor loss a solver adds above the loss
of smooth copper. A copper layer has a **treated** face, pressed into the dielectric the foil was
laminated on, and the other face; `treated_face` says whether the treated one is the layer's
`lower` or `upper` face. KESE writes the numbers and applies no formula; these are the formulas
the models stand for, with the skin depth $`\delta`$:

```math
\delta = \frac{1}{\sqrt{\pi f \mu_0 \sigma}}, \qquad K_{\mathrm{Hammerstad}} = 1 + \frac{2}{\pi} \arctan\left( 1.4 \left( \frac{R_q}{\delta} \right)^{2} \right), \qquad K_{\mathrm{Huray}} = 1 + \frac{3}{2} \cdot \frac{s}{1 + \dfrac{\delta}{a} + \dfrac{\delta^{2}}{2 a^{2}}} \qquad (21.4)
```

| Symbol | Meaning | Written as | Parameter |
|---|---|---|---|
| $`K`$ | the factor the smooth conductor's loss is multiplied by | | |
| $`\sigma`$ | conductivity of copper | `conductivity_S_per_m` | `Copper.COPPER_CONDUCTIVITY_S_PER_M` |
| $`R_q`$ | RMS height of the face's roughness | `rms_treated_um`, `rms_other_um` | `Copper.COPPER_ROUGHNESS_RMS_TREATED_UM`, `COPPER_ROUGHNESS_RMS_OTHER_UM` |
| $`a`$ | radius of the nodules on the face | `radius_treated_um`, `radius_other_um` | `Copper.COPPER_HURAY_RADIUS_TREATED_UM`, `COPPER_HURAY_RADIUS_OTHER_UM` |
| $`s`$ | surface of the nodules over the flat surface they stand on | `surface_ratio_treated`, `surface_ratio_other` | `Copper.COPPER_HURAY_SURFACE_RATIO_TREATED`, `COPPER_HURAY_SURFACE_RATIO_OTHER` |

| `Copper.COPPER_ROUGHNESS_MODEL` | `roughness` |
|---|---|
| `"none"` (the default) | `{"model": "none"}` |
| `"hammerstad"` | `{"model": "hammerstad", "rms_treated_um": 1.2, "rms_other_um": 0.4}` |
| `"huray"` | `{"model": "huray", "radius_treated_um": 0.5, "radius_other_um": 0.5, "surface_ratio_treated": 1.0, "surface_ratio_other": 1.0}` |

Foil makers quote Rz, the peak-to-valley height, which is larger than the RMS height: standard
foil 3 to 6 µm, reverse-treated foil 1 to 1.5 µm, very-low-profile foils 0.3 to 1 µm. The
Hammerstad factor stops rising at 2, so above a few GHz on standard foil the Huray model is the
one that keeps following the measured loss. `surface_roughness_um`, the one number KESE wrote
before 25.2, is still there: it is the treated face's RMS height.

## 21.7 Using The File

- **openEMS**: read `parts`, create one material per part from `properties`, and import the file
  named in `file_names.stl`. See [openEMS Workflow](OpenEMS-Workflow.md).
- **FreeCAD, and Elmer or CalculiX through its FEM workbench**: the STEP solids carry the part
  names; assign the material of each name by hand or by script from `properties`.
- **Any script**: `file_names` ties every entry to the STL file, GLB node and STEP solid of the
  same part; the OBJ object and material names are the STL name without `.stl`.
- **A model with frequency**: read `dielectric_model` of each laminate part. `constant` needs
  `epsilon_r` and `loss_tangent` alone; `djordjevic_sarkar` gives the four numbers of equation
  (21.1); `table` gives the rows.

| Previous | Next |
|:---|---:|
| [Checks, Errors And Warnings](Checks-Errors-And-Warnings.md) | [KiCad And Solver Compatibility](Compatibility.md) |
