// playwright.config.mjs - the KESE web tool's browser tests.  See README.md.
//
// Before a run, build the site into .site/ (npm run build, or python3 ../build_site.py .site); the runner serves it
// with serve.mjs.  jsDelivr is replaced by that build's own vendor/ copy (helpers.mjs, `cdn` option), so the
// tests are the same with or without internet; @network tests use the real jsDelivr (CI only: KESE_NETWORK=1).
import { defineConfig, devices } from "@playwright/test";

const PORT = Number(process.env.KESE_PORT || 8811);
const CI = !!process.env.CI;
const LIVE = process.env.KESE_LIVE_URL;      // after a deploy: test the published site instead (no local server)

export default defineConfig({
  testDir: "specs",
  outputDir: "test-results",
  snapshotPathTemplate: "{testDir}/__screenshots__/{projectName}/{arg}{ext}",
  timeout: 240_000,                         // a test that generates a board waits for Python and the run
  expect: { timeout: 30_000, toHaveScreenshot: { maxDiffPixelRatio: 0.02, threshold: 0.25, animations: "disabled" } },
  fullyParallel: false,
  workers: CI ? 2 : 3,
  retries: CI ? 1 : 0,
  forbidOnly: CI,
  grep: LIVE ? /@live/ : undefined,
  grepInvert: LIVE ? undefined : process.env.KESE_NETWORK ? /@live/ : /@network|@live/,
  reporter: CI ? [["list"], ["html", { open: "never" }], ["github"]] : [["list"]],
  use: {
    baseURL: LIVE || `http://127.0.0.1:${PORT}/WebUI/`,
    viewport: { width: 1440, height: 900 },
    actionTimeout: 30_000,                  // a click that cannot happen fails in 30 s, not at the test's end
    trace: "off",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"], viewport: { width: 1440, height: 900 } } },
    { name: "firefox", use: { ...devices["Desktop Firefox"], viewport: { width: 1440, height: 900 } } },
    { name: "webkit", use: { ...devices["Desktop Safari"], viewport: { width: 1440, height: 900 } } },
  ],
  webServer: LIVE ? undefined : {
    command: `node serve.mjs .site ${PORT}`,
    url: `http://127.0.0.1:${PORT}/WebUI/version.json`,
    reuseExistingServer: !CI,
    timeout: 30_000,
  },
});
