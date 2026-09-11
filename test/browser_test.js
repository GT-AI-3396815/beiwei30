const path = require("path");
const pwDir = path.join(__dirname, "node_modules", "agent-browser", "node_modules", "playwright-core");
let chromium;
try { chromium = require(pwDir).chromium; }
catch (e) { chromium = require("playwright-core").chromium; }

(async () => {
  let browser;
  for (const exe of ["C:/Program Files/Google/Chrome/Application/chrome.exe", "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"]) {
    try { browser = await chromium.launch({ headless: true, executablePath: exe }); break; } catch (e) { /* try next */ }
  }
  if (!browser) throw new Error("No Chrome/Edge found");
  const errors = [];
  const consoleMsgs = [];
  const failedRequests = [];
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  page.on("pageerror", (e) => errors.push("PAGEERROR: " + e.message));
  page.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") consoleMsgs.push(m.type().toUpperCase() + ": " + m.text().slice(0, 200)); });
  page.on("requestfailed", (r) => failedRequests.push(r.url() + " -> " + (r.failure() || {}).errorText));
  page.on("response", (r) => { if (r.status() >= 400) failedRequests.push(r.url() + " -> HTTP " + r.status()); });

  const results = {};
  const BASE = process.env.BASE_URL || "http://127.0.0.1:8093/";
  for (const [label, url] of [["root", BASE], ["indexHtml", BASE + "index.html"]]) {
    const p = await browser.newPage({ viewport: { width: 1280, height: 900 } });
    p.on("pageerror", (e) => errors.push(label + " PAGEERROR: " + e.message));
    p.on("console", (m) => { if (m.type() === "error" || m.type() === "warning") consoleMsgs.push(label + " " + m.type().toUpperCase() + ": " + m.text().slice(0, 200)); });
    p.on("requestfailed", (r) => failedRequests.push(r.url() + " -> " + (r.failure() || {}).errorText));
    p.on("response", (r) => { if (r.status() >= 400) failedRequests.push(r.url() + " -> HTTP " + r.status()); });
    await p.goto(url, { waitUntil: "load", timeout: 30000 });
    await p.waitForTimeout(3500);
    // wait until all images complete (max 15s) so slow networks don't false-positive brokenImgs
    await p.evaluate(() => Promise.race([
      Promise.all(Array.from(document.querySelectorAll("img")).map((i) => i.complete ? Promise.resolve() : new Promise((res) => { i.onload = i.onerror = res; }))),
      new Promise((res) => setTimeout(res, 15000)),
    ]));
    await p.waitForTimeout(300);
    results[label] = await p.evaluate(() => ({
      bodyHeight: document.body.scrollHeight,
      rootChildren: document.getElementById("root") ? document.getElementById("root").children.length : -1,
      textLen: document.body.innerText.length,
      textSample: document.body.innerText.replace(/\s+/g, " ").slice(0, 200),
      imgCount: document.querySelectorAll("img").length,
      brokenImgs: Array.from(document.querySelectorAll("img")).filter((i) => !i.complete || i.naturalWidth === 0).length,
      sectionCount: document.querySelectorAll("section,header,footer").length,
      linkCount: document.querySelectorAll("a").length,
    }));
    if (label === "root") await p.screenshot({ path: __dirname + "/../test-desktop.png", fullPage: false });
    await p.close();
  }

  // mobile viewport test
  const mp = await browser.newPage({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  mp.on("pageerror", (e) => errors.push("MOBILE PAGEERROR: " + e.message));
  await mp.goto((process.env.BASE_URL || "http://127.0.0.1:8093/") + "index.html", { waitUntil: "load", timeout: 30000 });
  await mp.waitForTimeout(3000);
  const minfo = await mp.evaluate(() => ({
    rootChildren: document.getElementById("root") ? document.getElementById("root").children.length : -1,
    bodyHeight: document.body.scrollHeight,
    hOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 2,
  }));
  await mp.screenshot({ path: __dirname + "/test-mobile.png", fullPage: false });

  // dup, errors, consoleMsgs: consoleMsgs.slice(0, 20), failedRequests }, null, 2));
  console.log(JSON.stringify({ results, minfo, errors, consoleMsgs: consoleMsgs.slice(0, 20), failedRequests }, null, 2)); await browser.close();
})().catch((e) => { console.error("FATAL:", e.message); process.exit(1); });
