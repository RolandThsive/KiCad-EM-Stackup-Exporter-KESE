"""Boards 19 and 19b: board items that are not tracks, pads, zones or plain drawings, several of them
on copper, where a fab plots them as copper too: dimensions, targets, a group, a 3D model, a
picture and text boxes in KiCad 7's format, and a table, barcodes, points and a reference image in
KiCad 10's."""
import base64
import re
import struct
import zlib

from common import X0, Y0, at, new_board
from footprints7 import footprint, pad, text
from kicad7 import effects, gr_rect, gr_text, gr_text_box, q, segment, xy
from kicad_later import K10, Board, effects as effects_later, outline

SMD = ("F.Cu", "F.Paste", "F.Mask")


def png(size=16, square=4):
    """A small black and white chequerboard as a PNG file."""
    rows = b"".join(b"\0" + bytes(255 * ((x // square + y // square) % 2) for x in range(size)) for y in range(size))
    chunk = lambda kind, data: (struct.pack(">I", len(data)) + kind + data
                                + struct.pack(">I", zlib.crc32(kind + data)))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 0, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))


def base64_lines():
    data = base64.b64encode(png()).decode()
    return [data[i:i + 76] for i in range(0, len(data), 76)]


def uuid_of(item):
    return re.findall(r"\(tstamp ([0-9a-f-]{36})\)", item)[-1]


def dimension(b, kind, layer, a, c, geo="", label=None, style=""):
    """A KiCad 7 dimension from a to c.  KiCad works out its text and arrows again when it reads the
    board, except for a leader's label, which stands at c."""
    s = f"(dimension (type {kind}) (layer {q(layer)}) {b.ts()} (pts (xy {xy(a)}) (xy {xy(c)})) {geo}"
    if kind != "center":
        s += f" (gr_text {q(label or '')} (at {xy(c if label else a)}) (layer {q(layer)}) {b.ts()} {effects()})"
        units = f"(units 0) (units_format 0) (precision 4) (override_value {q(label)})" if label else \
            "(units 3) (units_format 1) (precision 4)"
        s += f' (format (prefix "") (suffix "") {units})'
    return s + (f" (style (thickness 0.1) (arrow_length 1.27) (text_position_mode 0) {style}"
                f"(extension_offset 0.5) keep_text_aligned))")


def skipped_items():
    """Dimensions (aligned on F.Cu, orthogonal, leader, center and radial on silk), targets on F.Cu
    and silk, a group of a copper rectangle, a track and silk text, a footprint with a 3D model, a
    picture on silk, and text boxes on F.Cu and on silk."""
    b = new_board("skipped_items", 2, (40, 30))
    ext = "(extension_height 0.58642) "
    b.add(dimension(b, "aligned", "F.Cu", at(3, 6), at(19, 6), "(height -2)", style=ext),
          dimension(b, "center", "F.SilkS", at(25, 5), at(26, 5)),
          dimension(b, "radial", "F.SilkS", at(31, 4), at(32.5, 5.5), "(leader_length 2)"),
          dimension(b, "orthogonal", "F.SilkS", at(3, 10), at(13, 13), "(height 2) (orientation 0)", style=ext),
          dimension(b, "leader", "F.SilkS", at(20, 13), at(24, 10), label="LEADER", style="(text_frame 0) "))
    b.add(f'(target plus (at {xy(at(5, 17))}) (size 4) (width 0.15) (layer "F.Cu") {b.ts()})',
          f'(target x (at {xy(at(11, 17))}) (size 3) (width 0.15) (layer "F.SilkS") {b.ts()})')
    members = [gr_rect(b, at(15, 15), at(19, 19), "F.Cu", 0.1, True),
               segment(b, at(20, 17), at(25, 17), 0.4, "F.Cu", "GROUPED"),
               gr_text(b, "GROUP", at(20, 20), "F.SilkS", size=1, thickness=0.15)]
    b.add(*members, f'(group "GROUPED" (id {uuid_of(b.ts())}) (members {" ".join(uuid_of(m) for m in members)}))')
    b.add(footprint(b, "Feature:Model", at(32, 17), model="${KICAD7_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_0805_2012Metric.wrl",
                    children=[text("reference", "R1", (0, -1.8), "F.SilkS"),
                              pad("1", "smd", "rect", (-1, 0), (1.0, 1.3), SMD, net="M1"),
                              pad("2", "smd", "rect", (1, 0), (1.0, 1.3), SMD, net="M2")]))
    data = " ".join(base64_lines())
    b.add(f'(image (at {xy(at(5, 25))}) (layer "F.SilkS") (scale 4) (data {data}))')
    b.add(gr_text_box(b, "COPPER BOX", at(12, 23), at(24, 27), "F.Cu", 0.2, size=1, thickness=0.2),
          gr_text_box(b, "SILK BOX", at(26, 23), at(37, 27), "F.SilkS", 0.15, size=1, thickness=0.15))
    return b


def skipped_items_k10():
    """KiCad 10's table (on F.Cu), QR codes on silk and on F.Cu, points on F.Cu and on a user
    layer, and a reference image."""
    b = Board("skipped_items_k10", K10)
    b.add(outline(b, X0, Y0, X0 + 40, Y0 + 24))
    stroke = "(stroke (width 0.1) (type solid))"
    widths, heights, cells = (10, 8), (3, 3), (("NET", "WIDTH"), ("SIG", "0.3"))
    s = (f'(table (column_count 2) {b.ts()} (layer "F.Cu") (border (external yes) (header yes) {stroke}) '
         f"(separators (rows yes) (cols yes) {stroke}) (column_widths {' '.join(map(str, widths))}) "
         f"(row_heights {' '.join(map(str, heights))}) (cells")
    y = Y0 + 3
    for r, h in enumerate(heights):
        x = X0 + 3
        for c, w in enumerate(widths):
            s += (f" (table_cell {q(cells[r][c])} (start {xy((x, y))}) (end {xy((x + w, y + h))}) "
                  f'(margins 0.5 0.5 0.5 0.5) (span 1 1) (layer "F.Cu") {b.ts()} '
                  f"{effects_later(b, 1, 0.15, justify=('left', 'top'))})")
            x += w
        y += h
    b.add(s + "))")
    for p, layer, shown in ((at(27, 6), "F.SilkS", True), (at(35, 6), "F.Cu", False)):
        b.add(f'(barcode (at {xy(p)} 0) (layer {q(layer)}) (size 6 6) (text "KESE") (text_height 1) (type qr) '
              f'(ecc_level M) (hide {"no" if shown else "yes"}) (knockout no) {b.ts()})')
    b.add(f'(point (at {xy(at(5, 16))}) (size 1) (layer "F.Cu") {b.ts()})',
          f'(point (at {xy(at(10, 16))}) (size 1) (layer "Dwgs.User") {b.ts()})')
    data = " ".join(q(line) for line in base64_lines())
    b.add(f'(image (at {xy(at(20, 17))}) (layer "F.SilkS") (scale 4) (data {data}) {b.ts()})')
    return b


BOARDS = [skipped_items, skipped_items_k10]
