import io
f = r"C:\Users\AW\WorkBuddy\2026-09-07-22-49-44\beiwei30\assets\index-DDzmKV-h.js"
s = io.open(f, encoding="utf-8").read()

NEW = "光体•北纬三十度觉醒之爱"

# 1) Navbar brand short label
old_nav = 'children:"北纬30°"'
assert old_nav in s, "nav pattern not found"
s = s.replace(old_nav, 'children:"%s"' % NEW)

# 2) Hero heading split into ["北纬30°", <br>, "文明觉醒之爱"]
i = s.find('北纬30°",x.jsx("br"')
assert i != -1, "hero start not found"
start = s.rfind("children:[", 0, i)
end = s.find(']', i)
old_hero = s[start:end+1]
assert "文明觉醒之爱" in old_hero, "hero end not captured"
new_hero = 'children:["%s"]' % NEW
s = s[:start] + new_hero + s[end+1:]

io.open(f, "w", encoding="utf-8").write(s)

# verify
s2 = io.open(f, encoding="utf-8").read()
print("nav replaced:", NEW in s2)
print("hero replaced:", NEW in s2 and "北纬30°" not in s2)
print("remaining bare 北纬30° (should be geography only):")
i=0; n=0
while True:
    i=s2.find('北纬30°',i)
    if i==-1: break
    n+=1
    print("  ", s2[max(0,i-25):i+12].replace("\n"," "))
    i+=5
print("total bare 北纬30° now:", n)
print("remaining bare 文明觉醒之爱:", s2.count("文明觉醒之爱"))
