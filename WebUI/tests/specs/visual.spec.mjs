// visual.spec.mjs - screenshots compared with the ones in __screenshots__/ (Chromium, Linux): a change of the look
// that nobody meant shows up as a failed test, with the difference in the report.  What changes by itself is masked:
// the build stamp and the run's time; the 3D view is compared only in its own shot, more loosely (GPU drawing).
// After a deliberate change of the look: npx playwright test specs/visual.spec.mjs --update-snapshots, check the
// new pictures, commit them.
import { test, expect, open, runBoard, QUICK } from "../helpers.mjs";

test.skip(({ browserName }) => browserName !== "chromium", "Chromium only: the pictures are per browser and system");
const masks = (page) => [page.locator("#foot .build"), page.locator("#run-note"), page.locator("#view")];

test("ready, before a board", async ({ page, problems }) => {
  await open(page);
  await expect(page).toHaveScreenshot("ready.png", { mask: masks(page) });
});

test("a model made, Basic, then Advanced, then portrait", async ({ page, problems }) => {
  await open(page);
  await runBoard(page, QUICK);
  await page.mouse.move(0, 0);
  await expect(page).toHaveScreenshot("made-basic.png", { mask: masks(page) });
  await page.click("#ui-switch [data-ui=advanced]");
  await page.$eval("#sections details[data-module=Copper]", (d) => (d.open = true));
  await page.mouse.move(0, 0);
  await expect(page).toHaveScreenshot("made-advanced.png", { mask: masks(page) });
  await page.setViewportSize({ width: 1080, height: 1920 });
  await page.waitForTimeout(500);
  await expect(page).toHaveScreenshot("made-portrait.png", { mask: masks(page) });
});

test("the 3D preview of a model", async ({ page, problems }) => {
  await open(page);
  await runBoard(page, QUICK);
  await page.mouse.move(0, 0);
  await expect(page.locator("#canvas-wrap")).toHaveScreenshot("preview.png", { maxDiffPixelRatio: 0.05, threshold: 0.3, mask: [page.locator("#readout")] });
});

test("the Reset dialog", async ({ page, problems }) => {
  await open(page);
  await page.click("#btn-reset");
  await expect(page).toHaveScreenshot("reset-dialog.png", { mask: masks(page) });
});

test("the privacy page", async ({ page }) => {
  await page.goto("privacy.html");
  await expect(page).toHaveScreenshot("privacy.png", { fullPage: true });
});
