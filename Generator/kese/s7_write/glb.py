"""GLB: one mesh per part, with PBR materials from stage 5 (materials)."""
import json
import struct

import numpy as np
import trimesh
from trimesh.visual.material import PBRMaterial
from trimesh.visual.texture import TextureVisuals

from parameters import P


def _srgb_to_linear(rgb):
    s = np.asarray(rgb, dtype=float) / 255
    return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)


def pbr(mat):
    factor = [*np.round(_srgb_to_linear(mat["rgb"]), 5), round(float(mat["alpha"]), 4)]
    kw = {"alphaMode": "BLEND"} if mat["alpha"] < 1 else {}
    return PBRMaterial(name=mat["name"], baseColorFactor=factor, metallicFactor=mat["metallic"],
                       roughnessFactor=mat["roughness"], **kw)


def scene_of(model):
    scene = trimesh.Scene()
    for part, mesh in model.meshes.items():
        # the same arrays, with the normals finish_mesh set (trimesh would redo zero ones), and
        # the material: a copy of every mesh would double the memory on a big board
        m = trimesh.Trimesh(mesh.vertices, mesh.faces, vertex_normals=mesh.vertex_normals, process=False,
                            visual=TextureVisuals(material=pbr(model.materials[part])))
        scene.add_geometry(m, node_name=part, geom_name=part)
    return scene


def write(model, path):
    glb = scene_of(model).export(file_type="glb", include_normals=P.Run.EXPORT_INCLUDE_NORMALS)
    with open(path, "wb") as f:
        for piece in (_set_targets(glb) if P.Run.EXPORT_SET_BUFFERVIEW_TARGETS else [glb]):
            f.write(piece)
    return path


def _set_targets(glb):
    """The GLB with a target on every buffer view, as the pieces to write one after another (the
    binary chunk is not copied)."""
    jlen = struct.unpack_from("<I", glb, 12)[0]
    j = json.loads(glb[20:20 + jlen])
    rest = memoryview(glb)[20 + jlen:]
    for mesh in j.get("meshes", []):
        for prim in mesh["primitives"]:
            for acc in prim.get("attributes", {}).values():
                bv = j["accessors"][acc].get("bufferView")
                if bv is not None:
                    j["bufferViews"][bv]["target"] = 34962
            if "indices" in prim:
                bv = j["accessors"][prim["indices"]].get("bufferView")
                if bv is not None:
                    j["bufferViews"][bv]["target"] = 34963
    js = json.dumps(j, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    chunk = struct.pack("<I4s", len(js), b"JSON") + js
    return [struct.pack("<4sII", b"glTF", 2, 12 + len(chunk) + len(rest)), chunk, rest]
