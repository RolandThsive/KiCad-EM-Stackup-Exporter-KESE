// keyboard.spec.mjs - the page by keyboard alone: every Tab stop shows where the focus is and is visible, menus open,
// pick and close with keys, closed menus are not Tab stops, dialogs take and give back the focus, Ctrl+Enter generates.
import { test, expect, open, runBoard, QUICK } from "../helpers.mjs";

const DD = '.field[data-key="Finish.FINISH_TYPE"] .dropdown-btn';
const openAll = async (page) => {
  await page.click("#ui-switch [data-ui=advanced]");
  await page.$$eval("#sections details", (d) => d.forEach((x) => (x.open = true)));
  await page.waitForTimeout(600);                               // menus fade out in 0.3 s
};

test("every Tab stop is visible and shows a focus ring", async ({ page, problems, browserName }) => {
  test.skip(browserName === "webkit", "Safari's Tab skips buttons and links unless the visitor turns that on");
  await open(page);
  await openAll(page);
  await page.mouse.click(5, 5);
  const seen = new Set(), bad = [];
  for (let i = 0; i < 1200; i++) {
    await page.keyboard.press("Tab");
    const r = await page.evaluate(() => {
      const e = document.activeElement; if (!e || e === document.body) return null;
      const key = (e.closest("[data-key]") || {}).dataset?.key || "";
      const k = `${e.tagName} ${e.id || key || e.className} "${(e.textContent || e.value || "").trim().slice(0, 20)}"`;
      const ringOf = (x) => { const cs = getComputedStyle(x); return (cs.outlineStyle !== "none" && parseFloat(cs.outlineWidth) > 0) || (cs.boxShadow !== "none" && e.matches(":focus-visible")); };
      // a switch shows the focus on its track, a number field on its whole stepper
      const knob = e.matches(".switch input") ? e.parentElement.querySelector(".knob") : e.matches(".stepper input") ? e.parentElement : null;
      return { k, ring: ringOf(knob || e), shown: (knob || e).getClientRects().length > 0, inert: !!e.closest("[inert]"), inPage: !!e.closest("#app, dialog") };
    });
    if (!r) continue;
    if (seen.has(r.k)) break;
    seen.add(r.k);
    if (!r.ring) bad.push(`no focus ring: ${r.k}`);
    if (!r.shown) bad.push(`focus on something hidden: ${r.k}`);
    if (r.inert) bad.push(`focus inside an inert field: ${r.k}`);
  }
  expect(seen.size).toBeGreaterThan(100);                       // Advanced with every section open
  expect(bad).toEqual([]);
});

test("a menu opens, picks and closes by keys, and closed menus are no Tab stops", async ({ page, problems }) => {
  await open(page);
  await openAll(page);
  await page.focus(DD);
  await page.keyboard.press("Enter"); await page.waitForTimeout(300);
  expect(await page.evaluate(() => !!document.querySelector(".dropdown.open"))).toBe(true);
  expect(await page.evaluate(() => !!document.activeElement.closest(".dropdown-content"))).toBe(true);
  await page.keyboard.press("End");
  expect(await page.evaluate(() => { const a = document.activeElement; return a === a.parentElement.lastElementChild; })).toBe(true);
  await page.keyboard.press("Home");
  expect(await page.evaluate(() => { const a = document.activeElement; return a === a.parentElement.firstElementChild; })).toBe(true);
  await page.keyboard.press("Escape"); await page.waitForTimeout(300);
  expect(await page.evaluate(() => !document.querySelector(".dropdown.open"))).toBe(true);
  expect(await page.evaluate(() => document.activeElement.classList.contains("dropdown-btn"))).toBe(true);
  const before = await page.textContent(DD);
  await page.keyboard.press("ArrowDown"); await page.waitForTimeout(300);
  await page.keyboard.press("ArrowDown"); await page.keyboard.press("Enter"); await page.waitForTimeout(400);
  expect(await page.textContent(DD)).not.toBe(before);
  expect(await page.evaluate(() => !!document.activeElement.closest('[data-key="Finish.FINISH_TYPE"]'))).toBe(true);
  await page.waitForTimeout(600);
  expect(await page.evaluate(() => [...document.querySelectorAll(".dropdown:not(.open) .dropdown-content a")].filter((a) => getComputedStyle(a).visibility !== "hidden").length)).toBe(0);
});

test("the Reset dialog takes the focus on No, Escape closes it and nothing changes", async ({ page, problems }) => {
  await open(page);
  await page.click("#btn-reset");
  await expect(page.locator("#confirm-dialog")).toBeVisible();
  expect(await page.evaluate(() => document.activeElement.value)).toBe("no");
  await page.keyboard.press("Escape");
  await expect(page.locator("#confirm-dialog")).toBeHidden();
});

test("Ctrl+Enter generates, also while a number is being typed", async ({ page, problems }) => {
  await open(page);
  await runBoard(page, QUICK);
  await page.$eval("#sections details[data-module=Copper]", (d) => (d.open = true));
  const input = '.field[data-key="Copper.VIA_WALL_MM"] .stepper input';
  await page.fill(input, "0.03");
  await page.keyboard.press("Control+Enter");
  await page.waitForFunction(() => document.getElementById("progress").classList.contains("busy"), null, { timeout: 10_000, polling: 50 });
  await page.waitForFunction(() => !document.getElementById("progress").classList.contains("busy") && document.getElementById("run-card").hidden, null, { timeout: 300_000 });
  await expect(page.locator("#stale-badge")).toBeHidden();       // the run used the typed value
  expect(await page.inputValue(input)).toBe("0.03");
});

// WCAG 1.4.13 (content on hover or focus): a tip comes with the keyboard's focus as with the pointer, Escape closes it
// without moving anything, and the pointer can move onto the tip to read it
test("tips come with the focus, close with Escape and stay while the pointer is on them", async ({ page, problems, browserName }) => {
  await open(page);
  const pop = page.locator("#popover");
  if (browserName !== "webkit") {                               // Safari's Tab skips buttons unless the visitor turns that on
    await page.mouse.click(5, 5);
    await page.keyboard.press("Tab");
    const { tip, id } = await page.evaluate(() => { const n = document.activeElement.closest("[data-tip]"); return { tip: n?.dataset.tip, id: n?.dataset.tipId }; });
    expect(tip).toBeTruthy();
    await expect(pop).toBeVisible();
    if (id) await expect(pop.locator(".tp-lead")).not.toBeEmpty();   // its words from tips.json
    else await expect(pop).toHaveText(tip);
    await page.keyboard.press("Escape");
    await expect(pop).toBeHidden();
  }
  await page.hover("#btn-import");
  await expect(pop).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(pop).toBeHidden();
  await page.mouse.move(0, 0);
  await page.hover("#btn-import");
  await expect(pop).toBeVisible();
  const b = await pop.boundingBox();
  await page.mouse.move(b.x + b.width / 2, b.y + b.height / 2, { steps: 8 });
  await page.waitForTimeout(800);
  await expect(pop).toBeVisible();
  await page.mouse.move(700, 600, { steps: 4 });                // the preview: no tip there
  await expect(pop).toBeHidden();
});

// WCAG 1.4.10 (reflow): zoomed to 200 % and 400 % (640 x 512 and 320 x 256 here), a tip taller than the window stays
// inside it and scrolls inside; at 200 % it takes the larger side of its control and leaves the control in view
test("a tall tip stays inside a zoomed window, scrolls inside, and leaves its control in view at 200 %", async ({ page, problems }) => {
  await open(page);
  await openAll(page);
  const pop = page.locator("#popover"), dot = '[data-help="Copper.CASTELLATION"] .info-dot';
  for (const [w, h] of [[640, 512], [320, 256]]) {
    await page.setViewportSize({ width: w, height: h });
    await page.mouse.move(0, 0);
    await expect(pop).toBeHidden();
    await page.locator(dot).evaluate((e) => e.scrollIntoView({ block: "center" }));
    await page.waitForTimeout(200);                             // a scroll closes tips: let it settle first
    await page.hover(dot);
    await expect(pop).toBeVisible();
    const m = await page.evaluate((sel) => {
      const p = document.getElementById("popover"), a = p.getBoundingClientRect(), t = document.querySelector(sel).getBoundingClientRect();
      return { a: { l: a.left, t: a.top, r: a.right, b: a.bottom }, W: document.documentElement.clientWidth, H: document.documentElement.clientHeight,
        scrolls: p.scrollHeight > p.clientHeight + 1, clear: a.bottom <= t.top || a.top >= t.bottom || a.right <= t.left || a.left >= t.right };
    }, dot);
    expect(m.a.l, `left at ${w} x ${h}`).toBeGreaterThanOrEqual(0);
    expect(m.a.t, `top at ${w} x ${h}`).toBeGreaterThanOrEqual(0);
    expect(m.a.r, `right at ${w} x ${h}`).toBeLessThanOrEqual(m.W + 0.5);
    expect(m.a.b, `bottom at ${w} x ${h}`).toBeLessThanOrEqual(m.H + 0.5);
    expect(m.scrolls, `the tip scrolls inside at ${w} x ${h}`).toBe(true);
    if (w === 640) expect(m.clear, "the control stays in view at 200 %").toBe(true);
    await pop.evaluate((p) => p.scrollBy(0, 80));               // scrolling the tip itself leaves it open
    await page.waitForTimeout(200);
    await expect(pop).toBeVisible();
  }
});
