# 8. Output Modes

KESE writes the same geometry in two modes, chosen with `Run.MODE` or `--mode`. The old names
`real` (for `simulation`) and `pretty` (for `visual`) are still accepted.

<!-- Picture wanted: Modes 1, the same corner of a board in simulation mode (an exploded view
     showing the closed solids) and in visual mode (the skin only). -->

## 8.1 Simulation Mode

`--mode simulation`: the physical board as it leaves the factory. **Every part is a closed
solid**: each dielectric between two copper layers (core or prepreg), each net's copper with all of its layers and vias joined into
one body, via and hole plating, solder mask conformal over the copper, silkscreen and, if
enabled, the surface finish.

- Parts touch exactly (shared vertices, exact z values) and never overlap; the Verifier checks
  that every part is closed and that no two parts overlap.
- All four formats are allowed: GLB, STEP, STL, OBJ.
- This is the mode for EM, SI / PI, thermal and mechanical solvers and for CAD.

Part names in simulation mode, with the default grouping:

| Role | Parts | Example |
|---|---|---|
| `board` | one per dielectric (`Run.DIELECTRIC_GROUPING = "layer"`) or one `Board` (`"merged"`) | `Board_dielectric 1` |
| `copper` | one per net (`Run.COPPER_GROUPING = "net"`), per layer (`"layer"`), or one `Copper` (`"merged"`) | `Copper_GND`, `Copper_no_net` |
| `plating` | its own `Plating` part only with `"layer"` grouping; otherwise the barrels belong to the copper parts | `Plating` |
| `mask` | `Top Solder Mask`, `Bottom Solder Mask`, each including the mask on top of copper | |
| `silk` | `Top Silkscreen`, `Bottom Silkscreen` | |
| `finish` | per side and metal, or per side, metal and net | `Top Finish Gold`, `Top Finish Nickel_GND` |

## 8.2 Visual Mode

`--mode visual`: **only the visible surface** of the same geometry, for web viewers such as
`<model-viewer>` and three.js, and for renders. The `Skin` builder (`Generator/Geometry/Skin.py`)
slices every prism at every height in the stack, rebuilds all regions from one planar
arrangement so that neighbours share exact vertices, triangulates, and then drops every face that is buried inside another prism:

```math
\text{keep face } f \iff \mathbf{c}_f + \varepsilon \hat{\mathbf{n}}_f \notin P \ \text{ for every prism } P \qquad (8.1)
```

| Symbol | Meaning | Parameter |
|---|---|---|
| $`\mathbf{c}_f`$, $`\hat{\mathbf{n}}_f`$ | centre and outward unit normal of triangle $`f`$ | |
| $`\varepsilon`$ | test offset (0.5 µm) | `Geometry.SKIN_BURIED_TEST_OFFSET_MM` |
| $`P`$ | any prism of the model (a region between two heights), tested with the open z interval | |

What remains is one closed outer surface, still split into named parts.

Why it exists: in the simulation model the mask lies on the copper and the copper on the
laminate, with surfaces only microns apart. Viewers draw these with a depth buffer and the
surfaces fight for the same pixels (z-fighting). The skin has no hidden surfaces, so nothing
fights.

Differences from simulation mode:

- Only `glb` and `obj` are allowed; asking for `stl` or `step` is an error, because the skin is a
  surface, not solids.
- The mask on top of copper becomes its own part, `Top Mask over Copper` / `Bottom Mask over
  Copper`, with its own colour, so traces read through the mask the way they do on a real board.
- The mask is drawn opaque whatever its alpha (`Color.VISUAL_MASK_OPAQUE`), since a translucent
  surface with nothing behind it would look wrong.
- All copper and plating take the `Copper_exposed` colour, since only bare copper is visible.
- The parts are not closed solids: the Verifier's closed-solid and winding checks do not apply (the
  copper parts even come out with zero or negative signed volumes in the regression baseline), and
  it checks instead that every vertical ray that hits the board meets exactly one upward and one
  downward face.

## 8.3 Which Mode For What

| Need | Mode |
|---|---|
| HFSS, CST, openEMS, FEKO, COMSOL, any FEA or thermal solver | simulation |
| Mechanical CAD, checking the stack-up in a CAD viewer | simulation (STEP) |
| A web page, a product render, a Blender scene | visual |
| Smallest GLB of a dense board | visual (about 10 MB against 15 MB for the 4-layer example) |

The `viewer` preset (`--for viewer`) selects visual mode, GLB, metres and a centred origin in one
go. See [Choosing An Export](Choosing-An-Export.md).

| Previous | Next |
|:---|---:|
| [Stack-Up Model](Stack-Up-Model.md) | [Choosing An Export](Choosing-An-Export.md) |
