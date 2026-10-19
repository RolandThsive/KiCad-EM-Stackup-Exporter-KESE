# Copyright and license notices

KiCad EM Stackup Exporter (KESE)
Copyright (C) 2026 RolandThsive

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>. The full text is in
[LICENSE](LICENSE).

## Work derived from KiCad

KESE contains material derived from KiCad (<https://www.kicad.org>), which is
licensed under the GNU General Public License. Its copyright notices are kept
here, and these parts are distributed under the GPL like the rest of KESE.

| KESE file | Derived from | Copyright | License |
|-----------|--------------|-----------|---------|
| `Parameters/Fonts/kicad_newstroke.json.gz` | KiCad `common/newstroke_font.cpp` (the "newstroke" stroke font) | Copyright (C) 2010 Vladimir Uryvaev; CJK glyphs copyright (c) 2018 Lingdong Huang; Copyright (C) The KiCad Developers | GPL-2.0-or-later; CJK glyphs under an MIT-style notice. See [`Parameters/Fonts/LICENSE_fonts.txt`](Parameters/Fonts/LICENSE_fonts.txt). |
| `Generator/Geometry/Text.py`, and the text metrics in `Parameters/Silkscreen_Parameters.py` | KiCad's stroke-font text layout (`STROKE_FONT`, `FONT::drawMultilineText`) | Copyright (C) The KiCad Developers | GPL-3.0-or-later |

KiCad's full license and the list of its contributors are in the KiCad source
code: <https://gitlab.com/kicad/code/kicad>.
