// perf.spec.mjs - time budgets, measured the way a visitor feels them (Chromium; jsDelivr's stand-in serves from
// disk, so the numbers are the page's own work, not the network's).  Measured when the budgets were set (4 cores):
// LCP 0.76 s, CLS 0.009, Python ready 3.5 s, 44 ms to answer a click during a run, 14_stackup_full 4.3 s,
// hdi_module 29 s.  The time budgets leave room for a slower CI runner (about 5x): a test fails when the page gets
// clearly slower, not on a noisy run.
// Core Web Vitals "good" limits (web.dev): LCP <= 2.5 s, CLS <= 0.1, INP <= 200 ms.
import { test, expect, open, runBoard, QUICK, EXAMPLES } from "../helpers.mjs";
import { join } from "node:path";

test.skip(({ browserName }) => browserName !== "chromium", "Chromium only (the APIs used are Chromium's)");
const BUDGET = { lcp: 2500, cls: 0.1, input: 200, python: 20_000, quick: 25_000, hdi: 150_000 };

test("loading: LCP and CLS within Core Web Vitals, Python ready within budget", async ({ page, problems }) => {
  await page.addInitScript(() => {
    window.__lcp = 0; window.__cls = 0;
    new PerformanceObserver((l) => { for (const e of l.getEntries()) window.__lcp = Math.max(window.__lcp, e.startTime); }).observe({ type: "largest-contentful-paint", buffered: true });
    new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; }).observe({ type: "layout-shift", buffered: true });
  });
  const t0 = Date.now();
  await open(page);
  const python = Date.now() - t0;
  const { lcp, cls } = await page.evaluate(() => ({ lcp: window.__lcp, cls: window.__cls }));
  test.info().annotations.push({ type: "measured", description: `LCP ${lcp | 0} ms, CLS ${cls.toFixed(3)}, Python ready ${python} ms` });
  expect(lcp).toBeLessThan(BUDGET.lcp);
  expect(cls).toBeLessThan(BUDGET.cls);
  expect(python).toBeLessThan(BUDGET.python);
});

test("the page answers within 200 ms while Python works", async ({ page, problems }) => {
  await open(page);
  await page.setInputFiles("#board-file", join(EXAMPLES, "hdi_module.kicad_pcb"));
  await page.waitForFunction(() => document.getElementById("progress").classList.contains("busy"), null, { polling: 50 });
  await page.waitForTimeout(2000);                                // well inside the run
  const worst = await page.evaluate(async () => {
    let worst = 0;
    for (let i = 0; i < 8; i++) {
      const b = document.querySelector(`#ui-switch [data-ui=${i % 2 ? "basic" : "advanced"}]`);
      const t = performance.now();
      b.click();
      await new Promise((r) => requestAnimationFrame(() => setTimeout(r, 0)));   // until the next frame is painted
      worst = Math.max(worst, performance.now() - t);
      await new Promise((r) => setTimeout(r, 150));
    }
    return worst;
  });
  test.info().annotations.push({ type: "measured", description: `worst answer ${worst | 0} ms during a run` });
  expect(worst).toBeLessThan(BUDGET.input);
});

test("making a board stays within budget", async ({ page, problems }) => {
  test.setTimeout(600_000);
  await open(page);
  let t = Date.now();
  await runBoard(page, QUICK);
  const quick = Date.now() - t;
  t = Date.now();
  await runBoard(page, join(EXAMPLES, "hdi_module.kicad_pcb"));
  const hdi = Date.now() - t;
  test.info().annotations.push({ type: "measured", description: `14_stackup_full ${quick} ms, hdi_module ${hdi} ms` });
  expect(quick).toBeLessThan(BUDGET.quick);
  expect(hdi).toBeLessThan(BUDGET.hdi);
});
