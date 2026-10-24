"""report.txt and parameters.txt next to every output."""
from datetime import datetime

from parameters import P


def write_parameters(path, overrides):
    text = P.snapshot()
    if overrides:
        text = "# command-line overrides applied: " + ", ".join(f"{k}={v!r}" for k, v in overrides) + "\n\n" + text
    path.write_text(text, encoding="utf-8")
    return path


def write_report(path, raw, b, model, outputs, timings, verify_lines, log_lines):
    L = []
    L.append(f"{raw.name}  ({raw.path.name})   generated {datetime.now():%Y-%m-%d %H:%M}")
    L.append(f"mode: {model.mode}   formats: {', '.join(outputs)}   units: {model.units}")
    L.append(f"KiCad format {raw.version}, generator {raw.generator}" + (f", title: {raw.title}" if raw.title else ""))
    for w in raw.warnings:
        L.append(f"warning: {w}")
    st, items = b.stackup, b.items
    L.append("")
    L.append("stack-up")
    L.append(f"  copper layers: {', '.join(b.layers)}")
    L.append(f"  laminate {st.laminate_thickness:.4f} mm ({st.thickness_source})")
    for l in b.layers:
        lo, hi = st.band[l]
        L.append(f"  {l:8s} z {lo:+.4f} .. {hi:+.4f} mm  (foil {st.copper_thickness[l]} mm)")
    for i, d in enumerate(st.dielectrics):
        lo, hi = st.dielectric_z(i)
        L.append(f"  {d.name:24s} {d.kind:8s} {d.material:10s} {d.thickness:.4f} mm  er {d.epsilon_r}  tan d {d.loss_tangent}   z {lo:+.4f} .. {hi:+.4f}")
    L.append(f"  vias: {items.tent_source}; pad-to-mask clearance {items.mask_clearance} mm; silkscreen over copper (mask openings): {P.Silkscreen.SILKSCREEN_OVER_COPPER}")
    L.append(f"  {b.transform_note}")
    L.append("")
    L.append("read")
    for what, n in sorted(items.found.items()):
        L.append(f"  {n:6d}  {what}")
    L.append("skipped")
    for what, n in sorted(items.skipped.items()):
        L.append(f"  {n:6d}  {what}")
    if not items.skipped:
        L.append("  nothing")
    L.append("")
    L.append("notes")
    for n in items.notes + model.prismset.notes + log_lines:
        L.append(f"  {n}")
    L.append("")
    L.append("parts")
    for part, mesh in model.meshes.items():
        m = model.materials[part]
        L.append(f"  {part:36s} {len(mesh.faces):8d} triangles  material {m['name']} {m['color']} alpha {m['alpha']}")
    L.append("")
    L.append("timing")
    for k, v in timings:
        L.append(f"  {k:14s} {v:7.1f} s")
    if verify_lines:
        L.append("")
        L.extend(verify_lines)
    path.write_text("\n".join(L) + "\n", encoding="utf-8")
    return path
