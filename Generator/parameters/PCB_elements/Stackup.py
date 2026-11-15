"""
parameters/PCB_elements/Stackup.py - what KESE builds: the stack-up, laid out as a real board is,
from the top silkscreen down to the bottom silkscreen.

This file is the list of what goes into the files KESE writes.  It holds no thickness, material or
colour: those are in each element's own file beside this one (SilkScreen.py, SolderMask.py,
Finish.py, Copper.py, Board.py).

There are two stack-ups, and FUSION_BUILD says which one is built:

    PLIES_SEPARATE  the laminate as a fabricator builds it: every prepreg ply, every core and the
                    resin between the traces of each inner copper layer is its own solid, with its
                    own thickness and material.  This is the default.
    PLIES_FUSED     the laminate as KESE built it up to version 3.3: one solid for each gap between
                    two copper layers.  The prepreg plies of a gap are fused into that solid, and so
                    is the resin between the traces of the inner copper beside it.  Fewer solids.

Each line of a stack-up is one layer of the board, or one kind of layer where a board has several.
True builds it and writes it to every output file, in every mode and format; False leaves it out.
KESE works every line out first and then leaves out the ones set to False, so what stays is exactly
as it is with every line True (with the top solder mask left out, the top finish still ends where
the mask would begin).  At least one line of the stack-up being built must be True.

The lines run as the layers lie in a real board: the top side from the outside in, the inside of
the board, the bottom side from the inside out, and last what goes through the board.  The order
is for reading and changes nothing: how many copper layers a board has, and the plies between
them, come from the board file.  The lines of the inside stand for every inner layer the board has.

On the command line:   --set Stackup.FUSION_BUILD=PLIES_FUSED      picks the stack-up
                       --set Stackup.top_solder_mask=True          sets that line, in both stack-ups
                       --set Stackup.solder_mask=True              sets the top and the bottom line
The short names that set several lines at once:
    silkscreen    top_silkscreen, bottom_silkscreen
    solder_mask   top_solder_mask, bottom_solder_mask
    finish        top_finish, bottom_finish, hole_finish
    copper        top_copper, inner_copper, bottom_copper, plated_holes
"""

# Which of the two stack-ups below KESE builds: "PLIES_FUSED" or "PLIES_SEPARATE"
FUSION_BUILD = "PLIES_SEPARATE"

# --------------------------------------------------------------------------------------------------
# The plies fused: one laminate solid for each gap between two copper layers
# --------------------------------------------------------------------------------------------------
PLIES_FUSED = {
    # line                     build     what it is                                                  set in
    # ---- the top side, from the outside in ------------------------------------------------------------
    "top_silkscreen":          False,  # the legend ink on the top solder mask                       SilkScreen.py
    "top_solder_mask":         False,  # the solder mask on the top face                             SolderMask.py
    "top_finish":              True,   # ENIG, HASL ... on the top copper the mask leaves bare       Finish.py
    "top_copper":              True,   # F.Cu: the foil and the copper plated on it                  Copper.py
    # ---- the inside of the board: these lines stand for every gap and every inner copper layer --------
    "board":                   True,   # the laminate: one solid for each gap, its plies fused       Board.py
    "resin_between_traces":    True,   # the board solids also fill the space between the traces     Board.py
                                       # of the inner copper; False leaves that space empty
    "inner_copper":            True,   # In1.Cu, In2.Cu ...                                          Copper.py
    # ---- the bottom side, from the inside out ---------------------------------------------------------
    "bottom_copper":           True,   # B.Cu: the foil and the copper plated on it                  Copper.py
    "bottom_finish":           True,   # ENIG, HASL ... on the bottom copper the mask leaves bare    Finish.py
    "bottom_solder_mask":      False,  # the solder mask on the bottom face                          SolderMask.py
    "bottom_silkscreen":       False,  # the legend ink on the bottom solder mask                    SilkScreen.py
    # ---- through the board ----------------------------------------------------------------------------
    "plated_holes":            True,   # the plated walls of the vias and the through-hole pads,     Copper.py
                                       # the copper in filled vias, castellations, the plated edge
    "hole_finish":             True,   # the finish inside the plated holes and on the board's edge  Finish.py
    "via_resin":               True,   # the resin in plugged and resin-filled vias                  Copper.py
}

# --------------------------------------------------------------------------------------------------
# The plies separate: every layer of the laminate that is made separately is its own solid
# --------------------------------------------------------------------------------------------------
PLIES_SEPARATE = {
    # line                     build     what it is                                                  set in
    # ---- the top side, from the outside in ------------------------------------------------------------
    "top_silkscreen":          False,  # the legend ink on the top solder mask                       SilkScreen.py
    "top_solder_mask":         False,  # the solder mask on the top face                             SolderMask.py
    "top_finish":              True,   # ENIG, HASL ... on the top copper the mask leaves bare       Finish.py
    "top_copper":              True,   # F.Cu: the foil and the copper plated on it                  Copper.py
    # ---- the inside of the board: these lines stand for every ply, core and inner copper layer --------
    "prepreg_plies":           True,   # each prepreg ply its own solid: "Board_dielectric 1 ply 1"  Board.py
    "resin_between_traces":    True,   # the resin between the traces of each inner copper layer     Board.py
                                       # its own solid: "Board_resin In1.Cu"; False leaves it empty
    "inner_copper":            True,   # In1.Cu, In2.Cu ...                                          Copper.py
    "cores":                   True,   # each core its own solid: "Board_dielectric 2"               Board.py
    # ---- the bottom side, from the inside out ---------------------------------------------------------
    "bottom_copper":           True,   # B.Cu: the foil and the copper plated on it                  Copper.py
    "bottom_finish":           True,   # ENIG, HASL ... on the bottom copper the mask leaves bare    Finish.py
    "bottom_solder_mask":      False,  # the solder mask on the bottom face                          SolderMask.py
    "bottom_silkscreen":       False,  # the legend ink on the bottom solder mask                    SilkScreen.py
    # ---- through the board ----------------------------------------------------------------------------
    "plated_holes":            True,   # the plated walls of the vias and the through-hole pads,     Copper.py
                                       # the copper in filled vias, castellations, the plated edge
    "hole_finish":             True,   # the finish inside the plated holes and on the board's edge  Finish.py
    "via_resin":               True,   # the resin in plugged and resin-filled vias                  Copper.py
}

# Not built in either stack-up: the seed copper under the plated copper (it lies inside the copper
# solid) and the glass cloth inside a ply (a ply is one uniform solid).
