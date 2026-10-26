"""One STEP file written part by part.  OpenCascade holds a whole STEP file in memory, entities
and text, until it has written it: on a big board that is many times the memory of the solids
(PC110: over 12.5 GB for 2.4 GB of solids).  So every part is exported on its own, as an assembly
of that one part, and its entity instances are renumbered into the file at once; the assembly that
holds the parts is written last, as OpenCascade writes it.  The file has the entities OpenCascade
writes for the whole assembly, in another order, but for the origin placement and the colours,
which every part keeps a copy of instead of sharing them; the memory it takes is that of the
biggest part."""
import re
import shutil
from pathlib import Path

_EMPTY, _HASH, _END = "\x01", "\x02", "\x03"         # '', and a '#' or a ';' in a string
_FIRST_STRING = re.compile("'[^']*'|\x01")
_REF = re.compile(r"#(\d+)")
_HEAD = re.compile(r"\s*#(\d+)\s*=\s*(?:\(\s*)?([A-Z0-9_]+)")
_SPACE = re.compile(r"\s*")
_ITEMS = re.compile(r"\(\s*#[^()]*\)")        # the item list of a representation
_DANGLING = "\x04"                             # a reference to an instance that is not written
_CHUNK = 1 << 23                               # characters renumbered at a time
# where the assembly's own instances go: #1 .. #16; the parts follow from #21
_APD, _APP, _SDR, _PDS, _PD, _PDF, _PRODUCT, _PC, _PDC, _REP, _CTX, _PRPC, _UNITS = range(1, 14)


class _Part:
    """The STEP file of one part, an assembly of that part written by OpenCascade, with the '#' and
    ';' in its strings hidden: then every ';' ends an instance, and every '#' starts a reference or
    the name of an instance."""

    def __init__(self, path):
        self.path, self.spans, self.near = path, {}, {}
        text = Path(path).read_text(encoding="latin-1")
        k = text.index("\nDATA;")
        self.head, data = text[:k] + "\nDATA;\n", text[k + 6:text.rindex("ENDSEC;")]
        del text
        pieces = data.replace("''", _EMPTY).split("'")
        del data
        for k in range(1, len(pieces), 2):                  # the strings
            if "#" in pieces[k] or ";" in pieces[k]:
                pieces[k] = pieces[k].replace("#", _HASH).replace(";", _END)
        self.data = "'".join(pieces)

    @staticmethod
    def put_back(text):
        """text with its strings as they were."""
        return text.replace(_EMPTY, "''").replace(_HASH, "#").replace(_END, ";")

    def span(self, i):
        """(start, end) of instance #i, looked for first after the instance that refers to it."""
        if i not in self.spans:
            name, near = f"#{i} =", self.near.get(i, 0)     # '#12 = ', as OpenCascade writes it
            start = self.data.find(name, near)
            if start < 0:
                start = self.data.find(name, 0, near + len(name))
            if start < 0:
                m = re.compile(rf"#{i}\s*=").search(self.data)
                if m is None:
                    raise ValueError(f"{self.path}: no instance #{i}")
                start = m.start()
            self.spans[i] = start, self.data.index(";", start) + 1
        return self.spans[i]

    def refs(self, i):
        """The instances #i refers to, in order."""
        start, end = self.span(i)
        out = [int(r) for r in _REF.findall(self.data, self.data.index("=", start), end)]
        for r in out:
            self.near.setdefault(r, start)
        return out

    def of_type(self, kind):
        """The instances of a (simple) type, in order."""
        out, k = [], self.data.find(kind + "(")
        while k >= 0:
            h = _HEAD.match(self.data, self.data.rfind(";", 0, k) + 1)
            if h and h.end() == k + len(kind):
                out.append(int(h.group(1)))
                self.spans.setdefault(out[-1], (h.start(1) - 1, self.data.index(";", k) + 1))
            k = self.data.find(kind + "(", k + 1)
        return out

    def assembly(self):
        """{id: place} of the instances that make the assembly, its NAUO, and (origin, placement):
        the two items its transformation maps, in the part and in the assembly."""
        nauo = self.of_type("NEXT_ASSEMBLY_USAGE_OCCURRENCE")[0]
        pd = self.refs(nauo)[0]
        _, rep, transform = self.refs(self.refs(self.of_type("CONTEXT_DEPENDENT_SHAPE_REPRESENTATION")[0])[0])
        origin, placement = self.refs(transform)
        ctx = self.refs(rep)[-1]
        pdf, pdc = self.refs(pd)
        product = self.refs(pdf)[0]
        apd = self.of_type("APPLICATION_PROTOCOL_DEFINITION")[0]
        top = {apd: _APD, self.refs(apd)[0]: _APP, pd: _PD, pdf: _PDF, product: _PRODUCT,
               self.refs(product)[0]: _PC, pdc: _PDC, rep: _REP, ctx: _CTX}
        top.update({i: _PDS for i in self.of_type("PRODUCT_DEFINITION_SHAPE") if self.refs(i) == [pd]})
        top.update({i: _SDR for i in self.of_type("SHAPE_DEFINITION_REPRESENTATION") if self.refs(i)[1:] == [rep]})
        top.update({i: _PRPC for i in self.of_type("PRODUCT_RELATED_PRODUCT_CATEGORY") if self.refs(i) == [product]})
        for k, i in enumerate(self.refs(ctx)):          # its units and uncertainty
            top[i] = _UNITS + k
        if len(set(top.values())) != len(top) or len(top) > 16:
            raise ValueError(f"{self.path}: unexpected STEP assembly")
        return top, nauo, origin, placement


class StepFile:
    """add(path) with the STEP file of every part, an assembly of that one part written by
    OpenCascade; then close(), and discard() to remove what is left."""

    def __init__(self, path):
        self.path = Path(path)
        self.body_path = self.path.with_name(self.path.name + ".body")
        self.body = open(self.body_path, "w", encoding="latin-1", newline="\n")   # as OpenCascade writes
        self.next_id, self.placements, self.top = 21, [], None

    def add(self, part_path):
        part = _Part(part_path)
        top, nauo, origin, placement = part.assembly()
        base, data = self.next_id - 1, part.data
        new = lambda i: top.get(i, i + base)
        # what is written: every instance but the assembly's, with the part's number as its NAUO's id
        start, end = part.span(nauo)
        edits = sorted([(*part.span(i), None) for i in top] +
                       [(start, end, _FIRST_STRING.sub(f"'{len(self.placements) + 1}'", data[start:end], count=1))])
        pieces, at = [], _SPACE.match(data).end()
        for start, end, text in edits:
            pieces.append((at, start))
            if text:
                pieces.append(text)
            at = _SPACE.match(data, end).end() if text is None else end
        pieces.append((at, data.rindex(";") + 1))
        # every '#' is a reference or a name: renumbered a chunk at a time, each ending an instance
        to = {i: f"#{top[i]}" if top[i] in (_APP, _PD, _REP) else _DANGLING for i in top}
        last = 0
        for piece in pieces:
            if isinstance(piece, str):
                last = max(last, self._write(part, piece, to, base))
                continue
            at, end = piece
            while at < end:
                cut = min(end, data.find(";", at + _CHUNK) + 1 or end)
                last = max(last, self._write(part, data[at:cut], to, base))
                at = cut
        self.body.write("\n")
        if self.top is None:
            self.head, self.origin = part.head, new(origin)
            self.top = {top[i]: part.put_back(_REF.sub(lambda m: f"#{new(int(m.group(1)))}", data[slice(*part.span(i))]))
                        for i in top}
        self.placements.append(new(placement))
        self.next_id = base + last + 1

    def _write(self, part, text, to, base):
        """text renumbered into the file -> the highest id in it."""
        pieces = _REF.split(text)
        ids = list(map(int, pieces[1::2]))
        pieces[1::2] = [to.get(i) or f"#{i + base}" for i in ids]
        text = part.put_back("".join(pieces))
        if _DANGLING in text:
            raise ValueError(f"{part.path}: a part refers to the assembly's own instances")
        self.body.write(text)
        return max(ids, default=0)

    def close(self):
        """Write the file: the assembly, then every part.  -> its path, or None with no part."""
        self.body.close()
        if self.top is None:
            return None
        refs = [f"#{i}" for i in [self.origin] + self.placements]
        items = ",\n    ".join(",".join(refs[k:k + 8]) for k in range(0, len(refs), 8))
        with open(self.path, "w", encoding="latin-1", newline="\n") as f:
            f.write(self.head)
            for i in sorted(self.top):
                x = self.top[i]
                if i == _REP:                             # the assembly: every part's placement
                    x = _ITEMS.sub(lambda m: f"({items})", x, count=1)
                f.write(x + "\n")
            with open(self.body_path, encoding="latin-1", newline="") as body:
                shutil.copyfileobj(body, f, 1 << 24)
            f.write("ENDSEC;\nEND-ISO-10303-21;\n")
        return self.path

    def discard(self):
        self.body.close()
        self.body_path.unlink(missing_ok=True)
