"""GLB packaging: one mesh per part, PBR materials from the Colorer."""
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
        m = mesh.copy()
        m.visual = TextureVisuals(material=pbr(model.materials[part]))
        scene.add_geometry(m, node_name=part, geom_name=part)
    return scene


def write(model, path):
    glb = scene_of(model).export(file_type="glb", include_normals=P.Run.EXPORT_INCLUDE_NORMALS)
    if P.Run.EXPORT_SET_BUFFERVIEW_TARGETS:
        glb = _set_targets(glb)
    path.write_bytes(glb)
    return path


def _set_targets(glb):
    jlen = struct.unpack_from("<I", glb, 12)[0]
    j = json.loads(glb[20:20 + jlen])
    rest = glb[20 + jlen:]
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
    body = struct.pack("<I4s", len(js), b"JSON") + js + rest
    return struct.pack("<4sII", b"glTF", 2, 12 + len(body)) + body
