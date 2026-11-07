// live.spec.mjs - after each deploy, the published site itself (KESE_LIVE_URL): it starts with the real jsDelivr,
// shows the commit that was just deployed, and makes a board.  Run by the Pages workflow; @live keeps it out of the
// normal runs.  KESE_EXPECT_COMMIT: the commit the footer must name (the first 7 characters of GITHUB_SHA).
import { test, expect, pythonReady, runBoard, result, QUICK } from "../helpers.mjs";

test("the published page starts on jsDelivr, names this commit and makes a board @live", async ({ page, problems, browserName }) => {
  test.skip(browserName !== "chromium", "once is enough");
  test.setTimeout(600_000);
  // GitHub Pages can take a minute to serve a new deploy everywhere: wait for this commit's version.json
  const want = process.env.KESE_EXPECT_COMMIT;
  if (want) await expect.poll(async () => (await (await page.request.get("version.json", { headers: { "Cache-Control": "no-cache" } })).json()).commit, { timeout: 300_000, intervals: [5_000] }).toBe(want);
  await page.goto("./");
  await pythonReady(page, 300_000);
  if (want) await expect(page.locator("#foot .build")).toContainText(want);
  expect(await page.evaluate(() => window.KESE_THREE)).toBe("cdn");
  expect(await page.evaluate(() => document.querySelector("#foot .build").dataset.tip)).toContain("Python from jsDelivr");
  await runBoard(page, QUICK);
  const r = await result(page);
  expect(r.counts).toMatch(/Warning|No Warnings/);
  expect(r.download).toBe(true);
});
