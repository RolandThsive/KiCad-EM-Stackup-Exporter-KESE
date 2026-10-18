"""materials.json: per part, everything a solver needs that geometry cannot carry."""
import json


def write(model, path):
    parts = {}
    for part, pr in model.props.items():
        m = model.materials.get(part, {})
        parts[part] = {
            "role": pr.get("role"),
            "layer": pr.get("layer"),
            "net": pr.get("net") or None,
            "z_range_mm": [pr.get("z_min_mm"), pr.get("z_max_mm")],
            "properties": {k: v for k, v in pr.items() if k not in ("role", "layer", "net", "z_min_mm", "z_max_mm", "prisms")},
            "look": {"color": m.get("color"), "alpha": m.get("alpha")},
            "file_names": {"stl": part.replace(" ", "_") + ".stl", "glb_node": part, "step_solid": part},
        }
    doc = {"board": model.name, "mode": model.mode, "units_of_files": model.units,
           "orientation": "board in XY, F.Cu toward +Z, Y up" if model.transform[1][1] == model.transform[0][0] else "board in XZ, F.Cu toward +Y",
           "parts": parts}
    path.write_text(json.dumps(doc, indent=2), encoding="utf-8")
    return path
