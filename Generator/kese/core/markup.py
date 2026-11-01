"""KiCad's text markup: ~{overbar}, ^{superscript} and _{subscript}, nested as deep as wanted, the way
KiCad's markup parser reads a line of text (include/markup_parser.h, its PEG grammar): a marker
starts a run only when followed by {, the run ends at its closing }, and a marker whose } never
comes is plain text.  Inside a run, {name} (an escape such as {slash}) is plain text.

A line -> [(text, (style, ...)), ...] runs in order, each style "~", "^" or "_"; and the same line
as [(start run, end run)] for each overbar, end exclusive."""
import re

ESCAPE = re.compile(r"\{[A-Za-z_][A-Za-z0-9_]*\}")


def _braces(s, i):
    """The index after the } closing the run whose marker is at i, or None when it never closes."""
    j = i + 2
    while j < len(s):
        if s[j] == "}":
            return j + 1
        if s[j] in "~^_" and j + 1 < len(s) and s[j + 1] == "{":
            end = _braces(s, j)
            if end is None:
                return None
            j = end
            continue
        m = ESCAPE.match(s, j)
        j = m.end() if m else j + 1
    return None


def parse(s):
    """(runs, overbars) of one line, as the module docstring says."""
    runs, bars = [], []

    def walk(i, end, styles, inside):
        text = []
        while i < end:
            close = _braces(s, i) if s[i] in "~^_" and i + 1 < end and s[i + 1] == "{" else None
            if close is not None and close <= end:
                if text:
                    runs.append(("".join(text), styles))
                    text = []
                first = len(runs)
                walk(i + 2, close - 1, styles + (s[i],), True)
                if s[i] == "~":
                    bars.append((first, len(runs)))
                i = close
                continue
            m = ESCAPE.match(s, i) if inside else None
            text.append(m.group(0) if m else s[i])
            i = m.end() if m else i + 1
        if text:
            runs.append(("".join(text), styles))

    walk(0, len(s), (), False)
    return runs, bars
