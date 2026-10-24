"""Stage 9 - report: report.txt (what was read, made and skipped, and how long each stage took)
and parameters.txt (every setting of the run) next to every output."""
from datetime import datetime

from kese.s4_geometry.heights import dielectric_z
from kese.s9_report.parameters_txt import write_parameters
from parameters import P


def run(files, job):
    write_parameters(files.out_dir / "parameters.txt", job.overrides)
    write_report(files.out_dir / "report.txt", files, job)
    return files


def write_report(path, files, job):
    model = files.model
    b = model.prismset.regions
    raw = b.items.raw
    L = []
    L.append(f"{raw.name}  ({raw.path.name})   generated {datetime.now():%Y-%m-%d %H:%M}")
    L.append(f"mode: {model.mode}   formats: {', '.join(job.formats)}   units: {model.units}")
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
        lo, hi = dielectric_z(st, i)
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
    for n in items.notes + model.prismset.notes + job.log_lines:
        L.append(f"  {n}")
    L.append("")
    L.append("parts")
    for part, mesh in model.meshes.items():
        m = model.materials[part]
        L.append(f"  {part:36s} {len(mesh.faces):8d} triangles  material {m['name']} {m['color']} alpha {m['alpha']}")
    L.append("")
    L.append("timing")
    for k, v in job.timings:
        L.append(f"  {k:14s} {v:7.1f} s")
    if files.verify_lines:
        L.append("")
        L.extend(files.verify_lines)
    path.write_text("\n".join(L) + "\n", encoding="utf-8")
    return path
