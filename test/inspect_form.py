# -*- coding: utf-8 -*-
import io, re

f = r'C:\Users\AW\WorkBuddy\2026-09-07-22-49-44\beiwei30\assets\index-DDzmKV-h.js'
s = io.open(f, encoding='utf-8').read()

i = s.find('childName')
print('childName first @', i)

# form state useState init
m = re.search(r'childName:""[^}]{0,300}', s)
if m:
    print('INIT:', m.group(0)[:320])

# region around form component: find its useState
j = s.rfind('useState', 0, i)
print()
print('useState before childName:', s[j:j+400])

# state keys used via l.xxx in register component (search window)
win = s[i-3000:i+12000]
keys = set(re.findall(r'l\.([a-zA-Z]+)', win))
print()
print('l.* keys in register window:', sorted(keys))

# input/select onChange value keys
pairs = re.findall(r'([a-zA-Z]+):[a-zA-Z]\.value', win)
print('onChange keys:', sorted(set(pairs)))
