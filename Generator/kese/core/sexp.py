"""KiCad s-expression parsing and small accessors used by every stage."""
import re


ESCAPES = {"n": "\n", "r": "\r", "t": "\t"}


def unescape(text):
    """A quoted string of the file as KiCad reads it: \\n a new line, \\t a tab, \\" and \\\\ the
    character itself (KiCad writes \\n, \\r, \\" and \\\\, and a tab as it is).  Done once, here, for
    every quoted string: net names, text and properties alike."""
    return re.sub(r"\\(.)", lambda m: ESCAPES.get(m.group(1), m.group(1)), text, flags=re.DOTALL)


def _tokenize(text):
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c in " \t\r\n":
            i += 1
        elif c in "()":
            yield c
            i += 1
        elif c == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            raw = text[i + 1:j]
            yield ("str", unescape(raw) if "\\" in raw else raw)
            i = j + 1
        else:
            j = i
            while j < n and text[j] not in ' \t\r\n()"':
                j += 1
            yield text[i:j]
            i = j


def parse(text):
    """Nested lists; quoted strings and bare atoms both become str."""
    root, stack = [], []
    stack.append(root)
    for tok in _tokenize(text):
        if tok == "(":
            node = []
            stack[-1].append(node)
            stack.append(node)
        elif tok == ")":
            if len(stack) > 1:
                stack.pop()
        else:
            stack[-1].append(tok[1] if isinstance(tok, tuple) else tok)
    if len(stack) > 1:      # KiCad refuses such a file too
        raise ValueError(f"the file ends with {len(stack) - 1} parenthes{'es' if len(stack) > 2 else 'is'} "
                         "still open: it is cut short (an incomplete download or copy?)")
    return root[0] if root else []


def children(node, name):
    return [c for c in node if isinstance(c, list) and c and c[0] == name]


def child(node, name):
    for c in node:
        if isinstance(c, list) and c and c[0] == name:
            return c
    return None


def atoms(node):
    return [a for a in node[1:] if not isinstance(a, list)]


def numbers(node):
    """The numeric atoms of a node, e.g. (at 1 2 90) -> [1.0, 2.0, 90.0]."""
    return [float(a) for a in atoms(node) if re.fullmatch(r"-?[\d.eE+-]+", str(a))]


def pt(node):
    return float(node[1]), float(node[2])


def num(node, name, default=None):
    c = child(node, name) if node is not None else None
    return float(c[1]) if c else default


def layer_of(node):
    c = child(node, "layer")
    return c[1] if c else None


def yes(value):
    return str(value).lower() in ("yes", "true", "solid")
