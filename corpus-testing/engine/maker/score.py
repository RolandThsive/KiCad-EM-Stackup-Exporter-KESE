"""A board's counts from its .kicad_pcb, as the corpus complexity list counts them, and its score:

    score = tracks + 3 x vias + 2 x parts + 60 x big chips + 150 x BGAs   (scaled down in proportion below 10 parts)

    parts      footprints with 2 or more pads (stitching vias, mounting holes, fiducials and logos not counted)
    tracks     routed copper track segments and arcs        vias       vias
    big chips  chips of 32 pads or more in QFP, QFN, BGA, LGA or DIMM-style packages
    BGAs       BGA, LGA or CSP chips of 25 pads or more, counted again on top of the big chips
    layers     copper layers                                kicad      the KiCad major version that wrote the file

The level: EXTREME 20,000 and over, VERY HIGH 8,000, HIGH 3,000, MEDIUM 1,000, LOW 250, SIMPLE below.

The maker works out every board's score, level and rank from the counts in its board.json. RunABoard/run_a_board.py
writes a new board's board.json with count() and features.scan(); this prints the same for one file:

    python3 corpus-testing/engine/maker/score.py <board.kicad_pcb>

Checked against the corpus complexity list on 160 of its boards: the score came out the same on about 9 in 10; the
others are older KiCad files (KiCad 4 and 5) and a few chip packages named in other ways."""
import json
import re
import sys
from pathlib import Path



def _parse(t):
    stack = [[]]
    for m in re.finditer(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()"]+', t):
        tok = m.group(0)
        if tok == "(":
            stack.append([])
        elif tok == ")":
            if len(stack) > 1:
                x = stack.pop(); stack[-1].append(x)
        else:
            stack[-1].append(tok[1:-1] if tok.startswith('"') else tok)
    while len(stack) > 1:                                  # a file cut short: close what is open
        x = stack.pop(); stack[-1].append(x)
    return next((x for x in stack[0] if isinstance(x, list) and x and x[0] == "kicad_pcb"), [])


def _kids(node, head):
    return [c for c in node if isinstance(c, list) and c and c[0] == head]


def kicad_major(root):
    gv = _kids(root, "generator_version")
    if gv and re.match(r"\d+", str(gv[0][1])):
        return int(re.match(r"\d+", str(gv[0][1])).group(0))
    v = int((_kids(root, "version") or [[0, "0"]])[0][1] or 0)
    for since, major in ((20240108, 8), (20221018, 7), (20211014, 6), (20171130, 5)):
        if v >= since:
            return major
    return 4


def count(data):
    """The counts of a .kicad_pcb file, given its bytes."""
    t = data.decode("utf-8", "replace")
    root = _parse(t)
    parts = big = bga = 0
    for fp in _kids(root, "footprint") + _kids(root, "module"):
        name = fp[1] if len(fp) > 1 and isinstance(fp[1], str) else ""
        pads = len(_kids(fp, "pad"))
        if pads < 2:                                       # mounting holes, fiducials, logos, stitching vias
            continue
        parts += 1
        if pads >= 32 and re.search(r"qfp|qfn|bga|lga|dimm", name, re.I): big += 1
        if pads >= 25 and re.search(r"bga|lga|csp", name, re.I): bga += 1
    tracks = len(_kids(root, "segment")) + len(_kids(root, "arc"))
    vias = len(re.findall(r"\(via\s+\(at", t))
    layers = max((sum(1 for l in ls[1:] if isinstance(l, list) and len(l) > 1 and str(l[1]).endswith(".Cu"))
                  for ls in _kids(root, "layers")), default=0)
    notes = "no components" if parts == 0 else "mostly unrouted" if parts >= 40 and tracks < 0.3 * parts else ""
    return dict(layers=layers, parts=parts, big=big, bga=bga, tracks=tracks, vias=vias,
                size_mb=round(len(data) / 1e6, 1), kicad=kicad_major(root), notes=notes)


def score(b):
    s = b["tracks"] + 3 * b["vias"] + 2 * b["parts"] + 60 * b["big"] + 150 * b["bga"]
    return s * b["parts"] // 10 if b["parts"] < 10 else s


def level(s):
    for name, low in (("EXTREME", 20000), ("VERY HIGH", 8000), ("HIGH", 3000), ("MEDIUM", 1000), ("LOW", 250)):
        if s >= low:
            return name
    return "SIMPLE"


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from features import scan
    data = Path(sys.argv[1]).read_bytes()
    c = count(data)
    c["features"] = scan(data.decode("utf-8", "replace"))
    print(json.dumps(c, indent=1))
    print(f"score {score(c):,} ({level(score(c))})", file=sys.stderr)
