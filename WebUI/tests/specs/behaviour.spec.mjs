// behaviour.spec.mjs - what the controls do: presets, Mode and the formats, the "Settings changed" badge, Reset,
// Export and Import round trip, the report, the preview tools, the parts list and the downloads.
import { test, expect, open, runBoard, result, QUICK } from "../helpers.mjs";
import { mkdtempSync, writeFileSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const dir = mkdtempSync(join(tmpdir(), "kese-beh-"));
const stale = (page) => page.evaluate(() => !document.getElementById("stale-badge").hidden);
const downloadOn = (page) => page.evaluate(() => !document.getElementById("btn-download").disabled);
const formats = (page) => page.$$eval("#formats label", (x) => x.map((l) => l.textContent.trim() + (l.querySelector("input").checked ? "*" : "") + (l.classList.contains("dis") ? "(off)" : "")));
const mode = (page) => page.$eval("#mode-switch button.on", (x) => x.textContent.trim());

test("a preset lights while its values hold; Reset puts everything back", async ({ page, problems }) => {
  await open(page);
  await page.$eval("#sections details[data-module=Run]", (d) => (d.open = true));
  const lit = () => page.$$eval(".presets-wrap button.on", (x) => x.map((e) => e.textContent.trim()));
  for (const n of ["FreeCAD", "Elmer", "Viewer", "Blender GLB", "openEMS"]) {
    await page.click(`.presets-wrap button:text-is("${n}")`); await page.waitForTimeout(200);
    expect(await lit()).toEqual([n]);
  }
  await page.click("#btn-reset"); await page.click("#confirm-dialog button[value=yes]"); await page.waitForTimeout(300);
  expect(await lit()).toEqual([]);
  expect(await mode(page)).toBe("Simulation");
});

test("Mode keeps the formats each mode had, and allows only that mode's formats", async ({ page, problems }) => {
  await open(page);
  const start = await formats(page);
  await page.click("#formats >> text=STL");
  const sim = await formats(page);
  expect(sim).not.toEqual(start);
  await page.click("#mode-switch >> text=Visual");
  expect(await mode(page)).toBe("Visual");
  const vis = await formats(page);
  // a visual model is a skin: STEP and STL (solids for solvers) can not be ticked
  expect(vis.filter((f) => /^(STEP|STL)/.test(f)).every((f) => f.endsWith("(off)") && !f.includes("*"))).toBe(true);
  expect(vis.some((f) => f.includes("*"))).toBe(true);
  await page.click("#mode-switch >> text=Simulation");
  expect(await formats(page)).toEqual(sim);                      // remembered
});

test("Settings changed shows while the settings differ from the run's, and Download waits", async ({ page, problems }) => {
  await open(page);
  await runBoard(page, QUICK);
  expect(await stale(page)).toBe(false);
  expect(await downloadOn(page)).toBe(true);
  await page.$eval("#sections details[data-module=Board]", (d) => (d.open = true));
  const sw = '.field[data-key="Board.BOARD_ENABLED"] .switch-row';
  await page.click(sw); await page.waitForTimeout(200);
  expect(await stale(page)).toBe(true);
  expect(await downloadOn(page)).toBe(false);
  await page.click(sw); await page.waitForTimeout(200);          // back as it was: the model is current again
  expect(await stale(page)).toBe(false);
  expect(await downloadOn(page)).toBe(true);
  await page.click("#mode-switch >> text=Visual"); await page.waitForTimeout(200);
  expect(await stale(page)).toBe(true);
  await page.click("#mode-switch >> text=Simulation"); await page.waitForTimeout(200);
  expect(await stale(page)).toBe(false);
});

test("Export Parameters, then Import of that zip, gives the same settings", async ({ page, problems }) => {
  await open(page);
  await page.click("#formats >> text=STL");
  await page.$eval("#sections details[data-module=Copper]", (d) => (d.open = true));
  const sel = '.field[data-key="Copper.VIA_WALL_MM"] .stepper input';
  await page.fill(sel, "0.031"); await page.press(sel, "Enter");
  const [dl] = await Promise.all([page.waitForEvent("download"), page.click("#btn-export")]);
  expect(dl.suggestedFilename()).toBe("KESE_parameters.zip");
  const zip = join(dir, "export.zip"); await dl.saveAs(zip);
  expect(readFileSync(zip).subarray(0, 2).toString()).toBe("PK");
  const before = await formats(page);
  await page.click("#btn-reset"); await page.click("#confirm-dialog button[value=yes]"); await page.waitForTimeout(300);
  expect(await page.inputValue(sel)).not.toBe("0.031");
  await page.setInputFiles("#import-file", zip);
  await page.waitForFunction(() => /Loaded/.test(document.getElementById("toast").textContent), null, { timeout: 15_000 });
  expect(await page.inputValue(sel)).toBe("0.031");
  expect(await formats(page)).toEqual(before);
});

test("a parameters.txt of another run is imported, its unknown names listed", async ({ page, problems }) => {
  await open(page);
  const f = join(dir, "parameters.txt");
  writeFileSync(f, '[parameters/run.py]\nMODE = "visual"\nFILE_FORMAT = ["glb"]\nNOT_A_SETTING = 3\n');
  await page.setInputFiles("#import-file", f);
  await page.waitForFunction(() => /Loaded/.test(document.getElementById("toast").textContent), null, { timeout: 15_000 });
  expect(await page.textContent("#toast")).toMatch(/Ignored.*NOT_A_SETTING/);
  expect(await mode(page)).toBe("Visual");
});

test("the run's report, the preview tools, the parts list and the downloads", async ({ page, problems, browserName }) => {
  await open(page);
  await runBoard(page, QUICK);
  const r = await result(page);
  // Show Report
  await page.click("#btn-report");
  await expect(page.locator("#report-dialog")).toBeVisible();
  expect(await page.textContent("#report-text")).toMatch(/14_stackup_full[\s\S]*generated/);
  await page.keyboard.press("Escape");
  await expect(page.locator("#report-dialog")).toBeHidden();
  // the whole run as one zip, and one file
  const [zip] = await Promise.all([page.waitForEvent("download"), page.click("#btn-download")]);
  expect(zip.suggestedFilename()).toMatch(/^14_stackup_full_.*\.zip$/);
  const [one] = await Promise.all([page.waitForEvent("download"), page.click("#download-files button >> nth=0")]);
  expect(one.suggestedFilename().length).toBeGreaterThan(3);
  if (!r.webgl) return;                                          // no WebGL in this browser: no preview tools
  // views, the cut, Fit, a screenshot
  for (const v of ["top", "bottom", "iso"]) { await page.click(`#views [data-view=${v}]`); expect(await page.$eval(`#views [data-view=${v}]`, (b) => b.classList.contains("on"))).toBe(true); }
  await page.$eval("#cut", (c) => { c.value = 50; c.dispatchEvent(new Event("input", { bubbles: true })); });
  expect(await page.textContent("#cut-out")).toBe("50 %");
  await page.click("#btn-fit");
  const [shot] = await Promise.all([page.waitForEvent("download"), page.click("#btn-shot")]);
  expect(shot.suggestedFilename()).toBe("14_stackup_full_preview.png");
  // a part hidden and shown again
  const part = page.locator("#parts button.part").first();
  await part.click(); await expect(part).toHaveClass(/off/);
  await part.click(); await expect(part).not.toHaveClass(/off/);
});
