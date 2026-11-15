"""GLB: one mesh per part, PBR materials from stage 5, laid out byte for byte as trimesh 4/5 lays out
a glTF 2.0 binary: indices, positions and normals in one buffer, each array stored once, one node
per part."""
import json
import struct

import numpy as np

from kese.core.mesh_math import unitize
from kese.core.whole_files import whole
from parameters import P

ARRAY_BUFFER, ELEMENT_ARRAY_BUFFER = 34962, 34963       # buffer view targets
FLOAT, UNSIGNED_INT, TRIANGLES = 5126, 5125, 4
GENERATOR = "KESE"


def _srgb_to_linear(rgb):
    s = np.asarray(rgb, dtype=float) / 255
    return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)


def material(mat):
    """The glTF material of a stage 5 material: the colour factor held as 8 bit RGBA, as trimesh held it."""
    factor = np.array([*np.round(_srgb_to_linear(mat["rgb"]), 5), round(float(mat["alpha"]), 4)])
    rgba = np.clip(factor * 255, 0.0, 255).round().astype(np.uint8)
    out = {"pbrMetallicRoughness": {"baseColorFactor": (rgba.astype(np.float64) / 255).tolist(),
                                    "roughnessFactor": float(mat["roughness"]), "metallicFactor": float(mat["metallic"])},
           "name": mat["name"]}
    if mat["alpha"] < 1:
        out["alphaMode"] = "BLEND"
    out["doubleSided"] = False
    return out


class _Store:
    """The binary buffer, its views and the accessors, each array stored once."""
    def __init__(self):
        self.views, self.accessors, self._acc = {}, [], {}

    def add(self, blob, data, kind_width):
        raw = data.tobytes()
        if raw not in self.views:
            self.views[raw] = len(self.views)
        blob["bufferView"] = self.views[raw]
        key = tuple(blob.items())
        if key in self._acc:
            return self._acc[key]
        rows = data.reshape((-1, kind_width))
        blob["count"] = len(rows)
        blob["max"] = rows.max(axis=0).astype(data.dtype).tolist()
        blob["min"] = rows.min(axis=0).astype(data.dtype).tolist()
        self.accessors.append(blob)
        self._acc[key] = len(self.accessors) - 1
        return self._acc[key]


def glb_bytes(model, normals, targets):
    """The file in pieces of bytes: header, JSON, the binary chunk's header, the arrays.  `normals`:
    Mesh.EXPORT_INCLUDE_NORMALS, `targets`: Mesh.EXPORT_SET_BUFFERVIEW_TARGETS."""
    store, meshes, materials, mat_index, nodes = _Store(), [], [], {}, []
    for part, mesh in model.meshes.items():
        if not len(mesh.faces) or not len(mesh.vertices):
            continue
        faces = store.add({"componentType": UNSIGNED_INT, "type": "SCALAR"}, mesh.faces.astype(np.uint32), 1)
        pos = store.add({"componentType": FLOAT, "type": "VEC3", "byteOffset": 0}, mesh.vertices.astype(np.float32), 3)
        prim = {"attributes": {"POSITION": pos}, "indices": faces, "mode": TRIANGLES}
        mat = material(model.materials[part])
        key = json.dumps(mat)
        if key not in mat_index:
            mat_index[key] = len(materials)
            materials.append(mat)
        prim["material"] = mat_index[key]
        if normals:
            n = unitize(mesh.vertex_normals).astype(np.float32)
            prim["attributes"]["NORMAL"] = store.add(
                {"componentType": FLOAT, "count": len(mesh.vertices), "type": "VEC3", "byteOffset": 0}, n, 3)
        nodes.append({"name": part, "mesh": len(meshes)})
        meshes.append({"name": part, "extras": {}, "primitives": [prim]})
    tree = {"scene": 0, "scenes": [{"nodes": list(range(len(nodes)))}],
            "asset": {"version": "2.0", "generator": GENERATOR}}
    tree.update({key: value for key, value in (("accessors", store.accessors), ("meshes", meshes), ("materials", materials))
                 if value})
    tree["nodes"] = nodes
    pieces, views, at = [], [], 0
    for raw in store.views:
        pieces.append(raw + b"\x00" * (-len(raw) % 4))
        views.append({"buffer": 0, "byteOffset": at, "byteLength": len(pieces[-1])})
        at += len(pieces[-1])
    if at:
        tree["buffers"] = [{"byteLength": at}]
        tree["bufferViews"] = views
    if targets:
        for m in meshes:
            prim = m["primitives"][0]
            for acc in prim["attributes"].values():
                views[store.accessors[acc]["bufferView"]]["target"] = ARRAY_BUFFER
            views[store.accessors[prim["indices"]]["bufferView"]]["target"] = ELEMENT_ARRAY_BUFFER
    content = json.dumps(tree, separators=(",", ":"))
    # trimesh pads the JSON to 4 bytes with 1 to 4 spaces; the targets pass re-pads it with 0 to 3
    content = (content + " " * ((-len(content) % 4) if targets else 4 - len(content) % 4)).encode("utf-8")
    head = struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(content) + 8 + at) + struct.pack("<I4s", len(content), b"JSON")
    return [head, content, struct.pack("<I4s", at, b"BIN\x00"), *pieces]


def write(model, path):
    with whole(path), open(path, "wb") as f:
        for piece in glb_bytes(model, P.Mesh.EXPORT_INCLUDE_NORMALS, P.Mesh.EXPORT_SET_BUFFERVIEW_TARGETS):
            f.write(piece)
    return path
