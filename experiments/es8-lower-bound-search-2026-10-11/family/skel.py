import sys
sys.path.insert(0, '.')
from dp import build, combine
from math import comb
from collections import defaultdict
from functools import lru_cache
count, by_n = build()
idx = defaultdict(list)
for s in count: idx[s[0]].append(s)
def is_block(s):
    n,p,q,c = s
    return n == comb(p+q-2, p-1) and (n == 1 or c == p+q-2)
DEC = {}
def decomps(s):
    if s in DEC: return DEC[s]
    out = []
    n = s[0]
    for na in range(1, n):
        for sa in idx[na]:
            for sb in idx[n-na]:
                for d in 'UD':
                    if combine(sa, sb, d) == s:
                        out.append((d, sa, sb))
    DEC[s] = out
    return out
@lru_cache(None)
def nskel(s):
    if is_block(s): return 1
    return sum(nskel(a)*nskel(b) for d,a,b in decomps(s))
top = (64,7,7,7)
print('skeletons above maximal blocks:', nskel(top))
blocks = set()
def walk(s):
    if is_block(s): blocks.add(s); return
    for d,a,b in decomps(s): walk(a); walk(b)
walk(top)
print('block states used:', sorted(blocks))
