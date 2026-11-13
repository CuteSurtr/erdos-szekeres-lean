import sys, os, math, random
sys.path.insert(0, '.')
exec(open('generate.py').read().split("print('candidate trees:'")[0])
from collections import Counter
mag = Counter()
rows = []
seen = set()
for cat, t in cands:
    if t in seen: continue
    seen.add(t)
    b = bounds(parse(t))
    if not (b[0] == 64 and b[3] <= 7): continue
    P = realize(t)
    m = max(max(abs(x), abs(y)) for x, y in P)
    rows.append((cat, m))
import collections
for cat in dict.fromkeys(c for c, _ in rows):
    ms = sorted(m for c, m in rows if c == cat)
    within = sum(1 for m in ms if m < 2**27)
    print(f'{cat:22s} n={len(ms):5d} within2^27={within:5d} log2 min/med/max = {math.log2(ms[0]):.1f} {math.log2(ms[len(ms)//2]):.1f} {math.log2(ms[-1]):.1f}')
