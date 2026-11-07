// inputs.spec.mjs - what a visitor can get wrong: files that are not boards, broken boards, broken parameter files,
// numbers typed wrong.  Each one gets a clear message that fits the window, no crash dialog, and the page keeps working.
import { test, expect, open, runBoard, result, QUICK, HERE } from "../helpers.mjs";
import { mkdtempSync, writeFileSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const dir = mkdtempSync(join(tmpdir(), "kese-bad-"));
const file = (name, body) => { const p = join(dir, name); writeFileSync(p, body); return p; };
const toast = (page) => page.evaluate(() => { const t = document.getElementById("toast"); if (t.hidden) return null; const r = t.getBoundingClientRect(); return { text: t.textContent, fits: r.left >= 0 && r.right <= innerWidth && r.bottom <= innerHeight }; });
async function expectToast(page, re) {
  await page.waitForFunction(() => !document.getElementById("toast").hidden, null, { timeout: 15_000 });
  const t = await toast(page);
  expect(t.text).toMatch(re);
  expect(t.fits, `toast fits the window: "${t.text}"`).toBe(true);
  await page.evaluate(() => { document.getElementById("toast").hidden = true; });
}

test.describe("at 1024 x 768", () => {
  test.use({ viewport: { width: 1024, height: 768 } });

  test("files that are not boards are refused with a message", async ({ page, problems }) => {
    await open(page);
    await page.setInputFiles("#board-file", file("schematic.kicad_pcb", "(kicad_sch (version 1))\n"));
    await expectToast(page, /does not look like a KiCad board/);
    await page.setInputFiles("#board-file", file("notes.txt", "hello"));
    await expectToast(page, /not a \.kicad_pcb file/);
    await page.setInputFiles("#board-file", file("empty.kicad_pcb", ""));
    await expectToast(page, /does not look like a KiCad board/);
    await expect(page.locator("#crash-dialog")).toBeHidden();
    await runBoard(page, QUICK);                                // and a good board still works
    expect((await result(page)).download).toBe(true);
  });

  test("a board cut in half is not made, says why, and the next board works", async ({ page, problems }) => {
    await open(page);
    const text = readFileSync(QUICK, "utf8");
    await runBoard(page, file("half.kicad_pcb", text.slice(0, Math.floor(text.length / 2))));
    const r = await result(page);
    expect(r.counts).toMatch(/Not Generated/);
    expect(r.errors.length).toBeGreaterThan(0);
    expect(r.download).toBe(false);
    await expect(page.locator("#crash-dialog")).toBeHidden();
    await runBoard(page, QUICK);
    expect((await result(page)).counts).toMatch(/Warning|No Warnings/);
  });

  test("broken parameter files are refused with a message", async ({ page, problems }) => {
    await open(page);
    const cases = [
      [file("notes.txt", "hello world\n"), /No parameter values found|No settings/],
      [file("broken.zip", "not a zip"), /could not be read/],
      [file("run.py", "x = (\n"), /could not be read/],
      [file("long_ignored.txt", "[parameters/run.py]\n" + Array.from({ length: 40 }, (_, i) => `OLD_SETTING_NUMBER_${i} = ${i}`).join("\n") + '\nUNITS = "mm"\n'), /Loaded 1 value.*Ignored.*and \d+ more/],
    ];
    // a parameter file far too big, and a zip whose member unpacks to 6 MB (a zip bomb's trick)
    cases.push([file("huge.txt", Buffer.alloc(21 * 1048576, 32)), /too big for a parameter file/]);
    cases.push([join(HERE, "fixtures", "bomb.zip"), /could not be read.*too big for a parameter file/]);   // 6 KB, 6 MB unpacked
    for (const [f, re] of cases) {
      await page.setInputFiles("#import-file", f);
      await expectToast(page, re);
    }
    await expect(page.locator("#crash-dialog")).toBeHidden();
  });

  test("numbers: commas, spaces and exponents are read, words are refused", async ({ page, problems }) => {
    await open(page);
    await page.$eval("#sections details[data-module=Copper]", (d) => (d.open = true));
    const sel = '.field[data-key="Copper.VIA_WALL_MM"] .stepper input';
    for (const [typed, shown, msg] of [["1,5", "1.5", null], ["abc", "1.5", /"abc" is not a number/], ["12abc", "1.5", /not a number/], [" 0.5 ", "0.5", null], ["1e-3", "0.001", null], ["0.0250", "0.025", null]]) {
      await page.fill(sel, typed); await page.press(sel, "Enter"); await page.waitForTimeout(250);
      expect(await page.inputValue(sel), `typed ${JSON.stringify(typed)}`).toBe(shown);
      if (msg) await expectToast(page, msg); else expect(await toast(page)).toBeNull();
    }
    await page.focus(sel); await page.keyboard.press("ArrowUp"); await page.waitForTimeout(200);
    expect(await page.inputValue(sel)).toBe("0.026");             // one step (0.001) up from the last value
    await page.click('.field[data-key="Copper.VIA_WALL_MM"] .stepper button[aria-label=More]'); await page.waitForTimeout(200);
    expect(await page.inputValue(sel)).toBe("0.027");
  });

  test("a value the generator refuses ends as Not Generated with its reason", async ({ page, problems }) => {
    await open(page);
    await page.$eval("#sections details[data-module=Copper]", (d) => (d.open = true));
    const sel = '.field[data-key="Copper.VIA_WALL_MM"] .stepper input';
    await page.fill(sel, "-0.01"); await page.press(sel, "Enter");
    await runBoard(page, QUICK);
    const r = await result(page);
    await expect(page.locator("#crash-dialog")).toBeHidden();
    // either refused with a reason, or made with a warning about it: never a silent model
    if (/Not Generated/.test(r.counts)) expect(r.errors.join(" ")).toMatch(/VIA_WALL|via wall|wall/i);
    else expect(r.counts).toMatch(/Warning/);
  });
});
