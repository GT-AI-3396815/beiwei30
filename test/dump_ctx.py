# -*- coding: utf-8 -*-
import io
f = r'C:\Users\AW\WorkBuddy\2026-09-07-22-49-44\beiwei30\assets\index-DDzmKV-h.js'
s = io.open(f, encoding='utf-8').read()
out = io.open(r'C:\Users\AW\WorkBuddy\2026-09-07-22-49-44\beiwei30\test\ctx.txt', 'w', encoding='utf-8')
for kw in ['全透明', '可追溯', '吉尼斯认证主舞台']:
    i = 0
    while True:
        i = s.find(kw, i)
        if i == -1:
            break
        out.write('=== %s @ %d ===\n' % (kw, i))
        out.write(repr(s[max(0, i-70):i+90]) + '\n\n')
        i += len(kw)
out.close()
print('ok')
