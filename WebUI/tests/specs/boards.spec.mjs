// boards.spec.mjs - every feature board of featureTest/ (holes, vias, pads, zones, outlines, stack-ups, plating,
// finishes, KiCad 6 to 10, the three example boards), uploaded one after the other in one page as a visitor would:
// each one is made, previewed and offered for download, the layout holds, and nothing goes wrong.  Chromium only
// (the generator is the same Python in every browser; smoke.spec.mjs makes a board in Firefox and WebKit).
import { test, expect, pythonReady, runBoard, result, FEATURE_BOARDS } from "../helpers.mjs";
import { readdirSync } from "node:fs";
import { join } from "node:path";

const boards = readdirSync(FEATURE_BOARDS).filter((f) => f.endsWith(".kicad_pcb")).sort();
test.describe.configure({ mode: "serial" });
test.skip(({ browserName }) => browserName !== "chromium", "Chromium only");

let page, problems;
test.beforeAll(async ({ browser }) => {
  page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  problems = [];
  page.on("pageerror", (e) => problems.push(`pageerror: ${e.message}`));
  page.on("console", (m) => { if (m.type() === "error") problems.push(`console: ${m.text().slice(0, 300)}`); });
  await page.context().route("https://cdn.jsdelivr.net/**", (r) => r.abort());   // the backup copy: no stand-in needed here
  await page.goto("./");
  await pythonReady(page);
});
test.afterAll(async () => { await page?.close(); });   // no page when the file is skipped

for (const name of boards) {
  test(name, async () => {
    test.setTimeout(900_000);
    problems.length = 0;
    await runBoard(page, join(FEATURE_BOARDS, name));
    const r = await result(page);
    expect(r.board.replace(/\s/g, "")).toBe(name);
    expect(r.counts, r.errors.join("\n")).toMatch(/Warning|No Warnings/);
    expect(r.note).toMatch(/^Done in/);
    expect(r.download).toBe(true);
    expect(r.stale).toBe(false);
    expect(r.chips).toBeGreaterThan(0);
    expect(r.parts).toBeGreaterThan(0);
    expect(r.readout).toMatch(/parts · .* triangles/);
    const layout = await page.evaluate(() => {
      const bad = [], de = document.documentElement;
      if (de.scrollWidth > de.clientWidth + 1) bad.push(`page scrolls sideways (${de.scrollWidth} > ${de.clientWidth})`);
      for (const col of ["#controls", "#side", "#preview"]) {
        const cr = document.querySelector(col).getBoundingClientRect();
        for (const e of document.querySelectorAll(`${col} *`)) {
          if (!e.getClientRects().length || e.closest(".dropdown-content, .popover, canvas")) continue;
          const er = e.getBoundingClientRect();
          if (er.width && (er.right > cr.right + 1 || er.left < cr.left - 1)) { bad.push(`${col}: ${e.tagName} "${e.textContent.trim().slice(0, 24)}" sticks out`); break; }
        }
      }
      return bad;
    });
    expect(layout).toEqual([]);
    expect(problems).toEqual([]);
  });
}
