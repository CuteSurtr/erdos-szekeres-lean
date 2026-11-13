#!/usr/bin/env python3
"""Omission bound for N(5-cap, 8-gon): real point sets, distinct x, general
position, no 5-cap, no convex octagon.

Labels d(u,v) = (E_-(u,v)-1, E_+(u,v)-1) in [1..3]x[1..6]; cap triples raise
the first coordinate, cup triples the second (attained maxima).  Incoming
states are downsets of the 3x6 grid (84 profiles), injective by state
separation.  Rows:
  * cycle rows (Lemma 2.2 check): a list whose every triple, in list order, is
    forced positive for all six chronological orders has at most 7 occupied;
  * Baek block rows: a support on which every admissible label has cap
    coordinate in a 2-set has no 4-cap, so at most 22 occupied (Baek).
Lazy separation of cycle rows inside a HiGHS MIP; the result is a lower
bound on holes, valid only together with the soundness of the rows used.
"""
import itertools, json, sys, time
import numpy as np
import highspy

import os
A, B = int(os.environ.get("CAPA", 3)), int(os.environ.get("CUPB", 6))

def profiles():
    out = []
    for f in itertools.product(range(B + 1), repeat=A):
        if all(f[i] >= f[i + 1] for i in range(A - 1)):
            out.append(f)
    out.sort(key=lambda f: (sum(f), f))
    return out

ST = profiles()
N = len(ST)
CELLS = [frozenset((a + 1, y) for a in range(A) for y in range(1, f[a] + 1)) for f in ST]

def diff(s, t):
    return CELLS[t] - CELLS[s]

nonempty = np.zeros((N, N), bool)
mn = np.zeros((2, N, N), np.int16); mx = np.zeros((2, N, N), np.int16)
for s in range(N):
    for t in range(N):
        d = diff(s, t)
        if d:
            nonempty[s, t] = True
            mn[0, s, t] = min(z[0] for z in d); mx[0, s, t] = max(z[0] for z in d)
            mn[1, s, t] = min(z[1] for z in d); mx[1, s, t] = max(z[1] for z in d)

def parity(q):
    return sum(q[i] > q[j] for i in range(3) for j in range(i + 1, 3)) % 2

def triple_ok(a, b, c):
    if len({a, b, c}) < 3:
        return False
    g = (a, b, c)
    for perm in itertools.permutations(range(3)):
        coord = 1 if parity(perm) else 0
        p, q, r = (g[perm[k]] for k in range(3))
        if not (nonempty[p, q] and nonempty[q, r] and nonempty[p, r]):
            continue
        if not (mx[coord][q, r] <= mn[coord][p, q]):
            return False
    return True

T = np.zeros((N, N, N), bool)
for a, b, c in itertools.permutations(range(N), 3):
    T[a, b, c] = triple_ok(a, b, c)

def find_cycle(occ, k=8, limit=1):
    """Lists of k occupied states, every triple in list order forced positive."""
    occ = sorted(occ)
    res = []
    def dfs(seq):
        if len(seq) == k:
            res.append(tuple(seq)); return len(res) >= limit
        for x in occ:
            if x in seq or x < seq[0]:
                continue
            if all(T[seq[i], seq[j], x] for i in range(len(seq)) for j in range(i + 1, len(seq))):
                if dfs(seq + [x]):
                    return True
        return False
    for s in occ:
        if dfs([s]):
            break
    return res

def block_supports():
    """Supports whose admissible labels use only two cap coordinates."""
    sups = []
    for keep in itertools.combinations(range(1, A + 1), 2):
        S = [s for s in range(N)
             if all(z[0] in keep for t in range(N) for z in diff(s, t) | diff(t, s)
                    if False)]
        # exact test: all labels between members avoid the excluded coordinate
        excl = [a for a in range(1, A + 1) if a not in keep]
        cand = list(range(N))
        # greedy maximal: states s such that no member pair produces excluded coord
        # (pairwise condition, so take the largest clique via simple rule below)
        ok = lambda s, t: all(z[0] not in excl for z in diff(s, t) | diff(t, s))
        # build compatibility graph and take maximum clique by networkx-free greedy
        best = []
        order = sorted(cand, key=lambda s: -sum(ok(s, t) for t in cand))
        for s in order:
            if all(ok(s, t) for t in best):
                best.append(s)
        sups.append((keep, sorted(best)))
    return sups

def solve(rows, fixed_occupied, time_limit=60):
    h = highspy.Highs(); h.silent(); h.setOptionValue('threads', 1)
    h.setOptionValue('time_limit', float(time_limit))
    inf = highspy.kHighsInf
    for i in range(N):
        lo = 0.0; hi = 0.0 if i in fixed_occupied else 1.0
        h.addVar(lo, hi)
        h.changeColCost(i, 1.0)
        h.changeColIntegrality(i, highspy.HighsVarType.kInteger)
    for sup, d in rows:
        h.addRow(float(d), inf, len(sup), np.array(sup, dtype=np.int32), np.ones(len(sup)))
    h.run()
    sol = h.getSolution().col_value
    info = h.getInfo()
    holes = [i for i in range(N) if sol[i] > 0.5]
    return holes, info.mip_dual_bound, h.getModelStatus()

if __name__ == '__main__':
    t0 = time.time()
    print('states', N, 'triples forced', int(T.sum()))
    rows = []
    for keep, sup in block_supports():
        print('block', keep, len(sup), 'demand', len(sup) - 22)
        if len(sup) > 22:
            rows.append((sup, len(sup) - 22))
    fixed = {0, ST.index(tuple([1] + [0] * (A - 1)))}  # first two vertices: empty state and down(1,1)
    it = 0
    while True:
        it += 1
        holes, bound, status = solve(rows, fixed, time_limit=120)
        occ = [i for i in range(N) if i not in holes]
        cyc = find_cycle(occ, 8, limit=40)
        print(f'it {it} rows {len(rows)} holes {len(holes)} bound {bound:.2f} status {status} new {len(cyc)} t={time.time()-t0:.0f}s', flush=True)
        if not cyc:
            break
        for c in cyc:
            rows.append((list(c), 1))
        if time.time() - t0 > float(sys.argv[1] if len(sys.argv) > 1 else 3000):
            break
    json.dump({'states': ST, 'rows': rows, 'holes': holes}, open(f'omission_A{A}_B{B}_out.json', 'w'))
    print('final holes', len(holes), 'occupied', N - len(holes))
