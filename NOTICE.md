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

KESE contains material derived from KiCad (<https://www.kicad.org>), a free EDA
application licensed under the GNU General Public License. The original
copyright and license headers of the KiCad source files it comes from are kept,
word for word, in the [`licenses/`](licenses) folder, together with KiCad's
`AUTHORS.txt`, which those headers refer to.

| KESE file | Derived from (KiCad source) | Copyright | License |
|-----------|-----------------------------|-----------|---------|
| `Generator/kese/assets/fonts/kicad_newstroke.json.gz` | `common/newstroke_font.cpp` | Copyright (C) 2010 vladimir uryvaev; Copyright The KiCad Developers, see AUTHORS.txt for contributors | GPL-2.0-or-later. Header: [`licenses/KiCad-newstroke_font.cpp-header.txt`](licenses/KiCad-newstroke_font.cpp-header.txt) |
| CJK glyphs in the same file | `common/newstroke_font.cpp`, CJK portion added in 2019, drawn from Adobe's Source Han Sans | Code copyright (c) 2018 Lingdong Huang; Source Han Sans Copyright 2014-2019 Adobe, with Reserved Font Name 'Source' | MIT-style permission notice, and the SIL Open Font License 1.1 for the font. Both are in the same header file. |
| `Generator/kese/core/font.py`, and the text metrics in `Generator/parameters/silkscreen.py` | `common/font/font.cpp` (`FONT::drawMultilineText`) and `common/font/stroke_font.cpp` (`STROKE_FONT`) | Copyright (C) 2021 Ola Rinta-Koski; Copyright (C) 2012 Torsten Hueter; Copyright (C) 2013 CERN; Copyright The KiCad Developers, see AUTHORS.txt for contributors | GPL-2.0-or-later. Headers: [`licenses/KiCad-font.cpp-header.txt`](licenses/KiCad-font.cpp-header.txt), [`licenses/KiCad-stroke_font.cpp-header.txt`](licenses/KiCad-stroke_font.cpp-header.txt) |

KiCad's list of contributors: [`licenses/KiCad-AUTHORS.txt`](licenses/KiCad-AUTHORS.txt).

The KiCad material is licensed under the GPL version 2 or later, which allows
KESE as a whole to be distributed under version 3 or later. The CJK glyph data
keeps its MIT and SIL Open Font License terms: the font data may not be sold by
itself, and a modified version may not use the reserved name "Source".

The headers were copied from KiCad's master branch on 19 October 2026:
<https://gitlab.com/kicad/code/kicad>.
