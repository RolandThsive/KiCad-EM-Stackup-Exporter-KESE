"""Heights: the thickness of the solder mask (the copper layers' and dielectrics' are
s3_resolve/heights.py)."""
from parameters import P


def mask_thicknesses(st):
    """(over laminate, over copper, where the values come from), mm."""
    M = P.SolderMask
    if M.USE_STACKUP_MASK_THICKNESS and st.mask_thickness:
        return st.mask_thickness, st.mask_thickness, "stackup"
    return M.MASK_OVER_LAMINATE_MM, M.MASK_OVER_COPPER_MM, "parameters/solder_mask.py"
