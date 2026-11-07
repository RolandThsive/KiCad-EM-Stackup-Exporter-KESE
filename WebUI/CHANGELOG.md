# Changes to the web tool

The newest first. Each entry is one pull request into `WebUI`; the footer's build stamp names the commit that is live.

## Hardening: backup copy, security, privacy, accessibility, tests, tips (November 2026)

**Where Python and three.js come from**
- Still jsDelivr first, pinned to exact versions. If jsDelivr refuses, says nothing for 15 s, or serves a three.js
  file that differs from the build's, the page uses a backup copy on this site (`vendor/`). `build_site.py`
  downloads it and checks every file against the SHA-256 in `vendor.json`; one changed file stops the build.
- The browser checks every three.js file against the import map's `integrity` hash.
- The footer's build stamp says which source served Python and three.js.

**Security**
- Content-Security-Policy:
  - Scripts only from this site, the pinned three.js folder and the two import maps (by hash).
  - No inline script, no `eval`, no plug-ins; `<base>` and forms only to this site.
  - The privacy and licences pages allow even less.
- Referrer policy `strict-origin-when-cross-origin`.
- `?pyodide=` is only taken from this site.
- Size limits, checked before a file is read:
  - boards up to 500 MB;
  - parameter files up to 20 MB;
  - a zip member up to 5 MB unpacked, so a zip bomb is refused.
- Every action in the workflows is pinned to a commit; the web tool's workflows keep no token after checkout.
- Dependabot proposes updates for the actions and the test tools.

**Privacy**
- The fonts are served from this site, so the page makes no request to Google Fonts.
- A privacy page and a licences page (with the licence texts) are linked from the footer.

**When something goes wrong**
- Without WebGL (some Firefox set-ups) the page used to stop at "Loading Python". Now Generate and the downloads work,
  and the preview says why it is off.
- An unexpected error opens a dialog with the details to copy or report. Errors from browser extensions and other
  sites are ignored.
- **Report a Problem** in the footer opens a GitHub issue filled in with the build, the browser and the changed
  settings. The board and its name are never included.

**Accessibility (WCAG 2.2 AA, see docs/WCAG-EM.md)**
- Contrast of the grey text.
- Names for every input, table cell and the 3D canvas.
- Scrollable boxes take the focus.
- Parts rows are 24 px high, and their buttons say whether the part shows.
- One column at 400 % zoom (320 px).
- The layout holds with wider text spacing.
- Tips open on keyboard focus, close with Escape, and the pointer can move onto them.
- Status messages reach screen readers.

**Tips**
- Every tip has one layout: a title, one plain line, then only what helps: the choices, a few facts, a note, a picture.
- The words are in `tips.json`, no longer the parameter files' comments. A setting it does not have still shows its
  comment, so a new parameter is never without a tip.
- A setting's tip shows its unit, its choices with the file's value marked, the file's value, and a link to its
  section of the Parameter Reference. A desktop-only setting says so.
- The 46 settings that showed the comment of the setting above them now have their own words.
- A preset's tip says what it is for and lists what it sets. A section's tip says what is inside and how many settings
  Basic shows.
- 34 pictures in the tips (`docs/tooltipsPictures`, about 12 KB each), each loaded only when its tip opens.
  `build_site.py` copies them to `tooltips/` and stops if one is missing.
  - 15 are one panel cut from a wiki picture.
  - 19 are drawn for the tip, where the wiki picture's labels or colours were too small to read at tip size, each
    showing the setting's choices side by side where it has them: the silkscreen and mask colours, the stack-up,
    Etch Factor, Orientation, Origin, the two modes, Copper and Dielectric Grouping, Outer Plating Added, Via Wall,
    Castellation, Edge Plating and its net, Finish Enabled, Silk Thickness, Interline Pitch, Text Stroke Quad Segs
    and Outline Line Snap. Their SVG sources are in `drawn/`.
- Long board and file names wrap inside a tip instead of sticking out of it.
- Finish Type's layer table says what its rows are: the finish's layers, bottom to top, in mm.

**Tests and documents**
- Browser tests in Chromium, Firefox and WebKit on every pull request (`tests/`):
  - every feature board;
  - 13 window sizes and the blog's frame;
  - keyboard, wrong and oversized files;
  - the CDN refused, silent or tampered;
  - the CSP;
  - accessibility scans, screenshots;
  - every setting and button has its tip in `tips.json`, with its picture, and every tip falls back to plain words without it;
  - speed budgets and Lighthouse.
- After each deploy, a smoke test makes a board on the published page.
- New documents:
  - `README.md`: supported browsers, how the page is put together, releasing and rolling back.
  - `docs/ASVS-L1.md`: the OWASP ASVS level 1 checklist.
  - `docs/WCAG-EM.md`: the accessibility review.
  - `tests/README.md`: how to run the tests.
