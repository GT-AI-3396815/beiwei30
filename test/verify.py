import io
NEW = "光体•北纬三十度觉醒之爱"
js = io.open(r"C:\Users\AW\WorkBuddy\2026-09-07-22-49-44\beiwei30\assets\index-DDzmKV-h.js", encoding="utf-8").read()
html = io.open(r"C:\Users\AW\WorkBuddy\2026-09-07-22-49-44\beiwei30\index.html", encoding="utf-8").read()
print("NEW occurrences in JS:", js.count(NEW))
print("NEW in index.html:", html.count(NEW))
print("hero now single-line array:", ('children:["%s"]' % NEW) in js)
print("nav label fixed:", ('children:"%s"' % NEW) in js)
print("any leftover bare brand 北纬30° (non-geographic):", js.count("北纬30°文明觉醒之爱"))
