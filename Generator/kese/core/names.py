"""Names that are safe as file names and in OBJ / STL files."""
import re


def safe(name):
    return re.sub(r"[^A-Za-z0-9_.+-]+", "_", name).strip("_") or "part"
