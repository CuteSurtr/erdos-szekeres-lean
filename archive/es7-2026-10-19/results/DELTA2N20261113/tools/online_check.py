"""Independent cross-check of online_game.py (different code path): all valid signotopes on k = 1..depth points are
enumerated by SAT from the CNF base of eager_cert.Enc (blocking clauses); caps and convex sets come from the
4-subset definitions of siglib (brute force over subsets); the game is solved by backward induction.
usage: online_check.py a n depth weak|strong"""
import sys, itertools, time
from siglib import *
from eager_cert import Enc
from pysat.solvers import Cadical153
comb = itertools.combinations
a, n, depth, form = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
strong = form == 'strong'; t0 = time.time()
def all_valid(k):
    tris = list(comb(range(k), 3))
    if k < 3: return [()], tris
    E = Enc(a, n, k, False, base_only=True) if k >= n else None
    out = []
    if E is None:
        # fewer than n points: only signotope axioms and the a-cap condition matter; build the clauses directly
        tri = {t: i + 1 for i, t in enumerate(tris)}; cl = []
        for i, j, kk, l in comb(range(k), 4):
            s = [tri[i, j, kk], tri[i, j, l], tri[i, kk, l], tri[j, kk, l]]
            for p, q, r in comb(range(4), 3): cl.append([-s[p], s[q], -s[r]]); cl.append([s[p], -s[q], s[r]])
        for K in comb(range(k), a): cl.append([tri[K[i], K[i + 1], K[i + 2]] for i in range(a - 2)])
    else: cl = E.base
    cl = list(cl) + [[i + 1, -(i + 1)] for i in range(len(tris))]
    with Cadical153(bootstrap_with=cl) as S:
        while S.solve():
            mod = S.get_model(); sg = tuple(mod[i] > 0 for i in range(len(tris)))
            out.append(sg); S.add_clause([-mod[i] for i in range(len(tris))])
    return out, tris
levels = {}
for k in range(1, depth + 1):
    sigs, tris = all_valid(k); levels[k] = (sigs, tris)
def restrict(sg, tris, k):      # drop the last point k-1
    return tuple(v for v, t in zip(sg, tris) if t[2] != k - 1)
# children map
children = {k: {} for k in range(0, depth)}
for k in range(1, depth + 1):
    sigs, tris = levels[k]
    for sg in sigs:
        par = restrict(sg, tris, k) if k >= 1 else ()
        children[k - 1].setdefault(par, []).append(sg)
from functools import lru_cache
info = {}
def analyse(k, sg):
    key = (k, sg)
    if key not in info:
        o = dict(zip(levels[k][1], sg))
        cp = [sum(1 << i for i in K) for K in caps(o, k, a - 1) if K[-1] == k - 1] if k >= a - 1 else []
        gn = [sum(1 << i for i in G) for G in gons(o, k, n - 1) if G[-1] == k - 1] if k >= n - 1 else []
        info[key] = (cp, gn)
    return info[key]
memo = {}
def wins(k, sg, col):
    """colourer to survive from the position: k points revealed (signotope sg), Delta = col."""
    if k == depth: return True
    key = (k, sg, col)
    if key in memo: return memo[key]
    res = True
    for ch in children[k].get(sg, []):
        cp, gn = analyse(k + 1, ch); p = 1 << k; ok = False
        c1 = col | p
        if not any(c1 & K == K for K in cp) and not (strong and any(c1 & G == G for G in gn)):
            if wins(k + 1, ch, c1): ok = True
        if not ok and not any(col & G == 0 for G in gn):
            if wins(k + 1, ch, col): ok = True
        if not ok: res = False; break
    memo[key] = res
    return res
w = wins(0, (), 0)
print('online CHECK a=%d n=%d %s depth %d: %s wins; valid signotopes per size %s; %.1fs' % (a, n, form, depth, 'COLOURER' if w else 'ADVERSARY', [len(levels[k][0]) for k in range(1, depth + 1)], time.time() - t0), flush=True)
