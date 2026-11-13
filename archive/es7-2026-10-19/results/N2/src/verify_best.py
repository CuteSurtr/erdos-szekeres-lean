#!/usr/bin/env python3
"""Exact re-check of every run's best set: general position and convex k-gon counts by
cups/caps (Python integers), triangle-criterion DFS (Python) and cgon (C angular DP),
via results/D/src/triple_check.py.  Sets claiming 0 heptagons are listed first.
usage: verify_best.py runs out.json"""
import sys, glob, json, subprocess, os
from concurrent.futures import ProcessPoolExecutor
H = os.path.dirname(os.path.abspath(__file__))
TC = os.path.join(H, '..', '..', 'D', 'src', 'triple_check.py')
def chk(fn):
    r = subprocess.run([sys.executable, TC, fn, '8'], capture_output=True, text=True)
    try: d = json.loads(r.stdout)
    except Exception: d = {'error': r.stdout[-300:] + r.stderr[-300:]}
    d['file'] = fn; return d
files = sorted(glob.glob(f'{sys.argv[1]}/*/*.best.txt'))
with ProcessPoolExecutor(4) as ex: res = list(ex.map(chk, files))
zero = [d for d in res if d.get('cups_caps', {}).get('7') == 0]
out = dict(checked=len(res), all_agree=all(d.get('agree') for d in res), all_general_position=all(d.get('general_position') for d in res),
           zero_heptagon_sets=[d['file'] for d in zero], c7_hist={}, results=res)
for d in res:
    k = str(d.get('cups_caps', {}).get('7')); out['c7_hist'][k] = out['c7_hist'].get(k, 0) + 1
json.dump(out, open(sys.argv[2], 'w'), indent=1)
print(json.dumps({k: out[k] for k in ['checked', 'all_agree', 'all_general_position', 'zero_heptagon_sets', 'c7_hist']}))
