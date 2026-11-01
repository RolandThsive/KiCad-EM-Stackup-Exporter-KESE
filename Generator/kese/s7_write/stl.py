"""STL: one binary STL per part in an stl/ folder (what openEMS / CSXCAD import): an 80 byte zero
header, the triangle count, per triangle its unit normal, three float32 corners and 2 zero bytes."""
import numpy as np

from kese.core.names import model_file_names

HEADER = np.dtype([("header", np.void, 80), ("face_count", "<u4")])
TRIANGLE = np.dtype([("normals", "<f4", (3,)), ("vertices", "<f4", (3, 3)), ("attributes", "<u2")])


def stl_bytes(mesh):
    header = np.zeros(1, dtype=HEADER)
    header["face_count"] = len(mesh.faces)
    packed = np.zeros(len(mesh.faces), dtype=TRIANGLE)
    packed["normals"] = mesh.face_normals
    packed["vertices"] = mesh.triangles
    return header.tobytes() + packed.tobytes()


def write(model, folder):
    folder.mkdir(parents=True, exist_ok=True)
    names, written = model_file_names(model), []
    for part, mesh in model.meshes.items():
        p = folder / f"{names[part]}.stl"
        p.write_bytes(stl_bytes(mesh))
        written.append(p)
    return written
