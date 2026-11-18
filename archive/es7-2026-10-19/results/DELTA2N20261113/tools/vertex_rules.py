"""Canonical-vertex rules (exhaustive on the enumerated (4,5) signotopes): Delta = {sigma(H) : H convex (n-1)-gon} for a
rule sigma choosing one vertex of every gon.  Delta meets every gon by construction; is it (a-1)-cap-free?"""
import json, collections, itertools, sys
from siglib import *
a, n = int(sys.argv[1]), int(sys.argv[2]); files = sys.argv[3:]
def split(o, G):
    u, v = G[0], G[-1]; A = [g for g in G[1:-1] if not o[u, g, v]]; B = [g for g in G[1:-1] if o[u, g, v]]
    return u, v, A, B
rules = {
 'right end': lambda o, G, r: G[-1],
 'left end': lambda o, G, r: G[0],
 'last cap vertex, else right end': lambda o, G, r: (split(o, G)[2] or [G[-1]])[-1],
 'first cap vertex, else left end': lambda o, G, r: (split(o, G)[2] or [G[0]])[0],
 'last cap vertex, else left end': lambda o, G, r: (split(o, G)[2] or [G[0]])[-1],
 'first cap vertex, else right end': lambda o, G, r: (split(o, G)[2] or [G[-1]])[0],
 'last cup vertex before right end': lambda o, G, r: (split(o, G)[3] or [G[-1]])[-1],
 'first cup vertex after left end': lambda o, G, r: (split(o, G)[3] or [G[0]])[0],
 'vertex max beta-omega (tie right)': lambda o, G, r: max(G, key=lambda p: (r[0][p] - r[1][p], p)),
 'vertex min beta-omega (tie left)': lambda o, G, r: min(G, key=lambda p: (r[0][p] - r[1][p], p)),
 'vertex min cp (tie right)': lambda o, G, r: min(G, key=lambda p: (r[3][p], -p)),
 'vertex min cm (tie left)': lambda o, G, r: min(G, key=lambda p: (r[2][p], p)),
 'vertex min cp+cm (tie right)': lambda o, G, r: min(G, key=lambda p: (r[3][p] + r[2][p], -p)),
 'vertex min cp+cm (tie left)': lambda o, G, r: min(G, key=lambda p: (r[3][p] + r[2][p], p)),
 'vertex max beta+omega (tie right)': lambda o, G, r: max(G, key=lambda p: (r[0][p] + r[1][p], p)),
 'vertex min cp, then max beta': lambda o, G, r: min(G, key=lambda p: (r[3][p], -r[0][p], -p)),
}
ok = collections.Counter(); tot = 0
for fn in files:
    m = int(fn.split('_m')[1].split('_')[0])
    for l in open(fn):
        rec = json.loads(l); o = from_str(rec['s'], m); r = ranks(o, m); G = gons(o, m, n - 1); K = [set(c) for c in caps(o, m, a - 1)]
        tot += 1
        for name, f in rules.items():
            D = {f(o, g, r) for g in G}
            if not any(k <= D for k in K): ok[name] += 1
print('(a,n)=(%d,%d): %d signotopes' % (a, n, tot))
for name, v in ok.most_common(): print('   %-36s %d / %d' % (name, v, tot))
