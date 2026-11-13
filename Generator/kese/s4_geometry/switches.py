"""The stack-up lines: which lines of parameters/PCB_elements/Stackup.py keep each prism in the
model (and in every file).  Everything is built first; a prism stays when its lines are True."""
from parameters import GROUPS, P

FACE = {"F": "top", "B": "bottom"}


def lines_of(p):
    """The lines of the stack-up being built that prism p needs, all of them True, to stay.  A prism
    carries its role and its layer: "F.Cu", "In1.Cu", "B.Mask", "F.Finish", or, through the board, a
    span of copper layers ("F.Cu-B.Cu"), "Hole.Finish" and "Edge.Finish"."""
    side = FACE.get(p.layer.split(".")[0])
    if p.role == "silk":
        return (f"{side}_silkscreen",)
    if p.role in ("mask", "mask_over_copper"):
        return (f"{side}_solder_mask",)
    if p.role == "finish":                          # in the holes and on the edge: no side
        return (f"{side}_finish" if side else "hole_finish",)
    if p.role == "copper":
        return (f"{side}_copper" if side else "inner_copper",)
    if p.role == "plating":
        return ("plated_holes",)
    if p.role == "via_resin":
        return ("via_resin",)
    resin = "resin_fill_beside" in p.props          # the laminate: the resin beside the inner copper,
    if P.Stackup.FUSION_BUILD == "PLIES_FUSED":     # a part of its gap's solid with the plies fused
        return ("board", "resin_between_traces") if resin else ("board",)
    if resin:
        return ("resin_between_traces",)
    return ("prepreg_plies" if p.props.get("kind") == "prepreg" else "cores",)


def leave_out(prisms):
    """(the prisms whose lines are all True, the lines that are False in the file's order)."""
    building = P.building()
    return ([p for p in prisms if all(building[line] for line in lines_of(p))],
            [line for line, on in building.items() if not on])


def built(name):
    """Whether a line is built ("via_resin"), or any line of a short name ("finish": the top, the
    bottom or the hole finish)."""
    return any(P.value(f"Stackup.{line}") for line in GROUPS.get(name, (name,)))
