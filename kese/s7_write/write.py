"""Stage 7 - write: the Model -> files in a new output folder: the formats asked for (GLB, OBJ,
STL, STEP), then materials.json."""
from kese.model.files import Files
from kese.s7_write import glb, materials_json, obj, step, stl
from kese.s7_write.output_folder import new_folder
from parameters import P


def run(model, job):
    with job.stage("write"):
        out_dir = new_folder(job.out_root or P.Run.OUTPUT_DIR, model.name, job.mode, job.formats)
        return write(model, out_dir, job.formats, job.status.set, job.note)


def write(model, out_dir, formats, status, log):
    """Model -> Files.  `status` names what is being written, `log` takes the notes."""
    files = Files(model=model, out_dir=out_dir)
    if "glb" in formats:
        status("writing GLB")
        files.glb_path = glb.write(model, out_dir / f"{model.name}.glb")
        files.written.append(files.glb_path)
    if "obj" in formats:
        status("writing OBJ")
        files.written.append(obj.write(model, out_dir / f"{model.name}.obj"))
    if "stl" in formats:
        status("writing STL")
        files.written += stl.write(model, out_dir / "stl")
    if "step" in formats:
        status("writing STEP (exact solids, fusing per part - the slowest step on dense boards)")
        p = step.write(model, out_dir / f"{model.name}.step", log)
        if p:
            files.written.append(p)
    if P.Run.WRITE_MATERIALS_JSON:
        files.written.append(materials_json.write(model, out_dir / "materials.json"))
    return files
