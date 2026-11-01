"""Nets: the board's net table, and the net an item belongs to."""
from kese.core.sexp import child, children
from parameters import P

# KiCad's {token} escapes in net names (string_utils.cpp, UnescapeString)
NET_ESCAPES = {"dblquote": '"', "quote": "'", "lt": "<", "gt": ">", "backslash": "\\", "slash": "/", "bar": "|",
               "comma": ",", "colon": ":", "space": " ", "dollar": "$", "tab": "\t", "return": "\n", "brace": "{"}


def kicad_unescape(s):
    """A net name as KiCad shows it: KiCad 6+ stores characters a net name cannot hold as {slash},
    {colon}, ... (a label "A/B" on the root sheet is the net "/A{slash}B", shown "/A/B").  Markup -
    ~{overbar}, ^{super}, _{sub}, ${var} - and unknown tokens stay as written, as in KiCad."""
    if len(s) <= 2 or "{" not in s:
        return s
    out, i, n, prev = [], 0, len(s), ""
    while i < n:
        ch = s[i]
        if ch != "{":
            out.append(ch)
            prev, i = ch, i + 1
            continue
        depth, j = 1, i + 1
        while j < n:
            depth += {"{": 1, "}": -1}.get(s[j], 0)
            if depth <= 0:
                break
            j += 1
        token = s[i + 1:j]
        if j >= n:                                   # not closed
            out.append("{" + kicad_unescape(token))
        elif prev in "$~^_" and prev:
            out.append("{" + kicad_unescape(token) + "}")
        elif token in NET_ESCAPES:
            out.append(NET_ESCAPES[token])
        else:
            out.append("{" + kicad_unescape(token) + "}")
        prev, i = "}", j + 1
    return "".join(out)


def read_nets(items, tree):
    """(net 3 "GND") entries -> items.nets {"3": "GND"}."""
    for n in children(tree, "net"):
        items.nets[str(n[1])] = kicad_unescape(str(n[2])) if len(n) > 2 and str(n[2]) else P.Copper.NO_NET_NAME


def net_name(items, node):
    """(net 3) in KiCad <= 9 is a net number; KiCad 10 writes the net name itself."""
    n = child(node, "net")
    if not n or len(n) < 2:
        return P.Copper.NO_NET_NAME
    key = str(n[1])
    if key in items.nets:
        return items.nets[key]
    return kicad_unescape(key) if key and key != "0" else P.Copper.NO_NET_NAME
