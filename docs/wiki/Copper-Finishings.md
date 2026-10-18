# 13. Top And Bottom Copper Finishings

The surface finish is the metal a fabricator deposits on the copper that the solder mask leaves
bare: pads, exposed traces and test points. `Generator/Geometry/Finish.py` builds it; the settings
are in `Parameters/Finish_Parameters.py`.

<!-- Pictures wanted for this page (made by Roland):
     Finish 1: a pad in cross-section with mask, copper, nickel and gold layers (ENIG), to scale.
     Finish 2: the same pad with HASL. -->

## 13.1 Off By Default

`Finish.FINISH_ENABLED = False`: no finish is built, so the geometry matches KiCad. Turn it on for
an as-fabricated model. With it on, the finish adds its own thin solids on top of the outer
copper; it never changes the copper itself.

## 13.2 Where The Finish Goes

On each side, the finish covers **exposed copper**: the copper of the outer layer intersected
with the mask openings of that side (pads with their pad-to-mask clearance, drawn openings,
untented vias). Copper under the mask gets no finish. The finish layers are stacked from the top
of the outer copper outward, in the order the finish type lists them, each one its own solid:

```math
X_\sigma = C_\sigma \cap Q_\sigma \qquad (13.1)
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
| $`z_j`$ | z range of finish layer $`j`$ ($`j = 1`$ is the layer on the copper) | |
| $`\tau_i`$ | thickness of finish layer $`i`$ | `Finish.FINISH_TYPES` |
| $`L`$, $`t_{\mathrm{out}}`$ | laminate thickness and finished outer copper, equations (7.1) and (7.3) | |

For ENIG on `F.Cu` of a 1.6 mm board with 35 µm copper: nickel from 0.835 to 0.840 mm, gold from
0.840 to 0.84008 mm.

## 13.3 Finish Types

`Finish.FINISH_TYPE`: `"file"` (the default) takes the type from the stack-up's
`(copper_finish "...")`, matched against the keys below ignoring case, spaces and hyphens, and
falls back to `Finish.FINISH_DEFAULT_TYPE` (`"ENIG"`). Any key can also be set directly.

| Key | Layers, bottom to top (mm) |
|---|---|
| `ENIG` | Nickel 0.005, Gold 0.00008 |
| `HASL` | Tin 0.010 |
| `HASL_LF` | Tin 0.010 |
| `OSP` | OSP 0.0003 |
| `ImmersionSilver` | Silver 0.0002 |
| `ImmersionTin` | Tin 0.001 |
| `HardGold` | Nickel 0.005, Gold 0.001 |

The table is `Finish.FINISH_TYPES` and can be edited: add a key or change a thickness to match a
datasheet. An unknown type applies nothing and `report.txt` says so.

## 13.4 Parts And Grouping

`Finish.FINISH_GROUPING`:

| Value | Parts | Example |
|---|---|---|
| `"metal"` (default) | one per side and metal | `Top Finish Nickel`, `Top Finish Gold`, `Bottom Finish Nickel`, ... |
| `"net"` | one per side, metal and net | `Top Finish Gold_GND`, so a net's copper, nickel and gold can be picked together in the solver (`Copper_GND`, `Top Finish Nickel_GND`, `Top Finish Gold_GND`) |

Each finish part carries `side`, `metal`, `thickness_mm` and `conductivity_S_per_m` in
`materials.json`; the conductivities come from `Finish.FINISH_CONDUCTIVITY_S_PER_M`
(Nickel 1.4 × 10⁷, Gold 4.1 × 10⁷, Tin 9.1 × 10⁶, Silver 6.3 × 10⁷ S/m, OSP 0 since it is
organic). Colours come from the metal's entry in `Color.MATERIALS`.

In STEP, finish parts are written and fused by default (`Run.STEP_WRITE_ROLES` and
`Run.STEP_FUSE_ROLES` both include `"finish"`).

> [!NOTE]
> The gold of ENIG is 80 nm thick. Heights are not snapped to the 0.1 µm grid (only the 2D
> shapes are), so it is built as a real solid, but an FDTD or FEM mesher may not resolve a body
> that thin. Solvers that struggle can take the finish as a surface impedance instead and leave
> `FINISH_ENABLED` off.

## 13.5 Settings

| Name | Default | Range | Meaning |
|---|---|---|---|
| `FINISH_ENABLED` | `False` | bool | Build the finish |
| `FINISH_TYPE` | `"file"` | `"file"` or a key of `FINISH_TYPES` | Where the type comes from |
| `FINISH_DEFAULT_TYPE` | `"ENIG"` | a key of `FINISH_TYPES` | Type when the file gives none |
| `FINISH_GROUPING` | `"metal"` | `"metal"` / `"net"` | Part per metal, or per metal and net |
| `FINISH_TYPES` | table above | `{key: [(metal, mm), ...]}` | Layers of each finish |
| `FINISH_CONDUCTIVITY_S_PER_M` | table above | `{metal: S/m}` | Written to `materials.json` |

| Previous | Next |
|:---|---:|
| [Colorizing](Colorizing.md) | [Silkscreens](Silkscreens.md) |
