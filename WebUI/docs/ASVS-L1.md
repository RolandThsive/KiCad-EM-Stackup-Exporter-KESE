# OWASP ASVS 5.0 level 1: the web tool

Checked against the [OWASP Application Security Verification Standard 5.0.0](https://github.com/OWASP/ASVS/tree/v5.0.0/5.0/en)
(May 2025), level 1, on the WebUI branch. Last review: November 2026.

**What the tool is, for this checklist:** a static site on GitHub Pages. No server code, no accounts, no cookies, no
database, no API of its own. The visitor's board is read and processed in their own browser (Python in a Web Worker)
and never sent anywhere. So most of ASVS (authentication, sessions, authorisation, tokens, OAuth, server APIs, WebRTC:
chapters V4, V6 to V10, V17) has nothing to apply to. The chapters that do apply are below, requirement by requirement.

Status: **Met**, **N/A** (nothing in the tool it could apply to, with the reason), or **Host** (decided by GitHub
Pages, not by the project).

## V1 Encoding and Sanitization

| # | Requirement (short) | Status | How |
|---|---|---|---|
| 1.2.1 | Output encoding for the context | Met | All text from boards, files and Python goes into the page with `textContent`, `createTextNode` or `replaceChildren` (`el()` in WebUI.js); there is no `innerHTML`. |
| 1.2.2 | URLs built safely, only safe protocols | Met | The one URL built from data (Report a Problem) encodes it with `encodeURIComponent`; links come from `webui.json`. `?board=` only takes the name of a bundled example. `?pyodide=` only a folder of the same site. |
| 1.2.3 | Encoding when building JavaScript or JSON | Met | Messages to and from the worker are structured-clone objects or `JSON.stringify`; no script text is built. |
| 1.2.4 | Parameterised database queries | N/A | No database. |
| 1.2.5 | OS command injection | N/A | No OS commands (the browser sandbox). |
| 1.3.1 | Sanitise HTML from editors | N/A | No HTML input. |
| 1.3.2 | No `eval` or dynamic code execution | Met | No `eval`/`new Function` in the page; the CSP forbids `unsafe-eval` and inline script. Imported parameter files are read with Python's `ast.literal_eval`, never executed. Python itself runs only the generator's own code. |
| 1.5.1 | Safe XML parsing | N/A | No XML is parsed. |

## V2 Validation and Business Logic

| # | Requirement (short) | Status | How |
|---|---|---|---|
| 2.1.1 | Validation rules documented | Met | Each parameter's type, range and choices come from `Generator/parameters/*.py` (shown as the field's help); KESE checks them again before a run and stops with an error. |
| 2.2.1 | Input validated against expectations | Met | Boards must be `.kicad_pcb` starting with `(kicad_pcb`; numbers are parsed and refused when not numbers; choices only from their list; the generator validates every value. |
| 2.2.2 | Validation at a trusted layer | Met | There is no server: the visitor's own browser is the only layer, and nothing is trusted beyond it. |
| 2.3.1 | Steps in order | Met | Generate is disabled until Python is ready and a board is loaded; downloads are disabled while the settings differ from the run's. |

## V3 Web Frontend Security

| # | Requirement (short) | Status | How |
|---|---|---|---|
| 3.2.1 | Content not rendered in the wrong context | Met / Host | GitHub Pages serves each file with its type; user files are never served (they stay in the browser). |
| 3.2.2 | Text rendered as text | Met | See 1.2.1. |
| 3.3.1 | Cookies `Secure` | N/A | No cookies. |
| 3.4.1 | HSTS | Host | github.io sends HSTS and is on the browsers' HSTS preload list; the project cannot set headers on Pages. |
| 3.4.2 | CORS allow-origin fixed | Host | Pages answers `Access-Control-Allow-Origin: *` for static files; there is nothing private to read. |
| 3.5.1 to 3.5.3 | Cross-site requests to sensitive functions | N/A | No server-side functions. |

Above level 1, also done: **3.4.3** a Content-Security-Policy (in a meta tag, since Pages sets no headers;
`default-src 'self'`, scripts only from this site, the pinned three.js folder and the two import maps by SHA-256,
`object-src 'none'`, `base-uri 'self'`); **3.4.5** a referrer policy (`strict-origin-when-cross-origin`);
**3.6.1** subresource integrity for the CDN files (import-map `integrity` for every three.js file, Pyodide's lock-file
hashes for its packages, and the build checks the backup copy against `vendor.json`); **3.7.5** documented behaviour
when a browser lacks a feature (README: supported browsers). Not possible on Pages: 3.4.4 (`nosniff` header),
3.4.6 (`frame-ancestors` needs a header; the blog frames the page on purpose), 3.4.8 (COOP header).

Known gap: Pyodide's own runtime files (`pyodide.mjs`, `pyodide.asm.wasm`, the standard library) are loaded inside the
worker, where import maps do not apply, so the browser does not hash-check them. They come from a version-pinned
jsDelivr path; if jsDelivr fails, from the backup copy that was hash-checked at build time.

## V5 File Handling

| # | Requirement (short) | Status | How |
|---|---|---|---|
| 5.2.1 | Only files of a size it can process | Met | Boards over 500 MB and parameter files over 20 MB are refused before they are read; a zip member over 5 MB unpacked is refused (zip bombs). |
| 5.2.2 | Extension and content checked | Met | Boards: `.kicad_pcb` and must start with `(kicad_pcb`. Imports: `.txt`, `.py`, `.zip`; in a zip only `parameters/*.py` and `parameters.txt` are read, as text, with `ast.literal_eval`. |
| 5.3.1 | Uploaded files not executed on the server | N/A | Nothing is uploaded. |
| 5.3.2 | File paths from trusted data | Met | The worker writes the board to a fixed folder of its in-memory file system under its own name; zip member paths are only used to pick files to read, never to write. |

## V12 Secure Communication

| # | Requirement (short) | Status | How |
|---|---|---|---|
| 12.1.1 | Current TLS only | Host | GitHub Pages and jsDelivr (TLS 1.2 and 1.3). |
| 12.2.1 | TLS everywhere, no fallback | Met / Host | Pages enforces HTTPS; every URL the page uses is relative or `https://`. |
| 12.2.2 | Publicly trusted certificates | Host | GitHub's and jsDelivr's. |

## V13 Configuration

| # | Requirement (short) | Status | How |
|---|---|---|---|
| 13.4.1 | No source-control metadata deployed | Met | `build_site.py` copies the page files only; dotfiles, tests, tools, docs and `vendor.json` are not published. |

## V14 Data Protection

| # | Requirement (short) | Status | How |
|---|---|---|---|
| 14.2.1 | No sensitive data in URLs | Met | Nothing sensitive is sent anywhere. Report a Problem puts the build, browser and changed settings in a GitHub link, never the board or its name, and the visitor sees it before sending. |
| 14.3.1 | Client data cleared at the end | Met | The run's files (OPFS) are deleted when the tab closes or reloads, and leftovers of a crashed browser on the next visit. The only other storage is one `sessionStorage` flag. See `privacy.html`. |

## V15 Secure Coding and Architecture

| # | Requirement (short) | Status | How |
|---|---|---|---|
| 15.1.1 | Update and remediation time frames documented | Met | Below: "Third-party components". |
| 15.2.1 | Components within those time frames | Met | Pyodide 314.0.7, three.js 0.183.2 and the test tools are current releases (November 2026). |
| 15.3.1 | Only the needed fields returned | N/A | No API. |

### Third-party components

The page loads Pyodide (with NumPy and Shapely) and three.js, pinned in `webui.json` and `vendor.json`; the fonts and
earcut are part of the site. Licences: `licenses.html`.

- **A security fix** in one of them (a GitHub security advisory, a CVE, a release note): update within **14 days**
  (change `webui.json`, run `tools/vendor_lock.py`, open a pull request; the tests show whether anything broke).
- **Otherwise**: look for new releases **every 3 months** and update when the tests pass.
- **The workflows' actions and the test tools**: Dependabot proposes updates monthly (once `.github/dependabot.yml` is
  on the default branch); merge them within a month.

## V16 Security Logging and Error Handling

Level 1 has no requirement in this chapter that applies to a page without a server (logging is a server's job). Above
level 1, also done: **16.5.1** a generic message for unexpected errors (the crash dialog; the details are the page's
own, no secrets exist); **16.5.2** graceful degradation when an external resource fails (the backup copy after 15 s,
the page without WebGL); **16.5.4** a last-resort handler for uncaught errors and rejections (`catchCrashes` in
WebUI.js).

## How this is tested

`WebUI/tests/specs/security.spec.mjs` (every pull request, three browsers): the CSP blocks an injected inline script;
the page contacts no server but its own and jsDelivr; `?pyodide=` from another site is ignored; jsDelivr refused,
silent (15 s) or serving a changed three.js; the crash dialog; Report a Problem never contains the board.
`inputs.spec.mjs`: wrong files, a broken board, broken and oversized parameter files, a zip bomb.
