"""Nets: the board's net table, and the net an item belongs to."""
from kese.core.sexp import child, children
from parameters import P


def read_nets(items, tree):
    """(net 3 "GND") entries -> items.nets {"3": "GND"}."""
    for n in children(tree, "net"):
        items.nets[str(n[1])] = str(n[2]) if len(n) > 2 and str(n[2]) else P.Copper.NO_NET_NAME


def net_name(items, node):
    """(net 3) in KiCad <= 9 is a net number; KiCad 10 writes the net name itself."""
    n = child(node, "net")
    if not n or len(n) < 2:
        return P.Copper.NO_NET_NAME
    key = str(n[1])
    if key in items.nets:
        return items.nets[key]
    return key if key and key != "0" else P.Copper.NO_NET_NAME
