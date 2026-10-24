"""STL: one binary STL per part in an stl/ folder (what openEMS / CSXCAD import)."""
from kese.core.names import safe


def write(model, folder):
    folder.mkdir(parents=True, exist_ok=True)
    written = []
    for part, mesh in model.meshes.items():
        p = folder / f"{safe(part)}.stl"
        mesh.export(p, file_type="stl")
        written.append(p)
    return written
