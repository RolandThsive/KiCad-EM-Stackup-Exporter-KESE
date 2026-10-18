"""OBJ packaging: one .obj with one object per part and an .mtl with the colours."""
from Generator.Packager.stl import safe


def write(model, path):
    mtl_path = path.with_suffix(".mtl")
    obj = [f"mtllib {mtl_path.name}"]
    mtl = []
    offset = 1
    for part, mesh in model.meshes.items():
        name = safe(part)
        m = model.materials[part]
        r, g, b = (c / 255 for c in m["rgb"])
        mtl += [f"newmtl {name}", f"Kd {r:.4f} {g:.4f} {b:.4f}", f"d {m['alpha']:.3f}", ""]
        obj += [f"o {name}", f"usemtl {name}"]
        obj += [f"v {x:.9g} {y:.9g} {z:.9g}" for x, y, z in mesh.vertices]
        obj += [f"vn {x:.5f} {y:.5f} {z:.5f}" for x, y, z in mesh.vertex_normals]
        obj += [f"f {a + offset}//{a + offset} {b + offset}//{b + offset} {c + offset}//{c + offset}"
                for a, b, c in mesh.faces]
        offset += len(mesh.vertices)
    path.write_text("\n".join(obj) + "\n", encoding="utf-8")
    mtl_path.write_text("\n".join(mtl) + "\n", encoding="utf-8")
    return path
