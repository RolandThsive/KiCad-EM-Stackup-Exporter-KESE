# 25. License

KESE is free software, licensed under the **GNU General Public License, version 3 or later**
(SPDX `GPL-3.0-or-later`). The repository's
[`LICENSE`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/main/LICENSE)
and [`NOTICE.md`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/main/NOTICE.md)
files are the authority; this page summarises them.

## 25.1 Why The GPL

KESE includes material derived from KiCad, which is licensed under the GPL:

- the default stroke font, `kese/assets/fonts/kicad_newstroke.json.gz`, converted from KiCad's
  "newstroke" font (GPL v2 or later; its CJK glyphs come from Adobe's Source Han Sans under an
  MIT-style notice and the SIL Open Font License 1.1), and
- the text layout in `kese/core/font.py`, which follows KiCad's stroke-font text code
  (GPL v2 or later).

Work derived from GPL code has to stay under the GPL, with the original copyright notices kept.
KiCad's original copyright headers and its `AUTHORS.txt` are kept word for word in the
repository's `licenses/` folder, listed in `NOTICE.md` and
[`LICENSE_fonts.txt`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/main/Generator/kese/assets/fonts/LICENSE_fonts.txt).

## 25.2 What You May Do

| You May | As Long As |
|---|---|
| Run KESE for any purpose, including commercial work | Nothing; running it needs no permission |
| Study and change the source code | Changed versions you distribute are also GPL-3.0-or-later, with their source |
| Share copies, modified or not | Recipients get the same rights and the full source |

The GPL covers the program. The 3D models KESE writes from your own board are generally not
covered by it, in the same way a document printed by a GPL program is not.

## 25.3 Contributing

Contributions are accepted under the same license, GPL-3.0-or-later; you keep the copyright in
your contribution. If it includes someone else's work, say where it comes from and keep its
notice. See
[`CONTRIBUTING.md`](https://github.com/RolandThsive/KiCad-EM-Stackup-Exporter-KESE/blob/main/CONTRIBUTING.md).

## 25.4 No Warranty

KESE is provided as is, without any warranty; see sections 15 and 16 of the GPL. The models have
not yet been validated against measured boards; see
[Immediate Next Steps](Immediate-Next-Steps.md).

| Previous | Next |
|:---|---:|
| [Future Upgrades And Planning](Future-Upgrades-And-Planning.md) |  |
