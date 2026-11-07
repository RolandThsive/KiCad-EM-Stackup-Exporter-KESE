# The web tool's tests (WebUI/tests)

Browser tests with [Playwright](https://playwright.dev) in Chromium, Firefox and WebKit (the engine of Safari),
accessibility scans with axe-core, and Lighthouse speed and accessibility budgets. They test the **built** site, the
same files GitHub Pages would publish.

## Running them

You need Node 22 and Python 3.12 or later.

```sh
cd WebUI/tests
npm ci                               # the test tools, at the versions in package-lock.json
npx playwright install               # the three browsers (once)
npm run build                        # python3 ../build_site.py .site  (downloads the backup copy, checks vendor.json)
npm test                             # every spec, every browser
npx playwright test --project=chromium specs/security.spec.mjs    # one spec, one browser
npx playwright test -g "jsDelivr silent"                          # tests whose title matches
npm run lighthouse                   # Lighthouse, 3 runs, against the budgets in lighthouserc.json
```

**Without internet**, build from a folder that already holds the backup copy:
`python3 ../build_site.py .site --vendor-from <folder>` (or `KESE_VENDOR_FROM=<folder>`). The folder holds
`pyodide/` and `three/` laid out as on jsDelivr. The files are still checked against `vendor.json`. To download
only once and reuse the files on later builds, add `--vendor-cache <folder>` (or `KESE_VENDOR_CACHE`); a cached file
is used only while it still matches `vendor.json`.

**jsDelivr in the tests.** Every request to jsDelivr is answered from the build's own `vendor/` copy, so the tests give
the same result with or without internet. A test can ask for another behaviour with `test.use({ cdn: "…" })`:

| `cdn` | jsDelivr… |
|---|---|
| `local` (default) | answers with the build's backup copy (the same bytes) |
| `abort` | refuses at once |
| `stall` | never answers (the page must switch after 15 s) |
| `tamper` | serves a `three.module.js` with one extra comment (the import map's `integrity` must refuse it) |
| `abort-pyodide`, `stall-pyodide` | fails for Python only; three.js is served |
| `real` | the real jsDelivr (tests tagged `@network`; CI sets `KESE_NETWORK=1`) |

**Every test fails on an error it did not expect:** a page error, a console error or a CSP violation (the `problems`
fixture in `helpers.mjs`). A test that causes an error on purpose says so with an `allow` annotation.

## The specs

| Spec | Browsers | What it checks |
|---|---|---|
| `smoke` | all | starts, makes the HDI example, offers its files |
| `security` | all | the CSP blocks an injected script; only this site and jsDelivr are contacted; `?pyodide=` from another site is ignored; jsDelivr refused, silent, or serving a changed three.js; only Python's folder failing; the crash dialog; errors from other sites ignored; Report a Problem never names the board |
| `boards` | Chromium | every board in `featureTest/`, one after the other in one page: made, previewed, downloadable, layout intact |
| `layout` | Chromium | 13 window sizes, landscape and portrait, both modes, Basic and Advanced, sections closed and open; the page inside the blog's frame |
| `keyboard` | all | every Tab stop has a visible focus ring (not WebKit, whose Tab skips buttons); menus by keys; dialogs; Ctrl+Enter; tips on focus, closed by Escape, reachable by the pointer |
| `inputs` | all | wrong files, a half board, broken, oversized and zip-bomb parameter files, numbers typed and stepped |
| `behaviour` | all | presets, Mode and formats, stale results, export and import round trip, the report, downloads, views, cross-section, fit, screenshot, parts |
| `tips` | Chromium | every setting and button shown has its tip in `tips.json`; a setting's tip marks the file's value, loads its picture and links the Parameter Reference; a preset's and a section's tip; values filled in |
| `pages` | all | footer links, every licence text exists, versions match what is loaded, the privacy page names every server |
| `a11y` | Chromium | axe (WCAG 2.0 to 2.2, A and AA) in every state; reflow at 200 to 400 % zoom; wider text spacing; status messages |
| `perf` | Chromium | LCP, CLS, input delay, time to Python, time to make the quick and the HDI board, against budgets |
| `visual` | Chromium, CI only | screenshots of the main states against `specs/__screenshots__/chromium/` (made in CI's image) |
| `live` | Chromium | `@live`: the published page after a deploy (see below) |

Headless Firefox on some Linux machines has no WebGL. The tests then check the page without the preview (Generate and
downloads still work) instead of failing.

## Updating the screenshots

A change to the look fails `visual.spec.mjs`. When the change is meant, look at the diff in the HTML report
(`npx playwright show-report`) and then write new baselines **in CI's image**, never on your own machine: another
machine has other default fonts, so text wraps differently and every comparison fails in CI. With Docker, from the
repository's root, after `npm run build`:

```sh
docker run --rm --ipc=host --init -v "$PWD":/repo -w /repo/WebUI/tests -e CI=1 \
  mcr.microsoft.com/playwright:v1.64.1-noble \
  npx playwright test --project=chromium specs/visual.spec.mjs --update-snapshots
```

The image's version must match `@playwright/test` in `package.json` (and the workflow's `container: image:`).
Commit the new PNG files with the change. The build stamp, the run's time and the 3D canvas are masked, so they never
fail the comparison; a small tolerance (`playwright.config.mjs`) absorbs anti-aliasing.

## In CI

`.github/workflows/WebUI-Tests.yml` runs on every pull request into `WebUI`:

1. **generator:** the generator's own pytest suite.
2. **build:** `build_site.py`, kept as the artifact `site` (the exact site the pull request would publish).
3. **browsers:** this suite in Chromium, Firefox and WebKit, in the Playwright container that matches
   `package.json`, with `KESE_NETWORK=1`.
4. **lighthouse:** `lhci autorun` against `lighthouserc.json`.

Failed tests leave their screenshots in the artifact `playwright-report-<browser>`.

After a merge, `.github/workflows/WebUI-Pages.yml` deploys, then its `smoke` job runs `live.spec.mjs` against the
published page. It waits until `version.json` names the deployed commit, checks that the page loads from jsDelivr,
and makes a board. To run it by hand:

```sh
KESE_LIVE_URL=https://rolandthsive.github.io/KiCad-EM-Stackup-Exporter-KESE/WebUI/ npx playwright test --project=chromium
```

## Files

- `playwright.config.mjs`: browsers, timeouts, which tags run.
- `helpers.mjs`: the jsDelivr stand-in, error collection, waits for Python and for a run.
- `serve.mjs`: a small static server for `.site/`.
- `lighthouserc.json`: the Lighthouse budgets.
- `fixtures/`: test files (a zip bomb: 6 KB packed, 6 MB unpacked).
- `.site/`, `test-results/`, `playwright-report/`, `.lighthouseci/`: made by the runs, not committed.
