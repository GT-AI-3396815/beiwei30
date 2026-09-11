# -*- coding: utf-8 -*-
"""Sync core site files to GitHub via Contents API (bypass git push 502)."""
import io, os, sys, json, base64, urllib.request, urllib.error

TOKEN = os.environ.get('GH_TOKEN', '') or (sys.argv[1] if len(sys.argv) > 1 else '')
OWNER, REPO, BRANCH = 'GT-AI-3396815', 'beiwei30', 'main'
BASE = r'C:\Users\AW\WorkBuddy\2026-09-07-22-49-44\beiwei30'
FILES = ['index.html', 'assets/index-DDzmKV-h.js', 'assets/index-DTPUeIxS.css']

if not TOKEN:
    # read token from push.log context: ask user? fail loudly
    raise SystemExit('GH_TOKEN not provided (env or argv[1])')

API = 'https://api.github.com'

def api(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + url, data=data, method=method, headers={
        'Authorization': 'token ' + TOKEN,
        'Accept': 'application/vnd.github+json',
        'Content-Type': 'application/json',
        'User-Agent': 'workbuddy-sync',
    })
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode() or '{}')

results = {}
for path in FILES:
    st, cur = api('GET', '/repos/%s/%s/contents/%s?ref=%s' % (OWNER, REPO, path, BRANCH))
    sha = cur.get('sha') if st == 200 else None
    content = open(os.path.join(BASE, path.replace('/', os.sep)), 'rb').read()
    b64 = base64.b64encode(content).decode()
    st2, put = api('PUT', '/repos/%s/%s/contents/%s' % (OWNER, REPO, path), {
        'message': 'audit fixes: form submission, compliance wording, OG/SEO, a11y (' + path + ')',
        'content': b64,
        'sha': sha,
        'branch': BRANCH,
    })
    results[path] = ('OK' if st2 in (200, 201) else 'FAIL %s %s' % (st2, put.get('message', '')))
    print(path, '->', results[path])

if any(v.startswith('FAIL') for v in results.values()):
    raise SystemExit(1)
print('ALL SYNCED')
