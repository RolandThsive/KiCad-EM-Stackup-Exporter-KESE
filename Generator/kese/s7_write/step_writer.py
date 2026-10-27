"""A STEP file (AP214, as OpenCascade writes it) put together from text: the header, one product
per part with its solids and colour, and the assembly that holds the parts.  Entities are numbered
as they are reserved and written as they are made; the assembly, which lists every part's
placement, comes last."""
from datetime import UTC, datetime
from pathlib import Path

# the assembly's own entities, #1 to #24
ORIGIN, CONTEXT, PRODUCT, DEFINITION, REPRESENTATION = 11, 19, 7, 5, 10
FIRST_FREE = 25
PER_LINE = 8                      # references per line in a long list


def real(x):
    """A number as STEP writes reals: always with a decimal point, the exponent as E."""
    s = repr(float(x))
    if "e" in s:
        m, e = s.split("e")
        return (m if "." in m else m + ".") + "E" + e
    return s


def text(s):
    """A string as STEP writes it: quotes doubled, what is not ASCII as \\X2\\...\\X0\\."""
    out, k = [], 0
    while k < len(s):
        if ord(s[k]) < 128:
            out.append("''" if s[k] == "'" else s[k])
            k += 1
        else:
            j = k
            while j < len(s) and ord(s[j]) >= 128:
                j += 1
            wide = any(ord(c) > 0xFFFF for c in s[k:j])
            out.append(("\\X4\\" if wide else "\\X2\\") + "".join(f"{ord(c):08X}" if wide else f"{ord(c):04X}" for c in s[k:j]) + "\\X0\\")
            k = j
    return "'" + "".join(out) + "'"


def refs(ids):
    """A list of references, a few per line."""
    ids = [f"#{i}" for i in ids]
    return "(" + ",\n    ".join(",".join(ids[k:k + PER_LINE]) for k in range(0, len(ids), PER_LINE)) + ")"


class StepWriter:
    """reserve() ids, write() lines of entities, add_part() when a part's solids are written, then
    close().  The file is written from its first line as the parts come; the assembly that holds
    the parts (entities #1 to #24, which list every part's placement) goes at the end of the data
    section, where a STEP reader finds it as well as at the start."""

    def __init__(self, path, name, units):
        self.path, self.name, self.units = Path(path), name, units
        self.file = open(self.path, "w", encoding="latin-1", newline="\n")   # noqa: SIM115  (open until close())
        self.file.write(self.header())
        self.next, self.placements, self.parts = FIRST_FREE, [], 0

    def reserve(self, count):
        """The first of `count` fresh entity numbers."""
        first = self.next
        self.next += count
        return first

    def write(self, lines):
        self.file.write("\n".join(lines) + "\n")

    def add_part(self, name, rgb, solids):
        """The product that holds a part's solids (written already), its placement in the
        assembly, and its colour."""
        self.parts += 1
        p = self.reserve(26 + len(solids))                 # 19 for the product, a STYLED_ITEM per solid, 7 for the colour
        placement = p + 8
        self.placements.append(placement)
        colour = p + 19 + len(solids)
        lines = [
            f"#{p} = SHAPE_DEFINITION_REPRESENTATION(#{p + 1},#{p + 7});",
            f"#{p + 1} = PRODUCT_DEFINITION_SHAPE('','',#{p + 2});",
            f"#{p + 2} = PRODUCT_DEFINITION('design','',#{p + 3},#{p + 6});",
            f"#{p + 3} = PRODUCT_DEFINITION_FORMATION('','',#{p + 4});",
            f"#{p + 4} = PRODUCT({text(name)},{text(name)},'',(#{p + 5}));",
            f"#{p + 5} = PRODUCT_CONTEXT('',#2,'mechanical');",
            f"#{p + 6} = PRODUCT_DEFINITION_CONTEXT('part definition',#2,'design');",
            f"#{p + 7} = ADVANCED_BREP_SHAPE_REPRESENTATION('',{refs([ORIGIN] + list(solids))},#{CONTEXT});",
            f"#{placement} = AXIS2_PLACEMENT_3D('',#{p + 9},#{p + 10},#{p + 11});",
            f"#{p + 9} = CARTESIAN_POINT('',(0.,0.,0.));",
            f"#{p + 10} = DIRECTION('',(0.,0.,1.));",
            f"#{p + 11} = DIRECTION('',(1.,0.,0.));",
            f"#{p + 12} = CONTEXT_DEPENDENT_SHAPE_REPRESENTATION(#{p + 13},#{p + 15});",
            (f"#{p + 13} = ( REPRESENTATION_RELATIONSHIP('','',#{p + 7},#{REPRESENTATION}) "
             f"REPRESENTATION_RELATIONSHIP_WITH_TRANSFORMATION(#{p + 14}) SHAPE_REPRESENTATION_RELATIONSHIP() );"),
            f"#{p + 14} = ITEM_DEFINED_TRANSFORMATION('','',#{ORIGIN},#{placement});",
            f"#{p + 15} = PRODUCT_DEFINITION_SHAPE('Placement','Placement of an item',#{p + 16});",
            f"#{p + 16} = NEXT_ASSEMBLY_USAGE_OCCURRENCE('{self.parts}',{text(name)},'',#{DEFINITION},#{p + 2},$);",
            f"#{p + 17} = PRODUCT_RELATED_PRODUCT_CATEGORY('part',$,(#{p + 4}));",
            f"#{p + 18} = MECHANICAL_DESIGN_GEOMETRIC_PRESENTATION_REPRESENTATION('',{refs(range(p + 19, p + 19 + len(solids)))},#{CONTEXT});",
        ]
        lines += [f"#{p + 19 + k} = STYLED_ITEM('color',(#{colour}),#{s});" for k, s in enumerate(solids)]
        r, g, b = (real(c / 255) for c in rgb)
        lines += [
            f"#{colour} = PRESENTATION_STYLE_ASSIGNMENT((#{colour + 1}));",
            f"#{colour + 1} = SURFACE_STYLE_USAGE(.BOTH.,#{colour + 2});",
            f"#{colour + 2} = SURFACE_SIDE_STYLE('',(#{colour + 3}));",
            f"#{colour + 3} = SURFACE_STYLE_FILL_AREA(#{colour + 4});",
            f"#{colour + 4} = FILL_AREA_STYLE('',(#{colour + 5}));",
            f"#{colour + 5} = FILL_AREA_STYLE_COLOUR('',#{colour + 6});",
            f"#{colour + 6} = COLOUR_RGB('',{r},{g},{b});",
        ]
        self.write(lines)

    def header(self):
        """The file's header section and the start of its data section."""
        when = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S")
        return "\n".join([
            "ISO-10303-21;",
            "HEADER;",
            "FILE_DESCRIPTION(('KiCad EM Stackup Exporter model'),'2;1');",
            f"FILE_NAME({text(self.path.name)},'{when}',(''),(''),'KESE','KESE','');",
            "FILE_SCHEMA(('AUTOMOTIVE_DESIGN { 1 0 10303 214 1 1 1 1 }'));",
            "ENDSEC;",
            "DATA;",
        ]) + "\n"

    def assembly(self):
        """The assembly: its product, the units, and the placements of every part."""
        unit = "SI_UNIT(.MILLI.,.METRE.)" if self.units == "mm" else "SI_UNIT($,.METRE.)"
        accuracy = "1.E-07" if self.units == "mm" else "1.E-10"
        name = text(self.name)
        return "\n".join([
            "#1 = APPLICATION_PROTOCOL_DEFINITION('international standard','automotive_design',2000,#2);",
            "#2 = APPLICATION_CONTEXT('core data for automotive mechanical design processes');",
            "#3 = SHAPE_DEFINITION_REPRESENTATION(#4,#10);",
            "#4 = PRODUCT_DEFINITION_SHAPE('','',#5);",
            "#5 = PRODUCT_DEFINITION('design','',#6,#9);",
            "#6 = PRODUCT_DEFINITION_FORMATION('','',#7);",
            f"#7 = PRODUCT({name},{name},'',(#8));",
            "#8 = PRODUCT_CONTEXT('',#2,'mechanical');",
            "#9 = PRODUCT_DEFINITION_CONTEXT('part definition',#2,'design');",
            f"#10 = SHAPE_REPRESENTATION('',{refs([ORIGIN] + self.placements)},#19);",
            "#11 = AXIS2_PLACEMENT_3D('',#12,#13,#14);",
            "#12 = CARTESIAN_POINT('',(0.,0.,0.));",
            "#13 = DIRECTION('',(0.,0.,1.));",
            "#14 = DIRECTION('',(1.,0.,0.));",
            "#15 = CARTESIAN_POINT('',(0.,0.,0.));",
            "#16 = DIRECTION('',(0.,0.,1.));",
            "#17 = DIRECTION('',(1.,0.,0.));",
            "#18 = AXIS2_PLACEMENT_3D('',#15,#16,#17);",
            ("#19 = ( GEOMETRIC_REPRESENTATION_CONTEXT(3) GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT((#23)) "
             "GLOBAL_UNIT_ASSIGNED_CONTEXT((#20,#21,#22)) REPRESENTATION_CONTEXT('Context #1','3D Context with UNIT and UNCERTAINTY') );"),
            f"#20 = ( LENGTH_UNIT() NAMED_UNIT(*) {unit} );",
            "#21 = ( NAMED_UNIT(*) PLANE_ANGLE_UNIT() SI_UNIT($,.RADIAN.) );",
            "#22 = ( NAMED_UNIT(*) SI_UNIT($,.STERADIAN.) SOLID_ANGLE_UNIT() );",
            f"#23 = UNCERTAINTY_MEASURE_WITH_UNIT(LENGTH_MEASURE({accuracy}),#20,'distance_accuracy_value','confusion accuracy');",
            "#24 = PRODUCT_RELATED_PRODUCT_CATEGORY('part',$,(#7));",
        ]) + "\n"

    def close(self):
        """Finish the file: the assembly, then the end.  -> its path, or None with no part (the
        file is removed)."""
        if not self.parts:
            self.discard()
            return None
        self.file.write(self.assembly() + "ENDSEC;\nEND-ISO-10303-21;\n")
        self.file.close()
        return self.path

    def discard(self):
        """Close and remove the file: nothing in it, or an error on the way."""
        self.file.close()
        self.path.unlink(missing_ok=True)
