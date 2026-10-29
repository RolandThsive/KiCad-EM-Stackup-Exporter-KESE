# 13. Top And Bottom Copper Finishings

The surface finish is the metal a fabricator deposits on the copper that the solder mask leaves
bare: pads, exposed traces and test points. `kese/s4_geometry/finish.py` builds it; the settings
are in `parameters/finish.py`.

## 13.1 Off By Default

`Finish.FINISH_ENABLED = False`: no finish is built, so the geometry matches KiCad. Turn it on for
an as-fabricated model. With it on, the finish adds its own thin solids on top of the outer
copper; it never changes the copper itself.

## 13.2 Where The Finish Goes

![Board 18b with ENIG from above and from below with a numbered key of the copper that gets finish, and header pad J1 pad 2 cut through its hole at true scale](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/finish_1_where.webp)

On each side, the finish covers **exposed copper**: the copper of the outer layer intersected
with the mask openings of that side (pads with their pad-to-mask clearance, drawn openings,
untented vias). Copper under the mask gets no finish, nor does copper under silkscreen ink kept
in an opening (`Silkscreen.SILKSCREEN_OVER_COPPER = True`): the legend is taken as printed
before the finish. The finish layers are stacked from the top
of the outer copper outward, in the order the finish type lists them, each one its own solid:

```math
X_\sigma = \left( C_\sigma \cap Q_\sigma \right) \setminus S_\sigma \qquad (13.1)
```

```math
z_j \in \left[ \frac{L}{2} + t_{\mathrm{out}} + \sum_{i<j} \tau_i,\ \ \frac{L}{2} + t_{\mathrm{out}} + \sum_{i \le j} \tau_i \right] \qquad (13.2)
```

On the `B` side every z is mirrored.

| Symbol | Meaning | Parameter |
|---|---|---|
| $`X_\sigma`$ | exposed copper of side $`\sigma`$ (per net with `FINISH_GROUPING = "net"`) | |
| $`C_\sigma`$ | outer copper of side $`\sigma`$ | |
| $`Q_\sigma`$ | mask openings of side $`\sigma`$, equation (15.2) | |
| $`S_\sigma`$ | silkscreen ink of side $`\sigma`$ kept in the openings; empty unless `SILKSCREEN_OVER_COPPER = True` | `Silkscreen.SILKSCREEN_OVER_COPPER` |
| $`z_j`$ | z range of finish layer $`j`$ ($`j = 1`$ is the layer on the copper) | |
| $`\tau_i`$ | thickness of finish layer $`i`$ | `Finish.FINISH_TYPES` |
| $`L`$, $`t_{\mathrm{out}}`$ | laminate thickness and finished outer copper, equations (7.1) and (7.3) | |

For ENIG on `F.Cu` of a board with no stack-up and `(general (thickness 1.6))`, so
$`L = 1.6`$ mm, and 35 µm copper: nickel from 0.835 to 0.840 mm, gold from 0.840 to 0.84008 mm.
With a stack-up the laminate is thinner than the board's total thickness and the heights shift
accordingly: on board 18b below, a 1.51 mm core, the nickel starts at 0.790 mm.

## 13.3 Finish Types

`Finish.FINISH_TYPE`: `"file"` (the default) takes the type from the stack-up's
`(copper_finish "...")`. The name is compared, ignoring case, spaces, `-` and `_`, with the keys
of `FINISH_TYPES` and with the KiCad names in `Finish.FINISH_NAME_ALIASES`. `None` means the board
has no finish: nothing is built and `report.txt` notes `finish: the board's stackup says None,
nothing applied`. Any other name that matches nothing, or no finish in the file, falls back to
`Finish.FINISH_DEFAULT_TYPE` (`"ENIG"`). Any key can also be set directly.

With KiCad's own finish names (the list in Board Setup's stack-up) this gives:

| KiCad finish | KESE type |
|---|---|
| `ENIG` | `ENIG` |
| `ENEPIG` | `ENEPIG` |
| `HAL SnPb` | `HASL` |
| `HAL lead-free` | `HASL_LF` |
| `Hard gold` | `HardGold` |
| `Immersion tin` | `ImmersionTin` |
| `Immersion silver` | `ImmersionSilver` |
| `OSP`, `HT_OSP` | `OSP` |
| `None` | no finish |
| `Immersion nickel`, `Immersion gold`, `Not specified`, `User defined` | no match, so `FINISH_DEFAULT_TYPE` (`ENIG`) |

| Key | Layers, bottom to top (mm) |
|---|---|
| `ENIG` | Nickel 0.005, Gold 0.00008 |
| `ENEPIG` | Nickel 0.005, Palladium 0.0001, Gold 0.00005 |
| `HASL` | Tin 0.010 |
| `HASL_LF` | Tin 0.010 |
| `OSP` | OSP 0.0003 |
| `ImmersionSilver` | Silver 0.0002 |
| `ImmersionTin` | Tin 0.001 |
| `HardGold` | Nickel 0.005, Gold 0.001 |

The table is `Finish.FINISH_TYPES` and can be edited: add a key or change a thickness to match a
datasheet. `report.txt` names the type it applied and its layers, for example
`finish: ENIG Nickel 0.005 mm + Gold 8e-05 mm`. A `FINISH_TYPE` (or `FINISH_DEFAULT_TYPE`) that is
not a key applies nothing and `report.txt` notes `finish: unknown type '...', none applied`.

Each finish below is shown on board 18b (`featureTest/18b_finish_pads`) with `FINISH_ENABLED = True`
and its key in `FINISH_TYPE`: 1 how it looks (visual mode), 2 a cut-away of the 3 mm pad TP1 at its
left edge (simulation mode), 3 the side profile at true scale with the height of every surface above
the laminate, and 4 the thin layers enlarged (HASL and HASL_LF need no part 4). Board 18b has 35 µm
copper on a 1.51 mm core, so its laminate face is at z = 0.755 mm and its copper top at 0.790 mm.
The bottom face is the mirror image, with the parts named `Bottom Finish ...`.

### 13.3.1 ENIG

![ENIG on board 18b: how it looks, a cut-away of a pad's edge, the side profile at true scale with heights, and the thin layers enlarged](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/finish_2_enig.webp)

Electroless nickel, immersion gold; KiCad's `ENIG`.

| Layer, from the copper up | Thickness | Top above the copper | Part on the top face | Conductivity |
|---|---|---|---|---|
| Nickel | 5 µm | 5 µm | `Top Finish Nickel` | 1.4 × 10⁷ S/m |
| Gold | 0.08 µm | 5.08 µm | `Top Finish Gold` | 4.1 × 10⁷ S/m |

The pads take the gold's colour, `#E6C15A`. On board 18b the gold's top is 40.08 µm above the
laminate, at z = 0.79508 mm; at true scale the gold is under a pixel, so part 4 enlarges it.

### 13.3.2 ENEPIG

![ENEPIG on board 18b: how it looks, a cut-away of a pad's edge, the side profile at true scale with heights, and the thin layers enlarged](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/finish_3_enepig.webp)

Electroless nickel, electroless palladium, immersion gold; KiCad's `ENEPIG`.

| Layer, from the copper up | Thickness | Top above the copper | Part on the top face | Conductivity |
|---|---|---|---|---|
| Nickel | 5 µm | 5 µm | `Top Finish Nickel` | 1.4 × 10⁷ S/m |
| Palladium | 0.1 µm | 5.1 µm | `Top Finish Palladium` | 9.5 × 10⁶ S/m |
| Gold | 0.05 µm | 5.15 µm | `Top Finish Gold` | 4.1 × 10⁷ S/m |

From the top it looks like ENIG (`#E6C15A`); the palladium shows only in a cut. On board 18b the
gold's top is 40.15 µm above the laminate.

### 13.3.3 HASL

![HASL on board 18b: how it looks, a cut-away of a pad's edge, and the side profile at true scale with heights](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/finish_4_hasl.webp)

Hot air solder levelling with tin-lead solder; KiCad's `HAL SnPb`.

| Layer, from the copper up | Thickness | Top above the copper | Part on the top face | Conductivity |
|---|---|---|---|---|
| Tin | 10 µm | 10 µm | `Top Finish Tin` | 9.1 × 10⁶ S/m |

KESE models the solder as one flat layer of tin, coloured `#C9C9C9`. With `HASL_LF` it is the
thickest finish, and the only one with no layer thin enough to need part 4; on board 18b its top is
45 µm above the laminate.

### 13.3.4 HASL_LF

![HASL_LF on board 18b: how it looks, a cut-away of a pad's edge, and the side profile at true scale with heights](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/finish_5_hasl_lf.webp)

Lead-free hot air solder levelling; KiCad's `HAL lead-free`.

| Layer, from the copper up | Thickness | Top above the copper | Part on the top face | Conductivity |
|---|---|---|---|---|
| Tin | 10 µm | 10 µm | `Top Finish Tin` | 9.1 × 10⁶ S/m |

KESE builds it exactly as `HASL`: the same layer of tin, the same part and the same colour.

### 13.3.5 OSP

![OSP on board 18b: how it looks, a cut-away of a pad's edge, the side profile at true scale with heights, and the thin layers enlarged](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/finish_6_osp.webp)

Organic solderability preservative; KiCad's `OSP` and `HT_OSP`.

| Layer, from the copper up | Thickness | Top above the copper | Part on the top face | Conductivity |
|---|---|---|---|---|
| OSP | 0.3 µm | 0.3 µm | `Top Finish OSP` | 0 (organic) |

Coloured `#D9955A`, close to the copper under it. On board 18b its top is 35.3 µm above the
laminate.

### 13.3.6 ImmersionSilver

![ImmersionSilver on board 18b: how it looks, a cut-away of a pad's edge, the side profile at true scale with heights, and the thin layers enlarged](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/finish_7_immersion_silver.webp)

Immersion silver; KiCad's `Immersion silver`.

| Layer, from the copper up | Thickness | Top above the copper | Part on the top face | Conductivity |
|---|---|---|---|---|
| Silver | 0.2 µm | 0.2 µm | `Top Finish Silver` | 6.3 × 10⁷ S/m |

Coloured `#E4E4E0`. On board 18b its top is 35.2 µm above the laminate.

### 13.3.7 ImmersionTin

![ImmersionTin on board 18b: how it looks, a cut-away of a pad's edge, the side profile at true scale with heights, and the thin layers enlarged](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/finish_8_immersion_tin.webp)

Immersion tin; KiCad's `Immersion tin`.

| Layer, from the copper up | Thickness | Top above the copper | Part on the top face | Conductivity |
|---|---|---|---|---|
| Tin | 1 µm | 1 µm | `Top Finish Tin` | 9.1 × 10⁶ S/m |

The metal of `HASL`, a tenth as thick, with the same part name and colour (`#C9C9C9`). On board 18b
its top is 36 µm above the laminate.

### 13.3.8 HardGold

![HardGold on board 18b: how it looks, a cut-away of a pad's edge, the side profile at true scale with heights, and the thin layers enlarged](https://raw.githubusercontent.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/main/docs/images/finish_9_hard_gold.webp)

Electroplated hard gold, the finish of edge-connector fingers; KiCad's `Hard gold`.

| Layer, from the copper up | Thickness | Top above the copper | Part on the top face | Conductivity |
|---|---|---|---|---|
| Nickel | 5 µm | 5 µm | `Top Finish Nickel` | 1.4 × 10⁷ S/m |
| Gold | 1 µm | 6 µm | `Top Finish Gold` | 4.1 × 10⁷ S/m |

The thickest gold of the eight finishes, 12.5 times ENIG's; the pads look gold (`#E6C15A`). On
board 18b the gold's top is 41 µm above the laminate.

## 13.4 Parts And Grouping

`Finish.FINISH_GROUPING`:

| Value | Parts | Example |
|---|---|---|
| `"metal"` (default) | one per side and metal | `Top Finish Nickel`, `Top Finish Gold`, `Bottom Finish Nickel`, ... |
| `"net"` | one per side, metal and net | `Top Finish Gold_GND`, so a net's copper, nickel and gold can be picked together in the solver (`Copper_GND`, `Top Finish Nickel_GND`, `Top Finish Gold_GND`) |

In `materials.json` each finish part has the layer `F.Finish` or `B.Finish`, its `z_range_mm`, and
the properties `side`, `metal`, `thickness_mm` and `conductivity_S_per_m`; the conductivities come
from `Finish.FINISH_CONDUCTIVITY_S_PER_M` (Nickel 1.4 × 10⁷, Gold 4.1 × 10⁷, Palladium 9.5 × 10⁶,
Tin 9.1 × 10⁶, Silver 6.3 × 10⁷ S/m, OSP 0 since it is organic). Colours come from the metal's entry
in `Color.MATERIALS` ([Colorizing](Colorizing.md)).

In STEP, finish parts are written by default (`Run.STEP_WRITE_ROLES` includes `"finish"`), each
as the closed solids stage 6 built, one per connected piece. With the OpenCascade writer
(`Run.BUILD_WITH_KERNELS = True`) their pieces are also fused, as `Run.STEP_FUSE_ROLES` includes
`"finish"`.

> [!NOTE]
> The gold of ENIG is 80 nm thick and that of ENEPIG 50 nm. Heights are not snapped to the
> 0.1 µm grid (only the 2D shapes are), so in simulation mode each is built as a real solid, but
> an FDTD or FEM mesher may not resolve a body that thin. Solvers that struggle can take the finish
> as a surface impedance instead and leave `FINISH_ENABLED` off. In visual mode only the surface
> between material and air is kept ([Output Modes](Output-Modes.md)): the faces where two layers
> touch are dropped, so a pad's top is the top layer alone and each layer below shows only as a
> band in the pad's side.

## 13.5 Settings

| Name | Default | Range | Meaning |
|---|---|---|---|
| `FINISH_ENABLED` | `False` | bool | Build the finish |
| `FINISH_TYPE` | `"file"` | `"file"` or a key of `FINISH_TYPES` | Where the type comes from |
| `FINISH_DEFAULT_TYPE` | `"ENIG"` | a key of `FINISH_TYPES` | Type when the file gives none, or a name that matches no key |
| `FINISH_GROUPING` | `"metal"` | `"metal"` / `"net"` | Part per metal, or per metal and net |
| `FINISH_TYPES` | table above | `{key: [(metal, mm), ...]}` | Layers of each finish |
| `FINISH_NAME_ALIASES` | `HAL SnPb` → `HASL`, `HAL lead-free` → `HASL_LF`, `Hard gold` → `HardGold`, `Immersion tin` → `ImmersionTin`, `Immersion silver` → `ImmersionSilver`, `HT_OSP` → `OSP` | `{KiCad name: key}` | KiCad's finish names that differ from a key |
| `FINISH_CONDUCTIVITY_S_PER_M` | table above | `{metal: S/m}` | Written to `materials.json` |

| Previous | Next |
|:---|---:|
| [Colorizing](Colorizing.md) | [Silkscreens](Silkscreens.md) |
