"""Text variables, ${...}, resolved as KiCad resolves them without its project file (PCB_TEXT::GetShownText,
BOARD::ResolveTextVar, FOOTPRINT::ResolveTextVar, TITLE_BLOCK::TextVarResolver), and the words KiCad may
have shown for a text when it saved the board, to match a render cache against."""
import datetime
import re

from kese.core.sexp import child, children
from kese.s1_read.parse_kicad_version import footprint_text_fields, is_footprint, text_var_rules

TEXT_VAR = re.compile(r"\$\{([^{}]+)\}")
TITLE_VARS = (("title", "TITLE"), ("date", "ISSUE_DATE"), ("rev", "REVISION"), ("company", "COMPANY"))


def board_text_vars(items):
    """What a board text's ${...} can use, read once per board: the title block's values as written
    ({TITLE, ISSUE_DATE, REVISION, COMPANY, COMMENT1..9}), the board's own (property "name" "value"),
    which are KiCad's copy of the project's text variables (BOARD::SynchronizeProperties), the layers'
    user names, the footprints' fields, and the rules of the KiCad that wrote the file."""
    if getattr(items, "_title_block", None) is None:
        tree = items.raw.tree
        tb = child(tree, "title_block") or []
        title = {}
        for key, var in TITLE_VARS:
            c = child(tb, key)
            title[var] = str(c[1]) if c is not None and len(c) > 1 else ""
        for c in children(tb, "comment"):
            if len(c) > 2:
                title[f"COMMENT{c[1]}"] = str(c[2])
        for n in range(1, 10):
            title.setdefault(f"COMMENT{n}", "")
        props = {}
        for prop in children(tree, "property"):
            if len(prop) > 2:
                props.setdefault(str(prop[1]), str(prop[2]))
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
        items._board_props, items._layer_names, items._footprint_fields = props, layer_names, fps
        items._text_var_rules, items._title_block = text_var_rules(items.raw.dialect), title
    return items._title_block


def footprint_fields(fp):
    """{FIELD: value} of a footprint, for its own texts' ${...} and other texts' ${REF:FIELD}
    (FOOTPRINT::ResolveTextVar): its properties and reference / value, and its library and name."""
    out = footprint_text_fields(fp)
    lib, _, name = str(fp[1]).rpartition(":") if len(fp) > 1 and not isinstance(fp[1], list) else ("", "", "")
    out.setdefault("FOOTPRINT_LIBRARY", lib)
    out.setdefault("FOOTPRINT_NAME", name)
    return out


def today():
    return datetime.date.today().isoformat()


def title_value(items, token):
    """TITLE_BLOCK::TextVarResolver: the title block's value with its own ${...} expanded once by the
    project's variables (the board's properties stand in for them) and, where the rules say so,
    ${CURRENT_DATE}, as [(words, known)]; None when that leaves "${token}", which KiCad then looks up
    further.  A variable the properties do not hold stays as written and is not known."""
    raw, props, out, at = items._title_block[token], items._board_props, [], 0
    for m in TEXT_VAR.finditer(raw):
        name = m.group(1)
        out.append((raw[at:m.start()], True))
        if name in props:
            out.append((props[name], True))
        elif name == "CURRENT_DATE":                # before KiCad's project resolver knew it, as written
            out.append((today(), False) if items._text_var_rules.date_in_title_block else (m.group(0), True))
        else:
            out.append((m.group(0), False))
        at = m.end()
    out.append((raw[at:], True))
    return None if "".join(w for w, _ in out) == "${" + token + "}" else out


def field_value(items, fields, name, layer, levels, passes, depth):
    """A footprint field's value as [(words, known)], its own ${...} expanded in its footprint as
    FOOTPRINT::ResolveTextVar does: with the passes left where there are several (it gives every field's
    GetShownText), else a reference or value while levels are left, any other field as written."""
    value = fields[name]
    if "${" in value and passes > 1:
        return expand(items, value, layer, fields, passes - 1, depth)
    if "${" in value and depth < levels and name in ("REFERENCE", "VALUE"):
        return expand(items, value, layer, fields, 1, depth + 1)
    return [(value, True)]


def resolve_var(items, token, layer, fp_vars, passes=1, depth=0):
    """One variable's value in one pass, as [(words, known)] (PCB_TEXT::GetShownText's resolver): LAYER,
    the footprint's fields, ${REF:FIELD}, then the board (BOARD::ResolveTextVar: its file name and path,
    and its properties and title block in the order of the KiCad that wrote it).  Known is whether the
    words are what KiCad showed when it saved the board: not for a variable KESE cannot resolve (one
    only the project file defines stays as written, as KiCad shows an unknown one) or ${CURRENT_DATE}."""
    own, xref = items._text_var_rules.field_levels
    if token == "LAYER":
        return [(items._layer_names.get(layer, layer), True)]
    if fp_vars and token.upper() in fp_vars:
        return field_value(items, fp_vars, token.upper(), layer, own, passes, depth)
    if ":" in token:                                # ${<footprint uuid or reference>:<field>}
        ref, _, field = token.partition(":")
        fields = items._footprint_fields.get(ref) or items._footprint_fields.get(ref.upper())
        if fields and field.upper() in fields:
            return field_value(items, fields, field.upper(), layer, xref, passes, depth)
        return [(f"<Unresolved: {fields.get('REFERENCE', ref) if fields else ref}:{field}>", False)]
    if token in ("FILENAME", "FILEPATH"):
        path = items.raw.path
        return [(path.name if token == "FILENAME" else str(path.resolve()), True)]
    props = items._board_props
    if items._text_var_rules.properties_first and token in props:
        return [(props[token], True)]
    if token == "CURRENT_DATE":
        return [(today(), False)]
    if token in items._title_block and (value := title_value(items, token)) is not None:
        return value
    if token in props:
        return [(props[token], True)]
    return [("${" + token + "}", False)]


def expand(items, text, layer, fp_vars, passes, depth=0):
    """[(words, known)] of a text with its ${...} resolved as PCB_TEXT::GetShownText does: a value's own
    ${...} are resolved by the next pass while passes are left, else shown as written, as KiCad shows
    them."""
    out, at = [], 0
    for m in TEXT_VAR.finditer(text):
        out.append((text[at:m.start()], True))
        for words, known in resolve_var(items, m.group(1), layer, fp_vars, passes, depth):
            if passes > 1 and "${" in words:
                out += expand(items, words, layer, fp_vars, passes - 1, depth)
            else:
                out.append((words, known))
        at = m.end()
    out.append((text[at:], True))
    return out


def shown_text(items, text, layer, fp_vars=None):
    """A text with its ${...} variables resolved as PCB_TEXT::GetShownText does (expand)."""
    if "${" not in text:
        return text
    board_text_vars(items)
    return "".join(w for w, _ in expand(items, text, layer, fp_vars, items._text_var_rules.passes))


def saved_words(items, text, layer, fp_vars=None):
    """The words KiCad may have shown for a text when it saved the board, as a regular expression: the
    text with each part KESE cannot know (resolve_var) free to be any words, and the rest as shown.
    None when every part is known, as the shown text is then the only words."""
    if "${" not in text:
        return None
    board_text_vars(items)
    parts = expand(items, text, layer, fp_vars, items._text_var_rules.passes)
    if all(known for _, known in parts):
        return None
    return re.compile("".join(re.escape(w) if known else "(.*?)" for w, known in parts), re.S)
