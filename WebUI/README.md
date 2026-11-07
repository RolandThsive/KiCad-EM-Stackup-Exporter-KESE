# The KESE web tool (WebUI/)

The KiCad EM Stackup Exporter in a browser: the page at
<https://rolandthsive.github.io/KiCad-EM-Stackup-Exporter-KESE/WebUI/>, also shown inside the blog
(`BloggerPage.html`). It runs the real generator (`Generator/kese`, `Generator/parameters`) in Python compiled to
WebAssembly (Pyodide), in a Web Worker, so the visitor's board never leaves their computer.

Branches: `WebUI` is what GitHub Pages publishes (a push deploys it); work happens on `WebUI_modifs` and reaches
`WebUI` by pull request; `WebUI_LocalTesting` is `WebUI_modifs` plus `LocalTesting/serve.py`.

## Supported browsers

The tool is for computers (a phone or tablet gets a short message instead). Supported: the current and the previous
major version of **Chrome, Edge and Firefox** on Windows, macOS and Linux, and of **Safari** on macOS. Every pull
request is tested in Chromium, Firefox and WebKit (the engine of Safari); see [tests/README.md](tests/README.md).
Window sizes from 1024 × 768 up, landscape or portrait, and browser zoom up to 400 % (docs/WCAG-EM.md).

What the page needs, and what happens without it:

| Feature | Needed for | Without it |
|---|---|---|
| WebAssembly, module Web Workers, import maps | Python and the page itself | the page cannot start (every supported browser has them) |
| WebGL 2 | the 3D preview | the preview, its tools and the parts list are off with a note; Generate and the downloads still work |
| Origin Private File System | keeping a big run on disk instead of in memory | the run's files stay in memory |
| Import-map `integrity` | refusing a three.js file that differs from the build's | older browsers ignore it; the page still works |
| `sessionStorage` | remembering the backup copy for the tab | a `?threeBackup=1` in the address does the same |

## How the page is put together

| File | Role |
|---|---|
| `index.html` | the page; its Content-Security-Policy is written by `build_site.py` |
| `boot.js` | starts the page: phone check, settings, chooses jsDelivr or the backup copy for three.js, adds the import map |
| `WebUI.js` | the page's logic: settings, Generate, preview, checks, downloads, footer, Report a Problem, crash dialog |
| `PyodideWorker.js`, `WebGenerator.py` | the worker that runs KESE in Python, and its Python side |
| `Viewer.js`, `Section*.js`, `Step*.js` | the 3D preview (three.js), the cross-section, the STEP reader |
| `OutputStore.js` | the run's files on the visitor's disk (OPFS), deleted when the tab closes |
| `webui.json` | the page's own settings (which parameters Basic shows, CDN addresses, the 15 s wait) |
| `vendor.json` | the exact Pyodide and three.js files of the backup copy, with their SHA-256 (`tools/vendor_lock.py`) |
| `privacy.html`, `licenses.html`, `licenses/` | the privacy note and the third-party licences, linked from the footer |
| `fonts/` | the three fonts, served from the site (no Google request) |
| `build_site.py` | builds the site folder GitHub Pages serves |
| `tests/` | the browser tests, accessibility scans and Lighthouse budgets |
| `docs/` | the security checklist (OWASP ASVS level 1) and the accessibility review (WCAG-EM) |

## Where Python and three.js come from

From **jsDelivr**, pinned to exact versions (`webui.json`). If jsDelivr does not answer within **15 s**
(`cdnWaitSeconds`), refuses, or serves a three.js file that differs from the build's, the page uses the **backup
copy** on GitHub Pages (`WebUI/vendor/`), which `build_site.py` downloads at build time and checks file by file against
`vendor.json`. A file that differs stops the build. To move to a new Pyodide or three.js: change `webui.json`, run
`python WebUI/tools/vendor_lock.py`, and commit both.

## Security

- A strict Content-Security-Policy (scripts only from this site, the pinned three.js folder and the two import maps by
  hash; no inline script, no `eval`, no plug-ins); the privacy and licences pages allow even less.
- `?pyodide=` (local testing) is taken only from this site.
- Every action in the workflows is pinned to a commit; Dependabot proposes updates (`.github/dependabot.yml`).
- Boards over 500 MB and parameter files over 20 MB (or a zip member over 5 MB unpacked) are refused before they are
  read.
- The checklist against OWASP ASVS 5.0 level 1: [docs/ASVS-L1.md](docs/ASVS-L1.md).

## Releasing and rolling back

1. Work on `WebUI_modifs`; open (or update) the pull request into `WebUI`. The **Web UI Tests** workflow runs the
   generator's tests, builds the site, runs the browser tests in three browsers and Lighthouse. Its artifact `site` is
   the exact site the pull request would publish.
2. Merge when the checks are green. **Web UI On GitHub Pages** builds and deploys, then its `smoke` job opens the
   published page and makes a board. The footer names the commit (`build abc1234`).
3. Note the change in [CHANGELOG.md](CHANGELOG.md).

**Rolling back** a bad deploy, fastest first:
- Actions > "Web UI On GitHub Pages" > the last good run > **Re-run all jobs**. A re-run builds that run's commit
  again (same branch, so the `github-pages` environment allows it) and deploys it. Nothing changes in git.
- Then fix it properly: open the merged pull request on GitHub, press **Revert**, and merge the revert pull request into
  `WebUI` (or push the fix through `WebUI_modifs` as usual). The next deploy replaces the re-run.
- Either way, check the footer's build stamp on the live page: it names the commit that is live.

## Reporting a problem

The footer's **Report a Problem** opens a GitHub issue filled in with the build, browser, window size and the settings
that differ from the defaults; never the board. An unexpected error opens a dialog with the same details.
