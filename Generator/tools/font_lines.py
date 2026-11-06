"""A stroke font in this project's JSON, rewritten as JSON Lines, the layout KESE reads glyph by glyph
(kese/core/font_file.py): the header on the first line, then one glyph per line from
first_codepoint on.  The glyphs keep their numbers exactly; a .gz output is gzipped with no time
stamp, so the same font always gives the same bytes.

    python tools/font_lines.py my_font.json kese/assets/fonts/my_font.json.gz

KiCad's newstroke (kese/assets/fonts/kicad_newstroke.json.gz) was rewritten so on 6 November 2026.
"""
import gzip
import json
import sys
from pathlib import Path

GENERATOR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GENERATOR))
from kese.core.font_file import read_json  # noqa: E402


def font_lines(font):
    """The font as JSON Lines, in bytes."""
    head = {k: v for k, v in font.items() if k != "glyphs"}
    lines = [json.dumps(head, ensure_ascii=False, separators=(",", ":"))]
    lines += [json.dumps(font["glyphs"][i], separators=(",", ":")) for i in range(len(font["glyphs"]))]
    return ("\n".join(lines) + "\n").encode("utf-8")


def main(src, dst):
    data = font_lines(read_json(src))
    if str(dst).endswith(".gz"):
        data = gzip.compress(data, compresslevel=9, mtime=0)
    Path(dst).write_bytes(data)
    print(f"{dst}: {len(data):,} bytes")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
