"""Text variables, ${...}, resolved as KiCad resolves them without its project file (PCB_TEXT::GetShownText,
BOARD::ResolveTextVar, FOOTPRINT::ResolveTextVar, TITLE_BLOCK::TextVarResolver), and the words KiCad may
have shown for a text when it saved the board, to match a render cache against."""
import datetime
import re

from kese.core.sexp import child, children
from kese.s1_read.parse_kicad_version import footprint_text_fields, is_footprint

TEXT_VAR = re.compile(r"\$\{([^{}]+)\}")
# variables whose value when KiCad saved the board is not the value they have today
SAVE_TIME_VARS = {"CURRENT_DATE"}


def board_text_vars(items):
    """{variable: value} for the ${...} a board text can use, as KiCad resolves them without its
    project file (board.cpp BOARD::ResolveTextVar, title_block.cpp TITLE_BLOCK::TextVarResolver):
    the title block, the file name and path, and the board's own (property "name" "value")."""
    if getattr(items, "_text_vars", None) is None:
        tree, raw = items.raw.tree, items.raw
        out = {"FILENAME": raw.path.name, "FILEPATH": str(raw.path.resolve()),
               "CURRENT_DATE": datetime.date.today().isoformat()}
        tb = child(tree, "title_block") or []
        for key, var in (("title", "TITLE"), ("date", "ISSUE_DATE"), ("rev", "REVISION"), ("company", "COMPANY")):
            c = child(tb, key)
            out[var] = str(c[1]) if c is not None and len(c) > 1 else ""
        for c in children(tb, "comment"):
            if len(c) > 2:
                out[f"COMMENT{c[1]}"] = str(c[2])
        for n in range(1, 10):
            out.setdefault(f"COMMENT{n}", "")
        for prop in children(tree, "property"):
            if len(prop) > 2:
                out.setdefault(str(prop[1]), str(prop[2]))
        layer_names = {}
        for l in child(tree, "layers")[1:]:
            if isinstance(l, list) and len(l) > 1:
                layer_names[str(l[1])] = str(l[3]) if len(l) > 3 and not isinstance(l[3], list) else str(l[1])
        fps = {}
        for fp in (n for n in tree[1:] if isinstance(n, list) and n and is_footprint(n)):
            fields = footprint_fields(fp)
            for key in (child(fp, "uuid"), child(fp, "tstamp")):
                if key is not None and len(key) > 1:
                    fps[str(key[1])] = fields
            if "REFERENCE" in fields:
                fps.setdefault(fields["REFERENCE"].upper(), fields)
        items._text_vars, items._layer_names, items._footprint_fields = out, layer_names, fps
    return items._text_vars


def footprint_fields(fp):
    """{FIELD: value} of a footprint, for its own texts' ${...} and other texts' ${REF:FIELD}
    (FOOTPRINT::ResolveTextVar): its properties and reference / value, and its library and name."""
    out = footprint_text_fields(fp)
    lib, _, name = str(fp[1]).rpartition(":") if len(fp) > 1 and not isinstance(fp[1], list) else ("", "", "")
    out.setdefault("FOOTPRINT_LIBRARY", lib)
    out.setdefault("FOOTPRINT_NAME", name)
    return out


def resolve_var(items, board, token, layer, fp_vars):
    """A variable's value as PCB_TEXT::GetShownText gives it (LAYER, the footprint's fields, ${REF:FIELD},
    the board's variables), and whether it is the value KiCad showed when it saved the board: not when
    KESE cannot resolve it (one only the project file defines stays as written, as KiCad shows an unknown
    one), when it changes with the day (${CURRENT_DATE}), or when it holds variables of its own, which
    KiCad may resolve further."""
    if token == "LAYER":
        return items._layer_names.get(layer, layer), True
    if fp_vars and token.upper() in fp_vars:
        value = fp_vars[token.upper()]
        return value, "${" not in value
    if ":" in token:                                # ${<footprint uuid or reference>:<field>}
        ref, _, field = token.partition(":")
        fields = items._footprint_fields.get(ref) or items._footprint_fields.get(ref.upper())
        if fields and field.upper() in fields:
            value = fields[field.upper()]
            return value, "${" not in value
        return f"<Unresolved: {fields.get('REFERENCE', ref) if fields else ref}:{field}>", False
    if token in board:
        value = board[token]
        return value, token not in SAVE_TIME_VARS and "${" not in value
    return "${" + token + "}", False


def shown_text(items, text, layer, fp_vars=None):
    """A text with its ${...} variables resolved as PCB_TEXT::GetShownText does (resolve_var)."""
    if "${" not in text:
        return text
    board = board_text_vars(items)
    return TEXT_VAR.sub(lambda m: resolve_var(items, board, m.group(1), layer, fp_vars)[0], text)


def saved_words(items, text, layer, fp_vars=None):
    """The words KiCad may have shown for a text when it saved the board, as a regular expression: the
    text with each variable whose value then is unknown (resolve_var) free to be any words, and the rest
    as written.  None when every variable is known, as the shown text is then the only words."""
    if "${" not in text:
        return None
    board = board_text_vars(items)
    out, at, loose = [], 0, False
    for m in TEXT_VAR.finditer(text):
        value, known = resolve_var(items, board, m.group(1), layer, fp_vars)
        out += [re.escape(text[at:m.start()]), re.escape(value) if known else "(.*?)"]
        loose, at = loose or not known, m.end()
    out.append(re.escape(text[at:]))
    return re.compile("".join(out), re.S) if loose else None
