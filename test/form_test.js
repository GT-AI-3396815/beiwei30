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

  const report = { steps: [], formPost: null, formResponse: null, localStorage: null, successText: false };
  const BASE = process.env.BASE_URL || "http://127.0.0.1:8093/";
  await page.goto(BASE + "index.html", { waitUntil: "load", timeout: 30000 });
  await page.waitForTimeout(3000);

  // jump to register section
  await page.evaluate(() => {
    const el = document.querySelector("#register") || Array.from(document.querySelectorAll("section")).find((s) => s.textContent.includes("全球万名儿童"));
    if (el) el.scrollIntoView();
  });
  await page.waitForTimeout(1200);

  // Step 1: basic info
  await page.fill('input[placeholder="请输入孩子姓名"]', "测试小星");
  await page.selectOption('select:has(option:text-is("请选择年龄"))', { label: "8" }).catch(async () => {
    // fallback: choose by index if label differs
    const sel = await page.$('select');
    if (sel) await sel.selectOption({ index: 3 }).catch(() => {});
  });
  await page.fill('input[placeholder="请输入监护人姓名"]', "测试家长");
  await page.fill('input[placeholder="请输入联系电话"]', "13800000000");
  await page.fill('input[placeholder="请输入电子邮箱"]', "test@example.com").catch(() => {});
  report.steps.push("info-filled");
  // click 下一步
  await page.evaluate(() => {
    const b = Array.from(document.querySelectorAll("button")).find((x) => (x.textContent || "").includes("下一步"));
    if (b) b.click();
  });
  await page.waitForTimeout(1000);
  report.steps.push("step2=" + await page.evaluate(() => document.body.innerText.includes("点击上传")));

  // Step 2: works (decorative upload) -> 下一步
  await page.evaluate(() => {
    const b = Array.from(document.querySelectorAll("button")).find((x) => (x.textContent || "").includes("下一步"));
    if (b) b.click();
  });
  await page.waitForTimeout(1000);
  report.steps.push("step3=" + await page.evaluate(() => document.body.innerText.includes("孩子想说的话")));

  // Step 3: voice -> 下一步
  await page.evaluate(() => {
    const b = Array.from(document.querySelectorAll("button")).find((x) => (x.textContent || "").includes("下一步"));
    if (b) b.click();
  });
  await page.waitForTimeout(1000);
  report.steps.push("step4-confirm-visible=" + await page.evaluate(() => document.body.innerText.includes("确认提交报名")));

  // Step 4: submit — capture the network POST
  const reqPromise = page.waitForRequest((r) => r.url().includes("formsubmit.co"), { timeout: 15000 }).catch(() => null);
  const respPromise = page.waitForResponse((r) => r.url().includes("formsubmit.co"), { timeout: 20000 }).catch(() => null);
  await page.evaluate(() => {
    const b = Array.from(document.querySelectorAll("button")).find((x) => (x.textContent || "").includes("确认提交报名"));
    if (b) b.click();
  });
  const req = await reqPromise;
  report.formPost = req ? req.url() : null;
  if (req) report.formPostBody = (req.postData() || "").slice(0, 400);
  const resp = await respPromise;
  report.formResponse = resp ? resp.status() + " " + (await resp.text()).slice(0, 200) : null;
  await page.waitForTimeout(1500);

  report.successText = await page.evaluate(() => document.body.innerText.includes("已成功提交至组委会"));
  report.localStorage = await page.evaluate(() => localStorage.getItem("bw30_regs"));
  report.errors = errors;
  await page.screenshot({ path: path.join(__dirname, "..", "test-form-success.png") });
  console.log(JSON.stringify(report, null, 2));
  await browser.close();
})().catch((e) => { console.error("FATAL:", e.message); process.exit(1); });
