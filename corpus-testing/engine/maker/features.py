"""Finds which of the features KESE models each corpus board uses, from its .kicad_pcb text.
    python3 features.py <out.json>
Reads each board straight from its zip (nothing is written but the JSON of feature counts)."""
import json, re, sys, zipfile, glob
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ZIPS = Path("/mnt/project-files/Boards")
CU = r'"?(?:F\.Cu|B\.Cu|In\d+\.Cu)"?'


def _items(t, head):
    """The text of each top-level-ish item that starts with "(head", up to the next one (good enough to find its layer)."""
    starts = [m.start() for m in re.finditer(r"\(" + head + r"\b", t)]
    for i, s in enumerate(starts):
        yield t[s:starts[i + 1] if i + 1 < len(starts) else min(len(t), s + 4000)][:4000]


def scan(t):
    f = {}
    c = lambda pat, flags=0: len(re.findall(pat, t, flags))
    # vias
    f["through_vias"] = c(r"\(via\s+\(at")             # \s+ takes a line break too: KiCad 8 and later put (at on the next line
    f["blind_buried_vias"] = c(r"\(via\s+(?:blind|buried)\b") + c(r"\(type\s+(?:blind|buried)\)")
    f["microvias"] = c(r"\(via\s+micro\b") + c(r"\(type\s+micro\)")
    f["backdrills"] = c(r"\((?:backdrill|back_drill|tertiary_drill)\b")
    f["counterbores_countersinks"] = c(r"_post_machining\s+(?:counterbore|countersink)\b")
    f["via_protection"] = sum(1 for a, b in re.findall(r"\((?:covering|plugging)\s*\(front\s+(\w+)\)\s*\(back\s+(\w+)\)", t)
                              if "yes" in (a, b)) + c(r"\((?:capping|filling)\s+yes\)")
    # pads
    f["padstacks"] = c(r"\(padstack\b")
    f["slotted_holes"] = c(r"\(drill\s+oval\b")
    f["custom_pads"] = c(r"\(pad\s+\S+\s+\w+\s+custom\b")
    f["shaped_pads"] = c(r"\(pad\s+\S+\s+\w+\s+(?:roundrect|trapezoid)\b") + c(r"\(chamfer\s")
    f["drill_offsets"] = c(r"\(drill\b[^()]*\(offset")
    # copper
    f["arc_tracks"] = c(r"\(arc\s+\(start")
    f["filled_zones"] = c(r"\(filled_polygon\b") + c(r"\(fill_segments\b")
    gr = [(m.group(1), s) for s in _items(t, r"gr_(\w+)") for m in [re.match(r"\(gr_(\w+)", s)]]
    lay = lambda s: (re.search(r"\(layers?\s+(\"?[\w.]+\"?)", s) or [None, ""])[1].strip('"')
    f["copper_graphics"] = sum(1 for k, s in gr if k != "text" and re.fullmatch(r"(F|B|In\d+)\.Cu", lay(s)))
    f["copper_text"] = sum(1 for k, s in gr if k == "text" and re.fullmatch(r"(F|B|In\d+)\.Cu", lay(s)))
    f["curved_outline"] = sum(1 for k, s in gr if k in ("arc", "circle", "curve") and lay(s) == "Edge.Cuts") + \
        c(r"\(fp_(?:arc|circle|curve)\b[^\n]*?\(layer\s+\"?Edge\.Cuts")
    f["knockout_text"] = c(r"\bknockout\b")
    f["truetype_text"] = len(re.findall(r'\(face\s+"([^"]+)"', t)) - c(r'\(face\s+"KiCad Font"')
    f["hatched_fills"] = c(r"\(fill\s+hatch\b")
    f["bare_copper_tracks"] = c(r"\(segment(?:(?!\(segment).){0,400}?\(layers\s+" + CU + r"\s+\"?[FB]\.Mask", re.S)
    # stack-up and edge
    f["stackup"] = c(r"\(stackup\b")
    f["dielectric_properties"] = c(r"\(epsilon_r\s")
    f["copper_finish"] = len(re.findall(r'\(copper_finish\s+"?([^")]+)"?\)', t)) - c(r'\(copper_finish\s+"?None"?\)')
    f["mask_silk_colours"] = c(r'"?[FB]\.(?:Mask|SilkS)"?\s*\(type[^)]*\)\s*\(color\s')
    f["castellated_pads"] = c(r"pad_prop_castellated") + c(r"\(castellated_pads\s+yes")
    f["edge_plating"] = c(r"\(edge_plating\s+yes")
    return f


def job(a):
    rank, zname, member = a
    with zipfile.ZipFile(ZIPS / f"kicad_boards_{zname}.zip") as z:
        t = z.read(member).decode("utf-8", "replace")
    return rank, scan(t)


if __name__ == "__main__":
    seen, todo = set(), []
    for jf in sorted(glob.glob("/root/corpus/bundle/kcorpus/jobs/W*.json")):
        for j in json.load(open(jf)):
            if j["rank"] in seen: continue
            seen.add(j["rank"]); todo.append((j["rank"], j["zip"], j.get("member", j["path"])))
    todo.sort(key=lambda a: a[1])
    out = {}
    with ProcessPoolExecutor(3) as ex:
        for rank, f in ex.map(job, todo, chunksize=8):
            out[rank] = f
    json.dump(out, open(sys.argv[1], "w"))
    print(len(out), "boards")
