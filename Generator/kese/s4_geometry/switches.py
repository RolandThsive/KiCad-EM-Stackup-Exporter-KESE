"""The part switches: which parameter keeps each role of part in the model (and in every file)."""
from parameters import P

SWITCHES = {"board": "Board.BOARD_ENABLED", "copper": "Copper.COPPER_ENABLED", "plating": "Copper.COPPER_ENABLED",
            "finish": "Finish.FINISH_ENABLED", "mask": "SolderMask.SOLDER_MASK_ENABLED",
            "mask_over_copper": "SolderMask.SOLDER_MASK_ENABLED", "silk": "Silkscreen.SILKSCREEN_ENABLED"}


def is_on(key):
    """The value of a switch, "Module.NAME"."""
    module, name = key.split(".")
    return getattr(getattr(P, module), name)


def enabled(role):
    return is_on(SWITCHES[role])


def switched_off():
    """The switches that are off, sorted."""
    return sorted({key for key in SWITCHES.values() if not is_on(key)})
