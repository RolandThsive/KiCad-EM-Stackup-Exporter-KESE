# Local Testing

This branch (`WebUI_LocalTesting`) is how the web tool is tried out on a desktop before it goes live.
It always holds the latest web tool work (`WebUI_modifs`) plus this folder.

## Try it

1. Download or clone this branch.
2. Windows: double-click `LocalTesting/Start-Windows.bat`.
   Mac / Linux: run `LocalTesting/Start-Mac-Linux.command` (double-click, or in a terminal).
3. A small local web server starts (needs Python 3, nothing to install) and the page opens in your browser at
   `http://localhost:8000/WebUI/`. If port 8000 is busy it uses the next free one; the window shows the address.
4. The first start downloads Python for the browser (Pyodide, about 30 MB with numpy and shapely) and three.js from
   the internet; later starts are cached.

Caching is switched off in the test server, and every reload of the page builds the site again, so the browser
always shows the files of this branch: edit `WebUI/` or `Generator/`, then reload.

Why a server instead of double-clicking `WebUI/index.html`: browsers block the background Python thread, the
module scripts and the browser storage on `file://` pages, so the page has to come from `http://localhost`.

## How the tester is made

- `serve.py` runs `WebUI/build_site.py`, the same script the GitHub Pages workflow runs, into `LocalTesting/_site`
  (ignored by git), and serves that folder. So the test page is exactly what Pages would publish: `WebUI/`, the
  generator packed into `generator.zip`, `version.json`, the logo and the example boards.
- The Start scripts only run `serve.py`.
- Python for the browser (Pyodide) and three.js come from their CDNs, as on the live site. To test without the
  internet, serve local copies and open the page with `?pyodide=<url of the pyodide folder>/` and
  `?three=<url of the three package>/`.
- `?board=rf_module.kicad_pcb` (or another board of `Generator/Input`) loads that example and generates it at once.

## Keeping it current

1. Pull the working branch into it: `git checkout WebUI_LocalTesting && git merge origin/WebUI_modifs`, then push.
2. Changes to `LocalTesting/` are made on this branch only; they never go into `WebUI` or `main`.

## Checks before a change goes live

- An example board generates in both modes, and the preview shows every format ticked (GLB, OBJ, STL, STEP).
- Download Zip opens, and holds the run's folder.
- Import then Export gives back the same parameter files.
- The page works at 1920, 1600, 1100 and 1080 px wide, and the top bar keeps one line.
