"""Freshness of this dir's oleans (own code; bare `lean -o` tracks no dependencies): every module under lean/
N66R15{Enc,Geo,Chk} has an olean newer than its source and newer than the oleans of its local imports.
usage: python3 -I stale_check.py"""
import os, re
D = '/home/jay/research/data/formalize-20261122/n66-l15-rows/'
mods = {}
for pkg in ('N66R15Enc', 'N66R15Geo', 'N66R15Chk'):
    for f in os.listdir(D + 'lean/' + pkg):
        if f.endswith('.lean'): mods[pkg + '.' + f[:-5]] = pkg + '/' + f[:-5]
bad = 0
for m, p in sorted(mods.items()):
    src = D + 'lean/' + p + '.lean'; ol = D + 'build/olean/' + p + '.olean'
    if not os.path.exists(ol): print('NO OLEAN', m); bad += 1; continue
    t = os.path.getmtime(ol)
    if os.path.getmtime(src) > t: print('SOURCE NEWER', m); bad += 1
    for imp in re.findall(r'^import (\S+)', open(src).read(), re.M):
        if imp in mods:
            ti = os.path.getmtime(D + 'build/olean/' + mods[imp] + '.olean')
            if ti > t: print('IMPORT NEWER', m, imp); bad += 1
print(f'modules {len(mods)} problems {bad}')
