// security.spec.mjs - the page's defences: the Content-Security-Policy, the ?pyodide= lock, the backup copy when
// jsDelivr is refused, silent or serves a changed file, the crash dialog and Report a Problem (never the board).
import { test, expect, open, runBoard, result, CFG, QUICK } from "../helpers.mjs";
import { join } from "node:path";
import { copyFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";

const WAIT = (CFG.cdnWaitSeconds || 15) * 1000;
const footTip = (page) => page.evaluate(() => document.querySelector("#foot .build")?.dataset.tip || "");

test("the CSP allows no inline script, eval or plug-in, and blocks an injected script", async ({ page, problems }) => {
  test.info().annotations.push({ type: "allow", description: "CSP violation: script-src|Refused to execute inline script|Content.Security.Policy" });
  await open(page);
  const csp = await page.getAttribute('meta[http-equiv="Content-Security-Policy"]', "content");
  expect(csp).toContain("default-src 'self'");
  expect(csp).toContain("object-src 'none'");
  expect(csp).not.toMatch(/unsafe-inline|unsafe-eval|\*/);
  // an inline script someone manages to inject does not run
  const ran = await page.evaluate(() => { window.__ran = false; const s = document.createElement("script"); s.textContent = "window.__ran = true"; document.body.append(s); return window.__ran; });
  expect(ran).toBe(false);
  expect(await page.evaluate(() => window.__csp.length)).toBeGreaterThan(0);
});

test("talks to no server but this site and jsDelivr (no fonts or trackers)", async ({ page, problems }) => {
  const hosts = new Set();
  page.context().on("request", (r) => hosts.add(new URL(r.url()).host));
  await open(page);
  await runBoard(page, QUICK);
  const own = new URL(page.url()).host;
  expect([...hosts].filter((h) => h !== own && h !== "cdn.jsdelivr.net")).toEqual([]);
});

test("?pyodide= is taken only from this site", async ({ page, problems, cdnRequests }) => {
  const asked = [];
  await page.context().route("https://evil.example/**", (r) => { asked.push(r.request().url()); return r.abort(); });
  await open(page, "?pyodide=https://evil.example/py/");
  expect(asked).toEqual([]);
  expect(cdnRequests.some((u) => u.endsWith("pyodide.mjs"))).toBe(true);
  expect(await footTip(page)).toContain("Python from jsDelivr");
});

test.describe("jsDelivr refused", () => {
  test.use({ cdn: "abort" });
  test("everything comes from the backup copy, at once", async ({ page, problems }) => {
    const t0 = Date.now();
    await open(page);
    expect(Date.now() - t0).toBeLessThan(WAIT);                 // no waiting: a refusal is an answer
    expect(await page.evaluate(() => window.KESE_THREE)).toBe("backup");
    expect(await footTip(page)).toMatch(/Python from this site's backup copy · three.js from this site's backup copy/);
    await runBoard(page, QUICK);
    expect((await result(page)).download).toBe(true);
  });
});

test.describe("jsDelivr silent", () => {
  test.use({ cdn: "stall" });
  test(`the page switches to the backup after ${WAIT / 1000} s, once`, async ({ page, problems }) => {
    const t0 = Date.now();
    await open(page);
    const took = Date.now() - t0;
    expect(took).toBeGreaterThanOrEqual(WAIT - 500);
    expect(took).toBeLessThan(WAIT * 2 - 2000);                 // Python does not wait a second time
    expect(await footTip(page)).toMatch(/Python from this site's backup copy · three.js from this site's backup copy/);
  });
});

test.describe("only Pyodide's folder silent", () => {
  test.use({ cdn: "stall-pyodide" });
  test(`Python switches after ${WAIT / 1000} s, three.js stays on jsDelivr`, async ({ page, problems }) => {
    const t0 = Date.now();
    await open(page);
    expect(Date.now() - t0).toBeGreaterThanOrEqual(WAIT - 500);
    expect(await footTip(page)).toMatch(/Python from this site's backup copy · three.js from jsDelivr/);
  });
});

test.describe("only Pyodide's folder refused", () => {
  test.use({ cdn: "abort-pyodide" });
  test("Python comes from the backup at once", async ({ page, problems }) => {
    const t0 = Date.now();
    await open(page);
    expect(Date.now() - t0).toBeLessThan(WAIT);
    expect(await footTip(page)).toMatch(/Python from this site's backup copy · three.js from jsDelivr/);
  });
});

test.describe("jsDelivr serves a changed three.js", () => {
  test.use({ cdn: "tamper" });
  test("the browser refuses it and the page reloads on the backup", async ({ page, problems }) => {
    await open(page);
    expect(await page.evaluate(() => window.KESE_THREE)).toBe("backup");
    expect(await page.evaluate(() => sessionStorage.getItem("kese-three-backup"))).toBe("1");
  });
});

// The errors are raised as the browser raises them for the page's own scripts (an ErrorEvent from this site, an
// unhandled rejection); a script injected by the test would count as foreign (Firefox and WebKit name it eval code).
const raise = (page, message) => page.evaluate((m) => window.dispatchEvent(new ErrorEvent("error", { message: m, filename: new URL("WebUI.js", location.href).href, lineno: 1, error: new Error(m) })), message);
test("an error nobody caught opens the crash dialog, with details and a report link", async ({ page, problems }) => {
  await open(page);
  await raise(page, "test crash");
  const d = page.locator("#crash-dialog");
  await expect(d).toBeVisible();
  await expect(page.locator("#crash-details")).toContainText("test crash");
  const href = await page.getAttribute("#crash-report", "href");
  expect(href).toMatch(/\/issues\/new\?title=/);
  expect(decodeURIComponent(href)).toContain("test crash");
  await d.locator("button[value=close]").click();
  await expect(d).toBeHidden();
  // a second error does not open it again: it is added to the details
  await page.evaluate(() => window.dispatchEvent(new PromiseRejectionEvent("unhandledrejection", { promise: Promise.resolve(), reason: new Error("test rejection") })));
  await page.waitForTimeout(300);
  await expect(d).toBeHidden();
  await expect(page.locator("#crash-details")).toContainText("test rejection");
});

test("errors of other sites and browser extensions are left alone", async ({ page, problems }) => {
  await open(page);
  await page.evaluate(() => {
    window.dispatchEvent(new ErrorEvent("error", { message: "extension", filename: "chrome-extension://abc/content.js", error: new Error("extension") }));
    window.dispatchEvent(new ErrorEvent("error", { message: "Script error.", filename: "" }));
    window.dispatchEvent(new ErrorEvent("error", { message: "ResizeObserver loop completed with undelivered notifications.", filename: location.href }));
  });
  await page.waitForTimeout(300);
  await expect(page.locator("#crash-dialog")).toBeHidden();
});

test("Report a Problem says the build, browser and changed settings, never the board", async ({ page, problems }) => {
  await open(page);
  const dir = mkdtempSync(join(tmpdir(), "kese-"));
  const secret = join(dir, "SecretCustomerBoard_X9.kicad_pcb");
  copyFileSync(QUICK, secret);
  await page.click("#verify-row .switch");                    // one setting changed from the defaults
  await runBoard(page, secret);
  let opened = "";                                            // GitHub is not contacted: the link is caught
  await page.context().route("https://github.com/**", (r) => { opened = r.request().url(); return r.fulfill({ body: "caught" }); });
  const [popup] = await Promise.all([page.waitForEvent("popup"), page.click("#report-link")]);
  await popup.close();
  const url = decodeURIComponent(opened);
  expect(url).toContain("/issues/new");
  expect(url).toMatch(/build \w+/);
  expect(url).toContain("Verifier.VERIFY=");
  expect(url).not.toContain("SecretCustomerBoard");
  expect(url).not.toContain("kicad_pcb");
});

test.describe("real jsDelivr @network", () => {
  test.use({ cdn: "real" });
  test("Python and three.js load from jsDelivr, the integrity checks pass", async ({ page, problems }) => {
    await open(page);
    expect(await page.evaluate(() => window.KESE_THREE)).toBe("cdn");
    expect(await footTip(page)).toMatch(/Python from jsDelivr · three.js from jsDelivr/);
  });
});
