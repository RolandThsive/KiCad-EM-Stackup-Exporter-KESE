"""Names that are safe as file names and in OBJ / STL files."""
import re

# names Windows will not take as a file name, whatever the extension
RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def safe(name):
    """Letters (any script), digits and _ . + - kept; every other run of characters becomes _."""
    s = re.sub(r"[^\w.+-]+", "_", name).strip("_.") or "part"
    return s + "_" if s.upper().split(".")[0] in RESERVED else s


def unique_names(parts):
    """{part: safe name}, made unique (ignoring case, as Windows and macOS file systems do) by a
    counter on a clash: VCC(3V3) and VCC_3V3 would both be VCC_3V3, so the second becomes VCC_3V3_2."""
    out, taken = {}, set()
    for part in parts:
        base = name = safe(part)
        k = 2
        while name.lower() in taken:
            name, k = f"{base}_{k}", k + 1
        taken.add(name.lower())
        out[part] = name
    return out


def model_file_names(model):
    """The file name stem of every part of a model, the same in stl/, the OBJ and materials.json."""
    return unique_names(dict.fromkeys([*model.meshes, *model.props]))
