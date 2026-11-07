// tips.spec.mjs - the tips' words come from tips.json: every setting and button the page shows has its tip there, a
// setting's tip marks the file's value and shows its picture, a preset's tip lists what it sets, and a tip with
// values fills them in.
import { test, expect, open, runBoard, QUICK, SITE } from "../helpers.mjs";
import { readFileSync } from "node:fs";
import { join } from "node:path";

const TIPS = JSON.parse(readFileSync(join(SITE, "tips.json"), "utf8"));
test.skip(({ browserName }) => browserName !== "chromium", "the words are the same in every browser; the tips' behaviour is in keyboard.spec");

// Advanced, STEP ticked and every part switched on, so every section and field shows; then every section opened
async function everything(page) {
  await open(page);
  await page.click("#ui-switch [data-ui=advanced]");
  const step = page.locator("#formats label", { hasText: "STEP" }).locator("input");
  if (!(await step.isChecked())) await page.locator("#formats label", { hasText: "STEP" }).click();
  await page.$$eval("#sections details", (ds) => ds.forEach((d) => (d.open = true)));
  for (const key of ["SolderMask.SOLDER_MASK_ENABLED", "Silkscreen.SILKSCREEN_ENABLED", "Finish.FINISH_ENABLED"]) {
    const row = page.locator(`[data-key="${key}"] .switch-row`).first();
    if (!(await row.locator("input").isChecked())) await row.click();
    await page.$$eval("#sections details", (ds) => ds.forEach((d) => (d.open = true)));
  }
}
const tipOf = (page) => page.locator("#popover");
// a scroll closes any tip, and Playwright's hover scrolls first: scroll, let it settle, then hover
async function hover(page, sel) {
  await page.locator(sel).scrollIntoViewIfNeeded();
  await page.waitForTimeout(150);
  await page.hover(sel);
}

test("every setting and button the page shows has its own tip in tips.json", async ({ page, problems }) => {
  await everything(page);
  const { keys, ids } = await page.evaluate(() => ({
    keys: [...new Set([...document.querySelectorAll("[data-help]")].map((e) => e.dataset.help))],
    ids: [...new Set([...document.querySelectorAll("[data-tip-id]")].map((e) => e.dataset.tipId))],
  }));
  expect(keys.length).toBeGreaterThan(120);
  expect(keys.filter((k) => !TIPS.settings[k]), "settings without a tip").toEqual([]);
  const missing = ids.filter((id) => (id.startsWith("section.") ? !TIPS.sections[id.slice(8)]
    : id.startsWith("preset.") ? !TIPS.presets[id.slice(7)] : !TIPS.page[id]));
  expect(missing, "buttons whose tip is not in tips.json").toEqual([]);
  for (const [k, s] of Object.entries(TIPS.settings)) if (s.img) expect(TIPS.pictures[s.img], `${k}'s picture`).toBeTruthy();
  for (const [k, s] of Object.entries(TIPS.page)) if (s.img) expect(TIPS.pictures[s.img], `${k}'s picture`).toBeTruthy();
});

test("a setting's tip: title, unit, choices with the file's value marked, its picture and the wiki", async ({ page, problems }) => {
  await everything(page);
  await hover(page, '[data-help="Copper.ETCH_FACTOR"] .info-dot');
  const pop = tipOf(page);
  await expect(pop).toBeVisible();
  await expect(pop).toHaveClass(/rich/);
  await expect(pop.locator(".tp-title")).toHaveText("Etch Factor");
  await expect(pop.locator(".tp-eyebrow")).toHaveText("Copper · Etch factor");
  await expect(pop.locator(".tp-key")).toHaveText("copper.py · ETCH_FACTOR");
  await expect(pop.locator(".tp-chip.file")).toHaveCount(1);
  await expect(pop.locator(".tp-foot code")).toHaveText(await pop.locator(".tp-chip.file").textContent());
  const img = pop.locator(".tp-fig img");
  await expect(img).toHaveAttribute("src", /tooltips\/etch\.webp$/);
  await expect.poll(() => img.evaluate((i) => i.complete && i.naturalWidth)).toBeGreaterThan(0);
  await expect(pop.locator(".tp-foot a")).toHaveAttribute("href", /\/wiki\/Parameter-Reference#173-copper-/);
  // the pointer can reach the picture's wiki link
  const box = await pop.boundingBox();
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 6 });
  await page.waitForTimeout(500);
  await expect(pop).toBeVisible();
  // a desktop-only setting says so; a table's file value is a table, not JSON
  await page.mouse.move(0, 0); await expect(pop).toBeHidden();
  await hover(page, '[data-help="Parallel.WORKERS"] .info-dot');
  await expect(pop.locator(".tp-badge")).toHaveText("Desktop only");
  await page.mouse.move(0, 0); await expect(pop).toBeHidden();
  await hover(page, '[data-help="Finish.FINISH_CONDUCTIVITY_S_PER_M"] .info-dot');
  await expect(pop.locator(".tp-foot .tp-table tr")).not.toHaveCount(0);
  await expect(pop).not.toContainText("{");
});

test("a section's and a preset's tip; a tip with values fills them in", async ({ page, problems }) => {
  await open(page);
  await page.$eval("#sections details[data-module=Run]", (d) => (d.open = true));
  const pop = tipOf(page);
  await hover(page, "#sections details[data-module=Copper] > summary");
  await expect(pop.locator(".tp-eyebrow")).toHaveText("Section");
  await expect(pop.locator(".tp-facts")).toContainText("Settings");
  await page.mouse.move(0, 0); await expect(pop).toBeHidden();
  await hover(page, '.presets-wrap button:text-is("FreeCAD")');
  await expect(pop.locator(".tp-title")).toHaveText("FreeCAD");
  await expect(pop.locator(".tp-table")).toContainText("STEP");
  await expect(pop.locator(".tp-table")).toContainText("Simulation");
  await page.mouse.move(0, 0); await expect(pop).toBeHidden();
  await hover(page, "#drop");
  await expect(pop.locator(".tp-facts")).toContainText("up to 500 MB");
  await page.mouse.move(0, 0); await expect(pop).toBeHidden();
  await hover(page, "#examples button >> nth=0");
  await expect(pop.locator(".tp-title")).not.toHaveText("");
  await expect(pop).not.toContainText("{");
});

test("after a run, the tips of a part, a file and Download Zip name them", async ({ page, problems }) => {
  await open(page);
  await runBoard(page, QUICK);
  const pop = tipOf(page);
  const part = page.locator("#parts button.part").first();
  const name = (await part.locator(".part-name").textContent()).trim();
  await hover(page, "#parts button.part >> nth=0");
  await expect(pop.locator(".tp-title")).toHaveText(name);
  await expect(pop.locator(".tp-facts")).toContainText("Triangles");
  await page.mouse.move(0, 0); await expect(pop).toBeHidden();
  const chip = (await page.locator("#download-files button").first().textContent()).trim();
  await hover(page, "#download-files button >> nth=0");
  await expect(pop.locator(".tp-title")).toHaveText(chip);
  await expect(pop.locator(".tp-facts")).toContainText(/\d/);
  await page.mouse.move(0, 0); await expect(pop).toBeHidden();
  await hover(page, "#btn-download");
  await expect(pop.locator(".tp-facts")).toContainText(".zip");
  await expect(pop).not.toContainText("{");
});

test("without tips.json, every tip falls back to its plain words", async ({ page, problems }) => {
  test.info().annotations.push({ type: "allow", description: "Failed to load resource" });
  await page.route("**/tips.json", (route) => route.fulfill({ status: 404, body: "" }));
  await open(page);
  const pop = tipOf(page);
  await hover(page, "#drop");
  await expect(pop).toBeVisible();
  await expect(pop).not.toHaveClass(/rich/);
  await expect(pop).toHaveText(await page.locator("#drop").getAttribute("data-tip"));
  await page.mouse.move(0, 0); await expect(pop).toBeHidden();
  await page.click("#ui-switch [data-ui=advanced]");
  await page.$eval("#sections details[data-module=Copper]", (d) => (d.open = true));
  await hover(page, '[data-help="Copper.ETCH_FACTOR"] .info-dot');
  await expect(pop).not.toHaveClass(/rich/);
  await expect(pop.locator(".mono-name")).toHaveText("copper.py · ETCH_FACTOR");
  await expect(pop.locator(".tip-foot")).toContainText("In the file:");
});
