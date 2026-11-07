// helpers.mjs - what every spec shares: jsDelivr replaced by the built vendor/ copy, the page's errors and CSP
// violations collected (a test fails on any it did not expect), and waits for Python and for a run.
import { test as base, expect } from "@playwright/test";
import { readFileSync, existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export const HERE = dirname(fileURLToPath(import.meta.url));
export const SITE = join(HERE, ".site", "WebUI");
export const REPO = resolve(HERE, "..", "..");
export const FEATURE_BOARDS = join(REPO, "featureTest");
export const EXAMPLES = join(REPO, "Generator", "Input");
export const QUICK = join(FEATURE_BOARDS, "14_stackup_full.kicad_pcb");     // a full stack-up, made in about 5 s
export const LIVE = process.env.KESE_LIVE_URL || "";               // the published site (live.spec.mjs after a deploy)
if (!LIVE && !existsSync(join(SITE, "webui.json"))) throw new Error("Build the site first: npm run build (python3 ../build_site.py .site)");
export const CFG = JSON.parse(readFileSync(LIVE ? join(HERE, "..", "webui.json") : join(SITE, "webui.json"), "utf8"));
export const VENDOR = JSON.parse(readFileSync(join(HERE, "..", "vendor.json"), "utf8"));

const TYPES = { js: "text/javascript", mjs: "text/javascript", wasm: "application/wasm", json: "application/json", zip: "application/zip", whl: "application/zip" };
const CORS = { "Access-Control-Allow-Origin": "*", "Cache-Control": "no-cache" };

/* jsDelivr as the tests see it:
     local    served from the build's vendor/ copy (the same bytes, checked against vendor.json): the default
     abort    refused at once (blocked by a firewall, DNS failure)
     stall    never answers (a hanging connection): the page must switch after webui.json cdnWaitSeconds
     tamper   three.module.js changed by one comment: the import map's integrity must refuse it
     real     the real jsDelivr (needs internet; @network tests only)
   "abort-pyodide" / "stall-pyodide": only Pyodide's folder fails, three.js is served. */
async function routeCdn(context, mode, seen) {
  if (mode === "real") return;
  const [kind, only] = mode.split("-");
  for (const name of ["pyodide", "three"]) {
    const prefix = CFG[name], fails = !only || only === name;
    await context.route(`${prefix}**`, async (route) => {
      const url = route.request().url(), path = url.slice(prefix.length).split("?")[0];
      seen.push(url);
      if (kind === "abort" && fails) return route.abort("connectionrefused");
      if (kind === "stall" && fails) return;                 // never fulfilled: the request hangs
      const file = join(SITE, "vendor", name, path);
      if (!existsSync(file)) return route.fulfill({ status: 404, headers: CORS, body: "not in vendor/" });
      let body = readFileSync(file);
      if (kind === "tamper" && path === "build/three.module.js") body = Buffer.concat([body, Buffer.from("\n// changed\n")]);
      const ext = path.split(".").pop();
      return route.fulfill({ status: 200, headers: { ...CORS, "Content-Type": TYPES[ext] || "application/octet-stream" }, body });
    });
  }
}

// errors the browser itself logs for a request a test made fail on purpose (not the page's fault)
const EXPECTED = [/Failed to load resource/i, /ERR_CONNECTION_REFUSED|ERR_FAILED|NetworkError|Load failed|network connection was lost|Could not connect/i,
  /integrity/i, /Failed to fetch dynamically imported module|error loading dynamically imported module|Importing a module script failed/i,
  /Cross-Origin Request Blocked|CORS request did not succeed/i];

export const test = base.extend({
  cdn: [LIVE ? "real" : "local", { option: true }],
  cdnRequests: async ({}, use) => { await use([]); },
  context: async ({ context, cdn, cdnRequests }, use) => {
    await routeCdn(context, cdn, cdnRequests);
    await use(context);
  },
  // every page error and console error, and every CSP violation the page reports; checked after the test
  problems: async ({ page, cdn }, use, testInfo) => {
    const problems = [];
    const expected = (t) => cdn !== "local" && cdn !== "real" && EXPECTED.some((re) => re.test(t));
    page.on("pageerror", (e) => { if (!expected(e.message)) problems.push(`pageerror: ${e.message}`); });
    page.on("console", (m) => {
      if (m.type() !== "error") return;
      const t = m.text();
      if (expected(t)) return;
      problems.push(`console: ${t.slice(0, 300)}`);
    });
    await page.addInitScript(() => {
      window.__csp = [];
      document.addEventListener("securitypolicyviolation", (e) => window.__csp.push(`${e.violatedDirective} ${e.blockedURI} ${e.sourceFile || ""}:${e.lineNumber || ""}`));
    });
    await use(problems);
    const csp = await page.evaluate(() => window.__csp || []).catch(() => []);
    for (const v of csp) problems.push(`CSP violation: ${v}`);
    const allowed = testInfo.annotations.filter((a) => a.type === "allow").map((a) => new RegExp(a.description));
    const left = problems.filter((p) => !allowed.some((re) => re.test(p)));
    expect(left, "page errors, console errors or CSP violations").toEqual([]);
  },
});
export { expect };

export const generateIdle = (page) => page.waitForFunction(() => {
  const g = document.getElementById("btn-generate");
  return g && g.textContent.trim() === "Generate" && !document.getElementById("progress").classList.contains("busy") && document.getElementById("run-card").hidden;
}, null, { timeout: 600_000, polling: 250 });

// Python loaded (the page says "Generate", or waits for a board)
export async function pythonReady(page, timeout = 180_000) {
  await page.waitForFunction(() => {
    const g = document.getElementById("btn-generate");
    return g && (g.textContent.trim() === "Generate") && document.querySelector("#sections details");
  }, null, { timeout, polling: 250 });
}

export async function open(page, query = "") {
  await page.goto(query);
  await pythonReady(page);
}

// choose a board as a visitor does (the file input), wait for its run and its preview to finish
export async function runBoard(page, file) {
  await page.setInputFiles("#board-file", file);
  await page.waitForFunction(() => document.getElementById("progress").classList.contains("busy"), null, { timeout: 30_000, polling: 50 });
  await generateIdle(page);
  await page.waitForFunction(() => !/Reading|Loading/.test(document.getElementById("readout").textContent), null, { timeout: 120_000, polling: 250 });
}

export async function result(page) {
  return page.evaluate(() => {
    const t = (s) => (document.querySelector(s)?.textContent || "").trim().replace(/\s+/g, " ");
    return {
      counts: t("#counts"), note: t("#run-note"), readout: t("#readout"), board: t("#board-name"),
      parts: document.querySelectorAll("#parts button.part").length, chips: document.querySelectorAll("#download-files button").length,
      download: !document.getElementById("btn-download").disabled, stale: !document.getElementById("stale-badge").hidden,
      webgl: !document.getElementById("canvas-wrap").classList.contains("no-webgl"),
      errors: [...document.querySelectorAll("#checks-list .check.error .msg")].map((e) => e.textContent.trim()),
    };
  });
}
