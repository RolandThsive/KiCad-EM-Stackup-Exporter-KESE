"""Nets: the board's net table, and the net an item belongs to."""
from kese.s1_read.parse_kicad_version import kicad_unescape, net_of, net_table
from parameters import P

__all__ = ["kicad_unescape", "net_name", "read_nets"]


def read_nets(items, tree):
    """The board's net table -> items.nets {"3": "GND"}."""
    items.nets.update({k: v or P.Copper.NO_NET_NAME for k, v in net_table(tree, items.raw.dialect).items()})


def net_name(items, node):
    """The name of an item's net, NO_NET_NAME for none."""
    return net_of(items.nets, node, items.raw.dialect) or P.Copper.NO_NET_NAME
