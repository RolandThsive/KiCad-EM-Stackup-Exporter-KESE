"""STL packaging: one binary STL per part in an stl/ folder (what openEMS / CSXCAD import)."""
import re


def safe(name):
    return re.sub(r"[^A-Za-z0-9_.+-]+", "_", name).strip("_") or "part"


def write(model, folder):
    folder.mkdir(parents=True, exist_ok=True)
    written = []
    for part, mesh in model.meshes.items():
        p = folder / f"{safe(part)}.stl"
        mesh.export(p, file_type="stl")
        written.append(p)
    return written
