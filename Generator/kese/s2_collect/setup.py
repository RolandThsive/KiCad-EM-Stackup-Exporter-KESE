"""Board setup: the pad-to-mask clearance, and whether vias are tented (or covered, plugged,
capped, filled) when they don't say."""
from kese.core.sexp import num
from kese.s1_read.parse_kicad_version import board_tenting
from kese.s2_collect.left_out import protection_defaults
from parameters import P


def read_setup(items, setup):
    """(setup ...) -> items.mask_clearance, items.mask_min_width, items.tent_default, items.tent_source, items.via_protection."""
    M = P.SolderMask
    items.mask_clearance = num(setup, "pad_to_mask_clearance", 0.0) if M.PAD_TO_MASK_CLEARANCE_MM is None \
        else M.PAD_TO_MASK_CLEARANCE_MM
    items.mask_min_width = num(setup, "solder_mask_min_width", 0.0) if M.MASK_MIN_WIDTH_MM is None \
        else M.MASK_MIN_WIDTH_MM
    items.tent_default, items.tent_source = board_tenting(setup)
    items.via_protection = protection_defaults(setup)
