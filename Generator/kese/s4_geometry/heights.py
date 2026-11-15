"""Heights: the thickness of the solder mask (the copper layers' and dielectrics' are
s3_resolve/heights.py), and what the mask is made of."""
from parameters import P


def mask_thicknesses(st):
    """(over laminate, over copper, where the values come from), mm."""
    M = P.SolderMask
    if M.USE_STACKUP_MASK_THICKNESS and st.mask_thickness:
        return st.mask_thickness, st.mask_thickness, "stackup"
    return M.MASK_OVER_LAMINATE_MM, M.MASK_OVER_COPPER_MM, "parameters/PCB_elements/SolderMask.py"


def mask_material(st, layer):
    """{material, epsilon_r, loss_tangent} of the mask on `layer` ("F.Mask" / "B.Mask") for
    materials.json: what the board file gives for that layer (SolderMask.USE_STACKUP_MASK_MATERIAL),
    and the values of SolderMask.py for what it leaves out."""
    M = P.SolderMask
    given = st.mask_materials.get(layer, {}) if M.USE_STACKUP_MASK_MATERIAL else {}
    return {"material": M.MASK_MATERIAL, "epsilon_r": M.MASK_EPSILON_R, "loss_tangent": M.MASK_LOSS_TANGENT, **given}
