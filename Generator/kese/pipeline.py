"""The linear flow: nine stages, each a run(what the stage before made, job) -> what it makes.

    s1 read       .kicad_pcb file -> RawBoard   the parsed tree, checked
    s2 collect    RawBoard        -> Items      every item as a flat shape on its layer, with its net
    s3 resolve    Items           -> Regions    2D regions per layer and net, holes applied
    s4 geometry   Regions         -> PrismSet   flat regions between two heights
    s5 materials  PrismSet        -> PrismSet   with a material for every part
    s6 assemble   PrismSet        -> Model      meshes, in output units and orientation
    s7 write      Model           -> Files      glb, obj, stl, step, materials.json
    s8 verify     Files           -> Files      the opt-in checks
    s9 report     Files           -> Files      report.txt and parameters.txt"""
from kese.job import start
from kese.progress import hms
from kese.s1_read import read
from kese.s2_collect import collect
from kese.s3_resolve import resolve
from kese.s4_geometry import geometry
from kese.s5_materials import materials
from kese.s6_assemble import assemble
from kese.s7_write import write
from kese.s8_verify import verify
from kese.s9_report import report

STAGES = (read, collect, resolve, geometry, materials, assemble, write, verify, report)


def generate(pcb_path, mode=None, formats=None, out_root=None, overrides=(), verify=None, log=print):
    """One board -> (output folder, Model).  What is left as None comes from parameters/run.py."""
    job = start(mode, formats, out_root, overrides, verify, log)
    out = pcb_path
    try:
        for stage in STAGES:
            out = stage.run(out, job)
        total = job.status.elapsed()
    finally:
        job.status.stop()
    names = ", ".join(p.name if p.is_file() else p.name + "/" for p in out.written)
    log(f"  -> {out.out_dir}  ({names})  in {hms(total)}")
    return out.out_dir, out.model
