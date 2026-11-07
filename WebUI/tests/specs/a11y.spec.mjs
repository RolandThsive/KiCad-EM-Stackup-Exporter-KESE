// a11y.spec.mjs - automatic accessibility scans (axe-core) against WCAG 2.0, 2.1 and 2.2, levels A and AA, in each
// state of the page: starting, ready, a model made, Advanced with every section open, each dialog, the side pages.
// axe finds about a third to a half of WCAG problems; the rest is in docs/WCAG-EM.md (checked by hand).
import { test, expect, open, runBoard, QUICK } from "../helpers.mjs";
import AxeBuilder from "@axe-core/playwright";

test.skip(({ browserName }) => browserName !== "chromium", "Chromium only (the same page in every browser)");
const TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"];
async function scan(page, what) {
  // buttons fade in over 0.3 s once enabled: scan the end state, once every finite transition has finished
  await page.waitForTimeout(100);
  await page.waitForFunction(() => document.getAnimations().every((a) => a.playState !== "running" || a.effect?.getTiming().iterations === Infinity),
    null, { timeout: 10_000, polling: 100 });
  await page.waitForTimeout(100);
  const r = await new AxeBuilder({ page }).withTags(TAGS).exclude("#view").analyze();
  const found = r.violations.map((v) => `${what}: ${v.id} (${v.impact}) ${v.help} -> ${v.nodes.slice(0, 4).map((n) => n.target.join(" ")).join(" | ")}`);
  expect(found, `${what}: axe found`).toEqual([]);
}

test("ready, made, Advanced", async ({ page, problems }) => {
  test.setTimeout(600_000);
  await open(page);
  await scan(page, "ready");
  await runBoard(page, QUICK);
  await scan(page, "a model made");
  await page.$eval("#show-info", (i) => i.click());
  await scan(page, "checks with Info");
  await page.click("#ui-switch [data-ui=advanced]");
  await page.$$eval("#sections details", (d) => d.forEach((x) => (x.open = true)));
  await page.waitForTimeout(500);
  await scan(page, "Advanced, every section open");
  await page.click("#mode-switch >> text=Visual");
  await page.$$eval("#app details", (d) => d.forEach((x) => (x.open = true)));
  await scan(page, "Visual, Advanced, every section and colour group open");
});

test("the dialogs", async ({ page, problems }) => {
  await open(page);
  await runBoard(page, QUICK);
  await page.click("#btn-reset");
  await scan(page, "Reset dialog");
  await page.keyboard.press("Escape");
  await page.click("#btn-report");
  await scan(page, "report dialog");
  await page.keyboard.press("Escape");
  await page.evaluate(() => window.dispatchEvent(new ErrorEvent("error", { message: "a11y scan", filename: location.href, error: new Error("a11y scan") })));
  await expect(page.locator("#crash-dialog")).toBeVisible();
  await scan(page, "crash dialog");
});

test("while Python loads", async ({ page, problems }) => {
  await page.goto("./");
  await page.waitForSelector("#btn-generate");
  await scan(page, "starting");
});

for (const side of ["privacy.html", "licenses.html"]) {
  test(side, async ({ page }) => {
    await page.goto(side);
    await scan(page, side);
  });
}

// checked by hand once, kept as a test: a computer zoomed to 200, 300 and 400 % (WCAG 1.4.10 reflow, down to 320 CSS
// px) and wider letter, word, line and paragraph spacing (1.4.12): nothing scrolls sideways, no text is cut off
// (the file name in the preview's readout and the part names may end in "…": their full text is in a tip).
async function cutOff(page) {
  return page.evaluate(() => {
    const de = document.documentElement, bad = [];
    if (de.scrollWidth > de.clientWidth + 1) bad.push(`the page scrolls sideways (${de.scrollWidth} > ${de.clientWidth})`);
    for (const e of document.querySelectorAll("button, label, .table-label, h1, h2, h3, p, summary, a, span")) {
      if (!e.getClientRects().length || e.closest(".dropdown-content, .popover, canvas, dialog:not([open])")) continue;
      if (e.matches(".part-name") || (e.matches(".ro-name") && e.title)) continue;
      const cs = getComputedStyle(e);
      if ((cs.overflowX === "hidden" || cs.textOverflow === "ellipsis") && e.scrollWidth > e.clientWidth + 1 && e.textContent.trim())
        bad.push(`cut off: ${e.tagName}.${e.className} "${e.textContent.trim().slice(0, 30)}"`);
    }
    return bad;
  });
}
test.describe("zoom and text spacing", () => {
  test.use({ bypassCSP: true });                                // the spacing comes in as a user style sheet would
  test("reflow at 200 to 400 % zoom, and wider text spacing", async ({ page, problems }) => {
    test.setTimeout(400_000);
    await open(page);
    await runBoard(page, QUICK);
    const found = [];
    for (const [w, h, what] of [[720, 450, "1440x900 at 200%"], [640, 512, "1280x1024 at 200%"], [480, 300, "1440x900 at 300%"],
      [360, 225, "1440x900 at 400%"], [320, 256, "1280x1024 at 400%"]]) {
      await page.setViewportSize({ width: w, height: h }); await page.waitForTimeout(500);
      found.push(...(await cutOff(page)).map((b) => `${what}: ${b}`));
    }
    await page.addStyleTag({ content: "* { line-height: 1.5 !important; letter-spacing: 0.12em !important; word-spacing: 0.16em !important; } p { margin-bottom: 2em !important; }" });
    for (const [w, h] of [[1440, 900], [1024, 768]]) {
      await page.setViewportSize({ width: w, height: h }); await page.waitForTimeout(500);
      found.push(...(await cutOff(page)).map((b) => `text spacing at ${w}x${h}: ${b}`));
    }
    expect(found).toEqual([]);
  });
});

// WCAG 4.1.3: what the page says without moving the focus (the run's note, the checks' counts, "Settings changed",
// a refused file) is in a status region, so a screen reader reads it
test("status messages reach screen readers", async ({ page, problems }) => {
  await open(page);
  for (const id of ["run-note", "counts", "sr-status"]) await expect(page.locator(`#${id}`)).toHaveAttribute("role", "status");
  await expect(page.locator(".top-mid")).toHaveAttribute("role", "status");
  await page.setInputFiles("#board-file", { name: "notes.txt", mimeType: "text/plain", buffer: Buffer.from("hello") });
  await expect(page.locator("#sr-status")).toHaveText("That is not a .kicad_pcb file");
  await runBoard(page, QUICK);
  await expect(page.locator("#run-note")).toHaveText(/^Done in/);
});
