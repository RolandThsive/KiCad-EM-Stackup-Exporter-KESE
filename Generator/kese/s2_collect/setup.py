"""Board setup: the pad-to-mask clearance, and whether vias are tented (or covered, plugged,
capped, filled) when they don't say."""
from kese.core.sexp import atoms, child, num, yes
from kese.s2_collect.left_out import protection_defaults
from parameters import P


def read_setup(items, setup):
    """(setup ...) -> items.mask_clearance, items.tent_default, items.tent_source, items.via_protection."""
    M = P.SolderMask
    items.mask_clearance = num(setup, "pad_to_mask_clearance", 0.0) if M.PAD_TO_MASK_CLEARANCE_MM is None \
        else M.PAD_TO_MASK_CLEARANCE_MM
    ten = child(setup, "tenting")
    if ten is not None:
        items.tent_default = {}
        for side, key in (("F", "front"), ("B", "back")):
            c = child(ten, key)
            items.tent_default[side] = yes(c[1]) if c is not None and len(c) > 1 else key in atoms(ten)
        items.tent_source = "board setup (tenting)"
    else:
        pp = child(setup, "pcbplotparams")
        vom = child(pp, "viasonmask") if pp else None
        open_ = bool(vom) and yes(vom[1])
        items.tent_default = {"F": not open_, "B": not open_}
        items.tent_source = "plot setting viasonmask" if vom else "KiCad default (vias tented)"
    items.via_protection = protection_defaults(setup)
