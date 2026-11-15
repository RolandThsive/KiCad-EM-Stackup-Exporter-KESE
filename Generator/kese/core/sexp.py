"""KiCad s-expression parsing and small accessors used by every stage."""
import math
import re


ESCAPES = {b"a": b"\a", b"b": b"\b", b"f": b"\f", b"n": b"\n", b"r": b"\r", b"t": b"\t", b"v": b"\v",
           b'"': b'"', b"\\": b"\\", b"x": b"x"}
ESCAPE = re.compile(rb"\\(x[0-9A-Fa-f]{1,2}|[0-7]{1,3}|.)", re.DOTALL)


def _escaped(m):
    e = m.group(1)
    if e[:1] == b"x" and len(e) > 1:
        return bytes([int(e[1:], 16)])
    if e[:1] in b"01234567":
        return bytes([int(e, 8) & 0xFF])
    return ESCAPES.get(e, b"\\" + e)       # not an escape: the backslash stays, as in KiCad


def unescape(text):
    """A quoted string of the file as KiCad reads it (DSNLEXER::NextTok): \\n a new line, \\t a tab,
    \\a \\b \\f \\r \\v the other control characters, \\" and \\\\ the character itself, \\x and one or
    two hex digits or a backslash and one to three octal ones a byte of the UTF-8 text; before any
    other character the backslash is kept.  KiCad itself writes only \\n, \\r, \\" and \\\\, and a tab as
    it is.  Done once, here, for every quoted string: net names, text and properties alike."""
    return ESCAPE.sub(_escaped, text.encode("utf-8")).decode("utf-8", "replace")


SPACE = " \t\r\n\0"           # KiCad's whitespace (DSNLEXER's isSpace): a NUL byte is one too
ATOM_ENDS = SPACE + "()"
COMMENT_LINE = re.compile(r"^[ \t\r\0]*#[^\n]*", re.MULTILINE)


def _tokenize(text):
    """KiCad's tokens (DSNLEXER::NextTok): a parenthesis, a string in double quotes, or a bare atom.
    A bare atom runs to whitespace or a parenthesis: a double quote inside it is a character of it, as
    in the inch mark of an old board's (gr_text 0.062" ...), not the start of a string."""
    i, n = 0, len(text)
    while i < n:
        c = text[i]
        if c in SPACE:
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
            while j < n and text[j] not in ATOM_ENDS:
                j += 1
            yield text[i:j]
            i = j


def parse(text):
    """Nested lists; quoted strings and bare atoms both become str.  A line whose first character other
    than whitespace is # is a comment, and is passed over as DSNLEXER does (boards brought over from
    other tools have such lines between the items)."""
    if "#" in text:
        text = COMMENT_LINE.sub("", text)
    root = []
    stack = [root]
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


class NotANumber(ValueError):
    """A number of the file that is not one."""


NOT_FINITE = ("nan", "inf", "infinity")


def number(atom, node=None):
    """A number of the file.  KiCad refuses a board where a number is not one (DSNLEXER: "Expecting
    ..." or "Invalid floating point number"), and so does this: nan, inf, or a number too big for a
    float would put an item nowhere and leave it out without a word.  `node`, where it is, names it."""
    try:
        x = float(atom)
    except (TypeError, ValueError):
        x = math.nan
    if math.isfinite(x):
        return x
    where = f", in ({' '.join(str(a) for a in node if not isinstance(a, list))[:60]} ...)" if node else ""
    raise NotANumber(f"{'nothing' if atom is None else repr(str(atom))} where a number belongs{where}: KiCad refuses such a file too (a damaged file?)")


def numbers(node):
    """The numeric atoms of a node, e.g. (at 1 2 90) -> [1.0, 2.0, 90.0]; a word (unlocked) is passed
    over, a number that is not one (nan) refused."""
    return [number(a, node) for a in atoms(node)
            if re.fullmatch(r"-?[\d.eE+-]+", str(a)) or str(a).lower().lstrip("+-") in NOT_FINITE]


def pt(node):
    return number(node[1], node), number(node[2], node)


def num(node, name, default=None):
    """The number of child `name`, or `default` where the node has no such child; (thickness) with
    nothing in it is no number, as for KiCad."""
    c = child(node, name) if node is not None else None
    return number(c[1] if len(c) > 1 else None, c) if c else default


def word(node, name, default=None):
    """The first value of child `name`, or `default` where the node has no such child or it is empty."""
    c = child(node, name)
    return c[1] if c and len(c) > 1 else default


def layer_of(node):
    c = child(node, "layer")
    return c[1] if c else None


def yes(value):
    return str(value).lower() in ("yes", "true", "solid")
