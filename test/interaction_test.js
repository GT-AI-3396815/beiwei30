const path = require("path");
let chromium;
try { chromium = require(path.join(__dirname, "node_modules", "agent-browser", "node_modules", "playwright-core")).chromium; }
catch (e) { chromium = require("playwright-core").chromium; }

(async () => {
  let browser;
  for (const exe of ["C:/Program Files/Google/Chrome/Application/chrome.exe", "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"]) {
    try { browser = await chromium.launch({ headless: true, executablePath: exe }); break; } catch (e) {}
  }
  if (!browser) throw new Error("No browser");
  const errors = [];
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  page.on("pageerror", (e) => errors.push("PAGEERROR: " + e.message));
  page.on("console", (m) => { if (m.type() === "error") errors.push("CONSOLE: " + m.text().slice(0, 150)); });
  await page.goto("http://127.0.0.1:8093/", { waitUntil: "load", timeout: 30000 });
  await page.waitForTimeout(3000);

  const report = {};
  // collect nav-like buttons
  const navTexts = await page.evaluate(() =>
    Array.from(document.querySelectorAll("nav button, nav a, header button, header a")).map((b) => b.textContent.trim()).filter(Boolean).slice(0, 20)
  );
  report.navTexts = navTexts;

  // click each nav item, measure scroll
  const navItems = await page.$$("nav button, nav a, header button, header a");
  report.scrollResults = [];
  for (const item of navItems) {
    const label = (await item.textContent() || "").trim();
    if (!label || label.length > 10) continue;
    const before = await page.evaluate(() => window.scrollY);
    await item.click().catch(() => {});
    await page.waitForTimeout(900);
    const after = await page.evaluate(() => window.scrollY);
    report.scrollResults.push({ label, before, after, scrolled: after !== before });
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(300);
  }

  // try the CTA "对话策展精灵"
  const cta = await page.evaluateHandle(() => {
    const els = Array.from(document.querySelectorAll("button, a, div[role=button]"));
    return els.find((e) => (e.textContent || "").includes("策展精灵") && !e.closest("nav") && !e.closest("header"));
  });
  if (cta && (await cta.evaluate((e) => !!e))) {
    await cta.click().catch(() => {});
    await page.waitForTimeout(1200);
    report.curatorDialog = await page.evaluate(() => {
      const txt = document.body.innerText;
      return { opened: !!document.querySelector("[class*=modal],[class*=dialog],[class*=chat],[class*=panel],[class*=drawer]") || (txt.includes("策展精灵") && txt.length > 2764), textLen: txt.length };
    });
    await page.screenshot({ path: path.join(__dirname, "..", "test-curator.png") });
  }

  // "立即报名" CTA
  const signup = await page.evaluateHandle(() => Array.from(document.querySelectorAll("button, a")).find((e) => (e.textContent || "").includes("立即报名") && !e.closest("nav")));
  if (signup && (await signup.evaluate((e) => !!e))) {
    await signup.click().catch(() => {});
    await page.waitForTimeout(1000);
    report.signupAfter = await page.evaluate(() => ({ scrollY: window.scrollY, textLen: document.body.innerText.length }));
  }

  report.errors = errors;
  console.log(JSON.stringify(report, null, 2));
  await browser.close();
})().catch((e) => { console.error("FATAL:", e.message); process.exit(1); });
