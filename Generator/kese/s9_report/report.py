"""Stage 9 - report: report.txt (what was read, made and skipped, and how long each stage took)
and parameters.txt (every setting of the run) next to every output."""
from datetime import datetime

from kese.core.whole_files import whole
from kese.s3_resolve.heights import dielectric_z
from parameters import P


def run(files, job):
    write_parameters(files.out_dir / "parameters.txt", job.overrides)
    write_report(files.out_dir / "report.txt", files, job)
    return files


def write_parameters(path, overrides):
    """Every setting the run used, the command-line overrides first."""
    text = P.snapshot()
    if overrides:
        text = "# command-line overrides applied: " + ", ".join(f"{k}={v!r}" for k, v in overrides) + "\n\n" + text
    with whole(path):
        path.write_text(text, encoding="utf-8")


def write_report(path, files, job):
    """What was read, made and skipped, the notes, the parts, each stage's time and the Verifier's lines."""
    model = files.model
    r = model.prismset.regions
    st, items, raw = r.stackup, r.items, r.items.raw
    L = [f"{raw.name}  ({raw.path.name})   generated {datetime.now():%Y-%m-%d %H:%M}"]
    L.append(f"mode: {model.mode}   formats: {', '.join(job.formats)}   units: {model.units}")
    L.append(f"{raw.dialect.describe()}, generator {raw.generator}" + (f", title: {raw.title}" if raw.title else ""))
    L += [f"warning: {w}" for w in raw.warnings]
    L.append("")
    L.append("stack-up")
    L.append(f"  copper layers: {', '.join(r.layers)}")
    L.append(f"  laminate {st.laminate_thickness:.4f} mm ({st.thickness_source})")
    for l in r.layers:
        lo, hi = st.band[l]
        L.append(f"  {l:8s} z {lo:+.4f} .. {hi:+.4f} mm  (foil {st.copper_thickness[l]} mm)")
    for i, d in enumerate(st.dielectrics):
        lo, hi = dielectric_z(st, i)
        L.append(f"  {d.name:24s} {d.kind:8s} {d.material:10s} {d.thickness:.4f} mm  er {d.epsilon_r}  tan d {d.loss_tangent}   z {lo:+.4f} .. {hi:+.4f}")
    L.append(f"  vias: {items.tent_source}; pad-to-mask clearance {items.mask_clearance} mm; silkscreen over copper (mask openings): {P.Silkscreen.SILKSCREEN_OVER_COPPER}")
    L.append(f"  {r.transform_note}")
    L.append("")
    L.append("read")
    L += [f"  {n:6d}  {what}" for what, n in sorted(items.found.items())]
    L.append("skipped")
    L += [f"  {n:6d}  {what}" for what, n in sorted(items.skipped.items())]
    if not items.skipped:
        L.append("  nothing")
    L.append("")
    L.append("notes")
    L += [f"  {n}" for n in items.notes + model.prismset.notes + job.log_lines]
    L.append("")
    L.append("parts")
    for part, mesh in model.meshes.items():
        m = model.materials[part]
        L.append(f"  {part:36s} {len(mesh.faces):8d} triangles  material {m['name']} {m['color']} alpha {m['alpha']}")
    L.append("")
    L.append("timing")
    L += [f"  {k:14s} {v:9.4f} s" for k, v in job.timings]      # to 0.1 ms: a short stage shows its time
    if files.verify_lines:
        L.append("")
        L.extend(files.verify_lines)
    with whole(path):
        path.write_text("\n".join(L) + "\n", encoding="utf-8")
