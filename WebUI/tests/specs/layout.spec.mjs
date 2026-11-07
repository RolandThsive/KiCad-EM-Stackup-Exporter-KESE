// layout.spec.mjs - the layout at 13 window sizes, landscape and portrait, in both modes, Basic and Advanced, with
// every section closed and open, after a board was made: nothing overlaps, sticks out, is cut off or wraps where it
// should stay on one line, and in landscape the page fits the window (no page scroll).  Then the same in the blog's
// frame (another site framing the page).  Chromium only: the rules are the browser's layout, the same CSS everywhere.
import { test, expect, open, pythonReady, runBoard, FEATURE_BOARDS, HERE } from "../helpers.mjs";
import { readFileSync } from "node:fs";
import { join } from "node:path";

test.skip(({ browserName }) => browserName !== "chromium", "Chromium only");
const BOARD = join(FEATURE_BOARDS, "17_mask_silk.kicad_pcb");
const SIZES = [[1024, 768], [1280, 720], [1366, 768], [1440, 900], [1600, 900], [1920, 1080], [2560, 1440], [1280, 1024],
  [834, 1194], [900, 1600], [1080, 1920], [1200, 1920], [1440, 2560]];

// the audit itself runs in the page (or the frame): a list of what is wrong, empty when all is well
function audit() {
  const out = [], vis = (e) => { if (!e.getClientRects().length) return false; const cs = getComputedStyle(e); return cs.visibility !== "hidden" && cs.display !== "none" && +cs.opacity > 0.05; };
  const name = (e) => { const f = e.closest("[data-key]"); return (e.id ? "#" + e.id : e.tagName.toLowerCase() + (typeof e.className === "string" && e.className.trim() ? "." + e.className.trim().split(/\s+/).join(".") : "")) + (f ? ` @${f.dataset.key}` : "") + (e.textContent.trim() ? ` "${e.textContent.trim().slice(0, 30)}"` : ""); };
  const W = document.documentElement.clientWidth, H = document.documentElement.clientHeight;
  if (document.documentElement.scrollWidth > W + 1) out.push(`page scrolls sideways ${document.documentElement.scrollWidth}>${W}`);
  const app = document.getElementById("app"), all = [...app.querySelectorAll("*")].filter(vis);
  for (const c of all) {                                   // siblings in a flex or grid box that overlap
    if (!/flex|grid/.test(getComputedStyle(c).display)) continue;
    const kids = [...c.children].filter((k) => vis(k) && !/absolute|fixed/.test(getComputedStyle(k).position));
    for (let i = 0; i < kids.length; i++) for (let j = i + 1; j < kids.length; j++) {
      const a = kids[i].getBoundingClientRect(), z = kids[j].getBoundingClientRect();
      const ox = Math.min(a.right, z.right) - Math.max(a.left, z.left), oy = Math.min(a.bottom, z.bottom) - Math.max(a.top, z.top);
      if (ox > 2 && oy > 2 && a.width && z.width) out.push(`overlap: ${name(kids[i])} / ${name(kids[j])}`);
    }
  }
  for (const e of all) {                                   // sticking out sideways past a clipping ancestor
    if (e.children.length && !/^(INPUT|BUTTON|SELECT|TEXTAREA)$/.test(e.tagName)) continue;
    let a = e.parentElement; while (a && a !== app && getComputedStyle(a).overflowX === "visible") a = a.parentElement;
    if (!a) continue;
    const r = e.getBoundingClientRect(), q = a.getBoundingClientRect();
    if (r.width && (r.right > q.right + 1 || r.left < q.left - 1)) out.push(`clipped sideways by ${name(a).slice(0, 40)}: ${name(e)}`);
  }
  for (const e of all)                                     // text cut off
    if (!e.children.length && e.textContent.trim() && !e.closest(".download-row, .ro-name") && e.scrollWidth > e.clientWidth + 1 && /hidden|clip/.test(getComputedStyle(e).overflowX)) out.push(`text cut: ${name(e)}`);
  for (const e of all) {                                   // one-line things on two lines
    if (e.id === "counts" || !e.matches("button, h1, h2, .ps-name, label.format, .segmented > *, .glass-btn, .counts, summary > span, .part, .tab")) continue;
    const rects = [], tw = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let t;
    while ((t = tw.nextNode())) { if (!t.textContent.trim()) continue; const r = document.createRange(); r.selectNodeContents(t); rects.push(...[...r.getClientRects()].filter((x) => x.width > 1)); }
    if (rects.some((a) => rects.some((z) => z.top >= a.bottom - 2)) && e.textContent.trim().length < 60) out.push(`wraps: ${name(e)}`);
  }
  const gen = document.getElementById("btn-generate").getBoundingClientRect();
  if (W > H && W > 1080 && gen.bottom > H + 1) out.push("Generate off screen");
  if (W > H && W > 1080 && document.documentElement.scrollHeight > H + 1) out.push(`page scrolls down ${document.documentElement.scrollHeight}>${H}`);
  for (const id of ["controls", "preview", "side"]) { const r = document.getElementById(id).getBoundingClientRect(); if (r.right > W + 1 || r.left < -1) out.push(`#${id} off the page sideways`); if (r.height < 200) out.push(`#${id} only ${r.height | 0} high`); }
  return out;
}

async function sweep(page, frame, sizes, extra) {
  const found = new Map();
  for (const [w, h] of sizes) {
    await page.setViewportSize({ width: w, height: h }); await page.waitForTimeout(400);
    for (const mode of ["Simulation", "Visual"]) {
      await frame.click(`#mode-switch >> text=${mode}`); await page.waitForTimeout(250);
      for (const ui of ["basic", "advanced"]) {
        await frame.click(`#ui-switch [data-ui=${ui}]`); await page.waitForTimeout(250);
        for (const opened of [false, true]) {
          await frame.$$eval("#app details", (d, o) => d.forEach((x) => (x.open = o)), opened); await page.waitForTimeout(300);
          for (const x of [...await frame.evaluate(audit), ...(extra ? await page.evaluate(extra) : [])]) {
            if (!found.has(x)) found.set(x, []);
            found.get(x).push(`${w}x${h} ${mode} ${ui}${opened ? " open" : ""}`);
          }
        }
      }
    }
    await frame.$$eval("#app details", (d) => d.forEach((x) => (x.open = false)));
  }
  return [...found].map(([k, v]) => `${k}  (${v.length}x, e.g. ${v[0]})`);
}

test("13 window sizes, both modes, Basic and Advanced, sections closed and open", async ({ page, problems }) => {
  test.setTimeout(900_000);
  await open(page);
  await runBoard(page, BOARD);
  expect(await sweep(page, page.mainFrame(), SIZES)).toEqual([]);
});

test("in the blog's frame (another site), at three sizes", async ({ page, problems, baseURL }) => {
  test.setTimeout(900_000);
  // the blog page as Blogger serves it (BloggerPage.html), on another origin, framing this build.  Chrome asks before
  // a site it takes for public may frame 127.0.0.1 (Local Network Access): the test says yes.  The real blog and
  // github.io are both public, so visitors never meet that question.
  await page.context().grantPermissions(["local-network-access"]);
  const blog = readFileSync(join(HERE, "..", "BloggerPage.html"), "utf8").replace(/var APP_URL = "[^"]*";/, `var APP_URL = "${baseURL}";`);
  await page.context().route("http://localhost:8899/**", (r) => r.fulfill({ contentType: "text/html", body: `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head><body><header>blog header</header><main>${blog}</main></body></html>` }));
  await page.goto("http://localhost:8899/");
  await page.waitForSelector("#kese-frame");
  await expect.poll(() => page.frames().some((f) => f.url().startsWith(baseURL)), { timeout: 30_000 }).toBe(true);
  const frame = page.frames().find((f) => f.url().startsWith(baseURL));   // the frame once it shows the tool
  await pythonReady(frame);
  await runBoard(frame, BOARD);
  expect(await frame.evaluate(() => document.documentElement.classList.contains("embedded"))).toBe(true);
  const blogFits = () => { const o = [], W = document.documentElement.clientWidth; if (document.documentElement.scrollWidth > W + 1) o.push("blog page scrolls sideways"); const fr = document.getElementById("kese-frame").getBoundingClientRect(); if (fr.right > W + 1) o.push("frame wider than the page"); return o; };
  expect(await sweep(page, frame, [[1440, 900], [1280, 720], [1080, 1920]], blogFits)).toEqual([]);
});
