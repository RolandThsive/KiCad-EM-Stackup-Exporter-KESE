// pages.spec.mjs - the footer's pages: Privacy and Licences open from the footer, keep their own strict CSP, every
// licence text they link exists, and the versions they name are the ones the page really loads.
import { test, expect, open, CFG, VENDOR } from "../helpers.mjs";

for (const [link, file] of [["Privacy", "privacy.html"], ["Licences", "licenses.html"]]) {
  test(`${link} opens from the footer, with no error or CSP violation`, async ({ page, problems }) => {
    await open(page);
    const [tab] = await Promise.all([page.waitForEvent("popup"), page.click(`#foot a:text-is("${link}")`)]);
    await tab.waitForLoadState();
    expect(new URL(tab.url()).pathname).toMatch(new RegExp(`/WebUI/${file}$`));
    expect(await tab.getAttribute('meta[http-equiv="Content-Security-Policy"]', "content")).toContain("default-src 'none'");
    const errs = [];
    tab.on("console", (m) => { if (m.type() === "error") errs.push(m.text()); });
    await tab.reload();
    expect(await tab.locator("h1").textContent()).toBe(link);
    expect(errs).toEqual([]);
    await tab.close();
  });
}

test("every licence text linked exists, and the versions match what is loaded", async ({ page, request }) => {
  await page.goto("licenses.html");
  const hrefs = await page.$$eval('a[href^="licenses/"]', (a) => a.map((x) => x.href));
  expect(hrefs.length).toBeGreaterThan(8);
  for (const h of new Set(hrefs)) expect((await request.get(h)).status(), h).toBe(200);
  const text = await page.textContent("table");
  const pyodide = CFG.pyodide.match(/\/v([\d.]+)\//)[1], three = CFG.three.match(/three@([\d.]+)\//)[1];
  expect(text).toContain(pyodide);
  expect(text).toContain(three);
  for (const wheel of Object.keys(VENDOR.pyodide.files).filter((f) => f.endsWith(".whl"))) {
    const [name, version] = wheel.split("-");
    expect(text.toLowerCase(), `${name} ${version} in licenses.html`).toContain(version);
  }
});

test("the privacy page names every server the page talks to", async ({ page }) => {
  await page.goto("privacy.html");
  const text = await page.textContent("main");
  expect(text).toContain("GitHub Pages");
  expect(text).toContain("jsDelivr");
  expect(text).toMatch(/no request goes to Google Fonts/);
  expect(text).toContain("kese-three-backup");                  // the one storage key the page sets
});

// ASVS 13.4.1: the site holds the page's files only, not the project's notes, tests, tools or build inputs
test("the project's notes, tests and tools are not published", async ({ request }) => {
  for (const path of ["docs/ASVS-L1.md", "docs/WCAG-EM.md", "README.md", "CHANGELOG.md", "tests/helpers.mjs", "tools/vendor_lock.py",
    "vendor.json", "build_site.py", "BloggerPage.html", ".gitignore"])
    expect((await request.get(path)).status(), path).toBe(404);
});
