# Accessibility review of the web tool (WCAG-EM)

Reviewed with the [W3C WCAG-EM 1.0 method](https://www.w3.org/TR/WCAG-EM/) against
[WCAG 2.2](https://www.w3.org/TR/WCAG22/) level AA (the level the EU's EN 301 549 asks for), on the WebUI_modifs branch.
Last review: November 2026.

## 1. Scope

- **The pages:** the tool (`index.html`) on its own and inside the blog's frame, `privacy.html`, `licenses.html`.
- **Target:** WCAG 2.2 level AA.
- **Browsers and devices:** computers with a mouse or trackpad, in the latest Chrome, Edge and Firefox on Windows
  and Linux, and the latest Safari and Chrome on macOS (README: supported browsers). A phone or tablet gets a short
  page that says the tool needs a computer, and that page is checked too.
- **Left out:** the files the tool makes (GLB, STEP, STL, OBJ). They are for CAD and simulation programs, not for
  reading.

## 2. What the tool is (exploring it)

It is one page that changes state as you use it: starting, Python ready, a board chosen, a model made, Basic or
Advanced, Simulation or Visual mode, sections and colour groups open, the menus, three dialogs (Reset, report, crash),
the preview full screen. There is a 3D preview on a canvas. It has no forms that send anything, no accounts and no
time limits.

## 3. The sample

Every state in section 2 is in the sample. The tests open each one: `a11y.spec.mjs` (scans), `keyboard.spec.mjs`
(keyboard), `layout.spec.mjs` (13 window sizes and the blog's frame).

## 4. How it was checked

- **Automatic, on every pull request:** axe-core 4.14 with the WCAG 2.0, 2.1 and 2.2 A and AA rules, in each state
  (`a11y.spec.mjs`, Chromium), and Lighthouse's accessibility score (at least 0.95, `lighthouserc.json`). axe finds
  only part of the problems, so the rest was checked by hand, and what could be measured became a test.
- **By hand, in this review, then turned into tests:**
  - zoom at 200, 300 and 400 % (down to 320 CSS px wide);
  - wider letter, word, line and paragraph spacing;
  - every Tab stop, in Chromium and Firefox;
  - the tips;
  - the status messages;
  - each control's name, read from the accessibility tree.
- **Not done yet:** a run with a real screen reader (NVDA or JAWS on Windows, VoiceOver on macOS). That needs a person
  at the computer. The names, roles and status regions it depends on are checked by the tests.

## 5. Results

**Met** means it was checked and works. **N/A** means the page has nothing the rule applies to. **Limit** means it
partly works, with the reason given.

| WCAG 2.2 | Status | How it is met, and how it is checked |
|---|---|---|
| 1.1.1 Non-text content | Met | Icon buttons have names (Fullscreen, Fit, Screenshot, Back, Home); the logo has alt text. The 3D canvas is `role="img"` with a name that points to the readout and the Parts list, which describe the model in text. axe. |
| 1.2.x Audio and video | N/A | None. |
| 1.3.1 Info and relationships | Met | Headings, `header`/`main`/`aside`, label text tied to its input (`aria-labelledby`), each table cell named ("layer 2, mm"). axe. |
| 1.3.2 Meaningful sequence | Met | The reading order is the visual order: controls, preview, checks. |
| 1.3.3 Sensory characteristics | Met | No instruction depends on shape, colour or position alone. |
| 1.3.4 Orientation | Met | Works in landscape and portrait (layout.spec, portrait sizes). |
| 1.3.5 Input purpose | N/A | No fields about the visitor. |
| 1.4.1 Use of colour | Met | Warnings and errors have words and counts as well as colour; a hidden part is struck through as well as faded, and a screen reader hears its button as pressed while the part shows. |
| 1.4.3 Contrast (minimum) | Met | axe in every state. The fade-in of enabled buttons is waited for. `--text-3` was darkened to #6b6b6b for this. |
| 1.4.4 Resize text | Met | Browser zoom to 200 % keeps everything. a11y.spec "reflow". |
| 1.4.5 Images of text | Met | The title is text in a web font. |
| 1.4.10 Reflow | Met | At 320 CSS px wide (400 % zoom) the page becomes one column: preview, controls, side. Nothing scrolls sideways or is cut off; long file and part names end in "…" and show in full in a tip. The 3D preview itself needs two dimensions (an exception the rule allows). a11y.spec "reflow". |
| 1.4.11 Non-text contrast | Met | Focus rings, switch tracks and field borders are visible against their background. axe and by eye. |
| 1.4.12 Text spacing | Met | With line height 1.5, letter spacing 0.12 em, word spacing 0.16 em and 2 em after paragraphs, nothing is cut off at 1440 or 1024 px. The top bar wraps when it must. a11y.spec "text spacing". |
| 1.4.13 Content on hover or focus | Met | Tips come with the keyboard focus as well as the pointer. Escape closes them. The pointer can move onto a tip (300 ms grace on the way), and a tip stays until the pointer or focus leaves. keyboard.spec "tips". |
| 2.1.1 Keyboard | Met / Limit | Every control works by keyboard: menus (arrows, Enter, Escape), switches, steppers, dialogs, Ctrl+Enter to generate. Turning the 3D model by drag has keyboard buttons instead (Top, Bottom, 3D View, Fit, the cross-section slider). Free turning by keys is not offered. keyboard.spec. |
| 2.1.2 No keyboard trap | Met | Dialogs close with Escape and give the focus back. keyboard.spec. |
| 2.1.4 Character key shortcuts | Met | The only shortcut is Ctrl+Enter. |
| 2.2.1 Timing adjustable, 2.2.2 Pause | Met | No time limits. The progress bar and spinner only show work in progress, and stop for visitors who ask for reduced motion. |
| 2.3.1 Three flashes | Met | Nothing flashes. |
| 2.4.1 Bypass blocks | Met | Few controls come before the main content; landmarks `header`, `main`, `aside`. |
| 2.4.2 Page titled | Met | Each page has its own title. |
| 2.4.3 Focus order | Met | Follows the layout. keyboard.spec walks every Tab stop. |
| 2.4.4 Link purpose | Met | Link texts say where they go (Privacy, Licences, Report a Problem, Help / Wiki). |
| 2.4.5 Multiple ways | N/A | A single page (plus two linked from every footer). |
| 2.4.6 Headings and labels | Met | Each panel has a heading; labels are the parameter names in words. |
| 2.4.7 Focus visible | Met | A ring on every Tab stop: on the track of a switch, round the whole stepper of a number. keyboard.spec checks every stop. |
| 2.4.11 Focus not obscured | Met | Nothing sticky covers the focus. Tips open beside their control, never over it. |
| 2.5.1 Pointer gestures | Met | Turning and zooming the model also have single-click buttons. |
| 2.5.2 Pointer cancellation | Met | Buttons act on click (the up event). |
| 2.5.3 Label in name | Met | Visible text is the start of each name. |
| 2.5.4 Motion actuation | N/A | None. |
| 2.5.7 Dragging movements | Met | Dropping a board has the click-to-choose box. Dragging the model has the view buttons. The slider moves by click and keys. |
| 2.5.8 Target size | Met | At least 24 × 24 px (the Parts rows were raised to 24 px for this). axe `target-size`. |
| 3.1.1 Language of page | Met | `lang="en"` on every page. |
| 3.2.1 On focus, 3.2.2 On input | Met | Focus never starts anything. Choosing a board starts a run, which the drop box says ("Choose a board, then press Generate" before; the run's note after). |
| 3.2.3 Consistent navigation, 3.2.4 Consistent identification, 3.2.6 Consistent help | Met | The same top bar and footer on every state. Help / Wiki and Report a Problem are always in the same place. |
| 3.3.1 Error identification | Met | A refused file or value is named in words ("That is not a .kicad_pcb file", "board.kicad_pcb is 600 MB: boards up to 500 MB fit in the browser"). The run's problems are listed under Checks. inputs.spec. |
| 3.3.2 Labels or instructions | Met | Every setting has a label and a tip with its notes, range and file value. |
| 3.3.3 Error suggestion | Met | The generator's messages say which setting and what it accepts. |
| 3.3.4 Error prevention | Met | Reset asks first; nothing is sent or deleted. |
| 3.3.7 Redundant entry, 3.3.8 Accessible authentication | N/A | No multi-step process, no sign-in. |
| 4.1.2 Name, role, value | Met | Tabs, switches, menus and dialogs have their roles and states. axe. |
| 4.1.3 Status messages | Met | The run's note, the Checks counts, "Settings changed" and every short notice are status regions. A notice that appears and fades is repeated in a hidden status region, so a screen reader reads it. a11y.spec "status messages". |

## 6. Known limits

- **The 3D preview** is a picture on a canvas. Its contents are described in text by the readout (size, parts,
  triangles, board size) and by the Parts list, where each part can be hidden or shown by keyboard. Turning the
  model freely needs a mouse; the view buttons cover the fixed views.
- **Parameter notes for screen readers:** a setting's notes are in its tip, which now opens on focus. The tip is not
  yet tied to the field with `aria-describedby`, so a screen reader reads it only when asked to read the tip.
- **No screen reader run yet** (section 4). Do one before calling the tool fully checked.

## 7. Fixed in this review

- The grey text colour was too light (contrast); `--text-3` is now #6b6b6b.
- The report text and the checks list scroll, and now take the focus so they can be scrolled by keys.
- Parts rows are 24 px high (target size).
- Unlabelled inputs and table cells got names.
- One column at 320 px wide (reflow).
- The top bar wraps with wider text spacing.
- Generate no longer shrinks to "Gene…".
- The readout wraps.
- Tips on keyboard focus, closed by Escape, and reachable by the pointer.
- Status regions for messages.
- A name for the 3D canvas.
- Each part's button says whether the part shows, and a hidden part is struck through.
