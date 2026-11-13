"""Stage 9 - report: report.txt (what was read, made and skipped, and how long each stage took)
and parameters.txt (every setting of the run) next to every output."""
from datetime import datetime

from kese.core.whole_files import whole
from kese.s3_resolve.heights import dielectric_z, ply_z
from kese.s4_geometry.laminate import resin_values
from kese.s4_geometry.switches import built
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
    building = P.building()
    L.append(f"stack-up   built: {P.Stackup.FUSION_BUILD} (parameters/PCB_elements/Stackup.py)")
    L.append(f"  lines built: {', '.join(line for line, on in building.items() if on) or 'none'}")
    L.append(f"  lines left out: {', '.join(line for line, on in building.items() if not on) or 'none'}")
    L.append(f"  copper layers: {', '.join(r.layers)}")
    L.append(f"  laminate {st.laminate_thickness:.4f} mm ({st.thickness_source})")
    for l in r.layers:
        lo, hi = st.band[l]
        L.append(f"  {l:8s} z {lo:+.4f} .. {hi:+.4f} mm  (foil {st.copper_thickness[l]} mm)")
    L += laminate_lines(st)
    L.append(f"  vias: {items.tent_source}; pad-to-mask clearance {items.mask_clearance} mm; silkscreen over copper (mask openings): {P.SilkScreen.SILKSCREEN_OVER_COPPER}")
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


def laminate_lines(st):
    """The laminate, gap by gap: with the plies fused each gap's solid and under it the plies it was
    fused from; with the plies separate each ply and core as built."""
    how = lambda x: {"constant": "", "table": "   (table: Board.DIELECTRIC_TABLE)"}.get(
        x.model, f"   ({x.model}, values given at {x.frequency_hz / 1e9:g} GHz)")
    row = lambda x, t, lo, hi: (f"  {x.name:24s} {x.kind:8s} {x.material:10s} {t:.4f} mm  er {x.epsilon_r}"
                                f"  tan d {x.loss_tangent}   z {lo:+.4f} .. {hi:+.4f}{how(x)}")
    L = []
    for i, d in enumerate(st.dielectrics):
        lo, hi = dielectric_z(st, i)
        if d.solids:
            L += [row(ply, hi_p - lo_p, lo_p, hi_p) for ply, lo_p, hi_p in ply_z(st, i)]
            if i < len(st.dielectrics) - 1 and built("resin_between_traces"):      # the resin beside the copper under it
                (lo_r, hi_r), (ply, er, tand) = st.band[d.below], resin_values(st, i + 1)
                L.append(f"  {'resin ' + d.below:24s} {'resin':8s} {P.Board.RESIN_MATERIAL:10s} {hi_r - lo_r:.4f} mm  er {er}"
                         f"  tan d {tand}   z {lo_r:+.4f} .. {hi_r:+.4f}   (flowed from {ply.name})")
            continue
        L.append(row(d, d.thickness, lo, hi))
        if len(d.plies) > 1:
            L += [f"    fused from {ply.name}: {ply.kind} {ply.material} {ply.thickness:.4f} mm  er {ply.epsilon_r}"
                  f"  tan d {ply.loss_tangent}{how(ply)}" for ply in d.plies]
            if P.Board.FUSED_PROPERTIES == "series":
                L.append("    its er and tan d are its plies' in series (Board.FUSED_PROPERTIES)")
    return L
