"""What every item handler shares while the tree is walked: the Items being filled, and where a
shape on a given layer goes (copper of a net, a mask opening, silkscreen, or nowhere)."""
from kese.core.sexp import num
from parameters import P


class Context:
    def __init__(self, items):
        self.items = items
        self.layers = items.layers
        self.conditional_pads = []      # (layer, via ring, net): kept only where other copper meets them

    def expand(self, layers):
        """Layer names with wildcards (*.Cu, F&B.Cu, *.Mask, ...) -> plain layer names."""
        out = []
        for l in layers:
            l = str(l)
            if l in ("*.Cu", "F&B.Cu"):
                out += self.layers if l == "*.Cu" else ["F.Cu", "B.Cu"]
            elif l.startswith("*."):
                out += ["F." + l[2:], "B." + l[2:]]
            elif l.startswith("F&B."):
                out += ["F." + l[4:], "B." + l[4:]]
            else:
                out.append(l)
        return out

    def span(self, a, b):
        """The copper layers from a to b, outermost first."""
        i, j = sorted((self.layers.index(a), self.layers.index(b)))
        return self.layers[i:j + 1]

    def bare_margin(self, node, w, solid=False):
        """How far the mask opening of a bare track or drawing (KiCad 9+) reaches past its copper: its own
        solder_mask_margin, else the board's pad-to-mask clearance.  As in KiCad, a negative margin
        narrows a stroke at most to nothing (-w/2); a filled shape's opening keeps at least its inside."""
        m = num(node, "solder_mask_margin")
        m = self.items.mask_clearance if m is None else m
        return m if solid or m >= 0 else max(m, -w / 2)

    def add(self, layer, geom, what, net=None):
        """File a shape under its layer, and count it for the report as `what`."""
        items = self.items
        if geom is None or geom.is_empty:
            return
        if layer in self.layers:
            items.copper_items[layer].append((geom, net or P.Copper.NO_NET_NAME))
        elif layer in ("F.Mask", "B.Mask"):
            items.mask_open_items[layer[0]].append(geom)
        elif layer in P.Silkscreen.SILK_LAYERS:
            items.silk_items[layer[0]].append(geom)
        else:
            items.skipped[f"{what} on {layer} (not a physical layer)"] += 1
            return
        items.found[f"{what} on {layer}"] += 1
