// smoke.spec.mjs - in every browser: the page starts, Python loads, an example board is made, previewed and offered
// for download, and nothing goes wrong on the way (no page error, console error or CSP violation).
import { test, expect, open, runBoard, result, EXAMPLES } from "../helpers.mjs";
import { join } from "node:path";

test("starts, makes the HDI example and offers its files", async ({ page, problems, cdnRequests }) => {
  await open(page);
  await expect(page.locator("#foot")).toContainText(/build \w+/);
  await expect(page.locator("#foot")).toContainText("Privacy");
  // Python and three.js came from "jsDelivr" (the test's stand-in), not from the backup copy
  expect(await page.evaluate(() => window.KESE_THREE)).toBe("cdn");
  expect(cdnRequests.some((u) => u.endsWith("pyodide.asm.wasm"))).toBe(true);
  await runBoard(page, join(EXAMPLES, "hdi_module.kicad_pcb"));
  const r = await result(page);
  expect(r.counts).toMatch(/Warning|No Warnings/);
  expect(r.download).toBe(true);
  expect(r.chips).toBeGreaterThan(0);
  if (r.webgl) {
    expect(r.parts).toBeGreaterThan(3);
    expect(r.readout).toMatch(/parts · .* triangles/);
  } else {
    await expect(page.locator("#empty-note")).toContainText("WebGL");
    expect(r.readout).toMatch(/is made/);
  }
});
