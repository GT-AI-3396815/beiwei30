# -*- coding: utf-8 -*-
"""fix_all.py — 北纬三十度站点 15 项内容/功能/合规修复
每一处替换都带出现次数断言，任何一处不匹配立即中止，不做半成品。
"""
import io, shutil, sys, os

BASE = r'C:\Users\AW\WorkBuddy\2026-09-07-22-49-44\beiwei30'
JS = BASE + r'\assets\index-DDzmKV-h.js'
CSS = BASE + r'\assets\index-DTPUeIxS.css'
HTML = BASE + r'\index.html'

# ---- 0. 备份 ----
for src in (JS, CSS, HTML):
    shutil.copy2(src, BASE + r'\test\backup_' + os.path.basename(src))
print('backup ok')

s = io.open(JS, encoding='utf-8').read()
orig_len = len(s)

CONTACT = 'hcsu3839@agent.qq.com'

# ---- 1. JS 文本替换（old, new, expected_count）----
R = []

# 1a. 报名表单：注入真实提交（FormSubmit AJAX → 智能体邮箱 + localStorage 兜底）
R.append((
    ',y=()=>{f(!0)},p=l.childName',
    (',y=()=>{const _d0={_subject:"【光体北纬三十度】新报名-"+(l.childName||"未填"),'
     '_captcha:"false",_template:"table",'
     '"孩子姓名":l.childName||"未填写","年龄":l.age||"未填写",'
     '"监护人姓名":l.guardianName||"未填写","联系电话":l.phone||"未填写",'
     '"电子邮箱":l.email||"未填写","所在地区":l.region||"未填写",'
     '"特殊需求":l.special==="yes"?"是-"+(l.specialType||""):"否",'
     '"作品":"3幅（审核通过后按邮件指引补传）","来源页":location.href};'
     'try{const _r0=JSON.parse(localStorage.getItem("bw30_regs")||"[]");'
     '_r0.push(Object.assign({time:new Date().toLocaleString("zh-CN")},_d0));'
     'localStorage.setItem("bw30_regs",JSON.stringify(_r0))}catch(_e0){}'
     'try{fetch("https://formsubmit.co/ajax/' + CONTACT + '",{method:"POST",'
     'headers:{"Content-Type":"application/json",Accept:"application/json"},'
     'body:JSON.stringify(_d0)}).catch(()=>{})}catch(_e1){}f(!0)},p=l.childName'),
    1))

# 1b. 作品上传说明：如实告知补传流程
R.append((
    '请上传3幅原创绘画作品（画种不限），围绕「爱」的主题创作。单幅作品不超过20MB。',
    '请准备3幅原创绘画作品（画种不限），围绕「爱」的主题创作，单幅高清图不超过20MB。线上报名先登记参展信息，作品高清图或原作将在审核通过后按邮件指引提交。',
    1))

# 1c. 报名成功文案：如实、给联系方式、给后续动作
R.append((
    '感谢您对「光体•北纬三十度觉醒之爱」公益艺术大展的关注！我们已收到您的报名信息，审核结果将在15个工作日内通过短信通知您。',
    '感谢您对「光体•北纬三十度觉醒之爱」公益艺术大展的关注！您的报名信息已成功提交至组委会，审核结果将在15个工作日内通过电话或邮件通知您；作品高清图或原作将在审核通过后按邮件指引提交。如有疑问，请联系 ' + CONTACT + '。',
    1))

# 1d. 策展精灵：去掉"AI"夸大表述，如实定位
R.append(('AI智能服务', '在线咨询助手', 1))
R.append((
    '您的专属AI策展顾问，7×24小时为您解答参展疑问，陪伴每个家庭完成这段艺术旅程',
    '常见问题即时解答助手，随时为您介绍参展流程、作品要求与公益保障机制，陪伴每个家庭完成这段艺术旅程',
    1))
R.append(('您好！我是您的专属AI策展精灵「小靈」', '您好！我是策展精灵「小靈」', 1))
R.append((
    '或访问「全球招募」板块直接报名。请问还有什么想了解的吗？',
    '或访问「全球招募」板块直接报名。请问还有什么想了解的吗？如需人工协助，可发送邮件至 ' + CONTACT + '，组委会会尽快回复。',
    1))

# 1e. 公益透明：目标/筹备中标注
R.append(('资金流向全景图', '资金流向全景图（目标规划 · 实际以公示数据为准）', 1))
R.append(('六大合规保障机制', '六大合规保障机制（随项目推进陆续上线）', 1))
R.append(('text-gradient-gold",children:"可追溯"', 'text-gradient-gold",children:"可追溯（公示体系筹备中）"', 1))
R.append(('可追溯**模式：', '可追溯**模式（以下为目标规划，公示体系随项目推进陆续上线）：', 1))

# 1f. 指导单位降调
R.append(('指导单位', '拟邀指导单位（确认中）', 1))

# 1g. 吉尼斯表述降调
R.append(('双项吉尼斯世界纪录挑战', '计划挑战双项吉尼斯世界纪录（申请推进中）', 1))
R.append(('吉尼斯双纪录挑战', '双项吉尼斯纪录挑战（申请中）', 1))
R.append(('吉尼斯认证主舞台', '吉尼斯纪录挑战主舞台（拟）', 2))
R.append(('吉尼斯收官点 · 公益捐赠仪式', '吉尼斯挑战收官点（拟）· 公益捐赠仪式', 1))
R.append((
    '每位参展儿童获得吉尼斯世界纪录官方参展荣誉证书，全球可查、终身有效，成为孩子终身的精神底气。',
    '若吉尼斯纪录挑战成功，每位参展儿童将获得吉尼斯官方参展荣誉证书（以吉尼斯官方认证结果为准），全球可查、终身有效，成为孩子终身的精神底气。',
    1))

# 1h. 页脚简介：光体品牌说明 + 吉尼斯降调 + 招募启动动态
R.append((
    '全球万名儿童100KM绿道公益艺术大展，以成都环城绿道为载体， 挑战双项吉尼斯世界纪录，用艺术搭建无国界的爱的桥梁。',
    '「光体」为本大展发起品牌，专注于儿童艺术教育与心灵成长公益。全球万名儿童100KM绿道公益艺术大展，以成都环城绿道为载体，计划挑战双项吉尼斯世界纪录（申请推进中），用艺术搭建无国界的爱的桥梁。全球招募通道已于2026年9月开启。',
    1))

# 1i. 页脚联系方式
R.append((
    '中国 · 成都 · 环城生态公园100KM绿道',
    '中国 · 成都 · 环城生态公园100KM绿道｜组委会咨询：' + CONTACT,
    1))

# 1j. 版权年份
R.append((
    '© 2027 光体•北纬三十度觉醒之爱组委会',
    '© 2026-2027 光体•北纬三十度觉醒之爱组委会（主办）',
    1))

# 1k. 数字展厅：如实标注上线节奏
R.append(('1:1 数字孪生', '1:1 数字孪生（作品征集后上线）', 1))
R.append((
    '十大主题段，全球最长儿童艺术展览线路的线上沉浸体验',
    '十大主题段规划预览 · 数字展厅将于作品征集完成后正式上线',
    1))

# 1l. 中英双语表述如实
R.append(('中英双语 · 全球可访问', '中文版已上线 · 英文版筹备中 · 全球可访问', 1))

# ---- 执行替换 + 断言 ----
fail = []
for old, new, cnt in R:
    c = s.count(old)
    if c != cnt:
        fail.append((old[:40], 'expect %d got %d' % (cnt, c)))
if fail:
    for f0 in fail:
        print('MISMATCH:', f0)
    sys.exit(1)
for old, new, cnt in R:
    s = s.replace(old, new)
io.open(JS, 'w', encoding='utf-8', newline='').write(s)
print('JS patched: %d replacements, %d -> %d chars' % (len(R), orig_len, len(s)))

# ---- 2. index.html：SEO + OG 分享卡片 ----
html = io.open(HTML, encoding='utf-8').read()
DESC = ('2027年六一，全球万名儿童以成都100KM环城绿道为展线，以「爱」为主题联袂创作，'
        '联动北纬30°沿线23个国家，计划挑战双项吉尼斯世界纪录。3-18周岁全球儿童零门槛报名中。')
og = (
    '<meta name="description" content="' + DESC + '" />\n'
    '    <meta name="keywords" content="儿童艺术展,公益艺术,北纬三十度,吉尼斯世界纪录,成都绿道,特殊儿童,自闭症儿童绘画,全球招募" />\n'
    '    <meta property="og:type" content="website" />\n'
    '    <meta property="og:site_name" content="光体•北纬三十度觉醒之爱" />\n'
    '    <meta property="og:title" content="光体•北纬三十度觉醒之爱 — 全球万名儿童100KM绿道公益艺术大展" />\n'
    '    <meta property="og:description" content="' + DESC + '" />\n'
    '    <meta property="og:image" content="https://gt-ai-3396815.github.io/beiwei30/logo.jpg" />\n'
    '    <meta property="og:url" content="https://gt-ai-3396815.github.io/beiwei30/" />\n'
    '    <meta property="og:locale" content="zh_CN" />\n'
    '    <meta name="twitter:card" content="summary" />\n'
    '    <meta name="twitter:title" content="光体•北纬三十度觉醒之爱 — 全球万名儿童100KM绿道公益艺术大展" />\n'
    '    <meta name="twitter:description" content="' + DESC + '" />\n'
    '    <meta name="twitter:image" content="https://gt-ai-3396815.github.io/beiwei30/logo.jpg" />'
)
old_desc = '<meta name="description" content="光体•北纬三十度觉醒之爱 — 全球万名儿童100KM绿道公益艺术大展" />'
assert html.count(old_desc) == 1, 'desc meta not found'
html = html.replace(old_desc, og)
io.open(HTML, 'w', encoding='utf-8', newline='').write(html)
print('HTML patched: OG/SEO added')

# ---- 3. CSS：无障碍（reduced motion + 键盘焦点可见）----
css = io.open(CSS, encoding='utf-8').read()
css += (
    '\n/* a11y: respect prefers-reduced-motion */\n'
    '@media (prefers-reduced-motion: reduce){*,*::before,*::after{animation-duration:.01ms!important;'
    'animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}\n'
    '/* a11y: visible keyboard focus */\n'
    'a:focus-visible,button:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible'
    '{outline:2px solid #c4956a;outline-offset:2px}\n'
)
io.open(CSS, 'w', encoding='utf-8', newline='').write(css)
print('CSS patched: a11y rules appended')

print('ALL DONE')
