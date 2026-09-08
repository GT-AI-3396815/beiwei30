import io, sys
files = [
    r"C:\Users\AW\WorkBuddy\2026-09-07-22-49-44\beiwei30\index.html",
    r"C:\Users\AW\WorkBuddy\2026-09-07-22-49-44\beiwei30\assets\index-DDzmKV-h.js",
]
OLD = "北纬30°文明觉醒之爱"
NEW = "光体•北纬三十度觉醒之爱"

for f in files:
    with io.open(f, "r", encoding="utf-8") as fh:
        s = fh.read()
    before = s.count(OLD)
    s2 = s.replace(OLD, NEW)
    after = s2.count(OLD)
    with io.open(f, "w", encoding="utf-8") as fh:
        fh.write(s2)
    print(f"{f.split(chr(92))[-1]}: replaced {before} -> left {after}")

# audit: report every remaining 北纬30° context to confirm geography-only
print("\n=== remaining 北纬30° contexts (should be geography only) ===")
for f in files:
    with io.open(f, "r", encoding="utf-8") as fh:
        s = fh.read()
    idx = 0
    while True:
        i = s.find("北纬30°", idx)
        if i == -1:
            break
        ctx = s[i:i+28].replace("\n"," ")
        print(f"  [{f.split(chr(92))[-1]}] ...{ctx}...")
        idx = i + 1
