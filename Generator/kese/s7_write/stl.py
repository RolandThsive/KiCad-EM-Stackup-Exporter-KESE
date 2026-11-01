"""STL: one binary STL per part in an stl/ folder (what openEMS / CSXCAD import)."""
from kese.core.names import model_file_names


def write(model, folder):
    folder.mkdir(parents=True, exist_ok=True)
    names, written = model_file_names(model), []
    for part, mesh in model.meshes.items():
        p = folder / f"{names[part]}.stl"
        mesh.export(p, file_type="stl")
        written.append(p)
    return written
