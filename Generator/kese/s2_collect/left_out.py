"""What KESE reads past, counted under "skipped" in report.txt: unknown items, and KiCad 10's hole
options when a setting switches them off (Board.BACKDRILLS, Board.POST_MACHINING,
Copper.VIA_PROTECTION)."""
from kese.core.sexp import child
from kese.s2_collect.machining import SWITCHED_OFF

UNKNOWN = "items (unknown to KESE)"


def count_padstack(items, node, what):
    """A pad's or via's padstack (KiCad 9+, a shape per copper layer), under items.found."""
    if child(node, "padstack") is not None:
        items.found[f"{what} with a padstack (a shape per layer)"] += 1


def warn(items, log):
    """One warning for what the board has that a setting leaves out, one for the kinds KESE does not know."""
    left = [what.split(" (")[0] for what in sorted(items.skipped) if what.endswith(SWITCHED_OFF)]
    if left:
        log(f"warning: not modelled, see 'skipped' in report.txt: {', '.join(left)}")
    unknown = [f"{what[:-len(UNKNOWN)].strip()} ({n})" for what, n in sorted(items.skipped.items()) if what.endswith(UNKNOWN)]
    if unknown:
        log(f"warning: left out, of a kind KESE does not know: {', '.join(unknown)}")
