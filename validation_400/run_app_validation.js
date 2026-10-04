// Drives the REAL app (index.html) screen by screen for each synthetic patient,
// at iPhone 13 Pro Max size, and records exactly what the app displays.
// Output: app_results.json
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const cases = JSON.parse(fs.readFileSync(path.join(__dirname, 'cases.json')));
const APP = 'file://' + (process.env.SAB_APP || path.resolve(__dirname, '..', 'index.html'));

// Runs 4 phone windows side by side; "reduced motion" skips the slide animations to save time.
async function runBatch(browser, batch, out, pageErrors) {
  const ctx = await browser.newContext({ viewport: { width: 428, height: 926 }, isMobile: true, hasTouch: true, locale: 'en-US', reducedMotion: 'reduce' });
  const page = await ctx.newPage();
  page.setDefaultTimeout(5000);
  page.on('pageerror', e => pageErrors.push(e.message));

  const tap = sel => page.click(sel);
  const pick = (key, val) => tap(`[data-set="${key}"][data-val='${JSON.stringify(val)}']`);
  const stepName = () => page.textContent('.step-label');
  const next = async (where) => {
    if (await page.isDisabled('#nextBtn')) throw new Error('Continue disabled at ' + where);
    await tap('#nextBtn');
  };

  for (const c of batch) {
    const r = { id: c.id, error: null };
    try {
      await page.goto(APP);
      // Step 1 — patient
      await pick('adult', true); await pick('saConfirmed', true); await next('patient');
      // Step 2 — initial evaluation results
      await pick('fubc48', c.fubc48); await pick('tte', c.tte); await next('initial');
      // Step 3 — key factors
      await pick('community', c.community); await pick('device', c.device); await next('key');
      // Step 4 — other factors
      if (c.other.length) { for (const f of c.other) await tap(`[data-toggle="other"][data-id="${f}"]`); }
      else await tap('[data-none="1"]');
      await next('other');
      // Step 5 — risk & workup: read what the app shows
      r.riskText = (await page.textContent('.result h2')).trim();
      r.advice = await page.$$eval('.adv b', els => els.map(e => e.textContent.trim()));
      await next('risk');
      // Step 6 — workup results (only if the app shows it)
      r.results_screen = (await stepName()).includes('Workup results');
      if (r.results_screen) {
        await pick('focus', c.focus);
        if (c.focus === 'no') {
          await pick('resolved', c.resolved); await pick('workupComplete', c.workupComplete);
          for (const l of c.longer) await tap(`[data-toggle="longer"][data-id="${l}"]`);
        }
        await next('results');
      }
      // Step 7 — plan
      if (!(await stepName()).includes('Plan')) throw new Error('Did not reach Plan');
      r.classText = (await page.textContent('.result h2')).trim();
      r.durNum = await page.$eval('.duration .num', e => e.textContent.trim()).catch(() => null);
      r.durUnit = await page.$eval('.duration .unit', e => e.textContent.trim()).catch(() => null);
      r.flags = await page.$$eval('.result .factors span', els => els.map(e => e.textContent.trim()));
      if (await page.$('#clr')) {
        await page.fill('#clr', c.clearDate); await page.dispatchEvent('#clr', 'change');
        if (c.sourceDate) { await page.fill('#src', c.sourceDate); await page.dispatchEvent('#src', 'change'); }
        r.dates = await page.$$eval('.calc-out b', els => els.map(e => e.textContent.trim()));
      }
    } catch (e) { r.error = e.message; }
    out.push(r);
  }
  await ctx.close();
}

(async () => {
  const browser = await chromium.launch();
  const out = [], pageErrors = [];
  const W = 4, batches = Array.from({ length: W }, (_, i) => cases.filter((_, k) => k % W === i));
  await Promise.all(batches.map(b => runBatch(browser, b, out, pageErrors)));
  out.sort((a, b) => a.id.localeCompare(b.id));
  fs.writeFileSync(path.join(__dirname, 'app_results.json'), JSON.stringify(out, null, 1));
  console.log('ran', out.length, 'cases; page errors:', pageErrors.length, '; flow errors:', out.filter(x => x.error).length);
  await browser.close();
})();
